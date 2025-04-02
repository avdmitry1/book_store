#!/bin/bash

echo "Deleting migrations and database..."


# Remove the SQLite database file
# This will delete all data that was previously stored
rm -f db.sqlite3

# Remove all files in the migrations directories, except for __init__.py
# This will delete any existing migrations and their compiled versions
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "Migrations and database removed."

# Reapply the migrations
# This will recreate the database and all the tables
# But it will not delete any data that was previously stored
echo "Reapplying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser..."
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
DJANGO_SUPERUSER_PASSWORD=admin \
python manage.py createsuperuser --noinput

echo "Reset complete! Superuser: admin / admin"

python manage.py generate_dummy_data

echo "Dummy data generated!"