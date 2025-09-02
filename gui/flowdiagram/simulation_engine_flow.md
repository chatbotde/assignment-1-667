# Simulation Engine Flow Diagram

```mermaid
flowchart TD
    A[Start: SimulationEngine] --> B[Initialize Simulator<br/>self.initialize_simulator()]
    B --> C[Initialize State Variables<br/>forces_moments, performance<br/>time_data, force_history]
    
    C --> D[initialize_simulator Method]
    D --> E[Print Initialization Message]
    E --> F[Load Flight Sim Configuration<br/>fs_inputs = get_user_inputs()]
    F --> G[Build Main Rotor Model<br/>main_rotor = build_rotor(fs_inputs["rotor"])]
    
    G --> H[Define Component Positions<br/>Aircraft Reference Frame]
    H --> I[Main Rotor Position<br/>x=0.0, y=0.0, z=2.5m]
    H --> J[Tail Rotor Position<br/>x=-4.0, y=0.0, z=2.0m]
    H --> K[Center of Gravity<br/>x=-1.0, y=0.0, z=1.5m]
    
    I --> L[Print Success Messages<br/>Rotor radius, component model]
    J --> L
    K --> L
    
    L --> M[calculate_forces_and_moments Method]
    M --> N[Input: controls dictionary]
    N --> O[Try Import Shared Utilities<br/>from rotor_utils import rotor_calc]
    O --> P{Import Success?}
    P -->|Yes| Q[Call rotor_calc.calculate_forces_moments<br/>collective_pitch, cyclic_pitch, 0<br/>tail_rotor_pitch, throttle, altitude]
    P -->|No| R[Exception Handling<br/>Print calculation error]
    
    Q --> S[Extract Results<br/>Fx, Fy, Fz, Mx, My, Mz<br/>thrust, power]
    S --> T[Update forces_moments Dictionary<br/>Store all 6 components]
    T --> U[Update performance Dictionary<br/>Store thrust and power]
    
    R --> V[Set Safe Default Values<br/>All forces/moments = 0.0<br/>thrust = 0, power = 0]
    
    U --> W[update Method]
    V --> W
    W --> X[Input: controls dictionary]
    X --> Y[Call calculate_forces_and_moments<br/>Update current state]
    
    Y --> Z[Log Data for Plotting<br/>current_time = time.time() - start_time]
    Z --> AA[Append Time Data<br/>time_data.append(current_time)]
    AA --> BB[Append Force History<br/>For each key in forces_moments<br/>force_history[key].append(value)]
    
    BB --> CC[Buffer Management<br/>Keep only last 20 points]
    CC --> DD{len(time_data) > 20?}
    DD -->|Yes| EE[Trim Data Arrays<br/>time_data = time_data[-20:]<br/>force_history[key] = force_history[key][-20:]]
    DD -->|No| FF[Continue]
    
    EE --> GG[Getter Methods]
    FF --> GG
    GG --> HH[get_forces_moments<br/>Return current forces_moments]
    GG --> II[get_performance<br/>Return current performance]
    GG --> JJ[get_time_data<br/>Return time_data array]
    GG --> KK[get_force_history<br/>Return force_history dictionary]
    
    GG --> LL[reset_data Method]
    LL --> MM[Clear All Data Arrays<br/>time_data = []<br/>force_history[key] = []]
    MM --> NN[Reset Start Time<br/>start_time = time.time()]
    
    HH --> OO[End]
    II --> OO
    JJ --> OO
    KK --> OO
    NN --> OO

    style A fill:#e1f5fe
    style OO fill:#e8f5e8
    style P fill:#ffeb3b
    style DD fill:#ffeb3b
    style D fill:#e3f2fd
    style M fill:#e3f2fd
    style W fill:#e3f2fd
    style GG fill:#e3f2fd
    style LL fill:#e3f2fd
    style Q fill:#f3e5f5
    style R fill:#ffcdd2
    style V fill:#ffcdd2
    style H fill:#fff3e0
    style Z fill:#fff3e0
    style CC fill:#fff3e0
```

## Simulation Engine Component
**Purpose**: Physics calculation engine and data management for helicopter simulation

### Initialization Process
1. **Flight Sim Integration**: Load configuration from flight_sim_part1
2. **Rotor Model**: Build main rotor using shared utilities
3. **Component Layout**: Define aircraft reference frame positions
4. **State Variables**: Initialize forces, moments, and performance tracking

### Component Positions (Aircraft Reference Frame)
**Coordinate System**: X-forward, Y-right, Z-down
- **Main Rotor**: (0.0, 0.0, 2.5m) - Above fuselage centerline
- **Tail Rotor**: (-4.0, 0.0, 2.0m) - Aft and slightly lower
- **Center of Gravity**: (-1.0, 0.0, 1.5m) - Slightly aft of main rotor

### Force and Moment Calculation
**Primary Method**: calculate_forces_and_moments(controls)

**Process**:
1. **Import Utilities**: Attempt to load shared rotor calculation utilities
2. **Calculate Results**: Call rotor_calc with control inputs
3. **Extract Data**: Get forces (Fx, Fy, Fz) and moments (Mx, My, Mz)
4. **Update State**: Store results in internal dictionaries
5. **Error Handling**: Set safe defaults if calculations fail

**Control Inputs**:
- **collective_pitch**: Main rotor collective angle
- **cyclic_pitch**: Longitudinal cyclic (pitch control)
- **roll_cyclic**: 0 (simplified model)
- **tail_rotor_pitch**: Anti-torque control
- **throttle**: Engine power setting
- **altitude**: Flight altitude for atmospheric effects

### Data Management
**Real-time Data Logging**:
- **Time Tracking**: Relative time from simulation start
- **Force History**: Rolling buffer for each force/moment component
- **Buffer Size**: 20 data points (4 seconds at 5 Hz update rate)
- **Memory Management**: Automatic trimming of old data

### State Variables
**forces_moments Dictionary**:
- **Fx, Fy, Fz**: Forces in aircraft reference frame [N]
- **Mx, My, Mz**: Moments about aircraft axes [N⋅m]

**performance Dictionary**:
- **thrust**: Total rotor thrust [N]
- **power**: Total power consumption [kW]

### Update Cycle
**Main Update Method**:
1. Calculate current forces and moments
2. Log time stamp and data values
3. Append to history buffers
4. Trim buffers to maintain fixed size
5. Provide data to GUI components

### Error Handling
**Robust Operation**:
- **Import Failures**: Graceful fallback to default values
- **Calculation Errors**: Safe default state with error logging
- **Data Validation**: Ensure consistent data structures

### Integration Points
- **Flight Simulation**: Uses flight_sim_part1 rotor models
- **GUI Components**: Provides data to display and plot panels
- **Control System**: Receives inputs from control panel
- **Real-time Loop**: Updated every 200ms by main GUI loop

### Key Features
- **Real-time Calculation**: 5 Hz update rate for smooth operation
- **Memory Efficient**: Fixed-size rolling buffers
- **Error Resilient**: Continues operation despite calculation failures
- **Modular Design**: Clean separation of physics and GUI concerns