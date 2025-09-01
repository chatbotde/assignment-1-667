#!/usr/bin/env python3
"""
Aircraft Sizer Module
Handles overall aircraft sizing and mass breakdown
"""


class AircraftSizer:
    def __init__(self):
        """Initialize aircraft sizer"""
        pass
    
    def size_aircraft(self, requirements, main_rotor, tail_rotor, pusher_prop, wings):
        """Size the overall aircraft"""
        print("Sizing aircraft...")
        
        # Mass breakdown
        mass_breakdown = {
            "payload_kg": requirements["total_payload_kg"],
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
        
        mass_breakdown["empty_weight_kg"] = sum([
            mass_breakdown[key] for key in mass_breakdown.keys() 
            if key not in ["payload_kg", "crew_kg", "fuel_kg"]
        ])
        
        mass_breakdown["operating_empty_kg"] = (
            mass_breakdown["empty_weight_kg"] + 
            mass_breakdown["crew_kg"]
        )
        
        mass_breakdown["max_takeoff_kg"] = sum(mass_breakdown.values()) - mass_breakdown["empty_weight_kg"]
        
        # Dimensions
        dimensions = {
            "length_m": 18.5,
            "height_m": 4.8,
            "width_m": 2.8,
            "main_rotor_diameter_m": main_rotor["radius_m"] * 2,
            "tail_rotor_diameter_m": tail_rotor["radius_m"] * 2
        }
        
        print(f"  Max takeoff weight: {mass_breakdown['max_takeoff_kg']:.0f} kg")
        print(f"  Overall length: {dimensions['length_m']:.1f} m")
        
        return mass_breakdown, dimensions
    
    def calculate_component_masses(self, main_rotor, tail_rotor, pusher_prop, wings):
        """Calculate component masses based on sizing"""
        # Rotor mass estimation (simplified)
        main_rotor_mass = self._estimate_rotor_mass(main_rotor)
        tail_rotor_mass = self._estimate_rotor_mass(tail_rotor)
        pusher_prop_mass = self._estimate_propeller_mass(pusher_prop)
        wings_mass = self._estimate_wing_mass(wings)
        
        return {
            "main_rotor_kg": main_rotor_mass,
            "tail_rotor_kg": tail_rotor_mass,
            "pusher_prop_kg": pusher_prop_mass,
            "wings_kg": wings_mass
        }
    
    def _estimate_rotor_mass(self, rotor_config):
        """Estimate rotor mass based on configuration"""
        # Simplified mass estimation
        disk_area = 3.14159 * rotor_config["radius_m"]**2
        return disk_area * rotor_config["num_blades"] * 2.5  # kg per m² per blade
    
    def _estimate_propeller_mass(self, prop_config):
        """Estimate propeller mass"""
        disk_area = 3.14159 * prop_config["radius_m"]**2
        return disk_area * prop_config["num_blades"] * 1.5  # kg per m² per blade
    
    def _estimate_wing_mass(self, wing_config):
        """Estimate wing mass"""
        return wing_config["area_m2"] * 8.0  # kg per m²