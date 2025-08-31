import math

from imports import add_flight_sim_path
add_flight_sim_path()

from atmosphere import isa_properties
from user_inputs import build_rotor
from integrators import cycle_integrator
from stabilizers import Stabilizers

def tip_mach(omega, R_tip, a):
    return (omega*R_tip)/max(1e-9, a)

def solve_rpm_for_thrust(rotor, rho, a, V_forward, thrust_req_N, rpm_lo=200.0, rpm_hi=390.0, tol=1e-3):
    """
    Bisection on RPM to match required thrust, respecting rotor.tip_mach_limit.
    Returns (rpm, omega, T, Q, P) or raises ValueError if infeasible.
    """
    R = rotor.blade.R_tip
    # Trim rpm_hi to tip Mach limit
    rpm_hi = min(rpm_hi, (rotor.tip_mach_limit * a / max(1e-9, R)) * 60.0/(2*math.pi))

    def thrust_at_rpm(rpm):
        omega = 2*math.pi*rpm/60.0
        T, Q, P = cycle_integrator(rotor, V_forward, omega, rho)
        return T, Q, P

    T_lo, _, _ = thrust_at_rpm(rpm_lo)
    T_hi, _, _ = thrust_at_rpm(rpm_hi)
    if T_hi < thrust_req_N:
        raise ValueError(f"Thrust requirement {thrust_req_N:.1f} N exceeds capability under tip-Mach limit (max T={T_hi:.1f} N).")

    for _ in range(40):
        rpm_mid = 0.5*(rpm_lo+rpm_hi)
        T_mid, Q_mid, P_mid = thrust_at_rpm(rpm_mid)
        if abs(T_mid - thrust_req_N) <= tol*max(1.0, thrust_req_N):
            omega_mid = 2*math.pi*rpm_mid/60.0
            return rpm_mid, omega_mid, T_mid, Q_mid, P_mid
        if T_mid < thrust_req_N:
            rpm_lo = rpm_mid
        else:
            rpm_hi = rpm_mid

    rpm_mid = 0.5*(rpm_lo+rpm_hi)
    omega_mid = 2*math.pi*rpm_mid/60.0
    T_mid, Q_mid, P_mid = thrust_at_rpm(rpm_mid)
    return rpm_mid, omega_mid, T_mid, Q_mid, P_mid

def parasite_power(rho, V, S_ref_m2=6.0, CD0=0.04):
    q = 0.5*rho*V*V
    D = q*S_ref_m2*CD0
    return D*V  # Watts

def tail_power_fraction(V, f_hover=0.07, f_min=0.015, V0=30.0):
    import math
    return f_min + (f_hover - f_min)*math.exp(-(V/V0)**2)
