from django.contrib import admin
from .models import TestExecution, TestResult

@admin.register(TestExecution)
class TestExecutionAdmin(admin.ModelAdmin):
    list_display = ['project', 'status', 'started_at', 'completed_at', 'created_at']
    list_filter = ['status', 'started_at', 'completed_at', 'project']
    search_fields = ['project__name']
    readonly_fields = ['created_at', 'started_at', 'completed_at', 'duration']

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['test_case', 'execution', 'result', 'created_at']
    list_filter = ['result', 'created_at', 'execution']
    search_fields = ['test_case__title', 'execution__project__name']
    readonly_fields = ['created_at']