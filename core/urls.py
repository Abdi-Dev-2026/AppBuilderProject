from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # -----------------------------------------------------------
    # 1. BOGAGGA GUUD (Public Pages)
    # -----------------------------------------------------------
    # WAA LA SAXAY: 'homepage' waxaa loo beddelay 'home'
    path('', views.home, name='home'),
    
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('content/', views.content_page, name='content'),
    path('maintenance/', views.maintenance, name='maintenance'),

    # -----------------------------------------------------------
    # 2. XUBNAHA & AMAANKA (Auth & Dashboard)
    # -----------------------------------------------------------
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), 
    
    # Waxaan u beddelnay views.logout_view maadaama aan ku dhex dhisnay views.py-kaaga
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),

    # -----------------------------------------------------------
    # 3. DHISMAHA & MAAMULKA APP-KA (App Builder Logic)
    # -----------------------------------------------------------
    path('create-app/', views.create_app, name='create_app'),
    path('edit-code/<int:app_id>/', views.edit_code, name='edit_code'),
    path('app/<slug:slug>/', views.app_detail, name='app_detail'),
    path('download/<slug:slug>/', views.download_app, name='download_app'),

    # -----------------------------------------------------------
    # 4. WAXYAABAHA INTERACTIVE-KA AH (Quiz & Polls)
    # -----------------------------------------------------------
    path('quiz/', views.quiz_page, name='quiz'),
    path('poll/', views.poll_page, name='poll'),
    
    # Waxaan ka saarnay '#' si ay u shaqeeyaan interactive features-ka
    path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('vote/<int:poll_id>/', views.vote_poll, name='vote_poll'),
]