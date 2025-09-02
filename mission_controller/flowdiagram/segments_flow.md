# Mission Segments Flow Diagram

```mermaid
flowchart TD
    A[Start: Segment Execution] --> B[Segment Types]
    
    B --> C[run_hover]
    B --> D[run_vertical_climb]
    B --> E[run_forward_climb]
    B --> F[run_cruise]
    B --> G[run_loiter]
    B --> H[run_payload_op]
    
    C --> I[Hover Execution Loop<br/>t = 0 to duration_s]
    I --> J[Get ISA Properties<br/>ρ, a = isa_properties(alt_m)]
    J --> K[Calculate Weight<br/>W = heli.weight_N()]
    K --> L[Solve RPM for Thrust<br/>solve_rpm_for_thrust(rotor, ρ, a, V=0, W)]
    L --> M{RPM Solution Valid?}
    M -->|No| N[Return Failure<br/>"Hover infeasible"]
    M -->|Yes| O[Calculate Power Components<br/>P_main, P_tail, P_par=0]
    O --> P[Total Power<br/>P_req_kW = (P_main + P_tail + P_par)/1000]
    P --> Q[Check Power Available<br/>P_avail_kW = engine.power_available(ρ)]
    Q --> R{P_req ≤ P_avail?}
    R -->|No| S[Return Failure<br/>"Power shortfall"]
    R -->|Yes| T[Calculate Fuel Burn<br/>fuel_used = engine.fuel_burn(P_req_kW, dt_s)]
    T --> U{Sufficient Fuel?}
    U -->|No| V[Return Failure<br/>"Fuel exhausted"]
    U -->|Yes| W[Update Fuel<br/>heli.fuel_kg -= fuel_used]
    W --> X[Log Segment Data<br/>time, altitude, rpm, powers, fuel]
    X --> Y[Increment Time<br/>t += dt_s]
    Y --> Z{t < duration_s?}
    Z -->|Yes| J
    Z -->|No| AA[Return Success]
    
    D --> BB[Vertical Climb Loop<br/>Similar to hover with climb power]
    BB --> CC[Add Climb Power<br/>P_climb = W × climb_rate_mps]
    CC --> DD[Update Altitude<br/>alt += climb_rate × dt_s]
    
    E --> EE[Forward Climb Loop<br/>Similar to vclimb with forward velocity]
    EE --> FF[Add Parasite Power<br/>P_par = parasite_power(ρ, V, S_ref, CD0)]
    
    F --> GG[Cruise Loop<br/>Level flight at constant altitude/velocity]
    GG --> HH[No Climb Power<br/>P_climb = 0]
    
    G --> II[Loiter Loop<br/>Identical to cruise with different velocity parameter]
    
    H --> JJ[Payload Operation]
    JJ --> KK{duration_hover_s > 0?}
    KK -->|Yes| LL[Run Hover Phase<br/>run_hover(heli, engine, rotor, duration, alt)]
    KK -->|No| MM[Skip Hover]
    LL --> NN{Hover Success?}
    NN -->|No| OO[Return Failure<br/>Hover phase failed]
    NN -->|Yes| PP[Execute Payload Change]
    MM --> PP
    PP --> QQ{Payload Kind?}
    QQ -->|pickup| RR[heli.payload_kg += abs(delta_mass_kg)]
    QQ -->|drop| SS[heli.payload_kg -= abs(delta_mass_kg)]
    QQ -->|unknown| TT[Return Failure<br/>"Unknown payload op"]
    RR --> UU[Log Payload Change]
    SS --> UU
    UU --> VV[Return Success]
    
    N --> WW[End]
    S --> WW
    V --> WW
    AA --> WW
    OO --> WW
    TT --> WW
    VV --> WW

    style A fill:#e1f5fe
    style WW fill:#e8f5e8
    style M fill:#ffeb3b
    style R fill:#ffeb3b
    style U fill:#ffeb3b
    style Z fill:#ffeb3b
    style KK fill:#ffeb3b
    style NN fill:#ffeb3b
    style QQ fill:#ffeb3b
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style F fill:#e3f2fd
    style G fill:#e3f2fd
    style H fill:#e3f2fd
    style L fill:#f3e5f5
    style N fill:#ffcdd2
    style S fill:#ffcdd2
    style V fill:#ffcdd2
    style OO fill:#ffcdd2
    style TT fill:#ffcdd2
```

## Mission Segment Execution Functions
**Purpose**: Execute individual mission segments with power and fuel calculations

### Common Execution Pattern
1. **Time Loop**: Execute segment in time steps (default 1.0s)
2. **Atmospheric Conditions**: Get density and speed of sound
3. **Weight Calculation**: Current helicopter weight including fuel/payload
4. **RPM Solution**: Solve for RPM to achieve required thrust
5. **Power Calculation**: Main rotor, tail rotor, parasite, climb power
6. **Feasibility Check**: Verify power available vs required
7. **Fuel Consumption**: Calculate and update fuel burn
8. **Data Logging**: Record segment performance data

### Segment-Specific Features

#### Hover
- Zero forward velocity
- No parasite or climb power
- Pure vertical thrust requirement

#### Vertical Climb
- Adds climb power: P_climb = Weight × climb_rate
- Updates altitude continuously
- Higher power requirement than hover

#### Forward Climb
- Combines forward flight and climb
- Includes parasite power from forward velocity
- Most power-intensive segment type

#### Cruise/Loiter
- Level flight at constant altitude
- Optimized for forward flight efficiency
- Loiter uses lower velocity than cruise

#### Payload Operations
- Optional hover phase before mass change
- Pickup increases helicopter mass
- Drop decreases helicopter mass
- Immediate effect on subsequent power requirements