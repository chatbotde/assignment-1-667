# Mission Executor Flow Diagram

```mermaid
flowchart TD
    A[Start: MissionExecutor] --> B[Initialize<br/>mission_status=None<br/>mission_log=[]<br/>command_queue=[]]
    
    B --> C[create_mission]
    B --> D[execute_mission]
    B --> E[send_command]
    B --> F[process_commands]
    
    C --> G[Generate mission_id<br/>timestamp-based]
    G --> H[Create MissionStatus<br/>status='planning'<br/>segments, fuel, position]
    H --> I[Log Mission Creation]
    I --> J[Return mission_id]
    
    D --> K{Mission Exists?}
    K -->|No| L[Print Error<br/>Return False]
    K -->|Yes| M[Set status='executing'<br/>is_running=True]
    M --> N[Call run_mission from planner_main]
    N --> O{Execution Success?}
    O -->|Yes| P[Set status='completed']
    O -->|No| Q[Set status='failed']
    P --> R[Update timestamp]
    Q --> R
    R --> S[Set is_running=False]
    
    E --> T[Create MissionCommand<br/>with timestamp]
    T --> U[Add to command_queue]
    U --> V[Log Command Queued]
    
    F --> W[Command Queue Loop]
    W --> X{Commands Available?}
    X -->|No| Y[End Loop]
    X -->|Yes| Z[Pop Command]
    Z --> AA[execute_command]
    AA --> AB{Command Type?}
    AB -->|pause| AC[Set status='paused'<br/>is_running=False]
    AB -->|resume| AD[Set status='executing'<br/>is_running=True]
    AB -->|abort| AE[Set status='failed'<br/>is_running=False]
    AB -->|modify| AF[Handle Modifications]
    AC --> W
    AD --> W
    AE --> W
    AF --> W
    
    J --> AG[End]
    L --> AG
    S --> AG
    V --> AG
    Y --> AG

    style A fill:#e1f5fe
    style AG fill:#e8f5e8
    style K fill:#ffeb3b
    style O fill:#ffeb3b
    style X fill:#ffeb3b
    style AB fill:#ffeb3b
    style N fill:#f3e5f5
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style F fill:#e3f2fd
```

## Class: MissionExecutor
**Purpose**: Execute missions and handle real-time command processing

### Key Features
- **Mission Lifecycle**: Planning → Executing → Completed/Failed
- **Command Queue**: Real-time command processing
- **Status Tracking**: Continuous mission monitoring
- **Integration**: Direct interface with mission planner execution

### Command Types
- **pause**: Suspend mission execution
- **resume**: Continue paused mission
- **abort**: Terminate mission immediately
- **modify**: Update mission parameters

### Execution Flow
1. Validate mission configuration
2. Initialize execution environment
3. Call mission planner run_mission()
4. Monitor and log progress
5. Handle completion or failure