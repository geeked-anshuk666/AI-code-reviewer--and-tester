"""
Setup script for the VS Code extension development environment.
"""

import os
import subprocess
import sys

def setup_extension_environment():
    """Set up the development environment for the VS Code extension."""
    print("Setting up VS Code extension development environment...")
    
    # Check if npm is installed
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: npm is not installed. Please install Node.js and npm first.")
        return False
    
    # Install dependencies
    print("Installing Node.js dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True, cwd="ide_plugins/vscode_extension")
        print("Node.js dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to install Node.js dependencies.")
        return False
    
    # Compile TypeScript
    print("Compiling TypeScript...")
    try:
        subprocess.run(["npm", "run", "compile"], check=True, cwd="ide_plugins/vscode_extension")
        print("TypeScript compiled successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to compile TypeScript.")
        return False
    
    print("VS Code extension development environment is ready!")
    print("To run the extension in development mode:")
    print("  1. Open the ide_plugins/vscode_extension folder in VS Code")
    print("  2. Press F5 to launch the extension in a new Extension Development Host window")
    
    return True

if __name__ == "__main__":
    setup_extension_environment()