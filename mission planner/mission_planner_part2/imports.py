"""
imports.py
----------
Small helper to import the Flight Simulator (Part 1) modules when placed
as a sibling folder named 'flight_sim_part1'.
"""
import os, sys

def add_flight_sim_path():
    # assume sibling folder; adjust if not found
    here = os.path.dirname(os.path.abspath(__file__))
    sibling = os.path.join(os.path.dirname(here), "flight_sim_part1")
    if os.path.isdir(sibling) and sibling not in sys.path:
        sys.path.insert(0, sibling)
    return sibling
