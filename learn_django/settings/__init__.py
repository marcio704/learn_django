import os

if os.environ["DJANGO_SETTINGS_MODULE"] == "learn_django.settings.prd":
	from .prd import *
else:
	from .dev import *	