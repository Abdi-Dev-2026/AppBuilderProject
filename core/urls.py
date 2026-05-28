from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 0. Maintenance Mode (CUSUB)
    path('maintenance/', views.maintenance, name='maintenance'),

    # 1. Diiwaangelinta (Register)
    path('register/', views.register, name='register'),
    
    # 2. Gelitaanka (Login)
    path('login/', views.login_view, name='login'), 
    
    # 3. Ka bixitaanka (Logout)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 4. Dashboard-ka (Liiska Apps-ka uu user-ku dhistay)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # 5. Dhismaha App-ka cusub
    path('create-app/', views.create_app, name='create_app'),

    # 6. EDIT CODE (Matoorka Editor-ka iyo Live Preview-ga)
    path('edit-code/<int:app_id>/', views.edit_code, name='edit_code'),

    # 7. BOGGA LIVE-KA AH (Public App Link)
    path('app/<slug:slug>/', views.app_detail, name='app_detail'),

    # 8. SOO DEJINTA APP-KA (Download ZIP)
    path('download/<slug:slug>/', views.download_app, name='download_app'),
]