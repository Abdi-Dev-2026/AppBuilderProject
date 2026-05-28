from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at', 'is_read')
    readonly_fields = ('created_at',)
   
    fieldsets = (
        ('Xogta Farriinta', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Jawaab-celinta', {
            'fields': ('reply', 'is_read'),
        }),
    )