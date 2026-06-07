import random
from django.shortcuts import render, redirect
from .models import SiteSetting, HomepageContent  # Haddi model-adu halkan u guureen
from content.models import Content
from quiz.models import Quiz
from poll.models import Poll

def home(request):
    setting = SiteSetting.objects.first()

    if setting and setting.maintenance_mode and not request.user.is_staff:
        return redirect('maintenance_view')

    homepage_contents = HomepageContent.objects.filter(is_active=True).order_by('-created_at')
    all_contents = Content.objects.all().order_by('-created_at')

    quizzes = Quiz.objects.filter(is_active=True)
    quiz = random.choice(list(quizzes)) if quizzes.exists() else None

    poll = Poll.objects.filter(is_active=True).last()

    return render(request, 'homepage/homepage.html', {
        'homepage_contents': homepage_contents,
        'all_contents': all_contents,
        'setting': setting,
        'quiz': quiz,
        'poll': poll
    })
def logout_view(request):
    auth_logout(request)
    django_messages.info(request, "Waad ka baxday koontadaadii.")
    return redirect('login')