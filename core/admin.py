from django.contrib import admin
from .models import App, UserActivity, SiteSetting

# 1. Admin-ka App-ka
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'owner__username')

# 2. Admin-ka User Activity
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'app_name', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'app_name')

# 3. Admin-ka Site Settings (Maintenance Mode)
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('maintenance_mode',)