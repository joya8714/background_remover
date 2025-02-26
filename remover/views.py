from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from rembg import remove
from PIL import Image
import io
import os

def index(request):
    return render(request, 'remover/index.html')

def process_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Handle uploaded file
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        input_path = fs.save(uploaded_file.name, uploaded_file)

        # Remove background
        input_image_path = fs.path(input_path)
        output_image_path = f"media/output_{uploaded_file.name}"
        
        with open(input_image_path, "rb") as f:
            input_image = f.read()
        output_image_data = remove(input_image)
        
        with open(output_image_path, "wb") as f:
            f.write(output_image_data)

        return render(request, 'remover/result.html', {'output_file': f"output_{uploaded_file.name}"})
    return render(request, 'index.html')

def download_image(request, filename):
    output_path = os.path.join('media', filename)
    if os.path.exists(output_path):
        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("File not found")

# Create your views here.
