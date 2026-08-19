from django.contrib import admin
from .models import Trip, Booking

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'region', 'price', 'is_featured')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'status', 'amount_paid', 'created_at')
    list_filter = ('status',)