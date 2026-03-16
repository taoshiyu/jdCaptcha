import base64
import io
from pathlib import Path
from typing import Union

import cv2
import numpy as np
import onnxruntime as ort
import torch
from PIL import Image
from ultralytics import YOLO
from ultralytics.utils.ops import scale_boxes
from ultralytics.utils.nms import non_max_suppression
from ultralytics.data.augment import LetterBox
import torch

from utils.decrators import timer


class YoloDetector:
    def __init__(
            self,
            weights: str,
            imgsz: int = 320,
            device: int | str = 'cpu',
            conf: float = 0.25
    ):
        """
        YOLO 推理封装
        """
        print('detector started')
        self.model = YOLO(weights)
        self.imgsz = imgsz
        self.device = device
        self.conf = conf

        # 类名
        self.names = self.model.names

    def _load_img(self, src: Union[Path, str, bytes, Image.Image]) -> np.ndarray:
        # 1️⃣ 图片路径
        if isinstance(src, (str, Path)) and Path(src).exists():
            return str(src)

        # 2️⃣ bytes
        if isinstance(src, (bytes, bytearray)):
            return np.array(Image.open(io.BytesIO(src)).convert("RGB"))

        # 3️⃣ base64
        if isinstance(src, str):
            try:
                # 兼容 data:image/jpeg;base64,xxxx
                if "," in src:
                    src = src.split(",", 1)[1]
                img_bytes = base64.b64decode(src)
                return np.array(Image.open(io.BytesIO(img_bytes)).convert("RGB"))
            except Exception:
                pass
        if isinstance(src, Image.Image):
            return np.array(src)
        raise ValueError("Unsupported image input type")

    @timer
    @torch.no_grad()
    def detect(self, src: Union[Path, str, bytes, Image.Image]):
        """
        对单张图片进行检测
        返回：list[dict]
        """
        src = self._load_img(src)

        results = self.model.predict(
            source=src,
            imgsz=self.imgsz,
            conf=self.conf,
            device=self.device,
            verbose=False
        )

        detections = []

        if not results:
            return detections

        r = results[0]
        if r.boxes is None:
            return detections

        boxes = r.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            cls_name = self.names[cls_id]

            detections.append({
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "conf": round(conf, 4),
                "cls": cls_id,
                "cls_name": cls_name
            })

        return detections


class YoloOnnxDetector:

    def __init__(
            self,
            weights: str,
            imgsz: int = 320,
            conf: float = 0.25
    ):
        print("detector started (ONNX)")

        self.imgsz = imgsz
        self.conf = conf

        self.session = ort.InferenceSession(
            weights,
            providers=["CPUExecutionProvider"]
        )

        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [o.name for o in self.session.get_outputs()]

        # 类名 (如果有)
        self.names = {0: "captcha"}

    # ------------------------
    # 图片加载
    # ------------------------
    def _load_img(self, src: Union[Path, str, bytes, Image.Image]) -> np.ndarray:

        if isinstance(src, (str, Path)) and Path(src).exists():
            return cv2.imread(str(src))

        if isinstance(src, (bytes, bytearray)):
            return np.array(Image.open(io.BytesIO(src)).convert("RGB"))

        if isinstance(src, str):
            try:
                if "," in src:
                    src = src.split(",", 1)[1]
                img_bytes = base64.b64decode(src)
                return np.array(Image.open(io.BytesIO(img_bytes)).convert("RGB"))
            except Exception:
                pass

        if isinstance(src, Image.Image):
            return np.array(src)

        raise ValueError("Unsupported image input type")

    # ------------------------
    # 预处理
    # ------------------------
    def _preprocess(self, img):

        img = cv2.resize(img, (self.imgsz, self.imgsz))

        img = img[:, :, ::-1]  # BGR → RGB
        img = img.transpose(2, 0, 1)

        img = img.astype(np.float32) / 255.0

        img = np.expand_dims(img, axis=0)

        return img

    # ------------------------
    # YOLO NMS
    # ------------------------
    def _postprocess(self, preds):

        detections = []

        pred = preds[0]

        pred = np.transpose(pred, (0, 2, 1))[0]  # (8400, 84)

        boxes = pred[:, :4]
        scores = pred[:, 4:]

        cls_ids = np.argmax(scores, axis=1)
        cls_scores = scores[np.arange(len(scores)), cls_ids]

        mask = cls_scores > self.conf

        boxes = boxes[mask]
        cls_scores = cls_scores[mask]
        cls_ids = cls_ids[mask]

        for box, conf, cls_id in zip(boxes, cls_scores, cls_ids):
            x, y, w, h = box

            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)

            detections.append({
                "bbox": [x1, y1, x2, y2],
                "conf": float(conf),
                "cls": int(cls_id),
                "cls_name": self.names.get(int(cls_id), str(cls_id))
            })

        return detections



    @timer
    def detect(self, src):

        img0 = self._load_img(src)

        # 1 letterbox (和YOLO一致)
        letterbox = LetterBox(self.imgsz)
        img = letterbox(image=img0)

        img = img.transpose(2, 0, 1)[::-1]
        img = np.ascontiguousarray(img)

        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, 0)

        # 2 ONNX forward
        preds = self.session.run(
            None,
            {self.input_name: img}
        )[0]

        preds = torch.from_numpy(preds)

        # 3 NMS
        preds = non_max_suppression(
            preds,
            self.conf,
            0.45
        )

        detections = []

        if preds[0] is None:
            return detections

        # 4 scale bbox 到原图
        preds[0][:, :4] = scale_boxes(
            img.shape[2:],
            preds[0][:, :4],
            img0.shape
        )

        for box in preds[0]:
            x1, y1, x2, y2, conf, cls_id = box.tolist()

            detections.append({
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "conf": round(conf, 4),
                "cls": int(cls_id),
                "cls_name": self.names[int(cls_id)]
            })

        return detections


if __name__ == "__main__":
    def run():
        detector = YoloDetector(
            weights="runs/detect/captcha_run/weights/best.pt",
        )
        result = detector.detect('data/images/test/b1_1769073894137.png')
        print(result)

    def run_onnx():
        detector = YoloOnnxDetector(
            weights="runs/detect/captcha_run/weights/best.onnx",
        )
        result = detector.detect('data/images/test/b1_1769073894137.png')
        print(result)

    run()
    run_onnx()
