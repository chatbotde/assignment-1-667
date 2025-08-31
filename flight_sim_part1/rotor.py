import math
from blade import Blade

class Rotor:
    def __init__(self, B: int, blade: Blade, tip_mach_limit=0.90):
        self.B = B
        self.blade = blade
        self.tip_mach_limit = tip_mach_limit  # for safety in the solver
        
    def solidity_local(self, r):
        # local solidity based on circumference annulus
        return (self.B * self.blade.c(r)) / (2 * math.pi * r)