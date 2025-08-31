#!/usr/bin/env python3
"""
Flight Simulator GUI - Bonus Task Implementation
Interactive helicopter flight simulator with real-time controls and visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading
import time
import sys
import os
from datetime import datetime

# Add flight sim path
sys.path.append('flight_sim_part1')

from user_inputs import get_user_inputs, build_rotor
from atmosphere import isa_properties
from integrators import cycle_integrator
from blade import Blade
from rotor import Rotor
from airfoil import Airfoil
from stabilizers import Stabilizers

class FlightSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HAL Helicopter Flight Simulator - Bonus Task")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # Initialize flight simulation
        self.initialize_flight_sim()
        
        # GUI state variables
        self.is_running = False
        self.simulation_thread = None
        
        # Control inputs (pilot controls)
        self.collective_pitch = tk.DoubleVar(value=8.0)  # degrees
        self.cyclic_pitch = tk.DoubleVar(value=0.0)      # degrees
        self.cyclic_roll = tk.DoubleVar(value=0.0)       # degrees
        self.tail_rotor_pitch = tk.DoubleVar(value=5.0)  # degrees
        self.throttle = tk.DoubleVar(value=75.0)         # percent
        
        # Aircraft state variables
        self.altitude = tk.DoubleVar(value=100.0)        # meters
        self.forward_speed = tk.DoubleVar(value=0.0)     # m/s
        self.vertical_speed = tk.DoubleVar(value=0.0)    # m/s
        
        # Force and moment variables
        self.thrust_main = tk.DoubleVar(value=0.0)       # N
        self.thrust_tail = tk.DoubleVar(value=0.0)       # N
        self.power_main = tk.DoubleVar(value=0.0)        # kW
        self.power_tail = tk.DoubleVar(value=0.0)        # kW
        self.moment_pitch = tk.DoubleVar(value=0.0)      # N⋅m
        self.moment_roll = tk.DoubleVar(value=0.0)       # N⋅m
        self.moment_yaw = tk.DoubleVar(value=0.0)        # N⋅m
        
        # Data logging
        self.time_data = []
        self.force_data = {'Fx': [], 'Fy': [], 'Fz': [], 'Mx': [], 'My': [], 'Mz': []}
        self.start_time = time.time()
        
        # Create GUI
        self.create_gui()
        
        # Start simulation loop
        self.update_simulation()
        
    def initialize_flight_sim(self):
        """Initialize flight simulation components"""
        print("Initializing Flight Simulator...")
        
        # Load flight sim configuration
        self.fs_inputs = get_user_inputs()
        self.main_rotor = build_rotor(self.fs_inputs["rotor"])
        
        # Create tail rotor (smaller)
        tail_airfoil = Airfoil(a0=5.5, Cd0=0.010, e=1.3)
        tail_blade = Blade(0.05, 0.4, 0.03, 0.02, 0.1, 0.1, tail_airfoil)
        self.tail_rotor = Rotor(4, tail_blade)
        
        # Stabilizers
        self.stabilizers = Stabilizers(**self.fs_inputs["stabilizers"])
        
        # Component positions (relative to aircraft nose)
        self.component_positions = {
            'main_rotor': {'x': 0.0, 'y': 0.0, 'z': 2.5},
            'tail_rotor': {'x': -4.0, 'y': 0.0, 'z': 2.0},
            'h_stab': {'x': -4.5, 'y': 0.0, 'z': 1.5},
            'v_stab': {'x': -4.5, 'y': 0.0, 'z': 2.0},
            'cg': {'x': -0.5, 'y': 0.0, 'z': 1.8}  # Center of gravity
        }
        
        print("✓ Flight Simulator Initialized")
        print(f"  Main Rotor: {self.main_rotor.blade.R_tip:.2f}m radius")
        print(f"  Component positions defined")
        
    def create_gui(self):
        """Create the main GUI interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="🚁 HAL Helicopter Flight Simulator", 
                              font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=(0, 10))
        
        # Create main sections
        self.create_control_panel(main_frame)
        self.create_instrument_panel(main_frame)
        self.create_visualization_panel(main_frame)
        self.create_status_panel(main_frame)
        
    def create_control_panel(self, parent):
        """Create pilot control panel"""
        control_frame = ttk.LabelFrame(parent, text="Pilot Controls", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # Collective Control
        ttk.Label(control_frame, text="Collective Pitch", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        collective_frame = ttk.Frame(control_frame)
        collective_frame.pack(fill=tk.X, pady=5)
        
        collective_scale = ttk.Scale(collective_frame, from_=0, to=20, 
                                   variable=self.collective_pitch, orient=tk.HORIZONTAL)
        collective_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        collective_label = ttk.Label(collective_frame, text="8.0°", width=6)
        collective_label.pack(side=tk.RIGHT)
        
        def update_collective_label(*args):
            collective_label.config(text=f"{self.collective_pitch.get():.1f}°")
        self.collective_pitch.trace('w', update_collective_label)
        
        # Cyclic Pitch Control
        ttk.Label(control_frame, text="Cyclic Pitch", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        cyclic_pitch_frame = ttk.Frame(control_frame)
        cyclic_pitch_frame.pack(fill=tk.X, pady=5)
        
        cyclic_pitch_scale = ttk.Scale(cyclic_pitch_frame, from_=-10, to=10, 
                                     variable=self.cyclic_pitch, orient=tk.HORIZONTAL)
        cyclic_pitch_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        cyclic_pitch_label = ttk.Label(cyclic_pitch_frame, text="0.0°", width=6)
        cyclic_pitch_label.pack(side=tk.RIGHT)
        
        def update_cyclic_pitch_label(*args):
            cyclic_pitch_label.config(text=f"{self.cyclic_pitch.get():.1f}°")
        self.cyclic_pitch.trace('w', update_cyclic_pitch_label)
        
        # Cyclic Roll Control
        ttk.Label(control_frame, text="Cyclic Roll", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        cyclic_roll_frame = ttk.Frame(control_frame)
        cyclic_roll_frame.pack(fill=tk.X, pady=5)
        
        cyclic_roll_scale = ttk.Scale(cyclic_roll_frame, from_=-10, to=10, 
                                    variable=self.cyclic_roll, orient=tk.HORIZONTAL)
        cyclic_roll_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        cyclic_roll_label = ttk.Label(cyclic_roll_frame, text="0.0°", width=6)
        cyclic_roll_label.pack(side=tk.RIGHT)
        
        def update_cyclic_roll_label(*args):
            cyclic_roll_label.config(text=f"{self.cyclic_roll.get():.1f}°")
        self.cyclic_roll.trace('w', update_cyclic_roll_label)
        
        # Tail Rotor Control
        ttk.Label(control_frame, text="Tail Rotor Pitch", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        tail_frame = ttk.Frame(control_frame)
        tail_frame.pack(fill=tk.X, pady=5)
        
        tail_scale = ttk.Scale(tail_frame, from_=0, to=15, 
                             variable=self.tail_rotor_pitch, orient=tk.HORIZONTAL)
        tail_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tail_label = ttk.Label(tail_frame, text="5.0°", width=6)
        tail_label.pack(side=tk.RIGHT)
        
        def update_tail_label(*args):
            tail_label.config(text=f"{self.tail_rotor_pitch.get():.1f}°")
        self.tail_rotor_pitch.trace('w', update_tail_label)
        
        # Throttle Control
        ttk.Label(control_frame, text="Throttle", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        throttle_frame = ttk.Frame(control_frame)
        throttle_frame.pack(fill=tk.X, pady=5)
        
        throttle_scale = ttk.Scale(throttle_frame, from_=0, to=100, 
                                 variable=self.throttle, orient=tk.HORIZONTAL)
        throttle_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        throttle_label = ttk.Label(throttle_frame, text="75%", width=6)
        throttle_label.pack(side=tk.RIGHT)
        
        def update_throttle_label(*args):
            throttle_label.config(text=f"{self.throttle.get():.0f}%")
        self.throttle.trace('w', update_throttle_label)
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.start_button = ttk.Button(button_frame, text="Start Simulation", 
                                     command=self.toggle_simulation)
        self.start_button.pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="Reset Controls", 
                  command=self.reset_controls).pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="Save Data", 
                  command=self.save_simulation_data).pack(fill=tk.X, pady=2)
        
    def create_instrument_panel(self, parent):
        """Create flight instruments panel"""
        instrument_frame = ttk.LabelFrame(parent, text="Flight Instruments", padding=10)
        instrument_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Aircraft state display
        state_frame = ttk.LabelFrame(instrument_frame, text="Aircraft State", padding=5)
        state_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create instrument displays
        instruments = [
            ("Altitude", self.altitude, "m", "blue"),
            ("Forward Speed", self.forward_speed, "m/s", "green"),
            ("Vertical Speed", self.vertical_speed, "m/s", "orange")
        ]
        
        for i, (name, var, unit, color) in enumerate(instruments):
            frame = ttk.Frame(state_frame)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=f"{name}:", width=15).pack(side=tk.LEFT)
            label = tk.Label(frame, text=f"{var.get():.1f} {unit}", 
                           width=10, bg=color, fg='white', font=('Arial', 10, 'bold'))
            label.pack(side=tk.RIGHT)
            
            # Store reference for updates
            setattr(self, f"{name.lower().replace(' ', '_')}_label", label)
        
        # Forces and moments display
        forces_frame = ttk.LabelFrame(instrument_frame, text="Forces & Moments", padding=5)
        forces_frame.pack(fill=tk.X, pady=(0, 10))
        
        force_instruments = [
            ("Main Thrust", self.thrust_main, "N", "red"),
            ("Tail Thrust", self.thrust_tail, "N", "purple"),
            ("Main Power", self.power_main, "kW", "darkgreen"),
            ("Tail Power", self.power_tail, "kW", "darkblue"),
            ("Pitch Moment", self.moment_pitch, "N⋅m", "brown"),
            ("Roll Moment", self.moment_roll, "N⋅m", "navy"),
            ("Yaw Moment", self.moment_yaw, "N⋅m", "maroon")
        ]
        
        for i, (name, var, unit, color) in enumerate(force_instruments):
            frame = ttk.Frame(forces_frame)
            frame.pack(fill=tk.X, pady=1)
            
            ttk.Label(frame, text=f"{name}:", width=15).pack(side=tk.LEFT)
            label = tk.Label(frame, text=f"{var.get():.1f} {unit}", 
                           width=12, bg=color, fg='white', font=('Arial', 9, 'bold'))
            label.pack(side=tk.RIGHT)
            
            # Store reference for updates
            setattr(self, f"{name.lower().replace(' ', '_').replace('⋅', '_')}_label", label)
        
    def create_visualization_panel(self, parent):
        """Create real-time visualization panel"""
        viz_frame = ttk.LabelFrame(parent, text="Real-Time Visualization", padding=5)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 6), dpi=80, facecolor='white')
        
        # Create subplots for forces and moments
        self.ax1 = self.fig.add_subplot(2, 1, 1)
        self.ax2 = self.fig.add_subplot(2, 1, 2)
        
        self.ax1.set_title('Forces (Fx, Fy, Fz)', fontsize=12, fontweight='bold')
        self.ax1.set_ylabel('Force [N]')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend(['Fx', 'Fy', 'Fz'])
        
        self.ax2.set_title('Moments (Mx, My, Mz)', fontsize=12, fontweight='bold')
        self.ax2.set_xlabel('Time [s]')
        self.ax2.set_ylabel('Moment [N⋅m]')
        self.ax2.grid(True, alpha=0.3)
        self.ax2.legend(['Mx', 'My', 'Mz'])
        
        # Initialize empty plots
        self.force_lines = []
        self.moment_lines = []
        
        colors = ['red', 'green', 'blue']
        for i, color in enumerate(colors):
            line1, = self.ax1.plot([], [], color=color, linewidth=2)
            line2, = self.ax2.plot([], [], color=color, linewidth=2)
            self.force_lines.append(line1)
            self.moment_lines.append(line2)
        
        self.fig.tight_layout()
        
        # Embed plot in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_status_panel(self, parent):
        """Create status and information panel"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status display
        self.status_label = tk.Label(status_frame, text="Status: Ready", 
                                   bg='green', fg='white', font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Time display
        self.time_label = tk.Label(status_frame, text="Time: 0.0s", 
                                 bg='blue', fg='white', font=('Arial', 10, 'bold'))
        self.time_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Info display
        info_text = "Controls: Adjust sliders to change rotor pitch angles and throttle. Watch forces and moments change in real-time!"
        self.info_label = tk.Label(status_frame, text=info_text, 
                                 bg='#34495e', fg='white', font=('Arial', 9))
        self.info_label.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
    def calculate_forces_and_moments(self):
        """Calculate instantaneous forces and moments from all components"""
        # Get current atmospheric conditions
        rho, a = isa_properties(self.altitude.get())
        
        # Main rotor calculations
        main_rpm = self.fs_inputs["condition"]["rpm"] * (self.throttle.get() / 100.0)
        main_omega = 2 * np.pi * main_rpm / 60.0
        
        # Update main rotor blade pitch
        collective_rad = np.deg2rad(self.collective_pitch.get())
        cyclic_pitch_rad = np.deg2rad(self.cyclic_pitch.get())
        
        # Create main rotor with current collective
        main_blade = Blade(
            self.main_rotor.blade.R_root,
            self.main_rotor.blade.R_tip,
            self.main_rotor.blade.c_root,
            self.main_rotor.blade.c_tip,
            collective_rad,
            collective_rad - np.deg2rad(2),  # 2° twist
            self.main_rotor.blade.airfoil
        )
        main_rotor = Rotor(self.main_rotor.B, main_blade)
        
        # Calculate main rotor performance
        T_main, Q_main, P_main = cycle_integrator(
            main_rotor, self.forward_speed.get(), main_omega, rho)
        
        # Tail rotor calculations
        tail_rpm = main_rpm * 4.5  # Typical tail rotor gear ratio
        tail_omega = 2 * np.pi * tail_rpm / 60.0
        
        tail_pitch_rad = np.deg2rad(self.tail_rotor_pitch.get())
        tail_blade = Blade(
            self.tail_rotor.blade.R_root,
            self.tail_rotor.blade.R_tip,
            self.tail_rotor.blade.c_root,
            self.tail_rotor.blade.c_tip,
            tail_pitch_rad,
            tail_pitch_rad,
            self.tail_rotor.blade.airfoil
        )
        tail_rotor = Rotor(self.tail_rotor.B, tail_blade)
        
        T_tail, Q_tail, P_tail = cycle_integrator(
            tail_rotor, 0, tail_omega, rho)
        
        # Stabilizer forces
        stab_forces = self.stabilizers.forces_moments(rho, self.forward_speed.get())
        
        # Transform forces to aircraft reference frame
        # Main rotor: vertical thrust, affected by cyclic
        Fx_main = T_main * np.sin(cyclic_pitch_rad)
        Fy_main = T_main * np.sin(np.deg2rad(self.cyclic_roll.get()))
        Fz_main = T_main * np.cos(cyclic_pitch_rad) * np.cos(np.deg2rad(self.cyclic_roll.get()))
        
        # Tail rotor: side force
        Fx_tail = 0
        Fy_tail = T_tail
        Fz_tail = 0
        
        # Total forces
        Fx_total = Fx_main + Fx_tail
        Fy_total = Fy_main + Fy_tail
        Fz_total = Fz_main + Fz_tail
        
        # Calculate moments about center of gravity
        # Main rotor moments
        main_pos = self.component_positions['main_rotor']
        cg_pos = self.component_positions['cg']
        
        # Moment arms
        dx_main = main_pos['x'] - cg_pos['x']
        dy_main = main_pos['y'] - cg_pos['y']
        dz_main = main_pos['z'] - cg_pos['z']
        
        # Main rotor moments
        Mx_main = Fy_main * dz_main - Fz_main * dy_main + Q_main * np.sin(cyclic_pitch_rad)
        My_main = Fz_main * dx_main - Fx_main * dz_main + Q_main * np.sin(np.deg2rad(self.cyclic_roll.get()))
        Mz_main = Fx_main * dy_main - Fy_main * dx_main + Q_main * 0.1  # Small coupling
        
        # Tail rotor moments
        tail_pos = self.component_positions['tail_rotor']
        dx_tail = tail_pos['x'] - cg_pos['x']
        dy_tail = tail_pos['y'] - cg_pos['y']
        dz_tail = tail_pos['z'] - cg_pos['z']
        
        Mx_tail = Fy_tail * dz_tail - Fz_tail * dy_tail
        My_tail = Fz_tail * dx_tail - Fx_tail * dz_tail
        Mz_tail = Fx_tail * dy_tail - Fy_tail * dx_tail - Q_tail  # Anti-torque
        
        # Stabilizer moments
        Mx_stab = stab_forces.get('M_pitch', 0)
        My_stab = 0  # No roll moment from stabilizers in this model
        Mz_stab = stab_forces.get('M_yaw', 0)
        
        # Total moments
        Mx_total = Mx_main + Mx_tail + Mx_stab
        My_total = My_main + My_tail + My_stab
        Mz_total = Mz_main + Mz_tail + Mz_stab
        
        # Update GUI variables
        self.thrust_main.set(T_main)
        self.thrust_tail.set(T_tail)
        self.power_main.set(P_main / 1000)  # Convert to kW
        self.power_tail.set(P_tail / 1000)
        self.moment_pitch.set(Mx_total)
        self.moment_roll.set(My_total)
        self.moment_yaw.set(Mz_total)
        
        return {
            'Fx': Fx_total, 'Fy': Fy_total, 'Fz': Fz_total,
            'Mx': Mx_total, 'My': My_total, 'Mz': Mz_total
        }
        
    def update_simulation(self):
        """Main simulation update loop"""
        if self.is_running:
            # Calculate current forces and moments
            forces_moments = self.calculate_forces_and_moments()
            
            # Update data logging
            current_time = time.time() - self.start_time
            self.time_data.append(current_time)
            
            for key in self.force_data:
                self.force_data[key].append(forces_moments[key])
            
            # Keep only last 100 data points for plotting
            if len(self.time_data) > 100:
                self.time_data = self.time_data[-100:]
                for key in self.force_data:
                    self.force_data[key] = self.force_data[key][-100:]
            
            # Update plots
            self.update_plots()
            
            # Update instrument displays
            self.update_instruments()
            
            # Update status
            self.time_label.config(text=f"Time: {current_time:.1f}s")
            self.status_label.config(text="Status: Running", bg='green')
        
        # Schedule next update
        self.root.after(100, self.update_simulation)  # 10 Hz update rate
        
    def update_plots(self):
        """Update real-time plots"""
        if len(self.time_data) > 1:
            # Update force plots
            force_keys = ['Fx', 'Fy', 'Fz']
            for i, key in enumerate(force_keys):
                self.force_lines[i].set_data(self.time_data, self.force_data[key])
            
            # Update moment plots
            moment_keys = ['Mx', 'My', 'Mz']
            for i, key in enumerate(moment_keys):
                self.moment_lines[i].set_data(self.time_data, self.force_data[key])
            
            # Rescale axes
            self.ax1.relim()
            self.ax1.autoscale_view()
            self.ax2.relim()
            self.ax2.autoscale_view()
            
            # Redraw
            self.canvas.draw_idle()
    
    def update_instruments(self):
        """Update instrument panel displays"""
        # Update aircraft state labels
        self.altitude_label.config(text=f"{self.altitude.get():.1f} m")
        self.forward_speed_label.config(text=f"{self.forward_speed.get():.1f} m/s")
        self.vertical_speed_label.config(text=f"{self.vertical_speed.get():.1f} m/s")
        
        # Update force and moment labels
        self.main_thrust_label.config(text=f"{self.thrust_main.get():.1f} N")
        self.tail_thrust_label.config(text=f"{self.thrust_tail.get():.1f} N")
        self.main_power_label.config(text=f"{self.power_main.get():.1f} kW")
        self.tail_power_label.config(text=f"{self.power_tail.get():.1f} kW")
        self.pitch_moment_label.config(text=f"{self.moment_pitch.get():.1f} N⋅m")
        self.roll_moment_label.config(text=f"{self.moment_roll.get():.1f} N⋅m")
        self.yaw_moment_label.config(text=f"{self.moment_yaw.get():.1f} N⋅m")
    
    def toggle_simulation(self):
        """Start/stop simulation"""
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.time_data = []
            for key in self.force_data:
                self.force_data[key] = []
            self.start_button.config(text="Stop Simulation")
            self.status_label.config(text="Status: Running", bg='green')
        else:
            self.is_running = False
            self.start_button.config(text="Start Simulation")
            self.status_label.config(text="Status: Stopped", bg='red')
    
    def reset_controls(self):
        """Reset all controls to default values"""
        self.collective_pitch.set(8.0)
        self.cyclic_pitch.set(0.0)
        self.cyclic_roll.set(0.0)
        self.tail_rotor_pitch.set(5.0)
        self.throttle.set(75.0)
        self.altitude.set(100.0)
        self.forward_speed.set(0.0)
        self.vertical_speed.set(0.0)
        
    def save_simulation_data(self):
        """Save simulation data to file"""
        if not self.time_data:
            messagebox.showwarning("No Data", "No simulation data to save!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flight_sim_data_{timestamp}.csv"
        
        try:
            with open(filename, 'w') as f:
                # Write header
                f.write("Time,Fx,Fy,Fz,Mx,My,Mz,Collective,Cyclic_Pitch,Cyclic_Roll,Tail_Pitch,Throttle\n")
                
                # Write data
                for i in range(len(self.time_data)):
                    f.write(f"{self.time_data[i]:.2f}")
                    for key in ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']:
                        f.write(f",{self.force_data[key][i]:.2f}")
                    f.write(f",{self.collective_pitch.get():.1f}")
                    f.write(f",{self.cyclic_pitch.get():.1f}")
                    f.write(f",{self.cyclic_roll.get():.1f}")
                    f.write(f",{self.tail_rotor_pitch.get():.1f}")
                    f.write(f",{self.throttle.get():.1f}\n")
            
            messagebox.showinfo("Data Saved", f"Simulation data saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data: {e}")

def main():
    """Main function to run the flight simulator GUI"""
    print("=== HAL HELICOPTER FLIGHT SIMULATOR GUI ===")
    print("Starting GUI application...")
    
    try:
        root = tk.Tk()
        app = FlightSimulatorGUI(root)
        
        print("✓ GUI initialized successfully")
        print("✓ Flight simulator ready")
        print("\nInstructions:")
        print("1. Adjust control sliders to change rotor settings")
        print("2. Click 'Start Simulation' to begin real-time updates")
        print("3. Watch forces and moments change in real-time plots")
        print("4. Use 'Save Data' to export simulation results")
        print("\nGUI is now running...")
        
        root.mainloop()
        
    except Exception as e:
        print(f"✗ GUI startup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()