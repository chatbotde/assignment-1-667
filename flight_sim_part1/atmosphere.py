import math

def isa_properties(alt_m: float):
    # Sea-level
    T0 = 288.15
    p0 = 101325.0
    rho0 = 1.225
    g = 9.80665
    L = -0.0065   # K/m
    R = 287.05287
    gamma = 1.4

    if alt_m <= 11000.0:
        T = T0 + L*alt_m
        p = p0 * (T/T0) ** (-g/(L*R))
        rho = p / (R*T)
    else:
        # very simple extension (isothermal above 11 km)
        T = T0 + L*11000.0
        p = p0 * (T/T0) ** (-g/(L*R)) * math.exp(-g*(alt_m-11000.0)/(R*T))
        rho = p / (R*T)

    a = math.sqrt(gamma*R*T)
    return rho, a
