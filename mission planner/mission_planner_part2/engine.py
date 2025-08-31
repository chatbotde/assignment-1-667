import math

RHO0 = 1.225

class Engine:
    def __init__(self, P_sl_kW: float, sfc_kg_per_kWh: float = 0.32, derate_alpha: float = 0.7):
        self.P_sl_kW = P_sl_kW
        self.sfc_kg_per_kWh = sfc_kg_per_kWh
        self.derate_alpha = derate_alpha

    def power_available(self, rho: float) -> float:
        sigma = max(0.1, min(2.0, rho / RHO0))
        return self.P_sl_kW * (sigma ** self.derate_alpha)

    def fuel_burn(self, power_kW: float, dt_s: float) -> float:
        # power [kW] * time [h] * sfc [kg/kWh]
        hours = dt_s / 3600.0
        return max(0.0, power_kW) * hours * self.sfc_kg_per_kWh
