# Mission Planner Main Flow Diagram

```mermaid
flowchart TD
    A[Start: run_mission] --> B[Get Helicopter & Engine<br/>heli, engine, rotor = get_helicopter_and_engine()]
    B --> C[Get Mission Definition<br/>mission = mission_definition()]
    C --> D[Initialize<br/>full_log = []<br/>current_alt = 0.0]
    
    D --> E[Mission Segment Loop]
    E --> F{Segment Type?}
    
    F -->|hover| G[Call run_hover<br/>heli, engine, rotor, duration_s, altitude_m]
    F -->|vclimb| H[Call run_vertical_climb<br/>heli, engine, rotor, duration_s, start_alt_m, climb_rate_mps]
    F -->|fclimb| I[Call run_forward_climb<br/>heli, engine, rotor, duration_s, start_alt_m, climb_rate_mps, V_forward_mps]
    F -->|cruise| J[Call run_cruise<br/>heli, engine, rotor, duration_s, altitude_m, V_forward_mps]
    F -->|loiter| K[Call run_loiter<br/>heli, engine, rotor, duration_s, altitude_m, V_loiter_mps]
    F -->|payload| L[Call run_payload_op<br/>heli, kind, delta_mass_kg, duration_hover_s, altitude_m]
    F -->|unknown| M[Return False<br/>"Unknown segment type"]
    
    G --> N[Update current_alt = altitude_m]
    H --> O[Update current_alt = start_alt + climb_rate × duration]
    I --> P[Update current_alt = start_alt + climb_rate × duration]
    J --> Q[Update current_alt = altitude_m]
    K --> R[Update current_alt = altitude_m]
    L --> S[current_alt unchanged]
    
    N --> T[Extend full_log with segment results]
    O --> T
    P --> T
    Q --> T
    R --> T
    S --> T
    
    T --> U{Segment Success?}
    U -->|No| V[Return False, reason, full_log]
    U -->|Yes| W{More Segments?}
    W -->|Yes| E
    W -->|No| X[Return True, "Mission completed", full_log]
    
    M --> Y[End]
    V --> Y
    X --> Y

    style A fill:#e1f5fe
    style Y fill:#e8f5e8
    style F fill:#ffeb3b
    style U fill:#ffeb3b
    style W fill:#ffeb3b
    style G fill:#e3f2fd
    style H fill:#e3f2fd
    style I fill:#e3f2fd
    style J fill:#e3f2fd
    style K fill:#e3f2fd
    style L fill:#e3f2fd
    style M fill:#ffcdd2
    style V fill:#ffcdd2
    style X fill:#e8f5e8
```

## Function: run_mission()
**Purpose**: Execute complete mission by running individual segments sequentially

### Mission Execution Process
1. **Initialize Systems**: Get helicopter, engine, and rotor models
2. **Load Mission**: Get mission definition with segment list
3. **Execute Segments**: Run each segment type with appropriate parameters
4. **Track Progress**: Maintain altitude tracking and mission log
5. **Handle Results**: Aggregate logs and check for failures

### Segment Dispatch
Each segment type calls its specific execution function:
- **Hover**: Stationary flight power calculations
- **Vertical Climb**: Climb power with rate-of-climb energy
- **Forward Climb**: Combined forward flight and climb power
- **Cruise**: Level forward flight optimization
- **Loiter**: Low-speed forward flight
- **Payload**: Mass change operations with hover phases

### Error Handling
- Individual segment failures stop mission execution
- Unknown segment types cause immediate failure
- Complete mission log preserved for analysis

### Integration Points
- Mission planner segment execution functions
- Helicopter and engine models
- Flight simulation for performance calculations