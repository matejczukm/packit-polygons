from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hexagon/', views.hexagon, name='hexagon'),
    path('start_game/', views.start_new_game, name='start_game'),
    path('confirm_move/', views.confirm_move, name='confirm_move'),
    path('save_game/', views.save_game, name='save_game')

]
