"""
test_buchert_backreaction_and_late_time_nogo_engine.py

Comprehensive Test Suite for Inhomogeneous Buchert Backreaction Audit,
Local Void Exclusion, Late-Time No-Go Theorem, and S8-H0 Quadlemma.
"""

import unittest
import math
from buchert_backreaction_and_late_time_nogo_engine import (
    CosmologicalState,
    BuchertBackreactionEngine,
    LocalVoidExclusionEngine,
    LateTimeNoGoTheoremEngine,
    QuadlemmaSynthesisEngine,
    G_NEWTON,
)


class TestBuchertBackreactionEngine(unittest.TestCase):
    def setUp(self):
        self.state = CosmologicalState()
        self.backreaction = BuchertBackreactionEngine(self.state)
        self.void_audit = LocalVoidExclusionEngine(self.state)
        self.nogo = LateTimeNoGoTheoremEngine(self.state)
        self.quadlemma = QuadlemmaSynthesisEngine(self.state)

    def test_cosmological_baseline(self):
        """Verify baseline values match empirical parameters."""
        self.assertAlmostEqual(self.state.H0_planck, 67.4, places=1)
        self.assertAlmostEqual(self.state.H0_shoes, 73.04, places=2)
        self.assertAlmostEqual(self.state.Omega_m, 0.3134, places=3)
        self.assertAlmostEqual(self.state.r_s_planck_Mpc, 143.92, places=2)
        self.assertAlmostEqual(self.state.theta_star, 0.010396, places=5)

    def test_buchert_kinematical_backreaction(self):
        """Verify Q_D calculation follows (2/3)*Var(theta) - 2*<sigma^2>."""
        var_theta = 1.2e-35
        shear_sq = 2.0e-36
        q_d = self.backreaction.kinematical_backreaction(var_theta, shear_sq)
        expected = (2.0 / 3.0) * var_theta - 2.0 * shear_sq
        self.assertAlmostEqual(q_d, expected, delta=1e-40)

    def test_acceleration_condition(self):
        """Verify acceleration requirement Q_D > 4*pi*G*<rho>."""
        rho_avg = 1e-27  # kg/m^3
        q_threshold = 4.0 * math.pi * G_NEWTON * rho_avg
        # Below threshold
        res_sub = self.backreaction.acceleration_condition(rho_avg, Q_D=0.5 * q_threshold)
        self.assertFalse(res_sub["is_accelerating"])
        # Above threshold
        res_super = self.backreaction.acceleration_condition(rho_avg, Q_D=1.5 * q_threshold)
        self.assertTrue(res_super["is_accelerating"])

    def test_green_wald_theorem_bounds(self):
        """Verify Green-Wald theorem forbids negative pressure and dark energy mimicry."""
        gw = self.backreaction.evaluate_green_wald_theorem_bounds()
        self.assertTrue(gw["traceless_backreaction"])
        self.assertFalse(gw["can_produce_negative_pressure"])
        self.assertFalse(gw["can_drive_cosmic_acceleration"])
        self.assertGreaterEqual(gw["effective_w_min"], 0.0)

    def test_gevolution_numerical_magnitude(self):
        """Verify simulated backreaction is underpowered by ~100x to resolve H0."""
        gev = self.backreaction.evaluate_gevolution_numerical_magnitude()
        self.assertFalse(gev["physical_feasibility"])
        self.assertGreater(gev["shortfall_factor"], 50.0)
        self.assertLess(gev["omega_Q_simulated_upper_bound"], 0.001)

    def test_local_void_underdensity_and_exclusion(self):
        """Verify local void required is > 40% underdensity, excluded at > 5-sigma."""
        void_calc = self.void_audit.void_underdensity_required()
        self.assertLess(void_calc["delta_void_needed"], -0.40)
        
        exclusion = self.void_audit.void_significance_and_exclusion(R_void_Mpc=200.0)
        self.assertTrue(exclusion["ruled_out"])
        self.assertGreater(exclusion["gaussian_sigma_discrepancy"], 5.0)
        self.assertGreater(exclusion["empirical_exclusion_sigma"], 5.0)

    def test_late_time_no_go_geometry(self):
        """Verify naive scaling of H0 without shrinking r_s shifts theta_* at > 20 sigma."""
        geom = self.nogo.evaluate_no_go_geometry()
        self.assertFalse(geom["late_time_r_s_modified"])
        self.assertGreater(geom["tension_theta_sigma"], 20.0)
        self.assertGreater(abs(geom["delta_theta_pct"]), 5.0)

    def test_bao_intermediate_tension(self):
        """Verify intermediate H(z) suppression to save D_M is excluded by BAO."""
        bao = self.nogo.evaluate_bao_intermediate_tension()
        self.assertGreater(bao["delta_chi2"], 15.0)
        self.assertGreater(bao["sigma_exclusion"], 3.5)

    def test_quadlemma_synthesis_and_definitive_resolution(self):
        """Verify quadlemma audit answers Raman definitively with False."""
        audit = self.quadlemma.execute_complete_audit()
        ans = audit["definitive_answer_to_raman"]
        self.assertFalse(ans["can_buchert_backreaction_resolve_hubble_tension_without_shrinking_rs"])
        self.assertEqual(len(ans["primary_reasons"]), 4)
        
        growth = audit["growth_tension"]
        self.assertGreater(growth["tension_ede_lensing_sigma"], 4.0)


if __name__ == "__main__":
    unittest.main()
