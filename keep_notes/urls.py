from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_dashboard, name='notes_dashboard'),
    path('api/sync/', views.sync_notes_api, name='sync_notes_api'),
]