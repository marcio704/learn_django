from .common import *

DEBUG=False
ALLOWED_HOSTS = ['*']
SITE_URL = "http://www.easydjango.com"


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'learn_django',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

MEDIA_ROOT = '/home/ubuntu/dev/learn_django/media'
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = "uploads/"

STATIC_ROOT = '/home/ubuntu/dev/learn_django/static'
STATIC_URL = '/static/'

LOCALE_PATHS = (
    '/home/ubuntu/dev/learn_django/locale',
)

""" 
    For aditional secret settings such as E-mails, Passwords and Tokens, create an addtional file. 
    For example, create "secret_settings.py" inside app root directory, this file should not be shared through a Version Control System like GIT or SVN.

    File format should look like:
        SERVER_EMAIL = 'server@email.com'
        SERVER_EMAIL_PASS = 'password'
        EMAIL_HOST_SMTP = 'smtp.gmail.com:587'
        CLIENT_EMAIL = 'client@email.com'

    For later use, do like:

    from django.conf import settings
    email = settings.SERVER_EMAIL
"""
from blog.secret_settings import *