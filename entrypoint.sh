#!/bin/sh
set -e

uv run python manage.py migrate

uv run python manage.py collectstatic --noinput

# Register cron jobs and start cron service
uv run python manage.py crontab add
service cron start

exec uv run gunicorn Strike1v1.wsgi:application --bind 0.0.0.0:8000