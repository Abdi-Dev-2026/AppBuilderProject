import zipfile
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserRegisterForm, AppForm
from .models import App, UserActivity  # Waxaan ku darnay UserActivity

# 1. Qaybta Login-ka
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Dhaqdhaqaaqa Login-ka
                UserActivity.objects.create(
                    user=user, 
                    action="Wuxuu soo galay nidaamka (Login)",
                    ip_address=request.META.get('REMOTE_ADDR')
                )
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

# 2. Qaybta Diiwaangelinta
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Dhaqdhaqaaqa Register-ka
            UserActivity.objects.create(
                user=user, 
                action="Wuxuu sameystay Account cusub",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account-ka nambarkiisu yahay {username} si guul ah ayaa loo sameeyay!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

# 3. Dashboard-ka
@login_required
def dashboard(request):
    apps = App.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'apps': apps})

# 4. Qaybta App-ka Cusub
@login_required
def create_app(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.owner = request.user
            app.save()
            # LA SOCODKA DHAGDHAQAAQA
            UserActivity.objects.create(
                user=request.user,
                action="Wuxuu dhisay App cusub",
                app_name=app.name,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, "App-kaaga si guul ah ayaa loo dhisay!")
            return redirect('dashboard')
    else:
        form = AppForm()
    return render(request, 'core/create_app.html', {'form': form})

# 5. Qaybta EDIT CODE
@login_required
def edit_code(request, app_id):
    app = get_object_or_404(App, id=app_id, owner=request.user)

    if request.method == 'POST':
        app.html_code = request.POST.get('html_code')
        app.css_code = request.POST.get('css_code')
        app.js_code = request.POST.get('js_code')
        app.save()
        # LA SOCODKA DHAGDHAQAAQA
        UserActivity.objects.create(
            user=request.user,
            action="Wuxuu beddelay koodhka App-ka",
            app_name=app.name,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        messages.success(request, "Isbeddelka koodhka si guul ah ayaa loo kaydiyay!")
        return redirect('dashboard')

    return render(request, 'core/editor.html', {'app': app})

# 6. Bogga Live-ka ah
def app_detail(request, slug):
    app = get_object_or_404(App, slug=slug)
    return render(request, 'core/app_detail.html', {'app': app})

# 7. DOWNLOAD APP (ZIP EXPORT + TRACKING)
@login_required
def download_app(request, slug):
    app = get_object_or_404(App, slug=slug)

    # --- LA SOCODKA DHAGDHAQAAQA ---
    UserActivity.objects.create(
        user=request.user,
        action="Soo dejiyay ZIP App",
        app_name=app.name,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    # -------------------------------

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        zip_file.writestr("index.html", app.html_code)
        if app.css_code:
            zip_file.writestr("style.css", app.css_code)
        if app.js_code:
            zip_file.writestr("script.js", app.js_code)

        readme_content = f"Magaca App-ka: {app.name}\nLagu dhisay: App Builder Somali\nLink: https://maxamed.up.railway.app/app/{app.slug}/"
        zip_file.writestr("README.txt", readme_content)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={app.slug}_app.zip'

    return response