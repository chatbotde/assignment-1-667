#!/usr/bin/env python3
"""
Mission Controller Demo
Demonstrates how to use the mission controller for flight operations
"""

import sys
import os
from mission_interface import MissionInterface

def demo_basic_operations():
    """Demonstrate basic mission controller operations"""
    print("MISSION CONTROLLER DEMO")
    print("="*50)
    
    # Initialize mission interface
    print("1. Initializing Mission Controller...")
    interface = MissionInterface()
    print("✓ Mission controller ready")
    
    # Show available mission types
    print(f"\n2. Available Mission Types:")
    missions = interface.list_available_missions()
    for i, mission in enumerate(missions, 1):
        print(f"   {i}. {mission}")
    
    # Create a test mission
    print(f"\n3. Creating Test Mission...")
    mission_id = interface.create_simple_mission("test")
    
    # Show mission summary
    print(f"\n4. Mission Summary:")
    summary = interface.generate_mission_summary(mission_id)
    print(summary)
    
    # Analyze mission feasibility
    print(f"5. Feasibility Analysis:")
    feasibility = interface.analyze_mission_feasibility(mission_id)
    
    if feasibility['feasible']:
        print("✓ Mission is FEASIBLE")
    else:
        print("✗ Mission is NOT FEASIBLE")
        
    if feasibility['issues']:
        print("Issues found:")
        for issue in feasibility['issues']:
            print(f"  • {issue}")
    
    if feasibility['warnings']:
        print("Warnings:")
        for warning in feasibility['warnings']:
            print(f"  • {warning}")
    
    # Show flight performance at key conditions
    print(f"\n6. Flight Performance Analysis:")
    conditions = [
        (0, 0, "Ground hover"),
        (100, 0, "100m hover"),
        (200, 15, "200m cruise"),
        (500, 25, "500m high-speed cruise")
    ]
    
    print("Condition              | Power | Efficiency | Tip Mach")
    print("-" * 55)
    
    for alt, vel, desc in conditions:
        perf = interface.get_flight_performance(alt, vel)
        if perf:
            print(f"{desc:20s}   | {perf['power_kW']:5.1f} | {perf['efficiency_N_per_kW']:10.1f} | {perf['tip_mach']:8.3f}")
    
    return mission_id

def demo_custom_mission():
    """Demonstrate custom mission creation"""
    print(f"\n{'='*50}")
    print("CUSTOM MISSION DEMO")
    print('='*50)
    
    interface = MissionInterface()
    
    # Create a custom search and rescue mission
    print("Creating custom Search & Rescue mission...")
    
    custom_segments = [
        # Takeoff and climb
        {"type": "hover", "duration_s": 30, "altitude_m": 0},
        {"type": "vclimb", "duration_s": 90, "start_alt_m": 0, "climb_rate_mps": 2},
        
        # Transit to search area
        {"type": "cruise", "duration_s": 300, "altitude_m": 180, "V_forward_mps": 25},
        
        # Search pattern
        {"type": "loiter", "duration_s": 600, "altitude_m": 150, "V_loiter_mps": 8},
        {"type": "cruise", "duration_s": 120, "altitude_m": 150, "V_forward_mps": 15},
        {"type": "loiter", "duration_s": 300, "altitude_m": 150, "V_loiter_mps": 8},
        
        # Rescue hover
        {"type": "hover", "duration_s": 180, "altitude_m": 50},
        
        # Return transit
        {"type": "cruise", "duration_s": 300, "altitude_m": 200, "V_forward_mps": 30},
        {"type": "hover", "duration_s": 60, "altitude_m": 0}
    ]
    
    mission_id = interface.create_custom_mission(custom_segments, "Custom SAR Mission")
    
    # Analyze the custom mission
    print(f"\nCustom Mission Analysis:")
    feasibility = interface.analyze_mission_feasibility(mission_id)
    
    print(f"Feasible: {'✓ YES' if feasibility['feasible'] else '✗ NO'}")
    
    if feasibility['performance']:
        print("\nSegment Performance:")
        for seg_name, perf in feasibility['performance'].items():
            seg_num = seg_name.split('_')[1]
            print(f"  Segment {seg_num}: {perf['power_kW']:.1f} kW, {perf['efficiency_N_per_kW']:.1f} N/kW")
    
    return mission_id

