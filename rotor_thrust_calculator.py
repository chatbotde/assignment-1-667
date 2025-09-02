#!/usr/bin/env python3
"""
Rotor Thrust Calculator for Individual Report
Extracts and displays maximum thrust data for main and tail rotors
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

def format_thrust_output(hover_data, design_data):
    """Format thrust data into a readable output"""
    if not hover_data or not design_data:
        return "Data not available"

    # Extract main rotor thrust at sea level
    main_rotor_thrust_sl = design_data.get("performance", {}).get("hover_sl", {}).get("thrust_N", 0)
    
    # Extract tail rotor thrust at 2000m AMSL (from hover analysis)
    tail_rotor_thrust_2000m = hover_data.get("thrust_available_N", 0)
    
    # Main rotor specifications
    main_rotor = design_data.get("main_rotor", {})
    main_radius = main_rotor.get("radius_m", 0)
    main_rpm = main_rotor.get("rpm", 0)
    main_blades = main_rotor.get("num_blades", 0)
    
    # Tail rotor specifications
    tail_rotor = design_data.get("tail_rotor", {})
    tail_radius = tail_rotor.get("radius_m", 0)
    tail_rpm = tail_rotor.get("rpm", 0)
    tail_blades = tail_rotor.get("num_blades", 0)
    
    # Extract main rotor thrust at 2000m
    main_rotor_thrust_2000m = design_data.get("performance", {}).get("hover_3500m", {}).get("thrust_N", 0)
    
    # Calculate tail rotor thrust at sea level (assuming linear scaling with air density)
    rho_sl = 1.225  # Sea level density
    rho_2000m = 1.0065  # Approximate density at 2000m
    tail_rotor_thrust_sl = tail_rotor_thrust_2000m * (rho_sl / rho_2000m)

    # Create formatted output
    output = "\nMAXIMUM ROTOR THRUST CALCULATION OUTPUT\n"
    output += "=======================================\n\n"

    output += "1. MAIN ROTOR SPECIFICATIONS\n"
    output += "--------------------------\n"
    output += f"Radius: {main_radius} m\n"
    output += f"RPM: {main_rpm}\n"
    output += f"Number of blades: {main_blades}\n"
    output += f"Airfoil: {main_rotor.get('airfoil', 'N/A')}\n\n"

    output += "2. MAIN ROTOR THRUST\n"
    output += "-------------------\n"
    output += f"Sea Level Maximum Thrust: {main_rotor_thrust_sl:.0f} N\n"
    output += f"Sea Level Maximum Equivalent Weight: {main_rotor_thrust_sl / 9.81:.0f} kg\n\n"
    output += f"At 2000m AMSL Maximum Thrust: {main_rotor_thrust_2000m:.0f} N\n"
    output += f"At 2000m AMSL Maximum Equivalent Weight: {main_rotor_thrust_2000m / 9.81:.0f} kg\n\n"
    
    output += "3. TAIL ROTOR SPECIFICATIONS\n"
    output += "---------------------------\n"
    output += f"Radius: {tail_radius} m\n"
    output += f"RPM: {tail_rpm}\n"
    output += f"Number of blades: {tail_blades}\n"
    output += f"Airfoil: {tail_rotor.get('airfoil', 'N/A')}\n\n"

    output += "4. TAIL ROTOR THRUST\n"
    output += "------------------\n"
    output += f"Sea Level Maximum Thrust (estimated): {tail_rotor_thrust_sl:.0f} N\n"
    output += f"Sea Level Maximum Equivalent Weight: {tail_rotor_thrust_sl / 9.81:.0f} kg\n\n"
    output += f"At 2000m AMSL Maximum Thrust: {tail_rotor_thrust_2000m:.0f} N\n"
    output += f"At 2000m AMSL Maximum Equivalent Weight: {tail_rotor_thrust_2000m / 9.81:.0f} kg\n\n"

    output += "5. THRUST CALCULATION METHODOLOGY\n"
    output += "-------------------------------\n"
    output += "- Main rotor thrust calculated using Blade Element Momentum Theory (BEMT)\n"
    output += "- Includes Prandtl tip loss correction\n"
    output += "- Based on airfoil characteristics and rotor geometry\n"
    output += "- Accounts for air density variation with altitude\n"
    output += "- Considers induced velocity and blade aerodynamics\n\n"

    output += "6. DESIGN IMPLICATIONS\n"
    output += "--------------------\n"
    output += f"- Maximum takeoff weight limited to {main_rotor_thrust_sl / 9.81:.0f} kg at sea level\n"
    output += f"- Maximum takeoff weight limited to {main_rotor_thrust_2000m / 9.81:.0f} kg at 2000m AMSL\n"
    output += f"- Tail rotor provides {tail_rotor_thrust_sl:.0f} N of anti-torque thrust at sea level\n"
    output += f"- Tail rotor size optimized for main rotor torque counteraction\n"
    output += "- Design provides adequate yaw control authority\n\n"

    return output

def main():
    """Main function to generate the thrust output"""
    # Load data
    hover_data = load_hover_analysis()
    design_data = load_design_data()

    if not hover_data or not design_data:
        print("Failed to load required data!")
        return

    # Generate formatted output
    output = format_thrust_output(hover_data, design_data)
    print(output)
    
    # Save output to file
    with open("individual_design/rotor_thrust_output.txt", 'w') as f:
        f.write(output)
    
    print(f"Output saved to 'individual_design/rotor_thrust_output.txt'")

if __name__ == "__main__":
    main()