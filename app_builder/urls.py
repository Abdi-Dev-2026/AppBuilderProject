from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),

    # 2. Dhammaan dariiqyada App-ka Core (wax kasta halkan ayay galaan)
    path('', include('core.urls')), 
]

# Faylasha Media iyo Static si ay sawirrada u soo baxaan
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)