"""
WSGI config for Online_learning project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
import sys
import os

from django.core.wsgi import get_wsgi_application



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Online_learning.settings")

sys.path.append('/venv/lib/python3.6/site-packages')
sys.path.append('/usr/lib64/python3.6/site-packages')

application = get_wsgi_application()
