# Report Generator Flow Diagram

```mermaid
flowchart TD
    A[Start: ReportGenerator] --> B[Report Generation Methods]
    
    B --> C[generate_design_json Method]
    B --> D[generate_design_summary Method]
    B --> E[generate_performance_report Method]
    
    C --> F[Input: design_data, output_dir]
    F --> G[Write JSON File<br/>compound_helicopter_design.json]
    G --> H[Format: Indented JSON (indent=2)<br/>Complete design specification]
    
    D --> I[Input: helicopter_design, design_data, output_dir]
    I --> J[Extract Design Components<br/>main_rotor, tail_rotor, pusher_prop<br/>wings, mass_breakdown, dimensions<br/>requirements]
    
    J --> K[Build Summary Header<br/>Title, timestamp, design concept]
    K --> L[Design Concept Section<br/>Concept: "Compound Helicopter with Pusher Propeller"<br/>Configuration: Components description<br/>Philosophy: Design optimization approach]
    
    L --> M[Rotor Specifications Section]
    M --> N[Main Rotor Details<br/>Role, radius, RPM, blades<br/>chord distribution, twist, airfoil]
    M --> O[Tail Rotor Details<br/>Role, radius, RPM, blades<br/>chord distribution, power fraction]
    M --> P[Pusher Propeller Details<br/>Role, radius, RPM, blades<br/>blade design parameters]
    
    N --> Q[Aircraft Specifications Section]
    O --> Q
    P --> Q
    Q --> R[Dimensions Subsection<br/>Length, height, rotor diameters]
    Q --> S[Mass Breakdown Subsection<br/>Empty weight, operating empty<br/>max takeoff, payload, fuel]
    
    R --> T[Performance Requirements Section]
    S --> T
    T --> U[Requirements Checklist<br/>✓ Max takeoff altitude: {altitude}m<br/>✓ Top speed: {speed} km/h<br/>✓ Service ceiling: {ceiling}m<br/>✓ Range: {range} km<br/>✓ Payload: {persons} persons]
    
    U --> V[Design Features Section<br/>• Compound configuration benefits<br/>• Component optimization<br/>• Multi-mission capability]
    
    V --> W[Files Generated Section<br/>List of all output files with descriptions]
    
    W --> X[Write Summary File<br/>design_summary.txt, UTF-8 encoding]
    X --> Y[Return Summary String]
    
    E --> Z[Input: performance_data, output_dir]
    Z --> AA[Extract Performance Data<br/>hover_sl, hover_3500m, forward_180kmh<br/>disk_loading, tip_speed]
    
    AA --> BB[Build Performance Report Header<br/>Title, timestamp]
    BB --> CC[Hover Performance Section<br/>Sea Level: thrust, power<br/>High Altitude (3500m): thrust, power]
    
    CC --> DD[Forward Flight Performance Section<br/>At 180 km/h: thrust, power]
    
    DD --> EE[Rotor Characteristics Section<br/>Disk loading, tip speed]
    
    EE --> FF[Write Performance Report<br/>performance_report.txt, UTF-8 encoding]
    FF --> GG[Return Performance Report String]
    
    H --> HH[End]
    Y --> HH
    GG --> HH

    style A fill:#e1f5fe
    style HH fill:#e8f5e8
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style G fill:#fff3e0
    style J fill:#fff3e0
    style K fill:#fff3e0
    style M fill:#fff3e0
    style Q fill:#fff3e0
    style T fill:#fff3e0
    style AA fill:#fff3e0
    style BB fill:#fff3e0
    style L fill:#f3e5f5
    style N fill:#ffcdd2
    style O fill:#ffcdd2
    style P fill:#ffcdd2
    style R fill:#c8e6c9
    style S fill:#c8e6c9
    style U fill:#bbdefb
    style V fill:#fff9c4
    style W fill:#e1bee7
    style CC fill:#ffcdd2
    style DD fill:#c8e6c9
    style EE fill:#bbdefb
```

## Report Generator Component
**Purpose**: Generate comprehensive documentation for helicopter design

