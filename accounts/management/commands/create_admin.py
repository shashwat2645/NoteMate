from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        user.set_password('admin123')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        profile, profile_created = Profile.objects.get_or_create(user=user)
        profile.email_verified = True
        profile.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS('Admin user created with password admin123'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user updated with password admin123'))
        self.stdout.write(f'username: admin, password: admin123, is_active: {user.is_active}, email_verified: {profile.email_verified}')
