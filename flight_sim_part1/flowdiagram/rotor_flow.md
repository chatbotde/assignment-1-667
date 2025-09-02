# Rotor Module Flow Diagram

```mermaid
flowchart TD
    A[Start: Rotor Class] --> B[Initialize Parameters<br/>B: Number of blades<br/>blade: Blade object<br/>tip_mach_limit: Safety limit]
    
    B --> C[Method: solidity_local(r)]
    
    C --> D[Get chord at radius: c = blade.c(r)]
    D --> E[Calculate circumference: 2π×r]
    E --> F[Calculate local solidity<br/>σ = (B×c)/(2π×r)]
    F --> G[Return σ]
    
    G --> H[End]

    style A fill:#e1f5fe
    style H fill:#e8f5e8
    style C fill:#e3f2fd
    style F fill:#fff3e0
```

## Class: Rotor
**Purpose**: Define rotor configuration and calculate local properties

### Constructor Parameters
- **B**: Number of blades (integer)
- **blade**: Blade object containing geometry
- **tip_mach_limit**: Maximum allowable tip Mach number (default: 0.90)

### Methods
- **solidity_local(r)**: Calculate local solidity ratio at radius r

### Local Solidity Formula
σ = (B × c(r)) / (2π × r)

Where:
- B = number of blades
- c(r) = chord length at radius r
- r = radial position