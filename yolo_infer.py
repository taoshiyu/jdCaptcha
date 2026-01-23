from ultralytics import YOLO
import torch
from pathlib import Path
from PIL import Image
import numpy as np
import base64
import io
from typing import Union

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
        self.model = YOLO(weights)
        self.imgsz = imgsz
        self.device = device
        self.conf = conf

        # 类名
        self.names = self.model.names

    def _load_img(self,src:Union[Path,str,bytes,Image.Image]) -> np.ndarray:
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

    @torch.no_grad()
    def detect(self, src: Union[Path,str,bytes,Image.Image]):
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


if __name__ == "__main__":
    detector = YoloDetector(
        weights="runs/detect/captcha_run/weights/best.pt",
    )
    result = detector.detect('data/images/test/b1_1769073894137.png')
    print(result)
