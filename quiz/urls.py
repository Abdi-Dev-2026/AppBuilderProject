from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_page, name='quiz_page'),
    path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('reset-quiz/', views.reset_quiz, name='reset_quiz'),
]