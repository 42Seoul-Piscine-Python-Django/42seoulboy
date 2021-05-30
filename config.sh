#!/bin/sh

# Install python virtual environment
location="$(pwd)/django_venv"

python3 -m venv $location

# Run installed virtual environment
source $location/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python -m django --version

pagename="d04"
django-admin startproject $pagename
cd $pagename
python3 manage.py startapp ex00
python3 manage.py startapp ex01
python3 manage.py startapp ex02
python3 manage.py startapp ex03

python3 manage.py migrate
