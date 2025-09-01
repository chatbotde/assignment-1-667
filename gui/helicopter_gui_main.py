#!/usr/bin/env python3
"""
Helicopter Flight Simulator GUI - Main Application
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import time

# Add flight sim path
sys.path.append('flight_sim_part1')

from user_inputs import get_user_inputs, build_rotor
from gui.control_panel import ControlPanel
from gui.display_panel import DisplayPanel
from gui.plot_panel import PlotPanel
from gui.simulation_engine import SimulationEngine

class HelicopterSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚁 HAL Helicopter Flight Simulator - Bonus Task")
        self.root.geometry("1200x800")
        self.root.configure(bg='#34495e')
        
        # Initialize simulation engine
        self.simulation = SimulationEngine()
        
        # Control variables
        self.collective_pitch = tk.DoubleVar(value=8.0)
        self.cyclic_pitch = tk.DoubleVar(value=0.0)
        self.tail_rotor_pitch = tk.DoubleVar(value=5.0)
        self.throttle = tk.DoubleVar(value=80.0)
        self.altitude = tk.DoubleVar(value=100.0)
        self.forward_speed = tk.DoubleVar(value=0.0)
        
        # Create GUI components
        self.create_gui()
        
        # Start update loop
        self.update_loop()
        
    def create_gui(self):
        """Create the main GUI interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#34495e')
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(title_frame, text="🚁 HAL Helicopter Flight Simulator", 
                              font=('Arial', 18, 'bold'), bg='#34495e', fg='white')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Bonus Task: Real-time Forces and Moments Simulation", 
                                 font=('Arial', 12), bg='#34495e', fg='#bdc3c7')
        subtitle_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#34495e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create panels
        self.control_panel = ControlPanel(main_frame, self)
        self.display_panel = DisplayPanel(main_frame, self)
        self.plot_panel = PlotPanel(main_frame, self)
        
    def get_control_values(self):
        """Get current control values"""
        return {
            'collective_pitch': self.collective_pitch.get(),
            'cyclic_pitch': self.cyclic_pitch.get(),
            'tail_rotor_pitch': self.tail_rotor_pitch.get(),
            'throttle': self.throttle.get(),
            'altitude': self.altitude.get(),
            'forward_speed': self.forward_speed.get()
        }
    
    def reset_controls(self):
        """Reset all controls to default values"""
        self.collective_pitch.set(8.0)
        self.cyclic_pitch.set(0.0)
        self.tail_rotor_pitch.set(5.0)
        self.throttle.set(80.0)
        self.altitude.set(100.0)
        self.forward_speed.set(0.0)
        
        # Clear simulation data
        self.simulation.reset_data()
        
    def update_loop(self):
        """Main update loop"""
        # Get current control values
        controls = self.get_control_values()
        
        # Update simulation
        self.simulation.update(controls)
        
        # Update displays
        self.display_panel.update(self.simulation.get_forces_moments(), 
                                 self.simulation.get_performance())
        
        # Update plots
        self.plot_panel.update(self.simulation.get_time_data(), 
                              self.simulation.get_force_history())
        
        # Schedule next update (5 Hz)
        self.root.after(200, self.update_loop)


def main():
    """Main function"""
    print("=== HAL HELICOPTER SIMULATOR GUI ===")
    print("Starting helicopter flight simulator...")
    
    try:
        root = tk.Tk()
        app = HelicopterSimulatorGUI(root)
        
        print("✓ GUI initialized successfully")
        print("✓ Real-time simulation running")
        print("\nInstructions:")
        print("1. Adjust control sliders to change helicopter settings")
        print("2. Watch forces and moments update in real-time")
        print("3. Observe the effect on the plots")

        print("\nDemonstrating Bonus Task Requirements:")
        print("- Real-time forces and moments calculation")
        print("- Component placement and reference frame")
        print("- Interactive control inputs")
        print("- Live visualization")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()