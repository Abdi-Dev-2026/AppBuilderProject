from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

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