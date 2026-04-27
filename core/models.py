from django.db import models  # Waa la saxay (V-ga waa laga saaray)
from django.contrib.auth.models import User
from django.utils.text import slugify

# 1. MODEL-KA APP-KA
class App(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    icon = models.ImageField(upload_to='app_icons/', null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    download_link = models.URLField(null=True, blank=True)

    html_code = models.TextField(default="<h1>Ku soo dhawaaw App-kayga</h1>", blank=True, null=True)
    css_code = models.TextField(default="body { background-color: white; text-align: center; font-family: sans-serif; }", blank=True, null=True)
    js_code = models.TextField(default="console.log('App-ka waa diyaar!');", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"


# 2. MODEL-KA USER ACTIVITY
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


# 3. MODEL-KA SITE SETTINGS
class SiteSetting(models.Model):
    maintenance_mode = models.BooleanField(default=False)
    message = models.TextField(default="Website-ka waxaa ku socda horumarin, fadlan dib u soo laabo.")
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Site Settings"


# 4. MODEL-KA CONTENT
class Content(models.Model):
    title = models.CharField(max_length=200, verbose_name="Cinwaanka")
    image = models.ImageField(upload_to='content/', null=True, blank=True, verbose_name="Sawirka")
    video_url = models.URLField(blank=True, null=True, verbose_name="YouTube URL")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


# 5. MODEL-KA LIKE
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('user', 'content')


# 6. MODEL-KA COMMENT
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(verbose_name="Faallada")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"


# 7. MODEL-KA HOMEPAGE CONTENT
class HomepageContent(models.Model):
    title = models.CharField(max_length=100, verbose_name="Cinwaanka")
    description = models.TextField(blank=True, null=True, verbose_name="Sharaxaad")
    image = models.ImageField(upload_to='homepage/', blank=True, null=True, verbose_name="Sawirka")
    video_url = models.URLField(blank=True, null=True, verbose_name="YouTube Link")
    is_active = models.BooleanField(default=True, verbose_name="Muuqaalka (Active)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Homepage Contents"

    def __str__(self):
        return self.title


# 8. MODEL-KA QUIZ (Waa la mideeyay, lana saxay)
class Quiz(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100, blank=True, null=True)
    
    # Waxaan kuu daray doorasho (Choices) si Admin-ka loogu fududeeyo
    ANSWERS = (
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
    )
    correct_answer = models.CharField(max_length=1, choices=ANSWERS, help_text="Dooro nambarka option-ka saxda ah")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.question


# 9. MODEL-KA POLL
class Poll(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    votes1 = models.IntegerField(default=0)
    votes2 = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question