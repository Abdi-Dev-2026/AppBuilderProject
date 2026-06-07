from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # Tiirarka (Columns) ka soo muuqanaya bogga hore ee Admin-ka
    list_display = ('id', 'get_user_id', 'title', 'device_info', 'created_at', 'updated_at')
    
    # Qaybaha lagu baadhi karo (Search) gudaha Admin-ka
    search_fields = ('user_profile__user_id_code', 'title', 'content', 'device_info')
    
    # Sifaynta (Filters) lagu kala saari karo xogta si fudud
    list_filter = ('device_info', 'created_at', 'updated_at')
    
    # Tiirarka la rabo inay gujismaan (clickable) si note-ka loo beddelo
    list_display_links = ('id', 'title')

    # Kood kooban oo Admin-ka u soo saaraya ID-ga gaarka ah ee isticmaalaha
    def get_user_id(self, obj):
        return obj.user_profile.user_id_code
    get_user_id.short_description = 'User ID Code'