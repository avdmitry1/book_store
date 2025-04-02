#!/usr/bin/sh

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# command - ./run_migrations.sh
