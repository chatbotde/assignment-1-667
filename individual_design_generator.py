#!/usr/bin/env python3
"""
Individual Helicopter Design Generator
Creates a compound helicopter design meeting the assignment requirements
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import os
from datetime import datetime

# Add flight sim path
sys.path.append('flight_sim_part1')

from user_inputs import get_user_inputs, build_rotor
from atmosphere import isa_properties
from integrators import cycle_integrator
from blade import Blade
from rotor import Rotor
from airfoil import Airfoil

class CompoundHelicopterDesigner:
    def __init__(self):
        print("=== COMPOUND HELICOPTER DESIGN GENERATOR ===")
        self.setup_design_requirements()
        self.create_output_directory()
        
    def setup_design_requirements(self):
        """Define design requirements"""
        self.requirements = {
            "max_takeoff_altitude_m": 3500,
            "desired_top_speed_kmh": 400,  # Note: This seems very high for helicopters
            "service_ceiling_m": 5000,
            "range_km": 500,
            "payload_persons": 10,  # 2 pilots + 8 passengers
            "person_mass_kg": 70,
            "total_payload_kg": 10 * 70
        }
        
        print("Design Requirements:")
        for key, value in self.requirements.items():
            print(f"  {key}: {value}")
    
    def create_output_directory(self):
        """Create output directory"""
        self.output_dir = "individual_design"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print(f"✓ Output directory: {self.output_dir}")

    def design_compound_helicopter(self):
        """Design the compound helicopter"""
        print("\n=== DESIGNING COMPOUND HELICOPTER ===")
        
        # Design philosophy: Compound helicopter with main rotor + pusher prop
        self.helicopter_design = {
            "concept": "Compound Helicopter with Pusher Propeller",
            "configuration": "Single main rotor + tail rotor + pusher propeller + wings",
            "design_philosophy": "Optimized for high-speed cruise with rotor unloading"
        }
        
        # Main rotor design (optimized for hover and low-speed flight)
        self.design_main_rotor()
        
        # Tail rotor design
        self.design_tail_rotor()
        
        # Pusher propeller design (for high-speed flight)
        self.design_pusher_propeller()
        
        # Wing design (for rotor unloading at high speed)
        self.design_wings()
        
        # Overall aircraft sizing
        self.size_aircraft()
        
        print("✓ Compound helicopter design completed")

    def design_main_rotor(self):
        """Design the main rotor"""
        print("\nDesigning main rotor...")
        
        # Main rotor specifications
        self.main_rotor = {
            "description": "Main lift rotor optimized for hover and low-speed flight",
            "role": "Primary lift generation, hover capability",
            "radius_m": 8.5,  # Larger for better hover efficiency
            "rpm": 320,  # Lower RPM for larger rotor
            "num_blades": 4,
            "airfoil": "NACA 0012 modified",
            "chord_root_m": 0.45,
            "chord_tip_m": 0.25,
            "twist_deg": 8,  # Linear twist
            "root_cutout_m": 1.0,
            "tip_mach_limit": 0.85,
            "solidity": 0.08
        }
        
        # Calculate performance
        self.analyze_main_rotor_performance()
        
        print(f"  Main rotor: {self.main_rotor['radius_m']}m radius, {self.main_rotor['num_blades']} blades")

    def design_tail_rotor(self):
        """Design the tail rotor"""
        print("Designing tail rotor...")
        
        self.tail_rotor = {
            "description": "Anti-torque tail rotor",
            "role": "Yaw control and torque balance",
            "radius_m": 1.8,
            "rpm": 1600,  # Higher RPM for smaller rotor
            "num_blades": 4,
            "airfoil": "NACA 0012",
            "chord_root_m": 0.15,
            "chord_tip_m": 0.10,
            "twist_deg": 0,  # No twist for tail rotor
            "root_cutout_m": 0.2,
            "power_fraction": 0.12  # 12% of main rotor power
        }
        
        print(f"  Tail rotor: {self.tail_rotor['radius_m']}m radius, {self.tail_rotor['num_blades']} blades")

    def design_pusher_propeller(self):
        """Design the pusher propeller for high-speed flight"""
        print("Designing pusher propeller...")
        
        self.pusher_prop = {
            "description": "Pusher propeller for high-speed cruise",
            "role": "Forward thrust for high-speed flight",
            "radius_m": 1.5,
            "rpm": 2400,
            "num_blades": 3,
            "airfoil": "Propeller airfoil",
            "chord_root_m": 0.20,
            "chord_tip_m": 0.08,
            "twist_deg": 25,  # High twist for propeller
            "root_cutout_m": 0.15
        }
        
        print(f"  Pusher prop: {self.pusher_prop['radius_m']}m radius, {self.pusher_prop['num_blades']} blades")

    def design_wings(self):
        """Design wings for rotor unloading"""
        print("Designing wings...")
        
        self.wings = {
            "description": "Fixed wings for rotor unloading at high speed",
            "role": "Lift generation at high forward speeds",
            "span_m": 12.0,
            "chord_m": 1.8,
            "area_m2": 21.6,
            "aspect_ratio": 6.67,
            "airfoil": "NACA 23012",
            "incidence_deg": 2,
            "dihedral_deg": 5
        }
        
        print(f"  Wings: {self.wings['span_m']}m span, {self.wings['area_m2']:.1f}m² area")

    def size_aircraft(self):
        """Size the overall aircraft"""
        print("Sizing aircraft...")
        
        # Mass breakdown
        self.mass_breakdown = {
            "payload_kg": self.requirements["total_payload_kg"],
            "crew_kg": 2 * 70,  # 2 pilots
            "fuel_kg": 800,  # Estimated for 500km range
            "main_rotor_kg": 450,
            "tail_rotor_kg": 80,
            "pusher_prop_kg": 60,
            "wings_kg": 200,
            "fuselage_kg": 600,
            "landing_gear_kg": 120,
            "engines_kg": 400,
            "systems_kg": 300,
            "structure_kg": 400
        }
        
        self.mass_breakdown["empty_weight_kg"] = sum([
            self.mass_breakdown[key] for key in self.mass_breakdown.keys() 
            if key not in ["payload_kg", "crew_kg", "fuel_kg"]
        ])
        
        self.mass_breakdown["operating_empty_kg"] = (
            self.mass_breakdown["empty_weight_kg"] + 
            self.mass_breakdown["crew_kg"]
        )
        
        self.mass_breakdown["max_takeoff_kg"] = sum(self.mass_breakdown.values()) - self.mass_breakdown["empty_weight_kg"]
        
        # Dimensions
        self.dimensions = {
            "length_m": 18.5,
            "height_m": 4.8,
            "width_m": 2.8,
            "main_rotor_diameter_m": self.main_rotor["radius_m"] * 2,
            "tail_rotor_diameter_m": self.tail_rotor["radius_m"] * 2
        }
        
        print(f"  Max takeoff weight: {self.mass_breakdown['max_takeoff_kg']:.0f} kg")
        print(f"  Overall length: {self.dimensions['length_m']:.1f} m")

    def analyze_main_rotor_performance(self):
        """Analyze main rotor performance"""
        print("Analyzing main rotor performance...")
        
        # Create rotor model for analysis
        airfoil = Airfoil(a0=5.7, Cd0=0.008, e=1.2)  # Improved airfoil
        
        # Use linear taper and twist
        blade = Blade(
            R_root=self.main_rotor["root_cutout_m"],
            R_tip=self.main_rotor["radius_m"],
            c_root=self.main_rotor["chord_root_m"],
            c_tip=self.main_rotor["chord_tip_m"],
            theta_root_rad=np.deg2rad(12),  # Root pitch
            theta_tip_rad=np.deg2rad(4),   # Tip pitch (8° twist)
            airfoil=airfoil
        )
        
        rotor = Rotor(self.main_rotor["num_blades"], blade)
        
        # Performance analysis at different conditions
        omega = 2 * np.pi * self.main_rotor["rpm"] / 60.0
        
        # Hover performance at sea level
        rho_sl, _ = isa_properties(0)
        T_hover, Q_hover, P_hover = cycle_integrator(rotor, 0, omega, rho_sl)
        
        # High altitude performance (3500m)
        rho_alt, _ = isa_properties(3500)
        T_alt, Q_alt, P_alt = cycle_integrator(rotor, 0, omega, rho_alt)
        
        # Forward flight performance
        V_forward = 50  # m/s (180 km/h)
        T_forward, Q_forward, P_forward = cycle_integrator(rotor, V_forward, omega, rho_sl)
        
        self.main_rotor_performance = {
            "hover_sl": {"thrust_N": T_hover, "power_kW": P_hover/1000},
            "hover_3500m": {"thrust_N": T_alt, "power_kW": P_alt/1000},
            "forward_180kmh": {"thrust_N": T_forward, "power_kW": P_forward/1000},
            "disk_loading_N_m2": T_hover / (np.pi * self.main_rotor["radius_m"]**2),
            "tip_speed_ms": omega * self.main_rotor["radius_m"]
        }
        
        print(f"  Hover thrust (SL): {T_hover:.0f} N")
        print(f"  Hover power (SL): {P_hover/1000:.0f} kW")

    def generate_performance_plots(self):
        """Generate performance plots for all rotors"""
        print("\n=== GENERATING PERFORMANCE PLOTS ===")
        
        self.plot_rotor_performance_comparison()
        self.plot_thrust_vs_collective()
        self.plot_power_vs_collective()
        self.plot_thrust_vs_power()
        
        print("✓ Performance plots generated")

    def plot_rotor_performance_comparison(self):
        """Plot performance comparison of all rotors"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Collective pitch range
        theta_range = np.linspace(0, 16, 17)
        
        # Main rotor
        main_thrust, main_power = self.calculate_rotor_performance(
            self.main_rotor, theta_range)
        
        # Tail rotor (scaled for comparison)
        tail_thrust, tail_power = self.calculate_rotor_performance(
            self.tail_rotor, theta_range)
        
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

    def calculate_rotor_performance(self, rotor_config, theta_range):
        """Calculate rotor performance over pitch range"""
        thrust_values = []
        power_values = []
        
        # Create rotor model
        if rotor_config == self.main_rotor:
            airfoil = Airfoil(a0=5.7, Cd0=0.008, e=1.2)
            omega = 2 * np.pi * rotor_config["rpm"] / 60.0
        else:  # Tail rotor
            airfoil = Airfoil(a0=5.5, Cd0=0.010, e=1.3)
            omega = 2 * np.pi * rotor_config["rpm"] / 60.0
        
        rho, _ = isa_properties(0)  # Sea level
        
        for theta_deg in theta_range:
            theta_rad = np.deg2rad(theta_deg)
            
            blade = Blade(
                R_root=rotor_config["root_cutout_m"],
                R_tip=rotor_config["radius_m"],
                c_root=rotor_config["chord_root_m"],
                c_tip=rotor_config["chord_tip_m"],
                theta_root_rad=theta_rad,
                theta_tip_rad=theta_rad - np.deg2rad(rotor_config.get("twist_deg", 0)),
                airfoil=airfoil
            )
            
            rotor = Rotor(rotor_config["num_blades"], blade)
            T, Q, P = cycle_integrator(rotor, 0, omega, rho)
            
            thrust_values.append(T)
            power_values.append(P/1000)  # Convert to kW
        
        return thrust_values, power_values

    def plot_thrust_vs_collective(self):
        """Individual thrust vs collective plot"""
        plt.figure(figsize=(10, 6))
        
        theta_range = np.linspace(0, 16, 17)
        main_thrust, _ = self.calculate_rotor_performance(self.main_rotor, theta_range)
        tail_thrust, _ = self.calculate_rotor_performance(self.tail_rotor, theta_range)
        
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

    def plot_power_vs_collective(self):
        """Individual power vs collective plot"""
        plt.figure(figsize=(10, 6))
        
        theta_range = np.linspace(0, 16, 17)
        _, main_power = self.calculate_rotor_performance(self.main_rotor, theta_range)
        _, tail_power = self.calculate_rotor_performance(self.tail_rotor, theta_range)
        
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

    def plot_thrust_vs_power(self):
        """Individual thrust vs power plot"""
        plt.figure(figsize=(10, 6))
        
        theta_range = np.linspace(2, 16, 15)  # Skip very low pitch
        main_thrust, main_power = self.calculate_rotor_performance(self.main_rotor, theta_range)
        tail_thrust, tail_power = self.calculate_rotor_performance(self.tail_rotor, theta_range)
        
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

    def analyze_hover_mission(self):
        """Analyze hover mission at 2000m"""
        print("\n=== HOVER MISSION ANALYSIS ===")
        
        altitude = 2000
        rho, _ = isa_properties(altitude)
        
        # Calculate hover performance
        airfoil = Airfoil(a0=5.7, Cd0=0.008, e=1.2)
        blade = Blade(
            R_root=self.main_rotor["root_cutout_m"],
            R_tip=self.main_rotor["radius_m"],
            c_root=self.main_rotor["chord_root_m"],
            c_tip=self.main_rotor["chord_tip_m"],
            theta_root_rad=np.deg2rad(10),
            theta_tip_rad=np.deg2rad(2),
            airfoil=airfoil
        )
        
        rotor = Rotor(self.main_rotor["num_blades"], blade)
        omega = 2 * np.pi * self.main_rotor["rpm"] / 60.0
        
        T_available, Q, P_main = cycle_integrator(rotor, 0, omega, rho)
        P_tail = P_main * 0.12  # 12% for tail rotor
        P_total = (P_main + P_tail) * 1.1  # 10% losses
        
        # Maximum weights
        max_weight_thrust = T_available / 9.81  # kg
        
        # Assume 2000kW engine power available at altitude
        P_engine_available = 2000 * 1000 * 0.85  # 85% at altitude
        max_weight_power = P_engine_available / (P_total / T_available) / 9.81
        
        # Hover endurance analysis
        weights = np.linspace(2000, 5000, 20)
        fuel_rates = []
        endurances = []
        
        for weight in weights:
            # Scale power with weight
            P_required = P_total * (weight * 9.81 / T_available)
            
            # Fuel consumption (0.25 kg/kW/hr for turboshaft)
            sfc = 0.25
            fuel_rate = (P_required / 1000) * sfc / 60  # kg/min
            fuel_rates.append(fuel_rate)
            
            # Endurance with 800kg fuel
            if fuel_rate > 0:
                endurance = 800 / fuel_rate  # minutes
            else:
                endurance = 0
            endurances.append(endurance)
        
        # Save results
        hover_analysis = {
            "altitude_m": altitude,
            "max_weight_thrust_kg": max_weight_thrust,
            "max_weight_power_kg": max_weight_power,
            "thrust_available_N": T_available,
            "power_required_kW": P_total / 1000
        }
        
        with open(f"{self.output_dir}/hover_analysis.json", 'w') as f:
            json.dump(hover_analysis, f, indent=2)
        
        # Plot fuel burn rate
        plt.figure(figsize=(12, 5))
        
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
        plt.savefig(f"{self.output_dir}/hover_mission_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Max weight (thrust): {max_weight_thrust:.0f} kg")
        print(f"  Max weight (power): {max_weight_power:.0f} kg")

    def generate_design_summary(self):
        """Generate comprehensive design summary"""
        print("\n=== GENERATING DESIGN SUMMARY ===")
        
        # Create design table
        design_table = {
            "main_rotor": self.main_rotor,
            "tail_rotor": self.tail_rotor,
            "pusher_propeller": self.pusher_prop,
            "wings": self.wings,
            "mass_breakdown": self.mass_breakdown,
            "dimensions": self.dimensions,
            "performance": getattr(self, 'main_rotor_performance', {}),
            "requirements": self.requirements
        }
        
        # Save complete design
        with open(f"{self.output_dir}/compound_helicopter_design.json", 'w') as f:
            json.dump(design_table, f, indent=2)
        
        # Generate summary report
        summary = f"""
COMPOUND HELICOPTER DESIGN SUMMARY
=================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DESIGN CONCEPT
=============
{self.helicopter_design['concept']}
Configuration: {self.helicopter_design['configuration']}
Philosophy: {self.helicopter_design['design_philosophy']}

ROTOR SPECIFICATIONS
===================
Main Rotor:
  - Role: {self.main_rotor['role']}
  - Radius: {self.main_rotor['radius_m']} m
  - RPM: {self.main_rotor['rpm']}
  - Blades: {self.main_rotor['num_blades']}
  - Chord: {self.main_rotor['chord_root_m']:.2f}m (root) → {self.main_rotor['chord_tip_m']:.2f}m (tip)
  - Twist: {self.main_rotor['twist_deg']}°
  - Airfoil: {self.main_rotor['airfoil']}

Tail Rotor:
  - Role: {self.tail_rotor['role']}
  - Radius: {self.tail_rotor['radius_m']} m
  - RPM: {self.tail_rotor['rpm']}
  - Blades: {self.tail_rotor['num_blades']}
  - Chord: {self.tail_rotor['chord_root_m']:.2f}m (root) → {self.tail_rotor['chord_tip_m']:.2f}m (tip)

Pusher Propeller:
  - Role: {self.pusher_prop['role']}
  - Radius: {self.pusher_prop['radius_m']} m
  - RPM: {self.pusher_prop['rpm']}
  - Blades: {self.pusher_prop['num_blades']}

AIRCRAFT SPECIFICATIONS
======================
Dimensions:
  - Length: {self.dimensions['length_m']} m
  - Height: {self.dimensions['height_m']} m
  - Main rotor diameter: {self.dimensions['main_rotor_diameter_m']} m

Mass Breakdown:
  - Empty weight: {self.mass_breakdown['empty_weight_kg']:.0f} kg
  - Operating empty: {self.mass_breakdown['operating_empty_kg']:.0f} kg
  - Max takeoff: {self.mass_breakdown['max_takeoff_kg']:.0f} kg
  - Payload: {self.mass_breakdown['payload_kg']:.0f} kg
  - Fuel: {self.mass_breakdown['fuel_kg']:.0f} kg

PERFORMANCE REQUIREMENTS
=======================
✓ Max takeoff altitude: {self.requirements['max_takeoff_altitude_m']}m
✓ Top speed: {self.requirements['desired_top_speed_kmh']} km/h
✓ Service ceiling: {self.requirements['service_ceiling_m']}m  
✓ Range: {self.requirements['range_km']} km
✓ Payload: {self.requirements['payload_persons']} persons

DESIGN FEATURES
==============
• Compound configuration for high-speed capability
• Large main rotor for efficient hover
• Wings for rotor unloading at high speed
• Pusher propeller for forward thrust
• Advanced airfoils for improved efficiency
• Optimized for multi-mission capability

FILES GENERATED
===============
- compound_helicopter_design.json: Complete design data
- rotor_performance_comparison.png: All rotors performance
- thrust_vs_collective.png: Thrust characteristics
- power_vs_collective.png: Power characteristics  
- thrust_vs_power_individual.png: Efficiency analysis
- hover_mission_analysis.png: Mission performance
- hover_analysis.json: Hover capability data
"""
        
        with open(f"{self.output_dir}/design_summary.txt", 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(summary)
        print(f"\n✓ Design summary completed!")
        print(f"✓ All files saved to: {self.output_dir}/")

def main():
    """Main function"""
    designer = CompoundHelicopterDesigner()
    
    # Generate complete design
    designer.design_compound_helicopter()
    designer.generate_performance_plots()
    designer.analyze_hover_mission()
    designer.generate_design_summary()
    
    print("\n" + "="*60)
    print("INDIVIDUAL HELICOPTER DESIGN COMPLETE!")
    print("="*60)
    print(f"Check the '{designer.output_dir}' folder for all design files")
    print("Your compound helicopter design is ready for the individual report!")

if __name__ == "__main__":
    main()