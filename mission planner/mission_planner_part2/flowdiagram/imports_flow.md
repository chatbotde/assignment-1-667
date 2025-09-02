# Imports Module Flow Diagram

```mermaid
flowchart TD
    A[Start: Imports Module] --> B[add_flight_sim_path Function]
    
    B --> C[Get Current Directory<br/>here = os.path.dirname(os.path.abspath(__file__))]
    C --> D[Calculate Sibling Path<br/>sibling = os.path.join(os.path.dirname(here), "flight_sim_part1")]
    D --> E{Directory Exists?}
    E -->|No| F[Return Sibling Path<br/>(not added to sys.path)]
    E -->|Yes| G{Already in sys.path?}
    G -->|Yes| H[Return Sibling Path<br/>(already available)]
    G -->|No| I[Add to Python Path<br/>sys.path.insert(0, sibling)]
    I --> J[Return Sibling Path<br/>(successfully added)]
    
    F --> K[End]
    H --> K
    J --> K

    style A fill:#e1f5fe
    style K fill:#e8f5e8
    style B fill:#e3f2fd
    style E fill:#ffeb3b
    style G fill:#ffeb3b
    style C fill:#fff3e0
    style D fill:#fff3e0
    style I fill:#f3e5f5
```

## Imports Module
**Purpose**: Helper module to dynamically import flight simulation components

### Function: add_flight_sim_path()
**Purpose**: Add flight_sim_part1 directory to Python path for imports

**Process**:
1. **Get Current Location**: Find the current file's directory
2. **Calculate Sibling Path**: Navigate to parent directory and find flight_sim_part1
3. **Validate Directory**: Check if the flight simulation directory exists
4. **Check Path**: Verify if already in Python path to avoid duplicates
5. **Add to Path**: Insert at beginning of sys.path for priority import
6. **Return Path**: Provide path for verification or debugging

### Key Features
- **Dynamic Path Resolution**: Works regardless of installation location
- **Duplicate Prevention**: Checks before adding to avoid path pollution
- **Priority Import**: Uses insert(0, path) for highest import priority
- **Error Tolerance**: Returns path even if directory doesn't exist

### Usage Pattern
```python
from imports import add_flight_sim_path
add_flight_sim_path()

# Now can import flight simulation modules
from user_inputs import get_user_inputs
from atmosphere import isa_properties
from integrators import cycle_integrator
```

### Integration Points
- Used by all mission planner modules that need flight simulation
- Enables seamless integration between mission planner and flight simulation
- Supports flexible project structure and deployment