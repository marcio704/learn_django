import pika
import logging
import sys
import json
import string
from django.conf import settings

"""
 Run this inside your RabbitMQ Server in order to create your RMQ user:

	# rabbitmqctl add_user marcio mgderune2k
	# rabbitmqctl set_permissions -p / marcio ".*" ".*" ".*"

	Don't forget to allow external access to port 5672 where RabbitMQ is listening.
"""

class RabbitMessageProducer():
	host = settings.RABBIT_MQ_HOST
	port = settings.RABBIT_MQ_PORT
	user = settings.RABBIT_MQ_USER
	password = settings.RABBIT_MQ_PASSWORD

	def produce_email_message (self, to_address, msg):
		logging.basicConfig()

		credentials = pika.PlainCredentials(self.user, self.password)
		parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
		connection = pika.BlockingConnection(parameters)
		
		channel = connection.channel()

		channel.exchange_declare(exchange='emails', type='fanout')
		channel.queue_declare(queue='task_queue', durable=True)
		channel.queue_bind(exchange='emails', queue='task_queue')

		json_message = json.dumps({'to': to_address, 'message':  msg.encode('utf-8').decode('latin-1')})

		channel.basic_publish(exchange='emails',
		                      routing_key='',
		                      body=json_message,
		                      properties=pika.BasicProperties(
		                      	delivery_mode = 2, # make message persistent
		                      ))
		connection.close()
