import math

from imports import add_flight_sim_path
add_flight_sim_path()

from user_inputs import get_user_inputs as fs_get_inputs, build_rotor
from airfoil import Airfoil
from blade import Blade
from rotor import Rotor

from engine import Engine
from vehicle import Helicopter

def get_helicopter_and_engine():
    # Reuse the rotor from Flight Simulator Part 1
    fs_inputs = fs_get_user_inputs()
    rotor = build_rotor(fs_inputs["rotor"])

    heli = Helicopter(
        oew_kg = 2500.0,
        payload_kg = 300.0,
        fuel_kg = 400.0,
        S_ref_m2 = 6.0,
        CD0_body = 0.045,
        tail_power_hover_frac = 0.07,
        tail_power_min_frac = 0.015
    )
    engine = Engine(P_sl_kW=1500.0, sfc_kg_per_kWh=0.32, derate_alpha=0.7)
    return heli, engine, rotor

def fs_get_user_inputs():
    # alias to make the name explicit
    return fs_get_inputs()

def mission_definition():
    """
    A list of mission segments. Each item has a 'type' and parameters.
    Types: hover, vclimb, fclimb, cruise, loiter, payload
    """
    return [
        {"type":"hover",  "duration_s":60,  "altitude_m":0.0},
        {"type":"vclimb", "duration_s":120, "start_alt_m":0.0, "climb_rate_mps":3.0},
        {"type":"cruise", "duration_s":300, "altitude_m":360, "V_forward_mps":45.0},
        {"type":"payload","kind":"drop","delta_mass_kg":100.0,"duration_hover_s":30,"altitude_m":360},
        {"type":"loiter", "duration_s":120, "altitude_m":360, "V_loiter_mps":25.0},
        {"type":"fclimb","duration_s":60,  "start_alt_m":360, "climb_rate_mps":1.0, "V_forward_mps":35.0},
        {"type":"cruise", "duration_s":240, "altitude_m":420, "V_forward_mps":50.0},
    ]
