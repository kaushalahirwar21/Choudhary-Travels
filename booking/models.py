from django.db import models
from django.core.validators import MinValueValidator, RegexValidator


class VehicleCategory(models.TextChoices):
    SEDAN = 'sedan', 'Sedan'
    SUV = 'suv', 'SUV'
    INNOVA = 'innova', 'Innova / MUV'
    TEMPO = 'tempo', 'Tempo Traveller'
    BUS = 'bus', 'Mini Bus'


class Vehicle(models.Model):
    """Fleet vehicle available for booking."""

    name = models.CharField(max_length=120)
    category = models.CharField(
        max_length=20,
        choices=VehicleCategory.choices,
        default=VehicleCategory.SEDAN,
    )
    seats = models.PositiveSmallIntegerField(default=4)
    price_per_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Rate in INR per kilometre',
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Daily package rate in INR',
    )
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    description = models.TextField(blank=True)
    features = models.CharField(
        max_length=255,
        blank=True,
        help_text='Comma-separated features, e.g. AC, Music System, GPS',
    )
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'

    @property
    def feature_list(self):
        if not self.features:
            return []
        return [f.strip() for f in self.features.split(',') if f.strip()]


class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


phone_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message='Enter a valid 10-digit Indian mobile number.',
)


class Booking(models.Model):
    """Customer car rental / outstation booking request."""

    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=10, validators=[phone_validator])
    email = models.EmailField(blank=True)
    pickup_location = models.CharField(max_length=200)
    drop_location = models.CharField(max_length=200)
    pickup_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    pickup_time = models.TimeField(blank=True, null=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
    )
    passengers = models.PositiveSmallIntegerField(default=1)
    trip_type = models.CharField(
        max_length=20,
        choices=[
            ('one_way', 'One Way'),
            ('round_trip', 'Round Trip'),
            ('local', 'Local / City Tour'),
        ],
        default='one_way',
    )
    message = models.TextField(blank=True, help_text='Special requests or notes')
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )
    admin_notes = models.TextField(blank=True)
    whatsapp_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.customer_name} — {self.pickup_location} to {self.drop_location}'

    @property
    def vehicle_name(self):
        return self.vehicle.name if self.vehicle else 'Any Available'


class ContactMessage(models.Model):
    """Contact form enquiry from website visitors."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name}: {self.subject}'


class Testimonial(models.Model):
    """Customer review displayed on the homepage."""

    customer_name = models.CharField(max_length=120)
    location = models.CharField(max_length=100, blank=True)
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1)],
    )
    review = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.customer_name} ({self.rating}★)'


class Service(models.Model):
    """Travel service offering shown on the homepage."""

    title = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50,
        default='bi-car-front',
        help_text='Bootstrap Icons class, e.g. bi-airplane',
    )
    description = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title