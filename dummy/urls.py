from django.urls import path
from . import views

urlpatterns = [
    path('search', views.Aviatickets.as_view(), name='search'),
    path('airports', views.Airports.as_view(), name='airports'),
]
