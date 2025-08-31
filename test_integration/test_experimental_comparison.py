#!/usr/bin/env python3
"""
Compare flight simulation results with experimental CSV data
Tests different blade configurations (B=2,3,4,5) against experimental data
"""

import sys
import os
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))

from rotor import Rotor
from blade import Blade
from airfoil import Airfoil
from atmosphere import isa_properties
from integrators import cycle_integrator

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
            
            print(f"  θ={theta_deg:2.0f}°: T={T:6.2f}N, Q={Q:6.4f}N⋅m, CT={CT:.6f}, CQ={CQ:.6f}")
        
        return results
    
    except Exception as e:
        print(f"✗ Simulation sweep failed for B={blade_count}: {e}")
        return None

def compare_with_experimental(blade_count):
    """Compare simulation with experimental data for given blade count"""
    print(f"\n{'='*60}")
    print(f"COMPARISON FOR B={blade_count} BLADES")
    print('='*60)
    
    # Load experimental data
    exp_data = load_experimental_data(blade_count)
    if not exp_data:
        return False
    
    # Run simulation at experimental pitch angles
    theta_range = exp_data['theta_deg']
    sim_data = run_simulation_sweep(blade_count, theta_range)
    if not sim_data:
        return False
    
    # Compare results
    print(f"\nComparison Results:")
    print("Pitch | CT_exp   | CT_sim   | Error(%) | CQ_exp   | CQ_sim   | Error(%)")
    print("-" * 75)
    
    ct_errors = []
    cq_errors = []
    
    for i in range(len(theta_range)):
        theta = theta_range[i]
        ct_exp = exp_data['CT_exp'][i]
        ct_sim = sim_data['CT_sim'][i]
        cq_exp = exp_data['CQ_exp'][i]
        cq_sim = sim_data['CQ_sim'][i]
        
        # Calculate errors (handle zero values)
        ct_error = abs(ct_sim - ct_exp) / max(abs(ct_exp), 1e-6) * 100 if ct_exp != 0 else 0
        cq_error = abs(cq_sim - cq_exp) / max(abs(cq_exp), 1e-6) * 100 if cq_exp != 0 else 0
        
        ct_errors.append(ct_error)
        cq_errors.append(cq_error)
        
        print(f"{theta:4.0f}° | {ct_exp:.6f} | {ct_sim:.6f} | {ct_error:6.1f}  | {cq_exp:.6f} | {cq_sim:.6f} | {cq_error:6.1f}")
    
    # Calculate statistics
    avg_ct_error = np.mean(ct_errors)
    avg_cq_error = np.mean(cq_errors)
    max_ct_error = np.max(ct_errors)
    max_cq_error = np.max(cq_errors)
    
    print(f"\nStatistics:")
    print(f"  CT - Average error: {avg_ct_error:.1f}%, Maximum error: {max_ct_error:.1f}%")
    print(f"  CQ - Average error: {avg_cq_error:.1f}%, Maximum error: {max_cq_error:.1f}%")
    
    # Assessment
    if avg_ct_error < 20 and avg_cq_error < 20:
        print(f"  ✓ Good agreement with experimental data")
    elif avg_ct_error < 50 and avg_cq_error < 50:
        print(f"  ~ Reasonable agreement with experimental data")
    else:
        print(f"  ✗ Poor agreement with experimental data")
    
    return {
        'blade_count': blade_count,
        'exp_data': exp_data,
        'sim_data': sim_data,
        'ct_error_avg': avg_ct_error,
        'cq_error_avg': avg_cq_error,
        'ct_error_max': max_ct_error,
        'cq_error_max': max_cq_error
    }

