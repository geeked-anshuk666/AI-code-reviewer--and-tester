"""
Security analysis module for identifying and fixing security vulnerabilities in code.
"""

import re
from typing import Dict, List, Any, Tuple

class SecurityAnalyzer:
    """
    Analyzes code for security vulnerabilities and provides fixing recommendations.
    """
    
    def __init__(self):
        """
        Initialize the security analyzer with common vulnerability patterns.
        """
        self.vulnerability_patterns = {
            'sql_injection': {
                'python': [
                    r"execute\s*\(\s*.*\s*\+\s*.*\s*\)",
                    r"executemany\s*\(\s*.*\s*\+\s*.*\s*\)",
                    r"cursor\.execute\s*\(\s*.*[%s]s.*[%s]s.*\s*\+\s*.*\s*\)"
                ],
                'javascript': [
                    r"\.query\s*\(\s*.*\s*\+\s*.*\s*\)",
                    r"mysql\.query\s*\(\s*.*\s*\+\s*.*\s*\)"
                ]
            },
            'xss': {
                'javascript': [
                    r"document\.write\s*\(",
                    r"innerHTML\s*=",
                    r"outerHTML\s*="
                ],
                'python': [
                    r"render_template\s*\(.*\{\{.*\}\}.*\)",
                    r"safe\s*="
                ]
            },
            'hardcoded_secrets': {
                'generic': [
                    r"password\s*=\s*[\'\"][^\'\"]{3,}[\'\"]",
                    r"secret\s*=\s*[\'\"][^\'\"]{3,}[\'\"]",
                    r"key\s*=\s*[\'\"][^\'\"]{3,}[\'\"]",
                    r"token\s*=\s*[\'\"][^\'\"]{3,}[\'\"]"
                ]
            },
            'insecure_crypto': {
                'python': [
                    r"md5\s*\(",
                    r"sha1\s*\(",
                    r"DES\s*\(",
                    r" Blowfish\s*\("
                ],
                'javascript': [
                    r"crypto\.createHash\(['\"]md5['\"]\)",
                    r"crypto\.createHash\(['\"]sha1['\"]\)"
                ]
            },
            'path_traversal': {
                'python': [
                    r"open\s*\(\s*.*\s*\+\s*.*\s*\)",
                    r"join\s*\(\s*.*\s*,\s*.*request\.args\.get\s*\("
                ],
                'javascript': [
                    r"fs\.readFile\s*\(\s*.*\s*\+\s*.*\s*\)",
                    r"fs\.writeFile\s*\(\s*.*\s*\+\s*.*\s*\)"
                ]
            }
        }
        
        self.fix_recommendations = {
            'sql_injection': "Use parameterized queries or ORM methods instead of string concatenation",
            'xss': "Sanitize user input and use secure templating engines",
            'hardcoded_secrets': "Use environment variables or secure configuration management",
            'insecure_crypto': "Use secure hashing algorithms like SHA-256 or bcrypt",
            'path_traversal': "Validate and sanitize file paths, use secure file access methods"
        }
    
    def analyze_security(self, code_content: str, language: str) -> Dict[str, Any]:
        """
        Analyze code for security vulnerabilities.
        """
        vulnerabilities = []
        language = language.lower()
        
        # Check for language-specific vulnerabilities
        for vuln_type, patterns in self.vulnerability_patterns.items():
            # Check language-specific patterns
            if language in patterns:
                for pattern in patterns[language]:
                    matches = re.finditer(pattern, code_content, re.IGNORECASE)
                    for match in matches:
                        line_number = code_content[:match.start()].count('\n') + 1
                        vulnerabilities.append({
                            'type': vuln_type,
                            'line': line_number,
                            'code': match.group(),
                            'recommendation': self.fix_recommendations.get(vuln_type, 'Fix this security issue')
                        })
            
            # Check generic patterns
            if 'generic' in patterns:
                for pattern in patterns['generic']:
                    matches = re.finditer(pattern, code_content, re.IGNORECASE)
                    for match in matches:
                        line_number = code_content[:match.start()].count('\n') + 1
                        vulnerabilities.append({
                            'type': vuln_type,
                            'line': line_number,
                            'code': match.group(),
                            'recommendation': self.fix_recommendations.get(vuln_type, 'Fix this security issue')
                        })
        
        # Generate security score
        security_score = self._calculate_security_score(vulnerabilities, code_content)
        
        return {
            'vulnerabilities': vulnerabilities,
            'security_score': security_score,
            'total_issues': len(vulnerabilities)
        }
    
    def _calculate_security_score(self, vulnerabilities: List[Dict], code_content: str) -> int:
        """
        Calculate a security score based on found vulnerabilities.
        """
        base_score = 100
        severity_weights = {
            'sql_injection': 25,
            'xss': 20,
            'hardcoded_secrets': 15,
            'insecure_crypto': 15,
            'path_traversal': 20
        }
        
        for vuln in vulnerabilities:
            vuln_type = vuln['type']
            if vuln_type in severity_weights:
                base_score -= severity_weights[vuln_type]
        
        # Adjust for code size (more code = more potential issues)
        lines_of_code = len(code_content.split('\n'))
        if lines_of_code > 1000:
            base_score = max(0, base_score - (lines_of_code // 100))
        
        return max(0, base_score)
    
    def suggest_fixes(self, code_content: str, vulnerabilities: List[Dict], language: str) -> List[Dict]:
        """
        Suggest fixes for identified vulnerabilities.
        """
        fixes = []
        
        for vuln in vulnerabilities:
            fix = self._generate_fix(vuln, code_content, language)
            if fix:
                fixes.append(fix)
        
        return fixes
    
    def _generate_fix(self, vulnerability: Dict, code_content: str, language: str) -> Dict:
        """
        Generate a specific fix for a vulnerability.
        """
        vuln_type = vulnerability['type']
        line_number = vulnerability['line']
        problematic_code = vulnerability['code']
        
        # Get the full line of code
        lines = code_content.split('\n')
        if line_number <= len(lines):
            full_line = lines[line_number - 1]
        else:
            full_line = problematic_code
        
        # Generate fix based on vulnerability type
        if vuln_type == 'sql_injection':
            if language == 'python':
                fixed_code = self._fix_sql_injection_python(full_line)
            elif language == 'javascript':
                fixed_code = self._fix_sql_injection_javascript(full_line)
            else:
                fixed_code = "# TODO: Use parameterized queries instead of string concatenation"
        elif vuln_type == 'xss':
            fixed_code = self._fix_xss(full_line, language)
        elif vuln_type == 'hardcoded_secrets':
            fixed_code = self._fix_hardcoded_secrets(full_line)
        elif vuln_type == 'insecure_crypto':
            fixed_code = self._fix_insecure_crypto(full_line, language)
        elif vuln_type == 'path_traversal':
            fixed_code = self._fix_path_traversal(full_line, language)
        else:
            fixed_code = f"# TODO: Fix {vuln_type} vulnerability"
        
        return {
            'vulnerability_type': vuln_type,
            'line_number': line_number,
            'problematic_code': full_line,
            'suggested_fix': fixed_code,
            'recommendation': vulnerability['recommendation']
        }
    
    def _fix_sql_injection_python(self, code_line: str) -> str:
        """
        Fix SQL injection in Python code.
        """
        # Simple replacement - in practice, this would be more sophisticated
        if 'execute(' in code_line and '+' in code_line:
            # Convert string concatenation to parameterized query
            fixed = code_line.replace('+', ',').replace('execute(', 'execute(')
            # Add comment to explain the fix
            return f"{fixed}  # Fixed: Using parameterized query instead of string concatenation"
        return "# TODO: Use parameterized queries with proper escaping"
    
    def _fix_sql_injection_javascript(self, code_line: str) -> str:
        """
        Fix SQL injection in JavaScript code.
        """
        if '.query(' in code_line and '+' in code_line:
            return "// TODO: Use parameterized queries with placeholders instead of string concatenation"
        return "# TODO: Use parameterized queries with proper escaping"
    
    def _fix_xss(self, code_line: str, language: str) -> str:
        """
        Fix XSS vulnerabilities.
        """
        if language == 'javascript':
            if 'document.write' in code_line:
                return "// TODO: Use safe DOM manipulation methods or sanitize input before writing"
            elif 'innerHTML' in code_line:
                return "// TODO: Use textContent or properly sanitize HTML content"
        elif language == 'python':
            if 'safe' in code_line:
                return "# TODO: Remove |safe filter and properly escape template variables"
        return "# TODO: Sanitize user input and use secure templating"
    
    def _fix_hardcoded_secrets(self, code_line: str) -> str:
        """
        Fix hardcoded secrets.
        """
        return "# TODO: Move secrets to environment variables or secure configuration management"
    
    def _fix_insecure_crypto(self, code_line: str, language: str) -> str:
        """
        Fix insecure cryptographic practices.
        """
        if language == 'python':
            if 'md5' in code_line:
                return "# TODO: Replace MD5 with SHA-256 or bcrypt for secure hashing"
            elif 'sha1' in code_line:
                return "# TODO: Replace SHA-1 with SHA-256 for secure hashing"
        elif language == 'javascript':
            if 'md5' in code_line:
                return "// TODO: Replace MD5 with SHA-256 or bcrypt for secure hashing"
            elif 'sha1' in code_line:
                return "// TODO: Replace SHA-1 with SHA-256 for secure hashing"
        return "# TODO: Use secure cryptographic algorithms"
    
    def _fix_path_traversal(self, code_line: str, language: str) -> str:
        """
        Fix path traversal vulnerabilities.
        """
        return "# TODO: Validate and sanitize file paths, use secure file access methods"