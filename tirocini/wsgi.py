# """
# WSGI config for tirocini project.
#
# It exposes the WSGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
# """
#
# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tirocini.settings')
#
# application = get_wsgi_application()

import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/administrator/django_websites/tirocini/tirocini-venv/lib/python3.8/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/administrator/django_websites/tirocini/')
sys.path.append('/home/administrator/django_websites/tirocini/tirocini')

#to set enviroment settings for Django apps
os.environ['DJANGO_SETTINGS_MODULE'] = 'tirocini.settings'

# Activate your virtual env
activate_env=os.path.expanduser('/home/administrator/django_websites/tirocini/tirocini-venv/bin/activate_this.py')
exec(open(activate_env).read(), {'__file__': activate_env})

application = get_wsgi_application()