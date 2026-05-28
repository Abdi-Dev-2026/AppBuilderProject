from django.urls import path
from . import views

urlpatterns = [
    path('', views.banaadir_view, name='banaadir'),
    path('imtixaanka/', views.banaadir_view, name='exam_view'), # Khadkii labaad ee loo isticmaali jiray
]