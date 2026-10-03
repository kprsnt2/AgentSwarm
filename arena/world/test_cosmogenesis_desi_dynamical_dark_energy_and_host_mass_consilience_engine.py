"""
test_cosmogenesis_desi_dynamical_dark_energy_and_host_mass_consilience_engine.py

Unit test suite for the DESI 2024 Dynamical Dark Energy,
SNe Ia Host Mass Demographics, and Cosmological Consilience Engine.
"""

import unittest
import math
from cosmogenesis_desi_dynamical_dark_energy_and_host_mass_consilience_engine import (
    CPLCosmologicalEngine,
    CosmologicalParameters,
    DESI_2024_BAO_DATA,
    HaloSystematicsEngine,
    GrandConsilienceAuditEngine,
    C_LIGHT_KM_S
)


class TestDESIDynamicalDarkEnergyAndHostMassEngine(unittest.TestCase):

    def setUp(self):
        self.p_lcdm = CosmologicalParameters(
            H0=67.36, omega_b=0.02237, omega_c=0.1200, w0=-1.0, wa=0.0
        )
        self.p_desi = CosmologicalParameters(
            H0=68.60, omega_b=0.02237, omega_c=0.1180, w0=-0.727, wa=-1.05
        )
        self.eng_lcdm = CPLCosmologicalEngine(self.p_lcdm)
        self.eng_desi = CPLCosmologicalEngine(self.p_desi)

    def test_sound_horizon_aubourg_formula(self):
        """Verify Aubourg et al. (2015) sound horizon matches Planck fiducial 147.06 Mpc."""
        rd = self.eng_lcdm.sound_horizon_drag_rd()
        self.assertAlmostEqual(rd, 147.06, places=1)
        self.assertTrue(146.5 < rd < 147.5)

    def test_desi_2024_bao_data_integrity(self):
        """Verify all 13 DESI 2024 Year 1 BAO data points are well-defined."""
        self.assertEqual(len(DESI_2024_BAO_DATA), 13)
        for pt in DESI_2024_BAO_DATA:
            self.assertGreater(pt.z_eff, 0.0)
            self.assertGreater(pt.measured_val, 0.0)
            self.assertGreater(pt.sigma_stat_sys, 0.0)
            self.assertIn(pt.observable, ['DV_rd', 'DM_rd', 'DH_rd'])

    def test_cpl_dark_energy_equation_of_state(self):
        """Verify CPL w(z) parametrization at z=0 and asymptotic high-z."""
        # At z = 0, w(0) = w0
        self.assertAlmostEqual(self.eng_desi.w(0.0), -0.727, places=5)
        # As z -> infinity, a -> 0, w -> w0 + wa
        w_inf = self.eng_desi.w(1e6)
        self.assertAlmostEqual(w_inf, -0.727 - 1.05, places=2)

    def test_phantom_crossing_detection(self):
        """Verify detection of phantom crossing at z_cross ~ 0.351."""
        diag = self.eng_desi.phantom_crossing_diagnostics()
        self.assertTrue(diag["crosses_phantom_divide"])
        self.assertIsNotNone(diag["z_cross"])
        self.assertAlmostEqual(diag["z_cross"], 0.351, places=2)
        self.assertTrue(diag["canonical_ghost_instability"])

    def test_desi_chi2_comparison(self):
        """Verify DESI w0-wa model improves chi2 over Lambda-CDM and SH0ES."""
        chi2_lcdm, _ = self.eng_lcdm.evaluate_desi_chi2()
        chi2_desi, _ = self.eng_desi.evaluate_desi_chi2()

        # w0-wa CDM improves fit to DESI BAO data
        self.assertLess(chi2_desi, chi2_lcdm)

        # Forcing H0 = 73.04 with standard rd explodes chi2
        p_shoes = CosmologicalParameters(
            H0=73.04, omega_b=0.02237, omega_c=0.1200, w0=-1.0, wa=0.0
        )
        eng_shoes = CPLCosmologicalEngine(p_shoes)
        chi2_shoes, _ = eng_shoes.evaluate_desi_chi2()
        self.assertGreater(chi2_shoes, 40.0)

    def test_multi_anchor_trgb_joint(self):
        """Verify multi-anchor TRGB inverse-variance mean across N4258, LMC, MW."""
        h0_joint, sig_joint = HaloSystematicsEngine.compute_multi_anchor_trgb_joint()
        self.assertTrue(70.0 < h0_joint < 71.0)
        self.assertTrue(0.9 < sig_joint < 1.3)

    def test_host_mass_step_demographic_correction(self):
        """Verify that SNe Ia host mass demographic step shifts H0 downward by ~1.2 km/s/Mpc."""
        corr = HaloSystematicsEngine.compute_host_mass_demographic_correction()
        self.assertLess(corr["delta_H0_shift"], 0.0)
        self.assertTrue(-2.0 < corr["delta_H0_shift"] < -0.8)
        self.assertTrue(68.5 < corr["h0_corrected"] < 69.8)

    def test_grand_consilience_and_bayesian_evidence(self):
        """Verify mutual tension < 0.5 sigma and decisive Bayesian evidence against SH0ES intrusion."""
        results = GrandConsilienceAuditEngine.evaluate_model_compendium()
        comp = results["consilience_comparison"]

        # Mutual tension between DESI w0-wa H0 (68.60) and Corrected Halo H0 (69.23) is < 0.5 sigma
        self.assertLess(comp["mutual_tension_sigma"], 0.50)
        # Delta chi2 vs SH0ES intrusion > 50.0
        self.assertGreater(comp["delta_chi2_vs_shoes_intervention"], 50.0)
        # ln(Bayes factor) > 25.0
        self.assertGreater(comp["ln_bayes_factor_vs_shoes"], 25.0)


if __name__ == "__main__":
    unittest.main()
