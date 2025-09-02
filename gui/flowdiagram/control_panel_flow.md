# Control Panel Flow Diagram

```mermaid
flowchart TD
    A[Start: ControlPanel] --> B[Initialize<br/>parent, main_app reference]
    B --> C[create_control_panel Method]
    
    C --> D[Create Control Frame<br/>LabelFrame: "Pilot Controls"]
    D --> E[Create Flight Control Sliders]
    
    E --> F[Collective Pitch Slider<br/>Range: 0-20°, Default: 8.0°<br/>Description: "Controls main rotor thrust"]
    F --> G[Cyclic Pitch Slider<br/>Range: -10 to +10°, Default: 0.0°<br/>Description: "Controls forward/backward tilt"]
    G --> H[Tail Rotor Pitch Slider<br/>Range: 0-15°, Default: 5.0°<br/>Description: "Controls yaw/anti-torque"]
    H --> I[Throttle Slider<br/>Range: 0-100%, Default: 80%<br/>Description: "Controls engine power"]
    
    I --> J[Create Flight Conditions Section<br/>Label: "Flight Conditions"]
    J --> K[Altitude Slider<br/>Range: 0-3000m, Default: 100m<br/>Description: "Flight altitude"]
    K --> L[Forward Speed Slider<br/>Range: 0-50 m/s, Default: 0 m/s<br/>Description: "Forward flight speed"]
    
    L --> M[Create Control Buttons<br/>Reset Controls button]
    
    N[create_control_slider Method] --> O[Input: name, variable, min_val, max_val, unit, description]
    O --> P[Create Container Frame]
    P --> Q[Create Label<br/>Display control name]
    Q --> R[Create Slider Frame<br/>Container for slider + value]
    R --> S[Create Scale Widget<br/>Horizontal slider with range]
    S --> T[Create Value Label<br/>Display current value + unit]
    T --> U[Setup Variable Trace<br/>Update label when value changes]
    U --> V[Create Description Label<br/>Help text for control]
    
    W[Variable Trace Callback] --> X[Get Current Variable Value]
    X --> Y[Format Value with Unit<br/>"{value:.1f}{unit}"]
    Y --> Z[Update Value Label Display]
    
    M --> AA[End]
    V --> AA
    Z --> AA

    style A fill:#e1f5fe
    style AA fill:#e8f5e8
    style C fill:#e3f2fd
    style N fill:#e3f2fd
    style W fill:#e3f2fd
    style E fill:#fff3e0
    style J fill:#fff3e0
    style F fill:#f3e5f5
    style G fill:#f3e5f5
    style H fill:#f3e5f5
    style I fill:#f3e5f5
    style K fill:#f3e5f5
    style L fill:#f3e5f5
    style S fill:#ffeb3b
    style U fill:#ffeb3b
```

## Control Panel Component
**Purpose**: Provide pilot controls for helicopter flight parameters

### Flight Control Sliders
1. **Collective Pitch** (0-20°)
   - Controls main rotor thrust generation
   - Primary control for vertical movement
   - Default: 8.0° (moderate thrust)

2. **Cyclic Pitch** (-10° to +10°)
   - Controls forward/backward helicopter tilt
   - Affects longitudinal movement
   - Default: 0.0° (level attitude)

3. **Tail Rotor Pitch** (0-15°)
   - Controls anti-torque and yaw movement
   - Counteracts main rotor torque
   - Default: 5.0° (balanced torque)

4. **Throttle** (0-100%)
   - Controls engine power output
   - Affects rotor RPM and available power
   - Default: 80% (normal operating power)

### Flight Condition Controls
1. **Altitude** (0-3000m)
   - Sets flight altitude for atmospheric calculations
   - Affects air density and performance
   - Default: 100m (low altitude flight)

2. **Forward Speed** (0-50 m/s)
   - Sets forward flight velocity
   - Affects aerodynamic forces and power
   - Default: 0 m/s (hover condition)

### Slider Implementation
**create_control_slider Method**:
- **Container**: Frame for each control group
- **Label**: Control name and description
- **Scale Widget**: Horizontal slider with defined range
- **Value Display**: Real-time value with units
- **Variable Trace**: Automatic update when value changes

### Key Features
- **Real-time Updates**: Values update immediately when sliders move
- **Visual Feedback**: Color-coded value displays
- **Descriptive Labels**: Help text for each control
- **Reset Functionality**: Return all controls to defaults
- **Responsive Design**: Scales with window size

### Integration Points
- **Main App Variables**: Direct binding to Tkinter DoubleVar
- **Simulation Engine**: Values passed to physics calculations
- **Real-time Loop**: Continuous monitoring of control changes