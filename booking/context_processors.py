from django.conf import settings


def business_info(request):
    """Expose business contact details to all templates."""
    return {
        'business_name': settings.BUSINESS_NAME,
        'business_tagline': settings.BUSINESS_TAGLINE,
        'business_phone': settings.BUSINESS_PHONE,
        'business_email': settings.BUSINESS_EMAIL,
        'business_whatsapp': settings.BUSINESS_WHATSAPP,
        'business_address': settings.BUSINESS_ADDRESS,
    }
