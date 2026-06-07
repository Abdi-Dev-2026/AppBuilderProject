from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('session/<int:session_id>/', views.chat_session_view, name='chat_session_view'),
    path('new-chat/', views.new_chat, name='new_chat'),
]