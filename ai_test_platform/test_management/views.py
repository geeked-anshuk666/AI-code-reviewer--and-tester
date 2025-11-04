from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Project, TestCase
from .serializers import ProjectSerializer, TestCaseSerializer
from .ai_generator import AITestGenerator
from code_analysis.models import CodeAnalysis

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return only projects owned by the current user
        return Project.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Set the owner to the current user
        serializer.save(owner=self.request.user)

class TestCaseViewSet(viewsets.ModelViewSet):
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return only test cases belonging to projects owned by the current user
        return TestCase.objects.filter(project__owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_project(self, request):
        project_id = request.query_params.get('project_id', None)
        if project_id is not None:
            test_cases = TestCase.objects.filter(
                project_id=project_id,
                project__owner=self.request.user
            )
            serializer = self.get_serializer(test_cases, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'project_id parameter is required'}, status=400)
    
    @action(detail=True, methods=['post'])
    def generate_code(self, request, pk=None):
        test_case = get_object_or_404(TestCase, pk=pk, project__owner=self.request.user)
        # This is where we would integrate with our AI code generation
        # For now, we'll just return a placeholder
        generated_code = f"# Generated test code for {test_case.title}\n# This would be implemented with AI in the full version"
        test_case.test_code = generated_code
        test_case.save()
        return Response({'test_code': generated_code})
    
    @action(detail=False, methods=['post'])
    def generate_from_analysis(self, request):
        """
        Generate test cases based on code analysis results.
        """
        analysis_id = request.data.get('analysis_id')
        project_id = request.data.get('project_id')
        
        if not analysis_id or not project_id:
            return Response({'error': 'analysis_id and project_id are required'}, status=400)
        
        # Get the analysis and project
        analysis = get_object_or_404(CodeAnalysis, id=analysis_id)
        project = get_object_or_404(Project, id=project_id, owner=self.request.user)
        
        # Generate test cases using AI
        generator = AITestGenerator()
        test_cases = generator.generate_tests_from_analysis(analysis, project)
        
        # Set the created_by for each test case
        for test_case in test_cases:
            test_case.created_by = self.request.user
            test_case.save()
        
        # Serialize the created test cases
        serializer = TestCaseSerializer(test_cases, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_comprehensive_tests(self, request):
        """
        Generate comprehensive test suite based on multiple analysis results.
        """
        project_id = request.data.get('project_id')
        analysis_ids = request.data.get('analysis_ids', [])
        
        if not project_id:
            return Response({'error': 'project_id is required'}, status=400)
        
        # Get the project
        project = get_object_or_404(Project, id=project_id, owner=self.request.user)
        
        # Get all analyses
        analyses = CodeAnalysis.objects.filter(id__in=analysis_ids)
        
        # Generate test cases using AI for each analysis
        all_test_cases = []
        generator = AITestGenerator()
        
        for analysis in analyses:
            test_cases = generator.generate_tests_from_analysis(analysis, project)
            all_test_cases.extend(test_cases)
        
        # Set the created_by for each test case
        for test_case in all_test_cases:
            test_case.created_by = self.request.user
            test_case.save()
        
        # Serialize the created test cases
        serializer = TestCaseSerializer(all_test_cases, many=True)
        return Response(serializer.data)