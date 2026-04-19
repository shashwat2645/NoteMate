from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from .forms import RegistrationForm, LoginForm
from .emails import send_verification_email, send_welcome_email
from .models import Profile


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def verification_sent(request):
    return render(request, 'accounts/verification_sent.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            profile = Profile.objects.get(user=user)
            profile.generate_new_otp()
            send_verification_email(user, profile.verification_otp)
            messages.success(request, 'Registration successful! Check your email for verification OTP.')
            
            messages.success(request, 'Registration successful! Please check your email to verify your account.')
            return redirect(f'{reverse("verify_email")}?email={user.email}')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')
        
        if not otp or not email:
            messages.error(request, 'Please provide both email and OTP.')
            return render(request, 'accounts/verify_email.html', {'email': email})
        
        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)
        except (User.DoesNotExist, Profile.DoesNotExist):
            messages.error(request, 'Invalid email or OTP.')
            return render(request, 'accounts/verify_email.html', {'email': email})
        
        if profile.email_verified:
            messages.info(request, 'Email already verified. Please login.')
            return redirect('login')
        
        if profile.verification_otp != otp:
            messages.error(request, 'Invalid OTP.')
            return render(request, 'accounts/verify_email.html', {'email': email})
        
        if profile.verification_otp_expires and profile.verification_otp_expires < timezone.now():
            messages.error(request, 'OTP has expired. Please register again.')
            return redirect('register')
        
        profile.email_verified = True
        profile.verification_otp = ''
        profile.verification_otp_expires = None
        profile.save()
        
        user = profile.user
        user.is_active = True
        user.save()
        
        send_welcome_email(user)
        
        messages.success(request, 'Email verified! You can now log in.')
        return redirect('login')
    
    email = request.GET.get('email', '')
    return render(request, 'accounts/verify_email.html', {'email': email})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                profile = user.profile
                if not profile.email_verified:
                    messages.error(request, 'Please verify your email first.')
                    return render(request, 'accounts/login.html', {'form': form})
            except Profile.DoesNotExist:
                pass
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    from notes.models import Note
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')[:5]
    return render(request, 'accounts/dashboard.html', {'notes': notes})