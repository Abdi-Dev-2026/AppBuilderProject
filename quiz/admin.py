from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Quiz

@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin):
    list_display = ('question', 'correct_answer', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question',)