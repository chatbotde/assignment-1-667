#!/usr/bin/env python3
"""
Consolidated Rotor Utilities
Shared rotor calculation functions to eliminate code duplication
"""

import numpy as np
import sys
import os

# Add flight sim path
sys.path.append('flight_sim_part1')

from user_inputs import get_user_inputs, build_rotor
from atmosphere import isa_properties
from integrators import cycle_integrator
from blade import Blade
from rotor import Rotor
from airfoil import Airfoil

class RotorCalculator:
    """Centralized rotor calculation utilities"""
    
    def __init__(self):
        """Initialize with standard configuration"""
        self.fs_inputs = get_user_inputs()
        self.standard_rotor = build_rotor(self.fs_inputs["rotor"])
        self.standard_rpm = self.fs_inputs["condition"]["rpm"]
        
    def calculate_rotor_performance(self, rotor_config, theta_deg, forward_speed=0, altitude=0, rpm=None):
        """
        Calculate rotor performance for given conditions
        
        Args:
            rotor_config: Dict with rotor parameters or Rotor object
            theta_deg: Collective pitch in degrees
            forward_speed: Forward velocity in m/s
            altitude: Altitude in meters
            rpm: RPM (uses standard if None)
            
        Returns:
            Dict with thrust, torque, power
        """
        # Get atmospheric conditions
        rho, _ = isa_properties(altitude)
        
        # Set RPM
        if rpm is None:
            rpm = self.standard_rpm
        omega = 2 * np.pi * rpm / 60.0
        
        # Create rotor if config dict provided
        if isinstance(rotor_config, dict):
            rotor = self._create_rotor_from_config(rotor_config, theta_deg)
        else:
            rotor = rotor_config
            
        # Calculate performance
        T, Q, P = cycle_integrator(rotor, forward_speed, omega, rho)
        
        return {
            'thrust_N': T,
            'torque_Nm': Q, 
            'power_W': P,
            'power_kW': P / 1000
        }
    
    def _create_rotor_from_config(self, config, theta_deg):
        """Create rotor object from configuration dict"""
        theta_rad = np.deg2rad(theta_deg)
        twist_rad = np.deg2rad(config.get('twist_deg', 0))
        
        # Create airfoil
        airfoil = Airfoil(
            a0=config.get('a0', 5.7),
            Cd0=config.get('Cd0', 0.008),
            e=config.get('e', 1.2)
        )
        
        # Create blade
        blade = Blade(
            R_root=config.get('root_cutout_m', 0.125),
            R_tip=config.get('radius_m', 0.762),
            c_root=config.get('chord_root_m', 0.0508),
            c_tip=config.get('chord_tip_m', 0.0508),
            theta_root_rad=theta_rad,
            theta_tip_rad=theta_rad - twist_rad,
            airfoil=airfoil
        )
        
        # Create rotor
        return Rotor(config.get('num_blades', 4), blade)
    
    def calculate_forces_moments(self, collective, cyclic_pitch, cyclic_roll, tail_pitch, throttle, altitude=100):
        """
        Calculate aircraft forces and moments from control inputs
        Standard component positions and reference frame
        """
        # Component positions (aircraft reference frame)
        components = {
            'main_rotor': {'x': 0.0, 'y': 0.0, 'z': 2.5},
            'tail_rotor': {'x': -4.0, 'y': 0.0, 'z': 2.0},
            'cg': {'x': -1.0, 'y': 0.0, 'z': 1.5}
        }
        
        # Main rotor performance
        main_perf = self.calculate_rotor_performance(
            self.standard_rotor, collective, 0, altitude, 
            rpm=self.standard_rpm * (throttle / 100.0)
        )
        
        # Tail rotor (simplified)
        T_tail = 500 * (tail_pitch / 10.0)  # Simplified model
        
        # Transform to aircraft reference frame
        cyclic_pitch_rad = np.deg2rad(cyclic_pitch)
        cyclic_roll_rad = np.deg2rad(cyclic_roll)
        
        # Forces
        Fx = main_perf['thrust_N'] * np.sin(cyclic_pitch_rad)
        Fy = main_perf['thrust_N'] * np.sin(cyclic_roll_rad) + T_tail
        Fz = main_perf['thrust_N'] * np.cos(cyclic_pitch_rad) * np.cos(cyclic_roll_rad)
        
        # Moments about CG
        main_pos = components['main_rotor']
        tail_pos = components['tail_rotor']
        cg_pos = components['cg']
        
        # Moment arms
        dx_main = main_pos['x'] - cg_pos['x']
        dz_main = main_pos['z'] - cg_pos['z']
        dx_tail = tail_pos['x'] - cg_pos['x']
        dz_tail = tail_pos['z'] - cg_pos['z']
        
        # Moments
        Mx = Fy * dz_main - Fz * 0 + T_tail * dz_tail
        My = Fz * dx_main - Fx * dz_main
        Mz = main_perf['torque_Nm'] - T_tail * 0.1
        
        return {
            'Fx': Fx, 'Fy': Fy, 'Fz': Fz,
            'Mx': Mx, 'My': My, 'Mz': Mz,
            'thrust': main_perf['thrust_N'],
            'power': main_perf['power_kW']
        }

# Global instance for easy access
rotor_calc = RotorCalculator()