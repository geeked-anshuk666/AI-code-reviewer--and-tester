from django.db import models
from test_management.models import TestCase, Project

class TestExecution(models.Model):
    EXECUTION_STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_executions')
    test_cases = models.ManyToManyField(TestCase, related_name='executions')
    status = models.CharField(max_length=20, choices=EXECUTION_STATUS, default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)  # in seconds
    results = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Execution for {self.project.name} - {self.status}"

class TestResult(models.Model):
    EXECUTION_RESULT = [
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
        ('error', 'Error'),
    ]
    
    execution = models.ForeignKey(TestExecution, on_delete=models.CASCADE, related_name='test_results')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='test_results')
    result = models.CharField(max_length=20, choices=EXECUTION_RESULT)
    output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    duration = models.FloatField(null=True, blank=True)  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Result for {self.test_case.title} - {self.result}"