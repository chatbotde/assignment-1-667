# Detailed Segment Execution Flow Diagram

```mermaid
flowchart TD
    A[Start: Segment Execution] --> B[Initialize Segment<br/>t=0, log=[], dt_s=1.0]
    
    B --> C[Time Step Loop<br/>while t < duration_s]
    C --> D[Get Atmospheric Properties<br/>ρ, a = isa_properties(altitude)]
    D --> E[Calculate Current Weight<br/>W = heli.weight_N()]
    
    E --> F[Solve for Required RPM<br/>solve_rpm_for_thrust(rotor, ρ, a, V_forward, W)]
    F --> G{RPM Solution Valid?}
    G -->|No| H[Return SegmentResult<br/>success=False, reason="Infeasible"]
    G -->|Yes| I[Extract Results<br/>rpm, ω, T, Q, P_main]
    
    I --> J[Calculate Power Components]
    J --> K[Main Rotor Power<br/>P_main (from solver)]
    J --> L[Tail Rotor Power<br/>P_tail = P_main × tail_power_fraction(V)]
    J --> M[Parasite Power<br/>P_par = parasite_power(ρ, V, S_ref, CD0)]
    J --> N[Climb Power<br/>P_climb = W × climb_rate (if applicable)]
    
    K --> O[Sum Total Power Required<br/>P_req_kW = (P_main + P_tail + P_par + P_climb)/1000]
    L --> O
    M --> O
    N --> O
    
    O --> P[Check Power Available<br/>P_avail_kW = engine.power_available(ρ)]
    P --> Q{P_req ≤ P_avail?}
    Q -->|No| R[Return SegmentResult<br/>success=False, reason="Power shortfall"]
    Q -->|Yes| S[Calculate Fuel Consumption<br/>fuel_used = engine.fuel_burn(P_req_kW, dt_s)]
    
    S --> T{Sufficient Fuel?}
    T -->|No| U[Return SegmentResult<br/>success=False, reason="Fuel exhausted"]
    T -->|Yes| V[Update Helicopter State<br/>heli.fuel_kg -= fuel_used]
    
    V --> W[Update Position/Altitude<br/>(segment-specific)]
    W --> X[Log Time Step Data<br/>time, altitude, rpm, powers, fuel, mass]
    X --> Y[Increment Time<br/>t += dt_s]
    Y --> Z{t < duration_s?}
    Z -->|Yes| C
    Z -->|No| AA[Return SegmentResult<br/>success=True, reason="ok", log]
    
    subgraph "Segment-Specific Updates"
        BB[Hover<br/>altitude unchanged]
        CC[Vertical Climb<br/>alt += climb_rate × dt_s]
        DD[Forward Climb<br/>alt += climb_rate × dt_s]
        EE[Cruise<br/>altitude unchanged]
        FF[Loiter<br/>altitude unchanged]
        GG[Payload Op<br/>mass change + optional hover]
    end
    
    W --> BB
    W --> CC
    W --> DD
    W --> EE
    W --> FF
    W --> GG
    
    H --> HH[End]
    R --> HH
    U --> HH
    AA --> HH

    style A fill:#e1f5fe
    style HH fill:#e8f5e8
    style G fill:#ffeb3b
    style Q fill:#ffeb3b
    style T fill:#ffeb3b
    style Z fill:#ffeb3b
    style H fill:#ffcdd2
    style R fill:#ffcdd2
    style U fill:#ffcdd2
    style F fill:#f3e5f5
    style J fill:#fff3e0
    style O fill:#fff3e0
    style P fill:#fff3e0
    style S fill:#fff3e0
    style BB fill:#e8f5e8
    style CC fill:#e8f5e8
    style DD fill:#e8f5e8
    style EE fill:#e8f5e8
    style FF fill:#e8f5e8
    style GG fill:#e8f5e8
```

## Detailed Segment Execution Process
**Purpose**: Common execution pattern for all mission segments with comprehensive power and fuel modeling

### Time-Stepped Simulation
**Process**: 1-second time steps with continuous monitoring
- Allows for dynamic conditions and real-time feasibility checking
- Provides detailed mission logs for analysis
- Enables early termination on infeasible conditions

### Power Calculation Chain
1. **RPM Optimization**: Solve for RPM that produces required thrust
2. **Main Rotor Power**: From flight simulation cycle integrator
3. **Tail Rotor Power**: Anti-torque requirement (velocity-dependent)
4. **Parasite Power**: Fuselage drag in forward flight
5. **Climb Power**: Gravitational potential energy rate

### Feasibility Checks
**Three Critical Checks**:
1. **RPM Solvability**: Can required thrust be achieved within tip Mach limits?
2. **Power Availability**: Is engine power sufficient for total requirement?
3. **Fuel Sufficiency**: Is remaining fuel adequate for time step?

### State Updates
**Continuous Tracking**:
- **Fuel**: Decremented each time step based on power consumption
- **Altitude**: Updated based on segment type (climb/descent/level)
- **Mass**: Changes with fuel consumption and payload operations
- **Performance**: Logged for post-mission analysis

### Segment-Specific Variations

#### Hover
- **Velocity**: Zero forward speed
- **Power**: Main + tail rotor only
- **Altitude**: Constant

#### Vertical Climb
- **Velocity**: Zero forward speed
- **Power**: Main + tail + climb power
- **Altitude**: Increases at climb rate

#### Forward Climb
- **Velocity**: Forward speed component
- **Power**: Main + tail + parasite + climb power
- **Altitude**: Increases at climb rate

#### Cruise/Loiter
- **Velocity**: Constant forward speed
- **Power**: Main + tail + parasite power
- **Altitude**: Constant

#### Payload Operations
- **Special**: Mass change affects subsequent calculations
- **Optional Hover**: May include hover phase before/after mass change

### Error Handling
**Graceful Failure**: Each failure mode returns specific reason
- Enables mission analysis and optimization
- Preserves partial mission logs for debugging
- Allows for mission replanning based on failure points