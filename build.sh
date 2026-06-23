#!/usr/bin/env bash

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