""" 
	- Run "sudo pip install django-crontab" to install cron module.
	- Run "python manage.py crontab add" in order to add these functions to cron scheduling
"""

from .models import Contact
from django.utils import timezone
from .utils import utils

def send_contact_email():
	list_contact = Contact.objects.filter(is_email_sent=False)
	to_email = 'marcio704@yahoo.com.br'
	for contact in list_contact:
	    try:
	        msg = """
	            From: {0}
	            Email: {1}
	            Phone: {2}
	            Date: {3}
	            Message: {4}
	        """.format(contact.name, contact.email, contact.phone, contact.creation_date, contact.message)
	        utils.send_email(to_email, msg)
	        contact.is_email_sent = True
	        contact.save()

	    except Exception as ex:
	        print ('Error on sending email: {0}'.format(ex))

