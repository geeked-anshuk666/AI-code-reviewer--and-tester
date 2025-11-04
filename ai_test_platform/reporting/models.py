from django.db import models
from test_management.models import Project
from test_execution.models import TestExecution

class Report(models.Model):
    REPORT_TYPES = [
        ('test_summary', 'Test Summary'),
        ('execution_history', 'Execution History'),
        ('coverage', 'Coverage Report'),
        ('performance', 'Performance Report'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    content = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} - {self.report_type}"

class Dashboard(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='dashboards')
    name = models.CharField(max_length=100)
    configuration = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"