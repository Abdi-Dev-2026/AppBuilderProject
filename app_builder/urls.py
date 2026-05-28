# app_builder/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Admin Panel-ka rasmiga ah ee Django
    path('admin/', admin.site.urls),
    
    # 2. Khadadka (URLs) ee dhammaan 20-ka Apps ee madaxa-bannaan
    path('', include('homepage.urls')),                  # Bogga weyn ee ugu horreeya ee shaqada
    path('about/', include('about.urls')),                # Bogga ku saabsan nidaamka
    path('app-detail/', include('app_detail.urls')),      # Faahfaahinta app-ka la dhisay
    path('banaadir/', include('banaadir.urls')),          # Nidaamka Imtixaanka Banaadir
    path('chat-window/', include('chat_window.urls')),    # Daaqada weyn ee wada sheekaysiga
    path('chats/', include('chats.urls')),                # Liiska sheekooyinka u furan
    path('contact/', include('contact.urls')),            # Bogga xiriirka iyo fariimaha
    path('content/', include('content.urls')),            # Qaybta maareynta nuxurka (Content)
    path('create-app/', include('create_app.urls')),      # Bogga lagu abuuro app-ka cusub
    path('dashboard/', include('dashboard.urls')),        # Control Panel-ka guud ee isticmaalaha
    path('editor/', include('editor.urls')),              # Editor-ka dhismaha (App Builder Studio)
    path('login/', include('login.urls')),                # Bogga soo gelidda akaount-ka
    path('maintenance/', include('maintenance.urls')),    # Bogga cilad-bixinta/Under Construction
    path('messages/', include('my_messages.urls')),      # Fariimaha khaaska ah ee u dhexeeya dadka
    path('poll/', include('poll.urls')),                  # Codeynta iyo ra'yi ururinta
    path('profile/', include('profile_html.urls')),       # Profile-ka guud ee qofka
    path('quiz/', include('quiz.urls')),                  # Kediska iyo su'aalaha caqliga
    path('register/', include('register.urls')),          # Bogga iska-diiwaangelinta cusub
    path('result/', include('result.urls')),              # Natiijooyinka imtixaanka ee dugsiyada
    path('tts/', include('tts_interface.urls')),          # Interface-ka codka (Text-to-Speech)
]

# Faylasha Media iyo Static waxay shaqaynayaan marka DEBUG=True la joogo (Local Development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)