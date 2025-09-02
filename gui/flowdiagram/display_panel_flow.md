# Display Panel Flow Diagram

```mermaid
flowchart TD
    A[Start: DisplayPanel] --> B[Initialize<br/>parent, main_app reference]
    B --> C[create_display_panel Method]
    
    C --> D[Create Main Display Frame<br/>LabelFrame: "Forces & Moments (Aircraft Reference Frame)"]
    
    D --> E[Create Forces Section<br/>LabelFrame: "Forces [N]"]
    E --> F[Create Force Display Labels]
    F --> G[Fx Label<br/>Color: #e74c3c (Red)<br/>Width: 12, Bold font]
    F --> H[Fy Label<br/>Color: #2ecc71 (Green)<br/>Width: 12, Bold font]
    F --> I[Fz Label<br/>Color: #3498db (Blue)<br/>Width: 12, Bold font]
    
    G --> J[Store in force_labels Dictionary<br/>self.force_labels['Fx'] = label]
    H --> J
    I --> J
    
    J --> K[Create Moments Section<br/>LabelFrame: "Moments [N⋅m]"]
    K --> L[Create Moment Display Labels]
    L --> M[Mx Label<br/>Color: #9b59b6 (Purple)<br/>Width: 12, Bold font]
    L --> N[My Label<br/>Color: #f39c12 (Orange)<br/>Width: 12, Bold font]
    L --> O[Mz Label<br/>Color: #1abc9c (Teal)<br/>Width: 12, Bold font]
    
    M --> P[Store in force_labels Dictionary<br/>self.force_labels['Mx'] = label]
    N --> P
    O --> P
    
    P --> Q[Create Performance Section<br/>LabelFrame: "Performance"]
    Q --> R[Create Performance Labels]
    R --> S[Thrust Label<br/>Color: #e67e22 (Orange)<br/>Unit: N, Width: 12]
    R --> T[Power Label<br/>Color: #8e44ad (Purple)<br/>Unit: kW, Width: 12]
    
    S --> U[Store in perf_labels Dictionary<br/>self.perf_labels['Thrust'] = label]
    T --> U
    
    U --> V[update Method]
    V --> W[Input: forces_moments, performance dictionaries]
    W --> X[Update Force and Moment Labels Loop]
    X --> Y[For each key in force_labels<br/>Get value from forces_moments[key]]
    Y --> Z[Format Value<br/>"{value:.1f}"]
    Z --> AA[Update Label Text<br/>label.config(text=formatted_value)]
    
    AA --> BB[Update Performance Labels]
    BB --> CC[Update Thrust Label<br/>"{performance['thrust']:.1f} N"]
    CC --> DD[Update Power Label<br/>"{performance['power']:.1f} kW"]
    
    DD --> EE[End]

    style A fill:#e1f5fe
    style EE fill:#e8f5e8
    style C fill:#e3f2fd
    style V fill:#e3f2fd
    style E fill:#fff3e0
    style K fill:#fff3e0
    style Q fill:#fff3e0
    style G fill:#ffcdd2
    style H fill:#c8e6c9
    style I fill:#bbdefb
    style M fill:#e1bee7
    style N fill:#ffe0b2
    style O fill:#b2dfdb
    style S fill:#ffcc80
    style T fill:#d1c4e9
    style X fill:#f3e5f5
    style BB fill:#f3e5f5
```

## Display Panel Component
**Purpose**: Real-time display of helicopter forces, moments, and performance data

### Forces Section
**Aircraft Reference Frame Forces**:
- **Fx (Red)**: Longitudinal force (forward/backward)
- **Fy (Green)**: Lateral force (left/right)  
- **Fz (Blue)**: Vertical force (up/down)

**Display Format**:
- Units: Newtons [N]
- Precision: 1 decimal place
- Color-coded labels for easy identification

### Moments Section
**Aircraft Reference Frame Moments**:
- **Mx (Purple)**: Rolling moment (about longitudinal axis)
- **My (Orange)**: Pitching moment (about lateral axis)
- **Mz (Teal)**: Yawing moment (about vertical axis)

**Display Format**:
- Units: Newton-meters [N⋅m]
- Precision: 1 decimal place
- Color-coded labels matching force scheme

### Performance Section
**Key Performance Indicators**:
- **Thrust**: Total rotor thrust output (N)
- **Power**: Total power consumption (kW)

**Display Format**:
- Real-time updates with simulation
- Color-coded for visual distinction
- Engineering units for practical reference

### Update Process
**Real-time Data Flow**:
1. Receive forces_moments dictionary from simulation
2. Receive performance dictionary from simulation
3. Loop through all force/moment labels
4. Format values to 1 decimal place
5. Update label text with new values
6. Update performance indicators

### Visual Design
**Color Scheme**:
- **Forces**: Red, Green, Blue (RGB mapping)
- **Moments**: Purple, Orange, Teal (complementary colors)
- **Performance**: Orange and Purple variants
- **Background**: Dark theme (#34495e) for contrast

### Key Features
- **Real-time Updates**: 5 Hz refresh rate
- **Color Coding**: Intuitive visual organization
- **Engineering Units**: Standard aerospace notation
- **Compact Layout**: Efficient use of screen space
- **Bold Typography**: High visibility for critical data

### Integration Points
- **Simulation Engine**: Receives calculated forces and moments
- **Main GUI Loop**: Updated every 200ms cycle
- **Aircraft Reference Frame**: Standard aerospace coordinate system