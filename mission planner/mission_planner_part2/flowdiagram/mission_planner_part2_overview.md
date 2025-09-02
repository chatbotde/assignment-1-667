# Mission Planner Part 2 System Overview

```mermaid
flowchart TB
    subgraph "Mission Planner Part 2 Core"
        A[planner_main.py<br/>Mission Execution Coordinator] --> B[segments.py<br/>Individual Segment Execution]
        C[mp_inputs.py<br/>Configuration & Mission Definition] --> A
        D[planner_utils.py<br/>Utility Functions & Solvers] --> B
    end
    
    subgraph "Vehicle & Propulsion Models"
        E[vehicle.py<br/>Helicopter Model] --> F[Mass Properties<br/>OEW, Payload, Fuel]
        E --> G[Aerodynamic Properties<br/>Reference Area, Drag]
        H[engine.py<br/>Engine Model] --> I[Power Available<br/>Altitude Derate]
        H --> J[Fuel Consumption<br/>SFC Model]
    end
    
    subgraph "Mission Segment Types"
        B --> K[run_hover<br/>Stationary Flight]
        B --> L[run_vertical_climb<br/>Pure Vertical Motion]
        B --> M[run_forward_climb<br/>Climbing Forward Flight]
        B --> N[run_cruise<br/>Level Forward Flight]
        B --> O[run_loiter<br/>Slow Forward Flight]
        B --> P[run_payload_op<br/>Mass Change Operations]
    end
    
    subgraph "Power Calculation Components"
        D --> Q[solve_rpm_for_thrust<br/>RPM Optimization]
        D --> R[parasite_power<br/>Fuselage Drag Power]
        D --> S[tail_power_fraction<br/>Anti-torque Power]
        D --> T[tip_mach<br/>Rotor Speed Limits]
    end
    
    subgraph "Flight Simulation Integration"
        U[imports.py<br/>Path Management] --> V[Flight Sim Part 1<br/>Integration Layer]
        V --> W[cycle_integrator<br/>Rotor Performance]
        V --> X[atmosphere<br/>ISA Properties]
        V --> Y[user_inputs<br/>Rotor Configuration]
    end
    
    subgraph "Mission Configuration"
        C --> Z[get_helicopter_and_engine<br/>System Setup]
        C --> AA[mission_definition<br/>7-Segment Mission]
        Z --> BB[Helicopter: 2500kg OEW<br/>300kg Payload, 400kg Fuel]
        Z --> CC[Engine: 1500kW<br/>0.32 kg/kWh SFC]
        AA --> DD[Hover → Climb → Cruise<br/>→ Payload → Loiter → Climb → Cruise]
    end
    
    subgraph "Execution Flow"
        A --> EE[Mission Loop<br/>Sequential Segment Execution]
        EE --> FF[Segment Dispatch<br/>Type-based Function Call]
        FF --> GG[Power Calculation<br/>Main + Tail + Parasite + Climb]
        GG --> HH[Feasibility Check<br/>Power Available vs Required]
        HH --> II[Fuel Consumption<br/>Update Remaining Fuel]
        II --> JJ[Data Logging<br/>Performance Recording]
    end
    
    %% Connections between major components
    K --> E
    L --> E
    M --> E
    N --> E
    O --> E
    P --> E
    
    K --> H
    L --> H
    M --> H
    N --> H
    O --> H
    
    Q --> W
    R --> E
    S --> E
    
    A --> U
    D --> U
    
    %% Styling
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e3f2fd
    style D fill:#fff3e0
    style E fill:#e8f5e8
    style H fill:#e8f5e8
    style U fill:#ffeb3b
    style V fill:#ffeb3b
```

## Mission Planner Part 2 Architecture

### Core Components

#### 1. Mission Execution Layer
- **planner_main.py**: Central mission coordinator
  - Loads helicopter, engine, and mission configuration
  - Executes segments sequentially with altitude tracking
  - Handles success/failure and comprehensive logging

- **segments.py**: Individual segment execution functions
  - Time-stepped simulation (1-second intervals)
  - Power calculations for each flight phase
  - Fuel consumption and feasibility checking

#### 2. Configuration Layer
- **mp_inputs.py**: System configuration and mission definition
  - Helicopter: 3200kg total mass (2500+300+400)
  - Engine: 1500kW with realistic fuel consumption
  - 7-segment mission profile for comprehensive testing

#### 3. Utility Layer
- **planner_utils.py**: Mathematical solvers and calculations
  - RPM optimization using bisection method
  - Power component calculations (parasite, tail)
  - Tip Mach number limiting for safety

#### 4. Vehicle Models
- **vehicle.py**: Helicopter mass and aerodynamic properties
- **engine.py**: Power availability and fuel consumption models

#### 5. Integration Layer
- **imports.py**: Dynamic path management for flight simulation integration
- Seamless connection to flight_sim_part1 components

### Mission Execution Flow

#### Sequential Process
1. **System Initialization**: Load helicopter, engine, rotor models
2. **Mission Loading**: Get predefined 7-segment mission
3. **Segment Loop**: Execute each segment with type dispatch
4. **Power Calculation**: Main rotor + tail + parasite + climb power
5. **Feasibility Check**: Verify power available vs required
6. **Fuel Update**: Calculate and subtract fuel consumption
7. **Data Logging**: Record comprehensive performance data
8. **Altitude Tracking**: Maintain current altitude for next segment

#### Power Components
- **Main Rotor**: From flight simulation cycle integrator
- **Tail Rotor**: Anti-torque power (7% hover → 1.5% cruise)
- **Parasite**: Fuselage drag power (0.5×ρ×V²×S×CD0×V)
- **Climb**: Gravitational power (Weight × climb_rate)

### Key Features
- **High Fidelity**: Integration with detailed flight simulation
- **Realistic Modeling**: Comprehensive power and fuel calculations
- **Robust Solving**: Bisection method for RPM optimization
- **Safety Limits**: Tip Mach number constraints
- **Comprehensive Logging**: Detailed mission performance records
- **Modular Design**: Clear separation of concerns and reusable components

### Mission Profile
**7-Segment Test Mission**:
1. Ground hover (60s) - System checkout
2. Vertical climb (120s to 360m) - Initial ascent
3. Cruise (300s at 45 m/s) - Transit to area
4. Payload drop (100kg with hover) - Mission task
5. Loiter (120s at 25 m/s) - Surveillance/patrol
6. Forward climb (60s to 420m) - Altitude change
7. Return cruise (240s at 50 m/s) - Return transit