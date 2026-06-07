from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    """Waxay kaydinaysaa casharka ama mawduuca sheekada (bogga cusub)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=255, default="Wada-sheekaysi Cusub")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.created_at.strftime('%Y-%m-%d')})"

class ChatMessage(models.Model):
    """Waxay kaydinaysaa farriin walba oo dhexmarta Qofka iyo AI-ga"""
    SENDER_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:30]}..."