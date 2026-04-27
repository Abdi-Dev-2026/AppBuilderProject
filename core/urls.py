from django.urls import path
from . import views

urlpatterns = [
    # 1. BOGAGGA GUUD (Public Pages)
    path('', views.home, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('content/', views.content_page, name='content'),
    path('maintenance/', views.maintenance, name='maintenance'),

    # 2. XUBNAHA & AMAANKA (Auth & Dashboard)
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # 3. DHISMAHA APP-KA (App Builder)
    path('create-app/', views.create_app, name='create_app'),
    path('edit-code/<int:app_id>/', views.edit_code, name='edit_code'),
    path('app/<slug:slug>/', views.app_detail, name='app_detail'),
    path('download/<slug:slug>/', views.download_app, name='download_app'),

    # 4. INTERACTIVE FEATURES (Quiz, Poll, Like, Comment)
    path('quiz/', views.quiz_page, name='quiz_page'),
    path('poll/', views.poll_page, name='poll_page'),
    path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('reset-quiz/', views.reset_quiz, name='reset_quiz'),  # Kani waa kii dhimnaa saaxiib
    path('vote/<int:poll_id>/', views.vote_poll, name='vote_poll'),
    path('like/<int:content_id>/', views.like_content, name='like_content'),
    path('comment/<int:content_id>/', views.add_comment, name='add_comment'),
]