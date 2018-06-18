# Zomato Scraper

This is a celery based Django app.
You need to have the following on your system before you can run the app :
Python2
Postgres
RabbitMQ
Anaconda

1. Once these are installed:
i) setup python2 based virtual environment in Anaconda
ii) conda activate 'Virtual_env_name'

2. Create a Database in Postgres under a particular user
i) in settings.py file in zomato_main edit the database config:

DATABASES = {  ####Give your own db configurations
    'default': {#        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.#        'NAME': #'db_calypso',                      # Or path to database file if using sqlite3.
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.#        'NAME': #'db_calypso',                      # Or path to database file if using sqlite3.
        'NAME': 'zomatodb',                      # Or path to database file if using sqlite3.
        'USER': 'vagrant',                      # Not used with sqlite3.
        'PASSWORD': 'admin',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ii) In root directory run:
python manage.py shell
from django.contrib.auth.models import User;
User.objects.create_superuser('[USER]', '[MAIL]', '[PASS]');

3. Start RabbitMQ

As Celery uses a queuing and worker based system, you need to send the task to the queue

4. First start the rest server using command:
gunicorn zomato_main.wsgi --workers 2 --timeout 10000

At localhost:prtnumber/admin
Go to periodic tasks
Press Add Periodic Task on Top right
Name the task
Add the Task from the list
Give an Interval (When should the scraper run periodically)
If you see no interval click on plus sign and add one


5. Now start the Beat using (in new terminal)
celery -A zomato_main beat -l info -S django

6. Start worker using (in 3rd terminal)
celery worker -A zomato_main --loglevel=DEBUG

P.S. - If you want to see the scraper run immediately give a time period of 10 sec. Once you see in beat that task has been sent to queue, stop beat so that it sends no new tasks to the queue. You can see the task running in worker.

7. Once the scraper gets all the data, it served on end point:
http://localhost:4567/scrapers/zomato/get_all/

P.S. - The API is a bit slow because it loads tons of data, a better design would be send the basic restaurant info first and send the comments later on where restaurant name is sent as query parameter from front end every time a restaurant is clicked.
