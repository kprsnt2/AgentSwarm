"""
Unit Tests for Outsider Cosmological Neutrino Deficit and Epicycle Refutation Engine
===================================================================================
Author: Outsider3 (A003, Generation 0)
"""

import unittest
import math
from outsider_cosmological_neutrino_deficit_and_epicycle_refutation_engine import (
    FreeStreamingScalingAudit,
    RelativisticThermodynamicsEngine,
    GeometricBAODistanceEngine,
    StatisticalConsilienceAudit,
    run_comprehensive_outsider_audit,
    SUM_M_NU_NO_MIN,
    SUM_M_NU_IO_MIN,
    Z_STAR,
)

class TestOutsiderNeutrinoRefutationEngine(unittest.TestCase):

    def setUp(self):
        self.bao_engine = GeometricBAODistanceEngine()

    def test_free_streaming_redshift_scaling(self):
        """Verify that true k_fs decreases with z as (1+z)^(-1/2)."""
        k_z0 = FreeStreamingScalingAudit.true_free_streaming_wavenumber(0.0, 0.0502)
        k_z3 = FreeStreamingScalingAudit.true_free_streaming_wavenumber(3.0, 0.0502)
        # Ratio should be exactly 1 / sqrt(1+3) = 0.50
        self.assertAlmostEqual(k_z3 / k_z0, 0.50, places=4)
        self.assertLess(k_z3, k_z0)

    def test_raman_scaling_discrepancy(self):
        """Verify that Raman's buggy formula overestimates k_fs at z=3 by a factor of ~25.4."""
        audit = FreeStreamingScalingAudit.audit_scaling_discrepancy(z=3.0, m_nu_ev=0.0502)
        self.assertGreater(audit["error_factor"], 24.0)
        self.assertLess(audit["error_factor"], 27.0)
        self.assertAlmostEqual(audit["k_fs_true_h_Mpc"], 0.00954, places=4)
        self.assertTrue(audit["is_plateau_deep_in_linear_regime"])

    def test_relativistic_decay_energy_injection(self):
        """Verify that late decay produces Delta N_eff ~ 22.57, exposing Raman's 282x underestimation."""
        thermo = RelativisticThermodynamicsEngine.calculate_decay_radiation_injection(0.0502, z_dec=3.2)
        self.assertAlmostEqual(thermo["delta_neff_true"], 22.57, delta=0.2)
        self.assertAlmostEqual(thermo["delta_neff_raman"], 0.0803, places=3)
        self.assertGreater(thermo["energy_violation_factor"], 250.0)
        self.assertTrue(thermo["is_raman_grossly_underestimated"])

    def test_primary_cmb_horizon_blindness(self):
        """Verify that primary CMB temperature/polarization power spectra are blind to decay at z=3.2."""
        cmb = RelativisticThermodynamicsEngine.evaluate_primary_cmb_response(z_dec=3.2)
        self.assertEqual(cmb["delta_neff_at_recombination"], 0.0)
        self.assertEqual(cmb["primary_cmb_acoustic_phase_shift"], 0.0)
        self.assertEqual(cmb["primary_cmb_silk_damping_tail_shift_pct"], 0.0)
        self.assertTrue(cmb["is_primary_cmb_blind"])

    def test_geometric_h0_preservation(self):
        """Verify that increasing sum m_nu forces H0 downward to preserve the acoustic scale."""
        h_0 = self.bao_engine.solve_h_for_stable_neutrinos(0.0)
        h_no = self.bao_engine.solve_h_for_stable_neutrinos(SUM_M_NU_NO_MIN)
        h_io = self.bao_engine.solve_h_for_stable_neutrinos(SUM_M_NU_IO_MIN)

        h0_0 = 100.0 * h_0
        h0_no = 100.0 * h_no
        h0_io = 100.0 * h_io

        self.assertGreater(h0_0, h0_no)
        self.assertGreater(h0_no, h0_io)
        # Check derivative dH0 / d(sum m_nu) ~ -10.3 km/s/Mpc/eV
        dh0_dm = (h0_no - h0_0) / SUM_M_NU_NO_MIN
        self.assertLess(dh0_dm, -9.0)
        self.assertGreater(dh0_dm, -12.0)

    def test_neutrino_decay_bao_negligible_benefit(self):
        """Verify that neutrino decay improves DESI BAO Chi2 by only -0.24 for Normal Ordering."""
        res_stable = self.bao_engine.evaluate_desi_bao_chi2(SUM_M_NU_NO_MIN, is_decayed=False)
        res_decay = self.bao_engine.evaluate_desi_bao_chi2(SUM_M_NU_NO_MIN, is_decayed=True, z_dec=3.2, ordering="NO")

        delta_chi2 = res_decay["total_chi2"] - res_stable["total_chi2"]
        self.assertAlmostEqual(delta_chi2, -0.24, delta=0.10)
        # Verify both achieve Chi2 around ~29.5
        self.assertGreater(res_stable["total_chi2"], 28.0)
        self.assertLess(res_stable["total_chi2"], 31.0)

    def test_inverted_ordering_remains_excluded_under_decay(self):
        """Verify that decaying neutrinos completely fail to rescue Inverted Ordering (Delta Chi2 ~ +3.51)."""
        res_no_stable = self.bao_engine.evaluate_desi_bao_chi2(SUM_M_NU_NO_MIN, is_decayed=False)
        res_io_decay = self.bao_engine.evaluate_desi_bao_chi2(SUM_M_NU_IO_MIN, is_decayed=True, z_dec=3.2, ordering="IO")

        delta_chi2 = res_io_decay["total_chi2"] - res_no_stable["total_chi2"]
        self.assertGreater(delta_chi2, 3.0)
        self.assertLess(delta_chi2, 4.0)

    def test_statistical_consilience_dataset_pulls(self):
        """Verify that Normal Ordering has only 1.34 sigma pull in Planck+DESI and 0.86 sigma with Pantheon+."""
        stats = StatisticalConsilienceAudit.evaluate_ordering_viability()
        
        desi_pull = stats["Planck_DESI"]["pull_normal_ordering_sigma"]
        self.assertAlmostEqual(desi_pull, 1.34, delta=0.05)
        self.assertTrue(stats["Planck_DESI"]["is_normal_ordering_viable"])

        pantheon_pull = stats["Planck_DESI_PantheonPlus"]["pull_normal_ordering_sigma"]
        self.assertAlmostEqual(pantheon_pull, 0.86, delta=0.05)
        self.assertTrue(stats["Planck_DESI_PantheonPlus"]["is_normal_ordering_viable"])
        self.assertTrue(stats["Planck_DESI_PantheonPlus"]["is_inverted_ordering_viable"])

    def test_end_to_end_audit_pipeline(self):
        """Verify that run_comprehensive_outsider_audit runs without error and returns complete fields."""
        report = run_comprehensive_outsider_audit()
        self.assertIn("scale_audit", report)
        self.assertIn("thermo_audit", report)
        self.assertIn("cmb_audit", report)
        self.assertIn("bao_comparisons", report)
        self.assertIn("statistical_consilience", report)

if __name__ == "__main__":
    unittest.main()
