"""
test_cosmogenesis_liturgy_breaker_and_trilemma_engine.py

Comprehensive Test Suite for Cosmogenesis Liturgy Breaker, Sound Horizon
Trilemma, Trans-Planckian Censorship, and Quantum Geometric Bounce.
"""

import unittest
import math
from cosmogenesis_liturgy_breaker_and_trilemma_engine import (
    LambdaCDMBaseline,
    CosmogenesisAnalyzer,
    C_LIGHT_KM_S,
    M_PLANCK_GEV,
)


class TestCosmogenesisLiturgyBreaker(unittest.TestCase):
    def setUp(self):
        self.baseline = LambdaCDMBaseline()
        self.analyzer = CosmogenesisAnalyzer(self.baseline)

    def test_baseline_parameters(self):
        """Verify standard Lambda-CDM parameter relationships."""
        self.assertAlmostEqual(self.baseline.H0, 67.4, places=1)
        self.assertAlmostEqual(self.baseline.Omega_b, 0.04924, places=3)
        self.assertAlmostEqual(self.baseline.Omega_c, 0.26415, places=3)
        self.assertAlmostEqual(self.baseline.Omega_m, 0.3134, places=2)
        self.assertTrue(0.68 < self.baseline.Omega_Lambda < 0.69)
        self.assertTrue(0.81 < self.baseline.S_8 < 0.85)

    def test_expansion_rate(self):
        """Test H(z) monotonic increase with redshift."""
        h0 = self.analyzer.hubble_at_z(0.0)
        h1 = self.analyzer.hubble_at_z(1.0)
        h_star = self.analyzer.hubble_at_z(1089.0)
        self.assertAlmostEqual(h0, 67.4, places=2)
        self.assertGreater(h1, h0)
        self.assertGreater(h_star, h1)

    def test_acoustic_scale_geometry(self):
        """Verify CMB angular scale theta_* matches Planck 0.0104 within 0.5%."""
        geom = self.analyzer.evaluate_acoustic_scale()
        self.assertTrue(142.0 < geom["r_s_Mpc"] < 146.0)
        self.assertTrue(13500.0 < geom["D_M_Mpc"] < 14200.0)
        self.assertAlmostEqual(geom["theta_star"], 0.0104, delta=0.0002)
        self.assertTrue(300.0 < geom["l_A"] < 305.0)

    def test_hubble_tension_sound_horizon_shrinkage(self):
        """Verify sound horizon must shrink by ~7% to match SH0ES."""
        result = self.analyzer.evaluate_hubble_tension_and_sound_horizon_shrinkage(H0_shoes=73.04)
        self.assertAlmostEqual(result["delta_H0"], 5.64, places=2)
        self.assertGreater(result["tension_sigma"], 4.5)
        self.assertTrue(-8.5 < result["delta_r_s_pct"] < -6.5)

    def test_early_dark_energy_trilemma(self):
        """Verify EDE exacerbates the S8 tension."""
        geom = self.analyzer.evaluate_acoustic_scale()
        res = self.analyzer.evaluate_early_dark_energy_trilemma(f_ede=0.10)
        self.assertLess(res["r_s_ede_Mpc"], geom["r_s_Mpc"])
        self.assertGreater(res["S_8_ede"], res["S_8_planck"])
        self.assertGreater(res["tension_ede_sigma"], res["tension_planck_sigma"])

    def test_trans_planckian_censorship(self):
        """Verify TCC limits single-field slow-roll inflation e-folds to < 15 for observable r."""
        tcc = self.analyzer.evaluate_trans_planckian_censorship(r_tensor=0.036, N_required=60.0)
        self.assertLess(tcc["N_max_TCC"], 15.0)
        self.assertGreater(tcc["delta_N_discrepancy"], 45.0)
        self.assertTrue(tcc["swampland_distance_violated"])
        self.assertLess(tcc["r_max_TCC_allowed"], 1e-30)

    def test_quantum_geometric_bounce(self):
        """Verify LQC eliminates singularity and yields finite maximum density."""
        bounce = self.analyzer.evaluate_quantum_geometric_bounce()
        self.assertTrue(bounce["singularity_eliminated"])
        self.assertGreater(bounce["rho_crit_bounce_kg_m3"], 1e95)
        self.assertLess(bounce["a_min_bounce"], 1e-30)
        self.assertGreater(bounce["a_min_bounce"], 0.0)

    def test_bbn_helium_anchor(self):
        """Verify primordial nucleosynthesis helium fraction matches empirical anchor."""
        bbn = self.analyzer.evaluate_bbn_helium_anchor()
        self.assertAlmostEqual(bbn["Y_p_calculated"], 0.247, delta=0.03)
        self.assertTrue(bbn["np_freeze"] < 0.25)
        self.assertTrue(bbn["np_at_nucleosynthesis"] < bbn["np_freeze"])


if __name__ == "__main__":
    unittest.main()
