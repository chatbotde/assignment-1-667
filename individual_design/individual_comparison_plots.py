#!/usr/bin/env python3
"""
Individual Helicopter Design Comparison Plots
Creates plots comparing experimental data with calculated values for the individual helicopter design
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import json

# Add path for flight simulation
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))

# Flight simulation imports
from rotor import Rotor
from blade import Blade
from airfoil import Airfoil
from integrators import cycle_integrator

def load_individual_experimental_data(filename):
    """Load experimental data for individual helicopter design"""
    csv_file = f"individual_design/{filename}"
    
    if not os.path.exists(csv_file):
        print(f"Warning: {csv_file} not found")
        return None
    
    try:
        data = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(data)} experimental points from {filename}")
        return data
    except Exception as e:
        print(f"✗ Error loading {csv_file}: {e}")
        return None

def load_helicopter_design():
    """Load the compound helicopter design parameters"""
    json_file = "individual_design/compound_helicopter_design.json"
    
    if not os.path.exists(json_file):
        print(f"Warning: {json_file} not found")
        return None
    
    try:
        with open(json_file, 'r') as f:
            design = json.load(f)
        print("✓ Loaded helicopter design parameters")
        return design
    except Exception as e:
        print(f"✗ Error loading {json_file}: {e}")
        return None

def run_individual_simulation_sweep(theta_range, rotor_config):
    """Run simulation for individual helicopter design at different collective pitch angles"""
    print(f"Running simulation sweep for {rotor_config['name']}...")
    
    try:
        # Create airfoil (using typical NACA 0012 parameters)
        airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25, alpha_stall_deg=15.0)
        
        # Create blade with individual design parameters
        blade = Blade(
            R_root=rotor_config['root_cutout_m'],
            R_tip=rotor_config['radius_m'],
            c_root=rotor_config['chord_root_m'],
            c_tip=rotor_config['chord_tip_m'],
            theta_root_rad=0,  # Will be varied
            theta_tip_rad=0,   # Will be varied
            airfoil=airfoil
        )
        
        # Create rotor
        rotor = Rotor(B=rotor_config['num_blades'], blade=blade)
        
        # Simulation conditions (using sea level ISA)
        rho = 1.225  # kg/m³
        rpm = rotor_config['rpm']
        omega = 2 * math.pi * rpm / 60.0
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
        
        print(f"✓ Completed simulation for {len(theta_range)} pitch angles")
        return results
    
    except Exception as e:
        print(f"✗ Simulation sweep failed: {e}")
        return None

def create_multi_comparison_plots():
    """Create comparison plots using multiple data sets"""
    print("Creating multi-comparison plots for individual helicopter design...")
    
    try:
        # Load helicopter design
        design = load_helicopter_design()
        if not design:
            print("No helicopter design available")
            return
        
        # Define rotor configurations
        rotor_configs = [
            {
                'name': 'Main Rotor',
                'radius_m': design['main_rotor']['radius_m'],
                'rpm': design['main_rotor']['rpm'],
                'num_blades': design['main_rotor']['num_blades'],
                'chord_root_m': design['main_rotor']['chord_root_m'],
                'chord_tip_m': design['main_rotor']['chord_tip_m'],
                'root_cutout_m': design['main_rotor']['root_cutout_m']
            },
            {
                'name': 'Tail Rotor',
                'radius_m': design['tail_rotor']['radius_m'],
                'rpm': design['tail_rotor']['rpm'],
                'num_blades': design['tail_rotor']['num_blades'],
                'chord_root_m': design['tail_rotor']['chord_root_m'],
                'chord_tip_m': design['tail_rotor']['chord_tip_m'],
                'root_cutout_m': design['tail_rotor']['root_cutout_m']
            },
            {
                'name': 'Pusher Propeller',
                'radius_m': design['pusher_propeller']['radius_m'],
                'rpm': design['pusher_propeller']['rpm'],
                'num_blades': design['pusher_propeller']['num_blades'],
                'chord_root_m': design['pusher_propeller']['chord_root_m'],
                'chord_tip_m': design['pusher_propeller']['chord_tip_m'],
                'root_cutout_m': design['pusher_propeller']['root_cutout_m']
            }
        ]
        
        # Load experimental data sets
        data_sets = [
            {'filename': 'rotor_data_set1.csv', 'label': 'Main Rotor Data'},
            {'filename': 'rotor_data_set2.csv', 'label': 'Tail Rotor Data'},
            {'filename': 'rotor_data_set3.csv', 'label': 'Propeller Data'}
        ]
        
        # Create plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        colors = ['blue', 'red', 'green']
        
        for i, (data_set, rotor_config, color) in enumerate(zip(data_sets, rotor_configs, colors)):
            # Load experimental data
            exp_data = load_individual_experimental_data(data_set['filename'])
            if exp_data is None:
                continue
            
            # Run simulation at experimental pitch angles
            theta_range = exp_data['theta_deg']
            sim_data = run_individual_simulation_sweep(theta_range, rotor_config)
            if sim_data is None:
                continue
            
            # CT comparison
            axes[0].plot(exp_data['theta_deg'], exp_data['CT_exp'], 'o-', color=color, 
                        label=f'{data_set["label"]} (Exp)', markersize=6)
            axes[0].plot(sim_data['theta_deg'], sim_data['CT_sim'], 's--', color=color, 
                        label=f'{data_set["label"]} (Sim)', markersize=6)
            
            # CQ comparison
            axes[1].plot(exp_data['theta_deg'], exp_data['CQ_exp'], 'o-', color=color, 
                        label=f'{data_set["label"]} (Exp)', markersize=6)
            axes[1].plot(sim_data['theta_deg'], sim_data['CQ_sim'], 's--', color=color, 
                        label=f'{data_set["label"]} (Sim)', markersize=6)
            
            # Thrust vs Power
            axes[2].plot(sim_data['P_W'], sim_data['T_N'], 'o-', color=color, 
                        label=f'{data_set["label"]}', markersize=6)
        
        # Format plots
        axes[0].set_xlabel('Collective Pitch (degrees)', fontsize=12)
        axes[0].set_ylabel('Thrust Coefficient (CT)', fontsize=12)
        axes[0].set_title('Thrust Coefficient vs Collective Pitch', fontsize=14)
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        
        axes[1].set_xlabel('Collective Pitch (degrees)', fontsize=12)
        axes[1].set_ylabel('Torque Coefficient (CQ)', fontsize=12)
        axes[1].set_title('Torque Coefficient vs Collective Pitch', fontsize=14)
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()
        
        axes[2].set_xlabel('Power (W)', fontsize=12)
        axes[2].set_ylabel('Thrust (N)', fontsize=12)
        axes[2].set_title('Thrust vs Power', fontsize=14)
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()
        
        # Remove the empty subplot
        fig.delaxes(axes[3])
        
        plt.tight_layout()
        plt.savefig('individual_design/multi_rotor_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved multi_rotor_comparison.png")
        
    except Exception as e:
        print(f"✗ Error creating multi-comparison plots: {e}")

def create_individual_comparison_plots():
    """Create comparison plots for individual helicopter design"""
    print("Creating comparison plots for individual helicopter design...")
    
    try:
        # Load experimental data
        exp_data = load_individual_experimental_data('exp_individual.csv')
        if exp_data is None:
            print("No experimental data available")
            return
        
        # Load helicopter design
        design = load_helicopter_design()
        if not design:
            print("No helicopter design available")
            return
        
        # Define main rotor configuration
        main_rotor_config = {
            'name': 'Main Rotor',
            'radius_m': design['main_rotor']['radius_m'],
            'rpm': design['main_rotor']['rpm'],
            'num_blades': design['main_rotor']['num_blades'],
            'chord_root_m': design['main_rotor']['chord_root_m'],
            'chord_tip_m': design['main_rotor']['chord_tip_m'],
            'root_cutout_m': design['main_rotor']['root_cutout_m']
        }
        
        # Run simulation at experimental pitch angles
        theta_range = exp_data['theta_deg']
        sim_data = run_individual_simulation_sweep(theta_range, main_rotor_config)
        if sim_data is None:
            print("Simulation failed")
            return
        
        # Create plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # CT comparison
        ax1.plot(exp_data['theta_deg'], exp_data['CT_exp'], 'bo-', label='Experimental', markersize=6)
        ax1.plot(sim_data['theta_deg'], sim_data['CT_sim'], 'rs--', label='Simulated', markersize=6)
        ax1.set_xlabel('Collective Pitch (degrees)', fontsize=12)
        ax1.set_ylabel('Thrust Coefficient (CT)', fontsize=12)
        ax1.set_title('Thrust Coefficient vs Collective Pitch', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # CQ comparison
        ax2.plot(exp_data['theta_deg'], exp_data['CQ_exp'], 'bo-', label='Experimental', markersize=6)
        ax2.plot(sim_data['theta_deg'], sim_data['CQ_sim'], 'rs--', label='Simulated', markersize=6)
        ax2.set_xlabel('Collective Pitch (degrees)', fontsize=12)
        ax2.set_ylabel('Torque Coefficient (CQ)', fontsize=12)
        ax2.set_title('Torque Coefficient vs Collective Pitch', fontsize=14)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('individual_design/individual_thrust_torque_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved individual_thrust_torque_comparison.png")
        
        # Create additional plot: Thrust vs Power
        plt.figure(figsize=(8, 6))
        plt.plot(sim_data['P_W'], sim_data['T_N'], 'ro-', markersize=6)
        plt.xlabel('Power (W)', fontsize=12)
        plt.ylabel('Thrust (N)', fontsize=12)
        plt.title('Thrust vs Power for Individual Design', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('individual_design/individual_thrust_vs_power.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved individual_thrust_vs_power.png")
        
    except Exception as e:
        print(f"✗ Error creating comparison plots: {e}")

def main():
    """Main function to generate all comparison plots"""
    print("Individual Helicopter Design Comparison Plots Generator")
    print("=" * 55)
    
    create_individual_comparison_plots()
    create_multi_comparison_plots()
    
    print("\nDone! Check the individual_design folder for generated plots.")

if __name__ == "__main__":
    main()