from django.urls import path
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # PWA Service Worker khadkiisa halkan ayuu soo galayaa saaxiib
    path('sw.js', RedirectView.as_view(url=staticfiles_storage.url('sw.js'), permanent=False), name='sw_js'),
]