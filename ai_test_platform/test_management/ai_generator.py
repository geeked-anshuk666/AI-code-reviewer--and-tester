"""
AI-powered test generation module.
This module provides advanced test generation capabilities based on AI code analysis.
"""

import json
from .models import TestCase

class AITestGenerator:
    """
    An advanced AI test generator that creates comprehensive test cases based on code analysis.
    """
    
    def generate_tests_from_analysis(self, code_analysis, project):
        """
        Generate test cases based on code analysis results.
        """
        test_cases = []
        
        # Extract analysis data
        analysis_type = code_analysis.analysis_type
        result = code_analysis.result
        
        if analysis_type == 'function_detection' or analysis_type == 'basic':
            # Generate unit tests for detected functions
            functions = result.get('functions', [])
            for func in functions:
                test_case = self._create_function_test(func, project, code_analysis)
                test_cases.append(test_case)
                
        elif analysis_type == 'class_detection':
            # Generate unit tests for detected classes
            classes = result.get('classes', [])
            for cls in classes:
                test_case = self._create_class_test(cls, project, code_analysis)
                test_cases.append(test_case)
                
        elif analysis_type == 'quality':
            # Generate tests based on quality analysis
            structure_analysis = result.get('structure_analysis', {})
            functions = structure_analysis.get('functions', [])
            classes = structure_analysis.get('classes', [])
            
            for func in functions:
                test_case = self._create_function_test(func, project, code_analysis)
                test_cases.append(test_case)
                
            for cls in classes:
                test_case = self._create_class_test(cls, project, code_analysis)
                test_cases.append(test_case)
                
        elif analysis_type == 'test_recommendations':
            # Generate tests based on AI recommendations
            recommendations = result.get('recommendations', [])
            for rec in recommendations:
                if rec['type'] == 'unit_test':
                    # Extract function name from description
                    target = rec['target']
                    func_name = target.replace('function ', '')
                    test_case = self._create_function_test(
                        {'name': func_name, 'line_number': 1}, 
                        project, 
                        code_analysis,
                        rec['description']
                    )
                    test_cases.append(test_case)
                elif rec['type'] == 'integration_test':
                    # Extract class name from description
                    target = rec['target']
                    class_name = target.replace('class ', '')
                    test_case = self._create_class_test(
                        {'name': class_name, 'line_number': 1}, 
                        project, 
                        code_analysis,
                        rec['description']
                    )
                    test_cases.append(test_case)
                    
        else:
            # Generate a basic test case for the file
            test_case = self._create_basic_test(code_analysis, project)
            test_cases.append(test_case)
            
        return test_cases
    
    def _create_function_test(self, func_data, project, code_analysis, description=None):
        """
        Create a test case for a detected function.
        """
        func_name = func_data['name']
        line_number = func_data.get('line_number', 1)
        
        title = f"Test for function {func_name}"
        if not description:
            description = f"Automated test case for function '{func_name}' detected at line {line_number}"
        
        # Generate more sophisticated test code based on function parameters
        parameters = func_data.get('parameters', [])
        test_code = self._generate_function_test_code(func_name, parameters)
        
        test_case = TestCase.objects.create(
            title=title,
            description=description,
            test_type='unit',
            status='draft',
            project=project,
            # created_by would be set in the view
            ai_generated=True,
            test_code=test_code
        )
        
        return test_case
    
    def _create_class_test(self, class_data, project, code_analysis, description=None):
        """
        Create a test case for a detected class.
        """
        class_name = class_data['name']
        line_number = class_data.get('line_number', 1)
        
        title = f"Test for class {class_name}"
        if not description:
            description = f"Automated test case for class '{class_name}' detected at line {line_number}"
        
        # Generate more sophisticated test code for classes
        test_code = self._generate_class_test_code(class_name)
        
        test_case = TestCase.objects.create(
            title=title,
            description=description,
            test_type='unit',
            status='draft',
            project=project,
            # created_by would be set in the view
            ai_generated=True,
            test_code=test_code
        )
        
        return test_case
    
    def _create_basic_test(self, code_analysis, project):
        """
        Create a basic test case for general code analysis.
        """
        file_path = code_analysis.code_file.file_path
        title = f"Test for {file_path}"
        description = f"Automated test case for file '{file_path}' based on code analysis"
        
        # Generate basic test code template
        test_code = f"""
# Test for file {file_path}
def test_{file_path.replace('/', '_').replace('.', '_')}():
    # TODO: Implement actual test logic
    # This test was automatically generated by AI
    assert True  # Placeholder assertion
"""
        
        test_case = TestCase.objects.create(
            title=title,
            description=description,
            test_type='unit',
            status='draft',
            project=project,
            # created_by would be set in the view
            ai_generated=True,
            test_code=test_code
        )
        
        return test_case
    
    def _generate_function_test_code(self, func_name, parameters):
        """
        Generate test code for a function based on its parameters.
        """
        # Create parameter placeholders
        param_assignments = []
        test_params = []
        
        for i, param in enumerate(parameters):
            param_name = param.strip() if param.strip() else f"param_{i}"
            # Remove any default values or type hints
            param_name = param_name.split(':')[0].split('=')[0].strip()
            if param_name and param_name not in ['self', 'cls']:
                param_assignments.append(f"{param_name} = None  # TODO: Replace with actual value")
                test_params.append(param_name)
        
        # Create the test function
        params_str = ", ".join(test_params) if test_params else ""
        
        test_code = f"""
# Test for function {func_name}
def test_{func_name}():
    # Setup
    {chr(10) + '    '.join(param_assignments) if param_assignments else '# No parameters to setup'}
    
    # Execute
    try:
        result = {func_name}({params_str})
        # TODO: Add assertions based on expected behavior
        assert result is not None  # Placeholder assertion
    except Exception as e:
        # TODO: Handle expected exceptions
        raise e
"""
        return test_code
    
    def _generate_class_test_code(self, class_name):
        """
        Generate test code for a class.
        """
        test_code = f"""
# Test for class {class_name}
class Test{class_name}:
    def setUp(self):
        # TODO: Initialize test fixtures
        self.instance = {class_name}()
    
    def test_{class_name}_initialization(self):
        # Test that the class can be instantiated
        assert self.instance is not None
    
    def test_{class_name}_methods(self):
        # TODO: Add tests for class methods
        # Example:
        # result = self.instance.some_method()
        # assert result == expected_value
        pass
"""
        return test_code