"""Unit tests for the Origin of the Universe Grand Consilience and Trans-Planckian Closure Engine.

Agent: Kepler (A001) | Generation: 0 | Domain: Origin of the Universe (Cosmogenesis)
Epistemic Class: Empirical Cosmology, Non-Perturbative Quantum Gravity, and Observational Verification
"""

import unittest
import math
from origin_of_universe_grand_consilience_and_transplanckian_closure_engine import (
    C, G_0, HBAR, K_B, E_PL_GEV, L_PL_M, RHO_PL_SI,
    T0_CMB_K, Y_P_BBN_OBSERVED, SIGMA_Y_P_OBSERVED, D_OVER_H_BBN_OBSERVED,
    H0_CMB_PLANCK, H0_LOCAL_SHOES,
    SorkinEverpresentLambdaBBNAdjudicator,
    AsymptoticSafetyAndStarobinskyAttractor,
    MasterCosmogenesisConsilienceMatrix,
    run_grand_consilience_validation
)


class TestGrandConsilienceEngine(unittest.TestCase):
    """Test suite verifying mathematical rigor and observational consilience of the engine."""

    def test_01_established_ground_truth_constants(self):
        """Validates fundamental Planck constants and established cosmological ground truths."""
        self.assertAlmostEqual(T0_CMB_K, 2.72548, places=4)
        self.assertAlmostEqual(Y_P_BBN_OBSERVED, 0.245, places=3)
        self.assertAlmostEqual(D_OVER_H_BBN_OBSERVED, 2.54e-5, places=6)
        self.assertAlmostEqual(H0_CMB_PLANCK, 67.36, places=2)
        self.assertAlmostEqual(H0_LOCAL_SHOES, 73.04, places=2)
        
        # Verify Planck energy scale is ~ 1.22e19 GeV
        self.assertTrue(1.2e19 < E_PL_GEV < 1.25e19)
        # Verify Planck length is ~ 1.62e-35 m
        self.assertTrue(1.6e-35 < L_PL_M < 1.63e-35)
        # Verify Planck density is ~ 5.15e96 kg/m^3
        self.assertTrue(5.0e96 < RHO_PL_SI < 5.3e96)

    def test_02_standard_bbn_helium_synthesis(self):
        """Validates that standard SBBN without early dark energy reproduces observed Helium-4."""
        res = SorkinEverpresentLambdaBBNAdjudicator.calculate_freezeout_and_helium(omega_lambda_early=0.0)
        self.assertAlmostEqual(res["h_acceleration_factor"], 1.0, places=4)
        self.assertAlmostEqual(res["t_freeze_mev"], 0.733, places=3)
        self.assertTrue(0.244 < res["predicted_y_p_helium"] < 0.246)
        self.assertFalse(res["is_ruled_out_by_bbn"])
        self.assertLess(abs(res["tension_sigma"]), 1.0)

    def test_03_sorkin_everpresent_lambda_bbn_falsification(self):
        """Verifies that unsuppressed Sorkin everpresent dark energy is catastrophically ruled out by BBN."""
        res = SorkinEverpresentLambdaBBNAdjudicator.calculate_freezeout_and_helium(omega_lambda_early=0.6847)
        # Expansion accelerated by ~ 1.78x
        self.assertTrue(1.7 < res["h_acceleration_factor"] < 1.85)
        # Freezeout temperature shifts from 0.733 MeV to ~ 0.89 MeV
        self.assertTrue(0.85 < res["t_freeze_mev"] < 0.92)
        # Predicted helium abundance exceeds 34%
        self.assertTrue(res["predicted_y_p_helium"] > 0.34)
        # Tension with observation exceeds 30 sigma
        self.assertTrue(res["tension_sigma"] > 30.0)
        self.assertTrue(res["is_ruled_out_by_bbn"])

    def test_04_early_dark_energy_bounds(self):
        """Validates early dark energy evaluation and Planck CMB limits."""
        bounds = SorkinEverpresentLambdaBBNAdjudicator.evaluate_early_dark_energy_bounds()
        self.assertIn("standard_bbn", bounds)
        self.assertIn("everpresent_lambda", bounds)
        self.assertEqual(bounds["planck_cmb_limit_omega_ede"], 0.02)
        self.assertTrue(bounds["everpresent_lambda"]["is_ruled_out_by_bbn"])

    def test_05_asymptotic_safety_starobinsky_observables(self):
        """Validates the derivation of Starobinsky inflation observables from Asymptotically Safe R^2 gravity."""
        res = AsymptoticSafetyAndStarobinskyAttractor.compute_starobinsky_observables(n_efolds=55.0)
        # n_s = 1 - 2/55 = 53/55 ~ 0.9636
        self.assertAlmostEqual(res["scalar_spectral_index_ns"], 53.0 / 55.0, places=4)
        self.assertTrue(res["matches_planck_ns"])
        # r = 12 / 55^2 = 12 / 3025 ~ 0.003967
        self.assertAlmostEqual(res["tensor_to_scalar_ratio_r"], 12.0 / 3025.0, places=5)
        # Must be detectable by LiteBIRD (sensitivity 0.001)
        self.assertTrue(res["is_detectable_by_litebird"])

    def test_06_frg_matter_stability_evaluation(self):
        """Validates Functional Renormalization Group stability index for Standard Model matter content."""
        res = AsymptoticSafetyAndStarobinskyAttractor.evaluate_frg_matter_stability(
            n_scalars=4, n_weyl_fermions=48, n_vectors=12
        )
        self.assertIn("stability_index", res)
        self.assertIsInstance(res["has_real_fixed_point"], bool)
        self.assertEqual(res["n_weyl_fermions"], 48)

    def test_07_master_open_problems_structure(self):
        """Verifies that the master open problems matrix contains all 8 required canonical problems."""
        problems = MasterCosmogenesisConsilienceMatrix.get_master_open_problems()
        self.assertEqual(len(problems), 8)
        required_keys = [
            "id", "title", "domain", "epistemic_status", "theoretical_barrier",
            "what_current_theory_fails_to_explain", "established_ground_truth",
            "resolving_observation", "decisive_falsification_threshold", "target_facilities"
        ]
        for prob in problems:
            for k in required_keys:
                self.assertIn(k, prob, f"Missing key {k} in problem {prob['id']}")
            self.assertTrue(len(prob["target_facilities"]) > 0)
            self.assertTrue(len(prob["decisive_falsification_threshold"]) > 20)

    def test_08_grand_consilience_validation_runner(self):
        """Validates that the comprehensive runner returns status SUCCESS and consistent metrics."""
        summary = run_grand_consilience_validation()
        self.assertEqual(summary["status"], "SUCCESS")
        self.assertEqual(summary["canonical_open_problems_count"], 8)
        self.assertTrue(summary["everpresent_lambda_tension_sigma"] > 30.0)
        self.assertAlmostEqual(summary["starobinsky_ns"], 53.0 / 55.0, places=4)


if __name__ == "__main__":
    unittest.main()
