from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import TestExecution, TestResult
from .serializers import TestExecutionSerializer, TestResultSerializer, TestExecutionCreateSerializer
from test_management.models import TestCase, Project
import tempfile
import os
import subprocess
import sys

class TestExecutionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TestExecutionCreateSerializer
        return TestExecutionSerializer
    
    def get_queryset(self):
        return TestExecution.objects.filter(project__owner=self.request.user)
    
    def perform_create(self, serializer):
        # Check if the project belongs to the current user
        project = get_object_or_404(Project, id=self.request.data.get('project'), owner=self.request.user)
        execution = serializer.save()
        
        # If no test cases were provided, add all test cases from the project
        if not execution.test_cases.exists():
            project_test_cases = TestCase.objects.filter(project=project)
            execution.test_cases.set(project_test_cases)
    
    @action(detail=True, methods=['post'])
    def start_execution(self, request, pk=None):
        """
        Start executing the tests in this test execution.
        """
        execution = get_object_or_404(TestExecution, pk=pk, project__owner=self.request.user)
        
        if execution.status != 'pending':
            return Response({'error': 'Execution is not in pending state'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update execution status
        execution.status = 'running'
        execution.started_at = timezone.now()
        execution.save()
        
        # Execute tests
        results = self._execute_tests(execution)
        
        # Update execution with results
        execution.status = 'completed'
        execution.completed_at = timezone.now()
        execution.duration = (execution.completed_at - execution.started_at).total_seconds()
        execution.results = results
        execution.save()
        
        serializer = TestExecutionSerializer(execution)
        return Response(serializer.data)
    
    def _execute_tests(self, execution):
        """
        Execute tests and return results.
        """
        results = {
            'total_tests': execution.test_cases.count(),
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'errors': 0,
            'test_details': []
        }
        
        # Create individual test results
        for test_case in execution.test_cases.all():
            # Execute the test code
            test_result_data = self._run_test_code(test_case)
            
            TestResult.objects.create(
                execution=execution,
                test_case=test_case,
                result=test_result_data['status'],
                output=test_result_data['output'],
                error_message=test_result_data['error_message'],
                duration=test_result_data['duration']
            )
            
            # Update counts
            if test_result_data['status'] == 'passed':
                results['passed'] += 1
            elif test_result_data['status'] == 'failed':
                results['failed'] += 1
            elif test_result_data['status'] == 'skipped':
                results['skipped'] += 1
            elif test_result_data['status'] == 'error':
                results['errors'] += 1
            
            # Add test details
            results['test_details'].append({
                'test_case': test_case.title,
                'status': test_result_data['status'],
                'duration': test_result_data['duration'],
                'error_message': test_result_data['error_message']
            })
        
        return results
    
    def _run_test_code(self, test_case):
        """
        Run the test code and return the result.
        """
        import time
        start_time = time.time()
        
        # Create a temporary file with the test code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Add necessary imports
            test_code = f"""
import sys
import traceback

# Add the current directory to the path so imports work
sys.path.insert(0, '.')

# Test code:
{test_case.test_code}

if __name__ == "__main__":
    try:
        # Run all test functions
        import inspect
        import types
        
        # Get all functions in the module
        current_module = sys.modules[__name__]
        test_functions = [obj for name, obj in inspect.getmembers(current_module) 
                         if (inspect.isfunction(obj) and name.startswith('test_')) or 
                            (inspect.isclass(obj) and name.startswith('Test'))]
        
        # Run test functions
        for test_func in test_functions:
            if inspect.isfunction(test_func):
                try:
                    test_func()
                    print(f"PASS: {{test_func.__name__}}")
                except Exception as e:
                    print(f"FAIL: {{test_func.__name__}} - {{str(e)}}")
                    traceback.print_exc()
            elif inspect.isclass(test_func):
                # For test classes, try to instantiate and run test methods
                try:
                    instance = test_func()
                    if hasattr(instance, 'setUp'):
                        instance.setUp()
                    
                    # Get test methods
                    test_methods = [method for method in dir(instance) 
                                   if method.startswith('test_')]
                    
                    for method_name in test_methods:
                        try:
                            method = getattr(instance, method_name)
                            method()
                            print(f"PASS: {{test_func.__name__}}.{{method_name}}")
                        except Exception as e:
                            print(f"FAIL: {{test_func.__name__}}.{{method_name}} - {{str(e)}}")
                            traceback.print_exc()
                except Exception as e:
                    print(f"ERROR: {{test_func.__name__}} - {{str(e)}}")
                    traceback.print_exc()
    except Exception as e:
        print(f"ERROR: {{str(e)}}")
        traceback.print_exc()
"""
            f.write(test_code)
            temp_file_path = f.name
        
        try:
            # Run the test code in a subprocess
            result = subprocess.run(
                [sys.executable, temp_file_path],
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            duration = time.time() - start_time
            
            # Parse the output to determine test results
            output = result.stdout
            error_output = result.stderr
            
            # Determine test status based on output
            if "FAIL:" in output or "ERROR:" in output or result.returncode != 0:
                status = "failed" if "FAIL:" in output else "error"
                error_message = error_output or "Test failed"
            elif "PASS:" in output:
                status = "passed"
                error_message = ""
            else:
                status = "skipped"
                error_message = "No tests found or executed"
            
            return {
                'status': status,
                'output': output,
                'error_message': error_message,
                'duration': duration
            }
        
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                'status': 'error',
                'output': '',
                'error_message': 'Test execution timed out',
                'duration': duration
            }
        
        except Exception as e:
            duration = time.time() - start_time
            return {
                'status': 'error',
                'output': '',
                'error_message': str(e),
                'duration': duration
            }
        
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass

class TestResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TestResult.objects.filter(execution__project__owner=self.request.user)