from django.urls import path
from . import views

urlpatterns = [
    path('edit-code/<int:app_id>/', views.edit_code, name='edit_code'),
]