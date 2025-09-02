# Power Calculation Flow Diagram

```mermaid
flowchart TD
    A[Start: Power Calculation] --> B[Input Parameters<br/>ρ, V_forward, altitude, climb_rate<br/>heli, engine, rotor]
    
    B --> C[Main Rotor Power Calculation]
    C --> D[Get Required Thrust<br/>T_req = heli.weight_N()]
    D --> E[Solve RPM for Thrust<br/>solve_rpm_for_thrust(rotor, ρ, a, V_forward, T_req)]
    E --> F[Extract Main Rotor Power<br/>P_main from cycle_integrator]
    
    F --> G[Tail Rotor Power Calculation]
    G --> H[Calculate Velocity-Dependent Fraction<br/>f_tail = tail_power_fraction(V_forward)]
    H --> I[Hover Fraction: f_hover = 0.07<br/>Minimum Fraction: f_min = 0.015<br/>Transition Speed: V0 = 30 m/s]
    I --> J[Exponential Decay Model<br/>f_tail = f_min + (f_hover - f_min) × exp(-(V/V0)²)]
    J --> K[Calculate Tail Power<br/>P_tail = P_main × f_tail]
    
    K --> L[Parasite Power Calculation]
    L --> M{V_forward > 0?}
    M -->|No| N[P_parasite = 0<br/>(No forward flight)]
    M -->|Yes| O[Calculate Dynamic Pressure<br/>q = 0.5 × ρ × V_forward²]
    O --> P[Calculate Drag Force<br/>D = q × S_ref_m2 × CD0_body]
    P --> Q[Calculate Parasite Power<br/>P_parasite = D × V_forward]
    
    N --> R[Climb Power Calculation]
    Q --> R
    R --> S{climb_rate ≠ 0?}
    S -->|No| T[P_climb = 0<br/>(Level flight)]
    S -->|Yes| U[Calculate Climb Power<br/>P_climb = heli.weight_N() × max(0, climb_rate)]
    
    T --> V[Sum Total Power Required]
    U --> V
    V --> W[P_total = P_main + P_tail + P_parasite + P_climb]
    W --> X[Convert to kW<br/>P_req_kW = P_total / 1000]
    
    X --> Y[Power Availability Check]
    Y --> Z[Get Engine Power Available<br/>P_avail_kW = engine.power_available(ρ)]
    Z --> AA[Engine Power Model<br/>σ = ρ/ρ₀, P_avail = P_sl × σ^α<br/>where α = derate_alpha = 0.7]
    
    AA --> BB[Power Margin Check]
    BB --> CC{P_req_kW ≤ P_avail_kW?}
    CC -->|No| DD[Power Shortfall<br/>Return Failure]
    CC -->|Yes| EE[Calculate Power Margin<br/>margin = P_avail_kW - P_req_kW]
    
    EE --> FF[Fuel Consumption Calculation]
    FF --> GG[Calculate Fuel Burn Rate<br/>fuel_rate = P_req_kW × SFC<br/>where SFC = 0.32 kg/kWh]
    GG --> HH[Calculate Time Step Fuel<br/>fuel_used = fuel_rate × (dt_s/3600)]
    HH --> II[Check Fuel Availability<br/>fuel_used ≤ heli.fuel_kg?]
    II -->|No| JJ[Fuel Exhausted<br/>Return Failure]
    II -->|Yes| KK[Return Power Summary<br/>P_main, P_tail, P_parasite, P_climb<br/>P_req_kW, P_avail_kW, fuel_used]
    
    DD --> LL[End]
    JJ --> LL
    KK --> LL

    style A fill:#e1f5fe
    style LL fill:#e8f5e8
    style M fill:#ffeb3b
    style S fill:#ffeb3b
    style CC fill:#ffeb3b
    style II fill:#ffeb3b
    style DD fill:#ffcdd2
    style JJ fill:#ffcdd2
    style C fill:#e3f2fd
    style G fill:#e3f2fd
    style L fill:#e3f2fd
    style R fill:#e3f2fd
    style Y fill:#e3f2fd
    style FF fill:#e3f2fd
    style E fill:#f3e5f5
    style J fill:#fff3e0
    style O fill:#fff3e0
    style P fill:#fff3e0
    style U fill:#fff3e0
    style AA fill:#fff3e0
    style GG fill:#fff3e0
```

## Power Calculation System
**Purpose**: Comprehensive power requirement calculation for helicopter mission segments

### Power Components

#### 1. Main Rotor Power (P_main)
**Source**: Flight simulation cycle integrator
- **Process**: Solve RPM to achieve required thrust
- **Integration**: Uses detailed rotor aerodynamics from flight_sim_part1
- **Constraints**: Limited by tip Mach number (typically 0.85-0.90)

#### 2. Tail Rotor Power (P_tail)
**Model**: Velocity-dependent anti-torque requirement
- **Hover**: 7% of main rotor power (maximum anti-torque)
- **Forward Flight**: Reduces to 1.5% minimum (aerodynamic unloading)
- **Transition**: Exponential decay with 30 m/s characteristic velocity
- **Formula**: f_tail = f_min + (f_hover - f_min) × exp(-(V/V0)²)

#### 3. Parasite Power (P_parasite)
**Model**: Fuselage drag power in forward flight
- **Formula**: P = D × V = (0.5 × ρ × V² × S_ref × CD0) × V
- **Parameters**: S_ref = 6.0 m², CD0 = 0.045
- **Significance**: Becomes dominant at high forward speeds

#### 4. Climb Power (P_climb)
**Model**: Gravitational potential energy rate
- **Formula**: P = Weight × climb_rate
- **Application**: Added for vertical climb and forward climb segments
- **Sign Convention**: Positive for climb, zero for descent (conservative)

### Engine Power Model
**Altitude Derate**: P_available = P_sea_level × (ρ/ρ₀)^α
- **Sea Level Power**: 1500 kW
- **Derate Factor**: α = 0.7 (typical turboshaft)
- **Density Ratio**: σ = ρ/ρ₀ where ρ₀ = 1.225 kg/m³

### Fuel Consumption Model
**Specific Fuel Consumption**: 0.32 kg/kWh (typical turboshaft)
- **Fuel Rate**: fuel_rate = P_required × SFC
- **Time Step**: fuel_used = fuel_rate × (dt_s/3600)
- **Tracking**: Continuous fuel depletion throughout mission

### Feasibility Checks
1. **RPM Solvability**: Can required thrust be achieved?
2. **Power Availability**: P_required ≤ P_available?
3. **Fuel Sufficiency**: fuel_required ≤ fuel_remaining?

### Integration Points
- **Flight Simulation**: Main rotor performance via cycle_integrator
- **Atmospheric Model**: Air density for power and performance
- **Vehicle Model**: Weight, reference area, drag coefficient
- **Engine Model**: Power availability and fuel consumption

### Key Features
- **High Fidelity**: Detailed physics-based power modeling
- **Real-time Feasibility**: Continuous power and fuel checking
- **Component Breakdown**: Individual power contributions tracked
- **Altitude Effects**: Realistic engine power degradation
- **Mission Optimization**: Power margins available for analysis