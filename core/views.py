import zipfile
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserRegisterForm, AppForm
from .models import App, UserActivity, SiteSetting, HomepageContent, Quiz, Poll, Content, Like, Comment

# -----------------------------------------------------------
# 1. BOGAGGA GUUD (Public & Static Pages)
# -----------------------------------------------------------

def home(request):
    """Homepage-ka rasmiga ah oo leh Content, Quiz, iyo Poll"""
    contents = HomepageContent.objects.filter(is_active=True).order_by('-created_at')
    main_contents = Content.objects.all().order_by('-created_at')
    setting = SiteSetting.objects.first()
    quiz = Quiz.objects.filter(is_active=True).last()
    poll = Poll.objects.filter(is_active=True).last()

    return render(request, 'core/homepage.html', {
        'contents': contents,
        'main_contents': main_contents,
        'setting': setting,
        'quiz': quiz,
        'poll': poll
    })

def homepage(request):
    """Simple view for homepage (Alternative)"""
    return render(request, 'core/homepage.html')

def quiz_page(request):
    return render(request, 'core/quiz.html')

def poll_page(request):
    return render(request, 'core/poll.html')

def about_page(request):
    return render(request, 'core/about.html')

def contact_page(request):
    return render(request, 'core/contact.html')

def content_page(request):
    return render(request, 'core/content.html')

def maintenance(request):
    setting = SiteSetting.objects.first()
    return render(request, 'core/maintenance.html', {'setting': setting})

# -----------------------------------------------------------
# 2. INTERACTIVE LOGIC (Like, Comment, Quiz & Poll)
# -----------------------------------------------------------

@login_required
def like_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    like, created = Like.objects.get_or_create(
        user=request.user,
        content=content
    )
    if not created:
        like.delete()  # Haddii uu hore u jiray waa laga masaxayaa (Unlike)
    return redirect('home')

@login_required
def add_comment(request, content_id):
    if request.method == "POST":
        content = get_object_or_404(Content, id=content_id)
        text = request.POST.get("text")
        if text:
            Comment.objects.create(
                user=request.user,
                content=content,
                text=text
            )
    return redirect('home')

def submit_quiz(request):
    if request.method == "POST":
        selected = request.POST.get("answer")
        correct = request.POST.get("correct")
        if selected == correct:
            messages.success(request, "Hambalyo! Jawaabtaadu waa sax. ✅")
            return redirect('/?quiz=correct')
        else:
            messages.error(request, "Waan ka xunnahay, jawaabtu ma saxna. ❌")
            return redirect('/?quiz=wrong')
    return redirect('home')

def vote_poll(request, poll_id):
    if request.method == "POST":
        poll = get_object_or_404(Poll, id=poll_id)
        choice = request.POST.get("choice")
        if choice == "1":
            poll.votes1 += 1
        elif choice == "2":
            poll.votes2 += 1
        poll.save()
        messages.success(request, "Codkaaga waa la diiwaangeliyey. 👍")
    return redirect('home')

# -----------------------------------------------------------
# 3. AUTH & DASHBOARD VIEWS
# -----------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        remember_me = request.POST.get('remember_me')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(60 * 60 * 24 * 365)
                
                UserActivity.objects.create(
                    user=user, 
                    action="Wuxuu soo galay (Login)", 
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                messages.info(request, f"Ku soo dhawaaw: {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Username ama password waa khalad")
        else:
            messages.error(request, "Xogta ma saxna.")
    else:
        form = AuthenticationForm()
        form.fields['username'].label = "Telefoonka / Username"
    return render(request, 'core/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserActivity.objects.create(
                user=user, 
                action="Wuxuu sameystay Account", 
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Si guul ah ayaa lagu diiwaangeliyey!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    apps = App.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'apps': apps})

# -----------------------------------------------------------
# 4. APP BUILDING & TOOLS
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
                action="Wuxuu dhisay App", 
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
        UserActivity.objects.create(
            user=request.user, 
            action="Wuxuu beddelay koodhka", 
            app_name=app.name, 
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return redirect('dashboard')
    return render(request, 'core/editor.html', {'app': app})

def app_detail(request, slug):
    app = get_object_or_404(App, slug=slug)
    return render(request, 'core/app_detail.html', {'app': app})

def download_app(request, slug):
    app = get_object_or_404(App, slug=slug)
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user, 
            action="Soo dejiyay ZIP Package", 
            app_name=app.name, 
            ip_address=request.META.get('REMOTE_ADDR')
        )
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        html_content = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>{app.name}</title><link rel='stylesheet' href='style.css'></head><body>{app.html_code}<script src='script.js'></script></body></html>"
        zip_file.writestr("index.html", html_content)
        zip_file.writestr("style.css", app.css_code or "")
        zip_file.writestr("script.js", app.js_code or "")
        readme = f"{app.name}\nDhisay: {app.owner.username}\nDouble click 'index.html' si aad u furto."
        zip_file.writestr("README.txt", readme)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={app.slug}.zip'
    return response