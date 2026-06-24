from django import template
from booking.models import Booking

register = template.Library()


@register.filter
def split_features(value):
    """Split comma-separated vehicle features into a list."""
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]

@register.simple_tag
def get_recent_bookings():
    return Booking.objects.exclude(status='Cancelled').order_by('-created_at')[:10]