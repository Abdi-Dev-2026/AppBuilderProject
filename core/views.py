import zipfile
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
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
    """Homepage-ka rasmiga ah: Wuxuu soo bandhigaa xogta ugu dambeysa"""
    # 1. Hubi haddii Website-ku Maintenance ku jiro
    setting = SiteSetting.objects.first()
    if setting and setting.maintenance_mode and not request.user.is_staff:
        return redirect('maintenance')

    contents = HomepageContent.objects.filter(is_active=True).order_by('-created_at')
    main_contents = Content.objects.all().order_by('-created_at')
    
    # Soo qaad Quiz-kii ugu dambeeyay ee Active ah
    quiz = Quiz.objects.filter(is_active=True).last()
    
    # Soo qaad Poll-kii ugu dambeeyay ee Active ah
    poll = Poll.objects.filter(is_active=True).last()

    return render(request, 'core/homepage.html', {
        'contents': contents,
        'main_contents': main_contents,
        'setting': setting,
        'quiz': quiz,
        'poll': poll
    })

def about_page(request):
    """Bogga ku saabsan website-ka"""
    return render(request, 'core/about.html')

def contact_page(request):
    """Bogga xiriirka (Contact)"""
    return render(request, 'core/contact.html')

def content_page(request):
    """Bogga muujinaya dhamaan content-ka"""
    all_contents = Content.objects.all().order_by('-created_at')
    return render(request, 'core/content.html', {'all_contents': all_contents})

def quiz_page(request):
    """Dhamaan Quizzes-ka firfircoon"""
    quizzes = Quiz.objects.filter(is_active=True).order_by('-id')
    return render(request, 'core/quiz.html', {'quizzes': quizzes})

def poll_page(request):
    """Dhamaan Polls-ka firfircoon"""
    polls = Poll.objects.filter(is_active=True).order_by('-id')
    return render(request, 'core/poll.html', {'polls': polls})

def maintenance(request):
    setting = SiteSetting.objects.first()
    return render(request, 'core/maintenance.html', {'setting': setting})

# -----------------------------------------------------------
# 2. INTERACTIVE LOGIC (Like, Comment, Quiz & Poll)
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

def submit_quiz(request):
    """Hubinta jawaabta Quiz-ka (Logic-ga saxda ah)"""
    if request.method == "POST":
        selected = request.POST.get("answer") # Tan waxaa laga helaa Radio Button-ka
        correct = request.POST.get("correct")   # Tan waxaa laga helaa Hidden Input-ka
        
        if selected == correct:
            messages.success(request, "Hambalyo! Jawaabtaadu waa sax. ✅")
        else:
            messages.error(request, "Waan ka xunnahay, jawaabtu ma saxna. ❌")
            
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def vote_poll(request, poll_id):
    """Codeynta Poll-ka"""
    if request.method == "POST":
        poll = get_object_or_404(Poll, id=poll_id)
        choice = request.POST.get("choice")
        if choice == "1":
            poll.votes1 += 1
        elif choice == "2":
            poll.votes2 += 1
        poll.save()
        messages.success(request, "Codkaaga waa la diiwaangeliyey. 👍")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# -----------------------------------------------------------
# 3. AUTH & DASHBOARD VIEWS
# -----------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            # Remember me logic
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600) # 2 todobaad

            UserActivity.objects.create(
                user=user, 
                action="Wuxuu soo galay (Login)", 
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.info(request, "Si guul ah ayaad uga baxday.")
    return redirect('login')

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
            messages.success(request, 'Si guul ah ayaad u diiwaangashay!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    # CILAD-BAX: 'order_of' waxaa loo beddelay 'order_by'
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
        messages.success(request, "Koodhka waa la badbaadiyey!")
        return redirect('dashboard')
    return render(request, 'core/editor.html', {'app': app})

def app_detail(request, slug):
    app = get_object_or_404(App, slug=slug)
    return render(request, 'core/app_detail.html', {'app': app})

def download_app(request, slug):
    app = get_object_or_404(App, slug=slug)
    
    # Record activity
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user, 
            action="Soo dejiyay ZIP Package", 
            app_name=app.name, 
            ip_address=request.META.get('REMOTE_ADDR')
        )

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
        
        readme = f"{app.name}\nDhisay: {app.owner.username}\nDouble click 'index.html' si aad u furto."
        zip_file.writestr("README.txt", readme)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={app.slug}.zip'
    return response