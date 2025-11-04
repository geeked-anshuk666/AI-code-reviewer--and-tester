from django.contrib import admin
from .models import Project, TestCase

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at']
    list_filter = ['created_at', 'owner']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'test_type', 'status', 'project', 'created_by', 'created_at']
    list_filter = ['test_type', 'status', 'created_at', 'project']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']