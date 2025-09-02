#!/usr/bin/env python3
"""
Individual Design Plots Generator
Creates the same plots as in report_output folder for individual helicopter design
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import json

# Add paths for flight simulation and mission planner
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mission planner', 'mission_planner_part2'))

# Flight simulation imports
from rotor import Rotor
from blade import Blade
from airfoil import Airfoil
from atmosphere import isa_properties
from integrators import cycle_integrator

# Mission planner imports
from engine import Engine
from vehicle import Helicopter

def load_experimental_data(blade_count):
    """Load experimental data for given blade count"""
    csv_file = f"flight_sim_part1/exp_B{blade_count}.csv"
    
    if not os.path.exists(csv_file):
        print(f"Warning: {csv_file} not found")
        return None
    
    data = {
        'theta_deg': [],
        'CT_exp': [],
        'CQ_exp': []
    }
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data['theta_deg'].append(float(row['theta_deg']))
                data['CT_exp'].append(float(row['CT_exp']))
                data['CQ_exp'].append(float(row['CQ_exp']))
        
        print(f"✓ Loaded {len(data['theta_deg'])} experimental points for B={blade_count}")
        return data
    
    except Exception as e:
        print(f"✗ Error loading {csv_file}: {e}")
        return None

def run_simulation_sweep(blade_count, theta_range):
    """Run simulation for different collective pitch angles"""
    print(f"\nRunning simulation sweep for B={blade_count} blades...")
    
    try:
        # Create rotor with experimental configuration
        airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25, alpha_stall_deg=15.0)
        blade = Blade(
            R_root=0.125,
            R_tip=0.762,
            c_root=0.0508,
            c_tip=0.0508,
            theta_root_rad=0,  # Will be varied
            theta_tip_rad=0,   # Will be varied
            airfoil=airfoil
        )
        rotor = Rotor(B=blade_count, blade=blade)
        
        # Simulation conditions
        rho, a = isa_properties(0)  # Sea level
        rpm = 960.0
        omega = 2*math.pi*rpm/60.0
        V = 0  # Hover condition
        
        # Calculate reference values for coefficients
        A = math.pi * rotor.blade.R_tip**2  # Disk area
        rho_ref = rho
        omega_ref = omega
        R_ref = rotor.blade.R_tip
        
        results = {
            'theta_deg': [],
            'CT_sim': [],
            'CQ_sim': [],
            'T_N': [],
            'Q_Nm': [],
            'P_W': []
        }
        
        for theta_deg in theta_range:
            # Update blade pitch
            theta_rad = math.radians(theta_deg)
            blade.theta_root = theta_rad
            blade.theta_tip = theta_rad
            
            # Run simulation
            T, Q, P = cycle_integrator(rotor, V, omega, rho)
            
            # Calculate coefficients
            CT = T / (rho_ref * A * (omega_ref * R_ref)**2)
            CQ = Q / (rho_ref * A * R_ref * (omega_ref * R_ref)**2)
            
            results['theta_deg'].append(theta_deg)
            results['CT_sim'].append(CT)
            results['CQ_sim'].append(CQ)
            results['T_N'].append(T)
            results['Q_Nm'].append(Q)
            results['P_W'].append(P)
        
        return results
    
    except Exception as e:
        print(f"✗ Simulation sweep failed for B={blade_count}: {e}")
        return None

def create_thrust_torque_vs_pitch_plots():
    """Create thrust and torque vs pitch plots comparing simulation with experimental data"""
    print("Creating thrust and torque vs pitch plots...")
    
    try:
        # Test all blade configurations
        blade_counts = [2, 3, 4, 5]
        comparison_results = []
        
        for B in blade_counts:
            # Load experimental data
            exp_data = load_experimental_data(B)
            if not exp_data:
                continue
            
            # Run simulation at experimental pitch angles
            theta_range = exp_data['theta_deg']
            sim_data = run_simulation_sweep(B, theta_range)
            if not sim_data:
                continue
            
            comparison_results.append({
                'blade_count': B,
                'exp_data': exp_data,
                'sim_data': sim_data
            })
        
        if not comparison_results:
            print("No comparison data available")
            return
        
        # Create plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        colors = ['blue', 'red', 'green', 'orange']
        
        for i, result in enumerate(comparison_results):
            B = result['blade_count']
            exp = result['exp_data']
            sim = result['sim_data']
            color = colors[i % len(colors)]
            
            # CT comparison
            ax1.plot(exp['theta_deg'], exp['CT_exp'], 'o-', color=color, label=f'B={B} Exp', markersize=6)
            ax1.plot(sim['theta_deg'], sim['CT_sim'], 's--', color=color, label=f'B={B} Sim', markersize=6)
            
            # CQ comparison
            ax2.plot(exp['theta_deg'], exp['CQ_exp'], 'o-', color=color, label=f'B={B} Exp', markersize=6)
            ax2.plot(sim['theta_deg'], sim['CQ_sim'], 's--', color=color, label=f'B={B} Sim', markersize=6)
        
        # Format CT plot
        ax1.set_xlabel('Collective Pitch (degrees)', fontsize=12)
        ax1.set_ylabel('Thrust Coefficient (CT)', fontsize=12)
        ax1.set_title('Thrust Coefficient vs Collective Pitch', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Format CQ plot
        ax2.set_xlabel('Collective Pitch (degrees)', fontsize=12)
        ax2.set_ylabel('Torque Coefficient (CQ)', fontsize=12)
        ax2.set_title('Torque Coefficient vs Collective Pitch', fontsize=14)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('individual_design/thrust_vs_pitch.png', dpi=300, bbox_inches='tight')
        plt.savefig('individual_design/torque_vs_pitch.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved thrust_vs_pitch.png and torque_vs_pitch.png")
        
    except Exception as e:
        print(f"✗ Error creating thrust/torque vs pitch plots: {e}")

def create_thrust_vs_power_plot():
    """Create thrust vs power plot using individual design parameters"""
    print("Creating thrust vs power plot...")
    
    try:
        # Load individual design parameters
        json_path = os.path.join(os.path.dirname(__file__), 'compound_helicopter_design.json')
        with open(json_path, 'r') as f:
            design = json.load(f)
        
        main_rotor_params = design['main_rotor']
        
        # Create rotor with individual design configuration
        airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25, alpha_stall_deg=15.0)
        blade = Blade(
            R_root=main_rotor_params['root_cutout_m'],
            R_tip=main_rotor_params['radius_m'],
            c_root=main_rotor_params['chord_root_m'],
            c_tip=main_rotor_params['chord_tip_m'],
            theta_root_rad=0,
            theta_tip_rad=math.radians(main_rotor_params['twist_deg']),
            airfoil=airfoil
        )
        
        # Simulation conditions
        rho, a = isa_properties(0)  # Sea level
        rpm = main_rotor_params['rpm']
        omega = 2*math.pi*rpm/60.0
        V = 0  # Hover condition
        
        # Test different blade counts
        blade_counts = [2, 3, 4, 5]
        colors = ['blue', 'red', 'green', 'orange']
        
        plt.figure(figsize=(10, 6))
        
        for i, B in enumerate(blade_counts):
            rotor = Rotor(B=B, blade=blade)
            color = colors[i % len(colors)]
            
            # Pitch angle sweep
            theta_range = np.linspace(0, 14, 15)
            thrust_values = []
            power_values = []
            
            for theta_deg in theta_range:
                # Update blade pitch
                theta_rad = math.radians(theta_deg)
                blade.theta_root = theta_rad
                blade.theta_tip = theta_rad + math.radians(main_rotor_params['twist_deg'])
                
                # Run simulation
                T, Q, P = cycle_integrator(rotor, V, omega, rho)
                thrust_values.append(T)
                power_values.append(P/1000)  # Convert to kW
            
            plt.plot(power_values, thrust_values, 'o-', color=color, label=f'B={B}', markersize=6)
        
        plt.xlabel('Power [kW]', fontsize=12)
        plt.ylabel('Thrust [N]', fontsize=12)
        plt.title('Thrust vs Power', fontsize=14)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('individual_design/thrust_vs_power.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved thrust_vs_power.png")
        
    except Exception as e:
        print(f"✗ Error creating thrust vs power plot: {e}")

def create_blade_count_variation_plot():
    """Create blade count variation plot using individual design parameters"""
    print("Creating blade count variation plot...")
    
    try:
        # Load individual design parameters
        json_path = os.path.join(os.path.dirname(__file__), 'compound_helicopter_design.json')
        with open(json_path, 'r') as f:
            design = json.load(f)
        
        main_rotor_params = design['main_rotor']
        
        # Create rotor with individual design configuration
        airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25, alpha_stall_deg=15.0)
        blade = Blade(
            R_root=main_rotor_params['root_cutout_m'],
            R_tip=main_rotor_params['radius_m'],
            c_root=main_rotor_params['chord_root_m'],
            c_tip=main_rotor_params['chord_tip_m'],
            theta_root_rad=math.radians(5),  # 5 degrees collective
            theta_tip_rad=math.radians(5 + main_rotor_params['twist_deg']),
            airfoil=airfoil
        )
        
        # Simulation conditions
        rho, a = isa_properties(0)  # Sea level
        rpm = main_rotor_params['rpm']
        omega = 2*math.pi*rpm/60.0
        V = 0  # Hover condition
        
        # Test different blade counts
        B_values = [2, 3, 4, 5]
        T_B = []
        P_B = []
        
        for B in B_values:
            rotor = Rotor(B=B, blade=blade)
            T, Q, P = cycle_integrator(rotor, V, omega, rho)
            T_B.append(T)
            P_B.append(P/1000)  # Convert to kW
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Thrust vs blade count
        ax1.plot(B_values, T_B, "o-", color='blue', markersize=8, linewidth=2)
        ax1.set_xlabel("Number of Blades B", fontsize=12)
        ax1.set_ylabel("Thrust [N]", fontsize=12)
        ax1.set_title("Thrust vs Number of Blades", fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        # Power vs blade count
        ax2.plot(B_values, P_B, "s-", color='red', markersize=8, linewidth=2)
        ax2.set_xlabel("Number of Blades B", fontsize=12)
        ax2.set_ylabel("Power [kW]", fontsize=12)
        ax2.set_title("Power vs Number of Blades", fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('individual_design/blade_count_variation.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved blade_count_variation.png")
        
    except Exception as e:
        print(f"✗ Error creating blade count variation plot: {e}")

def create_taper_ratio_variation_plot():
    """Create taper ratio variation plot using individual design parameters"""
    print("Creating taper ratio variation plot...")
    
    try:
        # Load individual design parameters
        json_path = os.path.join(os.path.dirname(__file__), 'compound_helicopter_design.json')
        with open(json_path, 'r') as f:
            design = json.load(f)
        
        main_rotor_params = design['main_rotor']
        
        # Create base blade configuration
        airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25, alpha_stall_deg=15.0)
        R_root = main_rotor_params['root_cutout_m']
        R_tip = main_rotor_params['radius_m']
        c_root_default = main_rotor_params['chord_root_m']
        theta_default = math.radians(5)  # 5 degrees collective
        twist_deg = main_rotor_params['twist_deg']
        
        # Simulation conditions
        rho, a = isa_properties(0)  # Sea level
        rpm = main_rotor_params['rpm']
        omega = 2*math.pi*rpm/60.0
        V = 0  # Hover condition
        
        # Test different taper ratios
        taper_ratios = np.linspace(0.3, 1.0, 8)   # c_tip / c_root
        T_taper = []
        P_taper = []
        B = main_rotor_params['num_blades']  # Use individual design blade count
        
        for tr in taper_ratios:
            c_tip = tr * c_root_default
            blade = Blade(
                R_root=R_root,
                R_tip=R_tip,
                c_root=c_root_default,
                c_tip=c_tip,
                theta_root_rad=theta_default,
                theta_tip_rad=theta_default + math.radians(twist_deg),
                airfoil=airfoil
            )
            rotor = Rotor(B=B, blade=blade)
            T, Q, P = cycle_integrator(rotor, V, omega, rho)
            T_taper.append(T)
            P_taper.append(P/1000)  # Convert to kW
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Thrust vs taper ratio
        ax1.plot(taper_ratios, T_taper, "o-", color='blue', markersize=8, linewidth=2)
        ax1.set_xlabel("Taper Ratio (c_tip / c_root)", fontsize=12)
        ax1.set_ylabel("Thrust [N]", fontsize=12)
        ax1.set_title("Thrust vs Taper Ratio", fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        # Power vs taper ratio
        ax2.plot(taper_ratios, P_taper, "s-", color='red', markersize=8, linewidth=2)
        ax2.set_xlabel("Taper Ratio (c_tip / c_root)", fontsize=12)
        ax2.set_ylabel("Power [kW]", fontsize=12)
        ax2.set_title("Power vs Taper Ratio", fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('individual_design/taper_ratio_variation.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved taper_ratio_variation.png")
        
    except Exception as e:
        print(f"✗ Error creating taper ratio variation plot: {e}")

def create_twist_variation_plot():
    """Create twist variation plot using individual design parameters"""
    print("Creating twist variation plot...")
    
    try:
        # Load individual design parameters
        json_path = os.path.join(os.path.dirname(__file__), 'compound_helicopter_design.json')
        with open(json_path, 'r') as f:
            design = json.load(f)
        
        main_rotor_params = design['main_rotor']
        
        # Create base blade configuration
        airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25, alpha_stall_deg=15.0)
        R_root = main_rotor_params['root_cutout_m']
        R_tip = main_rotor_params['radius_m']
        c_root_default = main_rotor_params['chord_root_m']
        theta_default = math.radians(5)  # 5 degrees collective
        
        # Simulation conditions
        rho, a = isa_properties(0)  # Sea level
        rpm = main_rotor_params['rpm']
        omega = 2*math.pi*rpm/60.0
        V = 0  # Hover condition
        
        # Test different twist angles
        twists = np.deg2rad(np.linspace(0, 20, 8))  # θ_tip - θ_root
        T_twist = []
        P_twist = []
        B = main_rotor_params['num_blades']  # Use individual design blade count
        
        for twist in twists:
            blade = Blade(
                R_root=R_root,
                R_tip=R_tip,
                c_root=c_root_default,
                c_tip=main_rotor_params['chord_tip_m'],
                theta_root_rad=theta_default,
                theta_tip_rad=theta_default + twist,
                airfoil=airfoil
            )
            rotor = Rotor(B=B, blade=blade)
            T, Q, P = cycle_integrator(rotor, V, omega, rho)
            T_twist.append(T)
            P_twist.append(P/1000)  # Convert to kW
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Thrust vs twist
        ax1.plot(np.rad2deg(twists), T_twist, "o-", color='blue', markersize=8, linewidth=2)
        ax1.set_xlabel("Twist (θ_tip - θ_root) [deg]", fontsize=12)
        ax1.set_ylabel("Thrust [N]", fontsize=12)
        ax1.set_title("Thrust vs Twist", fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        # Power vs twist
        ax2.plot(np.rad2deg(twists), P_twist, "s-", color='red', markersize=8, linewidth=2)
        ax2.set_xlabel("Twist (θ_tip - θ_root) [deg]", fontsize=12)
        ax2.set_ylabel("Power [kW]", fontsize=12)
        ax2.set_title("Power vs Twist", fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('individual_design/twist_variation.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved twist_variation.png")
        
    except Exception as e:
        print(f"✗ Error creating twist variation plot: {e}")

def create_fuel_burn_rate_plot():
    """Create fuel burn rate analysis plot using individual design parameters"""
    print("Creating fuel burn rate plot...")
    
    try:
        # Load individual design parameters
        json_path = os.path.join(os.path.dirname(__file__), 'compound_helicopter_design.json')
        with open(json_path, 'r') as f:
            design = json.load(f)
        
        mass_params = design['mass_breakdown']
        requirements = design['requirements']
        
        # Create helicopter and engine models using individual design
        heli = Helicopter(
            oew_kg = mass_params['operating_empty_kg'],
            payload_kg = requirements['total_payload_kg'],
            fuel_kg = mass_params['fuel_kg'],
            S_ref_m2 = 6.0,  # Default value
            CD0_body = 0.045,  # Default value
            tail_power_hover_frac = 0.12,  # From individual design (12%)
            tail_power_min_frac = 0.015
        )
        engine = Engine(P_sl_kW=1500.0, sfc_kg_per_kWh=0.32, derate_alpha=0.7)
        
        # Test different power levels
        power_levels_kW = np.linspace(100, 1500, 20)  # 100 kW to 1500 kW
        fuel_burn_rates = []
        
        for power_kW in power_levels_kW:
            # Calculate fuel burn rate (kg/hour)
            fuel_rate_kg_per_hour = power_kW * engine.sfc_kg_per_kWh
            fuel_burn_rates.append(fuel_rate_kg_per_hour)
        
        plt.figure(figsize=(10, 6))
        plt.plot(power_levels_kW, fuel_burn_rates, 'b-', linewidth=2, marker='o', markersize=6)
        plt.xlabel('Power [kW]', fontsize=12)
        plt.ylabel('Fuel Burn Rate [kg/hour]', fontsize=12)
        plt.title('Fuel Consumption vs Power', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('individual_design/fuel_burn_rate.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved fuel_burn_rate.png")
        
    except Exception as e:
        print(f"✗ Error creating fuel burn rate plot: {e}")

def create_hover_endurance_plot():
    """Create hover endurance analysis plot using individual design parameters"""
    print("Creating hover endurance plot...")
    
    try:
        # Load individual design parameters
        json_path = os.path.join(os.path.dirname(__file__), 'compound_helicopter_design.json')
        with open(json_path, 'r') as f:
            design = json.load(f)
        
        mass_params = design['mass_breakdown']
        requirements = design['requirements']
        
        # Create helicopter and engine models using individual design
        heli = Helicopter(
            oew_kg = mass_params['operating_empty_kg'],
            payload_kg = requirements['total_payload_kg'],
            fuel_kg = mass_params['fuel_kg'],
            S_ref_m2 = 6.0,  # Default value
            CD0_body = 0.045,  # Default value
            tail_power_hover_frac = 0.12,  # From individual design (12%)
            tail_power_min_frac = 0.015
        )
        engine = Engine(P_sl_kW=1500.0, sfc_kg_per_kWh=0.32, derate_alpha=0.7)
        
        # Test different weights
        weights_kg = np.linspace(
            mass_params['operating_empty_kg'] + mass_params['fuel_kg'],  # Min weight (no payload)
            mass_params['operating_empty_kg'] + requirements['total_payload_kg'] + mass_params['fuel_kg'],  # Max weight
            20
        )
        endurance_minutes = []
        
        for weight_kg in weights_kg:
            # Update helicopter weight
            heli.payload_kg = weight_kg - heli.oew_kg - heli.fuel_kg
            
            # Calculate required power for hover (simplified)
            # In hover, thrust equals weight
            required_thrust_N = weight_kg * 9.80665  # Weight in Newtons
            
            # Estimate power required (simplified model)
            # Assume efficiency of 50 N/kW for hover
            required_power_kW = required_thrust_N / 50.0
            
            # Calculate fuel burn rate (kg/hour)
            fuel_rate_kg_per_hour = required_power_kW * engine.sfc_kg_per_kWh
            
            # Calculate endurance (hours)
            if fuel_rate_kg_per_hour > 0:
                endurance_hours = heli.fuel_kg / fuel_rate_kg_per_hour
                endurance_minutes.append(endurance_hours * 60)
            else:
                endurance_minutes.append(0)
        
        plt.figure(figsize=(10, 6))
        plt.plot(weights_kg, endurance_minutes, 'r-', linewidth=2, marker='o', markersize=6)
        plt.xlabel('Gross Weight [kg]', fontsize=12)
        plt.ylabel('Hover Endurance [minutes]', fontsize=12)
        plt.title('Hover Endurance vs Gross Weight', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('individual_design/hover_endurance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved hover_endurance.png")
        
    except Exception as e:
        print(f"✗ Error creating hover endurance plot: {e}")

def main():
    """Main function to generate all individual design plots"""
    print("INDIVIDUAL DESIGN PLOTS GENERATOR")
    print("="*50)
    print("Creating plots similar to report_output folder...")
    
    # Create all plots
    create_thrust_torque_vs_pitch_plots()
    create_thrust_vs_power_plot()
    create_blade_count_variation_plot()
    create_taper_ratio_variation_plot()
    create_twist_variation_plot()
    create_fuel_burn_rate_plot()
    create_hover_endurance_plot()
    
    print("\n✓ All individual design plots have been generated!")
    print("Plots saved in: individual_design/")

if __name__ == "__main__":
    main()