import math
from dataclasses import dataclass

from imports import add_flight_sim_path
add_flight_sim_path()

from atmosphere import isa_properties
from planner_utils import solve_rpm_for_thrust, parasite_power, tail_power_fraction

@dataclass
class SegmentResult:
    success: bool
    reason: str
    log: list

def run_hover(heli, engine, rotor, duration_s, alt_m, dt_s=1.0):
    t = 0.0
    log = []
    while t < duration_s - 1e-6:
        rho, a = isa_properties(alt_m)
        W = heli.weight_N()
        # Solve RPM to match thrust = W
        try:
            rpm, omega, T, Q, P_main = solve_rpm_for_thrust(rotor, rho, a, V_forward=0.0, thrust_req_N=W)
        except ValueError as e:
            return SegmentResult(False, f"Hover infeasible: {e}", log)

        P_tail = P_main * tail_power_fraction(0.0, heli.tail_power_hover_frac, heli.tail_power_min_frac)
        P_par = 0.0
        P_req_kW = (P_main + P_tail + P_par)/1000.0

        P_avail_kW = engine.power_available(rho)
        if P_req_kW > P_avail_kW + 1e-6:
            return SegmentResult(False, f"Power shortfall in hover: need {P_req_kW:.1f} kW, have {P_avail_kW:.1f} kW", log)

        fuel_used = engine.fuel_burn(P_req_kW, dt_s)
        if fuel_used > heli.fuel_kg + 1e-9:
            return SegmentResult(False, "Fuel exhausted in hover.", log)
        heli.fuel_kg -= fuel_used

        log.append({
            "type":"hover","time_s":t,"altitude_m":alt_m,"rpm":rpm,
            "P_main_kW":P_main/1000.0,"P_tail_kW":P_tail/1000.0,"P_par_kW":P_par/1000.0,
            "P_avail_kW":P_avail_kW,"fuel_remaining_kg":heli.fuel_kg,"mass_kg":heli.mass_total()
        })
        t += dt_s
    return SegmentResult(True, "ok", log)

def run_vertical_climb(heli, engine, rotor, duration_s, start_alt_m, climb_rate_mps, dt_s=1.0):
    t = 0.0; alt = start_alt_m
    log = []
    while t < duration_s - 1e-6:
        rho, a = isa_properties(alt)
        W = heli.weight_N()
        # Match thrust ~ weight, add rate-of-climb power T*Vc
        try:
            rpm, omega, T, Q, P_main = solve_rpm_for_thrust(rotor, rho, a, V_forward=0.0, thrust_req_N=W)
        except ValueError as e:
            return SegmentResult(False, f"Vertical climb infeasible: {e}", log)

        P_climb = W * max(0.0, climb_rate_mps)  # Watts
        P_tail  = P_main * tail_power_fraction(0.0, heli.tail_power_hover_frac, heli.tail_power_min_frac)
        P_par   = 0.0
        P_req_kW = (P_main + P_tail + P_par + P_climb)/1000.0

        P_avail_kW = engine.power_available(rho)
        if P_req_kW > P_avail_kW + 1e-6:
            return SegmentResult(False, f"Power shortfall in vertical climb: need {P_req_kW:.1f} kW, have {P_avail_kW:.1f} kW", log)

        fuel_used = engine.fuel_burn(P_req_kW, dt_s)
        if fuel_used > heli.fuel_kg + 1e-9:
            return SegmentResult(False, "Fuel exhausted in vertical climb.", log)
        heli.fuel_kg -= fuel_used
        alt += climb_rate_mps * dt_s

        log.append({
            "type":"vclimb","time_s":t,"altitude_m":alt,"rpm":rpm,
            "P_main_kW":P_main/1000.0,"P_tail_kW":P_tail/1000.0,"P_par_kW":P_par/1000.0,
            "P_climb_kW":P_climb/1000.0,"P_avail_kW":P_avail_kW,"fuel_remaining_kg":heli.fuel_kg
        })
        t += dt_s
    return SegmentResult(True, "ok", log)

