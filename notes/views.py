import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class ExportNotes(View):
    def get(self, request):
        from notes.models import Note
        notes = Note.objects.filter(user=request.user)
        data = [{'title': n.title, 'content': n.content, 'created_at': n.created_at.isoformat(), 'updated_at': n.updated_at.isoformat()} for n in notes]
        return JsonResponse({'notes': data})


@method_decorator(login_required, name='dispatch')
class ImportNotes(View):
    def post(self, request):
        from notes.models import Note
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