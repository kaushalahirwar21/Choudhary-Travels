from django.core.management.base import BaseCommand
from booking.models import Vehicle

class Command(BaseCommand):
    help = 'Update the image for a specific vehicle'

    def handle(self, *args, **options):
        vehicle_name = 'Mahindra Bolero Neo'
        new_image_path = 'vehicles/car.png'

        try:
            vehicle = Vehicle.objects.get(name=vehicle_name)
            vehicle.image = new_image_path
            vehicle.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully updated image for '{vehicle_name}'."))
        except Vehicle.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Vehicle '{vehicle_name}' not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))