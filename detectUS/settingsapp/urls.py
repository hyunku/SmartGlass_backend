from django.urls import path
from .views import userAPIView, passwordAPIView
from rest_framework.urlpatterns import format_suffix_patterns

appname='settingsapp'

urlpatterns = [
   path('password/<str:user_name>/', passwordAPIView.as_view(),name="account-detail"),
   path('user/<str:user_name>/', userAPIView.as_view(),name="account-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
