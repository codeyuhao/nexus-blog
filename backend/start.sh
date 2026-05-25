#!/usr/bin/env bash
set -e

PORT=${PORT:-8000}
echo "Starting server on port $PORT..."
gunicorn blog_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -