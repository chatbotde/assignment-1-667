#!/usr/bin/env python3
"""
Individual Report Generator for Helicopter Design
Extracts and displays data specifically for takeoff weight analysis
"""

import json
import os
import sys

def load_hover_analysis():
    """Load hover analysis data from JSON file"""
    try:
        with open("individual_design/hover_analysis.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: hover_analysis.json not found!")
        return None

def load_design_data():
    """Load helicopter design data from JSON file"""
    try:
        with open("individual_design/compound_helicopter_design.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: compound_helicopter_design.json not found!")
        return None

def format_weight_table(hover_data, design_data):
    """Format takeoff weight data into a table"""
    if not hover_data or not design_data:
        return "Data not available"
    
    # Extract data
    altitude = hover_data.get("altitude_m", 2000)
    max_weight_stall = hover_data.get("max_weight_thrust_kg", 0)
    max_weight_power = hover_data.get("max_weight_power_kg", 0)
    
    # Create simple text table
    table = "\n+---------+---------------------------------------------------------+--------------+"
    table += "\n| Plots   | Description                                         | Value        |"
    table += "\n+---------+---------------------------------------------------------+--------------+"
    table += f"\n| 3.1     | Maximum Take Off Weight based on blade stall at {altitude} m AMSL | {max_weight_stall:.0f} kg     |"
    table += f"\n| 3.2     | Maximum Take Off Weight based on power requirement at {altitude} m AMSL | {max_weight_power:.0f} kg    |"
    table += "\n+---------+---------------------------------------------------------+--------------+"
    
    return table

def generate_calculation_outputs(hover_data, design_data):
    """Generate detailed calculation outputs for the report"""
    if not hover_data or not design_data:
        return "Calculation details not available"
    
    # Extract detailed data
    thrust_available = hover_data.get("thrust_available_N", 0)
    power_required = hover_data.get("power_required_kW", 0)
    max_weight_stall = hover_data.get("max_weight_thrust_kg", 0)
    max_weight_power = hover_data.get("max_weight_power_kg", 0)
    
    # Main rotor data
    main_rotor = design_data.get("main_rotor", {})
    radius = main_rotor.get("radius_m", 0)
    num_blades = main_rotor.get("num_blades", 0)
    rpm = main_rotor.get("rpm", 0)
    
    output_3_1 = f"""
3.1 Calculation Output for the Mission planner Code - Blade Stall Limit

Main Rotor Parameters:
- Radius: {radius} m
- Number of blades: {num_blades}
- RPM: {rpm}

Analysis at 2000m AMSL:
- Air density: 1.0065 kg/m³ (ISA standard)
- Maximum thrust available: {thrust_available:.0f} N
- Corresponding weight capacity: {max_weight_stall:.0f} kg
- Limiting factor: Blade stall at high collective pitch
- Safety margin applied: 5%

Notes:
- Calculation uses Blade Element Momentum Theory (BEMT)
- Includes Prandtl tip loss correction
- Based on NACA 0012 modified airfoil characteristics
- Assumes standard atmospheric conditions
"""

    output_3_2 = f"""
3.2 Calculation Output for the Mission planner Code - Power Limit

Engine and Power System:
- Maximum power available: 1350 kW (at sea level)
- Power reduction at 2000m: 17%
- Power available at 2000m: 1120.5 kW
- Power required for hover: {power_required:.0f} kW

Analysis at 2000m AMSL:
- Maximum weight based on power: {max_weight_power:.0f} kg
- Power requirement includes:
  * Main rotor induced power
  * Main rotor profile power
  * Tail rotor power (12% of main rotor)
  * Transmission losses (5%)

Notes:
- Based on momentum theory with empirical corrections
- Includes forward flight capability reserve (10%)
- Calculation accounts for available engine power
- Real-world operations should apply additional safety margins
"""

    return output_3_1, output_3_2

def main():
    """Main function to generate the individual report section"""
    # Load data
    hover_data = load_hover_analysis()
    design_data = load_design_data()
    
    if not hover_data or not design_data:
        print("Failed to load required data!")
        return
    
    # Generate formatted table
    table_html = format_weight_table(hover_data, design_data)
    print("\nTake Off Weight Analysis:\n")
    print(table_html)
    
    # Generate calculation outputs
    output_3_1, output_3_2 = generate_calculation_outputs(hover_data, design_data)
    print("\n" + "-"*80)
    print(output_3_1)
    print("\n" + "-"*80)
    print(output_3_2)
    
    print("\nReport data successfully extracted!")

if __name__ == "__main__":
    main()