from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# ---------------------------------------------------
# 1. APP MODEL
# ---------------------------------------------------
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


# ---------------------------------------------------
# 2. USER ACTIVITY
# ---------------------------------------------------
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


# ---------------------------------------------------
# 3. SITE SETTINGS
# ---------------------------------------------------
class SiteSetting(models.Model):
    maintenance_mode = models.BooleanField(default=False)
    message = models.TextField(default="Website-ka waxaa ku socda horumarin, fadlan dib u soo laabo.")
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Site Settings"


# ---------------------------------------------------
# 4. CONTENT
# ---------------------------------------------------
class Content(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='content/', null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


# ---------------------------------------------------
# 5. LIKE
# ---------------------------------------------------
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('user', 'content')


# ---------------------------------------------------
# 6. COMMENT
# ---------------------------------------------------
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"


# ---------------------------------------------------
# 7. HOMEPAGE CONTENT
# ---------------------------------------------------
class HomepageContent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Homepage Contents"

    def __str__(self):
        return self.title


# ---------------------------------------------------
# 8. QUIZ
# ---------------------------------------------------
class Quiz(models.Model):
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.question


# ---------------------------------------------------
# 9. POLL
# ---------------------------------------------------
class Poll(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    votes1 = models.IntegerField(default=0)
    votes2 = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question


# ---------------------------------------------------
# 10. CONTACT MESSAGE (FIXED + USER LINK)
# ---------------------------------------------------
class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    reply = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"