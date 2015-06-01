import math
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from django.conf import settings

#Utililty/ reusable functions:

def divide_list_by_two (whole_list):
    half_size_ceil = int(math.ceil(len(whole_list)/2))  
    half_size_floor = int(math.floor(len(whole_list)/2))
    list_1 = whole_list [:half_size_ceil]
    list_2 = whole_list [len(whole_list) - half_size_floor:]

    return {"list_1": list_1, "list_2": list_2}


def send_email(to_address, msg):

	from_address = settings.SERVER_EMAIL
	# Credentials (if needed)
	username = settings.SERVER_EMAIL
	password = settings.SERVER_EMAIL_PASS

	body = MIMEText(msg.encode('utf-8'), 'plain', 'utf-8')
	body['From'] = settings.SERVER_EMAIL
	body['To'] = settings.CLIENT_EMAIL
	body['Subject'] = Header('LearnDjango!', 'utf-8')

	# The actual mail send
	server = smtplib.SMTP(settings.EMAIL_HOST_SMTP)
	server.starttls()
	server.login(username,password)
	server.sendmail(from_address, to_address, body.as_string())
	server.quit()