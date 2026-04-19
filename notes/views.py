import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import NoteForm


@login_required
def note_list(request):
    """List all notes for the current user"""
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'notes/note_list.html', {'notes': notes})


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note created!')
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})


@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def note_update(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated!')
            return redirect('note_detail', note_id=note.id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'note': note})


@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted!')
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})


@method_decorator(login_required, name='dispatch')
class ExportNotes(View):
    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        data = [{'title': n.title, 'content': n.content, 'created_at': n.created_at.isoformat(), 'updated_at': n.updated_at.isoformat()} for n in notes]
        return JsonResponse({'notes': data})


@method_decorator(login_required, name='dispatch')
class ImportNotes(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            imported = 0
            for note_data in data.get('notes', []):
                Note.objects.create(
                    user=request.user,
                    title=note_data.get('title', 'Untitled'),
                    content=note_data.get('content', '')
                )
                imported += 1
            return JsonResponse({'imported': imported})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)