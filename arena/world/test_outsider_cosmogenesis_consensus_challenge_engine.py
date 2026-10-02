"""Unit Test Suite for Outsider Cosmogenesis Consensus Challenge Engine.

Agent: Outsider2 (A002) | Generation: 0 | Domain: Swarm Consensus Falsification
Epistemic Class: Foundational Physics & Quantitative Cosmological Duality
"""

import unittest
import math
from outsider_cosmogenesis_consensus_challenge_engine import (
    CPTSymmetricCosmologyEngine,
    UnimodularVacuumDecouplingEngine,
    WetterichConformalZeroExpansionEngine,
    EinsteinCartanSpinTorsionEngine,
    BarbourJanusPointComplexityEngine,
    MasterOutsiderConsensusAttackBenchmark,
    C, G, HBAR, K_B, L_PL, T_PL, M_PL_GEV, RHO_PL_SI, RHO_PL_CGS,
    ETA_B_OBSERVED, OMEGA_C_H2
)


class TestOutsiderCosmogenesisEngine(unittest.TestCase):

    def test_fundamental_constants_and_planck_units(self):
        """Verify dimensional correctness of fundamental and Planck units."""
        self.assertAlmostEqual(C, 299792458.0, places=1)
        self.assertGreater(L_PL, 1.6e-35)
        self.assertLess(L_PL, 1.65e-35)
        self.assertGreater(T_PL, 5.3e-44)
        self.assertLess(T_PL, 5.5e-44)
        self.assertGreater(M_PL_GEV, 1.2e19)
        self.assertLess(M_PL_GEV, 1.3e19)
        self.assertGreater(RHO_PL_SI, 1.0e96)
        self.assertGreater(RHO_PL_CGS, 1.0e93)

    def test_cpt_symmetric_baryon_asymmetry_and_dm(self):
        """Verify CPT double-sheet net baryon asymmetry cancellation and RH neutrino DM."""
        baryon_result = CPTSymmetricCosmologyEngine.evaluate_cpt_baryon_asymmetry()
        self.assertTrue(baryon_result["is_cpt_conserved"])
        self.assertEqual(baryon_result["net_baryon_asymmetry"], 0.0)
        self.assertFalse(baryon_result["sakharov_violation_needed"])

        # Dark matter relic density from gravitational freeze-in
        dm_result = CPTSymmetricCosmologyEngine.calculate_rh_neutrino_dark_matter(4.8e8)
        self.assertAlmostEqual(dm_result["omega_n_h2"], OMEGA_C_H2, places=3)
        self.assertAlmostEqual(dm_result["discordance_sigma"], 0.0, places=2)
        self.assertFalse(dm_result["requires_bsm_fields"])

    def test_cpt_neutrino_mass_spectrum_and_tensors(self):
        """Verify normal ordering with m1=0 and zero tensor-to-scalar ratio."""
        nu_result = CPTSymmetricCosmologyEngine.calculate_neutrino_mass_spectrum()
        self.assertEqual(nu_result["m1_ev"], 0.0)
        self.assertGreater(nu_result["m2_ev"], 0.008)
        self.assertGreater(nu_result["m3_ev"], 0.049)
        self.assertLess(nu_result["sum_m_nu_ev"], 0.065)
        self.assertTrue(nu_result["is_compatible_with_planck"])

        tensor_result = CPTSymmetricCosmologyEngine.evaluate_tensor_to_scalar_prediction()
        self.assertEqual(tensor_result["r_cpt"], 0.0)

    def test_unimodular_vacuum_decoupling(self):
        """Verify that vacuum energy couples to curvature with exactly zero strength in Unimodular gravity."""
        unimodular_result = UnimodularVacuumDecouplingEngine.compute_trace_free_coupling()
        self.assertEqual(unimodular_result["effective_vacuum_coupling_tensor_norm"], 0.0)
        self.assertEqual(unimodular_result["catastrophe_orders_in_unimodular"], 0.0)
        self.assertGreater(unimodular_result["catastrophe_orders_in_standard_gr"], 120.0)

        # Sorkin causal set Poisson fluctuation
        sorkin_result = UnimodularVacuumDecouplingEngine.sorkin_causal_set_unimodular_fluctuation(1.0e240)
        self.assertTrue(sorkin_result["resolves_coincidence_problem"])

    def test_wetterich_conformal_zero_expansion_equivalence(self):
        """Verify observational equivalence of static space with evolving masses vs expanding space."""
        for z in [0.5, 1.0, 1.5, 3.0, 6.34]:
            result = WetterichConformalZeroExpansionEngine.evaluate_conformal_transformation(z)
            self.assertTrue(result["observational_equivalence"])
            self.assertFalse(result["wetterich_frame"]["space_is_expanding"])
            self.assertTrue(result["wetterich_frame"]["physical_distance_between_galaxies_is_constant"])
            self.assertAlmostEqual(result["wetterich_frame"]["calculated_redshift"], z, places=7)

    def test_einstein_cartan_spin_torsion_bounce(self):
        """Verify that spin-torsion halts collapse at densities ~38-48 orders below Planck."""
        torsion_result = EinsteinCartanSpinTorsionEngine.compute_torsion_bounce_density()
        self.assertFalse(torsion_result["is_planck_scale_accessed"])
        self.assertFalse(torsion_result["quantum_gravity_required"])
        self.assertGreater(torsion_result["orders_of_magnitude_below_planck_density"], 35.0)
        self.assertLess(torsion_result["orders_of_magnitude_below_planck_density"], 55.0)
        self.assertLess(torsion_result["e_bounce_gev"], M_PL_GEV * 1e-3)

        # Bounce trajectory
        trajectory = EinsteinCartanSpinTorsionEngine.solve_torsion_bounce_trajectory(rho_fraction=1.0)
        self.assertEqual(trajectory["h_at_bounce"], 0.0)
        self.assertTrue(trajectory["is_acceleration_positive_at_bounce"])
        self.assertTrue(trajectory["singularity_avoided"])

    def test_barbour_janus_point_measure(self):
        """Verify that Janus point has measure 1.0, eliminating Penrose's 10^-10^122 fine-tuning."""
        janus_result = BarbourJanusPointComplexityEngine.evaluate_janus_point_measure()
        self.assertEqual(janus_result["janus_point_actual_probability"], 1.0)
        self.assertFalse(janus_result["is_fine_tuning_necessary"])
        self.assertEqual(janus_result["arrows_of_time_count"], 2)

        # Complexity growth away from Janus point
        c_at_0 = BarbourJanusPointComplexityEngine.compute_complexity_growth(0.0)
        c_at_pos = BarbourJanusPointComplexityEngine.compute_complexity_growth(2.0)
        c_at_neg = BarbourJanusPointComplexityEngine.compute_complexity_growth(-2.0)
        self.assertEqual(c_at_0, 1.0)
        self.assertGreater(c_at_pos, c_at_0)
        self.assertEqual(c_at_pos, c_at_neg)

    def test_master_outsider_consensus_attack_benchmark(self):
        """Verify comprehensive execution of all 5 outsider refutations and falsification matrix."""
        benchmark = MasterOutsiderConsensusAttackBenchmark.run_comprehensive_consensus_attack()
        self.assertEqual(benchmark["status"], "ALL_5_OUTSIDER_ATTACKS_QUANTITATIVELY_VERIFIED")
        self.assertEqual(len(benchmark["falsification_matrix"]), 5)
        for item in benchmark["falsification_matrix"]:
            self.assertTrue(item["id"].startswith("OUTSIDER-"))
            self.assertIn("resolving_facility", item)


if __name__ == "__main__":
    unittest.main()
