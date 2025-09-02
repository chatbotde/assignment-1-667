# Helicopter Designer Main Flow Diagram

```mermaid
flowchart TD
    A[Start: CompoundHelicopterDesigner] --> B[Initialize Components<br/>DesignRequirements, RotorDesigner<br/>AircraftSizer, PerformanceAnalyzer<br/>PlotGenerator, ReportGenerator]
    
    B --> C[create_output_directory<br/>Create "individual_design" folder]
    C --> D[design_compound_helicopter Method]
    
    D --> E[Define Design Philosophy<br/>Concept: "Compound Helicopter with Pusher Propeller"<br/>Configuration: "Single main rotor + tail rotor + pusher propeller + wings"<br/>Philosophy: "Optimized for high-speed cruise with rotor unloading"]
    
    E --> F[Design All Components]
    F --> G[Design Main Rotor<br/>rotor_designer.design_main_rotor()]
    F --> H[Design Tail Rotor<br/>rotor_designer.design_tail_rotor()]
    F --> I[Design Pusher Propeller<br/>rotor_designer.design_pusher_propeller()]
    F --> J[Design Wings<br/>rotor_designer.design_wings()]
    
    G --> K[Size Aircraft<br/>aircraft_sizer.size_aircraft()]
    H --> K
    I --> K
    J --> K
    
    K --> L[Calculate Mass Breakdown<br/>payload, crew, fuel, components<br/>empty weight, max takeoff weight]
    L --> M[Calculate Dimensions<br/>length, height, width<br/>rotor diameters]
    
    M --> N[generate_performance_plots Method]
    N --> O[Set Plot Output Directory<br/>plot_generator.set_output_dir()]
    O --> P[Generate Performance Plots]
    P --> Q[Rotor Performance Comparison<br/>plot_rotor_performance_comparison()]
    P --> R[Thrust vs Collective<br/>plot_thrust_vs_collective()]
    P --> S[Power vs Collective<br/>plot_power_vs_collective()]
    P --> T[Thrust vs Power<br/>plot_thrust_vs_power()]
    
    Q --> U[analyze_hover_mission Method]
    R --> U
    S --> U
    T --> U
    
    U --> V[Analyze Hover at 2000m<br/>performance_analyzer.analyze_hover_mission()]
    V --> W[Save Hover Results<br/>hover_analysis.json]
    W --> X[Generate Hover Plots<br/>plot_generator.plot_hover_mission_analysis()]
    
    X --> Y[generate_design_summary Method]
    Y --> Z[Analyze Main Rotor Performance<br/>performance_analyzer.analyze_main_rotor_performance()]
    Z --> AA[Create Design Data Dictionary<br/>main_rotor, tail_rotor, pusher_propeller<br/>wings, mass_breakdown, dimensions<br/>performance, requirements]
    
    AA --> BB[Generate Design JSON<br/>report_generator.generate_design_json()]
    BB --> CC[Generate Design Summary<br/>report_generator.generate_design_summary()]
    CC --> DD[Print Summary and Completion Message]
    
    DD --> EE[End]

    style A fill:#e1f5fe
    style EE fill:#e8f5e8
    style D fill:#e3f2fd
    style N fill:#e3f2fd
    style U fill:#e3f2fd
    style Y fill:#e3f2fd
    style E fill:#fff3e0
    style F fill:#fff3e0
    style K fill:#fff3e0
    style P fill:#fff3e0
    style V fill:#f3e5f5
    style Z fill:#f3e5f5
    style AA fill:#f3e5f5
```

## Helicopter Designer Main Class
**Purpose**: Central coordinator for compound helicopter design process

### Initialization Process
1. **Component Setup**: Initialize all design modules
   - DesignRequirements: Mission and performance requirements
   - RotorDesigner: Main rotor, tail rotor, pusher prop, wings
   - AircraftSizer: Mass breakdown and overall sizing
   - PerformanceAnalyzer: Flight performance calculations
   - PlotGenerator: Visualization and plotting
   - ReportGenerator: Documentation and summaries

2. **Output Management**: Create organized output directory structure

### Design Process Flow

#### 1. Component Design Phase
**design_compound_helicopter Method**:
- **Design Philosophy**: Compound helicopter optimized for high-speed cruise
- **Main Rotor**: 8.5m radius, 4 blades, optimized for hover efficiency
- **Tail Rotor**: 1.8m radius, 4 blades, anti-torque control
- **Pusher Propeller**: 1.5m radius, 3 blades, high-speed forward thrust
- **Wings**: 12m span, 21.6m² area, rotor unloading at high speed

#### 2. Aircraft Sizing Phase
**Mass and Dimension Calculation**:
- **Mass Breakdown**: Component masses, fuel, payload, empty weight
- **Dimensions**: Overall aircraft envelope and component positioning
- **Integration**: Ensure all components fit within design constraints

#### 3. Performance Analysis Phase
**generate_performance_plots Method**:
- **Comparative Analysis**: All rotors on same plots
- **Individual Characteristics**: Thrust, power, efficiency curves
- **Design Validation**: Performance against requirements

#### 4. Mission Analysis Phase
**analyze_hover_mission Method**:
- **High Altitude Performance**: 2000m hover capability
- **Weight Limits**: Maximum weight for thrust and power
- **Endurance Analysis**: Fuel consumption and hover time

#### 5. Documentation Phase
**generate_design_summary Method**:
- **Performance Data**: Detailed rotor performance analysis
- **Design Documentation**: Complete JSON specification
- **Summary Report**: Human-readable design overview

### Key Features
- **Modular Architecture**: Clean separation of design disciplines
- **Comprehensive Analysis**: Performance, mission, and design validation
- **Professional Documentation**: JSON data + human-readable summaries
- **Visual Analysis**: Multiple performance plots and comparisons
- **Requirements Traceability**: Design linked to original requirements

### Output Products
- **compound_helicopter_design.json**: Complete design specification
- **design_summary.txt**: Human-readable design overview
- **hover_analysis.json**: Mission performance data
- **Performance Plots**: 5 different visualization plots
- **Mission Analysis**: Hover capability and endurance plots

### Integration Points
- **Flight Simulation**: Uses flight_sim_part1 for rotor performance
- **Design Modules**: Coordinates all specialized design components
- **File Management**: Organized output structure for design documentation