#!/usr/bin/env python3
"""
Master test runner - runs all tests in sequence
"""

import subprocess
import sys
import os

def run_test_file(test_file):
    """Run a test file and return success status"""
    print(f"\n{'='*50}")
    print(f"Running {test_file}")
    print('='*50)
    
    try:
        # Get the full path to the test file
        test_dir = os.path.dirname(__file__)
        test_path = os.path.join(test_dir, test_file)
        
        result = subprocess.run([sys.executable, test_path], 
                              capture_output=False, 
                              text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False

def main():
    """Run all test files"""
    print("Flight Simulation Test Suite")
    print("="*50)
    
    test_files = [
        "test_components.py",
        "test_main.py", 
        "test_mission_integration.py",
        "test_complete_validation.py",
        "test_mission_controller.py"
    ]
    
    results = {}
    
    for test_file in test_files:
        test_path = os.path.join(os.path.dirname(__file__), test_file)
        if os.path.exists(test_path):
            results[test_file] = run_test_file(test_file)
        else:
            print(f"Warning: {test_file} not found at {test_path}")
            results[test_file] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_file, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_file}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} test files passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your flight simulation is ready!")
        print("\nNext steps:")
        print("- Integrate with mission planner")
        print("- Add more test scenarios")
        print("- Performance optimization")
    else:
        print(f"\n⚠️  {total - passed} test file(s) failed")
        print("Check the output above for details")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)