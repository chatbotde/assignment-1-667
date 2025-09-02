# Planner Utils Flow Diagram

```mermaid
flowchart TD
    A[Start: Planner Utils] --> B[tip_mach Function]
    A --> C[solve_rpm_for_thrust Function]
    A --> D[parasite_power Function]
    A --> E[tail_power_fraction Function]
    
    B --> F[Input: ω, R_tip, a]
    F --> G[Calculate Tip Mach<br/>M_tip = (ω × R_tip) / max(1e-9, a)]
    G --> H[Return M_tip]
    
    C --> I[Input: rotor, ρ, a, V_forward, thrust_req_N<br/>rpm_lo=200, rpm_hi=390, tol=1e-3]
    I --> J[Calculate Tip Mach Limit<br/>rpm_hi = min(rpm_hi, tip_mach_limit × a / R × 60/(2π))]
    J --> K[Define thrust_at_rpm Function<br/>ω = 2π×rpm/60<br/>T, Q, P = cycle_integrator(rotor, V, ω, ρ)]
    
    K --> L[Test Boundary Conditions<br/>T_lo = thrust_at_rpm(rpm_lo)<br/>T_hi = thrust_at_rpm(rpm_hi)]
    L --> M{T_hi ≥ thrust_req_N?}
    M -->|No| N[Raise ValueError<br/>"Thrust requirement exceeds capability"]
    M -->|Yes| O[Bisection Search Loop<br/>max 40 iterations]
    
    O --> P[Calculate Midpoint<br/>rpm_mid = 0.5 × (rpm_lo + rpm_hi)]
    P --> Q[Get Thrust at Midpoint<br/>T_mid, Q_mid, P_mid = thrust_at_rpm(rpm_mid)]
    Q --> R{|T_mid - thrust_req_N| ≤ tolerance?}
    R -->|Yes| S[Converged<br/>ω_mid = 2π×rpm_mid/60<br/>Return rpm_mid, ω_mid, T_mid, Q_mid, P_mid]
    R -->|No| T{T_mid < thrust_req_N?}
    T -->|Yes| U[Update Lower Bound<br/>rpm_lo = rpm_mid]
    T -->|No| V[Update Upper Bound<br/>rpm_hi = rpm_mid]
    U --> W{More Iterations?}
    V --> W
    W -->|Yes| P
    W -->|No| X[Return Final Result<br/>rpm_mid, ω_mid, T_mid, Q_mid, P_mid]
    
    D --> Y[Input: ρ, V, S_ref_m2=6.0, CD0=0.04]
    Y --> Z[Calculate Dynamic Pressure<br/>q = 0.5 × ρ × V²]
    Z --> AA[Calculate Drag Force<br/>D = q × S_ref_m2 × CD0]
    AA --> BB[Calculate Parasite Power<br/>P_parasite = D × V (Watts)]
    BB --> CC[Return P_parasite]
    
    E --> DD[Input: V, f_hover=0.07, f_min=0.015, V0=30.0]
    DD --> EE[Calculate Exponential Decay<br/>exp_term = exp(-(V/V0)²)]
    EE --> FF[Calculate Tail Power Fraction<br/>f_tail = f_min + (f_hover - f_min) × exp_term]
    FF --> GG[Return f_tail]
    
    H --> HH[End]
    N --> HH
    S --> HH
    X --> HH
    CC --> HH
    GG --> HH

    style A fill:#e1f5fe
    style HH fill:#e8f5e8
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style M fill:#ffeb3b
    style R fill:#ffeb3b
    style T fill:#ffeb3b
    style W fill:#ffeb3b
    style N fill:#ffcdd2
    style K fill:#f3e5f5
    style O fill:#fff3e0
    style Y fill:#fff3e0
    style DD fill:#fff3e0
```

## Planner Utils Module
**Purpose**: Utility functions for mission planning calculations and optimization

### Function: tip_mach(ω, R_tip, a)
**Purpose**: Calculate rotor tip Mach number
- Simple calculation: M_tip = (ω × R_tip) / a
- Used for rotor speed limitations and performance analysis

### Function: solve_rpm_for_thrust(rotor, ρ, a, V_forward, thrust_req_N)
**Purpose**: Find RPM that produces required thrust using bisection method

**Key Features**:
- **Tip Mach Limiting**: Automatically constrains RPM to stay within tip Mach limits
- **Bisection Search**: Robust numerical method with 40-iteration limit
- **Integration**: Uses flight simulation cycle_integrator for accurate thrust prediction
- **Error Handling**: Raises ValueError if thrust requirement is infeasible

**Process**:
1. Limit maximum RPM based on tip Mach constraint
2. Test boundary conditions to ensure feasibility
3. Iteratively narrow RPM range using bisection
4. Return converged RPM, angular velocity, and performance parameters

### Function: parasite_power(ρ, V, S_ref_m2, CD0)
**Purpose**: Calculate power required to overcome fuselage drag

**Formula**: P = D × V = (0.5 × ρ × V² × S_ref × CD0) × V
- Accounts for fuselage drag in forward flight
- Critical for cruise and forward climb power calculations

### Function: tail_power_fraction(V, f_hover, f_min, V0)
**Purpose**: Calculate tail rotor power as fraction of main rotor power

**Model**: Exponential decay from hover to forward flight
- **Hover**: 7% of main rotor power (anti-torque requirement)
- **Forward Flight**: Reduces to 1.5% minimum (reduced anti-torque need)
- **Transition**: Smooth exponential decay with 30 m/s characteristic velocity

### Integration Points
- Used by all mission segments for power calculations
- Critical for RPM optimization and feasibility analysis
- Provides realistic power component modeling