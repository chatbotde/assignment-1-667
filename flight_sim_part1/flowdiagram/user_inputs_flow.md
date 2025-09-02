# User Inputs Module Flow Diagram

```mermaid
flowchart TD
    A[Start: get_user_inputs] --> B[Define Rotor Configuration<br/>B=4, R_root=0.125, R_tip=0.762<br/>c_root=c_tip=0.0508<br/>θ_root=θ_tip=1.0°]
    
    B --> C[Define Airfoil Parameters<br/>a0=5.75, Cd0=0.0113<br/>e=1.25, α_stall=15°]
    
    C --> D[Define Stabilizer Parameters<br/>S_h=2.2, i_h=2°, CLa_h=6.5<br/>S_v=1.5, CYb_v=2.4]
    
    D --> E[Define Flight Conditions<br/>alt=0m, V_forward=0m/s<br/>rpm=960]
    
    E --> F[Return Configuration Dictionary]
    
    G[Start: build_rotor] --> H[Input: params dictionary]
    H --> I[Create Airfoil Object<br/>af = Airfoil(**params["airfoil"])]
    I --> J[Create Blade Object<br/>bl = Blade(R_root, R_tip, c_root, c_tip<br/>θ_root_rad, θ_tip_rad)]
    J --> K[Assign Airfoil to Blade<br/>bl.airfoil = af]
    K --> L[Create Rotor Object<br/>rotor = Rotor(B, bl, tip_mach_limit)]
    L --> M[Return Rotor Object]
    
    F --> N[End]
    M --> N

    style A fill:#e1f5fe
    style G fill:#e1f5fe
    style N fill:#e8f5e8
    style B fill:#fff3e0
    style C fill:#fff3e0
    style D fill:#fff3e0
    style E fill:#fff3e0
    style I fill:#f3e5f5
    style J fill:#f3e5f5
    style K fill:#f3e5f5
    style L fill:#f3e5f5
```

## Functions Overview

### get_user_inputs()
**Purpose**: Define default configuration parameters for helicopter simulation

**Configuration Sections**:
- **Rotor**: Blade count, geometry, airfoil properties
- **Stabilizers**: Horizontal and vertical stabilizer parameters  
- **Conditions**: Flight altitude, forward speed, RPM

### build_rotor(params)
**Purpose**: Construct rotor object from configuration parameters

**Process**:
1. Create Airfoil object with aerodynamic properties
2. Create Blade object with geometric properties
3. Link airfoil to blade
4. Create Rotor object with blade count and safety limits

### Default Configuration
- **4-blade rotor** with constant chord and twist
- **Experimental parameters** matching CSV data
- **Hover conditions** at sea level, 960 RPM