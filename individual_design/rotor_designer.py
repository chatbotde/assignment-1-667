#!/usr/bin/env python3
"""
Rotor Designer Module
Handles design of main rotor, tail rotor, pusher propeller, and wings
"""


class RotorDesigner:
    def __init__(self):
        """Initialize rotor designer"""
        pass
    
    def design_main_rotor(self):
        """Design the main rotor"""
        print("\nDesigning main rotor...")
        
        main_rotor = {
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
        
        print(f"  Main rotor: {main_rotor['radius_m']}m radius, {main_rotor['num_blades']} blades")
        return main_rotor

    def design_tail_rotor(self):
        """Design the tail rotor"""
        print("Designing tail rotor...")
        
        tail_rotor = {
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
        
        print(f"  Tail rotor: {tail_rotor['radius_m']}m radius, {tail_rotor['num_blades']} blades")
        return tail_rotor

    def design_pusher_propeller(self):
        """Design the pusher propeller for high-speed flight"""
        print("Designing pusher propeller...")
        
        pusher_prop = {
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
        
        print(f"  Pusher prop: {pusher_prop['radius_m']}m radius, {pusher_prop['num_blades']} blades")
        return pusher_prop

    def design_wings(self):
        """Design wings for rotor unloading"""
        print("Designing wings...")
        
        wings = {
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
        
        print(f"  Wings: {wings['span_m']}m span, {wings['area_m2']:.1f}m² area")
        return wings