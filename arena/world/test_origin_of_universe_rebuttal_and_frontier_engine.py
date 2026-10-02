"""Test Suite for Origin of the Universe Rebuttal and Frontier Engine.

Agent: Kepler (A001) | Generation: 0 | Domain: Origin of the Universe (Cosmogenesis)
Epistemic Class: Empirical Cosmology & Mathematical Verification
"""

import unittest
import math
from origin_of_universe_rebuttal_and_frontier_engine import (
    RelativisticECSKBounceAnalyzer,
    CPTSymmetricBSMAnalyzer,
    UnimodularAndConformalAnalyzer,
    CosmogenesisResolvingObservationsMatrix,
    run_comprehensive_validation,
    E_PL_GEV,
    RHO_PL_SI,
    T0_CMB_K,
    Y_P_BBN,
    D_OVER_H_BBN,
    H0_CMB_PLANCK,
    H0_LOCAL_SHOES,
    H0_TENSION_SIGMA
)


class TestOriginOfUniverseRebuttalAndFrontierEngine(unittest.TestCase):
    """Rigorous tests covering all physical derivations and matrix deliverables."""

    def test_established_ground_truth_constants(self):
        """Verify that ground truth constants match observational benchmarks."""
        self.assertAlmostEqual(T0_CMB_K, 2.72548, places=4)
        self.assertAlmostEqual(Y_P_BBN, 0.245, places=3)
        self.assertAlmostEqual(D_OVER_H_BBN, 2.54e-5, places=7)
        self.assertAlmostEqual(H0_CMB_PLANCK, 67.36, places=2)
        self.assertAlmostEqual(H0_LOCAL_SHOES, 73.04, places=2)
        self.assertGreater(H0_TENSION_SIGMA, 4.5)

    def test_cold_nucleon_ecsk_bounce(self):
        """Verify Poplawski cold degenerate nucleon bounce calculation."""
        res = RelativisticECSKBounceAnalyzer.compute_cold_nucleon_bounce()
        self.assertAlmostEqual(res["orders_below_planck_density"], 50.8, places=1)
        self.assertFalse(res["hadrons_exist_at_this_energy"])
        self.assertIn("INVALID", res["physical_validity_for_cosmogenesis"])

    def test_relativistic_thermal_ecsk_bounce(self):
        """Verify analytical derivation of thermal ECSK bounce in early-universe plasma."""
        res = RelativisticECSKBounceAnalyzer.compute_relativistic_thermal_bounce()
        # Analytical factor sqrt((32 * pi^5 * 106.75) / (135 * 1.2020569^2 * 90^2)) approx 0.8133
        self.assertAlmostEqual(res["e_ratio_to_planck"], 0.8133, places=2)
        # Bounce energy must be ~ 9.9e18 GeV (Planckian)
        self.assertGreater(res["e_bounce_gev"], 9.0e18)
        self.assertLess(res["e_bounce_gev"], 1.1e19)
        # Density must exceed Planck density (~ 15 rho_Pl)
        self.assertGreater(res["rho_ratio_to_planck"], 10.0)
        self.assertTrue(res["is_planckian"])
        self.assertTrue(res["quantum_gravity_required"])

    def test_cpt_symmetric_bsm_necessity(self):
        """Verify that Boyle-Finn-Turok model strictly requires BSM physics."""
        res = CPTSymmetricBSMAnalyzer.analyze_bsm_necessity()
        self.assertTrue(res["is_bsm_required"])
        self.assertEqual(res["cpt_universe_requirements"]["right_handed_neutrinos"], 3)
        self.assertEqual(res["cpt_universe_requirements"]["m_n1_gev"], 4.8e8)
        self.assertIn("Type-I Seesaw (BSM)", res["cpt_universe_requirements"]["seesaw_mechanism"])

    def test_cpt_observational_predictions(self):
        """Verify predictions of CPT cosmology (r = 0, normal neutrino ordering)."""
        res = CPTSymmetricBSMAnalyzer.evaluate_cpt_observational_predictions()
        self.assertEqual(res["predicted_tensor_to_scalar_r"], 0.0)
        self.assertAlmostEqual(res["predicted_sum_m_nu_ev"], 0.0587, places=3)
        self.assertLess(res["predicted_sum_m_nu_ev"], res["planck_bao_upper_limit_ev"])

    def test_unimodular_gravity(self):
        """Verify that unimodular gravity decouples vacuum energy but leaves integration constant unexplained."""
        res = UnimodularAndConformalAnalyzer.evaluate_unimodular_gravity()
        self.assertTrue(res["orders_of_magnitude_discrepancy_resolved"])
        self.assertFalse(res["coincidence_problem_resolved"])
        self.assertIn("1.1e-52", res["unexplained_parameter"])

    def test_wetterich_conformal_duality(self):
        """Verify that expanding metric and evolving mass frames are observationally identical."""
        res = UnimodularAndConformalAnalyzer.evaluate_wetterich_conformal_duality(z=3.0)
        self.assertTrue(res["are_frames_observationally_identical"])
        self.assertEqual(res["flrw_time_dilation"], 4.0)
        self.assertEqual(res["wetterich_time_dilation"], 4.0)

    def test_canonical_open_problems_matrix(self):
        """Verify that all 8 canonical open problems have complete fields and resolving observations."""
        problems = CosmogenesisResolvingObservationsMatrix.get_canonical_open_problems()
        self.assertEqual(len(problems), 8)
        
        expected_ids = [f"OP-0{i}" for i in range(1, 9)]
        for p in problems:
            self.assertIn(p["id"], expected_ids)
            self.assertIn("resolving_observation", p)
            self.assertIn("decisive_threshold", p)
            self.assertIn("established_ground_truth", p)
            self.assertGreater(len(p["target_facilities"]), 0)

    def test_comprehensive_validation_function(self):
        """Verify execution of the comprehensive validation runner."""
        val = run_comprehensive_validation()
        self.assertEqual(val["status"], "SUCCESS")
        self.assertEqual(val["open_problems_count"], 8)
        self.assertTrue(val["is_bsm_required_for_cpt"])


if __name__ == "__main__":
    unittest.main()
