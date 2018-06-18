#!/bin/sh

echo "------ Starting APP ------"
USER="abhinavgarg"
MAIL="test@zomato.com"
PASS="zomato"

if [-z $VCAP_APP_PORT];
	then SERVER_PORT=5000;
	else SERVER_PORT=$VCAP_APP_PORT;
fi

echo ------ Create database tables ------
#python manage.py makemigrations zomato_scrapers
#python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('${USER}', '${MAIL}', '${PASS}')" | python manage.py shell

echo ------Starting server ------
#gunicorn zomato_main.wsgi --workers 2 --timeout 10000 --bind 0.0.0.0:8000
gunicorn zomato_main.wsgi --workers 2 --timeout 10000
