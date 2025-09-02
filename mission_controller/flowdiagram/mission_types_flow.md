# Mission Types Flow Diagram

```mermaid
flowchart TD
    A[Start: MissionTypes] --> B[Static Methods]
    
    B --> C[get_predefined_missions]
    B --> D[validate_mission_segments]
    B --> E[list_available_missions]
    
    C --> F[Return Mission Dictionary<br/>test, patrol, search_rescue, cargo]
    F --> G[Test Mission<br/>hover → cruise → hover]
    F --> H[Patrol Mission<br/>vclimb → cruise → loiter → cruise → hover]
    F --> I[Search & Rescue<br/>vclimb → cruise → loiter → hover → payload → cruise → hover]
    F --> J[Cargo Mission<br/>payload → vclimb → cruise → hover → payload → cruise → hover]
    
    D --> K[Input: segments list]
    K --> L[Define Valid Types<br/>hover, vclimb, fclimb, cruise, loiter, payload]
    L --> M[Segment Validation Loop]
    M --> N{Has 'type' field?}
    N -->|No| O[Raise ValueError<br/>Missing type field]
    N -->|Yes| P{Type in valid_types?}
    P -->|No| Q[Raise ValueError<br/>Invalid segment type]
    P -->|Yes| R[Type-Specific Validation]
    
    R --> S{Segment Type?}
    S -->|hover| T[Required: duration_s, altitude_m]
    S -->|vclimb| U[Required: duration_s, start_alt_m, climb_rate_mps]
    S -->|fclimb| V[Required: duration_s, start_alt_m, climb_rate_mps, V_forward_mps]
    S -->|cruise| W[Required: duration_s, altitude_m, V_forward_mps]
    S -->|loiter| X[Required: duration_s, altitude_m, V_loiter_mps]
    S -->|payload| Y[Required: kind, delta_mass_kg]
    
    T --> Z[Check Required Fields]
    U --> Z
    V --> Z
    W --> Z
    X --> Z
    Y --> Z
    
    Z --> AA{All Fields Present?}
    AA -->|No| BB[Raise ValueError<br/>Missing required field]
    AA -->|Yes| CC{More Segments?}
    CC -->|Yes| M
    CC -->|No| DD[Print Validation Success]
    
    E --> EE[Return List of Mission Keys<br/>from get_predefined_missions]
    
    G --> FF[End]
    H --> FF
    I --> FF
    J --> FF
    O --> FF
    Q --> FF
    BB --> FF
    DD --> FF
    EE --> FF

    style A fill:#e1f5fe
    style FF fill:#e8f5e8
    style N fill:#ffeb3b
    style P fill:#ffeb3b
    style S fill:#ffeb3b
    style AA fill:#ffeb3b
    style CC fill:#ffeb3b
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style O fill:#ffcdd2
    style Q fill:#ffcdd2
    style BB fill:#ffcdd2
    style T fill:#fff3e0
    style U fill:#fff3e0
    style V fill:#fff3e0
    style W fill:#fff3e0
    style X fill:#fff3e0
    style Y fill:#fff3e0
```

## Class: MissionTypes
**Purpose**: Define and validate predefined mission configurations

### Predefined Missions
1. **Test Mission**: Simple validation mission
   - hover → cruise → hover
   
2. **Patrol Mission**: Standard patrol pattern
   - vclimb → cruise → loiter → cruise → hover
   
3. **Search & Rescue**: SAR mission with payload
   - vclimb → cruise → loiter → hover → payload pickup → cruise → hover
   
4. **Cargo Mission**: Heavy lift transport
   - payload pickup → vclimb → cruise → hover → payload drop → cruise → hover

### Segment Validation
**Valid Segment Types**:
- **hover**: Stationary flight at altitude
- **vclimb**: Vertical climb/descent
- **fclimb**: Forward climbing flight
- **cruise**: Level forward flight
- **loiter**: Slow forward flight pattern
- **payload**: Pickup/drop operations

### Field Requirements
Each segment type has specific required fields that are validated:
- Duration, altitude, velocities as appropriate
- Payload operations require kind and mass change
- Climb segments require rates and starting altitudes