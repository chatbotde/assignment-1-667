import math
from airfoil import Airfoil
from blade import Blade
from rotor import Rotor

def get_user_inputs():
    # Original experimental configuration for comparison with CSV data
    # Matches the specifications from your experimental table
    return {
        "rotor": {
            "B": 4,  # Can be changed to 2/3/4/5 for comparison
            "R_root": 0.125,  # Root cut-out
            "R_tip": 0.762,   # Radius from experimental table
            "c_root": 0.0508, # Chord length from table
            "c_tip": 0.0508,  # Constant chord
            "theta_root_deg": 1.0,
            "theta_tip_deg": 1.0,
            "airfoil": {"a0": 5.75, "Cd0": 0.0113, "e": 1.25, "alpha_stall_deg": 15.0},
            "tip_mach_limit": 0.90
        },
        "stabilizers": {
            "S_h": 2.2, "i_h_deg": 2.0, "CLa_h_per_rad": 6.5, "l_h": 5.0,
            "S_v": 1.5, "CYb_v_per_rad": 2.4, "l_v": 3.0,
        },
        "condition": {
            "alt_m": 0.0,
            "V_forward_mps": 0.0,
            "rpm": 960.0  # Original RPM for experimental comparison
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
