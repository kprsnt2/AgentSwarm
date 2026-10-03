"""
test_cosmogenesis_ede_sound_horizon_and_s8_tension_engine.py

Unit test suite verifying the Early Dark Energy (EDE) sound horizon compression,
Hubble tension resolution, and S_8 weak lensing structure growth tension catch-22.
Uses standard library unittest.
"""

import unittest
import math
from cosmogenesis_ede_sound_horizon_and_s8_tension_engine import (
    EarlyDarkEnergyS8Engine,
    EDEParameters,
    ConsensusBaseline,
    EmpiricalObservations
)


class TestEarlyDarkEnergyS8Engine(unittest.TestCase):

    def setUp(self):
        self.engine = EarlyDarkEnergyS8Engine()

    def test_baseline_lcdm_recovery(self):
        """Verify baseline recovery when f_ede = 0."""
        ede_zero = EDEParameters(f_ede=0.00)
        sol = self.engine.solve_inferred_h0_for_ede(ede_zero)
        self.assertAlmostEqual(sol["H0_solved"], 67.36, places=2)
        self.assertAlmostEqual(sol["r_s_mpc"], 144.18, delta=0.5)

        s8_sol = self.engine.evaluate_s8_growth_cascade(sol)
        self.assertAlmostEqual(s8_sol["sigma_8"], 0.8111, delta=0.01)
        self.assertAlmostEqual(s8_sol["S_8"], 0.830, delta=0.01)

    def test_sound_horizon_compression_and_h0_inversion(self):
        """Verify that f_ede = 0.10 compresses r_s and raises H0 to resolve tension with SH0ES."""
        ede_10 = EDEParameters(f_ede=0.10, z_c=3500.0)
        sol = self.engine.solve_inferred_h0_for_ede(ede_10)

        # Sound horizon must decrease by 4% to 6.5%
        self.assertTrue(sol["r_s_mpc"] < self.engine.base.r_s_star)
        self.assertTrue(-6.5 < sol["pct_rs_reduction"] < -4.0)

        # Inferred H0 must reach >= 72.0 km/s/Mpc
        self.assertTrue(sol["H0_solved"] >= 72.0)
        # Residual tension with SH0ES must drop below 1.0 sigma
        self.assertTrue(sol["residual_H0_tension_sigma"] < 1.0)

    def test_s8_growth_cascade_and_aggravation(self):
        """Verify that EDE aggravates S_8 structure growth tension to > 3.0 sigma."""
        ede_10 = EDEParameters(f_ede=0.10, z_c=3500.0)
        sol = self.engine.solve_inferred_h0_for_ede(ede_10)
        s8_sol = self.engine.evaluate_s8_growth_cascade(sol)

        # sigma_8 must increase due to early ISW compensation (omega_cdm) and Silk damping compensation (n_s)
        self.assertTrue(s8_sol["sigma_8"] > 0.835)
        # S_8 must stay elevated > 0.825
        self.assertTrue(s8_sol["S_8"] > 0.825)
        # Tension with combined cosmic shear (0.766) must exceed 3.0 sigma
        self.assertTrue(s8_sol["s8_tension_combined_sigma"] > 3.0)
        self.assertTrue(s8_sol["aggravates_s8_tension"])

    def test_catch22_no_go_theorem(self):
        """Verify that NO canonical EDE model simultaneously achieves H0 >= 72 and S_8 <= 0.780."""
        grid_results = self.engine.compute_joint_consilience_catch22()
        for res in grid_results:
            # Catch-22: satisfies_h0_and_s8 must be False everywhere
            self.assertFalse(res["satisfies_h0_and_s8"])
            if res["H0"] >= 72.0:
                self.assertTrue(res["S_8"] > 0.825)

    def test_extended_resolutions_evaluation(self):
        """Verify evaluation of physical mechanisms breaking the EDE-S8 Catch-22."""
        ext = self.engine.evaluate_extended_resolutions()

        # Decaying Dark Matter (DCDM + EDE) successfully suppresses S_8 to WL bounds
        self.assertTrue(ext["dcdm_ede"]["breaks_catch22"])
        self.assertTrue(ext["dcdm_ede"]["S_8"] < 0.785)
        self.assertTrue(ext["dcdm_ede"]["residual_S8_tension_sigma"] < 1.0)

        # Massive neutrinos under DESI 2024 bound cannot break the catch-22
        self.assertFalse(ext["massive_neutrino_ede"]["breaks_catch22"])
        self.assertTrue(ext["massive_neutrino_ede"]["max_sigma8_suppression_pct"] < 1.0)


if __name__ == "__main__":
    unittest.main()
