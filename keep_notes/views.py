from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Note
from profile_html.models import UserProfile
import json

@login_required
def notes_dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'keep_notes/dashboard.html', {'user_profile': user_profile})

@csrf_exempt
@login_required
def sync_notes_api(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # 1. ABURID (POST) - Waxaa ku jira File-ka
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        device_info = request.POST.get('device_info', 'Unknown')
        file_attachment = request.FILES.get('file_attachment')

        note = Note.objects.create(
            user_profile=user_profile,
            title=title,
            content=content,
            device_info=device_info,
            file_attachment=file_attachment
        )
        return JsonResponse({'status': 'success', 'note_id': note.id})

    # 2. AKHRIS (GET)
    elif request.method == 'GET':
        notes = Note.objects.filter(user_profile=user_profile).values(
            'id', 'title', 'content', 'device_info', 'updated_at', 'file_attachment'
        )
        return JsonResponse({'status': 'success', 'notes': list(notes)})

    # 3. TIRTIRID (DELETE)
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        note = get_object_or_404(Note, id=data.get('note_id'), user_profile=user_profile)
        note.delete()
        return JsonResponse({'status': 'success'})

    # 4. WAX KA BEDDEL (PUT)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        note = get_object_or_404(Note, id=data.get('note_id'), user_profile=user_profile)
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        note.save()
        return JsonResponse({'status': 'success'})