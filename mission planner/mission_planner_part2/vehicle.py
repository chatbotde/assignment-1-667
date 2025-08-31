from dataclasses import dataclass

g = 9.80665

@dataclass
class Helicopter:
    oew_kg: float
    payload_kg: float
    fuel_kg: float
    S_ref_m2: float = 6.0
    CD0_body: float = 0.04
    tail_power_hover_frac: float = 0.07
    tail_power_min_frac: float = 0.015

    def mass_total(self) -> float:
        return self.oew_kg + self.payload_kg + self.fuel_kg

    def weight_N(self) -> float:
        return self.mass_total() * g
