from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from contact.models import ContactMessage

@login_required
def my_messages(request):
    messages_list = ContactMessage.objects.filter(
        email__iexact=request.user.email
    ).order_by('-created_at')

    return render(request, 'my_messages/my_messages.html', {'messages': messages_list})