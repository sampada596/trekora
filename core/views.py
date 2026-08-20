from django.shortcuts import render, get_object_or_404, redirect
from .models import Trip
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Trip, Booking
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Avg
from .forms import ReviewForm
from .models import Trip, Booking, Review

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    reviews = trip.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(user=request.user, trip=trip).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        if user_has_reviewed:
            messages.error(request, "You've already reviewed this trip.")
            return redirect('trip_detail', slug=trip.slug)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.trip = trip
            review.save()
            messages.success(request, "Thanks for your review!")
            return redirect('trip_detail', slug=trip.slug)
    else:
        form = ReviewForm()

    context = {
        'trip': trip,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': form,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'trip_detail.html', context)

@login_required
def create_checkout_session(request, slug):
    trip = get_object_or_404(Trip, slug=slug)

    booking = Booking.objects.create(
        user=request.user,
        trip=trip,
        status='pending',
    )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': trip.title,
                },
                'unit_amount': int(trip.price * 100),  # Stripe uses cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('booking_success')) + f'?session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url=request.build_absolute_uri(reverse('booking_cancel')),
        metadata={
            'booking_id': booking.id,
        },
    )

    booking.stripe_session_id = session.id
    booking.save()

    return redirect(session.url, code=303)

@login_required
def booking_success(request):
    return render(request, 'booking_success.html')


@login_required
def booking_cancel(request):
    return render(request, 'booking_cancel.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        booking_id = session['metadata']['booking_id']

        try:
            booking = Booking.objects.get(id=booking_id)
            booking.status = 'paid'
            booking.amount_paid = session['amount_total'] / 100
            booking.save()
        except Booking.DoesNotExist:
            pass

    return HttpResponse(status=200)