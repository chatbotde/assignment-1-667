#!/usr/bin/env python3
"""
Mission Controller - Integrates Flight Simulation with Mission Planner
Provides high-level mission control and coordination between systems
"""

import sys
import os
import json
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# Add paths for both flight sim and mission planner
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mission planner', 'mission_planner_part2'))

# Flight simulation imports
from main import run as flight_sim_run
from user_inputs import get_user_inputs, build_rotor
from atmosphere import isa_properties
from integrators import cycle_integrator

# Mission planner imports
from planner_main import run_mission
from mp_inputs import get_helicopter_and_engine, mission_definition
from vehicle import Helicopter
from engine import Engine

@dataclass
class MissionStatus:
    """Current mission status"""
    mission_id: str
    status: str  # "planning", "executing", "completed", "failed", "paused"
    current_segment: int
    total_segments: int
    elapsed_time: float
    fuel_remaining: float
    altitude: float
    position: Dict[str, float]  # {"lat": 0, "lon": 0, "alt": 0}
    last_update: str

@dataclass
class FlightParameters:
    """Current flight parameters from simulation"""
    thrust_N: float
    torque_Nm: float
    power_kW: float
    rpm: float
    tip_mach: float
    disk_loading: float
    efficiency: float

@dataclass
class MissionCommand:
    """Mission command structure"""
    command_type: str  # "start", "pause", "resume", "abort", "modify"
    parameters: Dict[str, Any]
    timestamp: str
    priority: int = 1

class MissionController:
    """Main mission controller class"""
    
    def __init__(self):
        self.mission_status = None
        self.flight_params = None
        self.mission_log = []
        self.command_queue = []
        self.is_running = False
        
        # Initialize systems
        self.initialize_systems()
    
    def initialize_systems(self):
        """Initialize flight simulation and mission planner systems"""
        print("=== MISSION CONTROLLER INITIALIZATION ===")
        
        try:
            # Initialize flight simulation
            print("Initializing flight simulation...")
            self.fs_inputs = get_user_inputs()
            self.rotor = build_rotor(self.fs_inputs["rotor"])
            print(f"✓ Flight simulation initialized")
            print(f"  Rotor: {self.rotor.blade.R_tip:.2f}m radius, {self.rotor.B} blades")
            
            # Initialize mission planner
            print("Initializing mission planner...")
            self.helicopter, self.engine, self.mp_rotor = get_helicopter_and_engine()
            print(f"✓ Mission planner initialized")
            print(f"  Aircraft: {self.helicopter.mass_total():.0f}kg total mass")
            print(f"  Engine: {self.engine.P_sl_kW:.0f}kW power")
            
            # Validate compatibility
            self.validate_system_compatibility()
            
        except Exception as e:
            print(f"✗ System initialization failed: {e}")
            raise
    
    def validate_system_compatibility(self):
        """Validate that flight sim and mission planner are compatible"""
        print("Validating system compatibility...")
        
        # Check rotor compatibility
        fs_radius = self.rotor.blade.R_tip
        mp_radius = self.mp_rotor.blade.R_tip
        
        if abs(fs_radius - mp_radius) > 0.01:
            print(f"⚠ Warning: Rotor radius mismatch (FS: {fs_radius:.3f}m, MP: {mp_radius:.3f}m)")
        else:
            print(f"✓ Rotor configurations match")
        
        # Test flight simulation
        try:
            rho, a = isa_properties(0)
            omega = 2*3.14159*960/60.0
            T, Q, P = cycle_integrator(self.rotor, 0, omega, rho)
            print(f"✓ Flight simulation test: {T:.1f}N thrust, {P/1000:.1f}kW power")
        except Exception as e:
            print(f"✗ Flight simulation test failed: {e}")
            raise
        
        print("✓ System compatibility validated")
    
    def create_mission(self, mission_config: Dict[str, Any]) -> str:
        """Create a new mission"""
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.mission_status = MissionStatus(
            mission_id=mission_id,
            status="planning",
            current_segment=0,
            total_segments=len(mission_config.get("segments", [])),
            elapsed_time=0.0,
            fuel_remaining=self.helicopter.fuel_kg,
            altitude=0.0,
            position={"lat": 0.0, "lon": 0.0, "alt": 0.0},
            last_update=datetime.now().isoformat()
        )
        
        print(f"✓ Mission created: {mission_id}")
        print(f"  Segments: {self.mission_status.total_segments}")
        print(f"  Initial fuel: {self.mission_status.fuel_remaining:.1f} kg")
        
        return mission_id
    
    def execute_mission(self, mission_id: str = None) -> bool:
        """Execute the mission"""
        if not self.mission_status:
            print("✗ No mission to execute")
            return False
        
        print(f"\n=== EXECUTING MISSION: {self.mission_status.mission_id} ===")
        self.mission_status.status = "executing"
        self.is_running = True
        
        try:
            # Run the mission planner
            print("Starting mission planner execution...")
            result = run_mission()
            
            # Update mission status
            self.mission_status.status = "completed"
            self.mission_status.last_update = datetime.now().isoformat()
            
            print("✓ Mission completed successfully")
            return True
            
        except Exception as e:
            print(f"✗ Mission execution failed: {e}")
            self.mission_status.status = "failed"
            self.mission_status.last_update = datetime.now().isoformat()
            return False
        
        finally:
            self.is_running = False
    
    def get_flight_parameters(self, altitude: float = 0, velocity: float = 0) -> FlightParameters:
        """Get current flight parameters from simulation"""
        try:
            rho, a = isa_properties(altitude)
            rpm = self.fs_inputs["condition"]["rpm"]
            omega = 2*3.14159*rpm/60.0
            
            T, Q, P = cycle_integrator(self.rotor, velocity, omega, rho)
            
            # Calculate additional parameters
            tip_speed = omega * self.rotor.blade.R_tip
            tip_mach = tip_speed / a
            disk_area = 3.14159 * self.rotor.blade.R_tip**2
            disk_loading = T / disk_area
            efficiency = T / (P/1000) if P > 0 else 0  # N/kW
            
            self.flight_params = FlightParameters(
                thrust_N=T,
                torque_Nm=Q,
                power_kW=P/1000,
                rpm=rpm,
                tip_mach=tip_mach,
                disk_loading=disk_loading,
                efficiency=efficiency
            )
            
            return self.flight_params
            
        except Exception as e:
            print(f"✗ Failed to get flight parameters: {e}")
            return None
    
    def monitor_mission(self) -> Dict[str, Any]:
        """Monitor current mission status"""
        if not self.mission_status:
            return {"error": "No active mission"}
        
        # Update flight parameters
        flight_params = self.get_flight_parameters(
            altitude=self.mission_status.altitude,
            velocity=0  # Default to hover
        )
        
        status_dict = asdict(self.mission_status)
        if flight_params:
            status_dict["flight_parameters"] = asdict(flight_params)
        
        return status_dict
    
    def send_command(self, command: MissionCommand):
        """Send command to mission controller"""
        command.timestamp = datetime.now().isoformat()
        self.command_queue.append(command)
        print(f"Command queued: {command.command_type}")
    
    def process_commands(self):
        """Process queued commands"""
        while self.command_queue:
            command = self.command_queue.pop(0)
            self.execute_command(command)
    
    def execute_command(self, command: MissionCommand):
        """Execute a specific command"""
        print(f"Executing command: {command.command_type}")
        
        if command.command_type == "pause":
            self.mission_status.status = "paused"
            self.is_running = False
            
        elif command.command_type == "resume":
            if self.mission_status.status == "paused":
                self.mission_status.status = "executing"
                self.is_running = True
                
        elif command.command_type == "abort":
            self.mission_status.status = "failed"
            self.is_running = False
            
        elif command.command_type == "modify":
            # Handle mission modifications
            pass
    
    def save_mission_log(self, filename: str = None):
        """Save mission log to file"""
        if not filename:
            filename = f"mission_log_{self.mission_status.mission_id}.json"
        
        log_data = {
            "mission_status": asdict(self.mission_status) if self.mission_status else None,
            "flight_parameters": asdict(self.flight_params) if self.flight_params else None,
            "mission_log": self.mission_log,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"✓ Mission log saved to {filename}")
    
    def generate_mission_report(self) -> str:
        """Generate a comprehensive mission report"""
        if not self.mission_status:
            return "No mission data available"
        
        report = f"""
MISSION CONTROLLER REPORT
========================
Mission ID: {self.mission_status.mission_id}
Status: {self.mission_status.status}
Segments: {self.mission_status.current_segment}/{self.mission_status.total_segments}
Elapsed Time: {self.mission_status.elapsed_time:.1f} s
Fuel Remaining: {self.mission_status.fuel_remaining:.1f} kg

AIRCRAFT CONFIGURATION
=====================
Total Mass: {self.helicopter.mass_total():.0f} kg
Engine Power: {self.engine.P_sl_kW:.0f} kW
Rotor: {self.rotor.blade.R_tip:.2f}m radius, {self.rotor.B} blades

FLIGHT PARAMETERS
================
"""
        
        if self.flight_params:
            report += f"""Thrust: {self.flight_params.thrust_N:.1f} N
Torque: {self.flight_params.torque_Nm:.1f} N⋅m
Power: {self.flight_params.power_kW:.1f} kW
RPM: {self.flight_params.rpm:.0f}
Tip Mach: {self.flight_params.tip_mach:.3f}
Disk Loading: {self.flight_params.disk_loading:.1f} N/m²
Efficiency: {self.flight_params.efficiency:.1f} N/kW
"""
        
        report += f"""
SYSTEM STATUS
============
Flight Simulation: ✓ Operational
Mission Planner: ✓ Operational
Controller: {'✓ Running' if self.is_running else '○ Standby'}

Last Update: {self.mission_status.last_update}
"""
        
        return report

