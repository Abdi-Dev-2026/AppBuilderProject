from django.urls import path
from . import views

urlpatterns = [
    path('', views.maintenance, name='maintenance_view'),
]