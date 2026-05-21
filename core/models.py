import os
import string
import re
from django.db import models, transaction, IntegrityError
from django.contrib.auth.models import User
from django.utils.text import slugify

# ---------------------------------------------------
# HELPER: PREFIX INCREMENT & UPLOAD PATHS
# ---------------------------------------------------
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


def get_upload_path(instance, filename):
    """Nidaam si toos ah u habaynaya meesha ay galayaan files-ka TTS"""
    return os.path.join('tts_assets', filename)


# ---------------------------------------------------
# USER ID GENERATOR (SAFE VERSION)
# ---------------------------------------------------
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


# ---------------------------------------------------
# USER PROFILE
# ---------------------------------------------------
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


# ---------------------------------------------------
# CHAT SYSTEM MODELS (HAGAAGSAN)
# ---------------------------------------------------
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"


class ChatSetting(models.Model):
    BG_CHOICES = [
        ('image', 'Sawir (Image)'),
        ('video', 'Muuqaal (Video)'),
    ]
    title = models.CharField(max_length=100, default="MUCJISADA Chat Settings")
    bg_type = models.CharField(max_length=10, choices=BG_CHOICES, default='image', verbose_name="Nooca Background-ka")
    is_video_muted = models.BooleanField(default=True, verbose_name="Mute Muuqaalka")
    
    bg_image_file = models.ImageField(upload_to='chat_bg/', blank=True, null=True, verbose_name="Sawirka Gadaal (File)")
    bg_image_url = models.URLField(blank=True, null=True, verbose_name="Sawirka Gadaal (URL Link)")
    
    bg_video_file = models.FileField(upload_to='chat_bg_videos/', blank=True, null=True, verbose_name="Muuqaalka Gadaal (File)")
    bg_video_url = models.URLField(blank=True, null=True, verbose_name="Muuqaalka Gadaal (URL Link)")

    class Meta:
        verbose_name = "Habaynta Chat-ka"
        verbose_name_plural = "Habaynta Chat-ka"

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Qofka Diray")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name="Qofka Loo Diray")
    message = models.TextField(blank=True, null=True, verbose_name="Fariinta")
    image = models.ImageField(upload_to='chat/images/', blank=True, null=True, verbose_name="Sawirka la diray")
    voice = models.FileField(upload_to='chat/voices/', blank=True, null=True, verbose_name="Codka la diray")
    attachment = models.FileField(upload_to='chat/attachments/', blank=True, null=True, verbose_name="Faylka La Soo Raaciyay")
    is_folder = models.BooleanField(default=False, verbose_name="Ma yahay Folder (Zip/Rar)?")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Waqtiga La Diray")

    class Meta:
        verbose_name = "Fariinta Chat-ka"
        verbose_name_plural = "Fariimaha Chat-ka"
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp.strftime('%H:%M')}"


