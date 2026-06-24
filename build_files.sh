#!/bin/bash
echo "BUILD START"
python3 -m pip install -r requirements.txt --break-system-packages
python3 manage.py collectstatic --noinput --clear
python3 manage.py migrate --noinput
python3 manage.py ensure_superuser
python3 -c "import django; django.setup(); from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', '1234')" || true
echo "BUILD END"



