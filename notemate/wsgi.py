"""
WSGI config for notemate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notemate.settings')

application = django.core.wsgi.get_wsgi_application()
django.setup()

if os.getenv('DATABASE_URL'):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    admin = User.objects.filter(username='admin').first()
    if not admin or not admin.is_staff:
        if admin:
            admin.is_staff = True
            admin.is_superuser = True
            admin.is_active = True
            admin.set_password('Admin@123')
            admin.save()
        else:
            admin = User.objects.create_user(username='admin', email='admin@notemate.com', password='Admin@123')
            admin.is_staff = True
            admin.is_superuser = True
            admin.is_active = True
            admin.save()
            from accounts.models import Profile
            Profile.objects.get_or_create(user=admin, defaults={'email_verified': True})
        print("Admin user fixed on deployment")
