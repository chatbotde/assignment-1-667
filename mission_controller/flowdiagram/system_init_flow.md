# System Initialization Flow Diagram

```mermaid
flowchart TD
    A[Start: SystemInitializer] --> B[Initialize Variables<br/>fs_inputs=None<br/>rotor=None<br/>helicopter=None<br/>engine=None]
    
    B --> C[initialize_systems]
    C --> D[Initialize Flight Simulation]
    D --> E[Call get_user_inputs<br/>from flight_sim_part1]
    E --> F[Call build_rotor<br/>from flight_sim_part1]
    F --> G[Log Flight Sim Success<br/>Rotor radius, blade count]
    
    G --> H[Initialize Mission Planner]
    H --> I[Call get_helicopter_and_engine<br/>from mission_planner_part2]
    I --> J[Extract helicopter, engine, mp_rotor]
    J --> K[Log Mission Planner Success<br/>Aircraft mass, engine power]
    
    K --> L[validate_system_compatibility]
    L --> M[Check Rotor Compatibility<br/>Compare fs_radius vs mp_radius]
    M --> N{Radius Match?}
    N -->|No| O[Print Warning<br/>Radius mismatch]
    N -->|Yes| P[Log Compatibility Success]
    O --> Q[Test Flight Simulation]
    P --> Q
    
    Q --> R[Get ISA Properties<br/>isa_properties(0)]
    R --> S[Calculate omega<br/>2π×960/60]
    S --> T[Call cycle_integrator<br/>rotor, V=0, omega, rho]
    T --> U{Test Success?}
    U -->|No| V[Print Error<br/>Raise Exception]
    U -->|Yes| W[Log Test Results<br/>Thrust, Power]
    
    W --> X[Log Validation Complete]
    X --> Y[End]
    V --> Y

    style A fill:#e1f5fe
    style Y fill:#e8f5e8
    style N fill:#ffeb3b
    style U fill:#ffeb3b
    style D fill:#e3f2fd
    style H fill:#e3f2fd
    style L fill:#fff3e0
    style Q fill:#f3e5f5
    style V fill:#ffcdd2
    style O fill:#fff9c4
```

## Class: SystemInitializer
**Purpose**: Initialize and validate flight simulation and mission planner systems

### Initialization Process
1. **Flight Simulation Setup**
   - Load user inputs and configuration
   - Build rotor model with geometry and aerodynamics
   - Validate flight simulation components

2. **Mission Planner Setup**
   - Initialize helicopter, engine, and rotor models
   - Load mission planner configuration
   - Validate mission planner components

3. **Compatibility Validation**
   - Compare rotor configurations between systems
   - Test flight simulation with sample calculation
   - Ensure system integration works correctly

### Key Validations
- **Rotor Compatibility**: Radius and configuration matching
- **Flight Simulation Test**: Hover calculation at sea level
- **System Integration**: Cross-system data consistency

### Error Handling
- Graceful failure with detailed error messages
- System compatibility warnings
- Validation test results logging