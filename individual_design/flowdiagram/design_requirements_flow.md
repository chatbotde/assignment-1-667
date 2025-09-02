# Design Requirements Flow Diagram

```mermaid
flowchart TD
    A[Start: DesignRequirements] --> B[Initialize Requirements Dictionary]
    
    B --> C[Define Mission Requirements]
    C --> D[Max Takeoff Altitude: 3500m<br/>High altitude capability]
    C --> E[Desired Top Speed: 400 km/h<br/>Very high speed for helicopters]
    C --> F[Service Ceiling: 5000m<br/>Maximum operating altitude]
    C --> G[Range: 500km<br/>Long-range capability]
    
    D --> H[Define Payload Requirements]
    E --> H
    F --> H
    G --> H
    H --> I[Payload Persons: 10<br/>2 pilots + 8 passengers]
    H --> J[Person Mass: 70kg<br/>Standard person weight]
    H --> K[Total Payload: 10 × 70kg = 700kg<br/>Complete payload mass]
    
    I --> L[Print Requirements Summary<br/>Display all requirements with values]
    J --> L
    K --> L
    
    L --> M[Methods Available]
    M --> N[get_requirements Method]
    M --> O[update_requirement Method]
    M --> P[validate_requirements Method]
    
    N --> Q[Return requirements dictionary<br/>Complete requirements data]
    
    O --> R[Input: key, value]
    R --> S{Key exists in requirements?}
    S -->|Yes| T[Update requirements[key] = value<br/>Print update confirmation]
    S -->|No| U[Print warning message<br/>"Key is not a valid requirement"]
    
    P --> V[Check Requirement Reasonableness]
    V --> W[Initialize warnings list]
    W --> X[Validation Checks]
    
    X --> Y{Top speed > 350 km/h?}
    Y -->|Yes| Z[Add warning: "Top speed >350 km/h is very high for helicopters"]
    Y -->|No| AA[Continue validation]
    
    Z --> BB{Service ceiling > 6000m?}
    AA --> BB
    BB -->|Yes| CC[Add warning: "Service ceiling >6000m requires special considerations"]
    BB -->|No| DD[Continue validation]
    
    CC --> EE{Total payload > 1000kg?}
    DD --> EE
    EE -->|Yes| FF[Add warning: "Payload >1000kg requires large helicopter"]
    EE -->|No| GG[Validation complete]
    
    FF --> HH[Return warnings list]
    GG --> HH
    
    Q --> II[End]
    T --> II
    U --> II
    HH --> II

    style A fill:#e1f5fe
    style II fill:#e8f5e8
    style N fill:#e3f2fd
    style O fill:#e3f2fd
    style P fill:#e3f2fd
    style S fill:#ffeb3b
    style Y fill:#ffeb3b
    style BB fill:#ffeb3b
    style EE fill:#ffeb3b
    style C fill:#fff3e0
    style H fill:#fff3e0
    style M fill:#fff3e0
    style V fill:#fff3e0
    style X fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#f3e5f5
    style I fill:#c8e6c9
    style J fill:#c8e6c9
    style K fill:#c8e6c9
    style T fill:#e8f5e8
    style U fill:#ffcdd2
    style Z fill:#fff9c4
    style CC fill:#fff9c4
    style FF fill:#fff9c4
```

## Design Requirements Component
**Purpose**: Define and manage helicopter design requirements and constraints

### Requirements Definition
**Core Mission Requirements**:

#### Performance Requirements
- **Max Takeoff Altitude**: 3500m
  - High altitude capability for mountain operations
  - Requires consideration of engine power degradation
  - Affects rotor performance and sizing

- **Desired Top Speed**: 400 km/h
  - Very ambitious for helicopter (note: extremely high)
  - Drives compound configuration necessity
  - Requires advanced aerodynamic design

- **Service Ceiling**: 5000m
  - Maximum operational altitude
  - Critical for mission flexibility
  - Impacts engine and rotor design

- **Range**: 500km
  - Long-range capability requirement
  - Determines fuel capacity needs
  - Affects overall aircraft sizing

#### Payload Requirements
- **Payload Persons**: 10 total
  - 2 pilots (crew)
  - 8 passengers (payload)
  - Standard transport helicopter configuration

- **Person Mass**: 70kg standard
  - Industry standard person weight
  - Includes personal effects allowance
  - Used for mass calculations

- **Total Payload**: 700kg
  - 10 persons × 70kg each
  - Significant payload for helicopter
  - Drives aircraft size and power requirements

### Requirements Management Methods

#### get_requirements Method
**Purpose**: Provide access to complete requirements dictionary
- **Return**: Full requirements data structure
- **Usage**: Design modules access requirements
- **Integration**: Central requirements source

#### update_requirement Method
**Purpose**: Modify individual requirements during design process
- **Input**: Key-value pair for requirement update
- **Validation**: Checks if key exists in requirements
- **Feedback**: Confirmation or warning messages
- **Flexibility**: Allows design iteration and refinement

#### validate_requirements Method
**Purpose**: Check requirements for feasibility and reasonableness

##### Validation Checks
1. **Top Speed Validation**:
   - Warning if > 350 km/h
   - Reason: Very high for conventional helicopters
   - Implication: Requires advanced configuration

2. **Service Ceiling Validation**:
   - Warning if > 6000m
   - Reason: Requires special high-altitude considerations
   - Implication: Engine and cabin pressurization needs

3. **Payload Validation**:
   - Warning if > 1000kg
   - Reason: Requires large helicopter design
   - Implication: Significant size and power requirements

### Design Implications

#### High-Speed Requirement (400 km/h)
**Design Drivers**:
- Compound configuration necessity
- Advanced rotor systems
- Aerodynamic optimization
- Structural considerations

#### High-Altitude Requirement (3500m/5000m)
**Design Drivers**:
- Engine power degradation compensation
- Rotor performance at altitude
- Atmospheric density effects
- Oxygen system requirements

#### Large Payload (700kg)
**Design Drivers**:
- Large cabin volume
- High rotor disk loading
- Significant power requirements
- Structural strength needs

### Requirements Traceability
**Design Process Integration**:
- **Rotor Design**: Sized for altitude and payload
- **Aircraft Sizing**: Mass breakdown includes payload
- **Performance Analysis**: Validated against requirements
- **Mission Analysis**: Hover capability at altitude

### Key Features
- **Comprehensive Coverage**: All major design drivers included
- **Validation Logic**: Reasonableness checks for feasibility
- **Flexibility**: Updateable during design process
- **Integration**: Central source for all design modules
- **Documentation**: Clear requirement statements with rationale

### Design Challenge Recognition
The requirements represent a very challenging design:
- **400 km/h**: Extremely high for helicopters (typical max ~300 km/h)
- **High Altitude**: Significant performance degradation
- **Large Payload**: Requires substantial aircraft
- **Long Range**: High fuel requirements

This drives the compound helicopter configuration as the only feasible solution to meet all requirements simultaneously.