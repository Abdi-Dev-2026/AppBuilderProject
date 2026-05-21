from django.shortcuts import redirect
from django.urls import reverse
from .models import SiteSetting

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Ka dhowr maamulka, static-ga iyo media-ha
        if request.path.startswith('/admin') or request.path.startswith('/static') or request.path.startswith('/media'):
            return self.get_response(request)

        # Staff-ka iyo Superuser-ka ha u deynin maintenance-ka si ay u tijaabin karaan bogga
        if request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)

        setting = SiteSetting.objects.first()

        if setting and setting.maintenance_mode:
            # 2. Xalka dynamic-ga ah si looga fogaado loop-ka:
            try:
                maintenance_url = reverse('maintenance')
                if request.path != maintenance_url:
                    return redirect('maintenance')
            except Exception:
                # Haddii url-ka maintenance la waayo, koodhku yuusan hakin
                pass

        return self.get_response(request)