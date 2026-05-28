from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import ChatMessage

@login_required
def chat_with_user(request, username):
    other_user = get_object_or_404(User, username=username)
    
    if other_user not in request.user.userprofile.friends.all():
        django_messages.error(request, "Waa inaad saaxiib noqotaan si aad u wada hadashaan.")
        return redirect('chats_page')

    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    if request.method == "POST":
        msg_text = request.POST.get('message')
        attachment = request.FILES.get('attachment')
        is_folder = request.POST.get('is_folder') == 'true'

        if msg_text or attachment:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=other_user,
                message=msg_text,
                attachment=attachment,
                is_folder=is_folder
            )
        return redirect('chat_with_user', username=username)

    return render(request, 'chat_window/chat_window.html', {
        'other_user': other_user,
        'chat_messages': messages
    })