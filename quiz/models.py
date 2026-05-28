from django.db import models

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