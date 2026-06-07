from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatSession, ChatMessage
import requests
import json

def weydii_ai(prompt, xogta_hore=[]):
    """
    Shaqadan waxay farriinta u diraysaa Ollama si maxalli ah (100% Offline).
    Waxaan isticmaalaynaa qwen2.5-coder:1.5b oo ku habboon kombuyuutarkaaga.
    """
    url = "http://localhost:11434/api/generate"
    
    # SYSTEM PROMPT: Waxaan halkan ku baraynaa AI-ga inuu noqdo Maxamed AI oo Soomaali ah
    system_prompt = (
        "Role: Waxaad tahay Maxamed AI, caawiye software developer ah oo si dhalad ah u yaqaana af-Soomaaliga.\n"
        "Rules:\n"
        "1. Waa inaad mar walba ku jawaabto af-Soomaali cad, kooban, oo aad u fasiix ah.\n"
        "2. Marka lagu weydiiyo kood (Programming), u qor koodka si sax ah adoo isticmaalaya ``` markdown blocks, ka dibna ku sharax koodka af-Soomaali."
    )
    
    # Isku dar xogtii hore ee sheekada si uu u xasuusto wixii aad is tiriin
    context_text = ""
    for msg in xogta_hore:
        context_text += f"{msg}\n"

    payload = {
        "model": "qwen2.5-coder:1.5b",
        "prompt": f"{system_prompt}\n\nSheekadii hore:\n{context_text}\n\nUser: {prompt}\nAI:",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=180)
        if response.status_code == 200:
            return response.json().get('response', 'Waan ka xumahay saaxiib, cilad ayaa dhacday.')
    except Exception as e:
        return f"Cilad Offline AI: Hubi in Ollama uu shidanyahay! ({str(e)})"
    
    return "AI-gii ma uusan soo jawaabin."

@login_required
def chat_home(request):
    sessions = request.user.chat_sessions.all().order_by('-created_at')
    if not sessions.exists():
        session = ChatSession.objects.create(user=request.user, title="Wada-sheekaysi Cusub")
        return redirect('chat_session_view', session_id=session.id)
    return redirect('chat_session_view', session_id=sessions.first().id)

@login_required
def chat_session_view(request, session_id):
    sessions = request.user.chat_sessions.all().order_by('-created_at')
    current_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    
    # Halkan waxaan ka saarnay as_manager() si toos ah ayaan ugu yeernay fariimaha dhabta ah
    messages = current_session.messages.all().order_by('timestamp')
    
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        
        if user_message:
            # 1. Keydi farriinta qofka
            ChatMessage.objects.create(session=current_session, sender='user', message=user_message)
            
            # Dib u cusbooneysii magaca session-ka haddii uu cusub yahay
            if current_session.title == "Wada-sheekaysi Cusub" and len(user_message) > 5:
                current_session.title = user_message[:30] + "..."
                current_session.save()
            
            # 2. Xogta sheekadii hore (History) - Si fudud oo nadiif ah ayaa loo soo saaray hadda
            xogta_hore = []
            for msg in messages.order_by('-timestamp')[:5]:  # Waxay keenaysaa 5tii u dambeeyey
                xogta_hore.append(f"{msg.sender}: {msg.message}")
            xogta_hore.reverse() # Dib u habee nidaamka sheekada (Chronological)
            
            # 3. U dir AI-ga maxalliga ah (Ollama)
            ai_response = weydii_ai(user_message, xogta_hore=xogta_hore)
            
            # 4. Keydi jawaabta AI-ga dhexda ah
            ChatMessage.objects.create(session=current_session, sender='ai', message=ai_response)
            
            # QAABKA AJAX-KA: Labada habba waa inaan u xaqiijinnaa (Header ama POST xogteeda)
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('is_ajax') == 'true'
            
            if is_ajax:
                return JsonResponse({
                    'status': 'success',
                    'ai_message': ai_response
                })
            
            return redirect('chat_session_view', session_id=current_session.id)
            
    context = {
        'sessions': sessions,
        'current_session': current_session,
        'chat_messages': messages
    }
    return render(request, 'maxamed_Ai/chat.html', context)

@login_required
def new_chat(request):
    new_session = ChatSession.objects.create(user=request.user, title="Wada-sheekaysi Cusub")
    return redirect('chat_session_view', session_id=new_session.id)