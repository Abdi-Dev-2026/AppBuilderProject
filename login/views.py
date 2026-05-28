from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from profile_html.models import UserProfile

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        if not identifier or not password:
            django_messages.error(request, "Fadlan geli xogta oo dhan")
            return redirect('login')

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

    return render(request, 'login/login.html')

def logout_view(request):
    auth_logout(request)
    django_messages.info(request, "Waad ka baxday koontadaadii.")
    return redirect('login')