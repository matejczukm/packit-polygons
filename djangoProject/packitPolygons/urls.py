from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hexagon/', views.hexagon, name='hexagon'),
    # path('start_game/', views.start_game, name='start_game'),

]
