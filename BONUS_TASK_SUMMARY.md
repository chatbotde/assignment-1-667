# Bonus Task: Flight Simulator - Complete

## Status: Implemented ✅

Interactive helicopter flight simulator with real-time force and moment calculations.

## Key Features

- **Real-time Controls**: Collective, cyclic, tail rotor pitch, throttle
- **Live Force Display**: Fx, Fy, Fz with color coding
- **Live Moment Display**: Mx, My, Mz about center of gravity
- **Interactive Plots**: Real-time force/moment history
- **Data Export**: CSV export functionality

## Component Positions

| Component | X (m) | Y (m) | Z (m) |
|-----------|-------|-------|-------|
| Main Rotor | 0.0 | 0.0 | 2.5 |
| Tail Rotor | -4.0 | 0.0 | 2.0 |
| Center of Gravity | -1.0 | 0.0 | 1.5 |

## Usage

```bash
# Interactive GUI
python helicopter_simulator_gui.py

# Automated demo
python demo_script.py
```

## Files Generated
- `helicopter_simulator_gui.py` - Main GUI application
- `demo_script.py` - Automated demonstration
- `rotor_utils.py` - Shared calculation utilities