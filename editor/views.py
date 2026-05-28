from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from create_app.models import App

@login_required
def edit_code(request, app_id):
    app = get_object_or_404(App, id=app_id, owner=request.user)

    if request.method == 'POST':
        app.html_code = request.POST.get('html_code', '')
        app.css_code = request.POST.get('css_code', '')
        app.js_code = request.POST.get('js_code', '')
        app.save()

        django_messages.success(request, "Isbeddelka waa la save-gareeyay ✅")
        return redirect('dashboard')

    return render(request, 'editor/editor.html', {'app': app})