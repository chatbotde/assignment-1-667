#!/usr/bin/env python3
"""
Performance Analyzer Module
Handles rotor performance analysis and mission calculations
"""

import numpy as np
import sys
import os

# Add flight sim path
sys.path.append('flight_sim_part1')

from atmosphere import isa_properties
from airfoil import Airfoil
from blade import Blade
from rotor import Rotor
from integrators import cycle_integrator


class PerformanceAnalyzer:
    def __init__(self):
        """Initialize performance analyzer"""
        pass
    
    def analyze_main_rotor_performance(self, main_rotor):
        """Analyze main rotor performance"""
        print("Analyzing main rotor performance...")
        
        # Create rotor model for analysis
        airfoil = Airfoil(a0=5.7, Cd0=0.008, e=1.2)  # Improved airfoil
        
        # Use linear taper and twist
        blade = Blade(
            R_root=main_rotor["root_cutout_m"],
            R_tip=main_rotor["radius_m"],
            c_root=main_rotor["chord_root_m"],
            c_tip=main_rotor["chord_tip_m"],
            theta_root_rad=np.deg2rad(12),  # Root pitch
            theta_tip_rad=np.deg2rad(4),   # Tip pitch (8° twist)
            airfoil=airfoil
        )
        
        rotor = Rotor(main_rotor["num_blades"], blade)
        
        # Performance analysis at different conditions
        omega = 2 * np.pi * main_rotor["rpm"] / 60.0
        
        # Hover performance at sea level
        rho_sl, _ = isa_properties(0)
        T_hover, Q_hover, P_hover = cycle_integrator(rotor, 0, omega, rho_sl)
        
        # High altitude performance (3500m)
        rho_alt, _ = isa_properties(3500)
        T_alt, Q_alt, P_alt = cycle_integrator(rotor, 0, omega, rho_alt)
        
        # Forward flight performance
        V_forward = 50  # m/s (180 km/h)
        T_forward, Q_forward, P_forward = cycle_integrator(rotor, V_forward, omega, rho_sl)
        
        main_rotor_performance = {
            "hover_sl": {"thrust_N": T_hover, "power_kW": P_hover/1000},
            "hover_3500m": {"thrust_N": T_alt, "power_kW": P_alt/1000},
            "forward_180kmh": {"thrust_N": T_forward, "power_kW": P_forward/1000},
            "disk_loading_N_m2": T_hover / (np.pi * main_rotor["radius_m"]**2),
            "tip_speed_ms": omega * main_rotor["radius_m"]
        }
        
        print(f"  Hover thrust (SL): {T_hover:.0f} N")
        print(f"  Hover power (SL): {P_hover/1000:.0f} kW")
        
        return main_rotor_performance
    
    def analyze_hover_mission(self, main_rotor, altitude=2000):
        """Analyze hover mission at specified altitude"""
        rho, _ = isa_properties(altitude)
        
        # Calculate hover performance
        airfoil = Airfoil(a0=5.7, Cd0=0.008, e=1.2)
        blade = Blade(
            R_root=main_rotor["root_cutout_m"],
            R_tip=main_rotor["radius_m"],
            c_root=main_rotor["chord_root_m"],
            c_tip=main_rotor["chord_tip_m"],
            theta_root_rad=np.deg2rad(10),
            theta_tip_rad=np.deg2rad(2),
            airfoil=airfoil
        )
        
        rotor = Rotor(main_rotor["num_blades"], blade)
        omega = 2 * np.pi * main_rotor["rpm"] / 60.0
        
        T_available, Q, P_main = cycle_integrator(rotor, 0, omega, rho)
        P_tail = P_main * 0.12  # 12% for tail rotor
        P_total = (P_main + P_tail) * 1.1  # 10% losses
        
        # Maximum weights
        max_weight_thrust = T_available / 9.81  # kg
        
        # Assume 2000kW engine power available at altitude
        P_engine_available = 2000 * 1000 * 0.85  # 85% at altitude
        max_weight_power = P_engine_available / (P_total / T_available) / 9.81
        
        # Hover endurance analysis
        weights = np.linspace(2000, 5000, 20)
        fuel_rates = []
        endurances = []
        
        for weight in weights:
            # Scale power with weight
            P_required = P_total * (weight * 9.81 / T_available)
            
            # Fuel consumption (0.25 kg/kW/hr for turboshaft)
            sfc = 0.25
            fuel_rate = (P_required / 1000) * sfc / 60  # kg/min
            fuel_rates.append(fuel_rate)
            
            # Endurance with 800kg fuel
            if fuel_rate > 0:
                endurance = 800 / fuel_rate  # minutes
            else:
                endurance = 0
            endurances.append(endurance)
        
        return {
            "altitude_m": altitude,
            "max_weight_thrust_kg": max_weight_thrust,
            "max_weight_power_kg": max_weight_power,
            "thrust_available_N": T_available,
            "power_required_kW": P_total / 1000,
            "weights": weights.tolist(),
            "fuel_rates": fuel_rates,
            "endurances": endurances
        }
    
    def calculate_rotor_performance(self, rotor_config, theta_range):
        """Calculate rotor performance over pitch range"""
        try:
            from rotor_utils import rotor_calc
            
            thrust_values = []
            power_values = []
            
            for theta_deg in theta_range:
                results = rotor_calc.calculate_rotor_performance(
                    rotor_config, theta_deg, 
                    forward_speed=0, altitude=0, rpm=rotor_config["rpm"]
                )
                thrust_values.append(results['thrust_N'])
                power_values.append(results['power_kW'])
            
            return thrust_values, power_values
        except ImportError:
            # Fallback to simplified calculation
            return self._simplified_rotor_performance(rotor_config, theta_range)
    
    def _simplified_rotor_performance(self, rotor_config, theta_range):
        """Simplified rotor performance calculation"""
        thrust_values = []
        power_values = []
        
        # Simplified momentum theory calculations
        rho = 1.225  # Sea level density
        A = np.pi * rotor_config["radius_m"]**2
        
        for theta_deg in theta_range:
            # Simplified thrust calculation
            thrust = rho * A * (theta_deg * 0.1)**2 * 1000  # Very simplified
            power = thrust * np.sqrt(thrust / (2 * rho * A)) / 1000  # kW
            
            thrust_values.append(max(0, thrust))
            power_values.append(max(0, power))
        
        return thrust_values, power_values