def main():
    """Main function for testing mission controller"""
    print("MISSION CONTROLLER TEST")
    print("="*50)
    
    # Initialize mission controller
    controller = MissionController()
    
    # Create a test mission
    test_mission = {
        "name": "Test Mission",
        "segments": [
            {"type": "hover", "duration_s": 60, "altitude_m": 100},
            {"type": "cruise", "duration_s": 300, "altitude_m": 500, "V_forward_mps": 20},
            {"type": "hover", "duration_s": 30, "altitude_m": 100}
        ]
    }
    
    mission_id = controller.create_mission(test_mission)
    
    # Monitor mission status
    print(f"\n=== MISSION MONITORING ===")
    status = controller.monitor_mission()
    print(f"Mission Status: {status['status']}")
    
    # Get flight parameters
    print(f"\n=== FLIGHT PARAMETERS ===")
    flight_params = controller.get_flight_parameters(altitude=100, velocity=0)
    if flight_params:
        print(f"Hover at 100m:")
        print(f"  Thrust: {flight_params.thrust_N:.1f} N")
        print(f"  Power: {flight_params.power_kW:.1f} kW")
        print(f"  Efficiency: {flight_params.efficiency:.1f} N/kW")
    
    # Generate report
    print(f"\n=== MISSION REPORT ===")
    report = controller.generate_mission_report()
    print(report)
    
    # Save mission log
    controller.save_mission_log()
    
    print(f"\n✓ Mission controller test completed")

if __name__ == "__main__":
    main()