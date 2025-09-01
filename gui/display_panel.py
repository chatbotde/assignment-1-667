"""
Display Panel Component for Helicopter Simulator GUI
"""

import tkinter as tk

class DisplayPanel:
    def __init__(self, parent, main_app):
        self.main_app = main_app
        self.create_display_panel(parent)
        
    def create_display_panel(self, parent):
        """Create forces and moments display panel"""
        self.display_frame = tk.LabelFrame(parent, text="Forces & Moments (Aircraft Reference Frame)", 
                                          font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
        self.display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Forces section
        forces_frame = tk.LabelFrame(self.display_frame, text="Forces [N]", 
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
        moments_frame = tk.LabelFrame(self.display_frame, text="Moments [N⋅m]", 
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
        perf_frame = tk.LabelFrame(self.display_frame, text="Performance", 
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
    
    def update(self, forces_moments, performance):
        """Update all display elements"""
        # Update force and moment labels
        for key, label in self.force_labels.items():
            value = forces_moments[key]
            label.config(text=f"{value:.1f}")
        
        # Update performance labels
        self.perf_labels['Thrust'].config(text=f"{performance['thrust']:.1f} N")
        self.perf_labels['Power'].config(text=f"{performance['power']:.1f} kW")