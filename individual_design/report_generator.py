#!/usr/bin/env python3
"""
Report Generator Module
Handles generation of design reports and summaries
"""

import json
from datetime import datetime


class ReportGenerator:
    def __init__(self):
        """Initialize report generator"""
        pass
    
    def generate_design_json(self, design_data, output_dir):
        """Generate complete design JSON file"""
        with open(f"{output_dir}/compound_helicopter_design.json", 'w') as f:
            json.dump(design_data, f, indent=2)
    
    def generate_design_summary(self, helicopter_design, design_data, output_dir):
        """Generate comprehensive design summary"""
        main_rotor = design_data["main_rotor"]
        tail_rotor = design_data["tail_rotor"]
        pusher_prop = design_data["pusher_propeller"]
        wings = design_data["wings"]
        mass_breakdown = design_data["mass_breakdown"]
        dimensions = design_data["dimensions"]
        requirements = design_data["requirements"]
        
        summary = f"""
COMPOUND HELICOPTER DESIGN SUMMARY
=================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DESIGN CONCEPT
=============
{helicopter_design['concept']}
Configuration: {helicopter_design['configuration']}
Philosophy: {helicopter_design['design_philosophy']}

ROTOR SPECIFICATIONS
===================
Main Rotor:
  - Role: {main_rotor['role']}
  - Radius: {main_rotor['radius_m']} m
  - RPM: {main_rotor['rpm']}
  - Blades: {main_rotor['num_blades']}
  - Chord: {main_rotor['chord_root_m']:.2f}m (root) → {main_rotor['chord_tip_m']:.2f}m (tip)
  - Twist: {main_rotor['twist_deg']}°
  - Airfoil: {main_rotor['airfoil']}

Tail Rotor:
  - Role: {tail_rotor['role']}
  - Radius: {tail_rotor['radius_m']} m
  - RPM: {tail_rotor['rpm']}
  - Blades: {tail_rotor['num_blades']}
  - Chord: {tail_rotor['chord_root_m']:.2f}m (root) → {tail_rotor['chord_tip_m']:.2f}m (tip)

Pusher Propeller:
  - Role: {pusher_prop['role']}
  - Radius: {pusher_prop['radius_m']} m
  - RPM: {pusher_prop['rpm']}
  - Blades: {pusher_prop['num_blades']}

AIRCRAFT SPECIFICATIONS
======================
Dimensions:
  - Length: {dimensions['length_m']} m
  - Height: {dimensions['height_m']} m
  - Main rotor diameter: {dimensions['main_rotor_diameter_m']} m

Mass Breakdown:
  - Empty weight: {mass_breakdown['empty_weight_kg']:.0f} kg
  - Operating empty: {mass_breakdown['operating_empty_kg']:.0f} kg
  - Max takeoff: {mass_breakdown['max_takeoff_kg']:.0f} kg
  - Payload: {mass_breakdown['payload_kg']:.0f} kg
  - Fuel: {mass_breakdown['fuel_kg']:.0f} kg

PERFORMANCE REQUIREMENTS
=======================
✓ Max takeoff altitude: {requirements['max_takeoff_altitude_m']}m
✓ Top speed: {requirements['desired_top_speed_kmh']} km/h
✓ Service ceiling: {requirements['service_ceiling_m']}m  
✓ Range: {requirements['range_km']} km
✓ Payload: {requirements['payload_persons']} persons

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
        
        with open(f"{output_dir}/design_summary.txt", 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return summary
    
    def generate_performance_report(self, performance_data, output_dir):
        """Generate detailed performance report"""
        report = f"""
HELICOPTER PERFORMANCE ANALYSIS REPORT
=====================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

HOVER PERFORMANCE
================
Sea Level:
  - Thrust: {performance_data.get('hover_sl', {}).get('thrust_N', 'N/A'):.0f} N
  - Power: {performance_data.get('hover_sl', {}).get('power_kW', 'N/A'):.0f} kW

High Altitude (3500m):
  - Thrust: {performance_data.get('hover_3500m', {}).get('thrust_N', 'N/A'):.0f} N
  - Power: {performance_data.get('hover_3500m', {}).get('power_kW', 'N/A'):.0f} kW

FORWARD FLIGHT PERFORMANCE
=========================
At 180 km/h:
  - Thrust: {performance_data.get('forward_180kmh', {}).get('thrust_N', 'N/A'):.0f} N
  - Power: {performance_data.get('forward_180kmh', {}).get('power_kW', 'N/A'):.0f} kW

ROTOR CHARACTERISTICS
====================
  - Disk Loading: {performance_data.get('disk_loading_N_m2', 'N/A'):.1f} N/m²
  - Tip Speed: {performance_data.get('tip_speed_ms', 'N/A'):.1f} m/s
"""
        
        with open(f"{output_dir}/performance_report.txt", 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report