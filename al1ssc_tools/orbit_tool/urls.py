from django.urls import path

from . import views

urlpatterns = [
    path("3D", views.get_3Dorbit_data),
    path("2D", views.get_2Dorbit_plot),
    path("bodies", views.get_bodies),
]
