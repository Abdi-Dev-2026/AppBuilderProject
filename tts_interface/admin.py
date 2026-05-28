from django.contrib import admin
from .models import TTSSetting

@admin.register(TTSSetting)
class TTSSettingAdmin(admin.ModelAdmin):
    list_display = ('title', 'max_characters')
    
    fieldsets = (
        ('Xaddidaadda Qoraalka', {
            'fields': ('title', 'max_characters')
        }),
        ('Muuqaalka Gadaal (Background Media)', {
            'description': 'Muuqaalka ama sawirka dhalada ka dambeeya ee Interface-ka TTS',
            'fields': ('bg_image_file', 'bg_image_url', 'bg_video_file', 'bg_video_url')
        }),
        ('Avatar-ka Faiza (Codka Dumarka)', {
            'description': 'Sawirka ama Muuqaalka yar ee goobada ugu muuqanaya Faiza',
            'fields': ('faiza_avatar_image', 'faiza_avatar_video')
        }),
        ('Avatar-ka Maxamed (Codka Ragga)', {
            'description': 'Sawirka ama Muuqaalka yar ee goobada ugu muuqanaya Maxamed',
            'fields': ('maxamed_avatar_image', 'maxamed_avatar_video')
        }),
    )