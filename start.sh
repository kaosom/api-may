#!/bin/bash
set -o errexit

python manage.py migrate --noinput
exec gunicorn control_escolar_desit_api.wsgi:application

