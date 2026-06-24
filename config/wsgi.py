"""
WSGI config for Choudhary Travels project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
app = application

# Server startup migrations and superuser password setup
try:
    from django.core.management import call_command
    from django.contrib.auth import get_user_model
    
    call_command('migrate', interactive=False)
    
    User = get_user_model()
    user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
    user.set_password('1234')
    user.is_staff = True
    user.is_superuser = True
    user.save()
except Exception as e:
    import sys
    sys.stderr.write(f"Startup task error: {e}\n")
