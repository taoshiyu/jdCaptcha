from fastapi import FastAPI, UploadFile
import shutil
from infer import similarity

app = FastAPI()

@app.post("/similarity")
async def compare(img1: UploadFile, img2: UploadFile):
    with open("a.png", "wb") as f:
        shutil.copyfileobj(img1.file, f)
    with open("b.png", "wb") as f:
        shutil.copyfileobj(img2.file, f)
    score = similarity("a.png", "b.png")
    return {"similarity": score}
