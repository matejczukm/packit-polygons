from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page URL
    path('hexagon/', views.hexagon, name='hexagon'),  # Hexagonal board URL
]
