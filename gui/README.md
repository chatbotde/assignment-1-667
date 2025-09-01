# Helicopter Simulator GUI - Modular Structure

This directory contains the modular version of the helicopter simulator GUI, broken down from the original large `helicopter_simulator_gui.py` file.

## File Structure

```
gui/
├── __init__.py                 # Package initialization
├── helicopter_gui_main.py      # Main application class and entry point
├── control_panel.py           # Pilot control interface (sliders, buttons)
├── display_panel.py           # Forces/moments display panel
├── plot_panel.py              # Real-time plotting functionality
├── simulation_engine.py       # Simulation calculations and data management
└── README.md                  # This file
```

## Components

### 1. `helicopter_gui_main.py`
- Main application class `HelicopterSimulatorGUI`
- GUI initialization and layout
- Main update loop coordination
- Control variable management

### 2. `control_panel.py`
- `ControlPanel` class for pilot controls
- Slider creation and management
- Control reset functionality
- User input handling

### 3. `display_panel.py`
- `DisplayPanel` class for forces/moments display
- Real-time value updates
- Performance metrics display
- Color-coded force/moment indicators

### 4. `plot_panel.py`
- `PlotPanel` class for real-time plotting
- Matplotlib integration
- Force and moment time-series plots
- Auto-scaling and legend management

### 5. `simulation_engine.py`
- `SimulationEngine` class for calculations
- Forces and moments computation
- Data history management
- Integration with flight simulation components

## Usage

### Running the Modular GUI
```bash
python helicopter_simulator_gui_new.py
```

### Importing Components
```python
from gui import HelicopterSimulatorGUI, ControlPanel, DisplayPanel
from gui.simulation_engine import SimulationEngine
```

## Benefits of Modular Structure

1. **Maintainability**: Each component has a single responsibility
2. **Testability**: Individual components can be tested in isolation
3. **Reusability**: Components can be reused in other applications
4. **Readability**: Smaller files are easier to understand and modify
5. **Collaboration**: Multiple developers can work on different components

## Migration from Original File

The original `helicopter_simulator_gui.py` (800+ lines) has been split into:
- Main app: ~80 lines
- Control panel: ~80 lines  
- Display panel: ~70 lines
- Plot panel: ~80 lines
- Simulation engine: ~120 lines

Total: ~430 lines across 5 focused files instead of one large file.

## Dependencies

- tkinter (GUI framework)
- matplotlib (plotting)
- numpy (numerical operations)
- flight_sim_part1 package (simulation components)
- rotor_utils (shared calculation utilities)