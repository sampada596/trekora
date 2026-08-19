from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adventures/', views.trip_list, name='trip_list'),
    path('adventures/<slug:slug>/', views.trip_detail, name='trip_detail'),
    path('adventures/<slug:slug>/book/', views.create_checkout_session, name='create_checkout_session'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('booking-cancel/', views.booking_cancel, name='booking_cancel'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]