from django.urls import path
from . import views
from .views import signupAPIView 
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'accounts'

urlpatterns = [
  #  path('', views.index, name='accounts'),
  path('signup', signupAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)