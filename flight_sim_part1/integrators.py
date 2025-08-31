import math, numpy as np
from inflow import induced_velocity_annulus

def instantaneous_integrator(rotor, V_forward, omega, rho, n_sections=48, n_azimuth=36):
    b = rotor.blade
    mu = np.linspace(0, 1, n_sections)
    r_nodes = 0.5*(1 - np.cos(np.pi*mu))  # cosine spacing
    r = b.R_root + (b.R_tip - b.R_root) * r_nodes
    dr = np.gradient(r)

    T_psi = np.zeros(n_azimuth)
    Q_psi = np.zeros(n_azimuth)

    for j, psi in enumerate(np.linspace(0.0, 2*np.pi, n_azimuth, endpoint=False)):
        Vax_psi  = V_forward * math.cos(psi)
        Vtan_psi = V_forward * math.sin(psi)
        T = Q = 0.0

        for ri, dri in zip(r, dr):
            if b.c(ri) <= 0: 
                continue
            vi, phi, q, Cl, Cd, U0 = induced_velocity_annulus(rotor, ri, Vax_psi, omega, rho)

            Ut  = omega*ri + Vtan_psi
            Uax = Vax_psi + vi
            phi = math.atan2(Uax, Ut)
            U = math.hypot(Ut, Uax)
            q  = 0.5*rho*U*U

            Lp = q*b.c(ri)*Cl
            Dp = q*b.c(ri)*Cd
            dT = rotor.B * (Lp*math.cos(phi) - Dp*math.sin(phi)) * dri
            dQ = rotor.B * (Lp*math.sin(phi) + Dp*math.cos(phi)) * ri * dri
            T += dT; Q += dQ

        T_psi[j] = T
        Q_psi[j] = Q

    return T_psi, Q_psi

def cycle_integrator(rotor, V_forward, omega, rho):
    T_psi, Q_psi = instantaneous_integrator(rotor, V_forward, omega, rho)
    T = float(np.mean(T_psi))
    Q = float(np.mean(Q_psi))
    P = Q*omega
    return T, Q, P
