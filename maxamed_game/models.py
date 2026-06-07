from django.db import models
from django.contrib.auth.models import User
from profile_html.models import UserProfile

# SAAXIIB: Waxaan halkan ku kordhinay fields-ka Profiles-ka si ay u aqbalaan video/url
# Tani waxay si dadban u cusboonaysiinaysaa UserProfile-ka haddii uu u baahan yahay.
if not hasattr(UserProfile, 'image_url'):
    UserProfile.add_to_class('image_url', models.URLField(blank=True, null=True))
if not hasattr(UserProfile, 'video_file'):
    UserProfile.add_to_class('video_file', models.FileField(upload_to='profiles/videos/', blank=True, null=True))
if not hasattr(UserProfile, 'video_url'):
    UserProfile.add_to_class('video_url', models.URLField(blank=True, null=True))


# Model-ka kaydinaya macluumaadka Game kasta oo aad ku darto
class Game(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # 1. Maamulka Sawirada (File ahaan iyo URL ahaan)
    icon = models.ImageField(upload_to='game_icons/', blank=True, null=True, help_text="Soo geli sawirka icon-ka ah ee ciyaarta (File)")
    image_url = models.URLField(blank=True, null=True, help_text="Ama halkan ku qor URL-ka tooska ah ee sawirka")
    
    # 2. Maamulka Muuqaalada (File ahaan iyo URL ahaan)
    video_file = models.FileField(upload_to='game_videos/', blank=True, null=True, help_text="Soo geli muuqaal gaar ah (MP4 format) (File)")
    video_url = models.URLField(blank=True, null=True, help_text="Ama halkan ku qor URL-ka tooska ah ee muuqaalka")
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# Model-ka kaydinaya dhibciha (Scores) ciyaartoyda
class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_scores')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='scores')
    high_score = models.IntegerField(default=0)
    last_played = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-high_score']

    def __str__(self):
        return f"{self.user.username} - {self.game.title}: {self.high_score}"