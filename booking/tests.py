"""
Django tests for the booking application.
Run tests with: python manage.py test booking
"""

from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from .models import Booking, ContactMessage, Service, Testimonial, Vehicle


class VehicleModelTests(TestCase):
    """Test the Vehicle model."""

    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            name='Toyota Innova',
            category='innova',
            seats=7,
            price_per_km=18,
            price_per_day=4500,
            description='Test vehicle',
            is_available=True,
            is_featured=True,
        )

    def test_vehicle_str(self):
        """Test Vehicle __str__ method returns formatted name."""
        expected = 'Toyota Innova (Innova / MUV)'
        self.assertEqual(str(self.vehicle), expected)

    def test_vehicle_feature_list(self):
        """Test feature_list property parses comma-separated features."""
        self.vehicle.features = 'AC, Music System, GPS'
        self.assertEqual(self.vehicle.feature_list, ['AC', 'Music System', 'GPS'])

    def test_feature_list_empty(self):
        """Test feature_list returns empty list when no features."""
        self.vehicle.features = ''
        self.assertEqual(self.vehicle.feature_list, [])

    def test_vehicle_available_filter(self):
        """Test filtering vehicles by availability."""
        unavailable = Vehicle.objects.create(
            name='Test Sedan',
            category='sedan',
            seats=4,
            price_per_km=12,
            price_per_day=2500,
            is_available=False,
        )
        available_count = Vehicle.objects.filter(is_available=True).count()
        self.assertEqual(available_count, 1)
        self.assertIn(self.vehicle, Vehicle.objects.filter(is_available=True))
        self.assertNotIn(unavailable, Vehicle.objects.filter(is_available=True))


class BookingModelTests(TestCase):
    """Test the Booking model."""

    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            name='Swift Dzire',
            category='sedan',
            seats=4,
            price_per_km=12,
            price_per_day=2500,
            is_available=True,
        )
        self.today = datetime.now().date()
        self.tomorrow = self.today + timedelta(days=1)

    def test_booking_str(self):
        """Test Booking __str__ method."""
        booking = Booking.objects.create(
            customer_name='John Doe',
            phone='9876543210',
            email='john@example.com',
            pickup_location='Delhi',
            drop_location='Agra',
            pickup_date=self.today,
            vehicle=self.vehicle,
            passengers=2,
            trip_type='one_way',
        )
        expected = 'John Doe — Delhi to Agra'
        self.assertEqual(str(booking), expected)

    def test_booking_vehicle_name_property(self):
        """Test vehicle_name property."""
        booking = Booking.objects.create(
            customer_name='Jane Doe',
            phone='9876543210',
            pickup_location='Mumbai',
            drop_location='Pune',
            pickup_date=self.today,
            vehicle=self.vehicle,
        )
        self.assertEqual(booking.vehicle_name, 'Swift Dzire')

    def test_booking_vehicle_name_when_none(self):
        """Test vehicle_name returns default when no vehicle selected."""
        booking = Booking.objects.create(
            customer_name='Jane Doe',
            phone='9876543210',
            pickup_location='Mumbai',
            drop_location='Pune',
            pickup_date=self.today,
            vehicle=None,
        )
        self.assertEqual(booking.vehicle_name, 'Any Available')

    def test_booking_status_default(self):
        """Test booking status defaults to PENDING."""
        booking = Booking.objects.create(
            customer_name='Bob Smith',
            phone='9876543210',
            pickup_location='Bangalore',
            drop_location='Mysore',
            pickup_date=self.today,
        )
        self.assertEqual(booking.status, 'pending')

    def test_booking_round_trip_requires_return_date(self):
        """Test that round trip bookings are allowed with return date."""
        booking = Booking.objects.create(
            customer_name='Alice Brown',
            phone='9876543210',
            pickup_location='Delhi',
            drop_location='Goa',
            pickup_date=self.today,
            return_date=self.tomorrow,
            trip_type='round_trip',
            vehicle=self.vehicle,
        )
        self.assertEqual(booking.trip_type, 'round_trip')
        self.assertIsNotNone(booking.return_date)

    def test_booking_ordering(self):
        """Test bookings are ordered by created_at descending."""
        booking1 = Booking.objects.create(
            customer_name='First',
            phone='9876543210',
            pickup_location='Delhi',
            drop_location='Agra',
            pickup_date=self.today,
        )
        booking2 = Booking.objects.create(
            customer_name='Second',
            phone='9876543210',
            pickup_location='Mumbai',
            drop_location='Pune',
            pickup_date=self.today,
        )
        # Manually adjust created_at to ensure different timestamps and avoid test flakiness
        from django.utils import timezone
        Booking.objects.filter(pk=booking1.pk).update(created_at=timezone.now() - timedelta(days=1))
        Booking.objects.filter(pk=booking2.pk).update(created_at=timezone.now())

        bookings = list(Booking.objects.all())
        # Most recent booking should be first if ordered by created_at desc
        self.assertEqual(bookings[0].customer_name, 'Second')
        self.assertEqual(bookings[1].customer_name, 'First')



