from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('id-card/download/', views.download_id_card, name='download_id_card'),
]