from django.urls import path

from . import views

app_name = 'booking'

urlpatterns = [
    # Main pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Fleet and vehicles
    path('fleet/', views.FleetView.as_view(), name='fleet'),
    path('fleet/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    
    # Booking management
    path('book/', views.BookingCreateView.as_view(), name='book'),
    path('book/success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('my-bookings/', views.BookingTrackingView.as_view(), name='booking_tracking'),
    path('bookings/<int:pk>/cancel/', views.CancelBookingView.as_view(), name='cancel_booking'),
]
