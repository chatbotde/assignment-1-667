#!/usr/bin/env python3
"""
Main Helicopter Designer Class
Coordinates the overall design process
"""

import os
import json
from datetime import datetime
from .design_requirements import DesignRequirements
from .rotor_designer import RotorDesigner
from .aircraft_sizer import AircraftSizer
from .performance_analyzer import PerformanceAnalyzer
from .plot_generator import PlotGenerator
from .report_generator import ReportGenerator


class CompoundHelicopterDesigner:
    def __init__(self):
        print("=== COMPOUND HELICOPTER DESIGN GENERATOR ===")
        self.requirements = DesignRequirements()
        self.rotor_designer = RotorDesigner()
        self.aircraft_sizer = AircraftSizer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.plot_generator = PlotGenerator()
        self.report_generator = ReportGenerator()
        
        self.create_output_directory()
        
    def create_output_directory(self):
        """Create output directory"""
        self.output_dir = "individual_design"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print(f"✓ Output directory: {self.output_dir}")

    def design_compound_helicopter(self):
        """Design the compound helicopter"""
        print("\n=== DESIGNING COMPOUND HELICOPTER ===")
        
        # Design philosophy
        self.helicopter_design = {
            "concept": "Compound Helicopter with Pusher Propeller",
            "configuration": "Single main rotor + tail rotor + pusher propeller + wings",
            "design_philosophy": "Optimized for high-speed cruise with rotor unloading"
        }
        
        # Design all components
        self.main_rotor = self.rotor_designer.design_main_rotor()
        self.tail_rotor = self.rotor_designer.design_tail_rotor()
        self.pusher_prop = self.rotor_designer.design_pusher_propeller()
        self.wings = self.rotor_designer.design_wings()
        
        # Size the aircraft
        self.mass_breakdown, self.dimensions = self.aircraft_sizer.size_aircraft(
            self.requirements.get_requirements(),
            self.main_rotor,
            self.tail_rotor,
            self.pusher_prop,
            self.wings
        )
        
        print("✓ Compound helicopter design completed")

    def generate_performance_plots(self):
        """Generate performance plots for all rotors"""
        print("\n=== GENERATING PERFORMANCE PLOTS ===")
        
        self.plot_generator.set_output_dir(self.output_dir)
        self.plot_generator.plot_rotor_performance_comparison(self.main_rotor, self.tail_rotor)
        self.plot_generator.plot_thrust_vs_collective(self.main_rotor, self.tail_rotor)
        self.plot_generator.plot_power_vs_collective(self.main_rotor, self.tail_rotor)
        self.plot_generator.plot_thrust_vs_power(self.main_rotor, self.tail_rotor)
        
        print("✓ Performance plots generated")

    def analyze_hover_mission(self):
        """Analyze hover mission at 2000m"""
        print("\n=== HOVER MISSION ANALYSIS ===")
        
        hover_results = self.performance_analyzer.analyze_hover_mission(
            self.main_rotor, altitude=2000
        )
        
        # Save results
        with open(f"{self.output_dir}/hover_analysis.json", 'w') as f:
            json.dump(hover_results, f, indent=2)
        
        # Generate hover plots
        self.plot_generator.plot_hover_mission_analysis(hover_results, self.output_dir)
        
        print(f"  Max weight (thrust): {hover_results['max_weight_thrust_kg']:.0f} kg")
        print(f"  Max weight (power): {hover_results['max_weight_power_kg']:.0f} kg")

    def generate_design_summary(self):
        """Generate comprehensive design summary"""
        print("\n=== GENERATING DESIGN SUMMARY ===")
        
        # Analyze main rotor performance
        main_rotor_performance = self.performance_analyzer.analyze_main_rotor_performance(
            self.main_rotor
        )
        
        # Create design data
        design_data = {
            "main_rotor": self.main_rotor,
            "tail_rotor": self.tail_rotor,
            "pusher_propeller": self.pusher_prop,
            "wings": self.wings,
            "mass_breakdown": self.mass_breakdown,
            "dimensions": self.dimensions,
            "performance": main_rotor_performance,
            "requirements": self.requirements.get_requirements()
        }
        
        # Generate reports
        self.report_generator.generate_design_json(design_data, self.output_dir)
        summary = self.report_generator.generate_design_summary(
            self.helicopter_design, design_data, self.output_dir
        )
        
        print(summary)
        print(f"\n✓ Design summary completed!")
        print(f"✓ All files saved to: {self.output_dir}/")