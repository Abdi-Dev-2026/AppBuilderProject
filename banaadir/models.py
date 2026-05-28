from django.db import models

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