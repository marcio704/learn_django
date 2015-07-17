#Kill current uwsgi instance
killall -9 uwsgi

#Set env variable to prd settings
export DJANGO_SETTINGS_MODULE=learn_django.settings.prd

#Start threads for rabbitMQ consumers
killall -9 celery
nohup celery -A blog worker -l info > /tmp/celery.log 2>&1 &

#Start elasticsearch nodes
nohup /etc/elasticsearch-1.6.0/bin/elasticsearch > /tmp/celery.log 2>&1 &


#Start server
nohup uwsgi --ini deploy.ini:prd > /dev/null 2>&1 &
