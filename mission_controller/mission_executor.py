#!/usr/bin/env python3
"""
Mission Controller Execution Engine
Handles mission execution, monitoring, and command processing
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any

# Add paths for mission planner
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mission planner', 'mission_planner_part2'))

from planner_main import run_mission
from .core import MissionStatus, MissionCommand

class MissionExecutor:
    """Handles mission execution and monitoring"""
    
    def __init__(self):
        self.mission_status = None
        self.mission_log = []
        self.command_queue = []
        self.is_running = False
    
    def create_mission(self, mission_config: Dict[str, Any], helicopter) -> str:
        """Create a new mission"""
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.mission_status = MissionStatus(
            mission_id=mission_id,
            status="planning",
            current_segment=0,
            total_segments=len(mission_config.get("segments", [])),
            elapsed_time=0.0,
            fuel_remaining=helicopter.fuel_kg,
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
    
    def save_mission_log(self, filename: str = None, flight_params=None):
        """Save mission log to file"""
        if not filename:
            filename = f"mission_log_{self.mission_status.mission_id}.json"
        
        log_data = {
            "mission_status": self.mission_status.__dict__ if self.mission_status else None,
            "flight_parameters": flight_params.__dict__ if flight_params else None,
            "mission_log": self.mission_log,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"✓ Mission log saved to {filename}")