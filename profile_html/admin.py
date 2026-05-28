from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id_code', 'first_name', 'father_name')
    search_fields = ('user__username', 'user_id_code', 'first_name')
    readonly_fields = ('user_id_code',)