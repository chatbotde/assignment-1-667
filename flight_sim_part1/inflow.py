import math

def prandtl_tip_loss(B, r, R, lambda_):
    lambda_safe = max(abs(lambda_), 1e-8)
    f = 0.5 * B * (1.0 - r / R) / lambda_safe
    f = min(max(f, 1e-8), 50.0)        # keep in range
    exp_arg = math.exp(-f)
    F = (2.0 / math.pi) * math.acos(min(1.0, max(-1.0, exp_arg)))
    return max(F, 1e-6)


def induced_velocity_annulus(rotor, r, V, omega, rho, max_iter=200, tol=1e-6, damp=0.6):
    b = rotor.blade
    B = rotor.B
    Ut = omega * r
    c = b.c(r)
    th = b.theta(r)

    # initial guess for vi
    vi = 0.05 * max(1.0, Ut)

    for _ in range(max_iter):
        Uax = V + vi
        phi = math.atan2(Uax, Ut)

        lambda_local = (V + vi) / (omega * r) if (omega * r) != 0.0 else 1e-8
        F = prandtl_tip_loss(B, r, b.R_tip, lambda_local)

        U = math.hypot(Ut, Uax)
        q = 0.5 * rho * U * U
        alpha = th - phi
        Cl, Cd, _ = b.airfoil.lookup(alpha)   # ✅ lookup

        dT_BE_dr = B * q * c * (Cl * math.cos(phi) - Cd * math.sin(phi))
        dT_MT_dr = 4.0 * math.pi * rho * F * r * Uax * vi

        Rres = dT_BE_dr - dT_MT_dr
        if abs(Rres) < tol * (1.0 + abs(dT_BE_dr)):
            break

        # finite-difference slope
        dvi = max(1e-4, 0.01 * (vi + 1.0))
        vi_p = max(0.0, vi + dvi)
        Uax_p = V + vi_p
        phi_p = math.atan2(Uax_p, Ut)
        lambda_p = (V + vi_p) / (omega * r) if (omega * r) != 0.0 else 1e-8
        F_p = prandtl_tip_loss(B, r, b.R_tip, lambda_p)
        U_p = math.hypot(Ut, Uax_p)
        q_p = 0.5 * rho * U_p * U_p
        alpha_p = th - phi_p
        Cl_p, Cd_p, _ = b.airfoil.lookup(alpha_p)  # ✅ lookup
        dT_BE_dr_p = B * q_p * c * (Cl_p * math.cos(phi_p) - Cd_p * math.sin(phi_p))
        dT_MT_dr_p = 4.0 * math.pi * rho * F_p * r * Uax_p * vi_p
        Rres_p = dT_BE_dr_p - dT_MT_dr_p

        dR_dvi = (Rres_p - Rres) / dvi if abs(Rres_p - Rres) > 1e-16 else 1.0
        step = -Rres / dR_dvi
        vi = max(0.0, vi + damp * step)

    # final local quantities
    Uax = V + vi
    phi = math.atan2(Uax, Ut)
    U = math.hypot(Ut, Uax)
    q = 0.5 * rho * U * U
    alpha = th - phi
    Cl, Cd, _ = b.airfoil.lookup(alpha)   # ✅ lookup
    return vi, phi, q, Cl, Cd, U
