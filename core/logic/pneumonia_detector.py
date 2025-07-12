from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

# Load model and processor once
processor = AutoImageProcessor.from_pretrained("lxyuan/vit-xray-pneumonia-classification")
model = AutoModelForImageClassification.from_pretrained("lxyuan/vit-xray-pneumonia-classification")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

def detect_pneumonia_local(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    predicted_class = model.config.id2label[predicted_class_idx]
    confidence = torch.nn.functional.softmax(logits, dim=1)[0][predicted_class_idx].item()

    return {
        "label": predicted_class,
        "confidence": round(confidence * 100, 2)
    }