# ---------------------------------------------------
# APP MODEL
# ---------------------------------------------------
class App(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(upload_to='app_icons/', null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    download_link = models.URLField(null=True, blank=True)
    html_code = models.TextField(default="<h1>Ku soo dhawaaw App-kayga</h1>", blank=True, null=True)
    css_code = models.TextField(default="body { background-color: white; text-align: center; font-family: sans-serif; }", blank=True, null=True)
    js_code = models.TextField(default="console.log('App-ka waa diyaar!');", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while App.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"


# ---------------------------------------------------
# CONTENT (SOCIAL TIMELINE)
# ---------------------------------------------------
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


# ---------------------------------------------------
# BANAADIR EXAMS
# ---------------------------------------------------
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_emoji = models.CharField(max_length=50, default="📚", blank=True, null=True)
    icon_image_file = models.ImageField(upload_to='subject_icons/images/', blank=True, null=True)
    icon_image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Link-ga sawirka icon-ka")
    icon_video_file = models.FileField(upload_to='subject_icons/videos/', blank=True, null=True)
    icon_video_url = models.URLField(max_length=500, blank=True, null=True, help_text="Link-ga muuqaalka icon-ka")

    def __str__(self):
        return self.name


class ExamYear(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='years')
    year = models.IntegerField()

    class Meta:
        unique_together = ('subject', 'year')

    def __str__(self):
        return f"{self.subject.name} - {self.year}"


class ReadingMaterial(models.Model):
    exam_year = models.ForeignKey(ExamYear, on_delete=models.CASCADE, related_name='readings')
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.exam_year})"


class QuizQuestion(models.Model):
    exam_year = models.ForeignKey(ExamYear, on_delete=models.CASCADE, related_name='quizzes')
    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option_index = models.IntegerField(help_text="Geli 0 haddii option1 sax yahay, 1 haddii option2...")

    def __str__(self):
        return f"Q: {self.question_text[:50]}..."


# ---------------------------------------------------
# HOMEPAGE & SETTINGS
# ---------------------------------------------------
class HomepageContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to='homepage/images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Link-ga sawirka")
    video_file = models.FileField(upload_to='homepage/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="Link-ga muuqaalka (YouTube/Vimeo)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Homepage Contents"

    def __str__(self):
        return self.title


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "User Activities"

    def __str__(self):
        return f"{self.user.username} - {self.action}"


class SiteSetting(models.Model):
    maintenance_mode = models.BooleanField(default=False)
    message = models.TextField(default="Horumarin ayaa socota...")
    image_file = models.ImageField(upload_to='settings/images/', blank=True, null=True, verbose_name="Soo geli Sawir (File)")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Sawir Link ah (URL)")
    video_file = models.FileField(upload_to='settings/videos/', blank=True, null=True, verbose_name="Soo geli Muuqaal (File)")
    video_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Muuqaal Link ah (URL)")

    def __str__(self):
        return "Site Settings"


class Quiz(models.Model):
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"


# ---------------------------------------------------
# GLOBAL NOTICE & ADS SYSTEM
# ---------------------------------------------------
class GlobalNotice(models.Model):
    title = models.CharField(max_length=250, verbose_name="Ciwaanka Ogeysiiska/Xayeysiiska")
    description = models.TextField(blank=True, null=True, verbose_name="Faahfaahinta Qoraalka")
    image_file = models.ImageField(upload_to='notices/images/', blank=True, null=True, verbose_name="Soo geli Sawir (File)")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Sawir Link ah (URL)")
    video_file = models.FileField(upload_to='notices/videos/', blank=True, null=True, verbose_name="Soo geli Muuqaal (File)")
    video_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Muuqaal Link ah (URL - YouTube)")
    is_portrait = models.BooleanField(default=False, verbose_name="Muuqaalku ma taagan yahay? (Shorts/TikTok size)")
    is_active = models.BooleanField(default=True, verbose_name="Muu muuqanayaa App-ka? (Active)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Global Notice & Ad"
        verbose_name_plural = "Global Notices & Ads"

    def __str__(self):
        return self.title


# ---------------------------------------------------
# TTS GLOBAL SETTINGS
# ---------------------------------------------------
class TTSSetting(models.Model):
    title = models.CharField(max_length=100, default="TTS Global Settings")
    max_characters = models.PositiveIntegerField(default=1000, help_text="Tirada ugu badan ee xarfaha qofku qori karo hal mar.")
    bg_image_file = models.ImageField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Sawirka Gadaal (File)")
    bg_image_url = models.URLField(blank=True, null=True, verbose_name="Sawirka Gadaal (URL Link)")
    bg_video_file = models.FileField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Muuqaalka Gadaal (File)")
    bg_video_url = models.URLField(blank=True, null=True, verbose_name="Muuqaalka Gadaal (URL Link)")
    
    faiza_avatar_image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Faiza Avatar (Sawir)")
    faiza_avatar_video = models.FileField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Faiza Avatar (Muuqaal Loop ah)")
    
    maxamed_avatar_image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Maxamed Avatar (Sawir)")
    maxamed_avatar_video = models.FileField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Maxamed Avatar (Muuqaal Loop ah)")

    class Meta:
        verbose_name = "TTS Setting"
        verbose_name_plural = "TTS Settings"

    def __str__(self):
        return self.title


# ---------------------------------------------------
# MAINTENANCE SETTING
# ---------------------------------------------------
class MaintenanceSetting(models.Model):
    message = models.TextField()
    video_file = models.FileField(upload_to='maintenance/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    image_file = models.ImageField(upload_to='maintenance/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_portrait = models.BooleanField(default=False, help_text="Gali calaamad haddii sawirka/video-gu yahay mid taagan")

    def __str__(self):
        return f"Maintenance Mode: {self.message[:30]}..."


# ---------------------------------------------------
# POLL SYSTEM
# ---------------------------------------------------
class Poll(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    votes1 = models.IntegerField(default=0)
    votes2 = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    @property
    def total_votes(self):
        return self.votes1 + self.votes2

    @property
    def pct1(self):
        total = self.total_votes
        return round((self.votes1 / total) * 100) if total > 0 else 0

    @property
    def pct2(self):
        total = self.total_votes
        return round((self.votes2 / total) * 100) if total > 0 else 0

    def __str__(self):
        return self.question