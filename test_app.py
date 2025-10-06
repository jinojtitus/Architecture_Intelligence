#!/usr/bin/env python3
"""
Test script for Architecture Intelligence application
"""

import sys
import importlib.util

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'networkx',
        'matplotlib',
        'seaborn',
        'streamlit_option_menu'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing dependencies with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def test_utils():
    """Test utility modules"""
    print("\nTesting utility modules...")
    
    try:
        from utils import TechnologyDetector, DataFlowAnalyzer, ArchitectureGenerator, PatternManager
        
        # Test TechnologyDetector
        detector = TechnologyDetector()
        print("  ✅ TechnologyDetector initialized")
        
        # Test DataFlowAnalyzer
        analyzer = DataFlowAnalyzer()
        print("  ✅ DataFlowAnalyzer initialized")
        
        # Test ArchitectureGenerator
        generator = ArchitectureGenerator()
        print("  ✅ ArchitectureGenerator initialized")
        
        # Test PatternManager
        manager = PatternManager()
        print("  ✅ PatternManager initialized")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Utils test failed: {e}")
        return False

def test_config():
    """Test configuration module"""
    print("\nTesting configuration...")
    
    try:
        import config
        
        # Test key configuration values
        assert hasattr(config, 'APP_NAME')
        assert hasattr(config, 'THEME_CONFIG')
        assert hasattr(config, 'TECH_DETECTION')
        assert hasattr(config, 'PATTERNS')
        
        print("  ✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"  ❌ Config test failed: {e}")
        return False

def test_demo():
    """Test demo functionality"""
    print("\nTesting demo functionality...")
    
    try:
        from demo import demo_technology_detection, demo_data_flow_analysis
        
        # Test technology detection
        technologies = demo_technology_detection()
        # Note: technologies might be empty if no matches found, which is valid
        print("  ✅ Technology detection demo works")
        
        # Test data flow analysis
        flow_analysis = demo_data_flow_analysis()
        assert 'total_flows' in flow_analysis
        print("  ✅ Data flow analysis demo works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Demo test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Architecture Intelligence - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_utils,
        test_demo
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to run.")
        print("\nTo start the application:")
        print("  streamlit run app.py")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
