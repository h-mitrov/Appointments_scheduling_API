release: python manage.py migrate
web: sh -c 'cd ./scheduling_api/ && exec gunicorn scheduling_api.wsgi'