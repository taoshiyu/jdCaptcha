from ultralytics import YOLO
from pathlib import Path

# 配置
WEIGHTS_PATH = "runs/detect/captcha_run/weights/best.pt"
TEST_IMAGES = Path("data/images/test")
TEST_LABELS = Path("data/labels/test")
SAVE_DIR = Path("data/test_results")
SAVE_DIR.mkdir(parents=True, exist_ok=True)
SHOW_IMG = False

model = YOLO(WEIGHTS_PATH)

# 检查是否有 label
has_labels = any(TEST_LABELS.glob("*.txt"))

if has_labels:
    print("✅ Test set contains labels, computing metrics...")
    # 使用 yaml 的 test 集
    results = model.val(
        data="data/captcha.yaml",   # 你原来的 yaml
        split="test",          # 用 test 集
        save=True,
        save_dir=str(SAVE_DIR),
        show=SHOW_IMG,
        imgsz=320,
        batch=16
    )

    print("\n===== Test Set Metrics =====")
    print(f"Precision: {results.precision:.4f}")
    print(f"Recall   : {results.recall:.4f}")
    print(f"mAP@0.5  : {results.map50:.4f}")
    print(f"mAP@0.5:0.95 : {results.map50_95:.4f}")
    print("============================\n")

else:
    print("⚠️ Test set has no labels, only generating predictions...")
    results = model.predict(
        source=str(TEST_IMAGES),
        save=True,
        save_dir=str(SAVE_DIR),
        show=SHOW_IMG,
        imgsz=320,
        batch=16
    )
    print(f"Predictions saved to {SAVE_DIR}")
