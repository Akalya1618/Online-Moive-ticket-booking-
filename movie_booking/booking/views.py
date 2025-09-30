from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Showtime, Seat, Booking

def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    showtimes = movie.showtime_set.all()
    return render(request, 'movie_detail.html', {'movie': movie, 'showtimes': showtimes})

def seat_selection(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    seats = Seat.objects.filter(showtime=showtime)
    if request.method == "POST":
        selected_seats = request.POST.getlist('seats')
        request.session['selected_seats'] = selected_seats
        request.session['showtime_id'] = showtime_id
        return redirect('checkout')
    return render(request, 'seat_selection.html', {'showtime': showtime, 'seats': seats})

def checkout(request):
    showtime_id = request.session.get('showtime_id')
    selected_seats = request.session.get('selected_seats', [])
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    seats = Seat.objects.filter(id__in=selected_seats)
    total_price = showtime.price * len(seats)

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        booking = Booking.objects.create(showtime=showtime, name=name, email=email, phone=phone)
        booking.seats.set(seats)
        seats.update(is_booked=True)
        return redirect('booking_success', booking_id=booking.id)

    return render(request, 'checkout.html', {'showtime': showtime, 'seats': seats, 'total_price': total_price})

def booking_success(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    total_price = booking.showtime.price * booking.seats.count()

    # For now, just store a dummy payment method
    payment_method = "UPI"   # You can later fetch this from form/DB

    return render(request, 'booking_success.html', {
        'booking': booking,
        'total_price': total_price,
        'payment_method': payment_method,
    })
