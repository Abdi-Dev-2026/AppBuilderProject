import zipfile
import random
from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages as django_messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import UserRegisterForm, AppForm
from .models import (
    App, UserActivity, SiteSetting, HomepageContent,
    Quiz, Poll, Content, Like, Comment, ContactMessage
)

# -----------------------------------------------------------
# 1. BOGAGGA GUUD
# -----------------------------------------------------------

def home(request):
    setting = SiteSetting.objects.first()
    if setting and setting.maintenance_mode and not request.user.is_staff:
        return redirect('maintenance')

    contents = HomepageContent.objects.filter(is_active=True).order_by('-created_at')
    main_contents = Content.objects.all().order_by('-created_at')

    quizzes = Quiz.objects.filter(is_active=True)
    quiz = random.choice(quizzes) if quizzes.exists() else None

    poll = Poll.objects.filter(is_active=True).last()

    return render(request, 'core/homepage.html', {
        'contents': contents,
        'main_contents': main_contents,
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
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            django_messages.success(request, "Fariintaada waa la helay ✅")
            return redirect('contact')
        else:
            django_messages.error(request, "Fadlan buuxi dhammaan xogta.")

    return render(request, 'core/contact.html')


def content_page(request):
    all_contents = Content.objects.all().order_by('-created_at')
    return render(request, 'core/content.html', {'all_contents': all_contents})


def maintenance(request):
    setting = SiteSetting.objects.first()
    return render(request, 'core/maintenance.html', {'setting': setting})


# -----------------------------------------------------------
# 2. QUIZ LOGIC
# -----------------------------------------------------------

def quiz_page(request):
    quizzes = Quiz.objects.filter(is_active=True)
    quiz = random.choice(quizzes) if quizzes.exists() else None

    score = request.session.get('quiz_score', 0)
    total = request.session.get('quiz_total', 0)

    return render(request, 'core/quiz.html', {
        'quiz': quiz,
        'score': score,
        'total': total
    })


def submit_quiz(request):
    if request.method == "POST":
        user_answer = request.POST.get('answer', '').strip()
        correct_answer = request.POST.get('correct', '').strip()

        request.session['quiz_total'] = request.session.get('quiz_total', 0) + 1

        if user_answer.upper() == correct_answer.upper():
            request.session['quiz_score'] = request.session.get('quiz_score', 0) + 1
            django_messages.success(request, "Hambalyo! Jawaabtu waa sax. ✅")
        else:
            django_messages.error(request, f"Jawaabtu ma saxna ❌ (Sax: {correct_answer})")

        return redirect('quiz_page')

    return redirect('quiz_page')


def reset_quiz(request):
    request.session.pop('quiz_score', None)
    request.session.pop('quiz_total', None)
    django_messages.info(request, "Dhibcaha waa la reset gareeyay.")
    return redirect('quiz_page')


# -----------------------------------------------------------
# 3. INTERACTIVE FEATURES
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
    if request.method == "POST":
        content = get_object_or_404(Content, id=content_id)
        text = request.POST.get("text")
        if text:
            Comment.objects.create(user=request.user, content=content, text=text)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def vote_poll(request, poll_id):
    if request.method == "POST":
        poll = get_object_or_404(Poll, id=poll_id)
        choice = request.POST.get("choice")

        if choice == "1":
            poll.votes1 += 1
        elif choice == "2":
            poll.votes2 += 1

        poll.save()
        django_messages.success(request, "Codkaaga waa la diiwaangeliyey 👍")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


def poll_page(request):
    polls = Poll.objects.filter(is_active=True).order_by('-id')
    return render(request, 'core/poll.html', {'polls': polls})


# -----------------------------------------------------------
# 4. AUTH & DASHBOARD
# -----------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)

            UserActivity.objects.create(
                user=user,
                action="Login",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    django_messages.info(request, "Waad logout garaysay.")
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            UserActivity.objects.create(
                user=user,
                action="Register",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            django_messages.success(request, "Account waa la sameeyay.")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'core/register.html', {'form': form})


@login_required
def dashboard(request):
    apps = App.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'apps': apps})


# -----------------------------------------------------------
# 5. APP BUILDER
# -----------------------------------------------------------

@login_required
def create_app(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.owner = request.user
            app.save()

            UserActivity.objects.create(
                user=request.user,
                action="Create App",
                app_name=app.name,
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return redirect('dashboard')
    else:
        form = AppForm()

    return render(request, 'core/create_app.html', {'form': form})


@login_required
def edit_code(request, app_id):
    app = get_object_or_404(App, id=app_id, owner=request.user)

    if request.method == 'POST':
        app.html_code = request.POST.get('html_code')
        app.css_code = request.POST.get('css_code')
        app.js_code = request.POST.get('js_code')
        app.save()

        django_messages.success(request, "Koodhka waa la save gareeyay")
        return redirect('dashboard')

    return render(request, 'core/editor.html', {'app': app})


def app_detail(request, slug):
    app = get_object_or_404(App, slug=slug)
    return render(request, 'core/app_detail.html', {'app': app})


def download_app(request, slug):
    app = get_object_or_404(App, slug=slug)

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:

        html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<title>{app.name}</title>
<link rel='stylesheet' href='style.css'>
</head>
<body>
{app.html_code}
<script src='script.js'></script>
</body>
</html>"""

        zip_file.writestr("index.html", html_content)
        zip_file.writestr("style.css", app.css_code or "")
        zip_file.writestr("script.js", app.js_code or "")
        zip_file.writestr("README.txt", f"{app.name} - by {app.owner.username}")

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={app.slug}.zip'

    return response


# -----------------------------------------------------------
# 6. CONTACT MESSAGES (FIXED INBOX)
# -----------------------------------------------------------

@login_required
def my_messages(request):
    messages_list = ContactMessage.objects.filter(
        email__iexact=request.user.email
    ).order_by('-created_at')

    return render(request, 'core/my_messages.html', {
        'messages': messages_list
    })