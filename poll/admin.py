from django.contrib import admin
from .models import Poll

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'votes1', 'votes2')
    list_filter = ('is_active',)
    search_fields = ('question',)