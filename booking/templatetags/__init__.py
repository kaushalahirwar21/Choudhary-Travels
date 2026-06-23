<<<<<<< HEAD
from django import template

register = template.Library()


@register.filter
def split_features(value):
    """Split comma-separated vehicle features into a list."""
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]
=======
# init
>>>>>>> 85581e2fb793ac61c7fcc6a98dec5ac5ab2ee5b8
