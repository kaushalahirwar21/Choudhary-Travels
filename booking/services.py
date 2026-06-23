import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _format_booking_message(booking):
    """Build WhatsApp notification text for a new booking."""
    lines = [
        '🚗 *New Booking — Choudhary Travels*',
        '',
        f'👤 *Name:* {booking.customer_name}',
        f'📞 *Phone:* +91 {booking.phone}',
    ]
    if booking.email:
        lines.append(f'📧 *Email:* {booking.email}')
    lines.extend([
        f'📍 *From:* {booking.pickup_location}',
        f'📍 *To:* {booking.drop_location}',
        f'📅 *Pickup:* {booking.pickup_date.strftime("%d %b %Y")}',
    ])
    if booking.return_date:
        lines.append(f'📅 *Return:* {booking.return_date.strftime("%d %b %Y")}')
    if booking.pickup_time:
        lines.append(f'⏰ *Time:* {booking.pickup_time.strftime("%I:%M %p")}')
    lines.extend([
        f'🚙 *Vehicle:* {booking.vehicle_name}',
        f'👥 *Passengers:* {booking.passengers}',
        f'🔄 *Trip:* {booking.get_trip_type_display()}',
    ])
    if booking.message:
        lines.extend(['', f'💬 *Notes:* {booking.message}'])
    lines.extend(['', f'🆔 Booking ID: #{booking.pk}'])
    return '\n'.join(lines)


def _send_via_callmebot(message):
    """Send WhatsApp message using CallMeBot free API."""
    api_key = settings.CALLMEBOT_API_KEY
    phone = settings.CALLMEBOT_PHONE
    if not api_key or not phone:
        logger.warning('CallMeBot credentials not configured.')
        return False

    url = 'https://api.callmebot.com/whatsapp.php'
    params = {
        'phone': phone,
        'text': message,
        'apikey': api_key,
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        logger.error('CallMeBot notification failed: %s', exc)
        return False


def _send_via_twilio(message):
    """Send WhatsApp message using Twilio API."""
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_number = settings.TWILIO_WHATSAPP_FROM
    to_number = settings.TWILIO_WHATSAPP_TO

    if not all([account_sid, auth_token, from_number, to_number]):
        logger.warning('Twilio credentials not configured.')
        return False

    url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'
    try:
        response = requests.post(
            url,
            auth=(account_sid, auth_token),
            data={
                'From': from_number,
                'To': to_number,
                'Body': message,
            },
            timeout=15,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        logger.error('Twilio notification failed: %s', exc)
        return False


def send_booking_whatsapp(booking):
    """
    Send WhatsApp notification for a new booking.
    Returns True if sent successfully, False otherwise.
    """
    provider = settings.WHATSAPP_PROVIDER.lower()
    if provider in ('none', ''):
        logger.info('WhatsApp provider disabled; skipping notification.')
        return False

    message = _format_booking_message(booking)

    if provider == 'callmebot':
        return _send_via_callmebot(message)
    if provider == 'twilio':
        return _send_via_twilio(message)

    logger.warning('Unknown WhatsApp provider: %s', provider)
    return False


def process_new_booking(booking):
    """Post-booking business logic: notifications and status updates."""
    sent = send_booking_whatsapp(booking)
    if sent:
        booking.whatsapp_sent = True
        booking.save(update_fields=['whatsapp_sent', 'updated_at'])
    return sent
