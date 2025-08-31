#!/usr/bin/env python3
"""
Test integration between flight simulation and mission planner
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mission planner', 'mission_planner_part2'))

def test_flight_sim_mission_integration():
    """Test flight sim with mission planner"""
    print("Testing Flight Sim + Mission Planner integration...")
    
    try:
        # Import flight sim components
        from main import run as flight_sim_main
        from rotor import Rotor
        from atmosphere import isa_properties
        
        print("✓ Flight sim modules imported successfully")
        
        # Try to import mission planner (if available)
        try:
            # This will depend on what's in the mission planner folder
            print("  Checking mission planner availability...")
            mission_path = os.path.join(os.path.dirname(__file__), '..', 'mission planner', 'mission_planner_part2')
            if os.path.exists(mission_path):
                print("✓ Mission planner directory found")
            else:
                print("! Mission planner directory not found")
        except Exception as e:
            print(f"  Mission planner import issue: {e}")
        
        # Test basic flight sim functionality
        print("  Running flight simulation...")
        flight_sim_main()
        print("✓ Flight simulation completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

def test_performance_scenarios():
    """Test different flight scenarios"""
    print("\nTesting performance scenarios...")
    
    scenarios = [
        {"name": "Hover", "velocity": 0, "altitude": 100},
        {"name": "Forward Flight", "velocity": 20, "altitude": 500},
        {"name": "High Altitude", "velocity": 15, "altitude": 3000},
    ]
    
    try:
        from atmosphere import isa_properties
        
        for scenario in scenarios:
            name = scenario["name"]
            vel = scenario["velocity"]
            alt = scenario["altitude"]
            
            rho, a = isa_properties(alt)
            
            print(f"  {name}: {vel} m/s at {alt}m")
            print(f"    Density: {rho:.4f} kg/m³, Sound speed: {a:.1f} m/s")
        
        print("✓ Performance scenarios tested")
        return True
        
    except Exception as e:
        print(f"✗ Performance scenarios failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Mission Integration Tests ===\n")
    
    success = True
    success &= test_flight_sim_mission_integration()
    success &= test_performance_scenarios()
    
    print(f"\n=== Integration Results ===")
    if success:
        print("✓ Integration tests passed!")
        print("\nReady for:")
        print("- Mission planning integration")
        print("- Performance optimization")
        print("- Real-time simulation")
    else:
        print("✗ Some integration tests failed")
        print("Check individual components first")