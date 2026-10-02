"""Unit Test Suite for Quantum Foundations and Holographic Cosmogenesis Engine.

Agent: Kepler (A001) | Generation: 0 | Domain: Origin of the Universe (Cosmogenesis)
Epistemic Class: Empirical Precision Cosmology & Quantum Foundations
Date: October 2026
"""

import unittest
import math
from quantum_foundations_and_holographic_cosmogenesis_engine import (
    PageWoottersDecoherenceAnalyzer,
    KibbleZurekGraphityDefectAnalyzer,
    HolographicDarkEnergyAndCausalSetAnalyzer,
    TransPlanckianCensorshipAndSwamplandAnalyzer,
    MasterOpenProblemsResolvingMatrix,
    GrandFoundationalConsilienceBenchmark,
    C, G, HBAR, K_B, L_PL, T_PL, M_PL, RHO_PL, T_PL_KELVIN,
    H0_PLANCK_SI, H0_SHOES_SI, OMEGA_LAMBDA_PLANCK, RHO_CRIT_SI, AGE_OF_UNIVERSE_SEC
)


class TestQuantumFoundationsAndHolographicEngine(unittest.TestCase):

    def test_fundamental_planck_units(self):
        """Verify dimensional precision of fundamental Planck constants."""
        self.assertAlmostEqual(C, 299792458.0, places=1)
        self.assertGreater(L_PL, 1.61e-35)
        self.assertLess(L_PL, 1.62e-35)
        self.assertGreater(T_PL, 5.38e-44)
        self.assertLess(T_PL, 5.40e-44)
        self.assertGreater(M_PL, 2.17e-8)
        self.assertLess(M_PL, 2.18e-8)
        self.assertGreater(T_PL_KELVIN, 1.41e32)
        self.assertLess(T_PL_KELVIN, 1.42e32)

    def test_holographic_time_uncertainty(self):
        """Verify Lloyd-Ng-van Dam holographic time uncertainty over cosmic age."""
        res = PageWoottersDecoherenceAnalyzer.compute_holographic_time_uncertainty(AGE_OF_UNIVERSE_SEC)
        # delta_t_min should be ~ 1.08e-23 s
        self.assertGreater(res["holographic_time_uncertainty_sec"], 1.0e-23)
        self.assertLess(res["holographic_time_uncertainty_sec"], 1.2e-23)
        self.assertTrue(res["clock_survives_collapse"])
        self.assertGreater(res["max_computational_operations"], 1.0e40)

    def test_intrinsic_gravitational_decoherence(self):
        """Verify Gambini-Porto-Pullin / Marletto-Vedral gravitational Lindblad decoherence."""
        # A macroscopic energy superposition at GUT scale over 1e-35 s
        res = PageWoottersDecoherenceAnalyzer.compute_intrinsic_gravitational_decoherence(
            energy_spread_gev=1e16,
            time_elapsed_sec=1e-35
        )
        self.assertGreater(res["decoherence_rate_hz"], 1.0e35)
        self.assertTrue(res["is_macroscopically_classical"])
        self.assertLess(res["quantum_purity"], 1.0e-50)

        # A microscopic single photon superposition should maintain high purity
        res_micro = PageWoottersDecoherenceAnalyzer.compute_intrinsic_gravitational_decoherence(
            energy_spread_gev=1e-9,  # 1 eV
            time_elapsed_sec=1.0     # 1 second
        )
        self.assertAlmostEqual(res_micro["quantum_purity"], 1.0, places=5)
        self.assertFalse(res_micro["is_macroscopically_classical"])

    def test_kibble_zurek_graphity_overclosure(self):
        """Verify that unconstrained Quantum Graphity suffers catastrophic defect overclosure."""
        res = KibbleZurekGraphityDefectAnalyzer.evaluate_graphity_quench(
            quench_time_seconds=T_PL,
            critical_exponent_nu=0.5,
            dynamic_critical_exponent_z=1.0
        )
        # Omega_defect must be >> 1 (catastrophic overclosure ~ 10^122)
        self.assertTrue(res["is_catastrophically_overclosed"])
        self.assertGreater(res["omega_defect_relative_to_rhocrit"], 1.0e120)
        self.assertAlmostEqual(res["freeze_out_correlation_length_l_pl"], 1.0, places=2)

    def test_cohen_kaplan_nelson_holographic_dark_energy(self):
        """Verify Cohen-Kaplan-Nelson UV/IR bound reproduces Dark Energy within factor of order unity."""
        hubble_radius = C / H0_PLANCK_SI
        res = HolographicDarkEnergyAndCausalSetAnalyzer.evaluate_cohen_kaplan_nelson_bound(hubble_radius)
        # Ratio to observed dark energy should be between 1.0 and 2.0
        self.assertTrue(res["order_of_magnitude_agreement"])
        self.assertGreater(res["ratio_to_observed_de"], 1.2)
        self.assertLess(res["ratio_to_observed_de"], 1.8)
        self.assertAlmostEqual(res["ratio_to_observed_de"], 1.460, places=2)

    def test_sorkin_causal_set_poisson_fluctuation(self):
        """Verify Sorkin's unimodular Causal Set Poisson fluctuation of Lambda matches observation."""
        hubble_radius = C / H0_PLANCK_SI
        # In standard 4-volume V_4 = R_H^3 * (c * t_0)
        v_4 = (hubble_radius**3) * (C * AGE_OF_UNIVERSE_SEC)
        res = HolographicDarkEnergyAndCausalSetAnalyzer.evaluate_sorkin_causal_set_fluctuation(v_4)
        self.assertTrue(res["order_of_magnitude_agreement"])
        self.assertAlmostEqual(res["ratio_to_observed"], 0.500, places=2)
        self.assertGreater(res["delta_lambda_planck_units"], 1.0e-124)
        self.assertLess(res["delta_lambda_planck_units"], 1.0e-120)

    def test_trans_planckian_censorship_conjecture(self):
        """Verify Bedroya-Vafa TCC bounds on inflation energy scale and tensor-to-scalar ratio."""
        res_60 = TransPlanckianCensorshipAndSwamplandAnalyzer.evaluate_tcc_bounds(n_efolds=60.0)
        # r_max must be <= 10^-30
        self.assertLess(res_60["r_max_allowed_by_tcc"], 1.0e-30)
        self.assertFalse(res_60["is_high_scale_compatible"])
        # High scale inflation r >= 0.001 is ruled out if TCC holds
        self.assertLess(res_60["r_max_allowed_by_tcc"], res_60["litebird_sensitivity"])

    def test_master_open_problems_catalog(self):
        """Verify that exactly 8 canonical open problems are comprehensively cataloged."""
        problems = MasterOpenProblemsResolvingMatrix.get_all_problems()
        self.assertEqual(len(problems), 8)
        problem_ids = [p.problem_id for p in problems]
        self.assertEqual(problem_ids, [f"PROB-0{i}" for i in range(1, 9)])
        for prob in problems:
            self.assertTrue(len(prob.target_assumption) > 10)
            self.assertTrue(len(prob.fatal_bottleneck) > 15)
            self.assertTrue(len(prob.decisive_observation) > 15)
            self.assertTrue(len(prob.target_missions) > 5)

    def test_grand_benchmark_pipeline(self):
        """Verify the integrated grand foundational consilience benchmark runs cleanly."""
        res = GrandFoundationalConsilienceBenchmark.run_master_analysis()
        self.assertIn("holographic_time_uncertainty", res)
        self.assertIn("primordial_gravitational_decoherence", res)
        self.assertIn("kibble_zurek_graphity_overclosure", res)
        self.assertIn("cohen_kaplan_nelson_dark_energy", res)
        self.assertIn("sorkin_causal_set_fluctuation", res)
        self.assertIn("trans_planckian_censorship", res)
        self.assertEqual(res["total_open_problems_cataloged"], 8)


if __name__ == "__main__":
    unittest.main()
