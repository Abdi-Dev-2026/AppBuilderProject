from django.contrib import admin
from import_export.admin import ImportExportModelAdmin  # Tan waa muhiim in la soo dhisiyo
from .models import (
    App, UserActivity, SiteSetting, HomepageContent, 
    Quiz, Poll, Content, Like, Comment
)

# 1. Admin-ka App-ka
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)

# 2. Admin-ka User Activity
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'app_name', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'app_name')
    readonly_fields = ('timestamp', 'ip_address')

# 3. Admin-ka Site Settings
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('maintenance_mode', 'video_url')

# 4. Admin-ka Homepage Content
@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')

# 5. Admin-ka Content (Post-yada)
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'get_total_likes')
    search_fields = ('title',)

    def get_total_likes(self, obj):
        return obj.total_likes()
    get_total_likes.short_description = 'Total Likes'

# 6. Admin-ka Like & Comment
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'text', 'created_at')
    search_fields = ('text', 'user__username')
    list_filter = ('created_at',)

# -----------------------------------------------------------
# 7. ADMIN-KA QUIZ (CUSBOONAYSIIN: IMPORT/EXPORT)
# -----------------------------------------------------------
@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin): # Kani wuxuu kuu oggolaanayaa soo gelinta kumanaan su'aalood
    list_display = ('question', 'correct_answer', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question',)

# 8. Admin-ka Poll
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'votes1', 'votes2')
    list_filter = ('is_active',)
    search_fields = ('question',)