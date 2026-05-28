from django.contrib import admin
from .models import HomepageContent, SiteSetting

@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
   
    fieldsets = (
        ('Warbixinta Guud', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Sawirka (Image)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('image_file', 'image_url')
        }),
        ('Muuqaalka (Video)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('video_file', 'video_url')
        }),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('maintenance_mode', 'message')
    
    fieldsets = (
        ('Warbixinta Guud', {
            'fields': ('maintenance_mode', 'message')
        }),
        ('Sawirka (Image)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('image_file', 'image_url')
        }),
        ('Muuqaalka (Video)', {
            'description': 'Dooro midkood: Ka soo geli computer-ka ama geli Link',
            'fields': ('video_file', 'video_url')
        }),
    )