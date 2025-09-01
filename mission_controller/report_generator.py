#!/usr/bin/env python3
"""
Mission Controller Report Generator
Handles report generation and mission analysis
"""

from datetime import datetime
from dataclasses import asdict

class ReportGenerator:
    """Generates mission reports and analysis"""
    
    def __init__(self, mission_status, flight_params, helicopter, engine, rotor):
        self.mission_status = mission_status
        self.flight_params = flight_params
        self.helicopter = helicopter
        self.engine = engine
        self.rotor = rotor
        self.is_running = False
    
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
    
    def monitor_mission(self) -> dict:
        """Monitor current mission status"""
        if not self.mission_status:
            return {"error": "No active mission"}
        
        status_dict = asdict(self.mission_status)
        if self.flight_params:
            status_dict["flight_parameters"] = asdict(self.flight_params)
        
        return status_dict