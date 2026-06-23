from django import template
<<<<<<< HEAD

register = template.Library()


@register.filter
def split_features(value):
    """Split comma-separated vehicle features into a list."""
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]
=======
from booking.models import Booking

register = template.Library()

@register.simple_tag
def get_recent_bookings():
    return Booking.objects.exclude(status='Cancelled').order_by('-start_time')[:10]
>>>>>>> 85581e2fb793ac61c7fcc6a98dec5ac5ab2ee5b8
