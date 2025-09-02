# Vehicle and Engine Models Flow Diagram

```mermaid
flowchart TD
    A[Start: Vehicle & Engine Models] --> B[Helicopter Model]
    A --> C[Engine Model]
    
    B --> D[Helicopter Class<br/>@dataclass]
    D --> E[Properties<br/>oew_kg: Operating Empty Weight<br/>payload_kg: Current Payload<br/>fuel_kg: Current Fuel]
    E --> F[Configuration<br/>S_ref_m2: Reference Area<br/>CD0_body: Drag Coefficient<br/>tail_power_hover_frac: Tail Power Fraction<br/>tail_power_min_frac: Minimum Tail Power]
    
    F --> G[mass_total Method]
    G --> H[Calculate Total Mass<br/>return oew_kg + payload_kg + fuel_kg]
    
    F --> I[weight_N Method]
    I --> J[Calculate Weight<br/>return mass_total() × g<br/>where g = 9.80665 m/s²]
    
    C --> K[Engine Class]
    K --> L[Properties<br/>P_sl_kW: Sea Level Power<br/>sfc_kg_per_kWh: Specific Fuel Consumption<br/>derate_alpha: Altitude Derate Factor]
    
    L --> M[power_available Method]
    M --> N[Input: Air Density ρ]
    N --> O[Calculate Density Ratio<br/>σ = ρ / ρ₀<br/>Clamp to [0.1, 2.0]]
    O --> P[Apply Altitude Derate<br/>P_avail = P_sl_kW × σ^derate_alpha]
    P --> Q[Return Available Power]
    
    L --> R[fuel_burn Method]
    R --> S[Input: power_kW, dt_s]
    S --> T[Convert Time to Hours<br/>hours = dt_s / 3600]
    T --> U[Calculate Fuel Burn<br/>fuel_kg = max(0, power_kW) × hours × sfc_kg_per_kWh]
    U --> V[Return Fuel Consumption]
    
    H --> W[End]
    J --> W
    Q --> W
    V --> W

    style A fill:#e1f5fe
    style W fill:#e8f5e8
    style D fill:#e3f2fd
    style K fill:#e3f2fd
    style G fill:#fff3e0
    style I fill:#fff3e0
    style M fill:#fff3e0
    style R fill:#fff3e0
    style O fill:#f3e5f5
    style P fill:#f3e5f5
    style T fill:#f3e5f5
    style U fill:#f3e5f5
```

## Vehicle and Engine Models
**Purpose**: Define helicopter and engine characteristics for mission planning

### Helicopter Model
**Key Properties**:
- **Mass Components**: Operating empty weight, payload, fuel
- **Aerodynamics**: Reference area, body drag coefficient
- **Power Distribution**: Tail rotor power fractions

**Methods**:
- **mass_total()**: Sum of all mass components
- **weight_N()**: Total weight in Newtons (mass × gravity)

### Engine Model
**Key Properties**:
- **Power Rating**: Sea level maximum power (kW)
- **Fuel Consumption**: Specific fuel consumption (kg/kWh)
- **Altitude Performance**: Power derate factor with altitude

**Methods**:
- **power_available(ρ)**: Available power at given air density
  - Uses density ratio with altitude derate factor
  - Accounts for reduced performance at altitude
  
- **fuel_burn(power_kW, dt_s)**: Fuel consumption calculation
  - Based on actual power used and time duration
  - Uses specific fuel consumption rate

### Integration Points
- Mission segments use these models for:
  - Weight calculations (affects thrust requirements)
  - Power availability checks (feasibility)
  - Fuel consumption tracking (endurance)
  - Performance degradation with altitude