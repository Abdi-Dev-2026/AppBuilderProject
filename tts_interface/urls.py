from django.urls import path
from . import views

urlpatterns = [
    path('', views.tts_interface_view, name='tts_interface'),
]