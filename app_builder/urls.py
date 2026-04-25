from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    
    # Halkan u fiirso: Waa inuu jiri koodhka hoose iyo comma dhamaadka midka sare
    path('', lambda request: redirect('login')), 
]

# Khadkan hoose isna waa muhiim:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)