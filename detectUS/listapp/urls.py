from django.urls import path

from listapp.views import BuildingList

from listapp.views import CreateBuilding

from listapp.views import DeleteBuilding

from listapp.views import GlassList

from listapp.views import CreateGlass

from listapp.views import BuildingTest

from listapp.views import Connect_user_glass

app_name = 'listapp'

urlpatterns = [
    path('building/', BuildingList.as_view()),
    path('building/create/', CreateBuilding.as_view()),
    path('building/delete/<int:pk>/', DeleteBuilding.as_view()),
    path('glass/', GlassList.as_view()),
    path('glass/create/', CreateGlass.as_view()),
    path('building/testing/', BuildingTest.as_view()),
    path('glass/connect/<int:pk>/', Connect_user_glass.as_view())
]