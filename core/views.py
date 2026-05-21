import os
import asyncio
import zipfile
import random
import json
import uuid
from io import BytesIO
from datetime import datetime

# Django Core Imports
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Q

# Async helper for Django views
from asgiref.sync import async_to_sync
import edge_tts

# Local Imports (Models, Forms, Utils)
from .utils import generate_qr_code, generate_id_card_pdf
from .forms import UserRegisterForm, AppForm
from .models import (
    App, SiteSetting, HomepageContent,
    Quiz, Poll, Content, Like, Comment,
    ContactMessage, UserProfile,
    FriendRequest, ChatMessage, Subject, GlobalNotice, TTSSetting,
    ChatSetting  
)


# -----------------------------------------------------------
# 1. HOME & STATIC PAGES
# -----------------------------------------------------------
def home(request):
    setting = SiteSetting.objects.first()

    if setting and setting.maintenance_mode and not request.user.is_staff:
        return redirect('maintenance')

    homepage_contents = HomepageContent.objects.filter(is_active=True).order_by('-created_at')
    all_contents = Content.objects.all().order_by('-created_at')

    quizzes = Quiz.objects.filter(is_active=True)
    quiz = random.choice(list(quizzes)) if quizzes.exists() else None

    poll = Poll.objects.filter(is_active=True).last()

    return render(request, 'core/homepage.html', {
        'homepage_contents': homepage_contents,
        'all_contents': all_contents,
        'setting': setting,
        'quiz': quiz,
        'poll': poll
    })


def about_page(request):
    return render(request, 'core/about.html')


def contact_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject') or "General"
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            django_messages.success(request, "Fariintaada waa la helay ✅")
            return redirect('contact')

        django_messages.error(request, "Fadlan buuxi dhammaan xogta.")

    return render(request, 'core/contact.html')


def content_page(request):
    all_contents = Content.objects.all().order_by('-created_at')
    return render(request, 'core/content.html', {'all_contents': all_contents})


def maintenance(request):
    setting = SiteSetting.objects.first()
    return render(request, 'core/maintenance.html', {'setting': setting})


# -----------------------------------------------------------
# 2. AUTH SYSTEM
# -----------------------------------------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            try:
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                django_messages.success(
                    request,
                    f"Koontada waa la sameeyay! ID-gaaga waa: {user_profile.user_id_code}"
                )
            except Exception as e:
                django_messages.warning(request, "Koontada waa la sameeyay laakiin Profile-ka ayaa dib ka dhismi doona.")

            return redirect('profile')
    else:
        form = UserRegisterForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        if not identifier or not password:
            django_messages.error(request, "Fadlan geli xogta oo dhan")
            return redirect('login')

        user_obj = None
        user_obj = authenticate(request, username=identifier, password=password)

        if user_obj is None:
            user_by_email = User.objects.filter(email=identifier).first()
            if user_by_email:
                user_obj = authenticate(request, username=user_by_email.username, password=password)

        if user_obj is None:
            try:
                profile_obj = UserProfile.objects.get(user_id_code=identifier)
                user_obj = authenticate(request, username=profile_obj.user.username, password=password)
            except UserProfile.DoesNotExist:
                pass

        if user_obj:
            auth_login(request, user_obj)
            
            if remember_me:
                request.session.set_expiry(request.session.get_expiry_age())
            else:
                request.session.set_expiry(0)
            
            return redirect('dashboard')

        django_messages.error(request, "Xogta aad gelisay waa khaldan tahay ❌")

    return render(request, 'core/login.html')


def logout_view(request):
    auth_logout(request)
    django_messages.info(request, "Waad ka baxday koontadaadii.")
    return redirect('login')


@login_required
def dashboard(request):
    apps = App.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'apps': apps})


# -----------------------------------------------------------
# 3. PROFILE + QR + PROFESSIONAL ID CARD
# -----------------------------------------------------------
@login_required
def profile(request):
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)
    
    qr_image = ""
    if profile_obj.user_id_code:
        qr_image = generate_qr_code(profile_obj.user_id_code)

    return render(request, 'core/profile.html', {
        'profile': profile_obj,
        'qr_image': qr_image
    })


