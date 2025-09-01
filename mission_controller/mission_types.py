#!/usr/bin/env python3
"""
Mission Controller Mission Types
Predefined mission configurations and validation
"""

from typing import List, Dict, Any

class MissionTypes:
    """Handles predefined mission types and validation"""
    
    @staticmethod
    def get_predefined_missions() -> Dict[str, Dict[str, Any]]:
        """Get all predefined mission configurations"""
        return {
            "test": {
                "name": "Test Mission",
                "description": "Simple test mission for validation",
                "segments": [
                    {"type": "hover", "duration_s": 30, "altitude_m": 50},
                    {"type": "cruise", "duration_s": 120, "altitude_m": 200, "V_forward_mps": 15},
                    {"type": "hover", "duration_s": 30, "altitude_m": 50}
                ]
            },
            
            "patrol": {
                "name": "Patrol Mission",
                "description": "Standard patrol mission",
                "segments": [
                    {"type": "vclimb", "duration_s": 60, "start_alt_m": 0, "climb_rate_mps": 5},
                    {"type": "cruise", "duration_s": 600, "altitude_m": 300, "V_forward_mps": 25},
                    {"type": "loiter", "duration_s": 300, "altitude_m": 300, "V_loiter_mps": 10},
                    {"type": "cruise", "duration_s": 600, "altitude_m": 300, "V_forward_mps": 25},
                    {"type": "hover", "duration_s": 60, "altitude_m": 0}
                ]
            },
            
            "search_rescue": {
                "name": "Search and Rescue",
                "description": "Search and rescue mission pattern",
                "segments": [
                    {"type": "vclimb", "duration_s": 90, "start_alt_m": 0, "climb_rate_mps": 3},
                    {"type": "cruise", "duration_s": 300, "altitude_m": 150, "V_forward_mps": 20},
                    {"type": "loiter", "duration_s": 600, "altitude_m": 150, "V_loiter_mps": 8},
                    {"type": "hover", "duration_s": 120, "altitude_m": 150},
                    {"type": "payload", "kind": "pickup", "delta_mass_kg": 75, "duration_hover_s": 60, "altitude_m": 150},
                    {"type": "cruise", "duration_s": 300, "altitude_m": 150, "V_forward_mps": 15},
                    {"type": "hover", "duration_s": 60, "altitude_m": 0}
                ]
            },
            
            "cargo": {
                "name": "Cargo Transport",
                "description": "Cargo transport mission",
                "segments": [
                    {"type": "payload", "kind": "pickup", "delta_mass_kg": 200, "duration_hover_s": 120, "altitude_m": 0},
                    {"type": "vclimb", "duration_s": 120, "start_alt_m": 0, "climb_rate_mps": 2.5},
                    {"type": "cruise", "duration_s": 900, "altitude_m": 300, "V_forward_mps": 30},
                    {"type": "hover", "duration_s": 60, "altitude_m": 300},
                    {"type": "payload", "kind": "drop", "delta_mass_kg": -200, "duration_hover_s": 120, "altitude_m": 300},
                    {"type": "cruise", "duration_s": 900, "altitude_m": 300, "V_forward_mps": 35},
                    {"type": "hover", "duration_s": 60, "altitude_m": 0}
                ]
            }
        }
    
    @staticmethod
    def validate_mission_segments(segments: List[Dict[str, Any]]):
        """Validate mission segments"""
        valid_types = ["hover", "vclimb", "fclimb", "cruise", "loiter", "payload"]
        
        for i, segment in enumerate(segments):
            if "type" not in segment:
                raise ValueError(f"Segment {i}: Missing 'type' field")
            
            seg_type = segment["type"]
            if seg_type not in valid_types:
                raise ValueError(f"Segment {i}: Invalid type '{seg_type}'. Valid types: {valid_types}")
            
            # Type-specific validation
            if seg_type == "hover":
                required = ["duration_s", "altitude_m"]
            elif seg_type == "vclimb":
                required = ["duration_s", "start_alt_m", "climb_rate_mps"]
            elif seg_type == "fclimb":
                required = ["duration_s", "start_alt_m", "climb_rate_mps", "V_forward_mps"]
            elif seg_type == "cruise":
                required = ["duration_s", "altitude_m", "V_forward_mps"]
            elif seg_type == "loiter":
                required = ["duration_s", "altitude_m", "V_loiter_mps"]
            elif seg_type == "payload":
                required = ["kind", "delta_mass_kg"]
            
            for field in required:
                if field not in segment:
                    raise ValueError(f"Segment {i} ({seg_type}): Missing required field '{field}'")
        
        print("✓ Mission segments validated")
    
    @staticmethod
    def list_available_missions() -> List[str]:
        """List available predefined mission types"""
        return list(MissionTypes.get_predefined_missions().keys())