def demo_mission_comparison():
    """Demonstrate mission comparison"""
    print(f"\n{'='*50}")
    print("MISSION COMPARISON DEMO")
    print('='*50)
    
    interface = MissionInterface()
    
    # Create different mission types
    missions = {}
    mission_types = ["test", "patrol", "search_rescue"]
    
    print("Creating and comparing different mission types...")
    
    for mission_type in mission_types:
        try:
            mission_id = interface.create_simple_mission(mission_type)
            missions[mission_type] = mission_id
            print(f"✓ Created {mission_type} mission")
        except Exception as e:
            print(f"✗ Failed to create {mission_type} mission: {e}")
    
    # Compare feasibility
    print(f"\nMission Feasibility Comparison:")
    print("Mission Type    | Feasible | Issues | Warnings")
    print("-" * 50)
    
    for mission_type, mission_id in missions.items():
        feasibility = interface.analyze_mission_feasibility(mission_id)
        feasible = "✓" if feasibility['feasible'] else "✗"
        issues = len(feasibility['issues'])
        warnings = len(feasibility['warnings'])
        
        print(f"{mission_type:14s} | {feasible:8s} | {issues:6d} | {warnings:8d}")
    
    return missions

def demo_performance_envelope():
    """Demonstrate flight performance envelope"""
    print(f"\n{'='*50}")
    print("PERFORMANCE ENVELOPE DEMO")
    print('='*50)
    
    interface = MissionInterface()
    
    print("Flight Performance Envelope Analysis:")
    print("Testing aircraft performance across different conditions...")
    
    # Test altitude performance
    print(f"\nAltitude Performance (Hover):")
    print("Altitude(m) | Power(kW) | Efficiency(N/kW) | Feasible")
    print("-" * 55)
    
    altitudes = [0, 500, 1000, 1500, 2000, 2500, 3000]
    for alt in altitudes:
        perf = interface.get_flight_performance(alt, 0)
        if perf:
            feasible = "✓" if perf['power_kW'] < 1000 else "✗"  # Assuming 1000kW limit
            print(f"{alt:10d}  | {perf['power_kW']:8.1f}  | {perf['efficiency_N_per_kW']:14.1f}  | {feasible}")
    
    # Test speed performance
    print(f"\nSpeed Performance (Sea Level):")
    print("Speed(m/s) | Power(kW) | Efficiency(N/kW) | Tip Mach")
    print("-" * 55)
    
    speeds = [0, 5, 10, 15, 20, 25, 30, 35, 40]
    for speed in speeds:
        perf = interface.get_flight_performance(0, speed)
        if perf:
            print(f"{speed:9d}  | {perf['power_kW']:8.1f}  | {perf['efficiency_N_per_kW']:14.1f}  | {perf['tip_mach']:8.3f}")

def main():
    """Main demo function"""
    try:
        # Basic operations demo
        mission_id = demo_basic_operations()
        
        # Custom mission demo
        custom_mission_id = demo_custom_mission()
        
        # Mission comparison demo
        missions = demo_mission_comparison()
        
        # Performance envelope demo
        demo_performance_envelope()
        
        print(f"\n{'='*50}")
        print("DEMO COMPLETE")
        print('='*50)
        print("Mission Controller Features Demonstrated:")
        print("✓ Basic mission operations")
        print("✓ Custom mission creation")
        print("✓ Mission feasibility analysis")
        print("✓ Flight performance analysis")
        print("✓ Mission comparison")
        print("✓ Performance envelope testing")
        
        print(f"\nMission Controller is ready for:")
        print("• Real-time mission execution")
        print("• Integration with autopilot systems")
        print("• Mission planning and optimization")
        print("• Performance monitoring and analysis")
        
    except Exception as e:
        print(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()