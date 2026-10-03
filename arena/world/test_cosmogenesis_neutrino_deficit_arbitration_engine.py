"""
Unit tests for Cosmogenesis Neutrino Deficit Arbitration Engine
"""

import unittest
from cosmogenesis_neutrino_deficit_arbitration_engine import (
    DynamicalDarkEnergyArbitrator,
    DecayingNeutrinoArbitrator,
    JointArbitrationMatrixEngine,
    run_full_arbitration_audit,
    SUM_M_NU_NO_MIN_EV,
    SUM_M_NU_IO_MIN_EV,
    BOUND_W0WA_CDM_DESI_PLANCK,
    BOUND_LAMBDA_CDM_DESI_PLANCK,
    W0_DESI_BEST,
    WA_DESI_BEST
)


class TestArbitrationEngine(unittest.TestCase):

    def test_cpl_equation_of_state(self):
        """Verify w(z) calculation at z=0 and high z."""
        w_z0 = DynamicalDarkEnergyArbitrator.equation_of_state(0.0)
        self.assertAlmostEqual(w_z0, W0_DESI_BEST, places=4)
        
        # At high z (a -> 0), w(a) -> w0 + wa
        w_inf = DynamicalDarkEnergyArbitrator.equation_of_state(1000.0)
        self.assertAlmostEqual(w_inf, W0_DESI_BEST + WA_DESI_BEST, places=2)

    def test_phantom_crossing_detection(self):
        """Verify phantom divide crossing occurs at z ~ 0.25 - 0.40 for DESI best-fit."""
        has_crossing, z_cross = DynamicalDarkEnergyArbitrator.phantom_crossing_redshift()
        self.assertTrue(has_crossing)
        self.assertTrue(0.20 < z_cross < 0.45)

    def test_dynamical_de_mass_relaxation(self):
        """Verify that w0-wa-CDM relaxes the neutrino mass bound to accommodate Inverted Ordering."""
        res = DynamicalDarkEnergyArbitrator.evaluate_neutrino_mass_relaxation()
        self.assertTrue(res["is_inverted_ordering_viable"])
        self.assertGreater(res["sum_m_nu_upper_limit_ev"], SUM_M_NU_IO_MIN_EV)
        self.assertGreater(res["inverted_ordering_headroom_ev"], 0.0)
        self.assertLess(res["inverted_ordering_tension_sigma"], 1.5)

    def test_decaying_neutrino_suppression_erasure(self):
        """Verify that decay of nu_3 erases >80% of linear matter power spectrum suppression."""
        res = DecayingNeutrinoArbitrator.evaluate_decay_regimes(z_decay=3.5)
        self.assertGreater(res["suppression_erasure_ratio_pct"], 80.0)
        self.assertLess(res["apparent_cosmological_mass_ev"], 0.015)
        self.assertTrue(res["is_within_planck_act_n_eff_bounds"])
        self.assertGreater(res["headroom_under_desi_act_ev"], 0.05)

    def test_redshift_tomography_discrimination(self):
        """Verify high-z Lyman-alpha discriminates between Dynamical DE and Decaying Neutrinos."""
        tomo = JointArbitrationMatrixEngine.evaluate_redshift_tomography([0.0, 2.0, 4.0])
        # At z = 0 (post-decay): difference is large (~3%)
        row_z0 = next(r for r in tomo if r["redshift_z"] == 0.0)
        self.assertGreater(row_z0["discriminant_delta_pct"], 2.5)

        # At z = 4 (pre-decay): both have full suppression, discriminant delta is 0
        row_z4 = next(r for r in tomo if r["redshift_z"] == 4.0)
        self.assertAlmostEqual(row_z4["discriminant_delta_pct"], 0.0, places=2)

    def test_four_pillar_decision_matrix(self):
        """Verify 4 pillars are fully defined and populated."""
        matrix = JointArbitrationMatrixEngine.generate_arbitration_decision_matrix()
        self.assertEqual(len(matrix["four_pillar_matrix"]), 4)
        for pillar in matrix["four_pillar_matrix"]:
            self.assertIn("pillar", pillar)
            self.assertIn("dynamical_dark_energy_signature", pillar)
            self.assertIn("decaying_neutrino_signature", pillar)
            self.assertIn("decisive_observables", pillar)
            self.assertIn("verdict_criterion", pillar)

    def test_full_arbitration_audit(self):
        """Verify full arbitration audit returns structured comprehensive output."""
        audit = run_full_arbitration_audit()
        self.assertIn("dynamical_de_summary", audit)
        self.assertIn("decaying_neutrino_summary", audit)
        self.assertIn("redshift_tomography_trace", audit)
        self.assertIn("four_pillar_matrix", audit)
        self.assertIn("definitive_synthesis", audit)


if __name__ == "__main__":
    unittest.main()
