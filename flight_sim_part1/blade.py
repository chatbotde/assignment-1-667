import math

class Blade:
    def __init__(self, R_root, R_tip, c_root, c_tip, theta_root_rad, theta_tip_rad, airfoil=None):
        self.R_root = R_root
        self.R_tip = R_tip
        self.c_root = c_root
        self.c_tip = c_tip
        self.theta_root = theta_root_rad
        self.theta_tip = theta_tip_rad
        self.airfoil = airfoil

    def c(self, r):
        # linear taper
        mu = (r - self.R_root) / max(1e-9, (self.R_tip - self.R_root))
        return self.c_root + mu*(self.c_tip - self.c_root)

    def theta(self, r):
        # linear twist
        mu = (r - self.R_root) / max(1e-9, (self.R_tip - self.R_root))
        return self.theta_root + mu*(self.theta_tip - self.theta_root)
