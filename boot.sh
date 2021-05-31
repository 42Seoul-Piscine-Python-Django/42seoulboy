#!/bin/sh

rm LOCAL
lsof -t -i tcp:8000 | xargs kill -9
location="$(pwd)/.venv"

source $location/bin/activate

python manage.py runserver
