"""
Automated code fixer module that applies improvements to code based on analysis.
"""

import re
from typing import Dict, List, Any, Tuple, Callable, Union

class CodeFixer:
    """
    Automatically applies code improvements and fixes based on analysis results.
    """
    
    def __init__(self):
        """
        Initialize the code fixer with common improvement patterns.
        """
        self.improvement_patterns = {
            'code_style': {
                'python': [
                    # Convert old string formatting to f-strings
                    (r"\"%s\" % \(([^)]+)\)", r"f\"{\\1}\""),
                    (r"\"%s\" % ([^,]+)", r"f\"{\\1}\""),
                ]
            },
            'performance': {
                'python': [
                    # Convert list comprehensions in loops to generator expressions where appropriate
                    (r"for [^:]+ in \[.*\]:", self._optimize_list_comprehension),
                ]
            },
            'best_practices': {
                'python': [
                    # Add __name__ == '__main__' guard
                    (r"def main\(\):", self._add_main_guard),
                ],
                'javascript': [
                    # Add 'use strict' directive
                    (r"function", self._add_use_strict),
                ]
            }
        }
    
    def apply_fixes(self, code_content: str, language: str, analysis_results: Dict) -> Tuple[str, List[Dict]]:
        """
        Apply automated fixes to the code.
        """
        fixed_code: str = code_content
        applied_fixes: List[Dict] = []
        
        # Apply security fixes first
        if 'security_analysis' in analysis_results:
            security_fixes = analysis_results['security_analysis'].get('fixes', [])
            for fix in security_fixes:
                fixed_code, success = self._apply_security_fix(fixed_code, fix)
                if success:
                    applied_fixes.append({
                        'type': 'security_fix',
                        'description': fix['recommendation'],
                        'line': fix['line_number']
                    })
        
        # Apply general improvements
        language = language.lower()
        for category, patterns in self.improvement_patterns.items():
            if language in patterns:
                for pattern, replacement in patterns[language]:
                    if callable(replacement):
                        result = replacement(fixed_code)
                        if isinstance(result, str):
                            fixed_code = result
                    else:
                        fixed_code = re.sub(pattern, str(replacement), fixed_code)
                    
                    # Track applied improvements
                    if re.search(pattern, code_content):
                        applied_fixes.append({
                            'type': category,
                            'description': f'Applied {category} improvement',
                            'pattern': pattern
                        })
        
        return fixed_code, applied_fixes
    
    def _apply_security_fix(self, code_content: str, fix: Dict) -> Tuple[str, bool]:
        """
        Apply a specific security fix to the code.
        """
        line_number = fix['line_number']
        suggested_fix = fix['suggested_fix']
        
        lines = code_content.split('\n')
        if line_number <= len(lines):
            # Replace the problematic line with the suggested fix
            lines[line_number - 1] = str(suggested_fix)
            return '\n'.join(lines), True
        
        return code_content, False
    
    def _optimize_list_comprehension(self, code_content: str) -> str:
        """
        Optimize list comprehensions where appropriate.
        """
        # This is a placeholder - in practice, this would analyze and optimize
        return code_content
    
    def _add_main_guard(self, code_content: str) -> str:
        """
        Add __name__ == '__main__' guard to Python code.
        """
        if 'def main():' in code_content and '__name__ == "__main__"' not in code_content:
            return code_content + '\n\nif __name__ == "__main__":\n    main()\n'
        return code_content
    
    def _add_use_strict(self, code_content: str) -> str:
        """
        Add 'use strict' directive to JavaScript code.
        """
        if '"use strict";' not in code_content and "'use strict';" not in code_content:
            return '"use strict";\n' + code_content
        return code_content
    
    def generate_refactored_code(self, code_content: str, language: str, 
                               analysis_results: Dict) -> Dict[str, Any]:
        """
        Generate a fully refactored version of the code with all improvements.
        """
        # Apply fixes
        fixed_code, applied_fixes = self.apply_fixes(code_content, language, analysis_results)
        
        # Calculate improvement metrics
        original_lines = len(code_content.split('\n'))
        fixed_lines = len(fixed_code.split('\n'))
        
        return {
            'refactored_code': fixed_code,
            'applied_fixes': applied_fixes,
            'improvement_stats': {
                'lines_original': original_lines,
                'lines_refactored': fixed_lines,
                'fixes_applied': len(applied_fixes),
                'improvement_percentage': min(100, len(applied_fixes) * 10)  # Simplified calculation
            }
        }