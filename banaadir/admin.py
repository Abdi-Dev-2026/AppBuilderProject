from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Subject, ExamYear, ReadingMaterial, QuizQuestion, GlobalNotice

# Hubi in resource-ka uu ku dhex jiro abka banaadir haddii kale halkan toos ugu dhex samee ama ka soo dhoofi (.resources)
# tusaale: from .resources import ReadingMaterialResource, QuizQuestionResource

@admin.register(ReadingMaterial)
class ReadingMaterialAdmin(ImportExportModelAdmin):
    # resource_class = ReadingMaterialResource  # Fur haddii resource-ka uu diyaar yahay
    list_display = ('title', 'exam_year')
    search_fields = ('title', 'content')


@admin.register(QuizQuestion)
class QuizQuestionAdmin(ImportExportModelAdmin):
    # resource_class = QuizQuestionResource    # Fur haddii resource-ka uu diyaar yahay
    list_display = ('question_text', 'exam_year', 'correct_option_index')
    search_fields = ('question_text',)


class ReadingMaterialInline(admin.TabularInline):
    model = ReadingMaterial
    extra = 1


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 5  


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_emoji')
    search_fields = ('name',)

    fieldsets = (
        ('Warbixinta Guud', {
            'fields': ('name', 'icon_emoji')
        }),
        ('Icon Sawir Ah (Image)', {
            'description': 'Haddii aad rabto sawir, dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('icon_image_file', 'icon_image_url')
        }),
        ('Icon Muuqaal Ah (Video)', {
            'description': 'Haddii aad rabto muuqaal, dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('icon_video_file', 'icon_video_url')
        }),
    )


@admin.register(ExamYear)
class ExamYearAdmin(admin.ModelAdmin):
    list_display = ('subject', 'year')
    list_filter = ('subject', 'year')
    inlines = [ReadingMaterialInline, QuizQuestionInline]


@admin.register(GlobalNotice)
class GlobalNoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
   
    fieldsets = (
        ('Xogta Farriinta', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Sawirka (Image)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('image_file', 'image_url')
        }),
        ('Muuqaalka (Video)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('video_file', 'video_url', 'is_portrait')
        }),
    )