release: python manage.py makemigrations && python manage.py migrate --fake
web: gunicorn scheduling_API.wsgi