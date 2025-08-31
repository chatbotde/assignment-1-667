#!/usr/bin/env python3
"""
Test realistic helicopter configurations
Create configurations that can actually hover
"""

import sys
import os
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))

from rotor import Rotor
from blade import Blade
from airfoil import Airfoil
from atmosphere import isa_properties
from integrators import cycle_integrator

def test_small_helicopter_config():
    """Test configuration for small helicopter (100-200kg)"""
    print("=== Small Helicopter Configuration ===")
    
    try:
        # Realistic small helicopter parameters
        # Similar to Robinson R22 or small UAV helicopter
        config = {
            "R_tip": 4.0,      # 4m radius (8m diameter)
            "R_root": 0.4,     # 10% of tip radius
            "B": 2,            # 2 blades (typical for small helicopters)
            "c_root": 0.25,    # 25cm chord at root
            "c_tip": 0.15,     # 15cm chord at tip
            "theta_root_deg": 12,  # 12° collective at root
            "theta_tip_deg": 8,    # 8° at tip (twist)
            "rpm": 400,        # Lower RPM for larger rotor
            "weight_kg": 150   # 150kg aircraft
        }
        
        print(f"Configuration:")
        print(f"  Rotor diameter: {config['R_tip']*2:.1f} m")
        print(f"  Blades: {config['B']}")
        print(f"  RPM: {config['rpm']}")
        print(f"  Aircraft weight: {config['weight_kg']} kg")
        
        # Create rotor
        airfoil = Airfoil(a0=5.75, Cd0=0.008, e=0.9)
        blade = Blade(
            R_root=config["R_root"],
            R_tip=config["R_tip"],
            c_root=config["c_root"],
            c_tip=config["c_tip"],
            theta_root_rad=math.radians(config["theta_root_deg"]),
            theta_tip_rad=math.radians(config["theta_tip_deg"]),
            airfoil=airfoil
        )
        rotor = Rotor(B=config["B"], blade=blade)
        
        # Test conditions
        rho, a = isa_properties(0)  # Sea level
        omega = 2*math.pi*config["rpm"]/60.0
        M_tip = (omega * config["R_tip"]) / a
        
        print(f"  Tip Mach: {M_tip:.3f} (limit: {rotor.tip_mach_limit})")
        
        if M_tip <= rotor.tip_mach_limit:
            T, Q, P = cycle_integrator(rotor, 0, omega, rho)
            required_thrust = config["weight_kg"] * 9.81
            
            print(f"  Thrust capability: {T:.1f} N")
            print(f"  Required thrust: {required_thrust:.1f} N")
            print(f"  Power: {P/1000:.1f} kW")
            print(f"  Disk loading: {required_thrust/(math.pi*config['R_tip']**2):.1f} N/m²")
            
            if T >= required_thrust:
                print("  ✓ HOVER FEASIBLE!")
                margin = (T - required_thrust) / required_thrust * 100
                print(f"  Thrust margin: {margin:.1f}%")
            else:
                print("  ✗ Hover not feasible")
                deficit = (required_thrust - T) / required_thrust * 100
                print(f"  Thrust deficit: {deficit:.1f}%")
        else:
            print("  ✗ Tip speed too high")
        
        return config, T if M_tip <= rotor.tip_mach_limit else 0
        
    except Exception as e:
        print(f"✗ Small helicopter test failed: {e}")
        return None, 0

