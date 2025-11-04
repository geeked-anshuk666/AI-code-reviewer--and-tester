from rest_framework import serializers
from .models import TestExecution, TestResult
from test_management.models import TestCase, Project

class TestExecutionSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    test_case_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = TestExecution
        fields = [
            'id', 'project', 'project_name', 'status', 'started_at', 
            'completed_at', 'duration', 'results', 'created_at', 'test_case_count'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at', 'duration', 'results', 'created_at']

class TestResultSerializer(serializers.ModelSerializer):
    test_case_title = serializers.CharField(source='test_case.title', read_only=True)
    execution_status = serializers.CharField(source='execution.status', read_only=True)
    
    class Meta:
        model = TestResult
        fields = [
            'id', 'execution', 'test_case', 'test_case_title', 'execution_status',
            'result', 'output', 'error_message', 'duration', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class TestExecutionCreateSerializer(serializers.ModelSerializer):
    test_cases = serializers.PrimaryKeyRelatedField(
        queryset=TestCase.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = TestExecution
        fields = ['id', 'project', 'test_cases', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        test_cases = validated_data.pop('test_cases', [])
        execution = TestExecution.objects.create(**validated_data)
        if test_cases:
            execution.test_cases.set(test_cases)
        return execution