class ContactMessageTests(TestCase):
    """Test the ContactMessage model."""

    def test_contact_message_creation(self):
        """Test creating a contact message."""
        msg = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='Test message content',
        )
        self.assertEqual(msg.name, 'Test User')
        self.assertFalse(msg.is_read)

    def test_contact_message_str(self):
        """Test ContactMessage __str__ method."""
        msg = ContactMessage.objects.create(
            name='John Doe',
            email='john@example.com',
            subject='Inquiry',
            message='I have a question.',
        )
        expected = 'John Doe: Inquiry'
        self.assertEqual(str(msg), expected)


class TestimonialTests(TestCase):
    """Test the Testimonial model."""

    def test_testimonial_creation(self):
        """Test creating a testimonial."""
        testimonial = Testimonial.objects.create(
            customer_name='Happy Customer',
            location='Delhi',
            rating=5,
            review='Great service!',
            is_active=True,
        )
        self.assertEqual(testimonial.rating, 5)
        self.assertTrue(testimonial.is_active)

    def test_testimonial_str(self):
        """Test Testimonial __str__ method."""
        testimonial = Testimonial.objects.create(
            customer_name='Jane Doe',
            rating=4,
            review='Good experience.',
        )
        expected = 'Jane Doe (4★)'
        self.assertEqual(str(testimonial), expected)


class ServiceTests(TestCase):
    """Test the Service model."""

    def test_service_creation(self):
        """Test creating a service."""
        service = Service.objects.create(
            title='Airport Transfer',
            icon='bi-airplane',
            description='Fast and reliable airport transfers.',
            sort_order=1,
            is_active=True,
        )
        self.assertEqual(service.title, 'Airport Transfer')

    def test_service_str(self):
        """Test Service __str__ method."""
        service = Service.objects.create(
            title='Outstation Trip',
            description='Travel anywhere in India.',
        )
        self.assertEqual(str(service), 'Outstation Trip')


class HomeViewTests(TestCase):
    """Test the HomeView."""

    def setUp(self):
        self.client = Client()
        # Create some featured vehicles
        Vehicle.objects.create(
            name='Featured Car 1',
            category='sedan',
            seats=4,
            price_per_km=12,
            price_per_day=2500,
            is_available=True,
            is_featured=True,
        )
        # Create a non-featured vehicle
        Vehicle.objects.create(
            name='Non-Featured Car',
            category='sedan',
            seats=4,
            price_per_km=12,
            price_per_day=2500,
            is_available=True,
            is_featured=False,
        )

    def test_home_view_returns_200(self):
        """Test home page returns HTTP 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """Test home page uses correct template."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'booking/home.html')

    def test_home_view_context_featured_vehicles(self):
        """Test home page context includes featured vehicles."""
        response = self.client.get('/')
        featured = response.context['featured_vehicles']
        self.assertEqual(featured.count(), 1)
        self.assertEqual(featured[0].name, 'Featured Car 1')


