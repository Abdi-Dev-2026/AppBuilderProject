from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_messages, name='my_messages'),
]