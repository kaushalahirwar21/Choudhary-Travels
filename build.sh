#!/usr/bin/env bash
<<<<<<< HEAD

# Exit on error
set -o errexit

# Poetry configuration
# python -m pip install poetry
# python -m poetry config virtualenvs.in-project true
# python -m poetry install --no-root

# Pip configuration
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
=======
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py ensure_superuser
>>>>>>> 85581e2fb793ac61c7fcc6a98dec5ac5ab2ee5b8
