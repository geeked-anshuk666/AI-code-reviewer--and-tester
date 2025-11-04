# AI Testing Platform IDE Extension

This is a Visual Studio Code extension that integrates with the AI Testing Platform to provide code review, test generation, and security scanning directly within your IDE.

## Features

1. **Code Review**: Automatically analyze your code for quality issues
2. **Test Generation**: Generate unit tests based on your code structure
3. **Security Scanning**: Identify security vulnerabilities in your code
4. **Automated Fixes**: Apply code improvements automatically
5. **Test Execution**: Run tests directly from your IDE

## Installation

1. Install the extension from the VS Code Marketplace
2. Connect to your AI Testing Platform instance
3. Start using the features directly in your editor

## Usage

### Code Review
- Right-click on any file and select "AI Code Review"
- View detailed analysis in the Problems panel

### Test Generation
- Right-click on any file and select "Generate Tests"
- Tests will be created in your configured test directory

### Security Scanning
- Right-click on any file and select "Security Scan"
- View vulnerabilities and suggested fixes

### Automated Fixes
- After a code review, select "Apply Fixes" to automatically improve your code

## Configuration

The extension requires connection to an AI Testing Platform server:

1. Open VS Code settings (Ctrl+,)
2. Search for "AI Testing Platform"
3. Set the server URL and API key

## Requirements

- Visual Studio Code 1.60.0 or higher
- Access to an AI Testing Platform server
- Python 3.7+ (for local analysis features)

## Extension Settings

This extension contributes the following settings:

* `aiTestingPlatform.serverUrl`: URL of the AI Testing Platform server
* `aiTestingPlatform.apiKey`: API key for authentication
* `aiTestingPlatform.autoReview`: Enable automatic code review on save
* `aiTestingPlatform.testFramework`: Preferred test framework (pytest, unittest, etc.)

## Known Issues

- Large files may take longer to analyze
- Some security fixes require manual review

## Release Notes

### 1.0.0

Initial release with core features:
- Code review capabilities
- Test generation
- Security scanning
- Automated fixes