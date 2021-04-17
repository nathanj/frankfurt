#!/bin/sh
./venv/bin/python ./manage.py migrate
exec ./venv/bin/gunicorn mysite.wsgi
