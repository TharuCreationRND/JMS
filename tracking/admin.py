
from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'job_number', 'center', 'item_type', 'status',
        'job_date', 'finish_date', 'created_by'
    )
    list_filter = ('status', 'center', 'item_type')
    search_fields = ('job_number', 'center', 'item_type', 'serial_number')
