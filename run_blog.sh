#Run consumer thread for emails MQ:
python start_consumers.py

#Start the server
uwsgi --ini  deploy.ini:local