def run_forward_climb(heli, engine, rotor, duration_s, start_alt_m, climb_rate_mps, V_forward_mps, dt_s=1.0):
    t = 0.0; alt = start_alt_m
    log = []
    while t < duration_s - 1e-6:
        rho, a = isa_properties(alt)
        W = heli.weight_N()

        try:
            rpm, omega, T, Q, P_main = solve_rpm_for_thrust(rotor, rho, a, V_forward=V_forward_mps, thrust_req_N=W)
        except ValueError as e:
            return SegmentResult(False, f"Forward climb infeasible: {e}", log)

        P_climb = W * max(0.0, climb_rate_mps)
        P_tail = P_main * tail_power_fraction(V_forward_mps, heli.tail_power_hover_frac, heli.tail_power_min_frac)
        P_par  = parasite_power(rho, V_forward_mps, heli.S_ref_m2, heli.CD0_body)
        P_req_kW = (P_main + P_tail + P_par + P_climb)/1000.0

        P_avail_kW = engine.power_available(rho)
        if P_req_kW > P_avail_kW + 1e-6:
            return SegmentResult(False, f"Power shortfall in forward climb: need {P_req_kW:.1f} kW, have {P_avail_kW:.1f} kW", log)

        fuel_used = engine.fuel_burn(P_req_kW, dt_s)
        if fuel_used > heli.fuel_kg + 1e-9:
            return SegmentResult(False, "Fuel exhausted in forward climb.", log)
        heli.fuel_kg -= fuel_used
        alt += climb_rate_mps * dt_s

        log.append({
            "type":"fclimb","time_s":t,"altitude_m":alt,"rpm":rpm,
            "P_main_kW":P_main/1000.0,"P_tail_kW":P_tail/1000.0,"P_par_kW":P_par/1000.0,
            "P_climb_kW":P_climb/1000.0,"P_avail_kW":P_avail_kW,"fuel_remaining_kg":heli.fuel_kg
        })
        t += dt_s
    return SegmentResult(True, "ok", log)

def run_cruise(heli, engine, rotor, duration_s, alt_m, V_forward_mps, dt_s=1.0):
    t = 0.0
    log = []
    while t < duration_s - 1e-6:
        rho, a = isa_properties(alt_m)
        W = heli.weight_N()

        try:
            rpm, omega, T, Q, P_main = solve_rpm_for_thrust(rotor, rho, a, V_forward=V_forward_mps, thrust_req_N=W)
        except ValueError as e:
            return SegmentResult(False, f"Cruise infeasible: {e}", log)

        P_tail = P_main * tail_power_fraction(V_forward_mps, heli.tail_power_hover_frac, heli.tail_power_min_frac)
        P_par  = parasite_power(rho, V_forward_mps, heli.S_ref_m2, heli.CD0_body)
        P_req_kW = (P_main + P_tail + P_par)/1000.0

        P_avail_kW = engine.power_available(rho)
        if P_req_kW > P_avail_kW + 1e-6:
            return SegmentResult(False, f"Power shortfall in cruise: need {P_req_kW:.1f} kW, have {P_avail_kW:.1f} kW", log)

        fuel_used = engine.fuel_burn(P_req_kW, dt_s)
        if fuel_used > heli.fuel_kg + 1e-9:
            return SegmentResult(False, "Fuel exhausted in cruise.", log)
        heli.fuel_kg -= fuel_used

        log.append({
            "type":"cruise","time_s":t,"altitude_m":alt_m,"rpm":rpm,
            "P_main_kW":P_main/1000.0,"P_tail_kW":P_tail/1000.0,"P_par_kW":P_par/1000.0,
            "P_avail_kW":P_avail_kW,"fuel_remaining_kg":heli.fuel_kg
        })
        t += dt_s
    return SegmentResult(True, "ok", log)

def run_loiter(heli, engine, rotor, duration_s, alt_m, V_loiter_mps, dt_s=1.0):
    # identical to cruise but parameterized separately
    return run_cruise(heli, engine, rotor, duration_s, alt_m, V_loiter_mps, dt_s)

def run_payload_op(heli, kind: str, delta_mass_kg: float, duration_hover_s: float, alt_m: float, engine=None, rotor=None, dt_s=1.0):
    """
    kind: 'pickup' or 'drop' ; delta_mass_kg > 0
    If duration_hover_s > 0, holds hover for that time (with feasibility checks) before mass change.
    """
    logs = []
    if duration_hover_s > 0 and engine and rotor:
        res = run_hover(heli, engine, rotor, duration_hover_s, alt_m, dt_s)
        logs += res.log
        if not res.success:
            return SegmentResult(False, f"Payload op hover failed: {res.reason}", logs)

    if kind == "pickup":
        heli.payload_kg += abs(delta_mass_kg)
    elif kind == "drop":
        heli.payload_kg = max(0.0, heli.payload_kg - abs(delta_mass_kg))
    else:
        return SegmentResult(False, "Unknown payload op type", logs)
    logs.append({"type":"payload_"+kind, "delta_kg":delta_mass_kg, "payload_now_kg":heli.payload_kg})
    return SegmentResult(True, "ok", logs)
