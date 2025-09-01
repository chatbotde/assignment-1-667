#!/usr/bin/env python3
"""
Mission Controller Core - Core data structures and base functionality
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any
from datetime import datetime

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