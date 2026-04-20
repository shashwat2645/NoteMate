from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting create_admin command...")
        User = get_user_model()
        
        existing = User.objects.filter(username='admin').first()
        if existing:
            print(f"Found existing admin: is_staff={existing.is_staff}, is_superuser={existing.is_superuser}")
            existing.is_staff = True
            existing.is_superuser = True
            existing.is_active = True
            existing.set_password('Admin@123')
            existing.save()
            print("Updated existing admin user")
        else:
            print("Creating new admin user...")
            user = User.objects.create_user(
                username='admin',
                email='admin@notemate.com',
                password='Admin@123'
            )
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            Profile.objects.get_or_create(user=user, defaults={'email_verified': True})
            print("Created new admin user")
        
        # Verify
        admin = User.objects.get(username='admin')
        print(f"Final admin status: is_staff={admin.is_staff}, is_superuser={admin.is_superuser}, is_active={admin.is_active}")
