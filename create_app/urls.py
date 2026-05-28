from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_app, name='create_app'),
]