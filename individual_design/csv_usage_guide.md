# Using CSV Files for Experimental and Practical Value Comparisons

This guide explains how to use the CSV files in the individual design folder for comparing experimental data with calculated values, similar to how the flight simulator uses them.

## Available CSV Files

### 1. Experimental Data Files
These files contain experimental data that can be compared with simulation results:

- `exp_individual.csv` - General experimental data for the individual helicopter design
- `main_rotor_exp_data.csv` - Detailed experimental data for the main rotor
- `rotor_data_set1.csv` - Experimental data for main rotor configuration
- `rotor_data_set2.csv` - Experimental data for tail rotor configuration
- `rotor_data_set3.csv` - Experimental data for pusher propeller configuration

### 2. Airfoil Data Files
These files contain airfoil coefficient data at different Reynolds numbers:

- `naca0012_Re3e6.csv` - NACA 0012 airfoil data at Reynolds number 3×10⁶
- `naca0012_Re6e6.csv` - NACA 0012 airfoil data at Reynolds number 6×10⁶
- `naca0012_Re9e6.csv` - NACA 0012 airfoil data at Reynolds number 9×10⁶

## File Formats

### Experimental Data Format
All experimental rotor data files follow this format:
```
theta_deg,CT_exp,CQ_exp
0,0.0000,0.00012
2,0.0007,0.00015
...
```
Where:
- `theta_deg`: Collective pitch angle in degrees
- `CT_exp`: Experimental thrust coefficient
- `CQ_exp`: Experimental torque coefficient

### Airfoil Data Format
All airfoil data files follow this format:
```
alpha_deg,Cl,Cd
-10,-1.1,0.02081
-8,-0.88,0.01602
...
```
Where:
- `alpha_deg`: Angle of attack in degrees
- `Cl`: Lift coefficient
- `Cd`: Drag coefficient

## Using CSV Files for Comparisons

### 1. Loading Data
```python
import pandas as pd

# Load experimental data
exp_data = pd.read_csv("individual_design/exp_individual.csv")

# Load airfoil data
airfoil_data = pd.read_csv("individual_design/naca0012_Re3e6.csv")
```

### 2. Running Simulations
Use the flight simulation engine to calculate corresponding values:
```python
from rotor import Rotor
from blade import Blade
from airfoil import Airfoil
from integrators import cycle_integrator

# Create components based on design parameters
airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25)
blade = Blade(R_root, R_tip, c_root, c_tip, theta_root, theta_tip, airfoil)
rotor = Rotor(B, blade)

# Run simulation
T, Q, P = cycle_integrator(rotor, V_forward, omega, rho)

# Calculate coefficients for comparison
CT = 2 * T / (rho * math.pi * omega**2 * R_tip**4)
CQ = 2 * Q / (rho * math.pi * omega**2 * R_tip**5)
```

### 3. Creating Comparison Plots
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(exp_data['theta_deg'], exp_data['CT_exp'], 'o-', label='Experimental')
plt.plot(simulated_theta, simulated_CT, 's--', label='Simulated')
plt.xlabel('Collective Pitch Angle (degrees)')
plt.ylabel('Thrust Coefficient CT')
plt.title('CT vs Pitch Angle Comparison')
plt.legend()
plt.grid(True)
plt.savefig('individual_design/comparison_plot.png')
```

## Generated Analysis Files

The following analysis scripts have been created to demonstrate usage:

1. `individual_comparison_plots.py` - Compares individual design experimental data with simulations
2. `main_rotor_analysis.py` - Detailed analysis of main rotor performance with error metrics

## Running Analysis Scripts

To generate comparison plots and analysis:

```bash
cd c:\Users\yadav\Downloads\part1
python individual_design/individual_comparison_plots.py
python individual_design/main_rotor_analysis.py
```

## Output Files

The analysis scripts generate the following output files:

- `individual_thrust_torque_comparison.png` - Comparison of thrust and torque coefficients
- `individual_thrust_vs_power.png` - Thrust vs power characteristic
- `multi_rotor_comparison.png` - Comparison of all rotor components
- `main_rotor_detailed_analysis.png` - Detailed main rotor analysis with error distributions
- `main_rotor_error_metrics.txt` - Quantitative error metrics for main rotor performance

These files provide visual and quantitative validation of the simulation against experimental data, similar to the validation performed in the flight simulator component.