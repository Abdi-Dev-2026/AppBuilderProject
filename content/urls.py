from django.urls import path
from . import views

urlpatterns = [
    path('', views.content_page, name='content'),
    path('like/<int:content_id>/', views.like_content, name='like_content'),
    path('comment/<int:content_id>/', views.add_comment, name='add_comment'),
]