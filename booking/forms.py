from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Booking, ContactMessage, Vehicle, VehicleCategory


class BookingForm(forms.ModelForm):
    """
    Customer booking request form.
    
    Handles validation for:
    - Date ordering (pickup < return)
    - No past dates
    - Booking conflicts (Q objects for overlap detection)
    - Trip type requirements (round_trip requires return_date)
    """

    class Meta:
        model = Booking
        fields = [
            'customer_name',
            'phone',
            'email',
            'pickup_location',
            'drop_location',
            'pickup_date',
            'return_date',
            'pickup_time',
            'vehicle',
            'passengers',
            'trip_type',
            'message',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True,
                'pattern': "^[a-zA-Z\\s\\.\\-\\']+$",
                'title': 'Name must contain only alphabets and spaces.',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit mobile number',
                'maxlength': '10',
                'required': True,
                'pattern': '^[6-9]\\d{9}$',
                'title': 'Please enter a valid 10-digit Indian mobile number starting with 6-9.',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email (optional)',
            }),
            'pickup_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pickup city / address',
                'required': True,
            }),
            'drop_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Drop city / address',
                'required': True,
            }),
            'pickup_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'return_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'pickup_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'passengers': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '50',
            }),
            'trip_type': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests?',
            }),
        }

    def __init__(self, *args, **kwargs):
        vehicle_queryset = kwargs.pop('vehicle_queryset', None)
        super().__init__(*args, **kwargs)
        
        # Set vehicle queryset
        qs = vehicle_queryset or Vehicle.objects.filter(is_available=True)
        self.fields['vehicle'].queryset = qs
        self.fields['vehicle'].required = False
        self.fields['vehicle'].empty_label = '🚗 Any available vehicle'
        
        # Make optional fields
        self.fields['return_date'].required = False
        self.fields['pickup_time'].required = True
        self.fields['email'].required = False

    def clean(self):
        """
        Comprehensive form validation:
        - Check date ordering
        - Prevent past date bookings
        - Detect booking conflicts using Q objects
        - Validate trip type requirements
        """
        cleaned = super().clean()
        
        pickup_date = cleaned.get('pickup_date')
        return_date = cleaned.get('return_date')
        trip_type = cleaned.get('trip_type')
        vehicle = cleaned.get('vehicle')
        
        # Validate pickup date is not in the past
        if pickup_date:
            today = datetime.now().date()
            if pickup_date < today:
                self.add_error('pickup_date', '❌ Pickup date cannot be in the past.')
        
        # Validate round trip requires return date
        if trip_type == 'round_trip' and not return_date:
            self.add_error('return_date', '⚠️ Return date is required for round trips.')
        
        # Validate date ordering (return > pickup)
        if pickup_date and return_date:
            if return_date <= pickup_date:
                self.add_error(
                    'return_date',
                    '⚠️ Return date must be after pickup date.',
                )
        
        # Check for booking conflicts if vehicle is selected
        if vehicle and pickup_date:
            # Build Q object for overlapping bookings
            # Overlap occurs when: existing.start < new.end AND existing.end > new.start
            if return_date:
                end_date = return_date
            else:
                end_date = pickup_date
            
            # Find conflicting confirmed or completed bookings
            conflicts = Booking.objects.filter(
                vehicle=vehicle,
                status__in=['confirmed', 'completed'],
            ).filter(
                # Check overlap: existing_start < new_end AND existing_end > new_start
                Q(pickup_date__lt=end_date) & Q(
                    Q(return_date__isnull=True) & Q(pickup_date__gte=pickup_date) |
                    Q(return_date__isnull=False) & Q(return_date__gt=pickup_date)
                )
            )
            
            if conflicts.exists():
                conflict_dates = ', '.join([
                    f"{b.pickup_date.strftime('%d %b')}"
                    for b in conflicts[:3]
                ])
                self.add_error(
                    'vehicle',
                    f'❌ This vehicle is unavailable on selected dates. Conflicts: {conflict_dates}',
                )
        
        return cleaned

    def clean_customer_name(self):
        """Validate customer name: only letters, spaces, dots, hyphens, and apostrophes."""
        name = self.cleaned_data.get('customer_name', '').strip()
        if not name:
            return name
        
        import re
        if not re.match(r"^[a-zA-Z\s\.\-\']+$", name):
            raise ValidationError('Name must contain only alphabets and spaces.')
        return name

    def clean_phone(self):
        """Validate Indian mobile number (10 digits, starts with 6-9, only digits)."""
        phone = self.cleaned_data.get('phone', '').strip()
        
        if not phone:
            return phone
            
        if not phone.isdigit():
            raise ValidationError('Phone number must contain only digits (0-9).')
        
        if len(phone) != 10:
            raise ValidationError('Phone number must be exactly 10 digits.')
        
        if phone[0] not in '6789':
            raise ValidationError('Phone number must start with 6, 7, 8, or 9.')
        
        return phone

    def clean_passengers(self):
        """Validate passenger count."""
        passengers = self.cleaned_data.get('passengers')
        
        if passengers and passengers < 1:
            raise ValidationError('At least 1 passenger is required.')
        
        if passengers and passengers > 50:
            raise ValidationError('Maximum 50 passengers allowed.')
        
        return passengers


