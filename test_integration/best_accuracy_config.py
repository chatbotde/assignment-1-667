import math
from airfoil import Airfoil
from blade import Blade
from rotor import Rotor

def get_user_inputs():
    # Best accuracy configuration based on experimental validation
    # Uses 3D corrections and optimal blade count
    return {
        "rotor": {
            "B": 5,  # Optimal blade count for accuracy
            "R_root": 0.125,
            "R_tip": 0.762,
            "c_root": 0.0508,
            "c_tip": 0.0508,
            "theta_root_deg": 1.0,
            "theta_tip_deg": 1.0,
            # 3D-corrected airfoil parameters
            "airfoil": {"a0": 5.12, "Cd0": 0.008, "e": 0.85, "alpha_stall_deg": 18.0},
            "tip_mach_limit": 0.90
        },
        "stabilizers": {
            "S_h": 2.2, "i_h_deg": 2.0, "CLa_h_per_rad": 6.5, "l_h": 5.0,
            "S_v": 1.5, "CYb_v_per_rad": 2.4, "l_v": 3.0,
        },
        "condition": {
            "alt_m": 0.0,
            "V_forward_mps": 0.0,
            "rpm": 960.0
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
