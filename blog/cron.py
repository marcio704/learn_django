from .models import Contact
from django.utils import timezone
from .utils import utils
from django.conf import settings

""" 
	This cron feature uses django-crontab module, see specifications here: https://github.com/kraiz/django-crontabs

	- Run "sudo pip install django-crontab" to install cron module.
	- Configure settings.py
	- Run "python manage.py crontab add" in order to add these functions to cron scheduling
"""

def send_contact_email():
	list_contact = Contact.objects.filter(is_email_sent=False)
	to_email = settings.CLIENT_EMAIL
	for contact in list_contact:
	    try:
	        msg = """
	            From: {0}
	            Email: {1}
	            Date: {2}
	            Message: {3}
	        """.format(contact.name, contact.email, contact.creation_date, contact.message)
	        utils.send_email(to_email, msg)
	        contact.is_email_sent = True
	        contact.save()

	    except Exception as ex:
	        print ('Error on sending email: {0}'.format(ex))

