from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('banaadir/', views.banaadir_view, name='banaadir'),

    # ---------------------------------------------------
    # 🌍 1. PUBLIC PAGES
    # ---------------------------------------------------
    path('', views.home, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('content/', views.content_page, name='content'),
    path('maintenance/', views.maintenance, name='maintenance'),

    # ---------------------------------------------------
    # 🔐 2. AUTH SYSTEM
    # ---------------------------------------------------
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ---------------------------------------------------
    # 👤 3. PROFILE SYSTEM
    # ---------------------------------------------------
    path('profile/', views.profile, name='profile'),

    # ---------------------------------------------------
    # 🪪 4. ID CARD SYSTEM (PDF DOWNLOAD)
    # ---------------------------------------------------
    path('id-card/download/', views.download_id_card, name='download_id_card'),

    # ---------------------------------------------------
    # 🧩 5. APP BUILDER SYSTEM
    # ---------------------------------------------------
    path('create-app/', views.create_app, name='create_app'),
    path('edit-code/<int:app_id>/', views.edit_code, name='edit_code'),
    path('app/<slug:slug>/', views.app_detail, name='app_detail'),
    path('download/<slug:slug>/', views.download_app, name='download_app'),

    # ---------------------------------------------------
    # 💬 6. MESSAGES SYSTEM & CHAT (MUCJISADA)
    # ---------------------------------------------------
    path('my-messages/', views.my_messages, name='my_messages'),
   
    # --- MUCJISADA CHAT SYSTEM ROUTES ---
    path('chats/', views.chats_page, name='chats_page'),
    path('chats/request/<int:profile_id>/', views.send_friend_request, name='send_friend_request'),
    path('chats/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    # Kani waa kii aad codsatay in lagu daro:
    path('chats/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('chats/t/<str:username>/', views.chat_with_user, name='chat_with_user'),

    # ---------------------------------------------------
    # 🧠 7. QUIZ SYSTEM
    # ---------------------------------------------------
    path('quiz/', views.quiz_page, name='quiz_page'),
    path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('reset-quiz/', views.reset_quiz, name='reset_quiz'),

    # ---------------------------------------------------
    # 📊 8. POLL SYSTEM
    # ---------------------------------------------------
    path('poll/', views.poll_page, name='poll_page'),
    path('vote/<int:poll_id>/', views.vote_poll, name='vote_poll'),

    # ---------------------------------------------------
    # ❤️ 9. SOCIAL FEATURES
    # ---------------------------------------------------
    path('like/<int:content_id>/', views.like_content, name='like_content'),
    path('comment/<int:content_id>/', views.add_comment, name='add_comment'),
    # urls.py dhexdiisa ka dhig:
    path('imtixaanka/', views.banaadir_view, name='exam_view'),
    path('tts/', views.tts_interface_view, name='tts_interface'),
]

# ---------------------------------------------------
# 📁 MEDIA FILES (IMAGE & VIDEO CODSIGA)
# ---------------------------------------------------
# Habayntaan waxay suurtogal ka dhigaysaa in sawirrada iyo muuqaallada
# aad Admin-ka ka soo geliso laga furo Browser-ka xilliga horumarinta (Development).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
