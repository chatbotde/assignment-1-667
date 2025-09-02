# Airfoil Calculation Flow Diagram

```mermaid
flowchart TD
    A[Start: Initialize Airfoil] --> B[Set Parameters<br/>a0, Cd0, e, alpha_stall]
    B --> C[Input: alpha_rad]
    C --> D[Call lookup method]
    D --> E[Clamp alpha_eff<br/>within [-alpha_stall, +alpha_stall]]
    E --> F[Calculate Cl = a0 × alpha_eff]
    F --> G[Calculate k = 1/(π × 6 × e)]
    G --> H[Calculate Cd = Cd0 + k × Cl²]
    H --> I[Set Cm = 0.0]
    I --> J[Return Cl, Cd, Cm]
    J --> K[End]

    style A fill:#e1f5fe
    style K fill:#e8f5e8
    style F fill:#fff3e0
    style G fill:#fff3e0
    style H fill:#fff3e0
```

## Parameters
- **a0**: Lift curve slope (default: 2π)
- **Cd0**: Zero-lift drag coefficient (default: 0.008)
- **e**: Oswald efficiency factor (default: 0.9)
- **alpha_stall**: Stall angle in degrees (default: 15°)

## Outputs
- **Cl**: Coefficient of lift
- **Cd**: Coefficient of drag
- **Cm**: Coefficient of moment (constant 0.0)