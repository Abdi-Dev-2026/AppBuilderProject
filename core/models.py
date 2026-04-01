from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify # Kani wuxuu u beddelayaa magaca Link qurux badan

class App(models.Model):
    # 'owner' wuxuu ku xirayaa app-ka qofka dhistay.
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=200)
    
    # Slug waa link-ga tusaale: /app/whatsapp-clone/ (Waa inuu unique ahaado)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    # Sawirka App-ka (PC upload ama Link URL)
    icon = models.ImageField(upload_to='app_icons/', null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    
    # Link-ga laga soo dejisto App-ka (Haddii uu jiro APK dibadda ah)
    download_link = models.URLField(null=True, blank=True)

    # --- CODE FIELDS (Halkan ayaa lagu kaydinayaa koodhka uu user-ku qoro) ---
    html_code = models.TextField(
        default="<h1>Ku soo dhawaaw App-kayga</h1>", 
        blank=True, 
        null=True
    )
    css_code = models.TextField(
        default="body { background-color: white; text-align: center; font-family: sans-serif; }", 
        blank=True, 
        null=True
    )
    js_code = models.TextField(
        default="console.log('App-ka waa diyaar!');", 
        blank=True, 
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Function-kan wuxuu si iskiis ah u abuuraa Slug-ga markasta oo App la dhisayo
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        # Waxay Admin-ka ku tusi doontaa Magaca App-ka iyo qofka leh
        return f"{self.name} - {self.owner.username}"