# Main Module Flow Diagram

```mermaid
flowchart TD
    A[Start: run] --> B[Get User Inputs<br/>inputs = get_user_inputs()]
    B --> C[Build Rotor<br/>rotor = build_rotor(inputs["rotor"])]
    C --> D[Get Atmospheric Properties<br/>ρ, a = isa_properties(alt_m)]
    
    D --> E[Extract Flight Conditions<br/>rpm, V_forward]
    E --> F[Convert RPM to rad/s<br/>ω = 2π×rpm/60]
    
    F --> G[Calculate Tip Mach Number<br/>M_tip = (ω×R_tip)/a]
    G --> H{M_tip > tip_mach_limit?}
    H -->|Yes| I[Print Warning Message]
    H -->|No| J[Continue]
    I --> J
    
    J --> K[Run Cycle Integrator<br/>T, Q, P = cycle_integrator(rotor, V, ω, ρ)]
    K --> L[Print Results<br/>Thrust, Torque, Power]
    
    L --> M[Create Stabilizers Object<br/>stab = Stabilizers(**inputs["stabilizers"])]
    M --> N[Calculate Stabilizer Forces<br/>fm = stab.forces_moments(ρ, V)]
    N --> O[Print Stabilizer Results]
    
    O --> P[End]

    style A fill:#e1f5fe
    style P fill:#e8f5e8
    style H fill:#ffeb3b
    style I fill:#ffcdd2
    style K fill:#f3e5f5
    style L fill:#e8f5e8
    style N fill:#f3e5f5
    style O fill:#e8f5e8
```

## Function: run()
**Purpose**: Main execution function that orchestrates the helicopter simulation

### Execution Flow
1. **Configuration**: Load user inputs and build rotor model
2. **Atmosphere**: Calculate air density and speed of sound
3. **Safety Check**: Verify tip Mach number within limits
4. **Rotor Analysis**: Calculate thrust, torque, and power
5. **Stabilizers**: Calculate stabilizer forces and moments
6. **Output**: Display all results

### Key Calculations
- **Angular Velocity**: ω = 2π × rpm / 60
- **Tip Mach**: M_tip = (ω × R_tip) / a
- **Rotor Performance**: Using cycle integrator
- **Stabilizer Loads**: Using stabilizer model

### Safety Features
- Tip Mach number warning system
- Automatic parameter validation