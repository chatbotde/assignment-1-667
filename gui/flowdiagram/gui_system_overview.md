# GUI System Overview

```mermaid
flowchart TB
    subgraph "Entry Point"
        A[helicopter_simulator_gui_new.py<br/>Main Entry Point] --> B[gui.helicopter_gui_main.main()]
    end
    
    subgraph "Main Application Layer"
        C[HelicopterSimulatorGUI<br/>Main Application Class] --> D[Window Management<br/>1200x800, Dark Theme]
        C --> E[Control Variables<br/>Tkinter DoubleVar Bindings]
        C --> F[Update Loop<br/>5 Hz Real-time Cycle]
    end
    
    subgraph "GUI Component Layer"
        G[ControlPanel<br/>Pilot Controls] --> H[Flight Control Sliders<br/>Collective, Cyclic, Tail Rotor, Throttle]
        G --> I[Flight Condition Sliders<br/>Altitude, Forward Speed]
        
        J[DisplayPanel<br/>Real-time Display] --> K[Forces Display<br/>Fx, Fy, Fz with Color Coding]
        J --> L[Moments Display<br/>Mx, My, Mz with Color Coding]
        J --> M[Performance Display<br/>Thrust, Power]
        
        N[PlotPanel<br/>Time History Visualization] --> O[Matplotlib Integration<br/>Embedded Canvas]
        N --> P[Force Plot<br/>Real-time Fx, Fy, Fz]
        N --> Q[Moment Plot<br/>Real-time Mx, My, Mz]
    end
    
    subgraph "Simulation Engine Layer"
        R[SimulationEngine<br/>Physics Calculator] --> S[Flight Sim Integration<br/>flight_sim_part1 Components]
        R --> T[Component Positioning<br/>Aircraft Reference Frame]
        R --> U[Force/Moment Calculation<br/>rotor_calc Utilities]
        R --> V[Data Management<br/>Rolling Buffer System]
    end
    
    subgraph "Data Flow"
        W[Control Inputs<br/>Slider Values] --> X[Simulation Update<br/>Physics Calculation]
        X --> Y[State Update<br/>Forces, Moments, Performance]
        Y --> Z[GUI Update<br/>Display + Plot Refresh]
        Z --> AA[User Feedback<br/>Visual Response]
    end
    
    subgraph "Integration Points"
        BB[Flight Simulation<br/>flight_sim_part1] --> CC[Rotor Models<br/>user_inputs, build_rotor]
        DD[Shared Utilities<br/>rotor_utils] --> EE[Force Calculations<br/>rotor_calc.calculate_forces_moments]
        FF[Tkinter Framework<br/>GUI Toolkit] --> GG[Widget System<br/>Frames, Labels, Scales, Canvas]
        HH[Matplotlib<br/>Plotting Library] --> II[Real-time Plots<br/>FigureCanvasTkAgg]
    end
    
    %% Connections between layers
    B --> C
    C --> G
    C --> J
    C --> N
    C --> R
    
    G --> W
    R --> X
    X --> Y
    Y --> J
    Y --> N
    
    R --> BB
    R --> DD
    N --> HH
    C --> FF
    
    %% Styling
    style A fill:#e3f2fd
    style C fill:#e1f5fe
    style R fill:#f3e5f5
    style G fill:#fff3e0
    style J fill:#fff3e0
    style N fill:#fff3e0
    style BB fill:#ffeb3b
    style DD fill:#ffeb3b
    style FF fill:#e8f5e8
    style HH fill:#e8f5e8
```

## GUI System Architecture

### System Layers

#### 1. Entry Point Layer
**Purpose**: Application startup and initialization
- **helicopter_simulator_gui_new.py**: Main entry script
- **Path Management**: Adds GUI directory to Python path
- **Main Function Call**: Delegates to gui.helicopter_gui_main.main()

#### 2. Main Application Layer
**Purpose**: Central coordination and window management
- **HelicopterSimulatorGUI**: Main application class
- **Window Setup**: 1200x800 resolution with dark theme (#34495e)
- **Control Variables**: Tkinter DoubleVar for real-time data binding
- **Update Loop**: 5 Hz refresh cycle (200ms intervals)

#### 3. GUI Component Layer
**Purpose**: User interface panels and controls

##### ControlPanel
- **Flight Controls**: Collective, cyclic, tail rotor pitch, throttle
- **Flight Conditions**: Altitude and forward speed
- **Interactive Sliders**: Real-time value updates with visual feedback
- **Reset Functionality**: Return to default control settings

##### DisplayPanel
- **Forces Display**: Fx, Fy, Fz with color-coded labels
- **Moments Display**: Mx, My, Mz with color-coded labels
- **Performance Metrics**: Thrust and power indicators
- **Aircraft Reference Frame**: Standard aerospace coordinate system

##### PlotPanel
- **Matplotlib Integration**: Embedded canvas in Tkinter
- **Dual Plots**: Separate force and moment time histories
- **Real-time Updates**: Rolling 20-point data buffer
- **Color Consistency**: Matches display panel color scheme

#### 4. Simulation Engine Layer
**Purpose**: Physics calculations and data management
- **Flight Sim Integration**: Uses flight_sim_part1 components
- **Component Positioning**: Aircraft reference frame layout
- **Force Calculations**: Integration with rotor_calc utilities
- **Data Management**: Rolling buffer system for time history

### Data Flow Architecture

#### Real-time Update Cycle
1. **Control Inputs**: User adjusts sliders in ControlPanel
2. **Simulation Update**: SimulationEngine calculates new physics state
3. **State Update**: Forces, moments, and performance updated
4. **GUI Update**: DisplayPanel and PlotPanel refresh with new data
5. **User Feedback**: Visual response completes interaction loop

#### Data Structures
- **Control Dictionary**: All pilot input values
- **Forces/Moments Dictionary**: 6-DOF aircraft state
- **Performance Dictionary**: Thrust and power metrics
- **Time History**: Rolling buffers for plotting

### Integration Points

#### External Dependencies
- **Flight Simulation**: flight_sim_part1 for rotor performance models
- **Shared Utilities**: rotor_utils for force/moment calculations
- **Tkinter Framework**: Native Python GUI toolkit
- **Matplotlib**: Scientific plotting and visualization

#### Internal Integration
- **Variable Binding**: Tkinter DoubleVar for automatic updates
- **Component Communication**: Direct method calls between panels
- **Data Synchronization**: Centralized state management
- **Error Handling**: Graceful degradation on calculation failures

### Key Features

#### Real-time Operation
- **5 Hz Update Rate**: Smooth user interaction
- **Non-blocking Updates**: Matplotlib draw_idle() for performance
- **Rolling Buffers**: Memory-efficient time history management
- **Responsive Controls**: Immediate visual feedback

#### Visual Design
- **Dark Theme**: Professional aerospace appearance
- **Color Coding**: Intuitive force/moment identification
- **Typography**: Bold fonts for critical data visibility
- **Layout**: Efficient use of screen real estate

#### Robustness
- **Error Handling**: Graceful failure with safe defaults
- **Data Validation**: Consistent data structure maintenance
- **Memory Management**: Fixed-size buffers prevent growth
- **Modular Design**: Clean separation of concerns

### System Benefits
- **Educational**: Clear visualization of helicopter physics
- **Interactive**: Real-time control response demonstration
- **Professional**: Aerospace-standard reference frames and units
- **Extensible**: Modular architecture for future enhancements