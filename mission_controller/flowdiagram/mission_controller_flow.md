# Mission Controller Main Flow Diagram

```mermaid
flowchart TD
    A[Start: MissionController] --> B[Initialize Components<br/>SystemInitializer, MissionExecutor<br/>FlightAnalyzer, ReportGenerator]
    B --> C[Initialize Systems<br/>Flight Sim + Mission Planner]
    
    C --> D[Mission Operations]
    D --> E[create_mission]
    D --> F[execute_mission]
    D --> G[monitor_mission]
    D --> H[send_command]
    
    E --> I[Create Mission Config<br/>mission_id, segments, parameters]
    I --> J[Initialize MissionStatus<br/>planning, fuel_remaining, position]
    J --> K[Update ReportGenerator]
    K --> L[Return mission_id]
    
    F --> M[Validate Mission Exists]
    M --> N{Mission Valid?}
    N -->|No| O[Return False]
    N -->|Yes| P[Set Status: executing]
    P --> Q[Call run_mission from planner_main]
    Q --> R[Update Status: completed/failed]
    
    G --> S[Get Current Status<br/>from ReportGenerator]
    S --> T[Return Status Dictionary]
    
    H --> U[Create MissionCommand<br/>with timestamp]
    U --> V[Add to Command Queue]
    V --> W[Call process_commands]
    
    L --> X[End]
    O --> X
    R --> X
    T --> X
    W --> X

    style A fill:#e1f5fe
    style X fill:#e8f5e8
    style N fill:#ffeb3b
    style E fill:#e3f2fd
    style F fill:#e3f2fd
    style G fill:#e3f2fd
    style H fill:#e3f2fd
    style Q fill:#f3e5f5
```

## Class: MissionController
**Purpose**: Main orchestrator for mission planning and execution

### Key Components
- **SystemInitializer**: Sets up flight simulation and mission planner
- **MissionExecutor**: Handles mission execution and monitoring
- **FlightAnalyzer**: Calculates flight performance parameters
- **ReportGenerator**: Creates mission reports and status updates

### Main Operations
1. **create_mission**: Define mission segments and parameters
2. **execute_mission**: Run mission through planner execution engine
3. **monitor_mission**: Track real-time mission status
4. **send_command**: Issue control commands (pause/resume/abort)

### Integration Points
- Flight simulation system for performance calculations
- Mission planner for segment execution
- Command queue for real-time control