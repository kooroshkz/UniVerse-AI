from django.contrib import admin
from .models import StaffMember


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'phone', 'last_updated')
    search_fields = ('name', 'role', 'email', 'phone', 'tags')
    list_filter = ('role', 'last_updated')
    ordering = ('-last_updated',)
    actions = ['reset_role']

    def reset_role(self, request, queryset):
        queryset.update(role='Not Assigned')
        self.message_user(request, "Selected roles were reset to 'Not Assigned'.")
    reset_role.short_description = 'Reset Role for Selected Staff Members'
