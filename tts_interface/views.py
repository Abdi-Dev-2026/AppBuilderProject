import os
import uuid
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from asgiref.sync import async_to_sync
import edge_tts
from .models import TTSSetting

async def generate_somali_speech(text, voice_name, output_path):
    if voice_name == "maxamed":
        voice = "so-SO-MuuseNeural"
    else:
        voice = "so-SO-UbaxNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def tts_interface_view(request):
    tts_setting, created = TTSSetting.objects.get_or_create(id=1, defaults={'max_characters': 1000})
    max_chars = tts_setting.max_characters

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        text = request.POST.get('text', '').strip()
        voice = request.POST.get('voice', 'faiza')

        if len(text) > max_chars:
            return JsonResponse({
                'status': 'error', 
                'message': f'Fariintu waxay dhaaftay xadka laguu oggolaaday oo ah {max_chars} xaraf!'
            }, status=400)
        
        if not text:
            return JsonResponse({'status': 'error', 'message': 'Fadlan qor qoraal munaasab ah!'}, status=400)

        tts_dir = os.path.join(settings.MEDIA_ROOT, 'tts_voices')
        if not os.path.exists(tts_dir):
            os.makedirs(tts_dir)

        user_identifier = request.user.username if request.user.is_authenticated else 'guest'
        unique_id = uuid.uuid4().hex[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        file_name = f"tts_{voice}_{user_identifier}_{timestamp}_{unique_id}.mp3"
        output_path = os.path.join(tts_dir, file_name)
        file_url = f"{settings.MEDIA_URL}tts_voices/{file_name}"

        try:
            async_to_sync(generate_somali_speech)(text, voice, output_path)
            return JsonResponse({'status': 'success', 'audio_url': file_url})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Waxaa dhacay khalad: {str(e)}'}, status=500)

    return render(request, 'tts_interface/tts_interface.html', {
        'max_chars': max_chars,
        'tts_setting': tts_setting
    })