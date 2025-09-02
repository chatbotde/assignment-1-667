# Performance Analyzer Flow Diagram

```mermaid
flowchart TD
    A[Start: PerformanceAnalyzer] --> B[Performance Analysis Methods]
    
    B --> C[analyze_main_rotor_performance Method]
    B --> D[analyze_hover_mission Method]
    B --> E[calculate_rotor_performance Method]
    
    C --> F[Create Flight Sim Rotor Model]
    F --> G[Create Airfoil<br/>a0=5.7, Cd0=0.008, e=1.2]
    G --> H[Create Blade<br/>R_root=1.0m, R_tip=8.5m<br/>c_root=0.45m, c_tip=0.25m<br/>θ_root=12°, θ_tip=4° (8° twist)]
    H --> I[Create Rotor<br/>4 blades, blade object]
    
    I --> J[Calculate Performance at Multiple Conditions]
    J --> K[Hover at Sea Level<br/>ρ=1.225, V=0, ω=320 RPM]
    J --> L[Hover at 3500m<br/>ρ=isa_properties(3500), V=0]
    J --> M[Forward Flight<br/>V=50 m/s (180 km/h), ρ=1.225]
    
    K --> N[Call cycle_integrator<br/>T_hover, Q_hover, P_hover]
    L --> O[Call cycle_integrator<br/>T_alt, Q_alt, P_alt]
    M --> P[Call cycle_integrator<br/>T_forward, Q_forward, P_forward]
    
    N --> Q[Calculate Additional Parameters]
    O --> Q
    P --> Q
    Q --> R[Disk Loading = T_hover / (π × R²)]
    Q --> S[Tip Speed = ω × R_tip]
    
    R --> T[Return Performance Dictionary<br/>hover_sl, hover_3500m, forward_180kmh<br/>disk_loading, tip_speed]
    S --> T
    
    D --> U[Hover Mission Analysis at Altitude]
    U --> V[Get Atmospheric Properties<br/>ρ, a = isa_properties(altitude)]
    V --> W[Create Rotor Model<br/>Similar to main rotor analysis]
    W --> X[Calculate Available Performance<br/>T_available, Q, P_main = cycle_integrator()]
    
    X --> Y[Calculate Total Power Requirements]
    Y --> Z[P_tail = P_main × 0.12 (12% for tail rotor)]
    Z --> AA[P_total = (P_main + P_tail) × 1.1 (10% losses)]
    
    AA --> BB[Calculate Maximum Weights]
    BB --> CC[Max Weight (Thrust) = T_available / 9.81]
    BB --> DD[Max Weight (Power) = P_engine_available / (P_total/T_available) / 9.81]
    
    CC --> EE[Hover Endurance Analysis]
    DD --> EE
    EE --> FF[Weight Range: 2000-5000kg in 20 steps]
    FF --> GG[For Each Weight]
    GG --> HH[Scale Power: P_required = P_total × (weight×9.81/T_available)]
    HH --> II[Calculate Fuel Rate<br/>fuel_rate = (P_required/1000) × SFC / 60<br/>where SFC = 0.25 kg/kW/hr]
    II --> JJ[Calculate Endurance<br/>endurance = 800kg_fuel / fuel_rate]
    
    JJ --> KK{More Weights?}
    KK -->|Yes| GG
    KK -->|No| LL[Return Hover Analysis Dictionary<br/>altitude, max_weights, thrust_available<br/>power_required, weights, fuel_rates, endurances]
    
    E --> MM[Rotor Performance Calculation]
    MM --> NN{rotor_utils Available?}
    NN -->|Yes| OO[Import rotor_calc<br/>Call calculate_rotor_performance()]
    NN -->|No| PP[Use Simplified Calculation<br/>_simplified_rotor_performance()]
    
    OO --> QQ[Extract Results<br/>thrust_values, power_values]
    PP --> RR[Simplified Momentum Theory<br/>T = ρ × A × (θ × 0.1)² × 1000<br/>P = T × √(T/(2×ρ×A)) / 1000]
    
    QQ --> SS[Return thrust_values, power_values]
    RR --> SS
    
    T --> TT[End]
    LL --> TT
    SS --> TT

    style A fill:#e1f5fe
    style TT fill:#e8f5e8
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style NN fill:#ffeb3b
    style KK fill:#ffeb3b
    style F fill:#fff3e0
    style J fill:#fff3e0
    style U fill:#fff3e0
    style Y fill:#fff3e0
    style BB fill:#fff3e0
    style EE fill:#fff3e0
    style MM fill:#fff3e0
    style N fill:#f3e5f5
    style O fill:#f3e5f5
    style P fill:#f3e5f5
    style X fill:#f3e5f5
    style OO fill:#e8f5e8
    style PP fill:#ffcdd2
```

