"""
test_cosmogenesis_consensus_weakest_assumption_attack_engine.py

Unit test suite verifying the quantitative attacks on the consensus cosmology assumptions.
Uses standard library unittest.
"""

import unittest
import math
from cosmogenesis_consensus_weakest_assumption_attack_engine import WeakestAssumptionAttackEngine


class TestWeakestAssumptionAttackEngine(unittest.TestCase):

    def setUp(self):
        self.engine = WeakestAssumptionAttackEngine()

    def test_hubble_tension_quantification(self):
        res = self.engine.evaluate_hubble_tension()
        self.assertAlmostEqual(res["H0_early"], 67.36, places=2)
        self.assertAlmostEqual(res["H0_late"], 73.04, places=2)
        self.assertAlmostEqual(res["delta_H0"], 5.68, places=2)
        self.assertTrue(4.8 < res["tension_sigma"] < 5.2)

    def test_sound_horizon_deficit(self):
        res = self.engine.evaluate_sound_horizon_deficit()
        self.assertAlmostEqual(res["r_s_planck_mpc"], 147.09, places=2)
        self.assertTrue(135.0 < res["r_s_required_mpc"] < 136.0)
        self.assertTrue(res["percentage_deficit"] < -7.0)
        self.assertTrue(res["tension_sigma"] > 4.5)

    def test_dynamical_dark_energy_breakdown(self):
        res = self.engine.evaluate_dynamical_dark_energy_breakdown(w0=-0.827, wa=-0.750)
        self.assertEqual(res["w0"], -0.827)
        self.assertEqual(res["wa"], -0.750)
        self.assertTrue(res["delta_chi2_from_lcdm"] > 7.0)
        self.assertTrue(res["tension_sigma"] > 2.6)
        self.assertTrue(res["lcdm_falsified_above_2sigma"])
        self.assertIsNotNone(res["phantom_crossing_scale_factor"])
        self.assertTrue(0.0 < res["phantom_crossing_scale_factor"] < 1.0)

    def test_tcc_and_bgv_incompleteness(self):
        res = self.engine.evaluate_tcc_and_bgv_incompleteness(H_inf_gev=1.0e13, e_folds=60.0)
        self.assertTrue(res["violates_tcc"])
        self.assertTrue(res["max_H_inflation_tcc_gev"] < 1.0e-6)
        self.assertTrue(res["bgv_geodesic_incompleteness"])
        self.assertTrue(res["r_tcc_max_bound"] < 1.0e-30)

    def test_early_universe_reconciliation(self):
        res = self.engine.evaluate_early_universe_reconciliation(f_ede=0.10)
        self.assertAlmostEqual(res["sound_horizon_reduction_pct"], 5.0, places=1)
        self.assertTrue(res["inferred_H0_km_s_mpc"] > 70.0)
        self.assertTrue(res["residual_tension_sigma"] < 2.0)


if __name__ == "__main__":
    unittest.main()
