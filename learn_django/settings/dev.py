from .common import *

DEBUG=True
SITE_URL = "http://localhost:8000"

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

MEDIA_ROOT = '/home/marcio/dev/learn_django/media'
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = "uploads/"

STATIC_ROOT = '/home/marcio/dev/learn_django/static'
STATIC_URL = '/static/'


LOCALE_PATHS = (
    '/home/marcio/dev/learn_django/locale',
)

#[email] Tip: Amazon SES or MailGun are a very nice tools for email sending
SMTP_EMAIL_SENDER = 'admin@email.com'
SMTP_SERVER_LOGIN = 'postmaster@email.com'
SMTP_SERVER_PASSWORD = 'asdasdasd1231231eqwda'
SMTP_HOST = 'smtp.mailgun.org'
SMTP_HOST_PORT = 587
CLIENT_EMAIL = 'marcio704@email.com.br'

#Configs for RabbitMQ: Responsible for getting contact info (producer), queue and send email (consumer)
RABBIT_MQ_HOST = 'YOUR_IP_OR_LOCALHOST'
RABBIT_MQ_PORT = 'PORT_NUMBER'
RABBIT_MQ_USER = 'USER'
RABBIT_MQ_PASSWORD = 'PASSWORD'

ELASTIC_SEARCH_INDEX = 'easy_django'