#!/bin/sh
set -e

uv run python manage.py migrate

uv run python manage.py collectstatic --noinput

exec uv run gunicorn quality_management_tools.wsgi:application --bind 0.0.0.0:8000