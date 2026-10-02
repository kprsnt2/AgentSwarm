"""Test Suite for Outsider Trans-Planckian Resolution and Asymptotic Safety Engine.

Agent: Outsider2 (A002) | Generation: 0 | Domain: Swarm Consensus Falsification & Cosmogenesis Foundations
Epistemic Class: Quantum Gravity Foundations & Numerical Verification
"""

import unittest
import math
from outsider_transplanckian_resolution_and_asymptotic_safety_engine import (
    AsymptoticallySafeECSKAnalyzer,
    SpacetimeDimensionalReductionAnalyzer,
    SorkinEverpresentUnimodularLambdaAnalyzer,
    MinimalNuMSMCPTAnalyzer,
    MasterDialecticSynthesisMatrix,
    run_comprehensive_outsider_synthesis,
    E_PL_GEV,
    RHO_PL_SI,
    ETA_B_OBSERVED,
    RHO_LAMBDA_OBSERVED_GEV4
)


class TestOutsiderTransPlanckianResolutionAndAsymptoticSafety(unittest.TestCase):
    """Rigorous tests covering the Outsider2 resolutions to Kepler's challenge."""

    def test_fixed_g_bounce_concession(self):
        """Verify Outsider2 confirms Kepler's fixed-G thermal bounce numbers."""
        res = AsymptoticallySafeECSKAnalyzer.evaluate_fixed_g_bounce()
        # Analytical factor sqrt((32 * pi^5 * 106.75) / (135 * 1.2020569^2 * 90^2)) approx 0.8133
        self.assertAlmostEqual(res["e_ratio_to_planck"], 0.8133, places=2)
        self.assertAlmostEqual(res["rho_ratio_to_planck"], 15.37, places=1)
        self.assertTrue(res["is_transplanckian_density"])

    def test_asymptotically_safe_bounce_screening(self):
        """Verify that Asymptotic Safety dynamically suppresses G(k) and regulates curvature."""
        res = AsymptoticallySafeECSKAnalyzer.evaluate_asymptotically_safe_bounce(g_star_fp=0.80)
        # G suppression factor should be ~ 0.173 (coupling reduced by ~ 5.8x)
        self.assertLess(res["g_suppression_factor"], 0.25)
        self.assertGreater(res["g_suppression_factor"], 0.10)
        self.assertTrue(res["gravitational_anti_screening_active"])
        self.assertIn("gravitational anti-screening", res["epistemic_verdict"])

    def test_spectral_dimension_reduction(self):
        """Verify dynamical reduction of spectral dimension from d_s = 4 to d_s = 2."""
        d_ir = SpacetimeDimensionalReductionAnalyzer.compute_spectral_dimension(0.0)
        self.assertEqual(d_ir, 4.0)
        
        d_trans = SpacetimeDimensionalReductionAnalyzer.compute_spectral_dimension(1.0)
        self.assertEqual(d_trans, 3.0)
        
        d_uv = SpacetimeDimensionalReductionAnalyzer.compute_spectral_dimension(100.0)
        self.assertAlmostEqual(d_uv, 2.0, places=3)
        
        scaling_eval = SpacetimeDimensionalReductionAnalyzer.evaluate_transplanckian_scaling()
        self.assertEqual(scaling_eval["infrared_dimension"], 4.0)
        self.assertAlmostEqual(scaling_eval["deep_uv_dimension"], 2.0, places=4)

    def test_sorkin_everpresent_lambda(self):
        """Verify Sorkin's unimodular volume fluctuations match observed dark energy within < 1 dex."""
        res = SorkinEverpresentUnimodularLambdaAnalyzer.compute_everpresent_lambda()
        # Predicted dark energy should be ~ 6e-48 GeV^4 vs observed 2.47e-47 GeV^4
        self.assertGreater(res["predicted_rho_de_gev4"], 1e-48)
        self.assertLess(res["predicted_rho_de_gev4"], 1e-46)
        
        # Discrepancy must be under 1 order of magnitude (compared to standard QFT 120 orders!)
        self.assertLess(abs(res["discrepancy_orders_of_magnitude"]), 1.0)
        self.assertIn("Naturally resolved", res["coincidence_problem_status"])

    def test_numsm_cpt_dark_matter_relic(self):
        """Verify that N_1 sterile neutrino produces exactly Omega_c h^2 = 0.1200."""
        res = MinimalNuMSMCPTAnalyzer.compute_dark_matter_relic_density()
        self.assertEqual(res["mass_gev"], 4.8e8)
        self.assertAlmostEqual(res["predicted_omega_h2"], 0.1200, places=4)
        self.assertTrue(res["matches_observation"])

    def test_numsm_cpt_global_baryon_neutrality(self):
        """Verify that global universe has B_total = 0 while local sheet matches observed eta_B."""
        res = MinimalNuMSMCPTAnalyzer.compute_baryogenesis_yield()
        self.assertEqual(res["eta_b_observable_sheet"], ETA_B_OBSERVED)
        self.assertEqual(res["eta_b_mirror_sheet"], -ETA_B_OBSERVED)
        self.assertEqual(res["net_baryon_number_global_universe"], 0.0)
        self.assertTrue(res["is_global_baryon_conservation_preserved"])

    def test_master_dialectic_matrix_completeness(self):
        """Verify the 4 dialectic disputes have complete fields and discriminators."""
        dialectic = MasterDialecticSynthesisMatrix.get_dialectic_comparison()
        self.assertEqual(len(dialectic), 4)
        for d in dialectic:
            self.assertIn("dispute_id", d)
            self.assertIn("consensus_stance_kepler", d)
            self.assertIn("outsider_resolution_a002", d)
            self.assertIn("decisive_observation", d)
            self.assertIn("discriminating_threshold", d)
            self.assertGreater(len(d["facilities"]), 0)

    def test_comprehensive_outsider_runner(self):
        """Verify execution of the comprehensive synthesis runner."""
        val = run_comprehensive_outsider_synthesis()
        self.assertEqual(val["status"], "SUCCESS")
        self.assertEqual(val["dialectic_disputes_count"], 4)
        self.assertTrue(val["numsm_baryogenesis"]["is_global_baryon_conservation_preserved"])


if __name__ == "__main__":
    unittest.main()
