# Plot Generator Flow Diagram

```mermaid
flowchart TD
    A[Start: PlotGenerator] --> B[Initialize<br/>performance_analyzer, output_dir]
    B --> C[Plotting Methods]
    
    C --> D[plot_rotor_performance_comparison Method]
    C --> E[plot_thrust_vs_collective Method]
    C --> F[plot_power_vs_collective Method]
    C --> G[plot_thrust_vs_power Method]
    C --> H[plot_hover_mission_analysis Method]
    
    D --> I[Create 2×2 Subplot Figure<br/>15×12 inches]
    I --> J[Define Collective Pitch Range<br/>θ = 0° to 16° in 17 steps]
    J --> K[Calculate Main Rotor Performance<br/>performance_analyzer.calculate_rotor_performance()]
    K --> L[Calculate Tail Rotor Performance<br/>performance_analyzer.calculate_rotor_performance()]
    
    L --> M[Plot 1: Thrust vs Collective<br/>Main rotor (blue), Tail rotor ×5 (red)]
    M --> N[Plot 2: Power vs Collective<br/>Main rotor (blue), Tail rotor (red)]
    N --> O[Plot 3: Thrust vs Power<br/>Main rotor (blue), Tail rotor (red)]
    O --> P[Plot 4: Efficiency vs Collective<br/>Efficiency = Thrust/Power]
    
    P --> Q[Apply Formatting<br/>Labels, legends, grids, tight layout]
    Q --> R[Save Plot<br/>rotor_performance_comparison.png, 300 DPI]
    
    E --> S[Create Single Plot Figure<br/>10×6 inches]
    S --> T[Calculate Performance Data<br/>θ = 0° to 16°]
    T --> U[Plot Thrust Lines<br/>Main rotor (blue circles), Tail rotor (red squares)]
    U --> V[Format Plot<br/>Title: "Thrust vs Collective Pitch\nCompound Helicopter Rotors"]
    V --> W[Save Plot<br/>thrust_vs_collective.png, 300 DPI]
    
    F --> X[Create Single Plot Figure<br/>10×6 inches]
    X --> Y[Calculate Performance Data<br/>θ = 0° to 16°]
    Y --> Z[Plot Power Lines<br/>Main rotor (blue circles), Tail rotor (red squares)]
    Z --> AA[Format Plot<br/>Title: "Power vs Collective Pitch\nCompound Helicopter Rotors"]
    AA --> BB[Save Plot<br/>power_vs_collective.png, 300 DPI]
    
    G --> CC[Create Single Plot Figure<br/>10×6 inches]
    CC --> DD[Calculate Performance Data<br/>θ = 2° to 16° (skip low pitch)]
    DD --> EE[Plot Thrust vs Power<br/>Main rotor (blue circles), Tail rotor (red squares)]
    EE --> FF[Format Plot<br/>Title: "Thrust vs Power\nCompound Helicopter Rotors"]
    FF --> GG[Save Plot<br/>thrust_vs_power_individual.png, 300 DPI]
    
    H --> HH[Input: hover_results, output_dir]
    HH --> II[Extract Data<br/>weights, fuel_rates, endurances, altitude]
    II --> JJ[Create 1×2 Subplot Figure<br/>12×5 inches]
    
    JJ --> KK[Plot 1: Fuel Burn Rate vs Weight<br/>Blue line, 2px width]
    KK --> LL[Format: Title "Fuel Burn Rate vs Weight\nHover at {altitude}m AMSL"<br/>X-axis: "Gross Weight [kg]"<br/>Y-axis: "Fuel Burn Rate [kg/min]"]
    
    LL --> MM[Plot 2: Hover Endurance vs Weight<br/>Red line, 2px width]
    MM --> NN[Format: Title "Hover Endurance vs Weight\nAt {altitude}m AMSL"<br/>X-axis: "Take-Off Weight [kg]"<br/>Y-axis: "Hover Endurance [min]"]
    
    NN --> OO[Apply Formatting<br/>Grid, tight layout]
    OO --> PP[Save Plot<br/>hover_mission_analysis.png, 300 DPI]
    
    QQ[set_output_dir Method] --> RR[Update self.output_dir<br/>Set directory for plot output]
    
    R --> SS[End]
    W --> SS
    BB --> SS
    GG --> SS
    PP --> SS
    RR --> SS

    style A fill:#e1f5fe
    style SS fill:#e8f5e8
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style F fill:#e3f2fd
    style G fill:#e3f2fd
    style H fill:#e3f2fd
    style QQ fill:#e3f2fd
    style I fill:#fff3e0
    style J fill:#fff3e0
    style K fill:#f3e5f5
    style L fill:#f3e5f5
    style M fill:#ffcdd2
    style N fill:#c8e6c9
    style O fill:#bbdefb
    style P fill:#fff9c4
    style S fill:#fff3e0
    style X fill:#fff3e0
    style CC fill:#fff3e0
    style JJ fill:#fff3e0
    style U fill:#ffcdd2
    style Z fill:#c8e6c9
    style EE fill:#bbdefb
    style KK fill:#ffcdd2
    style MM fill:#ffcdd2
```

