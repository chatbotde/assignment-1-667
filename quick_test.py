#!/usr/bin/env python3
"""
Quick Test Script - Fast verification of core functionality
===========================================================

This script performs essential checks to verify your helicopter simulator
is ready to run. Use this for quick verification before running full tests.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        raise RuntimeError(f"Python 3.7+ required, found {version.major}.{version.minor}")
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_dependencies():
    """Check required packages"""
    required = ['numpy', 'matplotlib', 'pandas']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} - Available")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} - Missing")
        except Exception as e:
            print(f"❌ {package} - Error: {e}")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    return True

def check_core_files():
    """Check essential files exist"""
    essential_files = [
        'flight_sim_part1/main.py',
        'flight_sim_part1/user_inputs.py',
        'gui/helicopter_gui_main.py',
        'individual_design/helicopter_designer.py'
    ]
    
    missing = []
    for file_path in essential_files:
        if not Path(file_path).exists():
            missing.append(file_path)
            print(f"❌ {file_path} - Missing")
        else:
            print(f"✓ {file_path} - Found")
    
    if missing:
        print(f"\nMissing essential files: {len(missing)}")
        return False
    
    return True

def test_basic_import():
    """Test basic imports work"""
    try:
        sys.path.append('flight_sim_part1')
        from user_inputs import get_user_inputs
        inputs = get_user_inputs()
        print("✓ Core flight sim imports - Working")
        return True
    except Exception as e:
        print(f"❌ Core imports failed: {e}")
        return False

def main():
    """Run quick verification"""
    print("HELICOPTER SIMULATOR - QUICK VERIFICATION")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Essential Files", check_core_files),
        ("Basic Imports", test_basic_import)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 20)
        try:
            result = check_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {name} failed: {e}")
    
    print(f"\n{'='*50}")
    print(f"QUICK TEST RESULTS: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Ready to run! All basic checks passed.")
        print("\nNext steps:")
        print("1. Run full tests: python test_plan.py")
        print("2. Try core simulation: python flight_sim_part1/main.py")
        return True
    else:
        print("⚠️  Some checks failed. Fix issues above before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)