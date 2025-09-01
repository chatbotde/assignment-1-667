"""
Control Panel Component for Helicopter Simulator GUI
"""

import tkinter as tk
from tkinter import ttk

class ControlPanel:
    def __init__(self, parent, main_app):
        self.main_app = main_app
        self.create_control_panel(parent)
        
    def create_control_panel(self, parent):
        """Create pilot control panel"""
        self.control_frame = tk.LabelFrame(parent, text="Pilot Controls", 
                                          font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Collective Control
        self.create_control_slider("Collective Pitch", self.main_app.collective_pitch, 
                                 0, 20, "°", "Controls main rotor thrust")
        
        # Cyclic Control
        self.create_control_slider("Cyclic Pitch", self.main_app.cyclic_pitch, 
                                 -10, 10, "°", "Controls forward/backward tilt")
        
        # Tail Rotor Control
        self.create_control_slider("Tail Rotor Pitch", self.main_app.tail_rotor_pitch, 
                                 0, 15, "°", "Controls yaw/anti-torque")
        
        # Throttle Control
        self.create_control_slider("Throttle", self.main_app.throttle, 
                                 0, 100, "%", "Controls engine power")
        
        # Flight Condition Controls
        tk.Label(self.control_frame, text="Flight Conditions", font=('Arial', 10, 'bold'),
                bg='#34495e', fg='white').pack(pady=(20, 5))
        
        self.create_control_slider("Altitude", self.main_app.altitude, 
                                 0, 3000, "m", "Flight altitude")
        
        self.create_control_slider("Forward Speed", self.main_app.forward_speed, 
                                 0, 50, "m/s", "Forward flight speed")
        
        # Control buttons
        button_frame = tk.Frame(self.control_frame, bg='#34495e')
        button_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(button_frame, text="Reset Controls", command=self.main_app.reset_controls,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(fill=tk.X, pady=2)
        
    def create_control_slider(self, name, variable, min_val, max_val, unit, description):
        """Create a control slider with label"""
        frame = tk.Frame(self.control_frame, bg='#34495e')
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