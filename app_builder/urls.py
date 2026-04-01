from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Hubi in halkan ay ku qoran tahay .urls (ee aysan ahayn .py)
    path('admin/', admin.site.urls), 
    path('', include('core.urls')),
]

# Tani waxay muhiim u tahay in sawirrada (Icons) iyo faylasha Media-ga ay shaqeeyaan
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)