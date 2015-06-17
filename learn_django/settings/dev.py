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

#[email] Tip: Amazon SES is a very nice tool for email sending
SMTP_EMAIL_SENDER = 'your_sender@email.com'
SMTP_SERVER_LOGIN = 'your_STMP_login'
SMTP_SERVER_PASSWORD = 'your_STMP_password'
SMTP_HOST = 'your_SMTP_address'
CLIENT_EMAIL = 'your_receiver@email.com'