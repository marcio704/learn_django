#Kill current uwsgi instance
killall -9 uwsgi

#Set env variable to prd settings
export DJANGO_SETTINGS_MODULE=learn_django.settings.dev

#Start threads for rabbitMQ consumers
#nohup python start_consumers.py > /tmp/consumers.log 2>&1 &

#Start server
uwsgi --ini deploy.ini:local