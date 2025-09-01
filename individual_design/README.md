# Individual Helicopter Design - Modular Structure

This directory contains the modular helicopter design system, broken down from the original monolithic `individual_design_generator.py` file.

## Module Structure

### Core Modules

1. **`helicopter_designer.py`** - Main coordinator class
   - Orchestrates the entire design process
   - Manages component integration
   - Coordinates output generation

2. **`design_requirements.py`** - Requirements management
   - Defines design requirements and constraints
   - Validates requirement feasibility
   - Allows requirement updates

3. **`rotor_designer.py`** - Rotor and propulsion design
   - Main rotor design
   - Tail rotor design
   - Pusher propeller design
   - Wing design for compound configuration

4. **`aircraft_sizer.py`** - Aircraft sizing and mass estimation
   - Overall aircraft dimensions
   - Mass breakdown calculations
   - Component mass estimation

5. **`performance_analyzer.py`** - Performance calculations
   - Rotor performance analysis
   - Hover mission analysis
   - Flight performance calculations

6. **`plot_generator.py`** - Visualization and plotting
   - Performance comparison plots
   - Thrust/power characteristic plots
   - Mission analysis visualizations

7. **`report_generator.py`** - Report and documentation
   - Design summary generation
   - JSON data export
   - Performance reports

## Usage

### Using the New Modular System

```python
from individual_design import CompoundHelicopterDesigner

# Create designer instance
designer = CompoundHelicopterDesigner()

# Run complete design process
designer.design_compound_helicopter()
designer.generate_performance_plots()
designer.analyze_hover_mission()
designer.generate_design_summary()
```

### Using Individual Modules

```python
from individual_design import DesignRequirements, RotorDesigner

# Use specific modules
requirements = DesignRequirements()
rotor_designer = RotorDesigner()

main_rotor = rotor_designer.design_main_rotor()
```

## Benefits of Modular Structure

1. **Maintainability** - Each module has a single responsibility
2. **Testability** - Individual components can be tested separately
3. **Reusability** - Modules can be used in other projects
4. **Extensibility** - Easy to add new features or modify existing ones
5. **Readability** - Smaller, focused files are easier to understand

## Migration from Original File

The original `individual_design_generator.py` has been replaced by:
- `individual_design_generator_new.py` - New main script using modular design
- `individual_design/` package - All modular components

## Output Files

The system generates the same output files as the original:
- `compound_helicopter_design.json`
- `design_summary.txt`
- `hover_analysis.json`
- Various performance plots (PNG files)

## Dependencies

- NumPy
- Matplotlib
- Flight simulation modules from `flight_sim_part1/`
- Optional: `rotor_utils` for advanced calculations