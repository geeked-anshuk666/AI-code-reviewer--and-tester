from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import CodeRepository, CodeFile, CodeAnalysis
from .serializers import CodeRepositorySerializer, CodeFileSerializer, CodeAnalysisSerializer
from .ai_analyzer import AIAnalyzer
from test_management.models import Project

class CodeRepositoryViewSet(viewsets.ModelViewSet):
    serializer_class = CodeRepositorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CodeRepository.objects.filter(project__owner=self.request.user)
    
    def perform_create(self, serializer):
        # Check if the project belongs to the current user
        project = get_object_or_404(Project, id=self.request.data.get('project'), owner=self.request.user)
        serializer.save()

class CodeFileViewSet(viewsets.ModelViewSet):
    serializer_class = CodeFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CodeFile.objects.filter(repository__project__owner=self.request.user)
    
    @action(detail=False, methods=['post'])
    def analyze_file(self, request):
        file_id = request.data.get('file_id')
        analysis_type = request.data.get('analysis_type', 'basic')
        
        if not file_id:
            return Response({'error': 'file_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        code_file = get_object_or_404(CodeFile, id=file_id, repository__project__owner=self.request.user)
        
        # Perform AI-powered code analysis
        analyzer = AIAnalyzer()
        if analysis_type == 'quality':
            analysis_result = analyzer.analyze_code_quality(code_file.content, code_file.language)
        else:
            analysis_result = analyzer.analyze_code_structure(code_file.content, code_file.language)
        
        analysis = CodeAnalysis.objects.create(
            code_file=code_file,
            analysis_type=analysis_type,
            result=analysis_result
        )
        
        serializer = CodeAnalysisSerializer(analysis)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_test_recommendations(self, request):
        file_id = request.data.get('file_id')
        
        if not file_id:
            return Response({'error': 'file_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        code_file = get_object_or_404(CodeFile, id=file_id, repository__project__owner=self.request.user)
        
        # Perform AI-powered code analysis
        analyzer = AIAnalyzer()
        analysis_result = analyzer.analyze_code_structure(code_file.content, code_file.language)
        
        # Generate test recommendations
        recommendations = analyzer.generate_test_recommendations(analysis_result)
        
        # Create analysis record
        analysis = CodeAnalysis.objects.create(
            code_file=code_file,
            analysis_type='test_recommendations',
            result={
                'structure_analysis': analysis_result,
                'recommendations': recommendations
            }
        )
        
        serializer = CodeAnalysisSerializer(analysis)
        return Response(serializer.data)

class CodeAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CodeAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CodeAnalysis.objects.filter(code_file__repository__project__owner=self.request.user)