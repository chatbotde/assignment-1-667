import math

class Stabilizers:
    def __init__(self, S_h, i_h_deg, CLa_h_per_rad, l_h, S_v, CYb_v_per_rad, l_v):
        self.S_h = S_h
        self.i_h = math.radians(i_h_deg)
        self.CLa_h = CLa_h_per_rad
        self.l_h = l_h
        self.S_v = S_v
        self.CYb_v = CYb_v_per_rad
        self.l_v = l_v

    def forces_moments(self, rho, V, alpha_fus_rad=0.0, beta_rad=0.0):
        q = 0.5*rho*V*V
        L_h = q*self.S_h*self.CLa_h*(alpha_fus_rad + self.i_h)
        Y_v = q*self.S_v*self.CYb_v*beta_rad
        M_pitch = -L_h*self.l_h
        M_yaw   =  Y_v*self.l_v
        return {"L_h": L_h, "Y_v": Y_v, "M_pitch": M_pitch, "M_yaw": M_yaw}
