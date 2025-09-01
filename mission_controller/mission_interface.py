#!/usr/bin/env python3
"""
Mission Controller Interface - High-level API for mission operations
Provides simple functions for creating, executing, and monitoring missions
"""

import json
from typing import List, Dict, Any

# Import modular components
from .mission_controller import MissionController
from .core import MissionCommand
from .mission_types import MissionTypes
from .feasibility_analyzer import FeasibilityAnalyzer

class MissionInterface:
    """High-level interface for mission operations"""
    
    def __init__(self):
        self.controller = MissionController()
        self.active_missions = {}
        self.feasibility_analyzer = FeasibilityAnalyzer(
            self.controller.flight_analyzer, 
            self.controller.engine
        )
    
    def create_simple_mission(self, mission_type: str = "test") -> str:
        """Create a simple predefined mission"""
        missions = MissionTypes.get_predefined_missions()
        
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
        MissionTypes.validate_mission_segments(segments)
        
        mission_id = self.controller.create_mission(mission_config)
        self.active_missions[mission_id] = mission_config
        
        print(f"✓ Created custom mission: {mission_id}")
        print(f"  Segments: {len(segments)}")
        
        return mission_id
    
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
        command = MissionCommand("pause", {}, "")
        self.controller.send_command(command)
        self.controller.process_commands()
    
    def resume_mission(self):
        """Resume paused mission"""
        command = MissionCommand("resume", {}, "")
        self.controller.send_command(command)
        self.controller.process_commands()
    
    def abort_mission(self):
        """Abort current mission"""
        command = MissionCommand("abort", {}, "")
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
        
        return self.feasibility_analyzer.analyze_mission_feasibility(self.active_missions[mission_id])
    
    def generate_mission_summary(self, mission_id: str) -> str:
        """Generate a mission summary"""
        if mission_id not in self.active_missions:
            return "Mission not found"
        
        status = self.get_mission_status()
        return self.feasibility_analyzer.generate_mission_summary(
            self.active_missions[mission_id], mission_id, status
        )
    
    def list_available_missions(self) -> List[str]:
        """List available predefined mission types"""
        return MissionTypes.list_available_missions()
    
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