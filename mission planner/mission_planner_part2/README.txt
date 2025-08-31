Mission Planner Program — Part 2
================================

This package implements the **Mission Planner** that chains flight segments,
computes required power using the **Flight Simulator (Part 1)** cycle-integrator,
checks power feasibility vs engine available power, and burns fuel over time.

Guidelines satisfied:
1) Python (stdlib + numpy via dependency on Flight Simulator).
2) Modular files with preamble docstrings.
3) Variables and blocks are commented.
4) User inputs centralized in `mp_inputs.py` (vehicle, engine, mission).
5) `README.txt` explains how to run.

Folder
------
imports.py          (adds sibling flight_sim_part1 to sys.path)
engine.py           (Engine model + fuel burn)
vehicle.py          (Helicopter mass/drag/tail-power settings)
planner_utils.py    (RPM solve for thrust, parasite power, tail power fraction)
segments.py         (Hover, vertical/forward climb, cruise, loiter, payload ops)
mp_inputs.py      (Initial helicopter/engine + mission segments)
main.py             (Runs the mission and writes mission_log.json)

How to run
----------
1) Ensure **both folders** are siblings in the same directory:
       /parent/flight_sim_part1/
       /parent/mission_planner_part2/
2) In a terminal:
       cd mission_planner_part2
       python3 main.py
3) Output:
   - Console summary of success and final state
   - A detailed per-second log in `mission_log.json`

Assumptions & notes
-------------------
- Rotor thrust is matched to weight by solving for RPM (bisection). Real
  helicopters typically hold constant RPM and vary collective; this simplification
  keeps Part 2 independent from Part 1 without modifying rotor internals.
- Vertical and forward climb add **rate-of-climb power**: P_climb = W * Vc.
- Tail-rotor power modeled as a fraction of main-rotor power that shrinks with
  forward speed; parameters in `vehicle.py`.
- Parasite drag power added using S_ref and CD0 from `vehicle.py`.
- Engine available power derates with density ratio exponent (alpha ~ 0.7).
