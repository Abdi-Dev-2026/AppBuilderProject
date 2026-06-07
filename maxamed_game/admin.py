from django.contrib import admin
from django.utils.html import format_html
from .models import Game, GameScore

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    # Waxyaabaha ku soo muuqanaya liiska guud ee Admin-ka
    list_display = ('title', 'slug', 'is_active', 'media_preview')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    
    # Inuu slug-ga si iskood ah u qoro markaad Title-ka qoraysid
    prepopulated_fields = {'slug': ('title',)}
    
    # Meelaha xogta lagu kala nidaamiyo markaad wax ku daraysid (Fieldsets)
    fieldsets = (
        ('Macluumaadka Ciyaarta', {
            'fields': ('title', 'slug', 'description', 'is_active')
        }),
        ('Maamulka Sawirada (Images)', {
            'fields': ('icon', 'image_url'),
            'description': 'Dooro mid uun: Soo geli fayl ama dhig URL toos ah.'
        }),
        ('Maamulka Muuqaalada (Videos)', {
            'fields': ('video_file', 'video_url'),
            'description': 'Dooro mid uun: Soo geli fayl MP4 ah ama dhig URL toos ah.'
        }),
    )

    # Function kuu tusaya sawirka ama muuqaalka uu leeyahay Game-ku gudaha Admin-ka
    def media_preview(self, obj):
        if obj.video_url:
            return format_html('<video src="{}" style="width:50px; height:50px; object-fit:cover; border-radius:8px;" muted></video>', obj.video_url)
        elif obj.video_file:
            return format_html('<video src="{}" style="width:50px; height:50px; object-fit:cover; border-radius:8px;" muted></video>', obj.video_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="width:50px; height:50px; object-fit:cover; border-radius:8px;" />', obj.image_url)
        elif obj.icon:
            return format_html('<img src="{}" style="width:50px; height:50px; object-fit:cover; border-radius:8px;" />', obj.icon.url)
        return "Waxba la mada madiyin"
        
    media_preview.short_description = 'Muuqaalka / Icon'


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'high_score', 'last_played')
    list_filter = ('game', 'last_played')
    search_fields = ('user__username', 'game__title')