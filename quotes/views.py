import os
import json
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .quote_image_generator import QuoteImageGenerator  # Import your generator class

def upload_quotes(request):
    if request.method == 'POST' and request.FILES['quotes_file']:
        quotes_file = request.FILES['quotes_file']
        fs = FileSystemStorage()
        filename = fs.save(quotes_file.name, quotes_file)
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Initialize the quote image generator with the uploaded file
        authors_dir = os.path.join(settings.MEDIA_ROOT, 'authors')  # Path for authors' images
        output_dir = os.path.join(settings.MEDIA_ROOT, 'output')    # Path for generated images
        
        # Set paths for font files
        font_quote_path = os.path.join(settings.BASE_DIR, "fonts", "SuezOne-Regular.ttf")  # Path to quote font
        font_author_path = os.path.join(settings.BASE_DIR, "fonts", "SuezOne-Regular.ttf")  # Path to author font

        try:
            generator = QuoteImageGenerator(uploaded_file_path, authors_dir, output_dir, font_quote_path, font_author_path)
            generator.generate_images()
            return redirect('success')  # Redirect to a success page
        except Exception as e:
            print(f"Error generating images: {e}")  # Log the error (optional)
            return render(request, 'quotes/failed.html', {'error': str(e)})

    return render(request, 'quotes/upload.html')

def success(request):
    return render(request, 'quotes/success.html')

def failed(request):
    return render(request, 'quotes/failed.html')  # Render the failed template
