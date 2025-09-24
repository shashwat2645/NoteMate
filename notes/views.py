from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from NoteMate.forms import NoteForm
from notes.models import Note
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    if request.user.is_anonymous:
        return redirect('login')
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'index.html',{'notes':notes})

@login_required
def create_note(request):
    if request.method=="POST":
        name = request.POST.get('title')
        desc = request.POST.get('content')
    
        if name!="" and desc!="":
            note = Note(
                user=request.user, 
                title=name,
                content=desc
            )
            note.save()
            messages.success(request, "Note created successfully!")
            return redirect('index')

    return render(request, 'create_note.html')

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == "POST":
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()

        messages.success(request, "Note updated successfully!")
        return redirect('index')

    return render(request, 'edit_note.html', {'note': note})

@login_required
def delete_note(request, note_id):
    if request.method == "POST":
        note = note = get_object_or_404(Note, id=note_id, user=request.user)
        note.delete()
    return redirect('index')


def register(request):
    if request.method == "POST":
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not email or not password or not password2:
            messages.error(request, "All fields are required!")
            return redirect('register')

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('register')

        username = email.split('@')[0] 
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')


def login_user(request):
    if request.user.is_authenticated:  
        return redirect('index')
    if request.method == "POST":
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "All fields are required!")
            return redirect('login')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')

        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')
