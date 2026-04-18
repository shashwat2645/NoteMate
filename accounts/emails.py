from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_email(user, otp):
    subject = 'Verify your NoteMate account'
    text_message = f'Your OTP for email verification is: {otp}'
    html_message = render_to_string('accounts/verification_email.html', {
        'user': user,
        'otp': otp
    })
    
    email = EmailMultiAlternatives(
        subject,
        text_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.attach_alternative(html_message, 'text/html')
    email.send()


def send_welcome_email(user):
    subject = 'Welcome to NoteMate!'
    text_message = f'Welcome {user.username}! Thanks for joining NoteMate.'
    html_message = render_to_string('accounts/welcome_email.html', {
        'user': user
    })
    
    email = EmailMultiAlternatives(
        subject,
        text_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.attach_alternative(html_message, 'text/html')
    email.send()