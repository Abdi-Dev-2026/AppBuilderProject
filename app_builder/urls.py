# app_builder/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # Khadkan ku dar
from django.conf import settings
from django.conf.urls.static import static

# 🔥 HALKAN WAXAAN KAGA LABA-BAXNAY NAMEERROR-KII:
# Waxaan si toos ah u soo dhoofsanaynaa views-ka ka dhex shaqaynaya app-ka 'login'
from login import views as login_views 

urlpatterns = [
    # 1. Admin Panel-ka rasmiga ah ee Django
    path('admin/', admin.site.urls),
    
    # 2. Khadadka (URLs) ee dhammaan Apps-ka madaxa-bannaan
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
    path('login/', include('login.urls')),                # Bogga soo gelidda ee habaysan
    path('maintenance/', include('maintenance.urls')),    # Bogga cilad-bixinta/Under Construction
    path('messages/', include('my_messages.urls')),      # Fariimaha khaaska ah ee u dhexeeya dadka
    path('poll/', include('poll.urls')),                  # Codeynta iyo ra'yi ururinta
    path('profile/', include('profile_html.urls')),       # Profile-ka guud ee qofka
    path('quiz/', include('quiz.urls')),                  # Kediska iyo su'aalaha caqliga
    path('register/', include('register.urls')),          # Bogga iska-diiwaangelinta cusub
    path('result/', include('result.urls')),              # Natiijooyinka imtixaanka ee dugsiyada
    path('keep-notes/', include('keep_notes.urls')),      # App-ka cusub ee Keep Notes
    path('tts/', include('tts_interface.urls')),          # Interface-ka codka (Text-to-Speech)
    
    # 🔥 HALKAN KA ARY LOGOUT-KA SI UU SIGN OUT-KU U SHAQEEEYO:
    path('logout/', login_views.logout_view, name='logout'),
    path('ai/', include('maxamed_Ai.urls')),  # Xariiqan ka dhig mid shaqaynaya
    path('games/', include('maxamed_game.urls')),
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js'),
]

# Faylasha Media iyo Static waxay shaqaynayaan marka DEBUG=True la joogo (Local Development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)