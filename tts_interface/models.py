import os
from django.db import models

def get_upload_path(instance, filename):
    return os.path.join('tts_assets', filename)

class TTSSetting(models.Model):
    title = models.CharField(max_length=100, default="TTS Global Settings")
    max_characters = models.PositiveIntegerField(default=1000, help_text="Tirada ugu badan ee xarfaha qofku qori karo hal mar.")
    
    # Background Media
    bg_image_file = models.ImageField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Sawirka Gadaal (File)")
    bg_image_url = models.URLField(blank=True, null=True, verbose_name="Sawirka Gadaal (URL Link)")
    bg_video_file = models.FileField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Muuqaalka Gadaal (File)")
    bg_video_url = models.URLField(blank=True, null=True, verbose_name="Muuqaalka Gadaal (URL Link)")

    # Faiza Avatar
    faiza_avatar_image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Faiza Avatar (Sawir)")
    faiza_avatar_video = models.FileField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Faiza Avatar (Muuqaal Loop ah)")

    # Maxamed Avatar
    maxamed_avatar_image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Maxamed Avatar (Sawir)")
    maxamed_avatar_video = models.FileField(upload_to=get_upload_path, blank=True, null=True, verbose_name="Maxamed Avatar (Muuqaal Loop ah)")

    def __str__(self):
        return self.title