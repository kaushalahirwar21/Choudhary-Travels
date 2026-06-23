from django.core.management.base import BaseCommand

from booking.models import Service, Testimonial, Vehicle


class Command(BaseCommand):
    help = 'Populate database with sample vehicles, services, and testimonials'

    def handle(self, *args, **options):
        if Vehicle.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Skipping seed.'))
            return

        vehicles = [
            {
                'name': 'Swift Dzire',
                'category': 'sedan',
                'seats': 4,
                'price_per_km': 12,
                'price_per_day': 2500,
                'description': 'Perfect for city rides and short outstation trips. Fuel efficient and comfortable.',
                'features': 'AC, Music System, GPS, Bottle Water',
                'is_featured': True,
            },
            {
                'name': 'Honda City',
                'category': 'sedan',
                'seats': 4,
                'price_per_km': 14,
                'price_per_day': 3000,
                'description': 'Premium sedan for business travel and airport transfers.',
                'features': 'AC, Leather Seats, GPS, USB Charging',
                'is_featured': True,
            },
            {
                'name': 'Toyota Innova Crysta',
                'category': 'innova',
                'seats': 7,
                'price_per_km': 18,
                'price_per_day': 4500,
                'description': 'The most popular choice for family outstation trips across India.',
                'features': 'AC, Captain Seats, GPS, Ample Luggage Space',
                'is_featured': True,
            },
            {
                'name': 'Mahindra Scorpio',
                'category': 'suv',
                'seats': 7,
                'price_per_km': 16,
                'price_per_day': 4000,
                'description': 'Rugged SUV ideal for hill stations and rough terrain.',
                'features': 'AC, 4WD, GPS, High Ground Clearance',
                'is_featured': True,
            },
            {
                'name': 'Mahindra Bolero Neo',
                'category': 'suv',
                'seats': 7,
                'price_per_km': 20,
                'price_per_day': 5000,
                'description': 'A tough and reliable SUV for all kinds of Indian roads. Great for family trips and adventures.',
                'features': 'AC, Music System, GPS, Power Windows',
                'is_featured': True,
            },
            {
                'name': 'Tempo Traveller 12 Seater',
                'category': 'tempo',
                'seats': 12,
                'price_per_km': 22,
                'price_per_day': 6000,
                'description': 'Spacious tempo for group tours, weddings, and corporate outings.',
                'features': 'AC, Push-back Seats, GPS, PA System',
                'is_featured': True,
            },
            {
                'name': 'Tempo Traveller 17 Seater',
                'category': 'tempo',
                'seats': 17,
                'price_per_km': 26,
                'price_per_day': 7500,
                'description': 'Large group travel with maximum comfort and luggage capacity.',
                'features': 'AC, Push-back Seats, GPS, LCD Screen',
                'is_featured': False,
            },
            {
                'name': 'Toyota Fortuner',
                'category': 'suv',
                'seats': 7,
                'price_per_km': 25,
                'price_per_day': 7000,
                'description': 'Luxury SUV for VIP travel, weddings, and premium outstation trips.',
                'features': 'AC, Leather Interior, GPS, Sunroof',
                'is_featured': True,
            },
            {
                'name': 'Mini Bus 27 Seater',
                'category': 'bus',
                'seats': 27,
                'price_per_km': 35,
                'price_per_day': 12000,
                'description': 'Ideal for large group pilgrimages, school trips, and events.',
                'features': 'AC, Comfortable Seating, GPS, First Aid Kit',
                'is_featured': False,
            },
        ]

        for data in vehicles:
            Vehicle.objects.create(**data)

        services = [
            {
                'title': 'Outstation Trips',
                'icon': 'bi-signpost-split',
                'description': 'One-way and round-trip travel to any city in India with experienced drivers and well-maintained vehicles.',
                'sort_order': 1,
            },
            {
                'title': 'Airport Transfers',
                'icon': 'bi-airplane',
                'description': 'Punctual pickup and drop services to all major airports. Flight tracking included.',
                'sort_order': 2,
            },
            {
                'title': 'Wedding & Events',
                'icon': 'bi-heart',
                'description': 'Decorate your special occasions with our premium fleet and professional chauffeurs.',
                'sort_order': 3,
            },
            {
                'title': 'Corporate Travel',
                'icon': 'bi-briefcase',
                'description': 'Reliable transport solutions for business meetings, conferences, and employee travel.',
                'sort_order': 4,
            },
            {
                'title': 'Pilgrimage Tours',
                'icon': 'bi-building',
                'description': 'Comfortable group travel to temples and religious destinations across India.',
                'sort_order': 5,
            },
            {
                'title': 'Local City Tours',
                'icon': 'bi-geo-alt',
                'description': 'Explore cities at your own pace with hourly and full-day rental packages.',
                'sort_order': 6,
            },
        ]

        for data in services:
            Service.objects.create(**data)

        testimonials = [
            {
                'customer_name': 'Rajesh Sharma',
                'location': 'Jaipur',
                'rating': 5,
                'review': 'Excellent service! Booked an Innova for our family trip to Udaipur. Driver was polite and the car was spotless.',
            },
            {
                'customer_name': 'Priya Mehta',
                'location': 'Delhi',
                'rating': 5,
                'review': 'Used Choudhary Travels for airport pickup at 4 AM. They were on time and the ride was very comfortable.',
            },
            {
                'customer_name': 'Amit Kumar',
                'location': 'Mumbai',
                'rating': 4,
                'review': 'Great rates for outstation travel. No hidden charges. Will definitely book again for our next trip.',
            },
        ]

        for data in testimonials:
            Testimonial.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(vehicles)} vehicles, {len(services)} services, '
            f'and {len(testimonials)} testimonials.'
        ))