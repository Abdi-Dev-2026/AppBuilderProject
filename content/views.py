from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Content, Like, Comment

def content_page(request):
    all_contents = Content.objects.all().order_by('-created_at')
    return render(request, 'content/content.html', {'all_contents': all_contents})

@login_required
def like_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    like, created = Like.objects.get_or_create(user=request.user, content=content)

    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def add_comment(request, content_id):
    content = get_object_or_404(Content, id=content_id)

    if request.method == "POST":
        text = request.POST.get("comment_text", "").strip()
        if text:
            Comment.objects.create(
                user=request.user,
                content=content,
                text=text
            )

    return redirect(request.META.get('HTTP_REFERER', 'home'))