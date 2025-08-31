#!/usr/bin/env python3
"""
Mission Controller Interface - High-level API for mission operations
Provides simple functions for creating, executing, and monitoring missions
"""

import sys
import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Import mission controller
from mission_controller import MissionController, MissionCommand, MissionStatus

class MissionInterface:
    """High-level interface for mission operations"""
    
    def __init__(self):
        self.controller = MissionController()
        self.active_missions = {}
    
    def create_simple_mission(self, mission_type: str = "test") -> str:
        """Create a simple predefined mission"""
        
        missions = {
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
        
        if mission_type not in missions:
            raise ValueError(f"Unknown mission type: {mission_type}. Available: {list(missions.keys())}")
        
        mission_config = missions[mission_type]
        mission_id = self.controller.create_mission(mission_config)
        self.active_missions[mission_id] = mission_config
        
        print(f"✓ Created {mission_type} mission: {mission_id}")
        print(f"  Description: {mission_config['description']}")
        print(f"  Segments: {len(mission_config['segments'])}")
        
        return mission_id
    
    def create_custom_mission(self, segments: List[Dict[str, Any]], name: str = "Custom Mission") -> str:
        """Create a custom mission from segment list"""
        
        mission_config = {
            "name": name,
            "description": "Custom user-defined mission",
            "segments": segments
        }
        
        # Validate segments
        self.validate_mission_segments(segments)
        
        mission_id = self.controller.create_mission(mission_config)
        self.active_missions[mission_id] = mission_config
        
        print(f"✓ Created custom mission: {mission_id}")
        print(f"  Segments: {len(segments)}")
        
        return mission_id
    
    def validate_mission_segments(self, segments: List[Dict[str, Any]]):
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
    
    def execute_mission(self, mission_id: str) -> bool:
        """Execute a mission"""
        if mission_id not in self.active_missions:
            print(f"✗ Mission {mission_id} not found")
            return False
        
        print(f"Executing mission: {mission_id}")
        return self.controller.execute_mission(mission_id)
    
    def get_mission_status(self, mission_id: str = None) -> Dict[str, Any]:
        """Get current mission status"""
        return self.controller.monitor_mission()
    
    def pause_mission(self):
        """Pause current mission"""
        command = MissionCommand("pause", {})
        self.controller.send_command(command)
        self.controller.process_commands()
    
    def resume_mission(self):
        """Resume paused mission"""
        command = MissionCommand("resume", {})
        self.controller.send_command(command)
        self.controller.process_commands()
    
    def abort_mission(self):
        """Abort current mission"""
        command = MissionCommand("abort", {})
        self.controller.send_command(command)
        self.controller.process_commands()
    
    def get_flight_performance(self, altitude: float = 0, velocity: float = 0) -> Dict[str, float]:
        """Get flight performance at specified conditions"""
        params = self.controller.get_flight_parameters(altitude, velocity)
        if params:
            return {
                "thrust_N": params.thrust_N,
                "power_kW": params.power_kW,
                "efficiency_N_per_kW": params.efficiency,
                "tip_mach": params.tip_mach,
                "disk_loading_N_per_m2": params.disk_loading,
                "rpm": params.rpm
            }
        return {}
    
    def analyze_mission_feasibility(self, mission_id: str) -> Dict[str, Any]:
        """Analyze if a mission is feasible"""
        if mission_id not in self.active_missions:
            return {"error": "Mission not found"}
        
        mission = self.active_missions[mission_id]
        segments = mission["segments"]
        
        analysis = {
            "feasible": True,
            "issues": [],
            "warnings": [],
            "performance": {}
        }
        
        # Analyze each segment
        for i, segment in enumerate(segments):
            seg_type = segment["type"]
            
            if seg_type in ["hover", "cruise", "loiter"]:
                alt = segment.get("altitude_m", 0)
                vel = segment.get("V_forward_mps", segment.get("V_loiter_mps", 0))
                
                # Get performance at this condition
                perf = self.get_flight_performance(alt, vel)
                
                if perf:
                    analysis["performance"][f"segment_{i}"] = perf
                    
                    # Check for issues
                    if perf["tip_mach"] > 0.85:
                        analysis["warnings"].append(f"Segment {i}: High tip Mach ({perf['tip_mach']:.3f})")
                    
                    if perf["power_kW"] > self.controller.engine.P_sl_kW * 0.9:
                        analysis["issues"].append(f"Segment {i}: Power requirement too high ({perf['power_kW']:.1f} kW)")
                        analysis["feasible"] = False
        
        # Overall assessment
        if analysis["issues"]:
            analysis["feasible"] = False
        
        return analysis
    
    def generate_mission_summary(self, mission_id: str) -> str:
        """Generate a mission summary"""
        if mission_id not in self.active_missions:
            return "Mission not found"
        
        mission = self.active_missions[mission_id]
        status = self.get_mission_status()
        
        summary = f"""
MISSION SUMMARY
==============
Mission: {mission['name']}
ID: {mission_id}
Description: {mission['description']}
Status: {status.get('status', 'Unknown')}

SEGMENTS ({len(mission['segments'])}):
"""
        
        for i, segment in enumerate(mission["segments"]):
            seg_type = segment["type"]
            duration = segment.get("duration_s", 0)
            
            summary += f"  {i+1}. {seg_type.upper()}"
            
            if seg_type == "hover":
                summary += f" at {segment['altitude_m']}m for {duration}s"
            elif seg_type == "cruise":
                summary += f" at {segment['altitude_m']}m, {segment['V_forward_mps']} m/s for {duration}s"
            elif seg_type == "vclimb":
                summary += f" from {segment['start_alt_m']}m at {segment['climb_rate_mps']} m/s for {duration}s"
            elif seg_type == "loiter":
                summary += f" at {segment['altitude_m']}m, {segment['V_loiter_mps']} m/s for {duration}s"
            elif seg_type == "payload":
                summary += f" {segment['kind']} {segment['delta_mass_kg']}kg"
            
            summary += "\n"
        
        # Add feasibility analysis
        feasibility = self.analyze_mission_feasibility(mission_id)
        summary += f"\nFEASIBILITY: {'✓ FEASIBLE' if feasibility['feasible'] else '✗ NOT FEASIBLE'}\n"
        
        if feasibility["issues"]:
            summary += "ISSUES:\n"
            for issue in feasibility["issues"]:
                summary += f"  • {issue}\n"
        
        if feasibility["warnings"]:
            summary += "WARNINGS:\n"
            for warning in feasibility["warnings"]:
                summary += f"  • {warning}\n"
        
        return summary
    
    def list_available_missions(self) -> List[str]:
        """List available predefined mission types"""
        return ["test", "patrol", "search_rescue", "cargo"]
    
    def save_mission(self, mission_id: str, filename: str = None):
        """Save mission configuration to file"""
        if mission_id not in self.active_missions:
            print(f"✗ Mission {mission_id} not found")
            return
        
        if not filename:
            filename = f"{mission_id}_config.json"
        
        with open(filename, 'w') as f:
            json.dump(self.active_missions[mission_id], f, indent=2)
        
        print(f"✓ Mission saved to {filename}")
    
    def load_mission(self, filename: str) -> str:
        """Load mission configuration from file"""
        try:
            with open(filename, 'r') as f:
                mission_config = json.load(f)
            
            mission_id = self.controller.create_mission(mission_config)
            self.active_missions[mission_id] = mission_config
            
            print(f"✓ Mission loaded from {filename}: {mission_id}")
            return mission_id
            
        except Exception as e:
            print(f"✗ Failed to load mission from {filename}: {e}")
            return None

def main():
    """Test the mission interface"""
    print("MISSION INTERFACE TEST")
    print("="*50)
    
    # Create mission interface
    interface = MissionInterface()
    
    # List available missions
    print("Available mission types:", interface.list_available_missions())
    
    # Create a test mission
    print(f"\n=== CREATING TEST MISSION ===")
    mission_id = interface.create_simple_mission("test")
    
    # Get mission summary
    print(f"\n=== MISSION SUMMARY ===")
    summary = interface.generate_mission_summary(mission_id)
    print(summary)
    
    # Analyze feasibility
    print(f"\n=== FEASIBILITY ANALYSIS ===")
    feasibility = interface.analyze_mission_feasibility(mission_id)
    print(f"Feasible: {feasibility['feasible']}")
    if feasibility["issues"]:
        print("Issues:", feasibility["issues"])
    if feasibility["warnings"]:
        print("Warnings:", feasibility["warnings"])
    
    # Test flight performance
    print(f"\n=== FLIGHT PERFORMANCE ===")
    perf_hover = interface.get_flight_performance(altitude=100, velocity=0)
    perf_cruise = interface.get_flight_performance(altitude=200, velocity=20)
    
    print(f"Hover at 100m: {perf_hover['power_kW']:.1f} kW, {perf_hover['efficiency_N_per_kW']:.1f} N/kW")
    print(f"Cruise at 200m, 20 m/s: {perf_cruise['power_kW']:.1f} kW, {perf_cruise['efficiency_N_per_kW']:.1f} N/kW")
    
    # Save mission
    interface.save_mission(mission_id)
    
    print(f"\n✓ Mission interface test completed")

if __name__ == "__main__":
    main()