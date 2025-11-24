
from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'is_active', 'created_at']
    list_filter = ['job_type', 'is_active', 'created_at']
    search_fields = ['title', 'company', 'location', 'description']
    list_editable = ['is_active']
    prepopulated_fields = {}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'location', 'job_type', 'department', 'salary_range')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'responsibilities')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )