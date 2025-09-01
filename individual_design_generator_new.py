#!/usr/bin/env python3
"""
Individual Helicopter Design Generator - Modular Version
Creates a compound helicopter design using modular components
"""

from individual_design import CompoundHelicopterDesigner


def main():
    """Main function"""
    designer = CompoundHelicopterDesigner()
    
    # Generate complete design
    designer.design_compound_helicopter()
    designer.generate_performance_plots()
    designer.analyze_hover_mission()
    designer.generate_design_summary()
    
    print("\n" + "="*60)
    print("INDIVIDUAL HELICOPTER DESIGN COMPLETE!")
    print("="*60)
    print(f"Check the '{designer.output_dir}' folder for all design files")
    print("Your compound helicopter design is ready for the individual report!")


if __name__ == "__main__":
    main()