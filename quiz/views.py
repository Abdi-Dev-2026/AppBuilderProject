import random
from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from .models import Quiz

def quiz_page(request):
    quizzes = Quiz.objects.filter(is_active=True)
    quiz = random.choice(list(quizzes)) if quizzes.exists() else None

    return render(request, 'quiz/quiz.html', {
        'quiz': quiz,
        'score': request.session.get('quiz_score', 0),
        'total': request.session.get('quiz_total', 0)
    })

def submit_quiz(request):
    if request.method == "POST":
        user_answer = request.POST.get('answer', '').strip()
        correct_answer = request.POST.get('correct', '').strip()

        request.session['quiz_total'] = request.session.get('quiz_total', 0) + 1

        if user_answer.lower() == correct_answer.lower():
            request.session['quiz_score'] = request.session.get('quiz_score', 0) + 1
            django_messages.success(request, "Sax ✅")
        else:
            request.session['quiz_score'] = request.session.get('quiz_score', 0)
            django_messages.error(request, f"Khalad ❌ (Sax: {correct_answer})")

    return redirect('quiz_page')

def reset_quiz(request):
    request.session.pop('quiz_score', None)
    request.session.pop('quiz_total', None)
    return redirect('quiz_page')