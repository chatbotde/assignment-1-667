import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

from integrators import cycle_integrator
from blade import Blade
from rotor import Rotor
from airfoil import Airfoil

# -----------------------------
# Global Parameters
# -----------------------------
rho = 1.225
rpm = 960
omega = (np.pi/30.0) * rpm
R_root, R_tip = 0.125, 0.762
c_root = c_tip = 0.0508
airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25)

# Pitch angle sweep (0° → 14°)
thetas = np.deg2rad(np.linspace(0, 14, 15))

# -----------------------------
# Read Experimental Data
# (make sure filenames match your CSV files)
# CSVs must have columns: theta_deg, CT_exp, CQ_exp
# -----------------------------
exp_data = {
    2: pd.read_csv("exp_B2.csv"),
    3: pd.read_csv("exp_B3.csv"),
    4: pd.read_csv("exp_B4.csv"),
    5: pd.read_csv("exp_B5.csv"),
}

# -----------------------------
# Compute Calculated Results
# -----------------------------
calc_results = {B: {"theta": [], "CT": [], "CQ": [], "T": [], "P": []} for B in [2, 3, 4, 5]}

for B in [2, 3, 4, 5]:
    for theta in thetas:
        blade = Blade(R_root, R_tip, c_root, c_tip, theta, theta, airfoil)
        rotor = Rotor(B, blade)
        T, Q, P = cycle_integrator(rotor, V_forward=0, omega=omega, rho=rho)

        # Performance coefficients
        CT = 2 * T / (rho * math.pi * omega**2 * R_tip**4)
        CQ = 2 * Q / (rho * math.pi * omega**2 * R_tip**5)

        calc_results[B]["theta"].append(np.rad2deg(theta))
        calc_results[B]["CT"].append(CT)
        calc_results[B]["CQ"].append(CQ)
        calc_results[B]["T"].append(T)
        calc_results[B]["P"].append(P)

# -----------------------------
# Plot CT vs Pitch Angle
# -----------------------------
plt.figure(figsize=(8,6))
for B in [2, 3, 4, 5]:
    plt.plot(calc_results[B]["theta"], calc_results[B]["CT"], "o-", label=f"Calc B={B}")
    plt.plot(exp_data[B]["theta_deg"], exp_data[B]["CT_exp"], "s--", label=f"Exp B={B}")
plt.xlabel("Pitch Angle θ [deg]")
plt.ylabel("Thrust Coefficient CT")
plt.title("CT vs Pitch Angle")
plt.legend()
plt.grid(True)

# -----------------------------
# Plot CQ vs Pitch Angle
# -----------------------------
plt.figure(figsize=(8,6))
for B in [2, 3, 4, 5]:
    plt.plot(calc_results[B]["theta"], calc_results[B]["CQ"], "o-", label=f"Calc B={B}")
    plt.plot(exp_data[B]["theta_deg"], exp_data[B]["CQ_exp"], "s--", label=f"Exp B={B}")
plt.xlabel("Pitch Angle θ [deg]")
plt.ylabel("Torque Coefficient CQ")
plt.title("CQ vs Pitch Angle")
plt.legend()
plt.grid(True)

# -----------------------------
# Plot Thrust vs Power
# -----------------------------
plt.figure(figsize=(8,6))
for B in [2, 3, 4, 5]:
    plt.plot(calc_results[B]["P"], calc_results[B]["T"], "o-", label=f"Calc B={B}")
plt.xlabel("Power P [W]")
plt.ylabel("Thrust T [N]")
plt.title("Thrust vs Power")
plt.legend()
plt.grid(True)

plt.show()
