from django.db import models

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


class SiteSetting(models.Model):
    maintenance_mode = models.BooleanField(default=False)
    message = models.TextField(default="Horumarin ayaa socota...")
    image_file = models.ImageField(upload_to='settings/images/', blank=True, null=True, verbose_name="Soo geli Sawir (File)")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Sawir Link ah (URL)")
    video_file = models.FileField(upload_to='settings/videos/', blank=True, null=True, verbose_name="Soo geli Muuqaal (File)")
    video_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Muuqaal Link ah (URL)")

    def __str__(self):
        return "Site Settings"