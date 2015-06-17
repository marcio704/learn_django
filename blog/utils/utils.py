import math
import smtplib
import random
import string

from email.mime.text import MIMEText
from email.header import Header
from django.conf import settings

#Utililty/ reusable functions:

def generate_token():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(settings.TOKEN_SIZE))


def divide_list_by_two (whole_list):
    half_size_ceil = int(math.ceil(len(whole_list)/2))  
    half_size_floor = int(math.floor(len(whole_list)/2))
    list_1 = whole_list [:half_size_ceil]
    list_2 = whole_list [len(whole_list) - half_size_floor:]

    return {"list_1": list_1, "list_2": list_2}


def send_email(to_address, msg):

	body = MIMEText(msg.encode('utf-8'), 'plain', 'utf-8')
	body['From'] = settings.SMTP_EMAIL_SENDER
	body['To'] = to_address
	body['Subject'] = Header('EasyDjango!', 'utf-8')

	# The actual mail send
	server = smtplib.SMTP(settings.SMTP_HOST)
	server.starttls()
	server.login(settings.SMTP_SERVER_LOGIN, settings.SMTP_SERVER_PASSWORD)
	server.sendmail(settings.SMTP_EMAIL_SENDER, to_address, body.as_string())
	server.quit()
