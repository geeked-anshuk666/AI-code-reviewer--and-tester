from django.contrib import admin
from .models import CodeRepository, CodeFile, CodeAnalysis

@admin.register(CodeRepository)
class CodeRepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'language', 'created_at']
    list_filter = ['language', 'created_at', 'project']
    search_fields = ['name', 'url']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CodeFile)
class CodeFileAdmin(admin.ModelAdmin):
    list_display = ['file_path', 'repository', 'language', 'created_at']
    list_filter = ['language', 'created_at', 'repository']
    search_fields = ['file_path']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CodeAnalysis)
class CodeAnalysisAdmin(admin.ModelAdmin):
    list_display = ['code_file', 'analysis_type', 'created_at']
    list_filter = ['analysis_type', 'created_at']
    readonly_fields = ['created_at']