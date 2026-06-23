"""
<<<<<<< HEAD
WSGI config for Choudhary Travels project.
=======
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
>>>>>>> 85581e2fb793ac61c7fcc6a98dec5ac5ab2ee5b8
"""

import os

from django.core.wsgi import get_wsgi_application
<<<<<<< HEAD

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
=======
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'config.settings'
)
>>>>>>> 85581e2fb793ac61c7fcc6a98dec5ac5ab2ee5b8

application = get_wsgi_application()