## Performance Analyzer Component
**Purpose**: Analyze helicopter rotor performance and mission capabilities

### Main Rotor Performance Analysis
**analyze_main_rotor_performance Method**:

#### Flight Simulation Integration
1. **Airfoil Model**: Advanced airfoil (a0=5.7, Cd0=0.008, e=1.2)
2. **Blade Geometry**: Realistic taper and twist distribution
3. **Rotor Model**: 4-blade configuration matching design

#### Multi-Condition Analysis
**Performance Points**:
- **Hover at Sea Level**: Baseline performance capability
- **Hover at 3500m**: High altitude performance degradation
- **Forward Flight**: 180 km/h cruise performance

#### Key Metrics Calculated
- **Thrust and Power**: At each flight condition
- **Disk Loading**: T_hover / (π × R²) - rotor loading metric
- **Tip Speed**: ω × R_tip - compressibility consideration

### Hover Mission Analysis
**analyze_hover_mission Method**:

#### Mission Scenario
- **Altitude**: Specified altitude (default 2000m)
- **Flight Condition**: Stationary hover
- **Analysis**: Weight limits and endurance

#### Performance Calculations
1. **Available Thrust**: From flight simulation cycle integrator
2. **Power Requirements**: Main rotor + 12% tail rotor + 10% losses
3. **Engine Limitations**: 2000kW available, 85% at altitude

#### Weight Limitations
**Two Limiting Factors**:
- **Thrust Limit**: Maximum weight rotor can lift
- **Power Limit**: Maximum weight engine can support

#### Endurance Analysis
**Process**:
1. **Weight Range**: 2000-5000kg in 20 steps
2. **Power Scaling**: Linear with weight ratio
3. **Fuel Consumption**: 0.25 kg/kW/hr specific fuel consumption
4. **Endurance**: 800kg fuel capacity / fuel burn rate

### Rotor Performance Calculation
**calculate_rotor_performance Method**:

#### Primary Method (rotor_utils)
**Integration Attempt**:
- Import shared rotor calculation utilities
- Use high-fidelity rotor performance models
- Extract thrust and power over pitch range

#### Fallback Method (Simplified)
**Momentum Theory Approximation**:
- **Thrust**: T = ρ × A × (θ × 0.1)² × 1000
- **Power**: P = T × √(T/(2×ρ×A)) / 1000
- Simplified but provides reasonable trends

### Key Features

#### High-Fidelity Analysis
- **Flight Simulation Integration**: Uses flight_sim_part1 components
- **Realistic Models**: Proper airfoil and blade geometry
- **Multiple Conditions**: Sea level, altitude, forward flight

#### Mission-Relevant Metrics
- **Weight Limits**: Critical for helicopter operations
- **Endurance**: Important for mission planning
- **Performance Envelope**: Operating boundaries

#### Robust Implementation
- **Error Handling**: Graceful fallback to simplified methods
- **Flexible Input**: Configurable altitude and conditions
- **Comprehensive Output**: All relevant performance parameters

### Integration Points
- **Flight Simulation**: cycle_integrator for accurate performance
- **Atmospheric Model**: ISA properties for altitude effects
- **Design Data**: Uses rotor geometry from RotorDesigner
- **Mission Analysis**: Supports hover mission requirements

### Output Products
- **Performance Dictionary**: Multi-condition performance data
- **Hover Analysis**: Weight limits and endurance curves
- **Thrust/Power Arrays**: Performance over operating range
- **Design Validation**: Performance against requirements