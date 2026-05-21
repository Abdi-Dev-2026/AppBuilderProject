from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Hubi haddii uu horey u jiray profile u dhashay user-kan (Safe Guard)
        if not UserProfile.objects.filter(user=instance).exists():
            UserProfile.objects.create(user=instance)