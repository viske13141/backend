#!/bin/bash
python manage.py migrate
gunicorn your_project_name.wsgi:application