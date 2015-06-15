from .common import *

DEBUG=True

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

#[email]
SERVER_EMAIL = 'marcioacsantiago@gmail.com'
SERVER_EMAIL_PASS = 'mgderune2k'
EMAIL_HOST_SMTP = 'smtp.gmail.com:587'
CLIENT_EMAIL = 'marcio704@yahoo.com.br'