@login_required
def download_id_card(request):
    profile_obj = get_object_or_404(UserProfile, user=request.user)
    user_password = request.POST.get('manual_password', "Lama hayo")

    pdf_buffer = generate_id_card_pdf(profile_obj, password=user_password)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{profile_obj.user_id_code}_ID.pdf"'

    return response


# -----------------------------------------------------------
# 4. CHAT SYSTEM (ID SEARCH, FRIENDS, & REQUESTS)
# -----------------------------------------------------------
@login_required
def chats_page(request):
    """
    Shaqada maamusha bogga guud ee chat-ka, saaxiibada, 
    codsiyada furan, raadinta ID-ga, iyo soo qaadashada ChatSetting.
    """
    # 🚀 SOO QAADASHADA XOGTA BACKGROUND-KA ADMIN-KA
    chat_settings = ChatSetting.objects.first()
    
    # Xogta koontada isticmaalaha hadda jooga
    my_profile, created = UserProfile.objects.get_or_create(user=request.user)
    friend_ids = my_profile.friends.values_list('id', flat=True)
    
    # Dhammaan dadka kale ee nidaamka ku jira iyo codsiyada furan
    all_users = UserProfile.objects.exclude(user=request.user)
    pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
    
    # Raadinta (Search) qof cusub iyadoo la adeegsanayo User ID Code
    search_result = None
    search_id = request.GET.get('search_id')
    if search_id:
        try:
            search_result = UserProfile.objects.get(user_id_code=search_id)
        except UserProfile.DoesNotExist:
            search_result = None

    context = {
        'chat_settings': chat_settings,   # <--- Halkan ayaa muhiim ah si HTML-ku u akhriyo background-ka
        'my_profile': my_profile,
        'friend_ids': friend_ids,
        'pending_requests': pending_requests,
        'all_users': all_users,
        'search_result': search_result,
    }
    return render(request, 'core/chats.html', context)


@login_required
def send_friend_request(request, profile_id):
    receiver_profile = get_object_or_404(UserProfile, id=profile_id)
    receiver_user = receiver_profile.user
    
    if receiver_user != request.user:
        FriendRequest.objects.get_or_create(sender=request.user, receiver=receiver_user)
        django_messages.success(request, f"Codsiga saaxiibtinimo waa loo diray {receiver_user.username} ✅")
    
    return redirect('chats_page')


@login_required
def accept_request(request, request_id):
    friend_req = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_req.status = 'accepted'
    friend_req.save()
    
    request.user.userprofile.friends.add(friend_req.sender)
    friend_req.sender.userprofile.friends.add(request.user)
    
    django_messages.success(request, f"Hadda waad wada hadli kartaan {friend_req.sender.username}!")
    return redirect('chats_page')


@login_required
def reject_request(request, request_id):
    friend_req = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_req.delete()
    django_messages.info(request, "Codsigii saaxiibtinimo waa la diiday.")
    return redirect('chats_page')


@login_required
def chat_with_user(request, username):
    """
    Shaqada maamusha daaqadda chat-ka, fariin dirista, 
    iyo soo qaadashada beddelka background-ka (ChatSetting).
    """
    other_user = get_object_or_404(User, username=username)
    
    # Hubi in labada qof ay saaxiib yihiin
    if other_user not in request.user.userprofile.friends.all():
        django_messages.error(request, "Waa inaad saaxiib noqotaan si aad u wada hadashaan.")
        return redirect('chats_page')

    # Soo qaad dhammaan farriimaha u dhexeeya labada qof
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    # 🚀 SOO QAADASHADA XOGTA BACKGROUND-KA ADMIN-KA
    chat_settings = ChatSetting.objects.first()

    # Haddii foomka fariinta ama lifaaqa la soo diro
    if request.method == "POST":
        msg_text = request.POST.get('message')
        attachment = request.FILES.get('attachment')
        is_folder = request.POST.get('is_folder') == 'true'

        if msg_text or attachment:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=other_user,
                message=msg_text,
                attachment=attachment,
                is_folder=is_folder
            )
        return redirect('chat_with_user', username=username)

    return render(request, 'core/chat_window.html', {
        'other_user': other_user,
        'chat_messages': messages,
        'chat_settings': chat_settings,  # <--- Halkanna waa u muhiim daaqadda chat-ka dhexdiisa!
    })


