from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Report, Dashboard
from .serializers import ReportSerializer, DashboardSerializer
from test_management.models import Project
from test_execution.models import TestExecution, TestResult

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Report.objects.filter(project__owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate_summary(self, request):
        """
        Generate a test summary report for a project.
        """
        project_id = request.data.get('project_id')
        if not project_id:
            return Response({'error': 'project_id is required'}, status=400)
        
        project = get_object_or_404(Project, id=project_id, owner=self.request.user)
        
        # Get recent test executions
        executions = TestExecution.objects.filter(project=project).order_by('-created_at')[:10]
        
        # Generate summary data
        summary_data = {
            'project_name': project.name,
            'total_executions': executions.count(),
            'recent_executions': []
        }
        
        for execution in executions:
            execution_data = {
                'id': execution.id,
                'status': execution.status,
                'started_at': execution.started_at,
                'completed_at': execution.completed_at,
                'duration': execution.duration,
                'results': execution.results
            }
            summary_data['recent_executions'].append(execution_data)
        
        # Create the report
        report = Report.objects.create(
            project=project,
            report_type='test_summary',
            title=f'Test Summary for {project.name} - {timezone.now().strftime("%Y-%m-%d")}',
            content=summary_data,
            generated_by=self.request.user
        )
        
        serializer = ReportSerializer(report)
        return Response(serializer.data)

class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Dashboard.objects.filter(project__owner=self.request.user)
    
    def perform_create(self, serializer):
        # Verify the project belongs to the user
        project = get_object_or_404(Project, id=self.request.data.get('project'), owner=self.request.user)
        serializer.save()