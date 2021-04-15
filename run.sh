#!/bin/sh
./venv/bin/python ./manage.py migrate
./venv/bin/gunicorn mysite.wsgi

