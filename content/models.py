from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
    title = models.CharField(max_length=200)
    body_text = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to='content/images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Link-ga sawirka")
    video_file = models.FileField(upload_to='content/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="Link-ga muuqaalka (YouTube/Vimeo)")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('user', 'content')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.content.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"