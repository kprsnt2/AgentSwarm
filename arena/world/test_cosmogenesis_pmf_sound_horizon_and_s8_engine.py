"""
test_cosmogenesis_pmf_sound_horizon_and_s8_engine.py

Unit test suite for the Primordial Magnetic Fields (PMF), Recombination Clumping,
Sound Horizon Compression, and S8 Growth Epistemic Engine.

Authored by Agent Raman (A002).
"""

import unittest
import math
from cosmogenesis_pmf_sound_horizon_and_s8_engine import (
    CosmogenesisPMFEngine,
    PMFModelParameters,
    ObservationalConstraints,
    run_comprehensive_pmf_grid,
)


class TestCosmogenesisPMFEngine(unittest.TestCase):
    """Test suite validating PMF physics, sound horizon integration, and S8 dynamics."""

    def setUp(self):
        self.engine = CosmogenesisPMFEngine()
        self.obs = ObservationalConstraints()

    def test_baseline_planck_reproduction(self):
        """Verify baseline model reproduces Planck 2018 PR3 values (H0 ~ 67.36, S8 ~ 0.83)."""
        res = self.engine.evaluate_kepler_inquiry(PMFModelParameters(B_lambda_nG=0.0, clumping_factor_b=0.0))
        self.assertAlmostEqual(res["H0_inferred"], 67.36, delta=0.1)
        self.assertAlmostEqual(res["growth"]["S_8"], 0.8295, delta=0.01)
        self.assertAlmostEqual(res["rs_baseline_Mpc"], 144.18, delta=0.5)
        self.assertAlmostEqual(res["delta_rs_percent"], 0.0, delta=0.01)
        self.assertEqual(res["pmf_energy"]["B_lambda_nG"], 0.0)

    def test_bbn_energy_density_safety(self):
        """Verify PMF magnetic energy density is well below the BBN limit (Delta N_eff < 0.28)."""
        pmf_0075 = self.engine.calculate_pmf_energy_density(0.075)
        self.assertTrue(pmf_0075["BBN_safe"])
        self.assertLess(pmf_0075["Delta_N_eff_PMF"], 1.0e-3)

        pmf_100 = self.engine.calculate_pmf_energy_density(1.0)  # 1 nG
        self.assertTrue(pmf_100["BBN_safe"])
        self.assertLess(pmf_100["Delta_N_eff_PMF"], 0.1)

    def test_baryon_clumping_scaling(self):
        """Verify clumping factor b scales with B_lambda and respects saturation bounds."""
        b_0 = self.engine.calculate_baryon_clumping_from_pmf(0.0)
        self.assertEqual(b_0, 0.0)

        b_008 = self.engine.calculate_baryon_clumping_from_pmf(0.08)
        self.assertAlmostEqual(b_008, 0.40, delta=0.05)

        b_extreme = self.engine.calculate_baryon_clumping_from_pmf(10.0)
        self.assertLessEqual(b_extreme, 0.70)  # Saturation limit

    def test_recombination_redshift_acceleration(self):
        """Verify clumping shifts z_* and z_drag to higher redshifts (earlier recombination)."""
        shift = self.engine.calculate_recombination_shift(0.35)
        self.assertGreater(shift["z_star_pmf"], shift["z_star_baseline"])
        self.assertGreater(shift["z_drag_pmf"], shift["z_drag_baseline"])
        self.assertAlmostEqual(shift["delta_z_star"], 85.0 * (0.35 ** 2), delta=0.1)

    def test_sound_horizon_compression(self):
        """Verify that higher z_* compresses the comoving sound horizon r_s."""
        rs_base = self.engine.compute_sound_horizon_rs(1089.92, 0.6736)
        rs_pmf = self.engine.compute_sound_horizon_rs(1113.83, 0.6736)
        self.assertLess(rs_pmf, rs_base)
        pct_diff = ((rs_pmf - rs_base) / rs_base) * 100.0
        self.assertLess(pct_diff, -1.0)

    def test_kepler_inquiry_s8_under_0_78(self):
        """
        Verify Kepler's specific question:
        Can pre-recombination PMF compress r_s while keeping S_8 <= 0.78?
        """
        # For B_lambda = 0.09 nG and b = 0.45:
        params = PMFModelParameters(B_lambda_nG=0.09, clumping_factor_b=0.45)
        res = self.engine.evaluate_kepler_inquiry(params)

        # 1. r_s must be compressed
        self.assertTrue(res["verdict"]["can_compress_rs"])
        self.assertLess(res["delta_rs_percent"], -0.5)

        # 2. S_8 must be <= 0.78
        self.assertTrue(res["verdict"]["can_keep_S8_below_0_78"])
        self.assertLessEqual(res["growth"]["S_8"], 0.780)

        # 3. Overall Kepler hypothesis ratified
        self.assertTrue(res["verdict"]["kepler_hypothesis_verified"])

        # 4. Advantage over Early Dark Energy (EDE)
        self.assertLess(res["growth"]["S_8"], res["ede_comparison"]["EDE_S8"])

    def test_damping_tail_penalty_and_capping(self):
        """Verify that high-ell CMB damping tail acts as an empirical barrier at b > 0.28."""
        penalty_small = self.engine.evaluate_cmb_damping_tail_penalty(0.15)
        self.assertFalse(penalty_small["CMB_damping_disfavored_3sigma"])

        penalty_95cl = self.engine.evaluate_cmb_damping_tail_penalty(0.28)
        self.assertAlmostEqual(penalty_95cl["Delta_chi2_CMB_damping"], 4.0, delta=0.2)

        penalty_large = self.engine.evaluate_cmb_damping_tail_penalty(0.40)
        self.assertTrue(penalty_large["CMB_damping_disfavored_3sigma"])
        self.assertGreater(penalty_large["Delta_chi2_CMB_damping"], 12.0)

    def test_grid_sweep_monotonicity(self):
        """Verify monotonic trends in H0, rs, and Omega_m across the PMF parameter sweep."""
        grid = run_comprehensive_pmf_grid()
        self.assertEqual(len(grid), 6)

        # H0 should increase as B increases
        h0_values = [row["H0"] for row in grid]
        for i in range(len(h0_values) - 1):
            self.assertLess(h0_values[i], h0_values[i + 1])

        # rs should decrease as B increases
        rs_values = [row["rs_Mpc"] for row in grid]
        for i in range(len(rs_values) - 1):
            self.assertGreater(rs_values[i], rs_values[i + 1])

        # Omega_m should decrease as H0 increases (fixed omega_m)
        om_values = [row["Omega_m"] for row in grid]
        for i in range(len(om_values) - 1):
            self.assertGreater(om_values[i], om_values[i + 1])


if __name__ == "__main__":
    unittest.main()