def test_large_drone_config():
    """Test configuration for large drone (20-50kg)"""
    print("\n=== Large Drone Configuration ===")
    
    try:
        # Realistic large drone parameters
        config = {
            "R_tip": 1.5,      # 1.5m radius (3m diameter)
            "R_root": 0.15,    # 10% of tip radius
            "B": 4,            # 4 blades for efficiency
            "c_root": 0.12,    # 12cm chord at root
            "c_tip": 0.08,     # 8cm chord at tip
            "theta_root_deg": 15,  # Higher collective for smaller rotor
            "theta_tip_deg": 10,   # More twist
            "rpm": 1200,       # Higher RPM for smaller rotor
            "weight_kg": 35    # 35kg aircraft
        }
        
        print(f"Configuration:")
        print(f"  Rotor diameter: {config['R_tip']*2:.1f} m")
        print(f"  Blades: {config['B']}")
        print(f"  RPM: {config['rpm']}")
        print(f"  Aircraft weight: {config['weight_kg']} kg")
        
        # Create rotor
        airfoil = Airfoil(a0=5.75, Cd0=0.008, e=0.9)
        blade = Blade(
            R_root=config["R_root"],
            R_tip=config["R_tip"],
            c_root=config["c_root"],
            c_tip=config["c_tip"],
            theta_root_rad=math.radians(config["theta_root_deg"]),
            theta_tip_rad=math.radians(config["theta_tip_deg"]),
            airfoil=airfoil
        )
        rotor = Rotor(B=config["B"], blade=blade)
        
        # Test conditions
        rho, a = isa_properties(0)  # Sea level
        omega = 2*math.pi*config["rpm"]/60.0
        M_tip = (omega * config["R_tip"]) / a
        
        print(f"  Tip Mach: {M_tip:.3f} (limit: {rotor.tip_mach_limit})")
        
        if M_tip <= rotor.tip_mach_limit:
            T, Q, P = cycle_integrator(rotor, 0, omega, rho)
            required_thrust = config["weight_kg"] * 9.81
            
            print(f"  Thrust capability: {T:.1f} N")
            print(f"  Required thrust: {required_thrust:.1f} N")
            print(f"  Power: {P/1000:.1f} kW")
            print(f"  Disk loading: {required_thrust/(math.pi*config['R_tip']**2):.1f} N/m²")
            
            if T >= required_thrust:
                print("  ✓ HOVER FEASIBLE!")
                margin = (T - required_thrust) / required_thrust * 100
                print(f"  Thrust margin: {margin:.1f}%")
            else:
                print("  ✗ Hover not feasible")
                deficit = (required_thrust - T) / required_thrust * 100
                print(f"  Thrust deficit: {deficit:.1f}%")
        else:
            print("  ✗ Tip speed too high")
        
        return config, T if M_tip <= rotor.tip_mach_limit else 0
        
    except Exception as e:
        print(f"✗ Large drone test failed: {e}")
        return None, 0

def test_micro_helicopter_config():
    """Test configuration for micro helicopter (5-15kg)"""
    print("\n=== Micro Helicopter Configuration ===")
    
    try:
        # Realistic micro helicopter parameters
        config = {
            "R_tip": 0.8,      # 0.8m radius (1.6m diameter)
            "R_root": 0.08,    # 10% of tip radius
            "B": 2,            # 2 blades
            "c_root": 0.08,    # 8cm chord at root
            "c_tip": 0.05,     # 5cm chord at tip
            "theta_root_deg": 18,  # High collective for small rotor
            "theta_tip_deg": 12,   # Significant twist
            "rpm": 2000,       # High RPM for small rotor
            "weight_kg": 10    # 10kg aircraft
        }
        
        print(f"Configuration:")
        print(f"  Rotor diameter: {config['R_tip']*2:.1f} m")
        print(f"  Blades: {config['B']}")
        print(f"  RPM: {config['rpm']}")
        print(f"  Aircraft weight: {config['weight_kg']} kg")
        
        # Create rotor
        airfoil = Airfoil(a0=5.75, Cd0=0.008, e=0.9)
        blade = Blade(
            R_root=config["R_root"],
            R_tip=config["R_tip"],
            c_root=config["c_root"],
            c_tip=config["c_tip"],
            theta_root_rad=math.radians(config["theta_root_deg"]),
            theta_tip_rad=math.radians(config["theta_tip_deg"]),
            airfoil=airfoil
        )
        rotor = Rotor(B=config["B"], blade=blade)
        
        # Test conditions
        rho, a = isa_properties(0)  # Sea level
        omega = 2*math.pi*config["rpm"]/60.0
        M_tip = (omega * config["R_tip"]) / a
        
        print(f"  Tip Mach: {M_tip:.3f} (limit: {rotor.tip_mach_limit})")
        
        if M_tip <= rotor.tip_mach_limit:
            T, Q, P = cycle_integrator(rotor, 0, omega, rho)
            required_thrust = config["weight_kg"] * 9.81
            
            print(f"  Thrust capability: {T:.1f} N")
            print(f"  Required thrust: {required_thrust:.1f} N")
            print(f"  Power: {P/1000:.1f} kW")
            print(f"  Disk loading: {required_thrust/(math.pi*config['R_tip']**2):.1f} N/m²")
            
            if T >= required_thrust:
                print("  ✓ HOVER FEASIBLE!")
                margin = (T - required_thrust) / required_thrust * 100
                print(f"  Thrust margin: {margin:.1f}%")
            else:
                print("  ✗ Hover not feasible")
                deficit = (required_thrust - T) / required_thrust * 100
                print(f"  Thrust deficit: {deficit:.1f}%")
        else:
            print("  ✗ Tip speed too high")
        
        return config, T if M_tip <= rotor.tip_mach_limit else 0
        
    except Exception as e:
        print(f"✗ Micro helicopter test failed: {e}")
        return None, 0

