from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .logic.extract import extract_text_from_pdf, generate_medical_chronology
from .logic.pneumonia_detector import detect_pneumonia_local
from PIL import Image
from .logic.skin_detect import classify_image 

import os

UPLOAD_FOLDER = settings.MEDIA_ROOT  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def upload_form(request):
    return render(request, "upload.html")

def index(request):
    return render(request, 'index.html')

def chatbot(request):
    return render(request, 'chatbot.html')


@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("pdf")
        if not file:
            return HttpResponse("No file uploaded", status=400)

        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        text = extract_text_from_pdf(file_path)
        chronology = generate_medical_chronology(text)

        return render(request, "result.html", {"summary": chronology})

    return HttpResponse("Method Not Allowed", status=405)

@csrf_exempt
def download_json(request):
    if request.method == "POST":
        summary = request.POST.get("summary", "")
        response = HttpResponse(summary, content_type="application/json")
        response["Content-Disposition"] = 'attachment; filename="summary.json"'
        return response
    return HttpResponse("Method Not Allowed", status=405)

# ----------------------------
# Pneumonia detector
# ----------------------------

def pneumonia_page(request):
    return render(request, "pneumonia-upload.html")  

@csrf_exempt
def upload_xray(request):
    if request.method == "POST":
        image = request.FILES.get("xray")
        if not image:
            return HttpResponse("No image uploaded", status=400)

        file_path = os.path.join(settings.MEDIA_ROOT, image.name)
        with open(file_path, "wb+") as destination:
            for chunk in image.chunks():
                destination.write(chunk) 

        result = detect_pneumonia_local(file_path)  

        image_url = settings.MEDIA_URL + image.name  # <-- this line matters
        return render(request, "pneumonia-result.html", {
    "result": result,
    "image_path": image_url
})
    
# ----------------------------
# Skin cancer detector
# ----------------------------



@csrf_exempt
def skin_classifier(request):
    label = None
    confidence = None

    if request.method == 'POST' and request.FILES.get("image"):
        image = Image.open(request.FILES["image"]).convert("RGB")
        label, confidence = classify_image(image)

    return render(request, "skin_detect.html", {
        "label": label,
        "confidence": confidence
    })
