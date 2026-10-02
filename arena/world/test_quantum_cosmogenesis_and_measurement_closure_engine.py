"""Unit test suite for Quantum Cosmogenesis, Measurement Closure, and Singularity Resolution Engine.

Agent: Kepler (A001) | Generation: 0 | Domain: Origin of the Universe (Cosmogenesis)
"""

import unittest
import math
from quantum_cosmogenesis_and_measurement_closure_engine import (
    C, G, HBAR, K_B, L_PL, T_PL, M_PL, E_PL, RHO_PL_ENERGY,
    T_CMB_OBS, H0_PLANCK_KMS_MPC, H0_SHOES_KMS_MPC,
    QuantumMeasurementCosmogenesisAnalyzer,
    WavefunctionOfUniverseAnalyzer,
    PenroseWeylEntropyAnalyzer,
    CosmogenesisMasterDeliverableEngine,
    run_integrated_demonstration,
)


class TestPhysicalConstantsAndPlanckUnits(unittest.TestCase):
    """Verify exact numerical consistency of fundamental Planck scales."""

    def test_speed_of_light_and_constants(self):
        self.assertAlmostEqual(C, 299792458.0, delta=1e-1)
        self.assertAlmostEqual(K_B, 1.380649e-23, delta=1e-29)

    def test_planck_scales(self):
        # L_Pl ~ 1.616e-35 m
        self.assertTrue(1.61e-35 < L_PL < 1.63e-35)
        # t_Pl ~ 5.39e-44 s
        self.assertTrue(5.38e-44 < T_PL < 5.41e-44)
        # M_Pl ~ 2.176e-8 kg
        self.assertTrue(2.17e-8 < M_PL < 2.18e-8)
        # E_Pl ~ 1.956e9 J
        self.assertTrue(1.95e9 < E_PL < 1.96e9)


class TestQuantumMeasurementAnalyzer(unittest.TestCase):
    """Verify squeezing parameter and CSL collapse calculations."""

    def test_squeezing_parameter(self):
        res = QuantumMeasurementCosmogenesisAnalyzer.compute_squeezing_parameter(e_folds_after_horizon=60.0)
        self.assertEqual(res["e_folds_after_horizon"], 60.0)
        self.assertEqual(res["squeezing_parameter_r_k"], 60.0)
        self.assertAlmostEqual(res["quantum_purity"], 1.0)
        # Wigner aspect ratio log10(exp(120)) ~ 52.1
        self.assertTrue(50.0 < res["log10_wigner_aspect_ratio"] < 55.0)
        # Relative quantum dispersion is heavily suppressed
        self.assertTrue(res["quantum_dispersion_ratio"] < 1e-50)

    def test_squeezing_invalid_efolds(self):
        with self.assertRaises(ValueError):
            QuantumMeasurementCosmogenesisAnalyzer.compute_squeezing_parameter(-1.0)

    def test_csl_collapse_modification(self):
        res = QuantumMeasurementCosmogenesisAnalyzer.compute_csl_collapse_modification(
            k_mpc_inv=0.05,
            collapse_rate_gamma=1e-16,
            h_inf_gev=1e13,
        )
        self.assertEqual(res["wavenumber_k_mpc_inv"], 0.05)
        # Multipole ell ~ 0.05 * 14100 = 705
        self.assertAlmostEqual(res["approximate_multipole_ell"], 705.0, delta=10.0)
        self.assertIn("CMB-S4", res["falsification_test"])

    def test_csl_invalid_k(self):
        with self.assertRaises(ValueError):
            QuantumMeasurementCosmogenesisAnalyzer.compute_csl_collapse_modification(k_mpc_inv=0.0)


