"""
WSGI config for notemate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notemate.settings')

from django.conf import settings
from django.db import connection

if os.getenv('DATABASE_URL'):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM django_migrations LIMIT 1")
    except:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])

application = get_wsgi_application()
