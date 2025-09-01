#!/usr/bin/env python3
"""
Plot Generator Module
Handles all plotting and visualization tasks
"""

import numpy as np
import matplotlib.pyplot as plt
from .performance_analyzer import PerformanceAnalyzer


class PlotGenerator:
    def __init__(self):
        """Initialize plot generator"""
        self.performance_analyzer = PerformanceAnalyzer()
        self.output_dir = "individual_design"
    
    def set_output_dir(self, output_dir):
        """Set output directory for plots"""
        self.output_dir = output_dir
    
    def plot_rotor_performance_comparison(self, main_rotor, tail_rotor):
        """Plot performance comparison of all rotors"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Collective pitch range
        theta_range = np.linspace(0, 16, 17)
        
        # Main rotor
        main_thrust, main_power = self.performance_analyzer.calculate_rotor_performance(
            main_rotor, theta_range)
        
        # Tail rotor (scaled for comparison)
        tail_thrust, tail_power = self.performance_analyzer.calculate_rotor_performance(
            tail_rotor, theta_range)
        
        # Plot thrust vs collective
        ax1.plot(theta_range, main_thrust, 'b-o', label='Main Rotor', linewidth=2)
        ax1.plot(theta_range, np.array(tail_thrust)*5, 'r-s', label='Tail Rotor (×5)', linewidth=2)
        ax1.set_xlabel('Collective Pitch θ₀ [deg]')
        ax1.set_ylabel('Thrust [N]')
        ax1.set_title('Thrust vs Collective Pitch')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot power vs collective
        ax2.plot(theta_range, main_power, 'b-o', label='Main Rotor', linewidth=2)
        ax2.plot(theta_range, tail_power, 'r-s', label='Tail Rotor', linewidth=2)
        ax2.set_xlabel('Collective Pitch θ₀ [deg]')
        ax2.set_ylabel('Power [kW]')
        ax2.set_title('Power vs Collective Pitch')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot thrust vs power
        ax3.plot(main_power, main_thrust, 'b-o', label='Main Rotor', linewidth=2)
        ax3.plot(tail_power, np.array(tail_thrust), 'r-s', label='Tail Rotor', linewidth=2)
        ax3.set_xlabel('Power [kW]')
        ax3.set_ylabel('Thrust [N]')
        ax3.set_title('Thrust vs Power')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot efficiency
        main_eff = np.array(main_thrust) / np.array(main_power)
        tail_eff = np.array(tail_thrust) / np.array(tail_power)
        ax4.plot(theta_range, main_eff, 'b-o', label='Main Rotor', linewidth=2)
        ax4.plot(theta_range, tail_eff, 'r-s', label='Tail Rotor', linewidth=2)
        ax4.set_xlabel('Collective Pitch θ₀ [deg]')
        ax4.set_ylabel('Efficiency [N/kW]')
        ax4.set_title('Efficiency vs Collective Pitch')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/rotor_performance_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()

    def plot_thrust_vs_collective(self, main_rotor, tail_rotor):
        """Individual thrust vs collective plot"""
        plt.figure(figsize=(10, 6))
        
        theta_range = np.linspace(0, 16, 17)
        main_thrust, _ = self.performance_analyzer.calculate_rotor_performance(main_rotor, theta_range)
        tail_thrust, _ = self.performance_analyzer.calculate_rotor_performance(tail_rotor, theta_range)
        
        plt.plot(theta_range, main_thrust, 'b-o', label='Main Rotor', linewidth=2, markersize=6)
        plt.plot(theta_range, tail_thrust, 'r-s', label='Tail Rotor', linewidth=2, markersize=6)
        
        plt.xlabel('Collective Pitch θ₀ [deg]', fontsize=12)
        plt.ylabel('Thrust [N]', fontsize=12)
        plt.title('Thrust vs Collective Pitch\nCompound Helicopter Rotors', fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/thrust_vs_collective.png", dpi=300, bbox_inches='tight')
        plt.close()

    def plot_power_vs_collective(self, main_rotor, tail_rotor):
        """Individual power vs collective plot"""
        plt.figure(figsize=(10, 6))
        
        theta_range = np.linspace(0, 16, 17)
        _, main_power = self.performance_analyzer.calculate_rotor_performance(main_rotor, theta_range)
        _, tail_power = self.performance_analyzer.calculate_rotor_performance(tail_rotor, theta_range)
        
        plt.plot(theta_range, main_power, 'b-o', label='Main Rotor', linewidth=2, markersize=6)
        plt.plot(theta_range, tail_power, 'r-s', label='Tail Rotor', linewidth=2, markersize=6)
        
        plt.xlabel('Collective Pitch θ₀ [deg]', fontsize=12)
        plt.ylabel('Power [kW]', fontsize=12)
        plt.title('Power vs Collective Pitch\nCompound Helicopter Rotors', fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/power_vs_collective.png", dpi=300, bbox_inches='tight')
        plt.close()

    def plot_thrust_vs_power(self, main_rotor, tail_rotor):
        """Individual thrust vs power plot"""
        plt.figure(figsize=(10, 6))
        
        theta_range = np.linspace(2, 16, 15)  # Skip very low pitch
        main_thrust, main_power = self.performance_analyzer.calculate_rotor_performance(main_rotor, theta_range)
        tail_thrust, tail_power = self.performance_analyzer.calculate_rotor_performance(tail_rotor, theta_range)
        
        plt.plot(main_power, main_thrust, 'b-o', label='Main Rotor', linewidth=2, markersize=6)
        plt.plot(tail_power, tail_thrust, 'r-s', label='Tail Rotor', linewidth=2, markersize=6)
        
        plt.xlabel('Power [kW]', fontsize=12)
        plt.ylabel('Thrust [N]', fontsize=12)
        plt.title('Thrust vs Power\nCompound Helicopter Rotors', fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/thrust_vs_power_individual.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_hover_mission_analysis(self, hover_results, output_dir):
        """Plot hover mission analysis results"""
        plt.figure(figsize=(12, 5))
        
        weights = hover_results["weights"]
        fuel_rates = hover_results["fuel_rates"]
        endurances = hover_results["endurances"]
        altitude = hover_results["altitude_m"]
        
        plt.subplot(1, 2, 1)
        plt.plot(weights, fuel_rates, 'b-', linewidth=2)
        plt.xlabel('Gross Weight [kg]')
        plt.ylabel('Fuel Burn Rate [kg/min]')
        plt.title(f'Fuel Burn Rate vs Weight\nHover at {altitude}m AMSL')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.plot(weights, endurances, 'r-', linewidth=2)
        plt.xlabel('Take-Off Weight [kg]')
        plt.ylabel('Hover Endurance [min]')
        plt.title(f'Hover Endurance vs Weight\nAt {altitude}m AMSL')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/hover_mission_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()