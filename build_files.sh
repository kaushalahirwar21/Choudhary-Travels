#!/bin/bash
echo "BUILD START"
python3 -m pip install -r requirements.txt --break-system-packages
python3 manage.py collectstatic --noinput --clear
python3 manage.py migrate --noinput
python3 manage.py ensure_superuser
python3 -c "import django; django.setup(); from django.contrib.auth import get_user_model; User = get_user_model(); user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'}); user.set_password('1234'); user.is_staff = True; user.is_superuser = True; user.save(); print('Superuser created/updated')" || true
echo "BUILD END"



