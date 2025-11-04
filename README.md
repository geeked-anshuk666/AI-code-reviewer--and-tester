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

## Technology Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL
- **Message Queue**: Redis
- **API Documentation**: DRF Spectacular (Swagger UI)
- **Frontend**: React/Vue.js (to be implemented)
- **AI/ML Components**: Hugging Face Transformers library (to be implemented)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
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

4. Navigate to the project directory:
   ```bash
   cd ai_test_platform
   ```

5. Create a PostgreSQL database and update the settings in `ai_test_platform/settings.py`

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- OpenAPI schema: http://localhost:8000/api/schema/

## Project Structure

```
ai_test_platform/
├── ai_test_platform/          # Project settings and configuration
├── test_management/           # Test case and project management
├── code_analysis/             # Code analysis components (planned)
├── test_execution/            # Test execution components (planned)
├── reporting/                 # Reporting and analytics (planned)
├── manage.py                 # Django management script
└── requirements.txt          # Project dependencies
```

## Development Roadmap

Refer to [OPEN_SOURCE_TESTING_PLATFORM_PLAN.md](OPEN_SOURCE_TESTING_PLATFORM_PLAN.md) for the complete 12-month development roadmap.

## Contributing

We welcome contributions from the community. Please read our contribution guidelines before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.