from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.contrib.auth.models import User
from profile_html.models import UserProfile
from .models import FriendRequest

@login_required
def chats_page(request):
    search_query = request.GET.get('search_id')
    search_result = None
    if search_query:
        search_result = UserProfile.objects.filter(user_id_code=search_query).first()

    my_profile, created = UserProfile.objects.get_or_create(user=request.user)
    friend_ids = my_profile.friends.values_list('id', flat=True)
    all_users = UserProfile.objects.exclude(user=request.user)
    pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')

    return render(request, 'chats/chats.html', {
        'all_users': all_users,
        'search_result': search_result,
        'pending_requests': pending_requests,
        'friend_ids': friend_ids,
        'my_profile': my_profile
    })

@login_required
def send_friend_request(request, profile_id):
    receiver_profile = get_object_or_404(UserProfile, id=profile_id)
    receiver_user = receiver_profile.user
    
    if receiver_user != request.user:
        FriendRequest.objects.get_or_create(sender=request.user, receiver=receiver_user)
        django_messages.success(request, f"Codsiga saaxiibtinimo waa loo diray {receiver_user.username} ✅")
    
    return redirect('chats_page')

@login_required
def accept_request(request, request_id):
    friend_req = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_req.status = 'accepted'
    friend_req.save()
    
    request.user.userprofile.friends.add(friend_req.sender)
    friend_req.sender.userprofile.friends.add(request.user)
    
    django_messages.success(request, f"Hadda waad wada hadli kartaan {friend_req.sender.username}!")
    return redirect('chats_page')

@login_required
def reject_request(request, request_id):
    friend_req = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_req.delete()
    django_messages.info(request, "Codsigii saaxiibtinimo waa la diiday.")
    return redirect('chats_page')