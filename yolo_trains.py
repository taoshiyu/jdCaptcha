from ultralytics import YOLO

# 加载模型
model = YOLO("yolov8n.pt")

# 自定义超参数（你之前 hyp_captcha.yaml 内容转成字典）
hyp = {
    "hsv_h": 0.0,
    "hsv_s": 0.0,
    "hsv_v": 0.0,
    "degrees": 0.0,
    "translate": 0.0,
    "scale": 0.0,
    "shear": 0.0,
    "perspective": 0.0,
    "flipud": 0.0,
    "fliplr": 0.0,
    "mosaic": 0.0,
    "mixup": 0.0,
    "copy_paste": 0.0
}

# 开始训练，支持 resume
model.train(
    data="data/captcha.yaml",
    epochs=100,
    imgsz=320,
    batch=16,
    device='cpu',
    name="captcha_run",
    exist_ok=True,
    # resume=True,
    **hyp
)
