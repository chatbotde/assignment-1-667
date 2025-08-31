import json
from mp_inputs import get_helicopter_and_engine, mission_definition
from segments import run_hover, run_vertical_climb, run_forward_climb, run_cruise, run_loiter, run_payload_op

def run_mission():
    heli, engine, rotor = get_helicopter_and_engine()
    mission = mission_definition()

    full_log = []
    current_alt = 0.0

    for seg in mission:
        typ = seg["type"]
        if typ == "hover":
            res = run_hover(heli, engine, rotor, seg["duration_s"], seg["altitude_m"])
            current_alt = seg["altitude_m"]
        elif typ == "vclimb":
            res = run_vertical_climb(heli, engine, rotor, seg["duration_s"], seg["start_alt_m"], seg["climb_rate_mps"])
            current_alt = seg["start_alt_m"] + seg["climb_rate_mps"]*seg["duration_s"]
        elif typ == "fclimb":
            res = run_forward_climb(heli, engine, rotor, seg["duration_s"], seg["start_alt_m"], seg["climb_rate_mps"], seg["V_forward_mps"])
            current_alt = seg["start_alt_m"] + seg["climb_rate_mps"]*seg["duration_s"]
        elif typ == "cruise":
            res = run_cruise(heli, engine, rotor, seg["duration_s"], seg["altitude_m"], seg["V_forward_mps"])
            current_alt = seg["altitude_m"]
        elif typ == "loiter":
            res = run_loiter(heli, engine, rotor, seg["duration_s"], seg["altitude_m"], seg["V_loiter_mps"])
            current_alt = seg["altitude_m"]
        elif typ == "payload":
            res = run_payload_op(heli, seg["kind"], seg["delta_mass_kg"], seg.get("duration_hover_s",0.0), seg.get("altitude_m", current_alt), engine, rotor)
        else:
            return False, f"Unknown segment type: {typ}", full_log

        full_log.extend(res.log)
        if not res.success:
            return False, res.reason, full_log

    return True, "Mission completed", full_log

if __name__ == "__main__":
    ok, msg, log = run_mission()
    out = {"success": ok, "message": msg, "n_records": len(log), "last_state": log[-1] if log else None}
    print(json.dumps(out, indent=2))
    with open("mission_log.json","w") as f:
        json.dump(log, f, indent=2)
