from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random


def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_verified = models.BooleanField(default=False)
    verification_otp = models.CharField(max_length=6, default=generate_otp, editable=False)
    verification_otp_expires = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def generate_new_otp(self):
        self.verification_otp = generate_otp()
        self.verification_otp_expires = timezone.now() + timezone.timedelta(minutes=10)
        self.save()