class FleetViewTests(TestCase):
    """Test the FleetView."""

    def setUp(self):
        self.client = Client()
        self.sedan = Vehicle.objects.create(
            name='Swift Dzire',
            category='sedan',
            seats=4,
            price_per_km=12,
            price_per_day=2500,
            is_available=True,
        )
        self.suv = Vehicle.objects.create(
            name='Mahindra XUV',
            category='suv',
            seats=5,
            price_per_km=15,
            price_per_day=3500,
            is_available=True,
        )
        self.unavailable = Vehicle.objects.create(
            name='Broken Car',
            category='sedan',
            seats=4,
            price_per_km=12,
            price_per_day=2500,
            is_available=False,
        )

    def test_fleet_view_returns_200(self):
        """Test fleet page returns HTTP 200."""
        response = self.client.get('/fleet/')
        self.assertEqual(response.status_code, 200)

    def test_fleet_view_only_shows_available(self):
        """Test fleet only shows available vehicles."""
        response = self.client.get('/fleet/')
        vehicles = response.context['vehicles']
        self.assertEqual(vehicles.count(), 2)
        self.assertNotIn(self.unavailable, vehicles)

    def test_fleet_filter_by_category(self):
        """Test fleet can filter by category."""
        response = self.client.get('/fleet/?category=sedan')
        vehicles = response.context['vehicles']
        self.assertEqual(vehicles.count(), 1)
        self.assertEqual(vehicles[0].name, 'Swift Dzire')

    def test_fleet_search_by_name(self):
        """Test fleet can search by vehicle name."""
        response = self.client.get('/fleet/?q=XUV')
        vehicles = response.context['vehicles']
        self.assertEqual(vehicles.count(), 1)
        self.assertEqual(vehicles[0].name, 'Mahindra XUV')


class BookingCreateViewTests(TestCase):
    """Test the BookingCreateView."""

    def setUp(self):
        self.client = Client()
        self.vehicle = Vehicle.objects.create(
            name='Test Vehicle',
            category='sedan',
            seats=4,
            price_per_km=12,
            price_per_day=2500,
            is_available=True,
        )
        self.today = datetime.now().date()

    def test_booking_create_view_returns_200(self):
        """Test booking page returns HTTP 200."""
        response = self.client.get('/book/')
        self.assertEqual(response.status_code, 200)

    def test_booking_create_form_in_context(self):
        """Test booking form is in context."""
        response = self.client.get('/book/')
        self.assertIn('form', response.context)

    def test_booking_create_valid_submission(self):
        """Test valid booking submission."""
        data = {
            'customer_name': 'Test User',
            'phone': '9876543210',
            'email': 'test@example.com',
            'pickup_location': 'Delhi',
            'drop_location': 'Agra',
            'pickup_date': self.today,
            'pickup_time': '10:00',
            'trip_type': 'one_way',
            'passengers': 2,
            'vehicle': self.vehicle.pk,
        }
        response = self.client.post('/book/', data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Booking.objects.count(), 1)


    def test_booking_create_invalid_missing_name(self):
        """Test booking with missing customer name fails."""
        data = {
            'phone': '9876543210',
            'email': 'test@example.com',
            'pickup_location': 'Delhi',
            'drop_location': 'Agra',
            'pickup_date': self.today,
            'trip_type': 'one_way',
        }
        response = self.client.post('/book/', data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertEqual(Booking.objects.count(), 0)


class AboutViewTests(TestCase):
    """Test the AboutView."""

    def setUp(self):
        self.client = Client()

    def test_about_view_returns_200(self):
        """Test about page returns HTTP 200."""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_view_uses_correct_template(self):
        """Test about page uses correct template."""
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'booking/about.html')


class ContactViewTests(TestCase):
    """Test the ContactView."""

    def setUp(self):
        self.client = Client()

    def test_contact_view_returns_200(self):
        """Test contact page returns HTTP 200."""
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_contact_form_in_context(self):
        """Test contact form is in context."""
        response = self.client.get('/contact/')
        self.assertIn('form', response.context)

    def test_contact_form_submission(self):
        """Test valid contact form submission."""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message',
        }
        response = self.client.post('/contact/', data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_form_invalid_missing_email(self):
        """Test contact form with missing email fails."""
        data = {
            'name': 'Test User',
            'subject': 'Test Subject',
            'message': 'Test message',
        }
        response = self.client.post('/contact/', data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertEqual(ContactMessage.objects.count(), 0)