## Plot Generator Component
**Purpose**: Create comprehensive visualization plots for helicopter design analysis

### Comprehensive Performance Comparison
**plot_rotor_performance_comparison Method**:

#### Multi-Plot Layout
- **Figure Size**: 15×12 inches for detailed analysis
- **Subplot Grid**: 2×2 layout for comprehensive comparison
- **Data Range**: Collective pitch 0° to 16° in 17 steps

#### Individual Plots
1. **Thrust vs Collective**: Main rotor vs tail rotor (×5 scale)
2. **Power vs Collective**: Direct power comparison
3. **Thrust vs Power**: Efficiency relationship
4. **Efficiency vs Collective**: Thrust/power ratio analysis

#### Visual Design
- **Color Scheme**: Blue (main rotor), Red (tail rotor)
- **Markers**: Circles (main), Squares (tail)
- **Line Width**: 2px for visibility
- **Grid**: 30% transparency for reference

### Individual Performance Plots
**Specialized Single-Plot Analysis**:

#### Thrust vs Collective Plot
- **Focus**: Thrust generation characteristics
- **Comparison**: Main rotor vs tail rotor performance
- **Title**: "Thrust vs Collective Pitch\nCompound Helicopter Rotors"

#### Power vs Collective Plot
- **Focus**: Power consumption characteristics
- **Analysis**: Power requirements across operating range
- **Title**: "Power vs Collective Pitch\nCompound Helicopter Rotors"

#### Thrust vs Power Plot
- **Focus**: Efficiency analysis
- **Range**: 2° to 16° (excludes very low pitch)
- **Purpose**: Power loading and efficiency comparison

### Mission Analysis Visualization
**plot_hover_mission_analysis Method**:

#### Hover Performance Analysis
- **Input Data**: Weight range, fuel rates, endurances
- **Layout**: 1×2 subplot for dual analysis
- **Altitude**: Configurable altitude for analysis

#### Dual Plot Analysis
1. **Fuel Burn Rate vs Weight**:
   - Shows fuel consumption scaling with weight
   - Critical for mission planning
   - Units: kg/min vs kg

2. **Hover Endurance vs Weight**:
   - Shows mission duration capability
   - Weight-dependent endurance
   - Units: minutes vs kg

### Plot Formatting Standards

#### Professional Appearance
- **High Resolution**: 300 DPI for publication quality
- **Font Sizes**: 12pt labels, 14pt titles, 11pt legends
- **Grid Lines**: Subtle reference grid (alpha=0.3)
- **Tight Layout**: Optimal use of figure space

#### Consistent Styling
- **Color Scheme**: Blue/red for main/tail rotor consistency
- **Line Styles**: Solid lines with distinct markers
- **Titles**: Descriptive with subtitle for context
- **Axes Labels**: Engineering units with proper notation

### File Management
**Output Organization**:
- **Directory**: Configurable output directory
- **Naming**: Descriptive filenames for easy identification
- **Format**: PNG format for universal compatibility
- **Quality**: High DPI for professional presentation

### Integration Points
- **Performance Analyzer**: Data source for all calculations
- **Design Components**: Uses rotor specifications
- **File System**: Organized output structure
- **Professional Standards**: Publication-quality plots

### Key Features
- **Comprehensive Analysis**: Multiple plot types for complete picture
- **Comparative Visualization**: Main rotor vs tail rotor performance
- **Mission Relevance**: Hover analysis for operational planning
- **Professional Quality**: High-resolution, well-formatted plots
- **Modular Design**: Individual methods for specific plot types

### Output Products
- **rotor_performance_comparison.png**: 4-plot comprehensive analysis
- **thrust_vs_collective.png**: Thrust characteristics
- **power_vs_collective.png**: Power requirements
- **thrust_vs_power_individual.png**: Efficiency analysis
- **hover_mission_analysis.png**: Mission performance analysis