class TestWavefunctionOfUniverseAnalyzer(unittest.TestCase):
    """Verify Hartle-Hawking vs Vilenkin and String Gas evaluations."""

    def test_wavefunction_probabilities(self):
        res = WavefunctionOfUniverseAnalyzer.compare_wavefunction_probabilities(v_phi_over_m_pl4=1e-12)
        self.assertFalse(res["hh_favors_inflation"])
        self.assertTrue(res["vilenkin_favors_inflation"])
        self.assertFalse(res["hartle_hawking_picard_lefschetz_stable"])
        self.assertTrue(res["vilenkin_picard_lefschetz_stable"])
        self.assertTrue(res["log10_unnormalized_prob_hartle_hawking"] > 0)
        self.assertTrue(res["log10_unnormalized_prob_vilenkin"] < 0)

    def test_wavefunction_invalid_v(self):
        with self.assertRaises(ValueError):
            WavefunctionOfUniverseAnalyzer.compare_wavefunction_probabilities(0.0)

    def test_string_gas_cosmology(self):
        # 3 dimensions
        res3 = WavefunctionOfUniverseAnalyzer.evaluate_string_gas_cosmology(spatial_dimensions=3)
        self.assertTrue(res3["winding_modes_can_annihilate"])
        self.assertTrue(res3["exactly_three_dimensions_favored"])
        self.assertTrue(res3["string_gas_tensor_tilt_n_t"] > 0)  # Blue tilt
        self.assertTrue(res3["standard_inflation_tensor_tilt_n_t"] < 0)  # Red tilt

        # 4 dimensions: worldsheets cannot intersect generically in (4+1) spacetime dimensions
        res4 = WavefunctionOfUniverseAnalyzer.evaluate_string_gas_cosmology(spatial_dimensions=4)
        self.assertFalse(res4["winding_modes_can_annihilate"])
        self.assertFalse(res4["exactly_three_dimensions_favored"])


class TestPenroseWeylEntropyAnalyzer(unittest.TestCase):
    """Verify cosmological entropy budget and Penrose phase space deficit."""

    def test_entropy_budget(self):
        res = PenroseWeylEntropyAnalyzer.compute_cosmic_entropy_budget()
        # Thermal entropy ~ 10^89 k_B
        self.assertTrue(1e88 < res["thermal_entropy_kb"] < 1e91)
        # SMBH entropy ~ 10^104 k_B
        self.assertEqual(res["smbh_entropy_kb"], 1e104)
        # Maximal horizon entropy ~ 2.6e122 k_B
        self.assertTrue(1e122 < res["maximal_horizon_entropy_kb"] < 1e123)
        # Exponent order of magnitude ~ 122.4
        self.assertTrue(122.0 < res["exponent_orders_of_magnitude"] < 123.0)
        self.assertIn("10^122.4", res["penrose_probability_exponent"])


class TestCosmogenesisMasterDeliverableEngine(unittest.TestCase):
    """Verify the completeness of the canonical 8 open problems matrix."""

    def test_canonical_open_problems_count_and_ids(self):
        problems = CosmogenesisMasterDeliverableEngine.get_canonical_open_problems()
        self.assertEqual(len(problems), 8)
        ids = [p.problem_id for p in problems]
        expected_ids = ["OP-1", "OP-2", "OP-3", "OP-4", "OP-5", "OP-6", "OP-7", "OP-8"]
        self.assertEqual(ids, expected_ids)

    def test_canonical_open_problems_fields(self):
        problems = CosmogenesisMasterDeliverableEngine.get_canonical_open_problems()
        for p in problems:
            self.assertTrue(len(p.problem_name) > 0)
            self.assertTrue(len(p.theoretical_barrier) > 0)
            self.assertTrue(len(p.what_theory_does_not_explain) > 0)
            self.assertTrue(len(p.ground_truth_benchmark) > 0)
            self.assertTrue(len(p.resolving_observation) > 0)
            self.assertTrue(len(p.instrumentation) > 0)
            self.assertTrue(len(p.falsification_metric) > 0)


class TestIntegratedRunner(unittest.TestCase):
    """Verify end-to-end integrated demonstration function."""

    def test_integrated_demonstration_execution(self):
        res = run_integrated_demonstration()
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["canonical_open_problems_count"], 8)
        self.assertTrue(res["string_gas_favors_d3"])
        self.assertTrue(res["vilenkin_stable"])
        self.assertFalse(res["hartle_hawking_stable"])


if __name__ == "__main__":
    unittest.main()
