from re import A
from django.urls import path

# from home.views import hello_world
from . import views
from django.http import HttpResponse
from django.shortcuts import render

app_name = 'home'

urlpatterns = [

    path('user/<str:user_id>', views.show_user_crack_list, name="show_crack_list"),
    path('user/list/connect/1/<str:user_id>', views.show_glass_list, name="show_glass_list"),
    path('user/list/connect/2/<str:user_id>', views.show_building_list, name="show_building_list"),
    path('manager/list/<str:user_id>', views.show_manager_crack_list, name="show_manager_crack_list"),
    path('user/connect/iot',views.connect_glass_and_building, name="connect_glass_and_building"),
    path('user/disconnect/iot/<str:user_id>',views.disconnect_glass_and_building, name="connect_glass_and_building")

]