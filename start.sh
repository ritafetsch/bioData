#!/bin/bash
set -e

echo "Starting Django deployment"

echo "Running migrations..."
python manage.py migrate

echo "Populating data..."
python midtermBioData/scripts/populate_data.py

echo "Starting gunicorn server..."
gunicorn midtermProject.wsgi:application --bind 0.0.0.0:$PORT