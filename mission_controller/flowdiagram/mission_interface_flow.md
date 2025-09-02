# Mission Interface Flow Diagram

```mermaid
flowchart TD
    A[Start: MissionInterface] --> B[Initialize<br/>MissionController<br/>FeasibilityAnalyzer<br/>active_missions={}]
    
    B --> C[Mission Creation Methods]
    B --> D[Mission Control Methods]
    B --> E[Analysis Methods]
    B --> F[File Operations]
    
    C --> G[create_simple_mission]
    C --> H[create_custom_mission]
    
    G --> I[Get Predefined Missions<br/>from MissionTypes]
    I --> J{Mission Type Valid?}
    J -->|No| K[Raise ValueError]
    J -->|Yes| L[Get Mission Config]
    L --> M[Call controller.create_mission]
    M --> N[Store in active_missions]
    N --> O[Log Creation Success]
    
    H --> P[Validate Segments<br/>MissionTypes.validate_mission_segments]
    P --> Q[Create Mission Config<br/>name, description, segments]
    Q --> R[Call controller.create_mission]
    R --> S[Store in active_missions]
    
    D --> T[execute_mission]
    D --> U[pause_mission]
    D --> V[resume_mission]
    D --> W[abort_mission]
    
    T --> X{Mission in active_missions?}
    X -->|No| Y[Print Error<br/>Return False]
    X -->|Yes| Z[Call controller.execute_mission]
    
    U --> AA[Create pause MissionCommand]
    V --> BB[Create resume MissionCommand]
    W --> CC[Create abort MissionCommand]
    AA --> DD[Send Command & Process]
    BB --> DD
    CC --> DD
    
    E --> EE[analyze_mission_feasibility]
    E --> FF[get_flight_performance]
    E --> GG[generate_mission_summary]
    
    EE --> HH[Call feasibility_analyzer.analyze_mission_feasibility]
    FF --> II[Call controller.get_flight_parameters]
    GG --> JJ[Call feasibility_analyzer.generate_mission_summary]
    
    F --> KK[save_mission]
    F --> LL[load_mission]
    
    KK --> MM[Write JSON to file]
    LL --> NN[Read JSON from file<br/>Create mission]
    
    O --> OO[End]
    K --> OO
    S --> OO
    Y --> OO
    Z --> OO
    DD --> OO
    HH --> OO
    II --> OO
    JJ --> OO
    MM --> OO
    NN --> OO

    style A fill:#e1f5fe
    style OO fill:#e8f5e8
    style J fill:#ffeb3b
    style X fill:#ffeb3b
    style G fill:#e3f2fd
    style H fill:#e3f2fd
    style T fill:#e3f2fd
    style U fill:#e3f2fd
    style V fill:#e3f2fd
    style W fill:#e3f2fd
    style EE fill:#fff3e0
    style FF fill:#fff3e0
    style GG fill:#fff3e0
```

## Class: MissionInterface
**Purpose**: High-level API for mission operations and user interaction

### Mission Creation
- **Simple Missions**: Predefined mission types (test, patrol, search_rescue, cargo)
- **Custom Missions**: User-defined segment sequences
- **Validation**: Automatic segment validation and feasibility checking

### Mission Control
- **Execution**: Start mission execution
- **Real-time Control**: Pause, resume, abort commands
- **Status Monitoring**: Get current mission status

### Analysis Features
- **Feasibility Analysis**: Check if mission is executable
- **Performance Analysis**: Calculate flight parameters
- **Mission Summary**: Generate comprehensive reports

### File Operations
- **Save/Load**: JSON-based mission configuration persistence
- **Mission Library**: Manage multiple mission configurations