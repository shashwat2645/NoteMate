from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            user.set_password('admin123')
            user.save()
        
        profile, profile_created = Profile.objects.get_or_create(
            user=user,
            defaults={'email_verified': True}
        )
        if profile_created:
            profile.email_verified = True
            profile.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        else:
            self.stdout.write('Admin user already exists')
        self.stdout.write(f'User: admin, Password: admin123, email_verified: {profile.email_verified}')
