# Flight Analysis Flow Diagram

```mermaid
flowchart TD
    A[Start: FlightAnalyzer] --> B[Initialize<br/>rotor, fs_inputs]
    
    B --> C[get_flight_parameters]
    B --> D[analyze_performance_envelope]
    
    C --> E[Input: altitude, velocity]
    E --> F[Get ISA Properties<br/>ρ, a = isa_properties(altitude)]
    F --> G[Extract RPM from fs_inputs<br/>Convert to ω = 2π×rpm/60]
    G --> H[Call cycle_integrator<br/>rotor, velocity, ω, ρ]
    H --> I[Get T, Q, P from integrator]
    
    I --> J[Calculate Additional Parameters]
    J --> K[tip_speed = ω × R_tip]
    K --> L[tip_mach = tip_speed / a]
    L --> M[disk_area = π × R_tip²]
    M --> N[disk_loading = T / disk_area]
    N --> O[efficiency = T / (P/1000)]
    
    O --> P[Create FlightParameters Object<br/>thrust_N, torque_Nm, power_kW<br/>rpm, tip_mach, disk_loading, efficiency]
    P --> Q[Return FlightParameters]
    
    D --> R[Input: altitudes[], velocities[]]
    R --> S[Initialize envelope = {}]
    S --> T[Altitude Loop]
    T --> U[Velocity Loop]
    U --> V[Call get_flight_parameters<br/>for each (alt, vel) pair]
    V --> W[Store Results<br/>power_kW, efficiency, tip_mach]
    W --> X{More Velocities?}
    X -->|Yes| U
    X -->|No| Y{More Altitudes?}
    Y -->|Yes| T
    Y -->|No| Z[Return Performance Envelope]
    
    Q --> AA[End]
    Z --> AA

    style A fill:#e1f5fe
    style AA fill:#e8f5e8
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style H fill:#f3e5f5
    style J fill:#fff3e0
    style T fill:#fff3e0
    style U fill:#fff3e0
    style X fill:#ffeb3b
    style Y fill:#ffeb3b
```

## Class: FlightAnalyzer
**Purpose**: Calculate flight performance parameters using flight simulation

### Key Method: get_flight_parameters(altitude, velocity)
**Process**:
1. Get atmospheric properties at specified altitude
2. Extract RPM from flight simulation inputs
3. Run cycle integrator for thrust, torque, power
4. Calculate derived parameters (tip Mach, disk loading, efficiency)
5. Return structured FlightParameters object

### Performance Envelope Analysis
**Features**:
- Multi-point analysis across altitude/velocity grid
- Systematic performance mapping
- Tip Mach number tracking
- Power and efficiency analysis

### Calculated Parameters
- **Primary**: Thrust, torque, power, RPM
- **Derived**: Tip Mach, disk loading, efficiency
- **Environmental**: Atmospheric conditions integration

### Integration Points
- Flight simulation cycle integrator
- ISA atmospheric model
- Mission controller reporting system