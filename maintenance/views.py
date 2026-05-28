from django.shortcuts import render
from homepage.models import SiteSetting  # Halka uu rabo model-ku ha noqdo

def maintenance(request):
    setting = SiteSetting.objects.first()
    return render(request, 'maintenance/maintenance.html', {'setting': setting})