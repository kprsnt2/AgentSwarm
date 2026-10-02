"""Unit Test Suite for Pregeometric Cosmogenesis and Foundational Assumption Attack Engine.

Agent: Kepler (A001) | Generation: 0 | Domain: Origin of the Universe (Cosmogenesis)
Epistemic Class: Empirical Precision Cosmology & Quantum Foundations
"""

import unittest
import math
from pregeometric_cosmogenesis_and_backreaction_falsification_engine import (
    GreenWaldBackreactionAnalyzer,
    PantheonPlusLocalVoidAnalyzer,
    EkpyroticBounceInstabilityAnalyzer,
    PregeometricQuantumInformationEngine,
    MasterFoundationalAssumptionBenchmark,
    C, G, HBAR, K_B, L_PL, T_PL, M_PL, RHO_PL, T_PL_KELVIN,
    H0_PLANCK, H0_SHOES, OMEGA_LAMBDA_PLANCK
)


class TestPregeometricCosmogenesisEngine(unittest.TestCase):

    def test_physical_constants_and_planck_scales(self):
        """Verify dimensional correctness and numerical values of Planck units."""
        self.assertAlmostEqual(C, 299792458.0, places=1)
        self.assertGreater(L_PL, 1.6e-35)
        self.assertLess(L_PL, 1.65e-35)
        self.assertGreater(T_PL, 5.3e-44)
        self.assertLess(T_PL, 5.5e-44)
        self.assertGreater(M_PL, 2.1e-8)
        self.assertLess(M_PL, 2.2e-8)
        self.assertGreater(RHO_PL, 1.0e96)
        self.assertGreater(T_PL_KELVIN, 1.0e32)

    def test_green_wald_backreaction_bound(self):
        """Verify Green-Wald tracelessness theorem and failure to replace Dark Energy."""
        result = GreenWaldBackreactionAnalyzer.compute_conformal_backreaction_bound(
            psi_rms=1.0e-5,
            v_rms_km_s=350.0,
            h0_kms_mpc=67.36
        )
        self.assertFalse(result["can_replace_dark_energy"])
        self.assertEqual(result["w_gw"], 1.0 / 3.0)
        self.assertLess(result["ratio_gw_to_de"], 1.0e-8)
        self.assertIn("FALSIFIED", result["verdict"])
        self.assertEqual(result["trace_identity"], "t^mu_mu == 0 (strictly traceless)")

    def test_pantheon_plus_void_rejection(self):
        """Verify Pantheon+ SNe Ia rejection of the KBC local void resolution."""
        result = PantheonPlusLocalVoidAnalyzer.calculate_sn_ia_step_discrepancy(
            void_radius_mpc=300.0,
            delta_void_assumed=-0.25,
            h_in=73.04,
            h_out=67.36,
            pantheon_delta_mu_obs=0.005,
            pantheon_sigma_obs=0.018
        )
        self.assertTrue(result["void_model_ruled_out"])
        self.assertLess(result["delta_mu_predicted_mag"], -0.15)
        self.assertGreater(result["tension_sigma"], 4.5)
        self.assertGreater(result["density_tension_sigma"], 4.0)
        self.assertIn("REJECTED", result["verdict"])

    def test_ekpyrotic_bounce_gradient_instability(self):
        """Verify Horndeski no-go gradient instability in classical bounces."""
        result = EkpyroticBounceInstabilityAnalyzer.evaluate_horndeski_bounce_stability(
            w_contracting=3.1,
            rho_bounce_kg_m3=2.11e96,
            high_k_mode_m_inv=1.0e30
        )
        self.assertTrue(result["has_gradient_instability"])
        self.assertLess(result["c_s_squared_minimum"], 0.0)
        self.assertLess(result["tau_blowup_seconds"], 1.0e-35)
        self.assertGreater(result["ratio_to_planck_time"], 0.0)
        self.assertEqual(result["dhost_fine_tuning_required"], 1.0e-8)
        self.assertIn("VULNERABILITY CONFIRMED", result["verdict"])

    def test_page_wootters_relational_time(self):
        """Verify emergence of relational time via clock-system entanglement."""
        result = PregeometricQuantumInformationEngine.page_wootters_relational_evolution(
            dimension_clock=100,
            dimension_system=100
        )
        self.assertEqual(result["s_ent_precosmic_bits"], 0.0)
        self.assertGreater(result["s_ent_cosmic_bits"], 5.0)
        self.assertTrue(result["time_emerged"])

    def test_quantum_graphity_condensation(self):
        """Verify spatial condensation from complete graph to 3D manifold."""
        result = PregeometricQuantumInformationEngine.quantum_graphity_phase_transition()
        self.assertEqual(result["dimension_emergent"], 3.0)
        self.assertGreater(result["t_critical_kelvin"], 1.0e32)
        self.assertEqual(result["t_reheat_gev"], 1.0e16)

    def test_holographic_entanglement_budget(self):
        """Verify holographic cosmic horizon entropy and sub-capacity utilization."""
        result = PregeometricQuantumInformationEngine.holographic_entanglement_budget()
        self.assertGreater(result["s_holo_k_b"], 1.0e122)
        self.assertLess(result["s_holo_k_b"], 1.0e123)
        self.assertGreater(result["s_smbh_k_b"], 1.0e103)
        self.assertLess(result["fraction_utilized_by_smbh"], 1.0e-17)
        self.assertGreater(result["entropy_deficit"], 1.0e122)

    def test_master_foundational_assumption_benchmark(self):
        """Verify master benchmark execution and falsification matrix consistency."""
        master = MasterFoundationalAssumptionBenchmark.execute_all_attacks()
        self.assertIn("green_wald_backreaction", master)
        self.assertIn("pantheon_plus_void", master)
        self.assertIn("ekpyrotic_bounce_stability", master)
        self.assertIn("page_wootters_time", master)
        self.assertIn("quantum_graphity", master)
        self.assertIn("holographic_entropy", master)
        
        matrix = master["falsification_matrix"]
        self.assertEqual(len(matrix), 4)
        for item in matrix:
            self.assertIn("id", item)
            self.assertIn("assumption", item)
            self.assertIn("attack_mechanism", item)
            self.assertIn("quantitative_limit", item)
            self.assertIn("resolving_observation", item)


if __name__ == "__main__":
    unittest.main()
