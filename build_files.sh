#!/bin/bash
echo "BUILD START"
python3 -m pip install -r requirements.txt --break-system-packages
python3 manage.py collectstatic --noinput --clear
python3 manage.py migrate --noinput
python3 manage.py ensure_superuser
echo "BUILD END"


