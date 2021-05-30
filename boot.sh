#!/bin/sh

lsof -t -i tcp:8000 | xargs kill -9
location="$(pwd)/django_venv"

source $location/bin/activate

cd d04
python manage.py runserver
