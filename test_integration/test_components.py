#!/usr/bin/env python3
"""
Individual component tests for flight simulation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))

def test_atmosphere():
    """Test atmosphere module"""
    print("Testing Atmosphere module...")
    try:
        from atmosphere import isa_properties
        
        # Test standard conditions
        result_sl = isa_properties(0)
        print(f"  Sea level ISA properties calculated")
        
        # Test at altitude
        result_alt = isa_properties(3000)
        print(f"  3000m ISA properties calculated")
        
        print("✓ Atmosphere module working")
        return True
    except Exception as e:
        print(f"✗ Atmosphere test failed: {e}")
        return False

def test_airfoil():
    """Test airfoil module"""
    print("\nTesting Airfoil module...")
    try:
        from airfoil import Airfoil
        import math
        
        airfoil = Airfoil()
        
        # Test lift and drag coefficients
        alpha_deg = 5.0
        alpha_rad = math.radians(alpha_deg)
        cl, cd, cm = airfoil.lookup(alpha_rad)
        
        print(f"  At {alpha_deg}° AoA: Cl = {cl:.4f}, Cd = {cd:.4f}, Cm = {cm:.4f}")
        print("✓ Airfoil module working")
        return True
    except Exception as e:
        print(f"✗ Airfoil test failed: {e}")
        return False

def test_rotor():
    """Test rotor module"""
    print("\nTesting Rotor module...")
    try:
        from rotor import Rotor
        from blade import Blade
        from airfoil import Airfoil
        import math
        
        # Create a simple blade for testing
        airfoil = Airfoil()
        blade = Blade(
            R_root=0.5, 
            R_tip=5.0, 
            c_root=0.3, 
            c_tip=0.1, 
            theta_root_rad=math.radians(15), 
            theta_tip_rad=math.radians(5),
            airfoil=airfoil
        )
        rotor = Rotor(B=4, blade=blade)
        
        print(f"  Number of blades: {rotor.B}")
        print(f"  Tip Mach limit: {rotor.tip_mach_limit}")
        
        # Test solidity calculation
        solidity = rotor.solidity_local(2.5)
        print(f"  Local solidity at r=2.5m: {solidity:.4f}")
        
        print("✓ Rotor module working")
        return True
    except Exception as e:
        print(f"✗ Rotor test failed: {e}")
        return False

def test_inflow():
    """Test inflow module"""
    print("\nTesting Inflow module...")
    try:
        from inflow import prandtl_tip_loss, induced_velocity_annulus
        
        # Test Prandtl tip loss function
        B = 4
        r = 4.0
        R = 5.0
        lambda_ = 0.1
        F = prandtl_tip_loss(B, r, R, lambda_)
        
        print(f"  Prandtl tip loss factor: {F:.4f}")
        print("✓ Inflow module working")
        return True
    except Exception as e:
        print(f"✗ Inflow test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Component Tests ===\n")
    
    tests = [
        test_atmosphere,
        test_airfoil,
        test_rotor,
        test_inflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("✓ All component tests passed!")
    else:
        print("✗ Some component tests failed")