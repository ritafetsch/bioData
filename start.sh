#!/bin/bash
set -e

# Run migrations
python manage.py migrate

# Populate data
python midtermBioData/scripts/populate_data.py

# Start the application
gunicorn midtermProject.wsgi:application --bind 0.0.0.0:$PORT