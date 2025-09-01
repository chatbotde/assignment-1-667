#!/usr/bin/env python3
"""
Mission Controller Flight Analysis
Handles flight parameter calculations and performance analysis
"""

import sys
import os

# Add paths for flight simulation
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))

from atmosphere import isa_properties
from integrators import cycle_integrator
from .core import FlightParameters

class FlightAnalyzer:
    """Handles flight performance analysis"""
    
    def __init__(self, rotor, fs_inputs):
        self.rotor = rotor
        self.fs_inputs = fs_inputs
    
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
            
            return FlightParameters(
                thrust_N=T,
                torque_Nm=Q,
                power_kW=P/1000,
                rpm=rpm,
                tip_mach=tip_mach,
                disk_loading=disk_loading,
                efficiency=efficiency
            )
            
        except Exception as e:
            print(f"✗ Failed to get flight parameters: {e}")
            return None
    
    def analyze_performance_envelope(self, altitudes=None, velocities=None):
        """Analyze performance across altitude and velocity envelope"""
        if altitudes is None:
            altitudes = [0, 100, 200, 500, 1000]
        if velocities is None:
            velocities = [0, 10, 20, 30, 40]
        
        envelope = {}
        
        for alt in altitudes:
            envelope[alt] = {}
            for vel in velocities:
                params = self.get_flight_parameters(alt, vel)
                if params:
                    envelope[alt][vel] = {
                        'power_kW': params.power_kW,
                        'efficiency': params.efficiency,
                        'tip_mach': params.tip_mach
                    }
        
        return envelope