class CarFilterForm(forms.Form):
    """
    Vehicle filtering form for the fleet page.
    
    Allows filtering by:
    - Category (Sedan, SUV, Innova, Tempo, Bus)
    - Minimum seats
    - Maximum price per day
    """
    
    CATEGORY_CHOICES = [('', '📍 All Categories')] + list(VehicleCategory.choices)
    
    category = forms.ChoiceField(
        label='Category',
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
    )
    
    min_seats = forms.IntegerField(
        label='Minimum Seats',
        required=False,
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Min seats',
            'min': '1',
        }),
    )
    
    max_price_per_day = forms.DecimalField(
        label='Max Price/Day (₹)',
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Max price',
            'min': '0',
            'step': '100',
        }),
    )
    
    search_query = forms.CharField(
        label='Search',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Search by name...',
        }),
    )
    
    def clean_max_price_per_day(self):
        """Validate max price is reasonable."""
        max_price = self.cleaned_data.get('max_price_per_day')
        
        if max_price and max_price > 100000:
            raise ValidationError('Price seems too high. Please enter a reasonable value.')
        
        return max_price

    def clean_min_seats(self):
        """Validate min seats."""
        min_seats = self.cleaned_data.get('min_seats')
        
        if min_seats and min_seats < 1:
            raise ValidationError('Minimum seats must be at least 1.')
        
        return min_seats


class ContactForm(forms.ModelForm):
    """Website contact / enquiry form."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
                'pattern': "^[a-zA-Z\\s\\.\\-\\']+$",
                'title': 'Name must contain only alphabets and spaces.',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number (optional)',
                'maxlength': '10',
                'pattern': '^[6-9]\\d{9}$',
                'title': 'Please enter a valid 10-digit Indian mobile number starting with 6-9.',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'How can we help you?',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = False

    def clean_name(self):
        """Validate name: only letters, spaces, dots, hyphens, and apostrophes."""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            return name
        
        import re
        if not re.match(r"^[a-zA-Z\s\.\-\']+$", name):
            raise ValidationError('Name must contain only alphabets and spaces.')
        return name

    def clean_phone(self):
        """Validate Indian mobile number (10 digits, starts with 6-9, only digits)."""
        phone = self.cleaned_data.get('phone', '').strip()
        
        if not phone:
            return phone
            
        if not phone.isdigit():
            raise ValidationError('Phone number must contain only digits (0-9).')
        
        if len(phone) != 10:
            raise ValidationError('Phone number must be exactly 10 digits.')
        
        if phone[0] not in '6789':
            raise ValidationError('Phone number must start with 6, 7, 8, or 9.')
        
        return phone