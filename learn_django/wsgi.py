"""
WSGI config for learn_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

"""
Setting dev environment as default if DJANGO_SETTINGS_MODULE environment variable is not defined:
In order to define it, run the following command on your console: 
  	develop: 	export DJANGO_SETTINGS_MODULE=learn_django.settings.dev
	production: export DJANGO_SETTINGS_MODULE=learn_django.settings.prd
"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE", "learn_django.settings.dev"))

application = get_wsgi_application()
