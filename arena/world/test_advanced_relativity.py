"""
Unit Tests for Advanced Relativistic Mechanics and Cosmological Limits
Agent: Raman (A002, Gen 0)
"""

import unittest
import math
from advanced_relativity_analyzer import (
    c, g, m_p, e_charge, u_cmb_0, T_cmb_0,
    lorentz_factor, beta_from_gamma,
    cmb_radiation_drag_exact, cmb_flux_ultra,
    cosmological_crossover_threshold,
    bussard_ramjet_analysis,
    preionization_laser_power,
    bethe_bloch_and_spallation,
    spacelike_temporal_inversion_4vector
)

class TestAdvancedRelativisticPhysics(unittest.TestCase):

    def test_lorentz_and_beta_inversion(self):
        for gamma in [1.5, 2.0, 7.0888, 100.0, 10000.0]:
            beta = beta_from_gamma(gamma)
            gamma_recov = lorentz_factor(beta)
            self.assertAlmostEqual(gamma, gamma_recov, delta=gamma * 1e-6)

    def test_cmb_radiation_drag_exact_vs_approx(self):
        # In ultra-relativistic limit (gamma >= 10), exact flux should approach (4/3) * gamma^2 * c * u_0
        res = cmb_radiation_drag_exact(0.999)
        flux_exact = res["flux_W_m2"]
        flux_approx = res["ultra_approx_flux_W_m2"]
        # Within a few percent for gamma = 22.4
        self.assertAlmostEqual(flux_exact / flux_approx, 1.0, delta=0.08)

    def test_cmb_flux_ultra_continuity(self):
        # Check continuity between exact and ultra at gamma = 100
        beta_100 = beta_from_gamma(100.0)
        res_exact = cmb_radiation_drag_exact(beta_100)
        res_ultra = cmb_flux_ultra(100.0)
        self.assertAlmostEqual(res_exact["flux_W_m2"] / res_ultra["flux_W_m2"], 1.0, delta=1e-4)
        self.assertAlmostEqual(res_exact["pressure_Pa"] / res_ultra["pressure_Pa"], 1.0, delta=1e-4)

    def test_cosmological_crossover(self):
        # Galactic ISM n_H = 1 cm^-3: crossover should be at gamma ~ 2.7e9
        cross_ism = cosmological_crossover_threshold(1.0)
        self.assertAlmostEqual(cross_ism["gamma_crossover"] / 2.7e9, 1.0, delta=0.05)
        
        # Intergalactic IGM n_H = 1e-7 cm^-3: crossover at gamma ~ 270
        cross_igm = cosmological_crossover_threshold(1e-7)
        self.assertAlmostEqual(cross_igm["gamma_crossover"], 270.0, delta=5.0)

    def test_bussard_ramjet_kinematic_limit(self):
        # With beta_e = 0.089c, net thrust must be positive for v < 0.089c
        bj_sub = bussard_ramjet_analysis(0.05, beta_e=0.089)
        self.assertTrue(bj_sub["is_accelerating"])
        self.assertGreater(bj_sub["net_thrust_ideal_N"], 0.0)
        
        # At v = 0.089c, net thrust is 0
        bj_crit = bussard_ramjet_analysis(0.089, beta_e=0.089)
        self.assertAlmostEqual(bj_crit["net_thrust_ideal_N"], 0.0, delta=1.0)
        
        # For v > 0.089c, net thrust must be negative (deceleration)
        bj_super = bussard_ramjet_analysis(0.12, beta_e=0.089)
        self.assertFalse(bj_super["is_accelerating"])
        self.assertLess(bj_super["net_thrust_ideal_N"], 0.0)

    def test_preionization_laser_power(self):
        # Power for 5m diameter ship at 0.9c should exceed 100 Terawatts
        p_res = preionization_laser_power(0.9, ship_diameter_m=5.0)
        self.assertGreater(p_res["power_terawatts"], 100.0)
        self.assertGreater(p_res["human_planetary_grid_ratio"], 30.0)

    def test_hadronic_spallation_scale(self):
        # Nuclear interaction length (lambda_I) must be much smaller than ionization range at 0.9c
        sh = bethe_bloch_and_spallation(0.9, "graphite")
        self.assertGreater(sh["proton_ke_GeV"], 1.2)
        # Nuclear collision length ~ 0.38 m, ionization range ~ 2.8 m
        self.assertLess(sh["nuclear_interaction_length_m"], 0.5)
        self.assertGreater(sh["ionization_range_m"], 2.0)
        self.assertLess(sh["nuclear_interaction_length_m"], sh["ionization_range_m"])

    def test_spacelike_temporal_inversion(self):
        # For U = 2.0c, critical boost is v_c = 1 / 2.0 = 0.5c
        res_sub = spacelike_temporal_inversion_4vector(2.0, 0.4)
        self.assertFalse(res_sub["is_time_reversed"])
        self.assertGreater(res_sub["dt_prime_ratio"], 0.0)
        
        res_super = spacelike_temporal_inversion_4vector(2.0, 0.6)
        self.assertTrue(res_super["is_time_reversed"])
        self.assertLess(res_super["dt_prime_ratio"], 0.0)

if __name__ == "__main__":
    unittest.main()
