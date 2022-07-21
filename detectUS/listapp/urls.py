from django.urls import path

from listapp.views import BuildingList

app_name = 'listapp'

urlpatterns = [
    path('building/', BuildingList.as_view()),
]