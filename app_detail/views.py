import zipfile
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from create_app.models import App

def app_detail(request, slug):
    app = get_object_or_404(App, slug=slug)
    return render(request, 'app_detail/app_detail.html', {'app': app})

def download_app(request, slug):
    app = get_object_or_404(App, slug=slug)
    buffer = BytesIO()
    safe_name = slugify(app.name)

    with zipfile.ZipFile(buffer, 'w') as zip_file:
        html_content = f"<!DOCTYPE html>\n<html>\n<head>\n<title>{app.name}</title>\n<link rel='stylesheet' href='style.css'>\n</head>\n<body>\n{app.html_code}\n<script src='script.js'></script>\n</body>\n</html>"
        zip_file.writestr("index.html", html_content)
        zip_file.writestr("style.css", app.css_code or "")
        zip_file.writestr("script.js", app.js_code or "")
        zip_file.writestr("README.txt", f"App Name: {app.name}\nDeveloper: {app.owner.username}")

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={safe_name}.zip'

    return response