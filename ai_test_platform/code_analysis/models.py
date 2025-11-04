from django.db import models
from django.contrib.auth.models import User
from test_management.models import Project

class CodeRepository(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=200)
    url = models.URLField()
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"

class CodeFile(models.Model):
    repository = models.ForeignKey(CodeRepository, on_delete=models.CASCADE, related_name='files')
    file_path = models.CharField(max_length=500)
    content = models.TextField()
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.repository.name} - {self.file_path}"

class CodeAnalysis(models.Model):
    code_file = models.ForeignKey(CodeFile, on_delete=models.CASCADE, related_name='analyses')
    analysis_type = models.CharField(max_length=100)  # e.g., 'function_detection', 'class_detection'
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis of {self.code_file.file_path} - {self.analysis_type}"