# Inflow Module Flow Diagram

```mermaid
flowchart TD
    A[Start: Prandtl Tip Loss] --> B[Input: B, r, R, λ]
    B --> C[Calculate f = 0.5×B×(1-r/R)/λ]
    C --> D[Clamp f to [1e-8, 50.0]]
    D --> E[F = (2/π)×arccos(exp(-f))]
    E --> F[Return F ≥ 1e-6]
    
    G[Start: Induced Velocity] --> H[Input: rotor, r, V, ω, ρ]
    H --> I[Initialize Parameters<br/>Ut = ω×r, c = blade.c(r)<br/>θ = blade.theta(r)]
    I --> J[Initial Guess: vi = 0.05×max(1.0, Ut)]
    
    J --> K[Iteration Loop<br/>max_iter=200, tol=1e-6]
    K --> L[Calculate Uax = V + vi]
    L --> M[Calculate φ = atan2(Uax, Ut)]
    M --> N[Calculate λ_local = (V+vi)/(ω×r)]
    N --> O[Get Prandtl Factor F]
    O --> P[Calculate U = √(Ut² + Uax²)]
    P --> Q[Calculate q = 0.5×ρ×U²]
    Q --> R[Calculate α = θ - φ]
    R --> S[Get Airfoil Data: Cl, Cd = airfoil.lookup(α)]
    
    S --> T[Blade Element Theory<br/>dT_BE_dr = B×q×c×(Cl×cos(φ) - Cd×sin(φ))]
    T --> U[Momentum Theory<br/>dT_MT_dr = 4π×ρ×F×r×Uax×vi]
    U --> V[Residual: Rres = dT_BE_dr - dT_MT_dr]
    
    V --> W{|Rres| < tolerance?}
    W -->|No| X[Finite Difference Calculation<br/>Calculate dR/dvi]
    X --> Y[Newton-Raphson Step<br/>vi = vi + damp×(-Rres/(dR/dvi))]
    Y --> Z[Clamp vi ≥ 0]
    Z --> K
    
    W -->|Yes| AA[Final Calculations<br/>Update φ, q, α, Cl, Cd]
    AA --> BB[Return vi, φ, q, Cl, Cd, U]
    
    F --> CC[End]
    BB --> CC

    style A fill:#e1f5fe
    style G fill:#e1f5fe
    style CC fill:#e8f5e8
    style K fill:#fff3e0
    style W fill:#ffeb3b
    style S fill:#f3e5f5
    style O fill:#f3e5f5
```

## Functions Overview

### prandtl_tip_loss(B, r, R, lambda_)
**Purpose**: Calculate Prandtl tip loss factor to account for finite blade effects

### induced_velocity_annulus(rotor, r, V, omega, rho)
**Purpose**: Solve for induced velocity at blade annulus using Newton-Raphson iteration

### Key Features
- **Iterative Solution**: Newton-Raphson method with damping
- **Blade Element Theory**: Force calculation from airfoil data
- **Momentum Theory**: Theoretical thrust from induced velocity
- **Convergence**: Balance between BET and momentum theory