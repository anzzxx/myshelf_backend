#!/usr/bin/env bash
# install dependencies
pip install -r requirements.txt
# collect static files
python manage.py collectstatic --noinput
# migrate the database
python manage.py migrate