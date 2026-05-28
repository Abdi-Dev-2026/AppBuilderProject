from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .forms import AppForm

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

    return render(request, 'create_app/create_app.html', {'form': form})