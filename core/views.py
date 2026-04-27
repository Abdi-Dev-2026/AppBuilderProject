import zipfile
import random
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
    """Homepage-ka rasmiga ah: Wuxuu soo bandhigaa xogta ugu dambeeyey"""
    setting = SiteSetting.objects.first()
    if setting and setting.maintenance_mode and not request.user.is_staff:
        return redirect('maintenance')

    contents = HomepageContent.objects.filter(is_active=True).order_by('-created_at')
    main_contents = Content.objects.all().order_by('-created_at')
    
    # Soo qaad hal Quiz oo nasiib ah (Random) oo Active ah
    quizzes = Quiz.objects.filter(is_active=True)
    quiz = random.choice(quizzes) if quizzes.exists() else None
    
    # Soo qaad Poll-kii ugu dambeeyay
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
    return render(request, 'core/contact.html')

def content_page(request):
    all_contents = Content.objects.all().order_by('-created_at')
    return render(request, 'core/content.html', {'all_contents': all_contents})

def maintenance(request):
    setting = SiteSetting.objects.first()
    return render(request, 'core/maintenance.html', {'setting': setting})

# -----------------------------------------------------------
# 2. QUIZ LOGIC (HAGAAJISAN: NEXT QUESTION & SCORES)
# -----------------------------------------------------------

def quiz_page(request):
    """Bogga Quizzes-ka: Wuxuu soo saaraa hal su'aal oo random ah mar walba"""
    quizzes = Quiz.objects.filter(is_active=True)
    quiz = random.choice(quizzes) if quizzes.exists() else None
    
    # Waxaan soo qaadeynaa dhibcaha hadda u urursan qofka (Session)
    score = request.session.get('quiz_score', 0)
    total = request.session.get('quiz_total', 0)
    
    return render(request, 'core/quiz.html', {
        'quiz': quiz,
        'score': score,
        'total': total
    })

def submit_quiz(request):
    """Hubinta jawaabta iyo u gudbinta su'aasha xigta"""
    if request.method == "POST":
        user_answer = request.POST.get('answer', '').strip()
        correct_answer = request.POST.get('correct', '').strip()
        
        # 1. Kordhi tirada su'aalaha uu qofku isku dayay
        request.session['quiz_total'] = request.session.get('quiz_total', 0) + 1
        
        # 2. Hubi jawaabta (Case-insensitive)
        if user_answer.upper() == correct_answer.upper():
            request.session['quiz_score'] = request.session.get('quiz_score', 0) + 1
            messages.success(request, "Hambalyo! Jawaabtu waa sax. ✅")
        else:
            messages.error(request, f"Waan ka xunnahay, jawaabtu ma saxna. ❌ (Jawaabta saxda ahayd: {correct_answer})")
            
        # 3. Dib ugu celi bogga quiz-ka si uu mid kale u helo
        return redirect('quiz_page')
    
    return redirect('quiz_page')

def reset_quiz(request):
    """Eber ka bilaabista dhibcaha (Clearing Sessions)"""
    if 'quiz_score' in request.session:
        del request.session['quiz_score']
    if 'quiz_total' in request.session:
        del request.session['quiz_total']
    messages.info(request, "Dhibcahaagii waa la tirtiray, dib uga bilaabo.")
    return redirect('quiz_page')

# -----------------------------------------------------------
# 3. INTERACTIVE LOGIC (Like, Comment & Poll)
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
        messages.success(request, "Codkaaga waa la diiwaangeliyey. 👍")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def poll_page(request):
    polls = Poll.objects.filter(is_active=True).order_by('-id')
    return render(request, 'core/poll.html', {'polls': polls})

# -----------------------------------------------------------
# 4. AUTH & DASHBOARD VIEWS
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
    apps = App.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'apps': apps})

# -----------------------------------------------------------
# 5. APP BUILDING TOOLS
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
        messages.success(request, "Koodhka waa la badbaadiyey!")
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
        readme = f"{app.name}\nDhisay: {app.owner.username}"
        zip_file.writestr("README.txt", readme)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={app.slug}.zip'
    return response