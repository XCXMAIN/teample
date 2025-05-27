import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_image_features(image_paths):
    images = [preprocess(Image.open(p).convert("RGB")) for p in image_paths]
    image_input = torch.stack(images).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    return image_features

def search_images(text, image_paths, top_k=5):
    image_features = get_image_features(image_paths)
    with torch.no_grad():
        text_tokens = clip.tokenize([text]).to(device)
        text_features = model.encode_text(text_tokens)
        similarity = (text_features @ image_features.T).squeeze(0)
        top_indices = similarity.topk(top_k).indices
        return [image_paths[i] for i in top_indices]
