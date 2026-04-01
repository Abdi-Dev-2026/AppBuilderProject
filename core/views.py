from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, AppForm
from .models import App

# 1. Qaybta Login-ka (Nambar & Password)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"Ku soo dhawaaw, waxaad hadda u gashay nambarka: {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Nambarka ama Password-ka aad gelisay ma saxna.")
        else:
            messages.error(request, "Xogta aad gelisay ma saxna. Fadlan dib u eeg.")
    else:
        form = AuthenticationForm()
        form.fields['username'].label = "Telefoonka"
        
    return render(request, 'core/login.html', {'form': form})

# 2. Qaybta Diiwaangelinta (Register)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account-ka nambarkiisu yahay {username} si guul ah ayaa loo sameeyay!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

# 3. Qaybta Dashboard-ka (Wuxuu tusayaa kaliya Apps-ka uu User-kaas dhistay)
@login_required
def dashboard(request):
    apps = App.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'apps': apps})

# 4. Qaybta App-ka Cusub lagu dhisayo
@login_required
def create_app(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.owner = request.user
            app.save()
            messages.success(request, "App-kaaga si guul ah ayaa loo dhisay!")
            return redirect('dashboard')
    else:
        form = AppForm()
    return render(request, 'core/create_app.html', {'form': form})

# 5. Qaybta EDIT CODE (Matoorka Editor-ka)
@login_required
def edit_code(request, app_id):
    app = get_object_or_404(App, id=app_id, owner=request.user)

    if request.method == 'POST':
        app.html_code = request.POST.get('html_code')
        app.css_code = request.POST.get('css_code')
        app.js_code = request.POST.get('js_code')
        app.save()
        messages.success(request, "Isbeddelka koodhka si guul ah ayaa loo kaydiyay!")
        return redirect('dashboard')

    return render(request, 'core/editor.html', {'app': app})

# 6. BOGGA LIVE-KA AH (Public Link) - Kani waa qaybta cusub
def app_detail(request, slug):
    # Waxaan soo qabanaynaa App-ka isagoo loo marayo Slug-ga link-ga ku jira.
    # Qaybtani uma baahna @login_required si dadka kale ay u arkaan.
    app = get_object_or_404(App, slug=slug)
    return render(request, 'core/app_detail.html', {'app': app})