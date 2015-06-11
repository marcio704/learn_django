#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	"""Setting dev environment as default if DJANGO_SETTINGS_MODULE environment variable is not defined:
	   In order to define it, run the following command on your console: 
	   	develop: 	export DJANGO_SETTINGS_MODULE=learn_django.settings.dev
		production: export DJANGO_SETTINGS_MODULE=learn_django.settings.prd
	"""
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE", "learn_django.settings.dev"))

	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
