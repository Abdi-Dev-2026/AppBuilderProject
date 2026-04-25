from django.shortcuts import redirect
from .models import SiteSetting

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin') or request.path.startswith('/static') or request.path.startswith('/media'):
            return self.get_response(request)

        setting = SiteSetting.objects.first()

        if setting and setting.maintenance_mode:
            if request.path != '/maintenance/':
                return redirect('maintenance')

        return self.get_response(request)