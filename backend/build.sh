#!/usr/bin/env bash
set -e

echo "=== Python Version ==="
python --version

echo "=== Creating data directory ==="
mkdir -p /var/data

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Seeding data ==="
python manage.py seed_data

echo "=== Build complete! ==="