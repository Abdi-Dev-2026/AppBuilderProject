from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_page, name='poll_page'),
    path('vote/<int:poll_id>/', views.vote_poll, name='vote_poll'),
]