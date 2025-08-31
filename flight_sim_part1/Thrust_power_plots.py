import numpy as np
import matplotlib.pyplot as plt
from integrators import cycle_integrator
from blade import Blade
from rotor import Rotor
from airfoil import Airfoil

# -----------------------------
# Global Parameters
# -----------------------------
airfoil = Airfoil(a0=5.75, Cd0=0.0113, e=1.25)
R_root, R_tip = 0.125, 0.762
c_root_default = 0.0508
theta_default = np.deg2rad(5)  # baseline pitch
rho = 1.225
rpm = 960
omega = (np.pi/30.0) * rpm

# ==================================================
# 1. Thrust & Power vs Number of Blades
# ==================================================
B_values = [2, 3, 4, 5]
T_B, P_B = [], []

for B in B_values:
    blade = Blade(R_root, R_tip, c_root_default, c_root_default, theta_default, theta_default, airfoil)
    rotor = Rotor(B, blade)
    T, Q, P, *_ = cycle_integrator(rotor, V_forward=0, omega=omega, rho=rho)
    T_B.append(T)
    P_B.append(P)

plt.figure()
plt.plot(B_values, T_B, "o-", label="Thrust")
plt.xlabel("Number of Blades B")
plt.ylabel("Thrust [N]")
plt.title("Thrust vs Number of Blades")

plt.figure()
plt.plot(B_values, P_B, "s-", label="Power", color="red")
plt.xlabel("Number of Blades B")
plt.ylabel("Power [W]")
plt.title("Power vs Number of Blades")

# ==================================================
# 2. Thrust & Power vs Taper Ratio
# ==================================================
taper_ratios = np.linspace(0.3, 1.0, 8)   # c_tip / c_root
T_taper, P_taper = [], []
B = 4  # fix blade count

for tr in taper_ratios:
    c_tip = tr * c_root_default
    blade = Blade(R_root, R_tip, c_root_default, c_tip,
                  theta_default, theta_default, airfoil)
    rotor = Rotor(B, blade)
    T, Q, P, *_ = cycle_integrator(rotor, V_forward=0, omega=omega, rho=rho)
    T_taper.append(T)
    P_taper.append(P)

plt.figure()
plt.plot(taper_ratios, T_taper, "o-")
plt.xlabel("Taper Ratio (c_tip / c_root)")
plt.ylabel("Thrust [N]")
plt.title("Thrust vs Taper Ratio")

plt.figure()
plt.plot(taper_ratios, P_taper, "s-", color="red")
plt.xlabel("Taper Ratio (c_tip / c_root)")
plt.ylabel("Power [W]")
plt.title("Power vs Taper Ratio")

# ==================================================
# 3. Thrust & Power vs Twist
# ==================================================
twists = np.deg2rad(np.linspace(0, 20, 8))  # θ_tip - θ_root
T_twist, P_twist = [], []
B = 4

for twist in twists:
    blade = Blade(R_root, R_tip, c_root_default, c_root_default,
                  theta_default, theta_default + twist, airfoil)
    rotor = Rotor(B, blade)
    T, Q, P, *_ = cycle_integrator(rotor, V_forward=0, omega=omega, rho=rho)
    T_twist.append(T)
    P_twist.append(P)

plt.figure()
plt.plot(np.rad2deg(twists), T_twist, "o-")
plt.xlabel("Twist (θ_tip - θ_root) [deg]")
plt.ylabel("Thrust [N]")
plt.title("Thrust vs Twist")

plt.figure()
plt.plot(np.rad2deg(twists), P_twist, "s-", color="red")
plt.xlabel("Twist (θ_tip - θ_root) [deg]")
plt.ylabel("Power [W]")
plt.title("Power vs Twist")

# ==================================================
# Show all plots
# ==================================================
plt.show()
