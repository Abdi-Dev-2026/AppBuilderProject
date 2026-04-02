from django.contrib import admin
from .models import App, UserActivity

# Maamulka Apps-ka
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')

# Maamulka User Activities (CUSUB)
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'app_name', 'timestamp', 'ip_address')
    list_filter = ('timestamp', 'action')
    search_fields = ('user__username', 'app_name')
    readonly_fields = ('user', 'action', 'app_name', 'timestamp', 'ip_address')