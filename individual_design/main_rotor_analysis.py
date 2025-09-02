#!/usr/bin/env python3
"""
Main Rotor Performance Analysis
Detailed analysis of main rotor performance comparing experimental and simulated data
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

def load_experimental_data():
    """Load experimental data for main rotor"""
    csv_file = "individual_design/main_rotor_exp_data.csv"
    
    if not os.path.exists(csv_file):
        print(f"Warning: {csv_file} not found")
        return None
    
    try:
        data = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(data)} experimental points for main rotor")
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

def run_main_rotor_simulation(theta_range):
    """Run simulation for main rotor at different collective pitch angles"""
    print("Running main rotor simulation...")
    
    try:
        # Load helicopter design
        design = load_helicopter_design()
        if not design:
            return None
        
        # Extract main rotor parameters
        main_rotor = design['main_rotor']
        
        # Create airfoil (using typical NACA 0012 parameters)
        airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25, alpha_stall_deg=15.0)
        
        # Create blade with individual design parameters
        blade = Blade(
            R_root=main_rotor['root_cutout_m'],
            R_tip=main_rotor['radius_m'],
            c_root=main_rotor['chord_root_m'],
            c_tip=main_rotor['chord_tip_m'],
            theta_root_rad=0,  # Will be varied
            theta_tip_rad=0,   # Will be varied
            airfoil=airfoil
        )
        
        # Create rotor
        rotor = Rotor(B=main_rotor['num_blades'], blade=blade)
        
        # Simulation conditions (using sea level ISA)
        rho = 1.225  # kg/m³
        rpm = main_rotor['rpm']
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
        print(f"✗ Simulation failed: {e}")
        return None

def calculate_error_metrics(exp_data, sim_data):
    """Calculate error metrics between experimental and simulated data"""
    ct_exp = exp_data['CT_exp']
    cq_exp = exp_data['CQ_exp']
    ct_sim = sim_data['CT_sim']
    cq_sim = sim_data['CQ_sim']
    
    # Calculate mean absolute error
    ct_mae = np.mean(np.abs(np.array(ct_exp) - np.array(ct_sim)))
    cq_mae = np.mean(np.abs(np.array(cq_exp) - np.array(cq_sim)))
    
    # Calculate root mean square error
    ct_rmse = np.sqrt(np.mean((np.array(ct_exp) - np.array(ct_sim))**2))
    cq_rmse = np.sqrt(np.mean((np.array(cq_exp) - np.array(cq_sim))**2))
    
    # Calculate mean relative error (percentage)
    ct_mre = np.mean(np.abs((np.array(ct_exp) - np.array(ct_sim)) / np.array(ct_exp))) * 100
    cq_mre = np.mean(np.abs((np.array(cq_exp) - np.array(cq_sim)) / np.array(cq_exp))) * 100
    
    return {
        'CT_MAE': ct_mae,
        'CQ_MAE': cq_mae,
        'CT_RMSE': ct_rmse,
        'CQ_RMSE': cq_rmse,
        'CT_MRE_percent': ct_mre,
        'CQ_MRE_percent': cq_mre
    }

def create_detailed_comparison_plots():
    """Create detailed comparison plots with error analysis"""
    print("Creating detailed comparison plots...")
    
    try:
        # Load experimental data
        exp_data = load_experimental_data()
        if exp_data is None:
            print("No experimental data available")
            return
        
        # Run simulation at experimental pitch angles
        theta_range = exp_data['theta_deg']
        sim_data = run_main_rotor_simulation(theta_range)
        if sim_data is None:
            print("Simulation failed")
            return
        
        # Calculate error metrics
        error_metrics = calculate_error_metrics(exp_data, sim_data)
        
        # Create detailed plots
        fig = plt.figure(figsize=(20, 15))
        
        # Plot 1: CT comparison
        ax1 = plt.subplot(3, 2, 1)
        ax1.plot(exp_data['theta_deg'], exp_data['CT_exp'], 'bo-', label='Experimental', markersize=8)
        ax1.plot(sim_data['theta_deg'], sim_data['CT_sim'], 'rs--', label='Simulated', markersize=8)
        ax1.set_xlabel('Collective Pitch (degrees)', fontsize=12)
        ax1.set_ylabel('Thrust Coefficient (CT)', fontsize=12)
        ax1.set_title('Thrust Coefficient vs Collective Pitch', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: CQ comparison
        ax2 = plt.subplot(3, 2, 2)
        ax2.plot(exp_data['theta_deg'], exp_data['CQ_exp'], 'bo-', label='Experimental', markersize=8)
        ax2.plot(sim_data['theta_deg'], sim_data['CQ_sim'], 'rs--', label='Simulated', markersize=8)
        ax2.set_xlabel('Collective Pitch (degrees)', fontsize=12)
        ax2.set_ylabel('Torque Coefficient (CQ)', fontsize=12)
        ax2.set_title('Torque Coefficient vs Collective Pitch', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Plot 3: Thrust vs Power
        ax3 = plt.subplot(3, 2, 3)
        ax3.plot(sim_data['P_W'], sim_data['T_N'], 'ro-', markersize=8)
        ax3.set_xlabel('Power (W)', fontsize=12)
        ax3.set_ylabel('Thrust (N)', fontsize=12)
        ax3.set_title('Thrust vs Power Characteristic', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Error analysis - CT error
        ax4 = plt.subplot(3, 2, 4)
        ct_error = np.array(exp_data['CT_exp']) - np.array(sim_data['CT_sim'])
        ax4.bar(exp_data['theta_deg'], ct_error, color='orange', alpha=0.7)
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax4.set_xlabel('Collective Pitch (degrees)', fontsize=12)
        ax4.set_ylabel('CT Error (Exp - Sim)', fontsize=12)
        ax4.set_title('Thrust Coefficient Error Distribution', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        # Plot 5: Error analysis - CQ error
        ax5 = plt.subplot(3, 2, 5)
        cq_error = np.array(exp_data['CQ_exp']) - np.array(sim_data['CQ_sim'])
        ax5.bar(exp_data['theta_deg'], cq_error, color='purple', alpha=0.7)
        ax5.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax5.set_xlabel('Collective Pitch (degrees)', fontsize=12)
        ax5.set_ylabel('CQ Error (Exp - Sim)', fontsize=12)
        ax5.set_title('Torque Coefficient Error Distribution', fontsize=14, fontweight='bold')
        ax5.grid(True, alpha=0.3)
        
        # Plot 6: Error metrics summary
        ax6 = plt.subplot(3, 2, 6)
        ax6.axis('off')
        metrics_text = f"""
