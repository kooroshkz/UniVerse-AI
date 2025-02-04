from django.contrib import admin
from .models import StaffMember, CourseSchedule


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


@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_type', 'start_time', 'end_time', 'locations', 'staffs')
    search_fields = ('course_name', 'course_type', 'locations', 'staffs')
    list_filter = ('course_type', 'start_time', 'end_time')
    ordering = ('-start_time',)
