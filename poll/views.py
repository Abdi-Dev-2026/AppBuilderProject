from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll

def poll_page(request):
    polls = Poll.objects.filter(is_active=True).order_by('-id')
    return render(request, 'poll/poll.html', {'polls': polls})

def vote_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == "POST":
        choice = request.POST.get("choice")

        if choice == "1":
            poll.votes1 += 1
        elif choice == "2":
            poll.votes2 += 1

        poll.save()

    return redirect('poll_page')