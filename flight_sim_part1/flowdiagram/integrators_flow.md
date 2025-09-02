# Integrators Module Flow Diagram

```mermaid
flowchart TD
    A[Start: Instantaneous Integrator] --> B[Input: rotor, V_forward, ω, ρ]
    B --> C[Setup Radial Discretization<br/>n_sections=48, cosine spacing]
    C --> D[Setup Azimuthal Discretization<br/>n_azimuth=36, uniform spacing]
    D --> E[Initialize Arrays: T_psi, Q_psi]
    
    E --> F[Azimuth Loop: ψ = 0 to 2π]
    F --> G[Calculate Forward Velocity Components<br/>Vax_ψ = V_forward×cos(ψ)<br/>Vtan_ψ = V_forward×sin(ψ)]
    G --> H[Initialize T = 0, Q = 0]
    
    H --> I[Radial Loop: r from root to tip]
    I --> J{c(r) > 0?}
    J -->|No| K[Skip Section]
    J -->|Yes| L[Call induced_velocity_annulus<br/>Get vi, φ, q, Cl, Cd, U]
    
    L --> M[Update Velocities<br/>Ut = ω×r + Vtan_ψ<br/>Uax = Vax_ψ + vi]
    M --> N[Recalculate φ, U, q]
    N --> O[Calculate Forces<br/>Lp = q×c×Cl<br/>Dp = q×c×Cd]
    O --> P[Calculate Increments<br/>dT = B×(Lp×cos(φ) - Dp×sin(φ))×dr<br/>dQ = B×(Lp×sin(φ) + Dp×cos(φ))×r×dr]
    P --> Q[Accumulate: T += dT, Q += dQ]
    
    K --> R{More radial sections?}
    Q --> R
    R -->|Yes| I
    R -->|No| S[Store T_psi[j] = T, Q_psi[j] = Q]
    
    S --> T{More azimuth angles?}
    T -->|Yes| F
    T -->|No| U[Return T_psi, Q_psi arrays]
    
    V[Start: Cycle Integrator] --> W[Call instantaneous_integrator]
    W --> X[Calculate Averages<br/>T = mean(T_psi)<br/>Q = mean(Q_psi)]
    X --> Y[Calculate Power: P = Q×ω]
    Y --> Z[Return T, Q, P]
    
    U --> AA[End]
    Z --> AA

    style A fill:#e1f5fe
    style V fill:#e1f5fe
    style AA fill:#e8f5e8
    style F fill:#fff3e0
    style I fill:#fff3e0
    style J fill:#ffeb3b
    style L fill:#f3e5f5
    style T fill:#ffeb3b
    style R fill:#ffeb3b
```

## Functions Overview

### instantaneous_integrator(rotor, V_forward, omega, rho)
**Purpose**: Calculate thrust and torque distributions across azimuth angles

**Key Features**:
- **Radial Integration**: 48 sections with cosine spacing
- **Azimuthal Integration**: 36 uniform azimuth angles
- **Forward Flight**: Accounts for cyclic velocity variations

### cycle_integrator(rotor, V_forward, omega, rho)
**Purpose**: Calculate cycle-averaged thrust, torque, and power

**Process**:
1. Call instantaneous integrator
2. Average results over full rotor revolution
3. Calculate power from torque and angular velocity