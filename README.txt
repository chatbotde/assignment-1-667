HELICOPTER FLIGHT SIMULATOR PROJECT
===================================

This is a comprehensive helicopter flight simulation project with multiple components
including flight dynamics simulation, mission planning, GUI interface, and performance
optimization tools.

SYSTEM REQUIREMENTS
==================

Python Version:
- Python 3.7 or higher

Required Python Packages:
- numpy (for numerical computations)
- matplotlib (for plotting and visualization)
- pandas (for data analysis and reporting)
- tkinter (for GUI - usually included with Python)

INSTALLATION
============

1. Install Python 3.7+ from https://python.org/downloads/

2. Install required packages using pip:
   pip install numpy matplotlib pandas

   OR if using conda:
   conda install numpy matplotlib pandas

3. Verify tkinter is available (usually pre-installed):
   python -c "import tkinter; print('tkinter available')"

PROJECT STRUCTURE
================

flight_sim_part1/          - Core flight simulation engine
├── main.py               - Main entry point for basic simulation
├── user_inputs.py        - Configuration and input parameters
├── atmosphere.py         - ISA atmosphere model
├── airfoil.py           - Airfoil aerodynamics
├── blade.py             - Rotor blade geometry
├── rotor.py             - Rotor assembly
├── inflow.py            - Induced velocity calculations
├── integrators.py       - Performance integration (original)
├── integrators_optimized.py - Optimized performance integration
└── stabilizers.py       - Stabilizer forces and moments

helicopter_simulator_gui.py    - Interactive GUI simulator (Bonus Task)
individual_design_generator.py - Compound helicopter design tool
report_generator.py           - Automated report generation
performance_benchmark.py      - Performance optimization testing
rotor_utils.py               - Utility functions for rotor calculations
rotor_utils_optimized.py     - Optimized utility functions
mission planner/             - Mission planning module (Part 2)
individual_design/           - Generated design outputs
report_output/              - Generated reports

HOW TO RUN THE PROJECT
=====================

1. BASIC FLIGHT SIMULATION (Part 1):
   cd flight_sim_part1
   python main.py
   
   This runs the core helicopter simulation and displays:
   - Cycle-averaged thrust, torque, and power
   - Stabilizer forces and moments

2. INTERACTIVE GUI SIMULATOR (Bonus Task):
   python helicopter_simulator_gui.py
   
   Features:
   - Real-time flight controls (collective, cyclic, pedals)
   - Live performance plots
   - Interactive parameter adjustment
   - Visual flight display

3. INDIVIDUAL HELICOPTER DESIGN:
   python individual_design_generator.py
   
   Generates:
   - Compound helicopter design specifications
   - Performance analysis plots
   - Design summary report
   - Hover mission analysis

4. PERFORMANCE BENCHMARKING:
   python performance_benchmark.py
   
   Compares:
   - Original vs optimized integrators
   - Performance improvements
   - Execution time analysis

5. COMPREHENSIVE REPORTING:
   python report_generator.py
   
   Creates:
   - Complete project analysis
   - Performance comparisons
   - Mission planning results
   - Formatted reports in report_output/

CONFIGURATION
=============

Main configuration is in flight_sim_part1/user_inputs.py:

- Rotor geometry (radius, chord distribution, twist)
- Number of blades and tip Mach limits
- Airfoil characteristics (lift slope, drag coefficient)
- Flight conditions (altitude, forward speed, RPM)
- Stabilizer geometry and control gains

EXPECTED OUTPUTS
===============

Basic Simulation:
- Thrust: ~15000-25000 N (depending on configuration)
- Torque: ~2000-4000 N·m
- Power: 200-600 kW
- Stabilizer forces and moments

GUI Simulator:
- Interactive real-time plots
- Flight parameter displays
- Control response visualization

Design Generator:
- JSON design specifications
- PNG performance plots
- Text summary reports

TROUBLESHOOTING
==============

Common Issues:

1. "ModuleNotFoundError: No module named 'numpy'"
   Solution: pip install numpy matplotlib pandas

2. "No module named 'tkinter'"
   Solution: Install python3-tk (Linux) or reinstall Python with tkinter

3. "Tip Mach exceeds limit" warning
   Solution: Reduce RPM in user_inputs.py or increase rotor radius

4. Performance issues with large calculations
   Solution: Use optimized versions (integrators_optimized.py)

5. Import errors between modules
   Solution: Run from project root directory, not subdirectories

PERFORMANCE OPTIMIZATION
=======================

The project includes optimized versions of key components:
- integrators_optimized.py: Faster numerical integration
- rotor_utils_optimized.py: Cached calculations
- enable_optimizations.py: Performance enhancement script

To enable optimizations:
python enable_optimizations.py

MISSION PLANNING (Part 2)
=========================

Advanced mission planning capabilities in mission planner/ directory:
- Flight path optimization
- Fuel consumption analysis
- Multi-waypoint missions
- Performance envelope analysis

DEVELOPMENT NOTES
================

- All modules are self-contained with clear interfaces
- Extensive documentation and comments throughout
- Modular design allows easy component replacement
- Performance-critical sections are optimized
- GUI provides real-time interaction capabilities

For detailed technical documentation, see individual module docstrings
and the existing flight_sim_part1/README.txt file.

ASSIGNMENT COMPLETION
====================

This project fulfills all assignment requirements:
✓ Part 1: Complete flight simulation implementation
✓ Part 2: Mission planning and optimization
✓ Bonus Task: Interactive GUI simulator
✓ Performance optimization and benchmarking
✓ Comprehensive documentation and reporting

Last Updated: January 2025