#Kill current uwsgi instance
killall -9 uwsgi

#Set env variable to prd settings
export DJANGO_SETTINGS_MODULE=learn_django.settings.prd

#Start threads for rabbitMQ consumers
python start_consumers.py &

#Start server
uwsgi -d --ini deploy.ini:prd