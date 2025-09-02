# Mission Planner Inputs Flow Diagram

```mermaid
flowchart TD
    A[Start: Mission Planner Inputs] --> B[get_helicopter_and_engine]
    A --> C[mission_definition]
    A --> D[fs_get_user_inputs]
    
    B --> E[Add Flight Sim Path<br/>add_flight_sim_path()]
    E --> F[Get Flight Sim Inputs<br/>fs_inputs = fs_get_inputs()]
    F --> G[Build Rotor from Flight Sim<br/>rotor = build_rotor(fs_inputs["rotor"])]
    
    G --> H[Create Helicopter Object<br/>oew_kg=2500, payload_kg=300<br/>fuel_kg=400, S_ref_m2=6.0<br/>CD0_body=0.045]
    H --> I[Set Tail Power Parameters<br/>tail_power_hover_frac=0.07<br/>tail_power_min_frac=0.015]
    
    I --> J[Create Engine Object<br/>P_sl_kW=1500, sfc_kg_per_kWh=0.32<br/>derate_alpha=0.7]
    J --> K[Return heli, engine, rotor]
    
    C --> L[Define Mission Segments List]
    L --> M[Segment 1: Hover<br/>60s at 0m altitude]
    L --> N[Segment 2: Vertical Climb<br/>120s, 0→360m at 3 m/s]
    L --> O[Segment 3: Cruise<br/>300s at 360m, 45 m/s]
    L --> P[Segment 4: Payload Drop<br/>100kg drop with 30s hover at 360m]
    L --> Q[Segment 5: Loiter<br/>120s at 360m, 25 m/s]
    L --> R[Segment 6: Forward Climb<br/>60s, 360→420m at 1 m/s, 35 m/s forward]
    L --> S[Segment 7: Cruise<br/>240s at 420m, 50 m/s]
    
    M --> T[Return Mission Segments List]
    N --> T
    O --> T
    P --> T
    Q --> T
    R --> T
    S --> T
    
    D --> U[Alias Function<br/>return fs_get_inputs()]
    
    K --> V[End]
    T --> V
    U --> V

    style A fill:#e1f5fe
    style V fill:#e8f5e8
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style H fill:#fff3e0
    style I fill:#fff3e0
    style J fill:#fff3e0
    style M fill:#f3e5f5
    style N fill:#f3e5f5
    style O fill:#f3e5f5
    style P fill:#f3e5f5
    style Q fill:#f3e5f5
    style R fill:#f3e5f5
    style S fill:#f3e5f5
```

## Mission Planner Inputs Module
**Purpose**: Configure helicopter, engine, and mission parameters for mission planning

### Function: get_helicopter_and_engine()
**Process**:
1. Import flight simulation path and modules
2. Get flight simulation inputs and build rotor model
3. Create helicopter with realistic parameters
4. Create engine with power and fuel consumption specs
5. Return integrated system components

### Helicopter Configuration
- **Mass**: 2500kg empty + 300kg payload + 400kg fuel = 3200kg total
- **Aerodynamics**: 6.0m² reference area, 0.045 drag coefficient
- **Tail Power**: 7% in hover, minimum 1.5% in forward flight

### Engine Configuration
- **Power**: 1500kW sea level maximum
- **Fuel Consumption**: 0.32 kg/kWh specific fuel consumption
- **Altitude**: 0.7 derate factor for altitude performance

### Mission Definition
**7-Segment Mission Profile**:
1. **Ground Hover**: 60s preparation
2. **Climb**: 120s to 360m altitude
3. **Transit Cruise**: 300s at 45 m/s
4. **Payload Drop**: 100kg with 30s hover
5. **Loiter**: 120s surveillance at 25 m/s
6. **Climb**: 60s to 420m with forward speed
7. **Return Cruise**: 240s at 50 m/s

### Integration Points
- Flight simulation rotor model for performance
- Mission segments for execution planning
- Vehicle and engine models for feasibility analysis