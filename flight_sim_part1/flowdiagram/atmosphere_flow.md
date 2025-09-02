# Atmosphere Module Flow Diagram

```mermaid
flowchart TD
    A[Start: isa_properties] --> B[Input: alt_m]
    B --> C[Initialize Constants<br/>T0=288.15K, p0=101325Pa<br/>rho0=1.225, g=9.80665<br/>L=-0.0065, R=287.05287, γ=1.4]
    C --> D{alt_m ≤ 11000m?}
    
    D -->|Yes| E[Troposphere Calculation<br/>T = T0 + L×alt_m]
    E --> F[p = p0 × (T/T0)^(-g/(L×R))]
    F --> G[rho = p / (R×T)]
    
    D -->|No| H[Stratosphere Calculation<br/>T = T0 + L×11000]
    H --> I[p = p0 × (T/T0)^(-g/(L×R)) × exp(-g×(alt_m-11000)/(R×T))]
    I --> J[rho = p / (R×T)]
    
    G --> K[Calculate Speed of Sound<br/>a = √(γ×R×T)]
    J --> K
    K --> L[Return rho, a]
    L --> M[End]

    style A fill:#e1f5fe
    style M fill:#e8f5e8
    style E fill:#fff3e0
    style F fill:#fff3e0
    style G fill:#fff3e0
    style H fill:#ffebee
    style I fill:#ffebee
    style J fill:#ffebee
    style K fill:#f3e5f5
```

## Function: isa_properties(alt_m)
**Purpose**: Calculate atmospheric properties using International Standard Atmosphere model

### Inputs
- **alt_m**: Altitude in meters

### Outputs
- **rho**: Air density (kg/m³)
- **a**: Speed of sound (m/s)

### Logic
- **Troposphere (≤11km)**: Linear temperature decrease
- **Stratosphere (>11km)**: Isothermal approximation