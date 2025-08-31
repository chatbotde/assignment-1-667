import math
from user_inputs import get_user_inputs, build_rotor
from atmosphere import isa_properties
from integrators import cycle_integrator
from stabilizers import Stabilizers

def run():
    inputs = get_user_inputs()
    rotor = build_rotor(inputs["rotor"])
    rho, a = isa_properties(inputs["condition"]["alt_m"])

    rpm = inputs["condition"]["rpm"]
    omega = 2*math.pi*rpm/60.0
    V = inputs["condition"]["V_forward_mps"]

    # Tip Mach safety (informational)
    M_tip = (omega*rotor.blade.R_tip)/a
    if M_tip > rotor.tip_mach_limit:
        print(f"Warning: Tip Mach {M_tip:.3f} exceeds limit {rotor.tip_mach_limit:.2f}. Consider lowering RPM or enlarging rotor.")

    T, Q, P = cycle_integrator(rotor, V, omega, rho)
    print(f"Cycle-averaged: Thrust={T:.1f} N, Torque={Q:.1f} N·m, Power={P/1000:.1f} kW")

    stab = Stabilizers(**inputs["stabilizers"])
    fm = stab.forces_moments(rho, V)
    print("Stabilizers:", {k: round(v,1) for k,v in fm.items()})

if __name__ == "__main__":
    run()
