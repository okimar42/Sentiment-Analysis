#!/bin/bash
python3.11 manage.py migrate
python3.11 -m gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120 