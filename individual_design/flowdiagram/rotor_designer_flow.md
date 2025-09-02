# Rotor Designer Flow Diagram

```mermaid
flowchart TD
    A[Start: RotorDesigner] --> B[Component Design Methods]
    
    B --> C[design_main_rotor Method]
    B --> D[design_tail_rotor Method]
    B --> E[design_pusher_propeller Method]
    B --> F[design_wings Method]
    
    C --> G[Main Rotor Specifications]
    G --> H[Role: Primary lift generation, hover capability]
    G --> I[Geometry: 8.5m radius, 4 blades]
    G --> J[Operating Conditions: 320 RPM, tip Mach 0.85]
    G --> K[Blade Design: NACA 0012 modified airfoil<br/>0.45m root chord → 0.25m tip chord<br/>8° linear twist, 1.0m root cutout]
    G --> L[Performance: Solidity 0.08, optimized for hover]
    
    H --> M[Return Main Rotor Dictionary]
    I --> M
    J --> M
    K --> M
    L --> M
    
    D --> N[Tail Rotor Specifications]
    N --> O[Role: Yaw control and torque balance]
    N --> P[Geometry: 1.8m radius, 4 blades]
    N --> Q[Operating Conditions: 1600 RPM (higher for smaller rotor)]
    N --> R[Blade Design: NACA 0012 airfoil<br/>0.15m root chord → 0.10m tip chord<br/>No twist, 0.2m root cutout]
    N --> S[Performance: 12% of main rotor power]
    
    O --> T[Return Tail Rotor Dictionary]
    P --> T
    Q --> T
    R --> T
    S --> T
    
    E --> U[Pusher Propeller Specifications]
    U --> V[Role: Forward thrust for high-speed flight]
    U --> W[Geometry: 1.5m radius, 3 blades]
    U --> X[Operating Conditions: 2400 RPM (high speed)]
    U --> Y[Blade Design: Propeller airfoil<br/>0.20m root chord → 0.08m tip chord<br/>25° twist (high for propeller)<br/>0.15m root cutout]
    
    V --> Z[Return Pusher Propeller Dictionary]
    W --> Z
    X --> Z
    Y --> Z
    
    F --> AA[Wing Specifications]
    AA --> BB[Role: Lift generation at high forward speeds]
    AA --> CC[Geometry: 12.0m span, 1.8m chord<br/>21.6m² area, 6.67 aspect ratio]
    AA --> DD[Airfoil: NACA 23012 (cambered for lift)]
    AA --> EE[Configuration: 2° incidence, 5° dihedral]
    AA --> FF[Function: Rotor unloading at high speed]
    
    BB --> GG[Return Wings Dictionary]
    CC --> GG
    DD --> GG
    EE --> GG
    FF --> GG
    
    M --> HH[End]
    T --> HH
    Z --> HH
    GG --> HH

    style A fill:#e1f5fe
    style HH fill:#e8f5e8
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style F fill:#e3f2fd
    style G fill:#fff3e0
    style N fill:#fff3e0
    style U fill:#fff3e0
    style AA fill:#fff3e0
    style H fill:#f3e5f5
    style I fill:#f3e5f5
    style J fill:#f3e5f5
    style K fill:#f3e5f5
    style L fill:#f3e5f5
    style O fill:#ffcdd2
    style P fill:#ffcdd2
    style Q fill:#ffcdd2
    style R fill:#ffcdd2
    style S fill:#ffcdd2
    style V fill:#e8f5e8
    style W fill:#e8f5e8
    style X fill:#e8f5e8
    style Y fill:#e8f5e8
    style BB fill:#fff9c4
    style CC fill:#fff9c4
    style DD fill:#fff9c4
    style EE fill:#fff9c4
    style FF fill:#fff9c4
```

## Rotor Designer Component
**Purpose**: Design all rotating and lifting components for compound helicopter

### Main Rotor Design
**Optimization**: Hover efficiency and low-speed flight
- **Size**: 8.5m radius (large for efficient hover)
- **Configuration**: 4 blades for smooth operation
- **Speed**: 320 RPM (lower for larger rotor, tip Mach management)
- **Airfoil**: NACA 0012 modified for helicopter applications
- **Blade Planform**: Tapered from 0.45m root to 0.25m tip
- **Twist Distribution**: 8° linear twist for optimal inflow
- **Solidity**: 0.08 (8%) for good hover performance

### Tail Rotor Design
**Optimization**: Anti-torque efficiency and control authority
- **Size**: 1.8m radius (sized for main rotor torque)
- **Configuration**: 4 blades for reduced noise
- **Speed**: 1600 RPM (higher for smaller rotor)
- **Airfoil**: NACA 0012 (symmetric for bidirectional thrust)
- **Blade Planform**: Tapered from 0.15m root to 0.10m tip
- **Twist**: No twist (optimized for single operating condition)
- **Power**: 12% of main rotor power (typical helicopter ratio)

### Pusher Propeller Design
**Optimization**: High-speed forward thrust efficiency
- **Size**: 1.5m radius (compact for integration)
- **Configuration**: 3 blades (propeller standard)
- **Speed**: 2400 RPM (high speed for propeller efficiency)
- **Airfoil**: Specialized propeller airfoil sections
- **Blade Planform**: High taper ratio (0.20m to 0.08m)
- **Twist**: 25° (high twist typical for propellers)
- **Function**: Forward thrust for compound helicopter speed

### Wing Design
**Optimization**: High-speed rotor unloading
- **Span**: 12.0m (good aspect ratio for efficiency)
- **Chord**: 1.8m (constant chord for simplicity)
- **Area**: 21.6m² (sized for significant rotor unloading)
- **Aspect Ratio**: 6.67 (compromise between efficiency and structure)
- **Airfoil**: NACA 23012 (cambered for lift generation)
- **Incidence**: 2° (optimized for cruise conditions)
- **Dihedral**: 5° (lateral stability)

### Design Philosophy
**Compound Helicopter Concept**:
1. **Main Rotor**: Optimized for hover and low-speed flight
2. **Tail Rotor**: Conventional anti-torque system
3. **Pusher Propeller**: High-speed forward thrust
4. **Wings**: Rotor unloading at high forward speeds

### Performance Characteristics
- **Hover**: Main rotor provides all lift
- **Low Speed**: Main rotor dominant with tail rotor control
- **High Speed**: Wings provide lift, pusher provides thrust, main rotor unloaded
- **Transition**: Smooth transition between flight regimes

### Integration Considerations
- **Power Distribution**: Main rotor, tail rotor, pusher propeller
- **Control System**: Collective, cyclic, tail rotor, pusher thrust
- **Structural**: Wing mounting, propeller integration
- **Aerodynamic**: Interference effects between components

### Key Features
- **Multi-Mission Capability**: Hover efficiency + high-speed cruise
- **Advanced Configuration**: Compound helicopter benefits
- **Optimized Components**: Each component designed for its role
- **Realistic Parameters**: Based on existing helicopter technology