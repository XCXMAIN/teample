from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import torch
import clip
import io

app = FastAPI()

# CORS 설정 (필요 시)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CLIP 모델 로드
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# 분류 후보 텍스트
text_labels = ["에어컨", "냉장고", "세탁기", "청소기", "컴퓨터"]

@app.post("/predict/")
async def predict(file: UploadFile = File(...), user_text: str = Form(...)):
    # 이미지 로드
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # 전처리 및 이미지 임베딩
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)

    # 텍스트 임베딩
    text_inputs = clip.tokenize(text_labels).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_inputs)

    # 유사도 계산
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

    top_index = similarity.argmax().item()
    top_label = text_labels[top_index]
    confidence = similarity[0][top_index].item()

    return {
        "prediction": top_label,
        "confidence": round(confidence, 3),
        "user_text": user_text
    }
