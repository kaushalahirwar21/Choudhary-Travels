from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, View

from .forms import BookingForm, ContactForm
from .models import Booking, ContactMessage, Service, Testimonial, Vehicle

class HomeView(TemplateView):
    """Homepage with featured vehicles, services, and quick booking form."""
    
    template_name = 'booking/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_vehicles'] = Vehicle.objects.filter(
            is_available=True, is_featured=True,
        )[:6]
        context['services'] = Service.objects.filter(is_active=True)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:6]
        context['booking_form'] = BookingForm()
        return context


class FleetView(ListView):
    """Display all available vehicles with filtering and search."""
    
    model = Vehicle
    template_name = 'booking/fleet.html'
    context_object_name = 'vehicles'
    paginate_by = 12

    def get_queryset(self):
        """Filter vehicles to only show Mahindra Bolero Neo."""
        return Vehicle.objects.filter(name__icontains='Mahindra Bolero Neo', is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Vehicle._meta.get_field('category').choices
        context['active_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['min_seats'] = self.request.GET.get('min_seats', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        return context


class VehicleDetailView(DetailView):
    """Display vehicle details with booking form and unavailable dates."""
    
    model = Vehicle
    template_name = 'booking/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pre-fill the booking form with this vehicle
        context['booking_form'] = BookingForm(
            vehicle_queryset=Vehicle.objects.filter(pk=self.object.pk),
            initial={'vehicle': self.object.pk},
        )
        
        # Get unavailable dates for this vehicle (optional, for calendar UI)
        # This would require a more complex booking overlap detection
        # For now, we just note that bookings are checked in the form's clean() method
        booked_dates = Booking.objects.filter(
            vehicle=self.object,
            status__in=['confirmed', 'completed'],
        ).values_list('pickup_date', 'return_date')
        
        context['unavailable_dates'] = [
            {
                'start': str(start),
                'end': str(end) if end else str(start),
            }
            for start, end in booked_dates if start
        ]
        
        return context


class BookingCreateView(CreateView):
    """Handle new booking request creation."""
    
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    
    def get_initial(self):
        """Pre-fill vehicle if passed via GET parameter."""
        initial = super().get_initial()
        vehicle_id = self.request.GET.get('vehicle')
        if vehicle_id:
            try:
                initial['vehicle'] = int(vehicle_id)
            except (ValueError, TypeError):
                pass
        return initial

    def _build_whatsapp_message(self, form):
        """Build a formatted WhatsApp message from form data."""
        
        data = form.cleaned_data
        
        # Get data, providing an empty string as a default
        name = data.get('customer_name', '')
        phone = data.get('phone', '')
        pickup_location = data.get('pickup_location', '')
        drop_location = data.get('drop_location', '')
        
        # Format date and time, handling None cases
        pickup_date_str = data['pickup_date'].strftime('%d %B, %Y') if data.get('pickup_date') else ''
        pickup_time_str = data['pickup_time'].strftime('%I:%M %p') if data.get('pickup_time') else ''

        message_lines = [
            "NEW CAR BOOKING REQUEST",
            "",
            "---",
            "",
            f"Customer Name : {name}",
            f"Phone Number  : {phone}",
            f"Pickup Location : {pickup_location}",
            f"Destination    : {drop_location}",
            f"Travel Date    : {pickup_date_str}",
            f"Booking Time   : {pickup_time_str}",
            "",
            "---",
            "",
            "Kindly review the request and confirm vehicle availability."
        ]
        
        return "\n".join(message_lines)

    def form_valid(self, form):
        """On valid form, redirect to WhatsApp with pre-filled message."""
        
        # Build the formatted message
        message = self._build_whatsapp_message(form)
        
        # Get the business WhatsApp number from settings
        whatsapp_number = settings.BUSINESS_WHATSAPP
        
        # Create the WhatsApp URL
        whatsapp_url = f"https://wa.me/{whatsapp_number}?" + urlencode({'text': message}, encoding='utf-8')
        
        # Add a success message for the user
        messages.success(
            self.request,
            "✅ Your booking request has been sent! You will now be redirected to WhatsApp to confirm."
        )
        
        # Redirect the user
        return HttpResponseRedirect(whatsapp_url)

    def form_invalid(self, form):
        """Handle form validation errors."""
        messages.error(
            self.request,
            '⚠️ Please correct the errors below and try again.',
        )
        return super().form_invalid(form)


class BookingSuccessView(TemplateView):
    """Confirmation page after successful booking."""
    
    template_name = 'booking/booking_success.html'


class BookingTrackingView(FormView):
    """Track booking by phone number and email."""
    
    template_name = 'booking/booking_tracking.html'
    form_class = BookingForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        phone = self.request.GET.get('phone', '')
        email = self.request.GET.get('email', '')
        
        if phone or email:
            bookings = Booking.objects.all()
            if phone:
                bookings = bookings.filter(phone__iexact=phone)
            if email:
                bookings = bookings.filter(email__iexact=email)
            
            context['bookings'] = bookings.order_by('-created_at')
            context['search_performed'] = True
        else:
            context['bookings'] = []
            context['search_performed'] = False
        
        return context


class CancelBookingView(View):
    """Cancel a booking (POST only)."""
    
    def post(self, request, pk):
        """Handle booking cancellation."""
        booking = get_object_or_404(Booking, pk=pk)
        
        # Verify the requester knows booking details (phone + email)
        request_phone = request.POST.get('phone', '').strip()
        request_email = request.POST.get('email', '').strip()
        
        if request_phone.lower() != booking.phone.lower():
            messages.error(request, '❌ Invalid phone number.')
            return redirect('booking:booking_tracking')
        
        if request_email.lower() != (booking.email or '').lower():
            messages.error(request, '❌ Invalid email.')
            return redirect('booking:booking_tracking')
        
        # Allow cancellation only for pending or confirmed bookings
        if booking.status not in ['pending', 'confirmed']:
            messages.warning(
                request,
                f'⚠️ Bookings with status "{booking.get_status_display()}" cannot be cancelled.',
            )
            return redirect('booking:booking_tracking')
        
        # Cancel the booking
        booking.status = 'cancelled'
        booking.save(update_fields=['status', 'updated_at'])
        
        messages.success(
            request,
            '✅ Your booking has been cancelled successfully.',
        )
        
        logger.info(f'Booking #{booking.pk} cancelled by customer ({booking.phone})')
        
        return redirect('booking:booking_tracking')


class AboutView(TemplateView):
    """About page."""
    
    template_name = 'booking/about.html'


class ContactView(CreateView):
    """Handle contact form submissions."""
    
    model = ContactMessage
    form_class = ContactForm
    template_name = 'booking/contact.html'
    success_url = reverse_lazy('booking:contact')

    def form_valid(self, form):
        """Save contact message and show success message."""
        form.save()
        messages.success(
            self.request,
            '✅ Thank you for reaching out! We will get back to you soon.',
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Show form errors."""
        messages.error(
            self.request,
            '⚠️ Please fix the errors in the form and try again.',
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.get_form()
        return context