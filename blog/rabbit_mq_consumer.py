import pika
import time
import json
import threading
import string
from .utils import utils
from django.conf import settings

"""
 Run this inside your RabbitMQ Server in order to create your RMQ user:

	# rabbitmqctl add_user marcio mgderune2k
	# rabbitmqctl set_permissions -p / marcio ".*" ".*" ".*"

	Don't forget to allow external access to port 5672 where RabbitMQ is listening.
"""

class RabbitMessageConsumer(object):
    host = settings.RABBIT_MQ_HOST
    port = settings.RABBIT_MQ_PORT
    user = settings.RABBIT_MQ_USER
    password = settings.RABBIT_MQ_PASSWORD
    
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        #thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
 
    def run(self):
        self.consume_email_message()

    def consume_email_message (self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.exchange_declare(exchange='emails', type='fanout')
        channel.queue_declare(queue='task_queue', durable=True)
        channel.queue_bind(exchange='emails', queue='task_queue')
        print ('1 {0}'.format(' [*] Waiting for messages. To exit press CTRL+C'))

        def callback(ch, method, properties, body):
            json_message = json.loads(body)
            utils.send_email(json_message["to"], "FROM MQ: {0}".format(json_message["message"].encode('latin-1') ) )
            ch.basic_ack(delivery_tag = method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue='task_queue')

        channel.start_consuming()
