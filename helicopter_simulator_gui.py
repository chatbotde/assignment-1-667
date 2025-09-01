#!/usr/bin/env python3
"""
Helicopter Flight Simulator GUI - Bonus Task
Simple and stable GUI demonstrating helicopter simulation with real-time controls
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import time
import sys
import os

# Add flight sim path
sys.path.append('flight_sim_part1')

from user_inputs import get_user_inputs, build_rotor

class HelicopterSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚁 HAL Helicopter Flight Simulator - Bonus Task")
        self.root.geometry("1200x800")
        self.root.configure(bg='#34495e')
        
        # Initialize simulation
        self.initialize_simulator()
        
        # Control variables
        self.collective_pitch = tk.DoubleVar(value=8.0)
        self.cyclic_pitch = tk.DoubleVar(value=0.0)
        self.tail_rotor_pitch = tk.DoubleVar(value=5.0)
        self.throttle = tk.DoubleVar(value=80.0)
        
        # Aircraft state
        self.altitude = tk.DoubleVar(value=100.0)
        self.forward_speed = tk.DoubleVar(value=0.0)
        
        # Forces and moments (what the assignment asks for)
        self.forces_moments = {
            'Fx': 0.0, 'Fy': 0.0, 'Fz': 0.0,
            'Mx': 0.0, 'My': 0.0, 'Mz': 0.0
        }
        
        # Simplified data storage (reduced from 100 to 20 points)
        self.time_data = []
        self.force_history = {key: [] for key in self.forces_moments.keys()}
        self.start_time = time.time()
        
        # Create GUI
        self.create_gui()
        
        # Start update loop
        self.update_loop()
        
    def initialize_simulator(self):
        """Initialize helicopter simulation components"""
        print("Initializing Helicopter Simulator...")
        
        # Load configuration
        self.fs_inputs = get_user_inputs()
        self.main_rotor = build_rotor(self.fs_inputs["rotor"])
        
        # Essential component positions (removed mass data - not needed for GUI)
        self.components = {
            'main_rotor': {'x': 0.0, 'y': 0.0, 'z': 2.5},
            'tail_rotor': {'x': -4.0, 'y': 0.0, 'z': 2.0},
            'cg': {'x': -1.0, 'y': 0.0, 'z': 1.5}  # Center of gravity
        }
        
        print("✓ Helicopter simulator initialized")
        print(f"  Main rotor: {self.main_rotor.blade.R_tip:.2f}m radius")
        print(f"  Simplified component model loaded")
        
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
        self.create_control_panel(main_frame)
        self.create_display_panel(main_frame)
        self.create_plot_panel(main_frame)
        
    def create_control_panel(self, parent):
        """Create pilot control panel"""
        control_frame = tk.LabelFrame(parent, text="Pilot Controls", 
                                     font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Collective Control
        self.create_control_slider(control_frame, "Collective Pitch", self.collective_pitch, 
                                 0, 20, "°", "Controls main rotor thrust")
        
        # Cyclic Control
        self.create_control_slider(control_frame, "Cyclic Pitch", self.cyclic_pitch, 
                                 -10, 10, "°", "Controls forward/backward tilt")
        
        # Tail Rotor Control
        self.create_control_slider(control_frame, "Tail Rotor Pitch", self.tail_rotor_pitch, 
                                 0, 15, "°", "Controls yaw/anti-torque")
        
        # Throttle Control
        self.create_control_slider(control_frame, "Throttle", self.throttle, 
                                 0, 100, "%", "Controls engine power")
        
        # Flight Condition Controls
        tk.Label(control_frame, text="Flight Conditions", font=('Arial', 10, 'bold'),
                bg='#34495e', fg='white').pack(pady=(20, 5))
        
        self.create_control_slider(control_frame, "Altitude", self.altitude, 
                                 0, 3000, "m", "Flight altitude")
        
        self.create_control_slider(control_frame, "Forward Speed", self.forward_speed, 
                                 0, 50, "m/s", "Forward flight speed")
        
        # Control buttons (removed data export functionality)
        button_frame = tk.Frame(control_frame, bg='#34495e')
        button_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(button_frame, text="Reset Controls", command=self.reset_controls,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(fill=tk.X, pady=2)
        
    def create_control_slider(self, parent, name, variable, min_val, max_val, unit, description):
        """Create a control slider with label"""
        frame = tk.Frame(parent, bg='#34495e')
        frame.pack(fill=tk.X, pady=5)
        
        # Label
        label = tk.Label(frame, text=f"{name}:", font=('Arial', 10, 'bold'),
                        bg='#34495e', fg='white', width=15, anchor='w')
        label.pack(anchor=tk.W)
        
        # Slider frame
        slider_frame = tk.Frame(frame, bg='#34495e')
        slider_frame.pack(fill=tk.X)
        
        # Slider
        slider = tk.Scale(slider_frame, from_=min_val, to=max_val, resolution=0.1,
                         variable=variable, orient=tk.HORIZONTAL, bg='#34495e', fg='white',
                         highlightbackground='#34495e', troughcolor='#2c3e50')
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Value label
        value_label = tk.Label(slider_frame, text=f"{variable.get():.1f}{unit}",
                              bg='#34495e', fg='#3498db', font=('Arial', 9, 'bold'), width=8)
        value_label.pack(side=tk.RIGHT)
        
        # Update function
        def update_label(*args):
            value_label.config(text=f"{variable.get():.1f}{unit}")
        variable.trace('w', update_label)
        
        # Description
        desc_label = tk.Label(frame, text=description, font=('Arial', 8),
                             bg='#34495e', fg='#95a5a6')
        desc_label.pack(anchor=tk.W)
        
    def create_display_panel(self, parent):
        """Create forces and moments display panel"""
        display_frame = tk.LabelFrame(parent, text="Forces & Moments (Aircraft Reference Frame)", 
                                     font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
        display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Forces section
        forces_frame = tk.LabelFrame(display_frame, text="Forces [N]", 
                                    font=('Arial', 11, 'bold'), bg='#34495e', fg='white')
        forces_frame.pack(fill=tk.X, pady=5)
        
        self.force_labels = {}
        force_colors = {'Fx': '#e74c3c', 'Fy': '#2ecc71', 'Fz': '#3498db'}
        
        for force in ['Fx', 'Fy', 'Fz']:
            frame = tk.Frame(forces_frame, bg='#34495e')
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=f"{force}:", font=('Arial', 11, 'bold'),
                    bg='#34495e', fg='white', width=4).pack(side=tk.LEFT)
            
            label = tk.Label(frame, text="0.0", font=('Arial', 11, 'bold'),
                           bg=force_colors[force], fg='white', width=12)
            label.pack(side=tk.RIGHT)
            self.force_labels[force] = label
        
        # Moments section
        moments_frame = tk.LabelFrame(display_frame, text="Moments [N⋅m]", 
                                     font=('Arial', 11, 'bold'), bg='#34495e', fg='white')
        moments_frame.pack(fill=tk.X, pady=5)
        
        moment_colors = {'Mx': '#9b59b6', 'My': '#f39c12', 'Mz': '#1abc9c'}
        
        for moment in ['Mx', 'My', 'Mz']:
            frame = tk.Frame(moments_frame, bg='#34495e')
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=f"{moment}:", font=('Arial', 11, 'bold'),
                    bg='#34495e', fg='white', width=4).pack(side=tk.LEFT)
            
            label = tk.Label(frame, text="0.0", font=('Arial', 11, 'bold'),
                           bg=moment_colors[moment], fg='white', width=12)
            label.pack(side=tk.RIGHT)
            self.force_labels[moment] = label
        
        # Simplified performance info (removed redundant efficiency display)
        perf_frame = tk.LabelFrame(display_frame, text="Performance", 
                                  font=('Arial', 11, 'bold'), bg='#34495e', fg='white')
        perf_frame.pack(fill=tk.X, pady=5)
        
        self.perf_labels = {}
        perf_items = [('Thrust', 'N', '#e67e22'), ('Power', 'kW', '#8e44ad')]
        
        for name, unit, color in perf_items:
            frame = tk.Frame(perf_frame, bg='#34495e')
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=f"{name}:", font=('Arial', 10, 'bold'),
                    bg='#34495e', fg='white', width=10).pack(side=tk.LEFT)
            
            label = tk.Label(frame, text=f"0.0 {unit}", font=('Arial', 10, 'bold'),
                           bg=color, fg='white', width=12)
            label.pack(side=tk.RIGHT)
            self.perf_labels[name] = label
        
    def create_plot_panel(self, parent):
        """Create real-time plotting panel"""
        plot_frame = tk.LabelFrame(parent, text="Real-Time Forces & Moments", 
                                  font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 6), dpi=80, facecolor='#ecf0f1')
        
        # Create subplots
        self.ax1 = self.fig.add_subplot(2, 1, 1)
        self.ax2 = self.fig.add_subplot(2, 1, 2)
        
        # Configure force plot
        self.ax1.set_title('Forces (Fx, Fy, Fz)', fontweight='bold', color='#2c3e50')
        self.ax1.set_ylabel('Force [N]', fontweight='bold')
        self.ax1.grid(True, alpha=0.3)
        
        # Configure moment plot
        self.ax2.set_title('Moments (Mx, My, Mz)', fontweight='bold', color='#2c3e50')
        self.ax2.set_xlabel('Time [s]', fontweight='bold')
        self.ax2.set_ylabel('Moment [N⋅m]', fontweight='bold')
        self.ax2.grid(True, alpha=0.3)
        
        # Initialize plot lines
        self.force_lines = []
        self.moment_lines = []
        
        force_colors = ['#e74c3c', '#2ecc71', '#3498db']  # Red, Green, Blue
        moment_colors = ['#9b59b6', '#f39c12', '#1abc9c']  # Purple, Orange, Teal
        
        for i, color in enumerate(force_colors):
            line, = self.ax1.plot([], [], color=color, linewidth=2, 
                                 label=['Fx', 'Fy', 'Fz'][i])
            self.force_lines.append(line)
        
        for i, color in enumerate(moment_colors):
            line, = self.ax2.plot([], [], color=color, linewidth=2, 
                                 label=['Mx', 'My', 'Mz'][i])
            self.moment_lines.append(line)
        
        self.ax1.legend(loc='upper right')
        self.ax2.legend(loc='upper right')
        
        self.fig.tight_layout()
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def calculate_forces_and_moments(self):
        """Calculate forces and moments using shared utilities"""
        try:
            # Use shared calculation utilities
            from rotor_utils import rotor_calc
            
            results = rotor_calc.calculate_forces_moments(
                self.collective_pitch.get(),
                self.cyclic_pitch.get(),
                0,  # No roll cyclic in this simplified model
                self.tail_rotor_pitch.get(),
                self.throttle.get(),
                self.altitude.get()
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
    
    def update_displays(self):
        """Update all display elements"""
        # Update force and moment labels
        for key, label in self.force_labels.items():
            value = self.forces_moments[key]
            label.config(text=f"{value:.1f}")
        
        # Update performance labels
        self.perf_labels['Thrust'].config(text=f"{self.performance['thrust']:.1f} N")
        self.perf_labels['Power'].config(text=f"{self.performance['power']:.1f} kW")
        
    def update_plots(self):
        """Update real-time plots"""
        if len(self.time_data) > 1:
            # Update force lines
            force_keys = ['Fx', 'Fy', 'Fz']
            for i, key in enumerate(force_keys):
                self.force_lines[i].set_data(self.time_data, self.force_history[key])
            
            # Update moment lines
            moment_keys = ['Mx', 'My', 'Mz']
            for i, key in enumerate(moment_keys):
                self.moment_lines[i].set_data(self.time_data, self.force_history[key])
            
            # Rescale axes
            if len(self.time_data) > 2:
                self.ax1.relim()
                self.ax1.autoscale_view()
                self.ax2.relim()
                self.ax2.autoscale_view()
            
            # Redraw
            try:
                self.canvas.draw_idle()
            except:
                pass  # Ignore drawing errors
    
    def update_loop(self):
        """Main update loop"""
        # Calculate current forces and moments
        self.calculate_forces_and_moments()
        
        # Update displays
        self.update_displays()
        
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
        
        # Update plots
        self.update_plots()
        
        # Schedule next update (5 Hz - reduced from 10 Hz)
        self.root.after(200, self.update_loop)
    
    def reset_controls(self):
        """Reset all controls to default values"""
        self.collective_pitch.set(8.0)
        self.cyclic_pitch.set(0.0)
        self.tail_rotor_pitch.set(5.0)
        self.throttle.set(80.0)
        self.altitude.set(100.0)
        self.forward_speed.set(0.0)
        
        # Clear data
        self.time_data = []
        for key in self.force_history:
            self.force_history[key] = []
        self.start_time = time.time()
        


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