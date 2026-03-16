import torch
from PIL import Image
import torchvision.transforms as T
from model import SiameseNet
from io import BytesIO
import onnxruntime as ort
from utils.decrators import timer
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"

model = SiameseNet().to(device)
model.load_state_dict(torch.load("checkpoints/siamese.pth", map_location=device,weights_only=False))
model.eval()


session = ort.InferenceSession("checkpoints/siamese.onnx")

transform = T.Compose([
    T.Resize((100, 100)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
])

def embed(img_path):
    img = transform(Image.open(img_path).convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        return model.forward_once(img)

def embed_content(img):
    img = transform(img.convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        return model.forward_once(img)

def similarity(img1, img2):
    e1 = embed(img1)
    e2 = embed(img2)
    return float((e1 @ e2.T).item())

@timer
def similarity_content(img1_content, img2_content):
    e1 = embed_content(img1_content)
    e2 = embed_content(img2_content)
    return float((e1 @ e2.T).item())

def embed_onnx(img_path):
    img = transform(Image.open(img_path).convert("RGB")).unsqueeze(0).numpy()
    outputs = session.run(None, {"input": img})
    return outputs[0]  # shape (1, embedding_dim)

def embed_onnx_content(img):
    img = transform(img.convert("RGB")).unsqueeze(0).numpy()
    outputs = session.run(None, {"input": img})
    return outputs[0]


def similarity_onnx(img1, img2):
    e1 = embed_onnx(img1)
    e2 = embed_onnx(img2)
    return float(np.dot(e1, e2.T))

@timer
def similarity_onnx_content(img1_content, img2_content):
    e1 = embed_onnx_content(img1_content)
    e2 = embed_onnx_content(img2_content)
    return float(np.dot(e1, e2.T))

if __name__ == "__main__":
    with open('data/pairs.txt', 'r') as f:
        ls = f.readlines()
        for l in ls:
            b1,b2,s = l.strip().split()
            s_ = similarity_onnx(b1,b2)
            print(f"{b1} {b2} {s} {s_:.4f}")
            s_ = similarity(b1,b2)
            print(f"{b1} {b2} {s} {s_:.4f}")
