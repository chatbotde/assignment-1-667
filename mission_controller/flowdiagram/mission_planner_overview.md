# Mission Planner System Overview

```mermaid
flowchart TB
    subgraph "Mission Controller Layer"
        A[MissionInterface<br/>High-level API] --> B[MissionController<br/>Main Orchestrator]
        B --> C[MissionExecutor<br/>Execution Engine]
        B --> D[FlightAnalyzer<br/>Performance Calculator]
        B --> E[FeasibilityAnalyzer<br/>Mission Validator]
        B --> F[SystemInitializer<br/>System Setup]
    end
    
    subgraph "Mission Definition Layer"
        G[MissionTypes<br/>Predefined Missions] --> H[Mission Validation<br/>Segment Checking]
        I[Mission Configuration<br/>JSON/Dict Format]
    end
    
    subgraph "Mission Execution Layer"
        J[planner_main<br/>Mission Runner] --> K[Segment Execution<br/>Individual Segments]
        K --> L[run_hover<br/>Stationary Flight]
        K --> M[run_vertical_climb<br/>Climb/Descent]
        K --> N[run_forward_climb<br/>Climbing Forward Flight]
        K --> O[run_cruise<br/>Level Forward Flight]
        K --> P[run_loiter<br/>Slow Forward Flight]
        K --> Q[run_payload_op<br/>Mass Change Operations]
    end
    
    subgraph "Vehicle Models Layer"
        R[Helicopter Model<br/>Mass, Aerodynamics] --> S[Engine Model<br/>Power, Fuel Consumption]
        T[Rotor Model<br/>Performance Integration]
    end
    
    subgraph "Flight Simulation Integration"
        U[Flight Sim Part 1<br/>Rotor Performance] --> V[Atmospheric Model<br/>ISA Properties]
        U --> W[Cycle Integrator<br/>Thrust/Power Calculation]
    end
    
    subgraph "Utilities & Support"
        X[planner_utils<br/>RPM Solver, Power Calculations] --> Y[Power Components<br/>Main, Tail, Parasite, Climb]
        Z[Mission Logging<br/>JSON Output]
    end
    
    %% Connections between layers
    A --> G
    C --> J
    D --> U
    K --> R
    K --> X
    J --> Z
    L --> R
    M --> R
    N --> R
    O --> R
    P --> R
    Q --> R
    
    %% Styling
    style A fill:#e3f2fd
    style B fill:#e1f5fe
    style C fill:#f3e5f5
    style J fill:#f3e5f5
    style K fill:#fff3e0
    style R fill:#e8f5e8
    style S fill:#e8f5e8
    style U fill:#ffeb3b
```

## Mission Planner System Architecture

### System Layers

#### 1. Mission Controller Layer
**Purpose**: High-level mission management and system integration
- **MissionInterface**: User-friendly API for mission operations
- **MissionController**: Central orchestrator coordinating all components
- **MissionExecutor**: Handles mission execution and real-time control
- **FlightAnalyzer**: Calculates flight performance parameters
- **FeasibilityAnalyzer**: Validates mission feasibility
- **SystemInitializer**: Sets up and validates system integration

#### 2. Mission Definition Layer
**Purpose**: Mission configuration and validation
- **MissionTypes**: Predefined mission templates (test, patrol, SAR, cargo)
- **Mission Validation**: Segment structure and parameter checking
- **Configuration Format**: JSON-based mission definitions

#### 3. Mission Execution Layer
**Purpose**: Execute individual mission segments
- **planner_main**: Main mission execution coordinator
- **Segment Functions**: Specialized execution for each flight phase
  - Hover, vertical climb, forward climb, cruise, loiter, payload operations
- **Time-stepped Simulation**: 1-second intervals with continuous monitoring

#### 4. Vehicle Models Layer
**Purpose**: Aircraft and propulsion system modeling
- **Helicopter Model**: Mass properties, aerodynamics, configuration
- **Engine Model**: Power availability, fuel consumption, altitude effects
- **Rotor Model**: Integration with flight simulation performance

#### 5. Flight Simulation Integration
**Purpose**: High-fidelity rotor performance calculations
- **Flight Sim Part 1**: Detailed rotor aerodynamics and performance
- **Atmospheric Model**: ISA standard atmosphere properties
- **Cycle Integrator**: Thrust and power calculations

#### 6. Utilities & Support
**Purpose**: Supporting calculations and data management
- **planner_utils**: RPM solving, power component calculations
- **Mission Logging**: Comprehensive JSON-based mission records
- **Power Components**: Main rotor, tail rotor, parasite, climb power

### Key Features
- **Modular Architecture**: Clear separation of concerns
- **Real-time Control**: Command queue for mission control
- **Comprehensive Logging**: Detailed mission performance records
- **Feasibility Analysis**: Pre-flight mission validation
- **Integration**: Seamless connection between mission planning and flight simulation