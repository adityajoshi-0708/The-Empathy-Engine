#!/usr/bin/env python3
"""
🎤 Empathy Engine – Setup Verification Script

This script verifies that all components are properly installed and configured.
Run this before starting the application to ensure everything is ready.
"""

import os
import sys
import importlib

def check_python_version():
    """Verify Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} — OK")
    return True

def check_package(package_name, import_name=None):
    """Check if a Python package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} — installed")
        return True
    except ImportError:
        print(f"❌ {package_name} — NOT INSTALLED")
        return False

def check_file_structure():
    """Verify all required files exist."""
    required_files = [
        'app/main.py',
        'app/emotion.py',
        'app/voice.py',
        'app/config.py',
        'app/templates/index.html',
        'app/static/css/style.css',
        'app/static/js/script.js',
        'requirements.txt',
        'README.md',
    ]
    
    print("\n📁 Checking file structure...")
    all_exist = True
    for filepath in required_files:
        if os.path.isfile(filepath):
            print(f"✅ {filepath}")
        else:
            print(f"❌ {filepath} — MISSING")
            all_exist = False
    
    return all_exist

def check_directories():
    """Verify required directories exist."""
    required_dirs = [
        'app/static/audio',
        'app/templates',
    ]
    
    print("\n📂 Checking directories...")
    all_exist = True
    for dirpath in required_dirs:
        if os.path.isdir(dirpath):
            print(f"✅ {dirpath}")
        else:
            print(f"❌ {dirpath} — MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks."""
    print("=" * 60)
    print("🎤 Empathy Engine – Setup Verification")
    print("=" * 60)
    
    # Check Python version
    print("\n🐍 Python Environment:")
    if not check_python_version():
        print("\n❌ Setup incomplete. Please install Python 3.8 or higher.")
        return False
    
    # Check packages
    print("\n📦 Required Packages:")
    packages = [
        ('FastAPI', 'fastapi'),
        ('Uvicorn', 'uvicorn'),
        ('pyttsx3', 'pyttsx3'),
        ('Transformers', 'transformers'),
        ('PyTorch', 'torch'),
        ('Pydantic', 'pydantic'),
    ]
    
    missing_packages = []
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            missing_packages.append(package_name)
    
    # Check file structure
    files_ok = check_file_structure()
    dirs_ok = check_directories()
    
    # Summary
    print("\n" + "=" * 60)
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
        return False
    
    if not files_ok or not dirs_ok:
        print("⚠️  Missing files or directories. Check above for details.")
        return False
    
    print("✅ All checks passed! Ready to start the application.")
    print("\n🚀 To start, run:")
    print("  uvicorn app.main:app --reload")
    print("\n📖 Then open: http://localhost:8000")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
