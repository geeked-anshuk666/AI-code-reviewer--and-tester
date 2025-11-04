#!/usr/bin/env python
"""
Script to start the development server for the AI Testing Platform.
"""

import os
import sys
import subprocess
import time

def main():
    print("AI Testing Platform - Development Server Setup")
    print("=" * 50)
    
    # Change to the project directory
    project_dir = os.path.join(os.path.dirname(__file__), 'ai_test_platform')
    if not os.path.exists(project_dir):
        print("Error: Project directory not found!")
        return 1
    
    # Check if docker-compose is available
    try:
        subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
        use_docker = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        use_docker = False
        print("Docker Compose not found, using local development setup")
    
    if use_docker:
        print("Starting services with Docker Compose...")
        try:
            # Start the services
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            print("Services started successfully!")
            
            # Wait a moment for services to initialize
            time.sleep(10)
            
            # Run migrations
            print("Running database migrations...")
            subprocess.run(["docker-compose", "exec", "web", "python", "manage.py", "migrate"], check=True)
            
            # Create superuser if it doesn't exist
            print("Creating superuser (if needed)...")
            subprocess.run([
                "docker-compose", "exec", "web", "python", "manage.py", "shell", "-c",
                "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None"
            ], check=True)
            
            print("\n" + "=" * 50)
            print("Development server is ready!")
            print("Access the application at: http://localhost:8000/")
            print("API Documentation: http://localhost:8000/api/schema/swagger-ui/")
            print("Admin interface: http://localhost:8000/admin/")
            print("Username: admin, Password: admin")
            print("\nIDE Integration API endpoints are available at:")
            print("  - http://localhost:8000/ide-integration/api/")
            print("=" * 50)
            
            # Follow the logs
            subprocess.run(["docker-compose", "logs", "-f"])
            
        except subprocess.CalledProcessError as e:
            print(f"Error starting services: {e}")
            return 1
        except KeyboardInterrupt:
            print("\nShutting down services...")
            subprocess.run(["docker-compose", "down"])
            print("Services stopped.")
    else:
        # Local development setup
        os.chdir(project_dir)
        
        try:
            print("Running database migrations...")
            subprocess.run(["python", "manage.py", "migrate"], check=True)
            
            print("Starting development server...")
            print("Access the application at: http://127.0.0.1:8000/")
            print("API Documentation: http://127.0.0.1:8000/api/schema/swagger-ui/")
            print("IDE Integration API: http://127.0.0.1:8000/ide-integration/api/")
            print("Press Ctrl+C to stop the server")
            print("-" * 50)
            
            subprocess.run(["python", "manage.py", "runserver"], check=True)
            
        except KeyboardInterrupt:
            print("\nServer stopped.")
        except Exception as e:
            print(f"Error starting server: {e}")
            return 1
    
    return 0

def setup_ide_plugin():
    """Set up the IDE plugin development environment."""
    print("Setting up IDE plugin development environment...")
    
    # Check if npm is installed
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("npm found, setting up VS Code extension...")
        
        # Navigate to the extension directory
        extension_dir = os.path.join(os.path.dirname(__file__), 'ide_plugins', 'vscode_extension')
        if os.path.exists(extension_dir):
            try:
                subprocess.run(["npm", "install"], check=True, cwd=extension_dir)
                print("VS Code extension dependencies installed!")
                print("To develop the extension:")
                print("  1. Open {} in VS Code".format(extension_dir))
                print("  2. Press F5 to launch the extension")
            except subprocess.CalledProcessError:
                print("Error installing extension dependencies")
        else:
            print("IDE plugin directory not found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("npm not found. Please install Node.js to develop IDE plugins.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "setup-ide":
        setup_ide_plugin()
    else:
        sys.exit(main())