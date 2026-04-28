from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    App, UserActivity, SiteSetting, HomepageContent,
    Quiz, Poll, Content, Like, Comment, ContactMessage
)

# ---------------------------------------------------
# 1. APP ADMIN
# ---------------------------------------------------
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)


# ---------------------------------------------------
# 2. USER ACTIVITY ADMIN
# ---------------------------------------------------
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'app_name', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'app_name')
    readonly_fields = ('timestamp',)


# ---------------------------------------------------
# 3. SITE SETTINGS ADMIN
# ---------------------------------------------------
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('maintenance_mode', 'video_url')


# ---------------------------------------------------
# 4. HOMEPAGE CONTENT ADMIN
# ---------------------------------------------------
@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')


# ---------------------------------------------------
# 5. CONTENT ADMIN
# ---------------------------------------------------
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'get_total_likes')
    search_fields = ('title',)

    def get_total_likes(self, obj):
        return obj.total_likes()
    get_total_likes.short_description = 'Total Likes'


# ---------------------------------------------------
# 6. LIKE ADMIN
# ---------------------------------------------------
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')


# ---------------------------------------------------
# 7. COMMENT ADMIN
# ---------------------------------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'text', 'created_at')
    search_fields = ('text', 'user__username')
    list_filter = ('created_at',)


# ---------------------------------------------------
# 8. QUIZ ADMIN (IMPORT / EXPORT)
# ---------------------------------------------------
@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin):
    list_display = ('question', 'correct_answer', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question',)


# ---------------------------------------------------
# 9. POLL ADMIN
# ---------------------------------------------------
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'votes1', 'votes2')
    list_filter = ('is_active',)
    search_fields = ('question',)


# ---------------------------------------------------
# 10. CONTACT MESSAGE ADMIN (FIXED + REPLY SYSTEM)
# ---------------------------------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'reply')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)

    # waxa user-ka arki karo admin panel-ka
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

    # admin-ka kaliya buuxin karo reply
    fields = ('name', 'email', 'subject', 'message', 'reply')