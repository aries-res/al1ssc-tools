from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_3Dorbit_data),
    path("bodies", views.get_bodies),
]
