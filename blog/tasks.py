from __future__ import absolute_import
from celery import shared_task
from .utils import utils

@shared_task
def send_email(to_address, message):
    try:
    	utils.send_email(to_address, message.encode('utf-8').decode('latin-1'))
    except Exception as inst:
    	print("ERRO!!!!! {0}".format(inst))


@shared_task
def ping_on_file(a, b):
    #  Called via CRON: configured at blog/settings/common.py
    f = open('/home/marcio/Documents/workfile', 'w')
    f.write('ping {0} {1}'.format(a, b))