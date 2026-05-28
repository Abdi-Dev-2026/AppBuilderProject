from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from create_app.models import App  # Ama App_detail model meeshii uu jiro

@login_required
def dashboard(request):
    apps = App.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'dashboard/dashboard.html', {'apps': apps})