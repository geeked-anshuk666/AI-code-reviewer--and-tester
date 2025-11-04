from django.db import models
from django.contrib.auth.models import User

class IDEPlugin(models.Model):
    """
    Represents an IDE plugin installation.
    """
    IDE_CHOICES = [
        ('vscode', 'Visual Studio Code'),
        ('pycharm', 'PyCharm'),
        ('intellij', 'IntelliJ IDEA'),
        ('vim', 'Vim'),
        ('neovim', 'Neovim'),
        ('sublime', 'Sublime Text'),
        ('atom', 'Atom'),
        ('eclipse', 'Eclipse'),
        ('other', 'Other IDE'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ide_name = models.CharField(max_length=20, choices=IDE_CHOICES)
    plugin_version = models.CharField(max_length=20)
    installed_at = models.DateTimeField(auto_now_add=True)
    last_connected = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_ide_name_display()}"

class IDEConnection(models.Model):
    """
    Tracks connections from IDE plugins to the platform.
    """
    plugin = models.ForeignKey(IDEPlugin, on_delete=models.CASCADE)
    connection_token = models.CharField(max_length=100, unique=True)
    connected_at = models.DateTimeField(auto_now_add=True)
    disconnected_at = models.DateTimeField(null=True, blank=True)
    is_connected = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Connection for {self.plugin}"

class IDEEvent(models.Model):
    """
    Tracks events from IDE plugins (code reviews, test generations, etc.).
    """
    EVENT_TYPES = [
        ('code_review', 'Code Review Requested'),
        ('test_generation', 'Test Generation Requested'),
        ('test_execution', 'Test Execution Requested'),
        ('code_fix', 'Code Fix Applied'),
        ('security_scan', 'Security Scan Requested'),
    ]
    
    plugin = models.ForeignKey(IDEPlugin, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    file_path = models.CharField(max_length=500, blank=True)
    line_number = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.get_event_type_display()} - {self.plugin}"