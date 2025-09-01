"""
Plot Panel Component for Helicopter Simulator GUI
"""

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PlotPanel:
    def __init__(self, parent, main_app):
        self.main_app = main_app
        self.create_plot_panel(parent)
        
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
        
    def update(self, time_data, force_history):
        """Update real-time plots"""
        if len(time_data) > 1:
            # Update force lines
            force_keys = ['Fx', 'Fy', 'Fz']
            for i, key in enumerate(force_keys):
                self.force_lines[i].set_data(time_data, force_history[key])
            
            # Update moment lines
            moment_keys = ['Mx', 'My', 'Mz']
            for i, key in enumerate(moment_keys):
                self.moment_lines[i].set_data(time_data, force_history[key])
            
            # Rescale axes
            if len(time_data) > 2:
                self.ax1.relim()
                self.ax1.autoscale_view()
                self.ax2.relim()
                self.ax2.autoscale_view()
            
            # Redraw
            try:
                self.canvas.draw_idle()
            except:
                pass  # Ignore drawing errors