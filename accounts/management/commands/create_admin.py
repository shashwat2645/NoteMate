from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import traceback

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        try:
            if not User.objects.filter(username='admin').exists():
                user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                self.stdout.write(self.style.SUCCESS(f'Admin user created: {user.username}'))
            else:
                self.stdout.write('Admin user already exists')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            traceback.print_exc()
