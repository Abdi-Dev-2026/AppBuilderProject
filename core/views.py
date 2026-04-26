import zipfile
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserRegisterForm, AppForm
from .models import App, UserActivity, SiteSetting

# 1. Maintenance View
def maintenance(request):
    setting = SiteSetting.objects.first()
    return render(request, 'core/maintenance.html', {'setting': setting})

# 2. Login View (Nidaamka Remember Me iyo Activity Tracking)
def login_view(request):
    if request.method == 'POST':
        # Waxaan isticmaaleynaa AuthenticationForm si amniga loo sugo
        form = AuthenticationForm(request, data=request.POST)
        
        # Haddii aad isticmaaleyso HTML form caadi ah (ma ahan {{ form }})
        # waxaan ka aqrinaynaa 'remember_me' checkbox-ga
        remember_me = request.POST.get('remember_me')

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Hubinta user-ka
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                
                # Nidaamka Remember Me:
                # Haddii uusan calaamadeyn, session-ka wuxuu dhacayaa marka browser-ka la xiro (0)
                # Haddii uu calaamadeeyo, wuxuu raacayaa SESSION_COOKIE_AGE-ga settings.py (1 sano)
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(60 * 60 * 24 * 365) # 1 Year

                # Diiwaangelinta dhaqdhaqaaqa
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
            messages.error(request, "Nambarka ama Password-ka ma saxna.")
    else:
        form = AuthenticationForm()
        form.fields['username'].label = "Telefoonka / Username"
        
    return render(request, 'core/login.html', {'form': form})

# 3. Register View
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

# 4. Dashboard
@login_required
def dashboard(request):
    apps = App.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'apps': apps})

# 5. Create App
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

# 6. Edit Code
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

# 7. App Detail
def app_detail(request, slug):
    app = get_object_or_404(App, slug=slug)
    return render(request, 'core/app_detail.html', {'app': app})

# 8. Download App (Offline Package)
def download_app(request, slug):
    app = get_object_or_404(App, slug=slug)

    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user, 
            action="Soo dejiyay Offline Package (ZIP)", 
            app_name=app.name, 
            ip_address=request.META.get('REMOTE_ADDR')
        )

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{app.name}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{app.html_code}
<script src="script.js"></script>
</body>
</html>
"""
        zip_file.writestr("index.html", html_content)
        zip_file.writestr("style.css", app.css_code or "")
        zip_file.writestr("script.js", app.js_code or "")
        
        readme = f"""
{app.name}
Sida loo isticmaalo:
1. Fur (Unzip) folder-ka.
2. Double click ku samee faylka 'index.html'.
Waxaa dhisay: {app.owner.username}
"""
        zip_file.writestr("README.txt", readme)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={app.slug}.zip'
    return response