def create_optimal_user_inputs(best_config):
    """Create new user_inputs.py with optimal configuration"""
    print(f"\n=== Creating Optimal Configuration File ===")
    
    if not best_config:
        print("No feasible configuration found!")
        return
    
    config_code = f'''import math
from airfoil import Airfoil
from blade import Blade
from rotor import Rotor

def get_user_inputs():
    # Optimized configuration for hover feasibility
    # Based on realistic helicopter parameters
    return {{
        "rotor": {{
            "B": {best_config["B"]},
            "R_root": {best_config["R_root"]:.3f},
            "R_tip": {best_config["R_tip"]:.3f},
            "c_root": {best_config["c_root"]:.3f},
            "c_tip": {best_config["c_tip"]:.3f},
            "theta_root_deg": {best_config["theta_root_deg"]:.1f},
            "theta_tip_deg": {best_config["theta_tip_deg"]:.1f},
            "airfoil": {{"a0": 5.75, "Cd0": 0.008, "e": 0.9, "alpha_stall_deg": 15.0}},
            "tip_mach_limit": 0.90
        }},
        "stabilizers": {{
            "S_h": 2.2, "i_h_deg": 2.0, "CLa_h_per_rad": 6.5, "l_h": 5.0,
            "S_v": 1.5, "CYb_v_per_rad": 2.4, "l_v": 3.0,
        }},
        "condition": {{
            "alt_m": 0.0,
            "V_forward_mps": 0.0,
            "rpm": {best_config["rpm"]:.1f}
        }}
    }}

def build_rotor(params):
    af = Airfoil(**params["airfoil"])
    bl = Blade(params["R_root"], params["R_tip"],
               params["c_root"], params["c_tip"],
               math.radians(params["theta_root_deg"]),
               math.radians(params["theta_tip_deg"]))
    bl.airfoil = af
    return Rotor(params["B"], bl, tip_mach_limit=params.get("tip_mach_limit", 0.9))
'''
    
    # Save the optimized configuration
    with open("test_integration/optimized_user_inputs.py", "w") as f:
        f.write(config_code)
    
    print("✓ Created optimized_user_inputs.py")
    print("  Copy this to flight_sim_part1/user_inputs.py to use the optimal configuration")

if __name__ == "__main__":
    print("REALISTIC HELICOPTER CONFIGURATION TESTS")
    print("="*60)
    
    # Test different realistic configurations
    configs = []
    thrusts = []
    
    config1, thrust1 = test_small_helicopter_config()
    if config1: configs.append(("Small Helicopter", config1, thrust1))
    
    config2, thrust2 = test_large_drone_config()
    if config2: configs.append(("Large Drone", config2, thrust2))
    
    config3, thrust3 = test_micro_helicopter_config()
    if config3: configs.append(("Micro Helicopter", config3, thrust3))
    
    # Find best configuration
    print(f"\n{'='*60}")
    print("CONFIGURATION COMPARISON")
    print("="*60)
    
    feasible_configs = [(name, config, thrust) for name, config, thrust in configs if thrust >= config["weight_kg"] * 9.81]
    
    if feasible_configs:
        print("Feasible configurations:")
        for name, config, thrust in feasible_configs:
            required = config["weight_kg"] * 9.81
            margin = (thrust - required) / required * 100
            efficiency = thrust / (config["weight_kg"] * 9.81)
            print(f"  {name}: {thrust:.1f}N thrust, {margin:.1f}% margin, {efficiency:.2f} T/W ratio")
        
        # Choose the most efficient feasible configuration
        best = max(feasible_configs, key=lambda x: x[2] / (x[1]["weight_kg"] * 9.81))
        best_name, best_config, best_thrust = best
        
        print(f"\nRecommended: {best_name}")
        create_optimal_user_inputs(best_config)
    else:
        print("No feasible configurations found!")
        print("All tested configurations either:")
        print("- Exceed tip Mach limit, or")
        print("- Cannot generate sufficient thrust")
    
    print(f"\n{'='*60}")
    print("NEXT STEPS")
    print("="*60)
    print("1. Copy optimized_user_inputs.py to flight_sim_part1/user_inputs.py")
    print("2. Run the main flight simulation again")
    print("3. Verify hover feasibility")
    print("4. Test forward flight performance")