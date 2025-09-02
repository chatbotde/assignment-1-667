# Aircraft Sizer Flow Diagram

```mermaid
flowchart TD
    A[Start: AircraftSizer] --> B[size_aircraft Method]
    B --> C[Input: requirements, main_rotor<br/>tail_rotor, pusher_prop, wings]
    
    C --> D[Create Mass Breakdown Dictionary]
    D --> E[Fixed Mass Components]
    E --> F[Payload: requirements["total_payload_kg"]]
    E --> G[Crew: 2 × 70kg = 140kg]
    E --> H[Fuel: 800kg (estimated for 500km range)]
    
    F --> I[Component Mass Estimates]
    G --> I
    H --> I
    I --> J[Main Rotor: 450kg]
    I --> K[Tail Rotor: 80kg]
    I --> L[Pusher Propeller: 60kg]
    I --> M[Wings: 200kg]
    
    J --> N[Aircraft System Masses]
    K --> N
    L --> N
    M --> N
    N --> O[Fuselage: 600kg]
    N --> P[Landing Gear: 120kg]
    N --> Q[Engines: 400kg]
    N --> R[Systems: 300kg]
    N --> S[Structure: 400kg]
    
    O --> T[Calculate Derived Masses]
    P --> T
    Q --> T
    R --> T
    S --> T
    
    T --> U[Empty Weight = Sum of all components<br/>(excluding payload, crew, fuel)]
    U --> V[Operating Empty = Empty Weight + Crew]
    V --> W[Max Takeoff = Sum of all masses]
    
    W --> X[Create Dimensions Dictionary]
    X --> Y[Overall Dimensions]
    Y --> Z[Length: 18.5m]
    Y --> AA[Height: 4.8m]
    Y --> BB[Width: 2.8m]
    
    Z --> CC[Rotor Dimensions]
    AA --> CC
    BB --> CC
    CC --> DD[Main Rotor Diameter: main_rotor["radius_m"] × 2]
    CC --> EE[Tail Rotor Diameter: tail_rotor["radius_m"] × 2]
    
    DD --> FF[Print Summary Information<br/>Max takeoff weight, overall length]
    EE --> FF
    FF --> GG[Return mass_breakdown, dimensions]
    
    HH[calculate_component_masses Method] --> II[Input: main_rotor, tail_rotor<br/>pusher_prop, wings]
    II --> JJ[Estimate Individual Component Masses]
    JJ --> KK[_estimate_rotor_mass Method<br/>disk_area × num_blades × 2.5 kg/m²/blade]
    JJ --> LL[_estimate_propeller_mass Method<br/>disk_area × num_blades × 1.5 kg/m²/blade]
    JJ --> MM[_estimate_wing_mass Method<br/>wing_area × 8.0 kg/m²]
    
    KK --> NN[Return Component Mass Dictionary]
    LL --> NN
    MM --> NN
    
    GG --> OO[End]
    NN --> OO

    style A fill:#e1f5fe
    style OO fill:#e8f5e8
    style B fill:#e3f2fd
    style HH fill:#e3f2fd
    style D fill:#fff3e0
    style E fill:#fff3e0
    style I fill:#fff3e0
    style N fill:#fff3e0
    style T fill:#fff3e0
    style X fill:#fff3e0
    style Y fill:#fff3e0
    style CC fill:#fff3e0
    style JJ fill:#fff3e0
    style F fill:#f3e5f5
    style G fill:#f3e5f5
    style H fill:#f3e5f5
    style J fill:#ffcdd2
    style K fill:#ffcdd2
    style L fill:#ffcdd2
    style M fill:#ffcdd2
    style O fill:#e8f5e8
    style P fill:#e8f5e8
    style Q fill:#e8f5e8
    style R fill:#e8f5e8
    style S fill:#e8f5e8
```

## Aircraft Sizer Component
**Purpose**: Calculate overall aircraft mass breakdown and dimensions

### Mass Breakdown Process

#### Fixed Masses (Mission Requirements)
- **Payload**: From design requirements (10 persons × 70kg = 700kg)
- **Crew**: 2 pilots × 70kg = 140kg
- **Fuel**: 800kg (estimated for 500km range requirement)

#### Component Masses (Design-Based)
**Rotating Components**:
- **Main Rotor**: 450kg (large rotor system with hub and controls)
- **Tail Rotor**: 80kg (smaller anti-torque system)
- **Pusher Propeller**: 60kg (compact propeller system)

**Fixed Components**:
- **Wings**: 200kg (12m span wing structure)
- **Fuselage**: 600kg (large cabin for 10 persons)
- **Landing Gear**: 120kg (retractable gear for high-speed flight)

#### System Masses (Aircraft Systems)
- **Engines**: 400kg (twin turboshaft engines ~2000kW total)
- **Systems**: 300kg (avionics, hydraulics, electrical, environmental)
- **Structure**: 400kg (primary structure, connections, fairings)

### Mass Calculations
**Derived Masses**:
1. **Empty Weight**: Sum of all components (excluding payload, crew, fuel)
2. **Operating Empty Weight**: Empty weight + crew
3. **Maximum Takeoff Weight**: Sum of all mass components

### Dimensional Analysis
**Overall Aircraft Envelope**:
- **Length**: 18.5m (accommodates rotor disk and tail boom)
- **Height**: 4.8m (rotor clearance and landing gear)
- **Width**: 2.8m (fuselage width for passenger cabin)

**Rotor Dimensions**:
- **Main Rotor Diameter**: 17.0m (2 × 8.5m radius)
- **Tail Rotor Diameter**: 3.6m (2 × 1.8m radius)

### Component Mass Estimation Methods

#### Rotor Mass Estimation
**Formula**: disk_area × num_blades × 2.5 kg/m²/blade
- Accounts for blade mass, hub, controls, and mounting structure
- Higher mass factor for main rotor due to complexity

#### Propeller Mass Estimation  
**Formula**: disk_area × num_blades × 1.5 kg/m²/blade
- Lower mass factor than rotors (simpler system)
- Includes propeller, hub, and drive system

#### Wing Mass Estimation
**Formula**: wing_area × 8.0 kg/m²
- Typical structural mass for transport aircraft wings
- Includes primary structure, control surfaces, and systems

### Design Validation
**Mass Distribution Check**:
- **Payload Fraction**: ~20% of MTOW (reasonable for transport)
- **Fuel Fraction**: ~23% of MTOW (adequate for 500km range)
- **Empty Weight Fraction**: ~57% of MTOW (typical for helicopters)

### Key Features
- **Requirements-Driven**: Masses based on mission requirements
- **Component-Based**: Individual component mass estimation
- **Realistic Proportions**: Based on existing helicopter data
- **Scalable Methods**: Mass estimation methods can be refined
- **Integration**: Considers all major aircraft systems

### Output Products
- **mass_breakdown**: Complete mass dictionary with all components
- **dimensions**: Aircraft envelope and major component dimensions
- **Summary Data**: Key metrics for design validation