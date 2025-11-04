from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class TestCase(models.Model):
    TEST_TYPES = [
        ('unit', 'Unit Test'),
        ('integration', 'Integration Test'),
        ('e2e', 'End-to-End Test'),
        ('api', 'API Test'),
        ('ui', 'UI Test'),
    ]
    
    TEST_STATUS = [
        ('draft', 'Draft'),
        ('ready', 'Ready for Execution'),
        ('running', 'Running'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    test_type = models.CharField(max_length=20, choices=TEST_TYPES, default='unit')
    status = models.CharField(max_length=20, choices=TEST_STATUS, default='draft')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_cases')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ai_generated = models.BooleanField(default=False)
    test_code = models.TextField(blank=True, help_text="Generated test code")

    def __str__(self):
        return f"{self.title} ({self.test_type})"

    class Meta:
        ordering = ['-created_at']