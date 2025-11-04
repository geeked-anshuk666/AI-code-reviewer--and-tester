from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import IDEPlugin, IDEConnection, IDEEvent
from .serializers import IDEPluginSerializer, IDEConnectionSerializer, IDEEventSerializer
from code_analysis.models import CodeFile, CodeAnalysis
from code_analysis.ai_analyzer import AIAnalyzer
from code_analysis.security_analyzer import SecurityAnalyzer
from code_analysis.code_fixer import CodeFixer
from test_management.models import TestCase
from test_management.ai_generator import AITestGenerator
from test_execution.models import TestExecution

class IDEPluginViewSet(viewsets.ModelViewSet):
    serializer_class = IDEPluginSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return IDEPlugin.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IDEConnectionViewSet(viewsets.ModelViewSet):
    serializer_class = IDEConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return IDEConnection.objects.filter(plugin__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def connect(self, request, pk=None):
        """
        Establish a connection from an IDE plugin.
        """
        connection = get_object_or_404(IDEConnection, pk=pk, plugin__user=self.request.user)
        connection.is_connected = True
        connection.connected_at = timezone.now()
        connection.save()
        
        # Log the connection event
        IDEEvent.objects.create(
            plugin=connection.plugin,
            event_type='connection',
            details={'action': 'connected'}
        )
        
        return Response({'status': 'connected'})
    
    @action(detail=True, methods=['post'])
    def disconnect(self, request, pk=None):
        """
        Disconnect an IDE plugin.
        """
        connection = get_object_or_404(IDEConnection, pk=pk, plugin__user=self.request.user)
        connection.is_connected = False
        connection.disconnected_at = timezone.now()
        connection.save()
        
        # Log the disconnection event
        IDEEvent.objects.create(
            plugin=connection.plugin,
            event_type='connection',
            details={'action': 'disconnected'}
        )
        
        return Response({'status': 'disconnected'})

class IDEEventViewSet(viewsets.ModelViewSet):
    serializer_class = IDEEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return IDEEvent.objects.filter(plugin__user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def code_review(self, request):
        """
        Perform a code review for code sent from an IDE.
        """
        code_content = request.data.get('code_content', '')
        file_path = request.data.get('file_path', '')
        language = request.data.get('language', 'python')
        
        if not code_content:
            return Response({'error': 'code_content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create IDE plugin
        plugin_id = request.data.get('plugin_id')
        if not plugin_id:
            return Response({'error': 'plugin_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        plugin = get_object_or_404(IDEPlugin, id=plugin_id, user=self.request.user)
        
        # Create a temporary CodeFile for analysis
        code_file = CodeFile.objects.create(
            repository=None,  # This is a temporary file not tied to a repository
            file_path=file_path,
            content=code_content,
            language=language
        )
        
        # Perform AI analysis
        ai_analyzer = AIAnalyzer()
        analysis_result = ai_analyzer.analyze_code_quality(code_content, language)
        
        # Perform security analysis
        security_analyzer = SecurityAnalyzer()
        security_result = security_analyzer.analyze_security(code_content, language)
        
        # Combine results
        combined_result = {
            'code_analysis': analysis_result,
            'security_analysis': security_result
        }
        
        # Create analysis record
        code_analysis = CodeAnalysis.objects.create(
            code_file=code_file,
            analysis_type='ide_code_review',
            result=combined_result
        )
        
        # Log the event
        IDEEvent.objects.create(
            plugin=plugin,
            event_type='code_review',
            file_path=file_path,
            details={'analysis_id': code_analysis.id}
        )
        
        return Response({
            'analysis_id': code_analysis.id,
            'results': combined_result
        })
    
    @action(detail=False, methods=['post'])
    def generate_tests(self, request):
        """
        Generate tests for code sent from an IDE.
        """
        code_content = request.data.get('code_content', '')
        file_path = request.data.get('file_path', '')
        language = request.data.get('language', 'python')
        project_id = request.data.get('project_id')
        
        if not code_content:
            return Response({'error': 'code_content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not project_id:
            return Response({'error': 'project_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create IDE plugin
        plugin_id = request.data.get('plugin_id')
        if not plugin_id:
            return Response({'error': 'plugin_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        plugin = get_object_or_404(IDEPlugin, id=plugin_id, user=self.request.user)
        
        # Create a temporary CodeFile for analysis
        code_file = CodeFile.objects.create(
            repository=None,
            file_path=file_path,
            content=code_content,
            language=language
        )
        
        # Perform AI analysis to understand the code structure
        ai_analyzer = AIAnalyzer()
        analysis_result = ai_analyzer.analyze_code_structure(code_content, language)
        
        # Create analysis record
        code_analysis = CodeAnalysis.objects.create(
            code_file=code_file,
            analysis_type='ide_test_generation',
            result=analysis_result
        )
        
        # Generate test cases using AI
        from test_management.models import Project
        project = get_object_or_404(Project, id=project_id, owner=self.request.user)
        
        generator = AITestGenerator()
        test_cases = generator.generate_tests_from_analysis(code_analysis, project)
        
        # Set the created_by for each test case
        for test_case in test_cases:
            test_case.created_by = self.request.user
            test_case.save()
        
        # Log the event
        IDEEvent.objects.create(
            plugin=plugin,
            event_type='test_generation',
            file_path=file_path,
            details={
                'analysis_id': code_analysis.id,
                'test_cases_generated': len(test_cases)
            }
        )
        
        return Response({
            'analysis_id': code_analysis.id,
            'test_cases_generated': len(test_cases),
            'test_case_ids': [tc.id for tc in test_cases]
        })
    
    @action(detail=False, methods=['post'])
    def fix_code(self, request):
        """
        Apply automated fixes to code sent from an IDE.
        """
        code_content = request.data.get('code_content', '')
        file_path = request.data.get('file_path', '')
        language = request.data.get('language', 'python')
        analysis_id = request.data.get('analysis_id')
        
        if not code_content:
            return Response({'error': 'code_content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create IDE plugin
        plugin_id = request.data.get('plugin_id')
        if not plugin_id:
            return Response({'error': 'plugin_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        plugin = get_object_or_404(IDEPlugin, id=plugin_id, user=self.request.user)
        
        # Get the previous analysis if available
        analysis_results = {}
        if analysis_id:
            try:
                code_analysis = CodeAnalysis.objects.get(id=analysis_id)
                analysis_results = code_analysis.result
            except CodeAnalysis.DoesNotExist:
                pass
        
        # Apply automated fixes
        code_fixer = CodeFixer()
        refactored_result = code_fixer.generate_refactored_code(
            code_content, language, analysis_results
        )
        
        # Log the event
        IDEEvent.objects.create(
            plugin=plugin,
            event_type='code_fix',
            file_path=file_path,
            details={
                'fixes_applied': len(refactored_result['applied_fixes']),
                'improvement_percentage': refactored_result['improvement_stats']['improvement_percentage']
            }
        )
        
        return Response(refactored_result)
    
    @action(detail=False, methods=['post'])
    def security_scan(self, request):
        """
        Perform a security scan on code sent from an IDE.
        """
        code_content = request.data.get('code_content', '')
        file_path = request.data.get('file_path', '')
        language = request.data.get('language', 'python')
        
        if not code_content:
            return Response({'error': 'code_content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create IDE plugin
        plugin_id = request.data.get('plugin_id')
        if not plugin_id:
            return Response({'error': 'plugin_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        plugin = get_object_or_404(IDEPlugin, id=plugin_id, user=self.request.user)
        
        # Perform security analysis
        security_analyzer = SecurityAnalyzer()
        security_result = security_analyzer.analyze_security(code_content, language)
        
        # Generate fixes for identified vulnerabilities
        fixes = security_analyzer.suggest_fixes(code_content, security_result['vulnerabilities'], language)
        security_result['fixes'] = fixes
        
        # Log the event
        IDEEvent.objects.create(
            plugin=plugin,
            event_type='security_scan',
            file_path=file_path,
            details={
                'vulnerabilities_found': security_result['total_issues'],
                'security_score': security_result['security_score']
            }
        )
        
        return Response(security_result)