### JSON Design Specification
**generate_design_json Method**:

#### Complete Design Data Export
- **File**: compound_helicopter_design.json
- **Format**: Indented JSON (2 spaces) for readability
- **Content**: Complete design specification including:
  - All rotor configurations
  - Aircraft sizing data
  - Performance analysis results
  - Design requirements

#### Machine-Readable Format
- **Purpose**: Data exchange and further analysis
- **Structure**: Hierarchical organization of design data
- **Accessibility**: Standard JSON format for tool integration

### Comprehensive Design Summary
**generate_design_summary Method**:

#### Multi-Section Report Structure

##### 1. Design Concept Section
- **Concept**: "Compound Helicopter with Pusher Propeller"
- **Configuration**: Component layout description
- **Philosophy**: "Optimized for high-speed cruise with rotor unloading"

##### 2. Rotor Specifications Section
**Main Rotor Details**:
- Role and optimization purpose
- Geometric parameters (radius, blades, chord, twist)
- Operating conditions (RPM, airfoil)
- Performance characteristics

**Tail Rotor Details**:
- Anti-torque role and control authority
- Sizing relative to main rotor
- Power fraction and operating parameters

**Pusher Propeller Details**:
- High-speed thrust generation role
- Propeller-specific design parameters
- Integration with compound configuration

##### 3. Aircraft Specifications Section
**Dimensions**:
- Overall aircraft envelope
- Major component dimensions
- Integration considerations

**Mass Breakdown**:
- Empty weight progression
- Payload and fuel capacity
- Maximum takeoff weight

##### 4. Performance Requirements Section
**Requirements Traceability**:
- ✓ Max takeoff altitude: 3500m
- ✓ Top speed: 400 km/h
- ✓ Service ceiling: 5000m
- ✓ Range: 500 km
- ✓ Payload: 10 persons

##### 5. Design Features Section
**Key Innovations**:
- Compound configuration benefits
- Component optimization strategies
- Multi-mission capability
- Advanced technology integration

##### 6. Files Generated Section
**Output Documentation**:
- Complete list of generated files
- Description of each file's purpose
- Cross-reference for design package

### Performance Analysis Report
**generate_performance_report Method**:

#### Detailed Performance Documentation

##### Hover Performance Analysis
- **Sea Level**: Baseline performance capability
- **High Altitude (3500m)**: Performance degradation analysis
- **Metrics**: Thrust and power at each condition

##### Forward Flight Performance
- **Cruise Condition**: 180 km/h performance
- **Efficiency**: Power requirements for forward flight
- **Comparison**: Hover vs forward flight characteristics

##### Rotor Characteristics
- **Disk Loading**: Rotor loading metric (N/m²)
- **Tip Speed**: Compressibility considerations (m/s)
- **Design Validation**: Performance against limits

### Report Formatting Standards

#### Professional Documentation
- **Headers**: Clear section delineation
- **Timestamps**: Generation date and time
- **Units**: Consistent engineering units
- **Formatting**: Clean, readable layout

#### File Management
- **Encoding**: UTF-8 for international compatibility
- **Extensions**: .txt for universal readability
- **Organization**: Logical file naming convention

### Integration Features

#### Data Extraction
- **Flexible Input**: Handles various data structures
- **Error Handling**: Graceful handling of missing data
- **Validation**: Ensures data completeness

#### Cross-References
- **File Linking**: References between related files
- **Data Consistency**: Synchronized information across reports
- **Version Control**: Timestamp-based versioning

### Key Features
- **Comprehensive Coverage**: All aspects of design documented
- **Multiple Formats**: JSON (machine) + TXT (human) readable
- **Professional Quality**: Publication-ready documentation
- **Traceability**: Requirements linked to design decisions
- **Completeness**: Full design package documentation

### Output Products
- **compound_helicopter_design.json**: Complete machine-readable specification
- **design_summary.txt**: Human-readable design overview
- **performance_report.txt**: Detailed performance analysis
- **Cross-Referenced**: All files reference each other appropriately