#!/usr/bin/env python3
"""
Mission Controller System Initialization
Handles initialization and validation of flight simulation and mission planner systems
"""

import sys
import os

# Add paths for both flight sim and mission planner
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'flight_sim_part1'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mission planner', 'mission_planner_part2'))

# Flight simulation imports
from user_inputs import get_user_inputs, build_rotor
from atmosphere import isa_properties
from integrators import cycle_integrator

# Mission planner imports
from mp_inputs import get_helicopter_and_engine

class SystemInitializer:
    """Handles system initialization and validation"""
    
    def __init__(self):
        self.fs_inputs = None
        self.rotor = None
        self.helicopter = None
        self.engine = None
        self.mp_rotor = None
    
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