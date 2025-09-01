#!/usr/bin/env python3
"""
Design Requirements Module
Defines and manages helicopter design requirements
"""


class DesignRequirements:
    def __init__(self):
        """Initialize design requirements"""
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
    
    def get_requirements(self):
        """Get the requirements dictionary"""
        return self.requirements
    
    def update_requirement(self, key, value):
        """Update a specific requirement"""
        if key in self.requirements:
            self.requirements[key] = value
            print(f"Updated {key}: {value}")
        else:
            print(f"Warning: {key} is not a valid requirement")
    
    def validate_requirements(self):
        """Validate that all requirements are reasonable"""
        warnings = []
        
        if self.requirements["desired_top_speed_kmh"] > 350:
            warnings.append("Top speed >350 km/h is very high for helicopters")
        
        if self.requirements["service_ceiling_m"] > 6000:
            warnings.append("Service ceiling >6000m requires special considerations")
        
        if self.requirements["total_payload_kg"] > 1000:
            warnings.append("Payload >1000kg requires large helicopter")
        
        return warnings