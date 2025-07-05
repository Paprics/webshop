#!/bin/bash

python src/manage.py migrate
python src/manage.py check
python src/manage.py collectstatic --no-input

gunicorn -w${WSGI_WORKERS} -b 0.0.0.0:${WSGI_PORT} --chdir /app/src config.wsgi:application --log-level ${WSGI_LOG_LEVEL}

#python src/manage.py runserver 0.0.0.0:8000
