import math

class Airfoil:
    def __init__(self, a0=2*math.pi, Cd0=0.008, e=0.9, alpha_stall_deg=15.0):
        self.a0 = a0
        self.Cd0 = Cd0
        self.e = e
        self.alpha_stall = math.radians(alpha_stall_deg)

    def lookup(self, alpha_rad: float):
        # soft stall clamp
        alpha_eff = max(-self.alpha_stall, min(self.alpha_stall, alpha_rad))
        Cl = self.a0 * alpha_eff
        # simple drag polar: Cd = Cd0 + k*Cl^2
        k = 1.0/(math.pi*6.0*self.e)  # AR~6 surrogate
        Cd = self.Cd0 + k*Cl*Cl
        Cm = 0.0
        return Cl, Cd, Cm
