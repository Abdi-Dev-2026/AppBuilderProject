from django.urls import path
from . import views

urlpatterns = [
    path('', views.games_dashboard, name='games_dashboard'),
    path('play/<slug:game_slug>/', views.play_game, name='play_game'),
]