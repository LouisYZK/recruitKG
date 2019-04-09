set DJANGO_SETTINGS_MODULE=backend.settings.prod
set DJANGO_SECRET_KEY='verybadsecret!!!'
gunicorn backend.wsgi:application -c gunicorn.conf.py