Error Metrics Summary:
======================
CT Mean Absolute Error:     {error_metrics['CT_MAE']:.6f}
CQ Mean Absolute Error:     {error_metrics['CQ_MAE']:.6f}
CT Root Mean Square Error:  {error_metrics['CT_RMSE']:.6f}
CQ Root Mean Square Error:  {error_metrics['CQ_RMSE']:.6f}
CT Mean Relative Error:     {error_metrics['CT_MRE_percent']:.2f}%
CQ Mean Relative Error:     {error_metrics['CQ_MRE_percent']:.2f}%
        """
        ax6.text(0.1, 0.5, metrics_text, fontsize=12, verticalalignment='center', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        ax6.set_title('Performance Metrics', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('individual_design/main_rotor_detailed_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved main_rotor_detailed_analysis.png")
        
        # Save error metrics to a text file
        with open('individual_design/main_rotor_error_metrics.txt', 'w') as f:
            f.write("Main Rotor Performance Error Metrics\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"CT Mean Absolute Error:     {error_metrics['CT_MAE']:.6f}\n")
            f.write(f"CQ Mean Absolute Error:     {error_metrics['CQ_MAE']:.6f}\n")
            f.write(f"CT Root Mean Square Error:  {error_metrics['CT_RMSE']:.6f}\n")
            f.write(f"CQ Root Mean Square Error:  {error_metrics['CQ_RMSE']:.6f}\n")
            f.write(f"CT Mean Relative Error:     {error_metrics['CT_MRE_percent']:.2f}%\n")
            f.write(f"CQ Mean Relative Error:     {error_metrics['CQ_MRE_percent']:.2f}%\n")
        
        print("✓ Saved main_rotor_error_metrics.txt")
        
    except Exception as e:
        print(f"✗ Error creating detailed comparison plots: {e}")

def main():
    """Main function to generate detailed analysis"""
    print("Main Rotor Performance Detailed Analysis")
    print("=" * 40)
    
    create_detailed_comparison_plots()
    
    print("\nDone! Check the individual_design folder for generated analysis files.")

if __name__ == "__main__":
    main()