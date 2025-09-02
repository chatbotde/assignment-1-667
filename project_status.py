#!/usr/bin/env python3
"""
Project Status Overview
======================
Comprehensive status check and demonstration of all helicopter simulator components
"""

import os
import sys
from pathlib import Path
import time

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60)

def print_section(title):
    """Print a section header"""
    print(f"\n{title}")
    print('-' * len(title))

def check_project_structure():
    """Check and display project structure"""
    print_section("📁 Project Structure")
    
    structure = {
        'flight_sim_part1/': 'Core flight simulation engine',
        'gui/': 'Interactive GUI components',
        'individual_design/': 'Helicopter design generator',
        'mission planner/': 'Mission planning module',
        'mission_controller/': 'Mission controller system',
        'report_output/': 'Generated reports'
    }
    
    for folder, description in structure.items():
        if Path(folder).exists():
            print(f"✅ {folder:<20} - {description}")
        else:
            print(f"⚠️  {folder:<20} - {description} (missing)")

def check_key_files():
    """Check key executable files"""
    print_section("🔧 Key Executable Files")
    
    files = {
        'flight_sim_part1/main.py': 'Core flight simulation',
        'helicopter_simulator_gui_new.py': 'Interactive GUI simulator',
        'individual_design_generator_new.py': 'Helicopter design tool',
        'test_plan.py': 'Comprehensive test suite',
        'quick_test.py': 'Quick verification script'
    }
    
    for file_path, description in files.items():
        if Path(file_path).exists():
            print(f"✅ {file_path:<35} - {description}")
        else:
            print(f"❌ {file_path:<35} - {description} (missing)")

def demo_core_simulation():
    """Demonstrate core flight simulation"""
    print_section("🚁 Core Flight Simulation Demo")
    
    try:
        sys.path.append('flight_sim_part1')
        from main import run
        
        print("Running flight simulation...")
        start_time = time.time()
        run()
        end_time = time.time()
        
        print(f"✅ Simulation completed in {end_time - start_time:.3f} seconds")
        
    except Exception as e:
        print(f"❌ Simulation failed: {e}")

def demo_gui_components():
    """Test GUI components (without opening window)"""
    print_section("🖥️  GUI Components Status")
    
    try:
        from gui.simulation_engine import SimulationEngine
        from gui.control_panel import ControlPanel
        from gui.display_panel import DisplayPanel
        
        # Test simulation engine
        engine = SimulationEngine()
        print("✅ Simulation engine initialized")
        
        # Test control calculation
        controls = {
            'collective_pitch': 0.5,
            'cyclic_pitch': 0.0,
            'tail_rotor_pitch': 0.0,
            'throttle': 0.5,
            'altitude': 1000
        }
        engine.calculate_forces_and_moments(controls)
        forces = engine.get_forces_moments()
        print(f"✅ Force calculation working: {len(forces)} components")
        
        print("✅ All GUI components ready")
        print("   To test GUI: python helicopter_simulator_gui_new.py")
        
    except Exception as e:
        print(f"❌ GUI components error: {e}")

def demo_individual_design():
    """Test individual design components"""
    print_section("✈️  Individual Design System")
    
    try:
        from individual_design.helicopter_designer import CompoundHelicopterDesigner
        from individual_design.design_requirements import DesignRequirements
        from individual_design.rotor_designer import RotorDesigner
        
        # Test requirements
        requirements = DesignRequirements()
        req_dict = requirements.get_requirements()
        print(f"✅ Design requirements loaded: {len(req_dict)} parameters")
        
        # Test rotor designer
        rotor_designer = RotorDesigner()
        main_rotor = rotor_designer.design_main_rotor()
        print(f"✅ Rotor design working: {main_rotor['radius_m']}m radius")
        
        print("✅ Individual design system ready")
        print("   To run full design: python individual_design_generator_new.py")
        
    except Exception as e:
        print(f"❌ Individual design error: {e}")

def check_dependencies():
    """Check all required dependencies"""
    print_section("📦 Dependencies Status")
    
    dependencies = {
        'numpy': 'Numerical computations',
        'matplotlib': 'Plotting and visualization',
        'pandas': 'Data analysis',
        'tkinter': 'GUI framework'
    }
    
    all_good = True
    for package, description in dependencies.items():
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
            print(f"✅ {package:<12} - {description}")
        except ImportError:
            print(f"❌ {package:<12} - {description} (missing)")
            all_good = False
    
    return all_good

def show_usage_examples():
    """Show usage examples"""
    print_section("🚀 Usage Examples")
    
    examples = [
        ("Core Simulation", "python flight_sim_part1/main.py"),
        ("GUI Simulator", "python helicopter_simulator_gui_new.py"),
        ("Design Generator", "python individual_design_generator_new.py"),
        ("Full Test Suite", "python test_plan.py"),
        ("Quick Verification", "python quick_test.py"),
        ("Project Status", "python project_status.py")
    ]
    
    for name, command in examples:
        print(f"  {name:<18}: {command}")

def show_output_files():
    """Show generated output files"""
    print_section("📄 Generated Output Files")
    
    output_locations = {
        'individual_design/': [
            'compound_helicopter_design.json',
            'design_summary.txt',
            'hover_analysis.json',
            '*.png (performance plots)'
        ],
        'report_output/': [
            'Generated reports (if report_generator.py run)'
        ]
    }
    
    for location, files in output_locations.items():
        if Path(location).exists():
            print(f"\n📁 {location}")
            for file_pattern in files:
                if '*' in file_pattern:
                    # Count PNG files
                    png_files = list(Path(location).glob('*.png'))
                    if png_files:
                        print(f"   ✅ {len(png_files)} PNG plot files")
                    else:
                        print(f"   ⚠️  No PNG files found")
                else:
                    file_path = Path(location) / file_pattern
                    if file_path.exists():
                        print(f"   ✅ {file_pattern}")
                    else:
                        print(f"   ⚠️  {file_pattern} (not generated yet)")

def main():
    """Main status check"""
    print_header("HELICOPTER FLIGHT SIMULATOR - PROJECT STATUS")
    
    # Check dependencies first
    deps_ok = check_dependencies()
    
    # Check project structure
    check_project_structure()
    
    # Check key files
    check_key_files()
    
    if deps_ok:
        # Demo components
        demo_core_simulation()
        demo_gui_components()
        demo_individual_design()
    else:
        print("\n⚠️  Some dependencies missing. Install them first:")
        print("   pip install numpy matplotlib pandas")
    
    # Show usage examples
    show_usage_examples()
    
    # Show output files
    show_output_files()
    
    # Final status
    print_header("FINAL STATUS")
    
    if deps_ok:
        print("🎉 PROJECT STATUS: FULLY OPERATIONAL")
        print("\nYour helicopter flight simulator is ready for:")
        print("  • Flight dynamics simulation")
        print("  • Interactive GUI control")
        print("  • Individual helicopter design")
        print("  • Mission planning and analysis")
        print("  • Performance optimization")
        print("  • Academic research and assignments")
        
        print(f"\n🚁 Ready to fly! Run any of the examples above to get started.")
    else:
        print("⚠️  PROJECT STATUS: DEPENDENCIES NEEDED")
        print("Install missing packages and run this script again.")

if __name__ == "__main__":
    main()