from re import A
from django.urls import path

# from home.views import hello_world
from . import views
from django.http import HttpResponse
from django.shortcuts import render

app_name = 'home'

urlpatterns = [
    path('home/user/<str:user_id>', views.show_user_crack_list, name="show_crack_list"),
    path('home/user/list/glass_list', views.show_glass_list, name="show_glass_list"),
    path('home/user/building_list/<str:user_id>', views.show_building_list, name="show_building_list"),
    path('home/manager/<str:user_id>', views.show_manager_crack_list, name="show_manager_crack_list")
]