import math
from airfoil import Airfoil
from blade import Blade
from rotor import Rotor

def get_user_inputs():
    # Optimized configuration for hover feasibility
    # Based on realistic helicopter parameters
    return {
        "rotor": {
            "B": 4,
            "R_root": 0.150,
            "R_tip": 1.500,
            "c_root": 0.120,
            "c_tip": 0.080,
            "theta_root_deg": 15.0,
            "theta_tip_deg": 10.0,
            "airfoil": {"a0": 5.75, "Cd0": 0.008, "e": 0.9, "alpha_stall_deg": 15.0},
            "tip_mach_limit": 0.90
        },
        "stabilizers": {
            "S_h": 2.2, "i_h_deg": 2.0, "CLa_h_per_rad": 6.5, "l_h": 5.0,
            "S_v": 1.5, "CYb_v_per_rad": 2.4, "l_v": 3.0,
        },
        "condition": {
            "alt_m": 0.0,
            "V_forward_mps": 0.0,
            "rpm": 1200.0
        }
    }

def build_rotor(params):
    af = Airfoil(**params["airfoil"])
    bl = Blade(params["R_root"], params["R_tip"],
               params["c_root"], params["c_tip"],
               math.radians(params["theta_root_deg"]),
               math.radians(params["theta_tip_deg"]))
    bl.airfoil = af
    return Rotor(params["B"], bl, tip_mach_limit=params.get("tip_mach_limit", 0.9))