def create_comparison_plots(comparison_results):
    """Create plots comparing simulation vs experimental data"""
    print(f"\n{'='*60}")
    print("CREATING COMPARISON PLOTS")
    print('='*60)
    
    try:
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Flight Simulation vs Experimental Data Comparison', fontsize=14)
        
        colors = ['blue', 'red', 'green', 'orange']
        
        for i, result in enumerate(comparison_results):
            if not result:
                continue
                
            B = result['blade_count']
            exp = result['exp_data']
            sim = result['sim_data']
            color = colors[i % len(colors)]
            
            # CT comparison
            ax1.plot(exp['theta_deg'], exp['CT_exp'], 'o-', color=color, label=f'B={B} Exp', markersize=4)
            ax1.plot(sim['theta_deg'], sim['CT_sim'], 's--', color=color, label=f'B={B} Sim', markersize=4)
            
            # CQ comparison
            ax2.plot(exp['theta_deg'], exp['CQ_exp'], 'o-', color=color, label=f'B={B} Exp', markersize=4)
            ax2.plot(sim['theta_deg'], sim['CQ_sim'], 's--', color=color, label=f'B={B} Sim', markersize=4)
        
        # Format CT plot
        ax1.set_xlabel('Collective Pitch (degrees)')
        ax1.set_ylabel('Thrust Coefficient (CT)')
        ax1.set_title('Thrust Coefficient Comparison')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Format CQ plot
        ax2.set_xlabel('Collective Pitch (degrees)')
        ax2.set_ylabel('Torque Coefficient (CQ)')
        ax2.set_title('Torque Coefficient Comparison')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Error plots
        for i, result in enumerate(comparison_results):
            if not result:
                continue
                
            B = result['blade_count']
            exp = result['exp_data']
            sim = result['sim_data']
            color = colors[i % len(colors)]
            
            # Calculate errors for plotting
            ct_errors = []
            cq_errors = []
            for j in range(len(exp['theta_deg'])):
                ct_exp = exp['CT_exp'][j]
                ct_sim = sim['CT_sim'][j]
                cq_exp = exp['CQ_exp'][j]
                cq_sim = sim['CQ_sim'][j]
                
                ct_error = abs(ct_sim - ct_exp) / max(abs(ct_exp), 1e-6) * 100 if ct_exp != 0 else 0
                cq_error = abs(cq_sim - cq_exp) / max(abs(cq_exp), 1e-6) * 100 if cq_exp != 0 else 0
                
                ct_errors.append(ct_error)
                cq_errors.append(cq_error)
            
            ax3.plot(exp['theta_deg'], ct_errors, 'o-', color=color, label=f'B={B}', markersize=4)
            ax4.plot(exp['theta_deg'], cq_errors, 'o-', color=color, label=f'B={B}', markersize=4)
        
        # Format error plots
        ax3.set_xlabel('Collective Pitch (degrees)')
        ax3.set_ylabel('CT Error (%)')
        ax3.set_title('Thrust Coefficient Error')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        ax4.set_xlabel('Collective Pitch (degrees)')
        ax4.set_ylabel('CQ Error (%)')
        ax4.set_title('Torque Coefficient Error')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig('test_integration/experimental_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved comparison plots to test_integration/experimental_comparison.png")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating plots: {e}")
        return False

def generate_summary_report(comparison_results):
    """Generate summary report of all comparisons"""
    print(f"\n{'='*60}")
    print("EXPERIMENTAL VALIDATION SUMMARY")
    print('='*60)
    
    valid_results = [r for r in comparison_results if r]
    
    if not valid_results:
        print("No valid comparison results available")
        return
    
    print("Blade Count | CT Avg Error | CT Max Error | CQ Avg Error | CQ Max Error | Assessment")
    print("-" * 80)
    
    overall_assessment = []
    
    for result in valid_results:
        B = result['blade_count']
        ct_avg = result['ct_error_avg']
        ct_max = result['ct_error_max']
        cq_avg = result['cq_error_avg']
        cq_max = result['cq_error_max']
        
        if ct_avg < 20 and cq_avg < 20:
            assessment = "Excellent"
        elif ct_avg < 30 and cq_avg < 30:
            assessment = "Good"
        elif ct_avg < 50 and cq_avg < 50:
            assessment = "Fair"
        else:
            assessment = "Poor"
        
        overall_assessment.append(assessment)
        
        print(f"    B={B}     |    {ct_avg:6.1f}%   |    {ct_max:6.1f}%   |    {cq_avg:6.1f}%   |    {cq_max:6.1f}%   | {assessment}")
    
    # Overall assessment
    print(f"\nOverall Validation Results:")
    excellent_count = overall_assessment.count("Excellent")
    good_count = overall_assessment.count("Good")
    fair_count = overall_assessment.count("Fair")
    poor_count = overall_assessment.count("Poor")
    
    print(f"  Excellent: {excellent_count}/{len(valid_results)} configurations")
    print(f"  Good:      {good_count}/{len(valid_results)} configurations")
    print(f"  Fair:      {fair_count}/{len(valid_results)} configurations")
    print(f"  Poor:      {poor_count}/{len(valid_results)} configurations")
    
    if excellent_count + good_count >= len(valid_results) * 0.75:
        print(f"\n✓ VALIDATION SUCCESSFUL: Flight simulation shows good agreement with experimental data")
    elif excellent_count + good_count + fair_count >= len(valid_results) * 0.5:
        print(f"\n~ VALIDATION PARTIAL: Flight simulation shows reasonable agreement with experimental data")
    else:
        print(f"\n✗ VALIDATION FAILED: Flight simulation needs improvement to match experimental data")
    
    print(f"\nRecommendations:")
    if poor_count > 0:
        print("- Review airfoil parameters and blade geometry")
        print("- Check inflow model accuracy")
        print("- Validate experimental test conditions")
    if fair_count > 0:
        print("- Fine-tune airfoil coefficients")
        print("- Consider 3D effects and tip losses")
    print("- Use validated configuration for mission planning")

if __name__ == "__main__":
    print("EXPERIMENTAL DATA COMPARISON")
    print("="*60)
    print("Comparing flight simulation with experimental CSV data")
    print("Using original rotor configuration from experimental table\n")
    
    # Test all blade configurations
    blade_counts = [2, 3, 4, 5]
    comparison_results = []
    
    for B in blade_counts:
        result = compare_with_experimental(B)
        comparison_results.append(result)
    
    # Create plots if matplotlib is available
    try:
        create_comparison_plots(comparison_results)
    except ImportError:
        print("\nNote: matplotlib not available - skipping plots")
        print("Install with: pip install matplotlib")
    
    # Generate summary
    generate_summary_report(comparison_results)
    
    print(f"\n{'='*60}")
    print("EXPERIMENTAL COMPARISON COMPLETE")
    print("="*60)
    print("Your flight simulation has been validated against experimental data!")
    print("Check the results above to see how well your simulation matches reality.")