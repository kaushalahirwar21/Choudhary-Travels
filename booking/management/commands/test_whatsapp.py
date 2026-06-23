"""
Management command to test WhatsApp notification setup.
Usage: python manage.py test_whatsapp
"""

from django.core.management.base import BaseCommand, CommandError

from booking.models import Vehicle
from booking.services import send_booking_whatsapp


class FakeBooking:
    """Fake booking object for testing notification format."""

    def __init__(self, pk=999):
        self.pk = pk
        self.customer_name = 'Test Customer'
        self.phone = '9876543210'
        self.email = 'test@example.com'
        self.pickup_location = 'Delhi'
        self.drop_location = 'Agra'
        self.pickup_date = '2024-12-25'
        self.return_date = '2024-12-28'
        self.pickup_time = '10:00'
        self.passengers = 4
        self.trip_type = 'round_trip'
        self.message = 'Special request: Window seat preferred'
        self.vehicle = Vehicle.objects.first()

    def __str__(self):
        return 'Test Booking'

    @property
    def vehicle_name(self):
        return self.vehicle.name if self.vehicle else 'Any Available'

    def get_trip_type_display(self):
        return 'Round Trip'


class Command(BaseCommand):
    help = 'Test WhatsApp notification setup and send a test booking notification'

    def handle(self, *args, **options):
        from django.conf import settings

        self.stdout.write(self.style.SUCCESS('═' * 60))
        self.stdout.write(self.style.SUCCESS('WhatsApp Notification Test'))
        self.stdout.write(self.style.SUCCESS('═' * 60))

        # Check configuration
        self.stdout.write('\n📋 Configuration Check:')
        provider = settings.WHATSAPP_PROVIDER
        self.stdout.write(f'  Provider: {provider or "None (disabled)"}')

        if not provider or provider.lower() == 'none':
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  WhatsApp notifications are disabled.'
                    '\n   Set WHATSAPP_PROVIDER env var to "callmebot" or "twilio"'
                ),
            )
            return

        if provider.lower() == 'callmebot':
            api_key = settings.CALLMEBOT_API_KEY
            phone = settings.CALLMEBOT_PHONE

            if not api_key:
                raise CommandError(
                    '❌ CALLMEBOT_API_KEY not configured. Set it as an env var.',
                )
            if not phone:
                raise CommandError(
                    '❌ CALLMEBOT_PHONE not configured. Set it as an env var.',
                )

            self.stdout.write(f'  API Key: {api_key[:10]}...')
            self.stdout.write(f'  Phone: {phone}')

        elif provider.lower() == 'twilio':
            account_sid = settings.TWILIO_ACCOUNT_SID
            from_num = settings.TWILIO_WHATSAPP_FROM
            to_num = settings.TWILIO_WHATSAPP_TO

            if not all([account_sid, from_num, to_num]):
                raise CommandError(
                    '❌ Twilio credentials not configured. '
                    'Set TWILIO_ACCOUNT_SID, TWILIO_WHATSAPP_FROM, TWILIO_WHATSAPP_TO env vars.',
                )

            self.stdout.write(f'  Account SID: {account_sid[:10]}...')
            self.stdout.write(f'  From: {from_num}')
            self.stdout.write(f'  To: {to_num}')

        # Create test booking
        self.stdout.write('\n📦 Creating fake booking...')
        booking = FakeBooking()
        self.stdout.write(f'  Customer: {booking.customer_name}')
        self.stdout.write(f'  Route: {booking.pickup_location} → {booking.drop_location}')
        self.stdout.write(f'  Type: {booking.get_trip_type_display()}')

        # Send test notification
        self.stdout.write('\n📨 Sending test notification...')
        success = send_booking_whatsapp(booking)

        if success:
            self.stdout.write(
                self.style.SUCCESS('✅ Notification sent successfully!')
                + '\n\nCheck your WhatsApp for the test message within 30 seconds.',
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Failed to send notification. '
                    'Check Django logs for error details.',
                ),
            )
            self.stdout.write('\nNote: Make sure you have internet connection.')

        self.stdout.write(self.style.SUCCESS('\n' + '═' * 60))
