#!/usr/bin/env python3
"""
Mission Controller - Integrates Flight Simulation with Mission Planner
Provides high-level mission control and coordination between systems
"""

from typing import Dict, Any

# Import modular components
from .core import MissionStatus, FlightParameters, MissionCommand
from .system_init import SystemInitializer
from .flight_analysis import FlightAnalyzer
from .mission_executor import MissionExecutor
from .report_generator import ReportGenerator

class MissionController:
    """Main mission controller class"""
    
    def __init__(self):
        # Initialize components
        self.system_init = SystemInitializer()
        self.executor = MissionExecutor()
        
        # Initialize systems
        self.initialize_systems()
        
        # Initialize other components after system init
        self.flight_analyzer = FlightAnalyzer(self.system_init.rotor, self.system_init.fs_inputs)
        self.report_gen = ReportGenerator(
            self.executor.mission_status,
            None,  # flight_params will be updated dynamically
            self.system_init.helicopter,
            self.system_init.engine,
            self.system_init.rotor
        )
    
    def initialize_systems(self):
        """Initialize flight simulation and mission planner systems"""
        self.system_init.initialize_systems()
    
    def create_mission(self, mission_config: Dict[str, Any]) -> str:
        """Create a new mission"""
        mission_id = self.executor.create_mission(mission_config, self.system_init.helicopter)
        # Update report generator with new mission status
        self.report_gen.mission_status = self.executor.mission_status
        return mission_id
    
    def execute_mission(self, mission_id: str = None) -> bool:
        """Execute the mission"""
        return self.executor.execute_mission(mission_id)
    
    def get_flight_parameters(self, altitude: float = 0, velocity: float = 0) -> FlightParameters:
        """Get current flight parameters from simulation"""
        params = self.flight_analyzer.get_flight_parameters(altitude, velocity)
        # Update report generator with new flight params
        self.report_gen.flight_params = params
        return params
    
    def monitor_mission(self) -> Dict[str, Any]:
        """Monitor current mission status"""
        return self.report_gen.monitor_mission()
    
    def send_command(self, command: MissionCommand):
        """Send command to mission controller"""
        self.executor.send_command(command)
    
    def process_commands(self):
        """Process queued commands"""
        self.executor.process_commands()
    
    def save_mission_log(self, filename: str = None):
        """Save mission log to file"""
        self.executor.save_mission_log(filename, self.report_gen.flight_params)
    
    def generate_mission_report(self) -> str:
        """Generate a comprehensive mission report"""
        self.report_gen.is_running = self.executor.is_running
        return self.report_gen.generate_mission_report()
    
    # Properties for backward compatibility
    @property
    def mission_status(self):
        return self.executor.mission_status
    
    @property
    def is_running(self):
        return self.executor.is_running
    
    @property
    def helicopter(self):
        return self.system_init.helicopter
    
    @property
    def engine(self):
        return self.system_init.engine
    
    @property
    def rotor(self):
        return self.system_init.rotor

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