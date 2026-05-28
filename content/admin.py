from django.contrib import admin
from .models import Content, Like, Comment

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'get_total_likes')
    search_fields = ('title', 'body_text')
    list_filter = ('created_at',)

    def get_total_likes(self, obj):
        return obj.total_likes
    get_total_likes.short_description = 'Total Likes'

    fieldsets = (
        ('Xogta Maqaalka', {
            'fields': ('title', 'body_text'),
        }),
        ('Sawirka (Image)', {
            'fields': ('image_file', 'image_url')
        }),
        ('Muuqaalka (Video)', {
            'fields': ('video_file', 'video_url')
        }),
        ('Xogta Kale', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'text', 'created_at')
    search_fields = ('text', 'user__username')
    list_filter = ('created_at',)