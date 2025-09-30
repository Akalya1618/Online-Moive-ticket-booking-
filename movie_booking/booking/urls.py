from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('showtime/<int:showtime_id>/seats/', views.seat_selection, name='seat_selection'),
    path('checkout/', views.checkout, name='checkout'),
    path('booking/<int:booking_id>/success/', views.booking_success, name='booking_success'),
]
