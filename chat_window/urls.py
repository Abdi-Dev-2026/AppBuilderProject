from django.urls import path
from . import views

urlpatterns = [
    path('t/<str:username>/', views.chat_with_user, name='chat_with_user'),
]