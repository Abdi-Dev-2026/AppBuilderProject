from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),

    # 2. Dhammaan dariiqyada App-ka Core
    path('', include('core.urls')), 
    path('', include('exam_app.urls')), # <-- Khadkan ku dar saaxiib
]

# Faylasha Media iyo Static waxay shaqaynayaan marka DEBUG=True la joogo (Local Development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)