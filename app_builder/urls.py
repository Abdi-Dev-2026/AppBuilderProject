from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views  # Soo dhoweynta views-ka core

urlpatterns = [
    # 1. Homepage & Interactive Features
    # Waxaan u beddelay 'views.home' maadaama views.py ay saas ku qoran tahay
    path('', views.home, name='home'), 
    
    path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('vote/<int:poll_id>/', views.vote_poll, name='vote_poll'),
    
    # --- Like & Comment Paths ---
    path('like/<int:content_id>/', views.like_content, name='like_content'),
    path('comment/<int:content_id>/', views.add_comment, name='add_comment'),

    # 2. Admin Panel
    path('admin/', admin.site.urls),

    # 3. Core URLs (Login, Register, Dashboard, Code Editor, etc.)
    # Fadlan hubi in 'core.urls' aysan ku celinayn path-ka ('') si uusan isku dhac u imaan
    path('', include('core.urls')), 
]

# Faylasha Media iyo Static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)