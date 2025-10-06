#!/usr/bin/env python3
"""
Architecture Intelligence - Startup Script
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import streamlit
        import pandas
        import numpy
        import plotly
        import networkx
        import matplotlib
        import seaborn
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_files():
    """Check if all required files exist"""
    print("📁 Checking required files...")
    
    required_files = [
        'app.py',
        'utils.py',
        'config.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def run_tests():
    """Run basic tests"""
    print("🧪 Running basic tests...")
    
    try:
        result = subprocess.run([sys.executable, 'test_app.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tests passed")
            return True
        else:
            print(f"❌ Tests failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def start_application():
    """Start the Streamlit application"""
    print("🚀 Starting Architecture Intelligence...")
    print("=" * 50)
    print("Application will be available at: http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main startup function"""
    print("🏗️ Architecture Intelligence - Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("❌ app.py not found. Please run this script from the project root directory.")
        return False
    
    # Run checks
    if not check_dependencies():
        return False
    
    if not check_files():
        return False
    
    # Ask if user wants to run tests
    run_tests_choice = input("\n🧪 Run tests before starting? (y/n): ").lower().strip()
    if run_tests_choice in ['y', 'yes']:
        if not run_tests():
            print("❌ Tests failed. Please fix issues before starting the application.")
            return False
    
    # Start the application
    start_application()
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

