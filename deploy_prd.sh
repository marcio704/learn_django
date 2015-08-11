#Kill current uwsgi instance
killall -9 uwsgi

#Set env variable to prd settings
export DJANGO_SETTINGS_MODULE=learn_django.settings.prd


#Kill current celery instance
killall -9 celery
#Start threads for rabbitMQ consumers
nohup celery -A blog worker -l info > /tmp/celery.log 2>&1 &

#Kill current es instance
killall -9 java
#Start elasticsearch nodes
nohup /etc/elasticsearch-1.6.0/bin/elasticsearch > /tmp/celery.log 2>&1 &


#Start server
nohup uwsgi --ini deploy.ini:prd > /dev/null 2>&1 &
