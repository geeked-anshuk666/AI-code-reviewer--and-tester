from rest_framework import serializers
from .models import Report, Dashboard
from test_management.models import Project

class ReportSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    generated_by_name = serializers.CharField(source='generated_by.username', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'project', 'project_name', 'report_type', 'title', 
            'content', 'generated_at', 'generated_by', 'generated_by_name'
        ]
        read_only_fields = ['id', 'generated_at', 'generated_by']

class DashboardSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Dashboard
        fields = [
            'id', 'project', 'project_name', 'name', 'configuration', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']