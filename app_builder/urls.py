from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # Hubi inuu yahay .urls
    path('', include('core.urls')),
]

# Tani waxay muhiim u tahay in sawirrada iyo static-ka ay shaqeeyaan xilliga DEBUG-ta
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)