from django.shortcuts import render, get_object_or_404
from .models import Trip

def home(request):
    featured_trips = Trip.objects.filter(is_featured=True)
    context = {
        'featured_trips': featured_trips,
    }
    return render(request, 'home.html', context)


def trip_list(request):
    trips = Trip.objects.all()

    category = request.GET.get('category')
    if category:
        trips = trips.filter(category=category)

    context = {
        'trips': trips,
        'categories': Trip.CATEGORY_CHOICES,
        'selected_category': category,
    }
    return render(request, 'trip_list.html', context)


def trip_detail(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    context = {
        'trip': trip,
    }
    return render(request, 'trip_detail.html', context)