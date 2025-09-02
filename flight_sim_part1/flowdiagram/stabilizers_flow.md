# Stabilizers Module Flow Diagram

```mermaid
flowchart TD
    A[Start: Stabilizers Class] --> B[Initialize Parameters<br/>S_h, i_h_deg, CLa_h_per_rad, l_h<br/>S_v, CYb_v_per_rad, l_v]
    B --> C[Convert i_h to radians]
    
    C --> D[Method: forces_moments]
    D --> E[Input: ρ, V, α_fus_rad=0, β_rad=0]
    E --> F[Calculate dynamic pressure<br/>q = 0.5×ρ×V²]
    
    F --> G[Horizontal Stabilizer<br/>L_h = q×S_h×CLa_h×(α_fus + i_h)]
    G --> H[Vertical Stabilizer<br/>Y_v = q×S_v×CYb_v×β]
    
    H --> I[Pitching Moment<br/>M_pitch = -L_h×l_h]
    I --> J[Yawing Moment<br/>M_yaw = Y_v×l_v]
    
    J --> K[Return Dictionary<br/>{L_h, Y_v, M_pitch, M_yaw}]
    K --> L[End]

    style A fill:#e1f5fe
    style L fill:#e8f5e8
    style D fill:#e3f2fd
    style F fill:#fff3e0
    style G fill:#fff3e0
    style H fill:#fff3e0
    style I fill:#f3e5f5
    style J fill:#f3e5f5
```

## Class: Stabilizers
**Purpose**: Calculate forces and moments from horizontal and vertical stabilizers

### Constructor Parameters
- **S_h**: Horizontal stabilizer area (m²)
- **i_h_deg**: Horizontal stabilizer incidence angle (degrees)
- **CLa_h_per_rad**: Horizontal stabilizer lift curve slope (per radian)
- **l_h**: Horizontal stabilizer moment arm (m)
- **S_v**: Vertical stabilizer area (m²)
- **CYb_v_per_rad**: Vertical stabilizer side force curve slope (per radian)
- **l_v**: Vertical stabilizer moment arm (m)

### Method: forces_moments(ρ, V, α_fus_rad, β_rad)
**Inputs**:
- **ρ**: Air density (kg/m³)
- **V**: Airspeed (m/s)
- **α_fus_rad**: Fuselage angle of attack (rad)
- **β_rad**: Sideslip angle (rad)

**Outputs**:
- **L_h**: Horizontal stabilizer lift force (N)
- **Y_v**: Vertical stabilizer side force (N)
- **M_pitch**: Pitching moment (N·m)
- **M_yaw**: Yawing moment (N·m)