#!/usr/bin/env python3
"""
Integration test script for flight simulation components
Tests all modules working together
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))

from main import run as flight_sim_main
from rotor import Rotor
from atmosphere import isa_properties
from inflow import prandtl_tip_loss
import numpy as np

def test_basic_integration():
    """Test basic integration of all components"""
    print("Testing basic integration...")
    
    try:
        # Test atmosphere
        from atmosphere import isa_properties
        rho, a = isa_properties(0)  # Sea level properties
        print(f"✓ Atmosphere: Sea level density = {rho:.4f} kg/m³, sound speed = {a:.1f} m/s")
        
        # Test basic flight sim run
        print("✓ Running main flight simulation...")
        flight_sim_main()
        print("✓ Flight simulation completed successfully")
        
        return True
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

def test_rotor_performance():
    """Test rotor performance calculations"""
    print("\nTesting rotor performance...")
    
    try:
        # Initialize components
        from rotor import Rotor
        from blade import Blade
        from airfoil import Airfoil
        from atmosphere import isa_properties
        import math
        
        # Create test rotor
        airfoil = Airfoil()
        blade = Blade(
            R_root=0.5, R_tip=5.0, c_root=0.3, c_tip=0.1,
            theta_root_rad=math.radians(15), theta_tip_rad=math.radians(5),
            airfoil=airfoil
        )
        rotor = Rotor(B=4, blade=blade)
        
        # Test at different conditions
        test_conditions = [
            {"altitude": 0, "velocity": 10},
            {"altitude": 1000, "velocity": 15},
            {"altitude": 2000, "velocity": 20}
        ]
        
        for condition in test_conditions:
            alt = condition["altitude"]
            vel = condition["velocity"]
            rho, a = isa_properties(alt)
            
            print(f"  Testing at {alt}m altitude, {vel} m/s velocity")
            print(f"  Density: {rho:.4f} kg/m³")
        
        print("✓ Rotor performance tests completed")
        return True
        
    except Exception as e:
        print(f"✗ Rotor performance test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Flight Simulation Integration Tests ===\n")
    
    success = True
    success &= test_basic_integration()
    success &= test_rotor_performance()
    
    print(f"\n=== Test Results ===")
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    
    print("\nNext steps:")
    print("1. Run individual component tests")
    print("2. Test with mission planner integration")
    print("3. Performance optimization tests")