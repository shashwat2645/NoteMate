from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        
        User.objects.filter(username='admin').delete()
        
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
