"""
Advanced AI-powered code analysis module.
This module uses NLP and code parsing libraries to analyze code structure and generate insights.
"""

import re
from typing import Dict, List, Any
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import tree_sitter
from tree_sitter import Language, Parser

class AIAnalyzer:
    """
    Advanced AI code analyzer that uses NLP and code parsing to understand code structure.
    """
    
    def __init__(self):
        """
        Initialize the AI analyzer with necessary models and parsers.
        """
        # Initialize code parser (simplified for now)
        self.parser = None
        try:
            # This would require building language libraries
            # For production, you would need to build these libraries
            pass
        except Exception as e:
            print(f"Warning: Could not initialize tree-sitter parser: {e}")
        
        # Initialize NLP sentiment analyzer for code comments
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest"
            )
        except Exception as e:
            print(f"Warning: Could not initialize sentiment analyzer: {e}")
            self.sentiment_analyzer = None
    
    def analyze_code_structure(self, code_content: str, language: str) -> Dict[str, Any]:
        """
        Analyze the structure of code using tree-sitter or regex patterns.
        """
        results = {
            'functions': [],
            'classes': [],
            'imports': [],
            'complexity': 0,
            'lines_of_code': len(code_content.split('\n')),
            'comments': []
        }
        
        # Language-specific analysis
        if language.lower() in ['python', 'py']:
            return self._analyze_python_code(code_content, results)
        elif language.lower() in ['javascript', 'js']:
            return self._analyze_javascript_code(code_content, results)
        elif language.lower() in ['java']:
            return self._analyze_java_code(code_content, results)
        else:
            # Generic analysis using regex
            return self._analyze_generic_code(code_content, results)
    
    def _analyze_python_code(self, code_content: str, results: Dict) -> Dict[str, Any]:
        """
        Analyze Python code structure.
        """
        lines = code_content.split('\n')
        
        # Find functions
        function_pattern = r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\):'
        for i, line in enumerate(lines):
            match = re.match(function_pattern, line)
            if match:
                results['functions'].append({
                    'name': match.group(1),
                    'parameters': match.group(2).split(',') if match.group(2) else [],
                    'line_number': i + 1
                })
        
        # Find classes
        class_pattern = r'^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(\([^)]*\))?:'
        for i, line in enumerate(lines):
            match = re.match(class_pattern, line)
            if match:
                results['classes'].append({
                    'name': match.group(1),
                    'parent_class': match.group(2)[1:-1] if match.group(2) else None,
                    'line_number': i + 1
                })
        
        # Find imports
        import_pattern = r'^\s*(import\s+[a-zA-Z_][a-zA-Z0-9_.]*|from\s+[a-zA-Z_][a-zA-Z0-9_.]*\s+import\s+.*)'
        for line in lines:
            match = re.match(import_pattern, line)
            if match:
                results['imports'].append(match.group(1))
        
        # Find comments
        comment_pattern = r'^\s*#(.*)'
        for i, line in enumerate(lines):
            match = re.match(comment_pattern, line)
            if match:
                results['comments'].append({
                    'text': match.group(1).strip(),
                    'line_number': i + 1
                })
        
        # Calculate complexity (simplified)
        results['complexity'] = len(results['functions']) + len(results['classes'])
        
        return results
    
    def _analyze_javascript_code(self, code_content: str, results: Dict) -> Dict[str, Any]:
        """
        Analyze JavaScript code structure.
        """
        lines = code_content.split('\n')
        
        # Find functions
        function_patterns = [
            r'^\s*function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)',
            r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*function\s*\(([^)]*)\)',
            r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*function\s*\(([^)]*)\)',
            r'^\s*const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(([^)]*)\)\s*=>',
            r'^\s*let\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(([^)]*)\)\s*=>',
            r'^\s*var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\(([^)]*)\)\s*=>'
        ]
        
        for i, line in enumerate(lines):
            for pattern in function_patterns:
                match = re.match(pattern, line)
                if match:
                    results['functions'].append({
                        'name': match.group(1),
                        'parameters': match.group(2).split(',') if match.group(2) else [],
                        'line_number': i + 1
                    })
                    break
        
        # Find classes
        class_pattern = r'^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(extends\s+[a-zA-Z_][a-zA-Z0-9_.]*)?'
        for i, line in enumerate(lines):
            match = re.match(class_pattern, line)
            if match:
                results['classes'].append({
                    'name': match.group(1),
                    'parent_class': match.group(2)[7:] if match.group(2) else None,
                    'line_number': i + 1
                })
        
        # Find imports
        import_patterns = [
            r'^\s*import\s+(?:.*\s+from\s+)?[\'"]([^\'"]+)[\'"]',
            r'^\s*const\s+.*\s*=\s*require\([\'"]([^\'"]+)[\'"]\)'
        ]
        for line in lines:
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    results['imports'].append(match.group(1))
        
        # Find comments
        comment_patterns = [
            r'^\s*//(.*)',
            r'/\*(.*?)\*/'
        ]
        for i, line in enumerate(lines):
            for pattern in comment_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    results['comments'].append({
                        'text': match.strip(),
                        'line_number': i + 1
                    })
        
        # Calculate complexity (simplified)
        results['complexity'] = len(results['functions']) + len(results['classes'])
        
        return results
    
    def _analyze_java_code(self, code_content: str, results: Dict) -> Dict[str, Any]:
        """
        Analyze Java code structure.
        """
        lines = code_content.split('\n')
        
        # Find methods
        method_pattern = r'^\s*(public|private|protected)?\s*(static)?\s*\w+\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{?'
        for i, line in enumerate(lines):
            match = re.match(method_pattern, line)
            if match and not any(keyword in line for keyword in ['if ', 'for ', 'while ']):
                results['functions'].append({
                    'name': match.group(3),
                    'parameters': match.group(4).split(',') if match.group(4) else [],
                    'line_number': i + 1
                })
        
        # Find classes
        class_pattern = r'^\s*(public\s+)?(class|interface)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        for i, line in enumerate(lines):
            match = re.match(class_pattern, line)
            if match:
                results['classes'].append({
                    'name': match.group(3),
                    'type': match.group(2),
                    'line_number': i + 1
                })
        
        # Find imports
        import_pattern = r'^\s*import\s+([a-zA-Z_][a-zA-Z0-9_.]*);'
        for line in lines:
            match = re.match(import_pattern, line)
            if match:
                results['imports'].append(match.group(1))
        
        # Find comments
        comment_patterns = [
            r'^\s*//(.*)',
            r'/\*(.*?)\*/'
        ]
        for i, line in enumerate(lines):
            for pattern in comment_patterns:
                matches = re.findall(pattern, line, re.DOTALL)
                for match in matches:
                    results['comments'].append({
                        'text': match.strip(),
                        'line_number': i + 1
                    })
        
        # Calculate complexity (simplified)
        results['complexity'] = len(results['functions']) + len(results['classes'])
        
        return results
    
    def _analyze_generic_code(self, code_content: str, results: Dict) -> Dict[str, Any]:
        """
        Generic code analysis using basic regex patterns.
        """
        lines = code_content.split('\n')
        
        # Generic function detection
        function_pattern = r'^\s*(function|def|public|private)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        for i, line in enumerate(lines):
            match = re.match(function_pattern, line)
            if match:
                results['functions'].append({
                    'name': match.group(2),
                    'line_number': i + 1
                })
        
        # Generic class detection
        class_pattern = r'^\s*(class|interface)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        for i, line in enumerate(lines):
            match = re.match(class_pattern, line)
            if match:
                results['classes'].append({
                    'name': match.group(2),
                    'type': match.group(1),
                    'line_number': i + 1
                })
        
        # Generic comment detection
        comment_pattern = r'^\s*[#*/]+(.*)'
        for i, line in enumerate(lines):
            match = re.match(comment_pattern, line)
            if match:
                results['comments'].append({
                    'text': match.group(1).strip(),
                    'line_number': i + 1
                })
        
        # Calculate complexity (simplified)
        results['complexity'] = len(results['functions']) + len(results['classes'])
        
        return results
    
    def analyze_code_quality(self, code_content: str, language: str) -> Dict[str, Any]:
        """
        Analyze code quality using various metrics.
        """
        analysis = self.analyze_code_structure(code_content, language)
        
        quality_metrics = {
            'structure_analysis': analysis,
            'quality_score': 0,
            'issues': [],
            'recommendations': []
        }
        
        # Calculate quality score based on various factors
        score = 100
        
        # Deduct points for high complexity
        if analysis['complexity'] > 20:
            score -= 20
            quality_metrics['issues'].append({
                'type': 'complexity',
                'message': f'High code complexity detected ({analysis["complexity"]} functions/classes)',
                'severity': 'warning'
            })
            quality_metrics['recommendations'].append({
                'type': 'refactor',
                'message': 'Consider refactoring to reduce complexity'
            })
        
        # Deduct points for lack of comments
        if len(analysis['comments']) < max(1, len(analysis['functions']) // 3):
            score -= 10
            quality_metrics['issues'].append({
                'type': 'documentation',
                'message': 'Insufficient comments for code documentation',
                'severity': 'warning'
            })
            quality_metrics['recommendations'].append({
                'type': 'documentation',
                'message': 'Add more comments to explain complex logic'
            })
        
        # Deduct points for long functions
        long_functions = [f for f in analysis['functions'] if 'parameters' in f and len(f['parameters']) > 5]
        if long_functions:
            score -= 15
            quality_metrics['issues'].append({
                'type': 'function_parameters',
                'message': f'{len(long_functions)} functions have too many parameters',
                'severity': 'warning'
            })
            quality_metrics['recommendations'].append({
                'type': 'refactor',
                'message': 'Consider reducing function parameters by using objects or refactoring'
            })
        
        quality_metrics['quality_score'] = max(0, score)
        
        return quality_metrics
    
    def generate_test_recommendations(self, code_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate test recommendations based on code analysis.
        """
        recommendations = []
        
        # Recommend unit tests for functions
        for func in code_analysis.get('functions', []):
            recommendations.append({
                'type': 'unit_test',
                'target': f"function {func['name']}",
                'priority': 'high',
                'description': f"Create unit tests for function '{func['name']}' at line {func['line_number']}"
            })
        
        # Recommend integration tests for classes
        for cls in code_analysis.get('classes', []):
            recommendations.append({
                'type': 'integration_test',
                'target': f"class {cls['name']}",
                'priority': 'medium',
                'description': f"Create integration tests for class '{cls['name']}' at line {cls['line_number']}"
            })
        
        # Recommend API tests if there are HTTP-related functions
        http_functions = [f for f in code_analysis.get('functions', []) 
                         if any(keyword in f['name'].lower() for keyword in ['api', 'http', 'request', 'fetch'])]
        for func in http_functions:
            recommendations.append({
                'type': 'api_test',
                'target': f"function {func['name']}",
                'priority': 'high',
                'description': f"Create API tests for function '{func['name']}' at line {func['line_number']}"
            })
        
        return recommendations