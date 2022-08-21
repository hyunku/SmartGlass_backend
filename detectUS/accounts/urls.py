from django.urls import path
from . import views
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'accounts'

urlpatterns = [

  path('signup',views.Sign_up,name="Signup"),
  path('login',views.login,name="Login"),
  path('logout/<str:user_id>',views.logout,name="Logout"),

]

urlpatterns = format_suffix_patterns(urlpatterns)