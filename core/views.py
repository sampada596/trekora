from django.shortcuts import render
from .models import Trip

def home(request):
    featured_trips = Trip.objects.filter(is_featured=True)
    context = {
        'featured_trips': featured_trips,
    }
    return render(request, 'home.html', context)