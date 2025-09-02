# Blade Module Flow Diagram

```mermaid
flowchart TD
    A[Start: Blade Class] --> B[Initialize Parameters<br/>R_root, R_tip, c_root, c_tip<br/>theta_root_rad, theta_tip_rad, airfoil]
    
    B --> C[Method: c(r)]
    B --> D[Method: theta(r)]
    
    C --> E[Calculate μ = (r - R_root) / (R_tip - R_root)]
    E --> F[Linear Taper<br/>c = c_root + μ×(c_tip - c_root)]
    F --> G[Return chord c]
    
    D --> H[Calculate μ = (r - R_root) / (R_tip - R_root)]
    H --> I[Linear Twist<br/>θ = θ_root + μ×(θ_tip - θ_root)]
    I --> J[Return twist angle θ]
    
    G --> K[End]
    J --> K

    style A fill:#e1f5fe
    style K fill:#e8f5e8
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style F fill:#fff3e0
    style I fill:#fff3e0
```

## Class: Blade
**Purpose**: Define blade geometry with linear taper and twist distribution

### Constructor Parameters
- **R_root**: Root radius (m)
- **R_tip**: Tip radius (m) 
- **c_root**: Root chord (m)
- **c_tip**: Tip chord (m)
- **theta_root_rad**: Root twist angle (rad)
- **theta_tip_rad**: Tip twist angle (rad)
- **airfoil**: Airfoil object reference

### Methods
- **c(r)**: Returns chord length at radius r using linear taper
- **theta(r)**: Returns twist angle at radius r using linear distribution