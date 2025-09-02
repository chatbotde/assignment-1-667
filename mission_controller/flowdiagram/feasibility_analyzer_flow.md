# Feasibility Analyzer Flow Diagram

```mermaid
flowchart TD
    A[Start: FeasibilityAnalyzer] --> B[Initialize<br/>flight_analyzer, engine]
    
    B --> C[analyze_mission_feasibility]
    B --> D[generate_mission_summary]
    
    C --> E[Input: mission_config]
    E --> F[Extract segments from config]
    F --> G[Initialize Analysis Results<br/>feasible=True, issues=[], warnings=[]]
    
    G --> H[Segment Analysis Loop]
    H --> I{Segment Type?}
    I -->|hover/cruise/loiter| J[Extract altitude, velocity]
    I -->|other| K[Skip Analysis]
    
    J --> L[Call flight_analyzer.get_flight_parameters<br/>altitude, velocity]
    L --> M{Performance Valid?}
    M -->|No| N[Skip Segment]
    M -->|Yes| O[Store Performance Data<br/>thrust, power, efficiency, tip_mach]
    
    O --> P[Check Performance Limits]
    P --> Q{tip_mach > 0.85?}
    Q -->|Yes| R[Add Warning<br/>High tip Mach]
    Q -->|No| S[Check Power Limit]
    R --> S
    
    S --> T{power > 90% engine capacity?}
    T -->|Yes| U[Add Issue<br/>Power too high<br/>Set feasible=False]
    T -->|No| V[Continue]
    U --> V
    
    K --> W{More Segments?}
    N --> W
    V --> W
    W -->|Yes| H
    W -->|No| X[Return Analysis Results]
    
    D --> Y[Input: mission_config, mission_id, status]
    Y --> Z[Build Summary Header<br/>Name, ID, Description, Status]
    Z --> AA[Build Segments List]
    AA --> BB[Segment Details Loop]
    BB --> CC{Segment Type?}
    CC -->|hover| DD[Format: altitude, duration]
    CC -->|cruise| EE[Format: altitude, velocity, duration]
    CC -->|vclimb| FF[Format: start_alt, climb_rate, duration]
    CC -->|loiter| GG[Format: altitude, loiter_velocity, duration]
    CC -->|payload| HH[Format: operation, mass_change]
    
    DD --> II[Add to Summary]
    EE --> II
    FF --> II
    GG --> II
    HH --> II
    
    II --> JJ{More Segments?}
    JJ -->|Yes| BB
    JJ -->|No| KK[Call analyze_mission_feasibility]
    KK --> LL[Add Feasibility Results<br/>Issues and Warnings]
    LL --> MM[Return Complete Summary]
    
    X --> NN[End]
    MM --> NN

    style A fill:#e1f5fe
    style NN fill:#e8f5e8
    style I fill:#ffeb3b
    style M fill:#ffeb3b
    style Q fill:#ffeb3b
    style T fill:#ffeb3b
    style W fill:#ffeb3b
    style CC fill:#ffeb3b
    style JJ fill:#ffeb3b
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style L fill:#f3e5f5
    style P fill:#fff3e0
    style R fill:#fff9c4
    style U fill:#ffcdd2
```

## Class: FeasibilityAnalyzer
**Purpose**: Analyze mission feasibility and generate comprehensive reports

### Mission Feasibility Analysis
**Process**:
1. Extract flight segments from mission configuration
2. For each segment, calculate required performance
3. Check against aircraft and engine limitations
4. Identify issues (show-stoppers) and warnings

### Performance Checks
- **Tip Mach Limit**: Warning if > 0.85
- **Power Limit**: Issue if > 90% engine capacity
- **Flight Envelope**: Validate altitude/velocity combinations

### Mission Summary Generation
**Features**:
- Structured mission overview
- Segment-by-segment breakdown
- Feasibility assessment
- Issues and warnings listing

### Integration Points
- Flight analyzer for performance calculations
- Engine model for power limitations
- Mission types for segment validation