from django.contrib import admin
from .models import Trip

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'region', 'price', 'is_featured')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}