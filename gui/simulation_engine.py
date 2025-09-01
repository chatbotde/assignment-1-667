"""
Simulation Engine for Helicopter Simulator GUI
"""

import time
import sys
import os

# Add flight sim path
sys.path.append('flight_sim_part1')

from user_inputs import get_user_inputs, build_rotor

class SimulationEngine:
    def __init__(self):
        self.initialize_simulator()
        
        # Aircraft state
        self.forces_moments = {
            'Fx': 0.0, 'Fy': 0.0, 'Fz': 0.0,
            'Mx': 0.0, 'My': 0.0, 'Mz': 0.0
        }
        
        self.performance = {
            'thrust': 0.0,
            'power': 0.0
        }
        
        # Data storage (reduced from 100 to 20 points)
        self.time_data = []
        self.force_history = {key: [] for key in self.forces_moments.keys()}
        self.start_time = time.time()
        
    def initialize_simulator(self):
        """Initialize helicopter simulation components"""
        print("Initializing Helicopter Simulator...")
        
        # Load configuration
        self.fs_inputs = get_user_inputs()
        self.main_rotor = build_rotor(self.fs_inputs["rotor"])
        
        # Essential component positions
        self.components = {
            'main_rotor': {'x': 0.0, 'y': 0.0, 'z': 2.5},
            'tail_rotor': {'x': -4.0, 'y': 0.0, 'z': 2.0},
            'cg': {'x': -1.0, 'y': 0.0, 'z': 1.5}  # Center of gravity
        }
        
        print("✓ Helicopter simulator initialized")
        print(f"  Main rotor: {self.main_rotor.blade.R_tip:.2f}m radius")
        print(f"  Simplified component model loaded")
        
    def calculate_forces_and_moments(self, controls):
        """Calculate forces and moments using shared utilities"""
        try:
            # Use shared calculation utilities
            from rotor_utils import rotor_calc
            
            results = rotor_calc.calculate_forces_moments(
                controls['collective_pitch'],
                controls['cyclic_pitch'],
                0,  # No roll cyclic in this simplified model
                controls['tail_rotor_pitch'],
                controls['throttle'],
                controls['altitude']
            )
            
            # Update forces and moments
            self.forces_moments = {
                'Fx': results['Fx'],
                'Fy': results['Fy'],
                'Fz': results['Fz'],
                'Mx': results['Mx'],
                'My': results['My'],
                'Mz': results['Mz']
            }
            
            # Performance metrics
            self.performance = {
                'thrust': results['thrust'],
                'power': results['power']
            }
            
        except Exception as e:
            print(f"Calculation error: {e}")
            # Set safe default values
            self.forces_moments = {key: 0.0 for key in self.forces_moments.keys()}
            self.performance = {'thrust': 0, 'power': 0}
    
    def update(self, controls):
        """Update simulation with current control values"""
        # Calculate current forces and moments
        self.calculate_forces_and_moments(controls)
        
        # Log data for plotting
        current_time = time.time() - self.start_time
        self.time_data.append(current_time)
        
        for key in self.forces_moments:
            self.force_history[key].append(self.forces_moments[key])
        
        # Keep only last 20 points (reduced from 100)
        if len(self.time_data) > 20:
            self.time_data = self.time_data[-20:]
            for key in self.force_history:
                self.force_history[key] = self.force_history[key][-20:]
    
    def get_forces_moments(self):
        """Get current forces and moments"""
        return self.forces_moments
    
    def get_performance(self):
        """Get current performance metrics"""
        return self.performance
    
    def get_time_data(self):
        """Get time data for plotting"""
        return self.time_data
    
    def get_force_history(self):
        """Get force history for plotting"""
        return self.force_history
    
    def reset_data(self):
        """Reset simulation data"""
        self.time_data = []
        for key in self.force_history:
            self.force_history[key] = []
        self.start_time = time.time()