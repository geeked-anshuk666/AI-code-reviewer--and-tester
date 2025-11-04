from django.contrib import admin
from .models import Report, Dashboard

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'report_type', 'generated_at', 'generated_by']
    list_filter = ['report_type', 'generated_at', 'project']
    search_fields = ['title', 'project__name']
    readonly_fields = ['generated_at']

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'project']
    search_fields = ['name', 'project__name']
    readonly_fields = ['created_at', 'updated_at']