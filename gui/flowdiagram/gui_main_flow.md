# GUI Main Application Flow Diagram

```mermaid
flowchart TD
    A[Start: HelicopterSimulatorGUI] --> B[Initialize Root Window<br/>Title: HAL Helicopter Flight Simulator<br/>Size: 1200x800, Background: #34495e]
    
    B --> C[Initialize Simulation Engine<br/>self.simulation = SimulationEngine()]
    C --> D[Initialize Control Variables<br/>collective_pitch=8.0, cyclic_pitch=0.0<br/>tail_rotor_pitch=5.0, throttle=80.0<br/>altitude=100.0, forward_speed=0.0]
    
    D --> E[create_gui Method]
    E --> F[Create Title Frame<br/>Main title + subtitle]
    F --> G[Create Main Content Frame<br/>Container for all panels]
    G --> H[Initialize GUI Panels<br/>ControlPanel, DisplayPanel, PlotPanel]
    
    H --> I[Start Update Loop<br/>self.update_loop()]
    
    I --> J[Update Loop Execution]
    J --> K[Get Control Values<br/>controls = get_control_values()]
    K --> L[Update Simulation<br/>simulation.update(controls)]
    L --> M[Update Display Panel<br/>forces_moments, performance]
    M --> N[Update Plot Panel<br/>time_data, force_history]
    N --> O[Schedule Next Update<br/>root.after(200ms, update_loop)]
    O --> P{Continue Running?}
    P -->|Yes| J
    P -->|No| Q[End Application]
    
    R[get_control_values Method] --> S[Return Control Dictionary<br/>collective_pitch, cyclic_pitch<br/>tail_rotor_pitch, throttle<br/>altitude, forward_speed]
    
    T[reset_controls Method] --> U[Reset All Variables to Defaults<br/>collective_pitch=8.0, etc.]
    U --> V[Clear Simulation Data<br/>simulation.reset_data()]
    
    W[main Function] --> X[Print Startup Messages]
    X --> Y[Create Tkinter Root]
    Y --> Z[Create HelicopterSimulatorGUI Instance]
    Z --> AA[Print Success Messages]
    AA --> BB[Start Tkinter Main Loop<br/>root.mainloop()]
    
    Q --> CC[End]
    S --> CC
    V --> CC
    BB --> CC

    style A fill:#e1f5fe
    style CC fill:#e8f5e8
    style P fill:#ffeb3b
    style E fill:#e3f2fd
    style J fill:#fff3e0
    style R fill:#e3f2fd
    style T fill:#e3f2fd
    style W fill:#e3f2fd
    style C fill:#f3e5f5
    style L fill:#f3e5f5
    style M fill:#f3e5f5
    style N fill:#f3e5f5
```

## GUI Main Application
**Purpose**: Central coordinator for the helicopter simulator GUI application

### Initialization Process
1. **Window Setup**: Create main window with title and styling
2. **Simulation Engine**: Initialize physics and calculation engine
3. **Control Variables**: Set up Tkinter variables for all controls
4. **GUI Creation**: Build all interface panels and components
5. **Update Loop**: Start real-time update cycle

### Control Variables
- **Flight Controls**: Collective pitch, cyclic pitch, tail rotor pitch
- **Engine Control**: Throttle percentage
- **Flight Conditions**: Altitude, forward speed
- **All variables**: Tkinter DoubleVar for real-time binding

### Update Loop (5 Hz)
**Real-time Cycle**:
1. Get current control values from GUI
2. Update simulation engine with new inputs
3. Update display panel with forces/moments
4. Update plot panel with time history
5. Schedule next update in 200ms

### Key Features
- **Modular Design**: Separate panels for controls, display, plots
- **Real-time Updates**: 5 Hz refresh rate for smooth interaction
- **Error Handling**: Graceful failure with error messages
- **Reset Functionality**: Return to default control settings

### Integration Points
- **SimulationEngine**: Physics calculations and data management
- **ControlPanel**: User input controls and sliders
- **DisplayPanel**: Real-time force/moment display
- **PlotPanel**: Time history visualization