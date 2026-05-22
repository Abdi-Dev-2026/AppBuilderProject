from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import SchoolProfile, StudentResult
from .resources import StudentResultResource

@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'admin_user', 'sender_phone_number', 'subscription_years', 'amount_paid', 'is_active', 'created_at')
    list_filter = ('is_active', 'payment_method', 'created_at')
    search_fields = ('school_name', 'sender_phone_number', 'admin_user__username')
    actions = ['activate_schools', 'deactivate_schools']

    def activate_schools(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Iskuulada la doortay si guul ah ayaa loo hawlgaliyay!")
    activate_schools.short_description = "✔️ Ka dhig Iskuulada Active"

    def deactivate_schools(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Iskuulada la doortay waa laga joojiyay shaqada.")
    deactivate_schools.short_description = "❌ Ka dhig Iskuulada Inactive"


@admin.register(StudentResult)
class StudentResultAdmin(ImportExportModelAdmin):
    resource_class = StudentResultResource
    # Halkan waxaan ku soo qoray xogtii moodeelkaaga rasmiga ah saaxiib
    list_display = ('full_name', 'roll_number', 'school', 'celceliska', 'goaan', 'created_at')
    list_filter = ('school', 'celceliska', 'goaan')
    search_fields = ('full_name', 'roll_number', 'school__school_name')