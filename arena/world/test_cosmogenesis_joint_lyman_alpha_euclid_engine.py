"""
Unit tests for Cosmogenesis Joint Lyman-Alpha and Euclid Neutrino Mass Deficit Arbitration Engine
"""

import unittest
from cosmogenesis_joint_lyman_alpha_euclid_engine import (
    CosmologicalBackgroundEngine,
    MatterPowerSuppressionEngine,
    JointFalsificationArbitrator,
    run_full_joint_falsification_suite,
    SUM_M_NU_NO_MIN_EV,
    SUM_M_NU_IO_MIN_EV,
    W0_DESI,
    WA_DESI
)


class TestJointFalsificationEngine(unittest.TestCase):

    def test_background_dark_energy_fraction(self):
        """Verify dark energy density ratio and Omega_DE(z) diminish at high redshift."""
        omega_de_z0 = CosmologicalBackgroundEngine.dark_energy_fraction(0.0)
        self.assertAlmostEqual(omega_de_z0, 0.685, places=2)

        # At z = 3, dark energy fraction should be small (< 3%)
        omega_de_z3 = CosmologicalBackgroundEngine.dark_energy_fraction(3.0)
        self.assertLess(omega_de_z3, 0.05)

    def test_linear_power_suppression(self):
        """Verify Hu-Eisenstein -8 * f_nu suppression is ~ -3.55% for minimal NO mass."""
        supp = MatterPowerSuppressionEngine.linear_power_suppression(SUM_M_NU_NO_MIN_EV)
        self.assertAlmostEqual(supp * 100.0, -3.55, delta=0.2)

    def test_decaying_neutrino_suppression_erasure(self):
        """Verify decaying neutrinos reduce suppression by > 80% post-decay."""
        res_pre = MatterPowerSuppressionEngine.decaying_neutrino_suppression(4.0, z_decay=3.0, ordering="NO")
        res_post = MatterPowerSuppressionEngine.decaying_neutrino_suppression(1.0, z_decay=3.0, ordering="NO")
        
        self.assertAlmostEqual(res_pre["active_suppression_pct"], res_pre["suppression_pre_decay_pct"], places=2)
        self.assertAlmostEqual(res_post["active_suppression_pct"], res_post["suppression_post_decay_pct"], places=2)
        self.assertGreater(res_post["erasure_efficiency_pct"], 80.0)

    def test_joint_tomographic_trace(self):
        """Verify tomographic trace captures both Euclid and Lyman-alpha regimes."""
        trace = JointFalsificationArbitrator.compute_tomographic_trace([0.5, 2.0, 3.0, 4.0], z_decay=3.2)
        self.assertEqual(len(trace), 4)
        
        # At z=3.0 (post decay), discriminant delta should be ~ 3%
        row_z3 = next(r for r in trace if r["redshift_z"] == 3.0)
        self.assertGreater(row_z3["discriminant_delta_pct"], 2.5)

        # At z=4.0 (pre decay), discriminant delta should be 0.0
        row_z4 = next(r for r in trace if r["redshift_z"] == 4.0)
        self.assertAlmostEqual(row_z4["discriminant_delta_pct"], 0.0, places=2)

    def test_joint_fisher_separation(self):
        """Verify that joint Euclid + Lyman-alpha yields > 5 sigma separation."""
        sep = JointFalsificationArbitrator.compute_joint_fisher_separation()
        self.assertTrue(sep["is_falsification_guaranteed_gt_5_sigma"])
        self.assertGreater(sep["statistical_separation_sigma"], 10.0)
        self.assertGreater(sep["chi2_components"]["total_delta_chi2"], 100.0)

    def test_decision_classification_logic(self):
        """Verify arbitration decision rules correctly classify synthetic measurements."""
        # Simulated measurement matching Dynamical DE
        verdict_a = JointFalsificationArbitrator.evaluate_arbitration_decision(
            measured_w0=-0.825, measured_supp_z3_pct=-3.52
        )
        self.assertIn("CONFIRMED: Dynamical Dark Energy", verdict_a["verdict"])
        self.assertLess(verdict_a["distance_to_h_a_sigma"], 1.0)
        self.assertGreater(verdict_a["distance_to_h_b_sigma"], 5.0)

        # Simulated measurement matching Decaying Neutrinos
        verdict_b = JointFalsificationArbitrator.evaluate_arbitration_decision(
            measured_w0=-1.001, measured_supp_z3_pct=-0.54
        )
        self.assertIn("CONFIRMED: Decaying Relic Neutrinos", verdict_b["verdict"])
        self.assertLess(verdict_b["distance_to_h_b_sigma"], 1.0)
        self.assertGreater(verdict_b["distance_to_h_a_sigma"], 5.0)

    def test_full_suite_execution(self):
        """Verify the full execution pipeline runs cleanly."""
        suite = run_full_joint_falsification_suite()
        self.assertIn("tomographic_trace", suite)
        self.assertIn("fisher_separation", suite)
        self.assertIn("test_case_h_a", suite)
        self.assertIn("test_case_h_b", suite)


if __name__ == "__main__":
    unittest.main()
