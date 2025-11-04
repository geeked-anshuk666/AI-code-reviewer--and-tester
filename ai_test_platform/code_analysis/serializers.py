from rest_framework import serializers
from .models import CodeRepository, CodeFile, CodeAnalysis

class CodeRepositorySerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = CodeRepository
        fields = ['id', 'project', 'project_name', 'name', 'url', 'language', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CodeFileSerializer(serializers.ModelSerializer):
    repository_name = serializers.CharField(source='repository.name', read_only=True)
    
    class Meta:
        model = CodeFile
        fields = ['id', 'repository', 'repository_name', 'file_path', 'content', 'language', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CodeAnalysisSerializer(serializers.ModelSerializer):
    file_path = serializers.CharField(source='code_file.file_path', read_only=True)
    
    class Meta:
        model = CodeAnalysis
        fields = ['id', 'code_file', 'file_path', 'analysis_type', 'result', 'created_at']
        read_only_fields = ['id', 'created_at']