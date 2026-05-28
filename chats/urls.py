from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats_page, name='chats_page'),
    path('request/<int:profile_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
]