# -----------------------------------------------------------
# 5. SOCIAL FEATURES (LIKE/COMMENT)
# -----------------------------------------------------------
@login_required
def like_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    like, created = Like.objects.get_or_create(user=request.user, content=content)

    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def add_comment(request, content_id):
    content = get_object_or_404(Content, id=content_id)

    if request.method == "POST":
        text = request.POST.get("comment_text", "").strip()
        if text:
            Comment.objects.create(
                user=request.user,
                content=content,
                text=text
            )

    return redirect(request.META.get('HTTP_REFERER', 'home'))


# -----------------------------------------------------------
# 6. QUIZ SYSTEM
# -----------------------------------------------------------
def quiz_page(request):
    quizzes = Quiz.objects.filter(is_active=True)
    quiz = random.choice(list(quizzes)) if quizzes.exists() else None

    return render(request, 'core/quiz.html', {
        'quiz': quiz,
        'score': request.session.get('quiz_score', 0),
        'total': request.session.get('quiz_total', 0)
    })


def submit_quiz(request):
    if request.method == "POST":
        quiz_id = request.POST.get('quiz_id')
        user_answer = request.POST.get('answer', '').strip()

        quiz = get_object_or_404(Quiz, id=quiz_id)
        request.session['quiz_total'] = request.session.get('quiz_total', 0) + 1

        if user_answer.lower() == quiz.correct_answer.lower():
            request.session['quiz_score'] = request.session.get('quiz_score', 0) + 1
            django_messages.success(request, "Hambalyo! Jawaabtu waa sax. 🎉")
        else:
            request.session['quiz_score'] = request.session.get('quiz_score', 0)
            django_messages.error(request, f"Waa lagaa gubay! Jawaabta saxda ahayd waxay ahayd: {quiz.correct_answer}")

    return redirect('quiz_page')


def reset_quiz(request):
    request.session.pop('quiz_score', None)
    request.session.pop('quiz_total', None)
    return redirect('quiz_page')


# -----------------------------------------------------------
# 7. POLL SYSTEM
# -----------------------------------------------------------
def poll_page(request):
    polls = Poll.objects.filter(is_active=True).order_by('-id')
    return render(request, 'core/poll.html', {'polls': polls})


def vote_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == "POST":
        choice = request.POST.get("choice")

        if choice == "1":
            poll.votes1 += 1
        elif choice == "2":
            poll.votes2 += 1

        poll.save()

    return redirect('poll_page')


# -----------------------------------------------------------
# 8. APP BUILDER (NO-CODE FEATURE)
# -----------------------------------------------------------
@login_required
def create_app(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)

        if form.is_valid():
            app = form.save(commit=False)
            app.owner = request.user
            app.save()

            django_messages.success(request, "App-kaaga waa la abuuray ✅")
            return redirect('dashboard')
    else:
        form = AppForm()

    return render(request, 'core/create_app.html', {'form': form})


@login_required
def edit_code(request, app_id):
    app = get_object_or_404(App, id=app_id, owner=request.user)

    if request.method == 'POST':
        app.html_code = request.POST.get('html_code', '')
        app.css_code = request.POST.get('css_code', '')
        app.js_code = request.POST.get('js_code', '')
        app.save()

        django_messages.success(request, "Isbeddelka waa la save-gareeyay ✅")
        return redirect('dashboard')

    return render(request, 'core/editor.html', {'app': app})


def app_detail(request, slug):
    app = get_object_or_404(App, slug=slug)
    return render(request, 'core/app_detail.html', {'app': app})


