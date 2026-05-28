from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from django.contrib.auth import login as auth_login
from .forms import UserRegisterForm  # Hubi halka uu form-ka ku jiro
from profile_html.models import UserProfile

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

    return render(request, 'register/register.html', {'form': form})