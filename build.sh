#!/bin/bash

echo "BUILD SCRIPT STARTED: Attempting to run migrations..."

python manage.py migrate --no-input

echo "BUILD SCRIPT FINISHED: Migrations complete."