# Plot Panel Flow Diagram

```mermaid
flowchart TD
    A[Start: PlotPanel] --> B[Initialize<br/>parent, main_app reference]
    B --> C[create_plot_panel Method]
    
    C --> D[Create Plot Frame<br/>LabelFrame: "Real-Time Forces & Moments"]
    D --> E[Create Matplotlib Figure<br/>Size: 8x6, DPI: 80, Background: #ecf0f1]
    
    E --> F[Create Subplots]
    F --> G[Upper Subplot (ax1)<br/>Forces Plot: Fx, Fy, Fz]
    F --> H[Lower Subplot (ax2)<br/>Moments Plot: Mx, My, Mz]
    
    G --> I[Configure Forces Plot<br/>Title: "Forces (Fx, Fy, Fz)"<br/>Y-label: "Force [N]"<br/>Grid: True, Alpha: 0.3]
    
    H --> J[Configure Moments Plot<br/>Title: "Moments (Mx, My, Mz)"<br/>X-label: "Time [s]", Y-label: "Moment [N⋅m]"<br/>Grid: True, Alpha: 0.3]
    
    I --> K[Initialize Force Plot Lines]
    K --> L[Fx Line: Color #e74c3c (Red), Width: 2]
    K --> M[Fy Line: Color #2ecc71 (Green), Width: 2]
    K --> N[Fz Line: Color #3498db (Blue), Width: 2]
    
    J --> O[Initialize Moment Plot Lines]
    O --> P[Mx Line: Color #9b59b6 (Purple), Width: 2]
    O --> Q[My Line: Color #f39c12 (Orange), Width: 2]
    O --> R[Mz Line: Color #1abc9c (Teal), Width: 2]
    
    L --> S[Store in force_lines List<br/>self.force_lines.append(line)]
    M --> S
    N --> S
    
    P --> T[Store in moment_lines List<br/>self.moment_lines.append(line)]
    Q --> T
    R --> T
    
    S --> U[Add Legends<br/>ax1.legend(loc='upper right')<br/>ax2.legend(loc='upper right')]
    T --> U
    
    U --> V[Apply Tight Layout<br/>self.fig.tight_layout()]
    V --> W[Embed in Tkinter<br/>FigureCanvasTkAgg(self.fig, plot_frame)]
    W --> X[Pack Canvas Widget<br/>fill=BOTH, expand=True]
    
    X --> Y[update Method]
    Y --> Z[Input: time_data, force_history]
    Z --> AA{len(time_data) > 1?}
    AA -->|No| BB[Skip Update]
    AA -->|Yes| CC[Update Force Lines Loop]
    
    CC --> DD[For each force key (Fx, Fy, Fz)<br/>Get data: force_history[key]]
    DD --> EE[Update Line Data<br/>force_lines[i].set_data(time_data, data)]
    
    EE --> FF[Update Moment Lines Loop]
    FF --> GG[For each moment key (Mx, My, Mz)<br/>Get data: force_history[key]]
    GG --> HH[Update Line Data<br/>moment_lines[i].set_data(time_data, data)]
    
    HH --> II{len(time_data) > 2?}
    II -->|No| JJ[Skip Rescaling]
    II -->|Yes| KK[Rescale Axes<br/>ax1.relim(), ax1.autoscale_view()<br/>ax2.relim(), ax2.autoscale_view()]
    
    JJ --> LL[Redraw Canvas<br/>self.canvas.draw_idle()]
    KK --> LL
    LL --> MM{Drawing Success?}
    MM -->|No| NN[Ignore Drawing Errors<br/>pass]
    MM -->|Yes| OO[Update Complete]
    
    BB --> PP[End]
    NN --> PP
    OO --> PP

    style A fill:#e1f5fe
    style PP fill:#e8f5e8
    style AA fill:#ffeb3b
    style II fill:#ffeb3b
    style MM fill:#ffeb3b
    style C fill:#e3f2fd
    style Y fill:#e3f2fd
    style E fill:#fff3e0
    style F fill:#fff3e0
    style K fill:#fff3e0
    style O fill:#fff3e0
    style L fill:#ffcdd2
    style M fill:#c8e6c9
    style N fill:#bbdefb
    style P fill:#e1bee7
    style Q fill:#ffe0b2
    style R fill:#b2dfdb
    style CC fill:#f3e5f5
    style FF fill:#f3e5f5
    style LL fill:#ffeb3b
```

## Plot Panel Component
**Purpose**: Real-time visualization of helicopter forces and moments over time

### Matplotlib Integration
**Figure Setup**:
- **Size**: 8x6 inches at 80 DPI
- **Background**: Light gray (#ecf0f1) for contrast
- **Subplots**: Two vertically stacked plots
- **Embedding**: FigureCanvasTkAgg for Tkinter integration

### Plot Configuration
#### Upper Plot (Forces)
- **Title**: "Forces (Fx, Fy, Fz)"
- **Y-axis**: Force [N]
- **Lines**: Red (Fx), Green (Fy), Blue (Fz)
- **Grid**: Enabled with 30% transparency

#### Lower Plot (Moments)
- **Title**: "Moments (Mx, My, Mz)"
- **X-axis**: Time [s]
- **Y-axis**: Moment [N⋅m]
- **Lines**: Purple (Mx), Orange (My), Teal (Mz)
- **Grid**: Enabled with 30% transparency

### Line Initialization
**Force Lines**:
- **Fx**: Red (#e74c3c), 2px width
- **Fy**: Green (#2ecc71), 2px width
- **Fz**: Blue (#3498db), 2px width

**Moment Lines**:
- **Mx**: Purple (#9b59b6), 2px width
- **My**: Orange (#f39c12), 2px width
- **Mz**: Teal (#1abc9c), 2px width

### Real-time Update Process
**Update Method Flow**:
1. **Data Validation**: Check if sufficient data points exist
2. **Force Line Updates**: Update each force line with new time/data
3. **Moment Line Updates**: Update each moment line with new time/data
4. **Axis Rescaling**: Automatically adjust axis limits for new data
5. **Canvas Redraw**: Refresh display with new plot data

### Data Management
**Time History**:
- **Buffer Size**: 20 data points (4 seconds at 5 Hz)
- **Rolling Window**: Oldest data removed when buffer full
- **Time Base**: Relative time from simulation start

### Error Handling
**Robust Drawing**:
- **Try-Catch**: Ignore matplotlib drawing errors
- **Graceful Degradation**: Continue operation if drawing fails
- **Data Validation**: Check data length before processing

### Performance Optimization
**Efficient Updates**:
- **draw_idle()**: Non-blocking canvas updates
- **Conditional Rescaling**: Only rescale when sufficient data
- **Limited Buffer**: Prevent memory growth with fixed-size history

### Visual Features
- **Color Consistency**: Matches display panel color scheme
- **Legends**: Upper right positioning for both plots
- **Grid Lines**: Subtle visual reference grid
- **Tight Layout**: Optimal use of available space

### Integration Points
- **Simulation Engine**: Receives time_data and force_history
- **Main GUI Loop**: Updated every 200ms cycle
- **Data Buffer**: Synchronized with simulation data management
- **Tkinter Canvas**: Embedded matplotlib figure in GUI