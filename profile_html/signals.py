from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Maadaama uu ku dhex jiro isla app-ka, waxaan si toos ah uga soo dhoofsanaynaa .models
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)