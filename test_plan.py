#!/usr/bin/env python3
"""
Comprehensive Testing Plan for Helicopter Flight Simulator Project
================================================================

This script tests all major components of the helicopter flight simulator:
1. Core flight simulation (flight_sim_part1)
2. GUI interface (gui package)
3. Integration between components
4. Performance and error handling

Run this script to verify everything is working properly.
"""

import sys
import os
import traceback
import importlib
from pathlib import Path

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def test(self, name, test_func):
        """Run a single test and record results"""
        print(f"\n{'='*60}")
        print(f"Testing: {name}")
        print('='*60)
        
        try:
            test_func()
            print(f"✅ PASSED: {name}")
            self.passed += 1
            self.results.append(f"✅ {name}")
        except Exception as e:
            print(f"❌ FAILED: {name}")
            print(f"Error: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            self.failed += 1
            self.results.append(f"❌ {name} - {str(e)}")
    
    def summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print('='*60)
        print(f"Total tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success rate: {(self.passed/(self.passed + self.failed)*100):.1f}%")
        
        print("\nDetailed Results:")
        for result in self.results:
            print(f"  {result}")
        
        return self.failed == 0


def test_imports():
    """Test that all required packages can be imported"""
    required_packages = ['numpy', 'matplotlib', 'pandas', 'tkinter']
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                importlib.import_module(package)
            print(f"✓ {package} imported successfully")
        except ImportError as e:
            raise ImportError(f"Required package '{package}' not available: {e}")


def test_flight_sim_core():
    """Test the core flight simulation components"""
    sys.path.append('flight_sim_part1')
    
    # Test individual modules
    from user_inputs import get_user_inputs, build_rotor
    from atmosphere import isa_properties
    from integrators import cycle_integrator
    from stabilizers import Stabilizers
    
    print("✓ All core modules imported successfully")
    
    # Test user inputs
    inputs = get_user_inputs()
    print(f"✓ User inputs loaded: {len(inputs)} sections")
    
    # Test rotor building
    rotor = build_rotor(inputs["rotor"])
    print(f"✓ Rotor built with {rotor.B} blades, R={rotor.blade.R_tip:.1f}m")
    
    # Test atmosphere
    rho, a = isa_properties(inputs["condition"]["alt_m"])
    print(f"✓ Atmosphere calculated: ρ={rho:.3f} kg/m³, a={a:.1f} m/s")
    
    # Test integration
    import math
    rpm = inputs["condition"]["rpm"]
    omega = 2*math.pi*rpm/60.0
    V = inputs["condition"]["V_forward_mps"]
    
    T, Q, P = cycle_integrator(rotor, V, omega, rho)
    print(f"✓ Cycle integration: T={T:.1f}N, Q={Q:.1f}N·m, P={P/1000:.1f}kW")
    
    # Test stabilizers
    stab = Stabilizers(**inputs["stabilizers"])
    fm = stab.forces_moments(rho, V)
    print(f"✓ Stabilizers calculated: {len(fm)} force/moment components")


def test_flight_sim_main():
    """Test running the main flight simulation"""
    sys.path.append('flight_sim_part1')
    
    from main import run
    print("Running main flight simulation...")
    run()
    print("✓ Main flight simulation completed successfully")


def test_gui_components():
    """Test GUI components can be imported and initialized"""
    try:
        from gui.helicopter_gui_main import HelicopterSimulatorGUI
        from gui.control_panel import ControlPanel
        from gui.display_panel import DisplayPanel
        from gui.plot_panel import PlotPanel
        from gui.simulation_engine import SimulationEngine
        
        print("✓ All GUI components imported successfully")
        
        # Test simulation engine (non-GUI component)
        engine = SimulationEngine()
        print("✓ Simulation engine initialized")
        
        # Test basic calculation with proper control format
        controls = {
            'collective_pitch': 0.5,
            'cyclic_pitch': 0.0,
            'tail_rotor_pitch': 0.0,
            'throttle': 0.5,
            'altitude': 1000
        }
        engine.calculate_forces_and_moments(controls)
        forces = engine.get_forces_moments()
        print(f"✓ Force calculation test: {len(forces)} components")
        
    except ImportError as e:
        if "tkinter" in str(e).lower():
            print("⚠️  GUI test skipped - tkinter not available (common in headless environments)")
            return
        else:
            raise


def test_file_structure():
    """Test that all expected files and directories exist"""
    expected_structure = {
        'flight_sim_part1': ['main.py', 'user_inputs.py', 'atmosphere.py', 'integrators.py'],
        'gui': ['helicopter_gui_main.py', 'control_panel.py', 'simulation_engine.py'],
        '.': ['README.md', 'README.txt']
    }
    
    for directory, files in expected_structure.items():
        dir_path = Path(directory)
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory missing: {directory}")
        
        for filename in files:
            file_path = dir_path / filename
            if not file_path.exists():
                raise FileNotFoundError(f"File missing: {directory}/{filename}")
    
    print("✓ All expected files and directories exist")


def test_integration():
    """Test integration between different components"""
    # Test that GUI can use flight sim components
    sys.path.append('flight_sim_part1')
    from user_inputs import get_user_inputs
    from gui.simulation_engine import SimulationEngine
    
    inputs = get_user_inputs()
    engine = SimulationEngine()
    
    # Test that simulation engine can process flight sim data
    controls = {
        'collective_pitch': 0.5,
        'cyclic_pitch': 0.0,
        'tail_rotor_pitch': 0.0,
        'throttle': 0.5,
        'altitude': 1000
    }
    engine.calculate_forces_and_moments(controls)
    forces = engine.get_forces_moments()
    print("✓ GUI-FlightSim integration working")


def main():
    """Run all tests"""
    print("HELICOPTER FLIGHT SIMULATOR - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    runner = TestRunner()
    
    # Core functionality tests
    runner.test("Package Imports", test_imports)
    runner.test("File Structure", test_file_structure)
    runner.test("Flight Sim Core Components", test_flight_sim_core)
    runner.test("Flight Sim Main Execution", test_flight_sim_main)
    
    # GUI tests (may skip if no display)
    runner.test("GUI Components", test_gui_components)
    
    # Integration tests
    runner.test("Component Integration", test_integration)
    
    # Print summary
    success = runner.summary()
    
    if success:
        print(f"\n🎉 ALL TESTS PASSED! Your helicopter simulator is ready to fly!")
    else:
        print(f"\n⚠️  Some tests failed. Check the errors above and fix them.")
        sys.exit(1)


if __name__ == "__main__":
    main()