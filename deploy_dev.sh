#Kill current uwsgi instance
killall -9 uwsgi

#Set env variable to prd settings
export DJANGO_SETTINGS_MODULE=learn_django.settings.dev

#Start threads for rabbitMQ consumers
killall -9 celery
nohup celery -A blog worker -l info > /tmp/celery.log 2>&1 &

#Start nodes for elasticsearch

#Start server
uwsgi --ini deploy.ini:local