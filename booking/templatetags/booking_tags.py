from django import template

register = template.Library()


@register.filter
def split_features(value):
    """Split comma-separated vehicle features into a list."""
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]
