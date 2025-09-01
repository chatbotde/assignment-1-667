Flight Simulator Program — Part 1
=================================

This folder contains a **self‑contained, modular** implementation of the Flight
Simulator part of  assignment. It follows the guidelines:

1) Free language: **Python 3** (uses only stdlib + numpy).
2) Modular files (one module per requirement) with preamble docstrings.
3) Variable and block comments throughout.
4) User inputs are centralized in `user_inputs.py`.
5) Instructions below show exactly how to run.

Folder layout
-------------
airfoil.py        (Module 4: Airfoil data / polar lookup)
blade.py          (Module 2: Blade geometry)
rotor.py          (Rotor container — blades + count)
atmosphere.py     (Module 3: ISA atmosphere model)
inflow.py         (Module 5: Induced velocity annulus solver + tip-loss)
integrators.py    (Modules 6 & 7: Instantaneous and Cycle integrators)
stabilizers.py    (Module 8: Horizontal & Vertical stabilizers)
user_inputs.py    (Module 1: User inputs; also builds the Rotor object)
main.py           (Entry point; wires all modules, prints results)

How to run
----------
1) Ensure Python 3 and numpy are installed.
2) From a terminal in this folder, run:
       python3 main.py

What you can edit quickly
-------------------------
- In `user_inputs.py`:
  * change rotor geometry (radii, chord, twist)
  * number of blades, tip Mach limit
  * airfoil parameters (a0, Cd0, e)
  * flight condition (altitude, forward speed, RPM)
  * stabilizer geometry & gains

Outputs printed
---------------
- Cycle-averaged rotor Thrust [N], Torque [N·m], Power [kW]
- Stabilizer forces/moments (L_h, Y_v, M_pitch, M_yaw)

Notes & assumptions
-------------------
- BEMT formulation is simplified for clarity; compressibility effects are not
  explicitly modeled beyond a tip Mach warning. For higher fidelity, add Mach
  corrections and non-linear polars.
- Azimuthal inflow variation is included in the instantaneous integrator.
- The stabilizer model is linear; tune gains to your configuration.

 
