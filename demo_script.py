#!/usr/bin/env python3
"""
Demo Script for Helicopter Simulator GUI
Demonstrates the bonus task requirements with automated control changes
"""

import time
from rotor_utils import rotor_calc

class HelicopterDemo:
    def __init__(self):
        print("=== HELICOPTER SIMULATOR DEMO ===")
        print("Demonstrating Bonus Task Requirements")
        print("="*50)
        
        # Component positions (as required by bonus task)
        self.components = {
            'main_rotor': {'x': 0.0, 'y': 0.0, 'z': 2.5},
            'tail_rotor': {'x': -4.0, 'y': 0.0, 'z': 2.0},
            'h_stabilizer': {'x': -4.5, 'y': 0.0, 'z': 1.5},
            'v_stabilizer': {'x': -4.5, 'y': 0.0, 'z': 2.0},
            'cg': {'x': -1.0, 'y': 0.0, 'z': 1.5}  # Center of gravity
        }
        
        print("Component Positions (relative to helicopter nose):")
        for comp, pos in self.components.items():
            print(f"  {comp}: X={pos['x']:.1f}m, Y={pos['y']:.1f}m, Z={pos['z']:.1f}m")
        
    def calculate_forces_moments(self, collective, cyclic_pitch, cyclic_roll, tail_pitch, throttle, altitude=100):
        """Calculate forces and moments using shared utilities"""
        return rotor_calc.calculate_forces_moments(
            collective, cyclic_pitch, cyclic_roll, tail_pitch, throttle, altitude
        )
    
    def run_demo_sequence(self):
        """Run 10-second demo sequence as required by bonus task"""
        print("\n" + "="*50)
        print("RUNNING 10-SECOND DEMO SEQUENCE")
        print("Changing controls sequentially and showing force/moment changes")
        print("="*50)
        
        # Demo sequence: Change controls every 2 seconds
        demo_steps = [
            {"name": "Hover (Baseline)", "collective": 8, "cyclic_pitch": 0, "cyclic_roll": 0, "tail_pitch": 5, "throttle": 80},
            {"name": "Increase Collective", "collective": 12, "cyclic_pitch": 0, "cyclic_roll": 0, "tail_pitch": 5, "throttle": 80},
            {"name": "Forward Cyclic", "collective": 10, "cyclic_pitch": 5, "cyclic_roll": 0, "tail_pitch": 5, "throttle": 80},
            {"name": "Right Cyclic", "collective": 10, "cyclic_pitch": 0, "cyclic_roll": 3, "tail_pitch": 5, "throttle": 80},
            {"name": "Increase Tail Rotor", "collective": 10, "cyclic_pitch": 0, "cyclic_roll": 0, "tail_pitch": 10, "throttle": 80},
        ]
        
        print(f"{'Time':<6} {'Step':<20} {'Fx':<8} {'Fy':<8} {'Fz':<8} {'Mx':<10} {'My':<10} {'Mz':<10}")
        print("-" * 80)
        
        start_time = time.time()
        
        for i, step in enumerate(demo_steps):
            # Calculate forces and moments
            results = self.calculate_forces_moments(
                step["collective"], step["cyclic_pitch"], step["cyclic_roll"], 
                step["tail_pitch"], step["throttle"]
            )
            
            # Display results
            elapsed = time.time() - start_time
            print(f"{elapsed:5.1f}s {step['name']:<20} "
                  f"{results['Fx']:7.1f} {results['Fy']:7.1f} {results['Fz']:7.1f} "
                  f"{results['Mx']:9.1f} {results['My']:9.1f} {results['Mz']:9.1f}")
            
            # Show control settings
            print(f"       Controls: Collective={step['collective']}°, "
                  f"Cyclic=({step['cyclic_pitch']}°,{step['cyclic_roll']}°), "
                  f"Tail={step['tail_pitch']}°, Throttle={step['throttle']}%")
            print()
            
            # Wait 2 seconds (simulating real-time demo)
            time.sleep(2)
        
        print("="*50)
        print("10-SECOND DEMO COMPLETE")
        print("✓ Demonstrated sequential control changes")
        print("✓ Showed forces and moments on all three axes")
        print("✓ Component placement effects included")
        print("✓ Real-time calculation demonstrated")
        
    def show_component_analysis(self):
        """Show component placement analysis"""
        print("\n" + "="*50)
        print("COMPONENT PLACEMENT ANALYSIS")
        print("="*50)
        
        print("Aircraft Configuration:")
        print("- Main Rotor: Primary lift generation")
        print("- Tail Rotor: Anti-torque and yaw control")
        print("- Horizontal Stabilizer: Pitch stability")
        print("- Vertical Stabilizer: Yaw stability")
        print("- Center of Gravity: Reference point for moments")
        
        print("\nMoment Calculation Method:")
        print("- Forces calculated from rotor performance")
        print("- Moments = r × F (cross product of position and force)")
        print("- All moments calculated about aircraft center of gravity")
        print("- Component placement affects moment arms")
        
        # Example calculation
        baseline = self.calculate_forces_moments(8, 0, 0, 5, 80)
        
        print(f"\nBaseline Hover Condition:")
        print(f"- Forces: Fx={baseline['Fx']:.1f}N, Fy={baseline['Fy']:.1f}N, Fz={baseline['Fz']:.1f}N")
        print(f"- Moments: Mx={baseline['Mx']:.1f}N⋅m, My={baseline['My']:.1f}N⋅m, Mz={baseline['Mz']:.1f}N⋅m")
        print(f"- Performance: {baseline['thrust']:.1f}N thrust, {baseline['power']:.1f}kW power")

def main():
    """Main demo function"""
    demo = HelicopterDemo()
    
    # Show component analysis
    demo.show_component_analysis()
    
    # Run the 10-second demo sequence
    demo.run_demo_sequence()
    
    print("\n" + "="*50)
    print("BONUS TASK DEMONSTRATION COMPLETE")
    print("="*50)
    print("This demo shows:")
    print("✓ Component placement and reference frame")
    print("✓ Real-time force and moment calculations")
    print("✓ Sequential control input changes")
    print("✓ All three axes forces (Fx, Fy, Fz)")
    print("✓ All three axes moments (Mx, My, Mz)")
    print("✓ Integration with flight simulation system")
    print("\nFor interactive GUI demo, run: python helicopter_simulator_gui.py")

if __name__ == "__main__":
    main()