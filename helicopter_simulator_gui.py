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
from datetime import datetime

# Add flight sim path
sys.path.append('flight_sim_part1')

from user_inputs import get_user_inputs, build_rotor
from atmosphere import isa_properties
from integrators import cycle_integrator
from blade import Blade
from rotor import Rotor
from airfoil import Airfoil

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
        
        # Data storage for plotting
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
        
        # Component positions relative to helicopter nose (meters)
        self.components = {
            'main_rotor': {'x': 0.0, 'y': 0.0, 'z': 2.5, 'mass': 200},
            'tail_rotor': {'x': -4.0, 'y': 0.0, 'z': 2.0, 'mass': 30},
            'fuselage': {'x': -1.0, 'y': 0.0, 'z': 1.0, 'mass': 1500},
            'engine': {'x': -0.5, 'y': 0.0, 'z': 1.5, 'mass': 300},
            'fuel': {'x': -1.5, 'y': 0.0, 'z': 1.0, 'mass': 400},
            'cg': {'x': -1.0, 'y': 0.0, 'z': 1.5}  # Center of gravity
        }
        
        print("✓ Helicopter simulator initialized")
        print(f"  Main rotor: {self.main_rotor.blade.R_tip:.2f}m radius")
        print(f"  Components positioned relative to aircraft reference frame")
        
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
        
        # Control buttons
        button_frame = tk.Frame(control_frame, bg='#34495e')
        button_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(button_frame, text="Reset Controls", command=self.reset_controls,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(fill=tk.X, pady=2)
        
        tk.Button(button_frame, text="Save Data", command=self.save_data,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(fill=tk.X, pady=2)
        
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
        
        # Performance info
        perf_frame = tk.LabelFrame(display_frame, text="Performance", 
                                  font=('Arial', 11, 'bold'), bg='#34495e', fg='white')
        perf_frame.pack(fill=tk.X, pady=5)
        
        self.perf_labels = {}
        perf_items = [('Thrust', 'N', '#e67e22'), ('Power', 'kW', '#8e44ad'), ('Efficiency', 'N/kW', '#16a085')]
        
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
        """Calculate forces and moments from helicopter components"""
        try:
            # Get atmospheric conditions
            rho, a = isa_properties(self.altitude.get())
            
            # Main rotor calculation
            rpm = 960 * (self.throttle.get() / 100.0)  # Scale RPM with throttle
            omega = 2 * np.pi * rpm / 60.0
            
            # Create main rotor with current collective pitch
            collective_rad = np.deg2rad(self.collective_pitch.get())
            cyclic_rad = np.deg2rad(self.cyclic_pitch.get())
            
            # Simple rotor model for demonstration
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
                main_rotor, self.forward_speed.get(), omega, rho)
            
            # Tail rotor (simplified)
            tail_pitch_rad = np.deg2rad(self.tail_rotor_pitch.get())
            T_tail = 500 * (tail_pitch_rad / np.deg2rad(10))  # Simplified model
            Q_tail = T_tail * 0.1  # Simplified torque
            
            # Transform to aircraft reference frame
            # Main rotor forces (affected by cyclic)
            Fx_main = T_main * np.sin(cyclic_rad)  # Forward/backward
            Fy_main = 0  # No lateral force from main rotor in this model
            Fz_main = T_main * np.cos(cyclic_rad)  # Vertical (up positive)
            
            # Tail rotor forces
            Fx_tail = 0
            Fy_tail = T_tail  # Side force for anti-torque
            Fz_tail = 0
            
            # Total forces
            Fx_total = Fx_main + Fx_tail
            Fy_total = Fy_main + Fy_tail
            Fz_total = Fz_main + Fz_tail
            
            # Calculate moments about center of gravity
            main_pos = self.components['main_rotor']
            tail_pos = self.components['tail_rotor']
            cg_pos = self.components['cg']
            
            # Moment arms
            dx_main = main_pos['x'] - cg_pos['x']
            dy_main = main_pos['y'] - cg_pos['y']
            dz_main = main_pos['z'] - cg_pos['z']
            
            dx_tail = tail_pos['x'] - cg_pos['x']
            dy_tail = tail_pos['y'] - cg_pos['y']
            dz_tail = tail_pos['z'] - cg_pos['z']
            
            # Moments (using cross product: r × F)
            # Main rotor moments
            Mx_main = Fy_main * dz_main - Fz_main * dy_main
            My_main = Fz_main * dx_main - Fx_main * dz_main
            Mz_main = Fx_main * dy_main - Fy_main * dx_main + Q_main
            
            # Tail rotor moments
            Mx_tail = Fy_tail * dz_tail - Fz_tail * dy_tail
            My_tail = Fz_tail * dx_tail - Fx_tail * dz_tail
            Mz_tail = Fx_tail * dy_tail - Fy_tail * dx_tail - Q_tail
            
            # Total moments
            Mx_total = Mx_main + Mx_tail
            My_total = My_main + My_tail
            Mz_total = Mz_main + Mz_tail
            
            # Update forces and moments
            self.forces_moments = {
                'Fx': Fx_total,
                'Fy': Fy_total,
                'Fz': Fz_total,
                'Mx': Mx_total,
                'My': My_total,
                'Mz': Mz_total
            }
            
            # Performance metrics
            self.performance = {
                'thrust': T_main,
                'power': P_main / 1000,  # kW
                'efficiency': T_main / (P_main / 1000) if P_main > 0 else 0
            }
            
        except Exception as e:
            print(f"Calculation error: {e}")
            # Set safe default values
            self.forces_moments = {key: 0.0 for key in self.forces_moments.keys()}
            self.performance = {'thrust': 0, 'power': 0, 'efficiency': 0}
    
    def update_displays(self):
        """Update all display elements"""
        # Update force and moment labels
        for key, label in self.force_labels.items():
            value = self.forces_moments[key]
            label.config(text=f"{value:.1f}")
        
        # Update performance labels
        self.perf_labels['Thrust'].config(text=f"{self.performance['thrust']:.1f} N")
        self.perf_labels['Power'].config(text=f"{self.performance['power']:.1f} kW")
        self.perf_labels['Efficiency'].config(text=f"{self.performance['efficiency']:.1f} N/kW")
        
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
        
        # Keep only last 100 points
        if len(self.time_data) > 100:
            self.time_data = self.time_data[-100:]
            for key in self.force_history:
                self.force_history[key] = self.force_history[key][-100:]
        
        # Update plots
        self.update_plots()
        
        # Schedule next update (10 Hz)
        self.root.after(100, self.update_loop)
    
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
        
    def save_data(self):
        """Save simulation data to CSV file"""
        if not self.time_data:
            messagebox.showwarning("No Data", "No simulation data to save!")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"helicopter_sim_data_{timestamp}.csv"
            
            with open(filename, 'w') as f:
                # Header
                f.write("Time,Fx,Fy,Fz,Mx,My,Mz,Collective,Cyclic,TailRotor,Throttle,Altitude,Speed\n")
                
                # Data
                for i in range(len(self.time_data)):
                    f.write(f"{self.time_data[i]:.2f}")
                    for key in ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']:
                        f.write(f",{self.force_history[key][i]:.2f}")
                    f.write(f",{self.collective_pitch.get():.1f}")
                    f.write(f",{self.cyclic_pitch.get():.1f}")
                    f.write(f",{self.tail_rotor_pitch.get():.1f}")
                    f.write(f",{self.throttle.get():.1f}")
                    f.write(f",{self.altitude.get():.1f}")
                    f.write(f",{self.forward_speed.get():.1f}\n")
            
            messagebox.showinfo("Success", f"Data saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

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
        print("4. Use 'Save Data' to export results for analysis")
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