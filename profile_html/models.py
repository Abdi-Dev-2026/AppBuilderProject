import re
import string
from django.db import models, transaction, IntegrityError
from django.contrib.auth.models import User

def increment_prefix(prefix):
    letters = string.ascii_uppercase
    prefix = list(prefix)
    i = len(prefix) - 1
    while i >= 0:
        if prefix[i] != 'Z':
            prefix[i] = letters[letters.index(prefix[i]) + 1]
            return ''.join(prefix)
        else:
            prefix[i] = 'A'
            i -= 1
    return 'A' + ''.join(prefix)

def generate_user_id():
    last_user = UserProfile.objects.select_for_update().order_by('-id').first()
    if not last_user:
        return "0001"
    last_code = last_user.user_id_code or "0000"
    match = re.match(r"([A-Z]*)(\d+)", last_code)
    if not match:
        return "0001"
    prefix = match.group(1)
    number = int(match.group(2)) + 1
    if number >= 10000:
        number = 1
        prefix = increment_prefix(prefix) if prefix else "A"
    return f"{prefix}{number:04d}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    grandfather_name = models.CharField(max_length=100, null=True, blank=True)
    user_id_code = models.CharField(max_length=20, unique=True, blank=True)
    friends = models.ManyToManyField(User, related_name='user_friends', blank=True, db_table='user_profile_friends_map')

    def save(self, *args, **kwargs):
        if not self.user_id_code:
            with transaction.atomic():
                self.user_id_code = generate_user_id()
                try:
                    super().save(*args, **kwargs)
                except IntegrityError:
                    self.user_id_code = generate_user_id()
                    super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.user_id_code}"