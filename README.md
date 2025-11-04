# Open Source AI Testing Platform

An open-source alternative to TestSprite AI, an autonomous software testing platform that uses AI agents to automatically generate, execute, and analyze test cases.

## Overview

This platform integrates with IDEs and AI coding assistants to validate both frontend and backend systems without requiring manual test scripting. It provides autonomous test generation, auto-generated test code, cloud-based execution, IDE integration, and detailed reporting and analysis.

## Features

- **Autonomous Test Generation**: Automatically creates comprehensive test plans and cases based on product requirements and codebase analysis
- **Auto-generated Test Code**: Writes executable test scripts for both frontend (UI) and backend (API) systems
- **Cloud-Based Execution**: Runs tests in parallel on scalable cloud environments
- **IDE Integration**: Connects with popular code editors and AI coding assistants
- **Detailed Reporting and Analysis**: Generates structured reports with actionable insights
- **Security Analysis**: Identifies security vulnerabilities and suggests fixes
- **Code Quality Improvement**: Automatically improves code quality with AI-powered refactoring
- **Model Context Protocol (MCP) Support**: Integrates with AI coding assistants via MCP

## Technology Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL (SQLite for development)
- **Message Queue**: Redis
- **API Documentation**: DRF Spectacular (Swagger UI)
- **AI/ML Components**: Hugging Face Transformers, Tree-sitter
- **Containerization**: Docker
- **Deployment**: Docker Compose, Nginx
- **CI/CD**: GitHub Actions

## Quick Start

### Prerequisites
- Python 3.13+
- Docker and Docker Compose (recommended)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai_testing_and_code_reviewer_app
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Navigate to the Django project:
   ```bash
   cd ai_test_platform
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Using Docker (Recommended)

1. Build and start services:
   ```bash
   docker-compose up -d
   ```

2. Run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. Access the application:
   - Web interface: http://localhost:8000/
   - API Documentation: http://localhost:8000/api/schema/swagger-ui/
   - Admin interface: http://localhost:8000/admin/

## IDE Integration

The platform includes full IDE integration capabilities through the Model Context Protocol (MCP) and custom plugins:

### VS Code Extension

A fully-featured VS Code extension is available in the `ide_plugins/vscode_extension` directory with the following features:

1. **Code Review**: Automatically analyze your code for quality issues
2. **Test Generation**: Generate unit tests based on your code structure
3. **Security Scanning**: Identify security vulnerabilities in your code
4. **Automated Fixes**: Apply code improvements automatically
5. **Test Execution**: Run tests directly from your IDE

### Installation

1. Open VS Code
2. Navigate to the Extensions view (Ctrl+Shift+X)
3. Install the "AI Testing Platform" extension
4. Configure the extension with your server URL and API key

### API Endpoints for IDE Integration

- POST `/ide-integration/api/events/code_review/` - Perform code review
- POST `/ide-integration/api/events/generate_tests/` - Generate tests
- POST `/ide-integration/api/events/security_scan/` - Security scanning
- POST `/ide-integration/api/events/fix_code/` - Apply automated fixes

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- OpenAPI schema: http://localhost:8000/api/schema/

## Project Structure

```
ai_test_platform/
├── ai_test_platform/          # Project settings and configuration
├── test_management/           # Test case and project management
├── code_analysis/             # Code analysis components
├── test_execution/            # Test execution components
├── reporting/                 # Reporting and analytics
├── ide_integration/           # IDE integration components
├── manage.py                 # Django management script
└── requirements.txt          # Project dependencies

ide_plugins/
└── vscode_extension/         # VS Code extension implementation
```

## Development

### Running the Development Server

You can use the provided script to start the development environment:

```bash
python start_dev_server.py
```

### Running Tests

```bash
cd ai_test_platform
python manage.py test
```

## Deployment

For production deployment, use the production Docker Compose configuration:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

We welcome contributions from the community. Please read our contribution guidelines before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.