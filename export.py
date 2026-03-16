# export.py
import torch
import torch.nn as nn
from model import SiameseNet

device = "cuda" if torch.cuda.is_available() else "cpu"

# ---------------------------------------------
# 1️⃣ 包装 forward_once，保证 torch.onnx.export 可以接受 nn.Module
# ---------------------------------------------
class ForwardOnceWrapper(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x):
        return self.model.forward_once(x)


# ---------------------------------------------
# 2️⃣ 加载模型权重
# ---------------------------------------------
model = SiameseNet().to(device)
checkpoint_path = "checkpoints/siamese.pth"
model.load_state_dict(
    torch.load(checkpoint_path, map_location=device, weights_only=True)
)
model.eval()

# 包装 forward_once
model_wrap = ForwardOnceWrapper(model).to(device)
model_wrap.eval()

# ---------------------------------------------
# 3️⃣ 准备 dummy 输入
# ---------------------------------------------
# 你的训练 transform 输入是 100×100
dummy_input = torch.randn(1, 3, 100, 100).to(device)

# ---------------------------------------------
# 4️⃣ 导出 ONNX
# ---------------------------------------------
onnx_path = "checkpoints/siamese.onnx"
torch.onnx.export(
    model_wrap,                   # nn.Module 对象
    dummy_input,                  # dummy input
    onnx_path,                     # 输出路径
    input_names=["input"],         # 输入名
    output_names=["embedding"],    # 输出名
    dynamic_axes={
        "input": {0: "batch_size"},      # batch 可变
        "embedding": {0: "batch_size"}   # 输出 batch 可变
    },
    opset_version=18                 # 使用最新稳定 opset
)

print(f"ONNX 模型导出完成: {onnx_path}")