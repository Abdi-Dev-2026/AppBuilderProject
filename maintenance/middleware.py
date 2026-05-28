from django.shortcuts import redirect

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Admin-ka, Static files-ka iyo Media-ha iska daa ha shaqeeyaan mar kasta
        if request.path.startswith('/admin') or request.path.startswith('/static') or request.path.startswith('/media'):
            return self.get_response(request)

        # 2. XALKA CILADDA: Waxaan halkan ku dhex import-gareynaynaa model-ka
        # Tani waxay ka hortagaysaa "AppRegistryNotReady: Apps aren't loaded yet."
        from homepage.models import SiteSetting

        # 3. Soo jiid xogta maintenance-ka ee ku jirta homepage settings
        setting = SiteSetting.objects.first()

        if setting and setting.maintenance_mode:
            # Haddii uu qofku rabo inuu aado bogga maintenance-ka iska daa, haddii kale u leexi (redirect)
            if request.path != '/maintenance/':
                return redirect('maintenance_view')
                
        return self.get_response(request)