from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adventures/', views.trip_list, name='trip_list'),
    path('adventures/<slug:slug>/', views.trip_detail, name='trip_detail'),
]