def download_app(request, slug):
    app = get_object_or_404(App, slug=slug)

    buffer = BytesIO()
    safe_name = slugify(app.name)

    with zipfile.ZipFile(buffer, 'w') as zip_file:
        html_content = f"<!DOCTYPE html>\n<html>\n<head>\n<title>{app.name}</title>\n<link rel='stylesheet' href='style.css'>\n</head>\n<body>\n{app.html_code}\n<script src='script.js'></script>\n</body>\n</html>"

        zip_file.writestr("index.html", html_content)
        zip_file.writestr("style.css", app.css_code or "")
        zip_file.writestr("script.js", app.js_code or "")
        zip_file.writestr("README.txt", f"App Name: {app.name}\nDeveloper: {app.owner.username}")

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={safe_name}.zip'

    return response


# -----------------------------------------------------------
# 9. USER MESSAGES
# -----------------------------------------------------------
@login_required
def my_messages(request):
    messages_list = ContactMessage.objects.filter(
        email__iexact=request.user.email
    ).order_by('-created_at')

    return render(request, 'core/my_messages.html', {
        'messages': messages_list
    })


# -----------------------------------------------------------
# 10. BANAADIR EXAM SYSTEM
# -----------------------------------------------------------
def banaadir_view(request):
    subjects = Subject.objects.all()
    data_dict = {}
    
    for sub in subjects:
        data_dict[sub.name] = {}
        for yr in sub.years.all():
            data_dict[sub.name][str(yr.year)] = {
                "read": [
                    {
                        "title": r.title,
                        "content": r.content,
                        "image_file": r.image_file.url if hasattr(r, 'image_file') and r.image_file else "",
                        "image_url": getattr(r, 'image_url', ""),
                        "video_file": r.video_file.url if hasattr(r, 'video_file') and r.video_file else "",
                        "video_url": getattr(r, 'video_url', ""),
                        "is_portrait": getattr(r, 'is_portrait', False)
                    } for r in yr.readings.all()
                ],
                "quiz": [
                    {
                        "q": q.question_text,
                        "choices": [q.option1, q.option2, q.option3, q.option4],
                        "answer": q.correct_option_index,
                        "image_file": q.image_file.url if hasattr(q, 'image_file') and q.image_file else "",
                        "image_url": getattr(q, 'image_url', ""),
                        "video_file": q.video_file.url if hasattr(q, 'video_file') and q.video_file else "",
                        "video_url": getattr(q, 'video_url', ""),
                        "is_portrait": getattr(q, 'is_portrait', False)
                    } for q in yr.quizzes.all()
                ]
            }

    notices_from_admin = GlobalNotice.objects.filter(is_active=True).order_by('-created_at')
    global_ads_list = []
    for notice in notices_from_admin:
        global_ads_list.append({
            'title': notice.title,
            'description': notice.description or '',
            'image_file': notice.image_file.url if notice.image_file else '',
            'image_url': notice.image_url or '',
            'video_file': notice.video_file.url if notice.video_file else '',
            'video_url': notice.video_url or '',
            'is_portrait': notice.is_portrait,
        })
    
    data_dict['global_ads'] = global_ads_list

    subjects_data = []
    for s in subjects:
        subjects_data.append({
            'name': s.name,
            'icon_emoji': getattr(s, 'icon_emoji', ''),
            'icon_image_file': s.icon_image_file.url if hasattr(s, 'icon_image_file') and s.icon_image_file else '',
            'icon_image_url': getattr(s, 'icon_image_url', ''),
            'icon_video_file': s.icon_video_file.url if hasattr(s, 'icon_video_file') and s.icon_video_file else '',
            'icon_video_url': getattr(s, 'icon_video_url', ''),
        })

    context = {
        'subjects_json': json.dumps(subjects_data),
        'data_json': json.dumps(data_dict)
    }
    return render(request, 'core/banaadir.html', context)


# -----------------------------------------------------------
# 11. TTS ENGINE SYSTEM (SAFE & ASYNC-TO-SYNC CONVERTED)
# -----------------------------------------------------------
async def generate_somali_speech(text, voice_name, output_path):
    """Nidaamka rasmiga ah ee u hadlaya luuqada Soomaaliga ee Edge-TTS"""
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

    return render(request, 'core/tts_interface.html', {
        'max_chars': max_chars,
        'tts_setting': tts_setting
    })