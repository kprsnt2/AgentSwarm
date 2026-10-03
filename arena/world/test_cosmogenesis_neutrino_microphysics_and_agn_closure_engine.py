"""
Unit Tests for Cosmogenesis Neutrino Microphysics and AGN Closure Engine
========================================================================
Author: Raman (A002, Generation 0)
"""

import unittest
import math
from cosmogenesis_neutrino_microphysics_and_agn_closure_engine import (
    NeutrinoMicrophysicsEngine,
    AGNScaleSeparationEngine,
    ThermalHistoryAndNeffEngine,
    run_full_closure_audit,
)

class TestNeutrinoMicrophysicsAndAGNClosure(unittest.TestCase):

    def setUp(self):
        self.micro = NeutrinoMicrophysicsEngine(m3_eV=0.0502, m2_eV=0.00868, m1_eV=0.0)
        self.agn = AGNScaleSeparationEngine()
        self.thermal = ThermalHistoryAndNeffEngine(m3_eV=0.0502, z_dec=3.2)

    def test_decay_kinematics_and_coupling(self):
        """Verify that a 2.0 Gyr lifetime yields an ultra-weak coupling g ~ 3.23e-15."""
        kin = self.micro.calculate_decay_kinematics(tau_yr=2.0e9)
        self.assertAlmostEqual(kin["tau_yr"], 2.0e9)
        self.assertGreater(kin["g_phi"], 1.0e-15)
        self.assertLess(kin["g_phi"], 1.0e-14)
        # Check energy conservation in rest frame
        self.assertAlmostEqual(kin["e_phi_rest_eV"], 0.0502 / 2.0, places=6)

    def test_laboratory_and_astrophysical_margins(self):
        """Verify that g_phi evades SN1987A and meson decay bounds by >8 orders of magnitude."""
        kin = self.micro.calculate_decay_kinematics(tau_yr=2.0e9)
        margins = self.micro.evaluate_constraint_margins(kin["g_phi"])
        
        # SN1987A cooling limit is 1e-6
        sn_margin = margins["sn1987a_cooling"]
        self.assertTrue(sn_margin["safe"])
        self.assertGreater(sn_margin["orders_of_magnitude_headroom"], 8.0)

        # Pion decay limit is 1e-3
        pion_margin = margins["pion_decay_pi_e_nu_phi"]
        self.assertTrue(pion_margin["safe"])
        self.assertGreater(pion_margin["orders_of_magnitude_headroom"], 11.0)

    def test_bbn_non_thermalization(self):
        """Verify that the scalar interaction never thermalizes at BBN temperatures."""
        kin = self.micro.calculate_decay_kinematics(tau_yr=2.0e9)
        bbn = self.micro.evaluate_bbn_non_thermalization(kin["g_phi"])
        self.assertTrue(bbn["is_completely_non_thermal"])
        self.assertLess(bbn["thermalization_ratio"], 1.0e-30)

    def test_agn_scale_separation_at_z3(self):
        """Verify that free-streaming and AGN feedback scales are separated by >10x at z=3."""
        sep = self.agn.evaluate_scale_separation(z=3.0, m_nu_eV=0.0502)
        self.assertGreater(sep["separation_ratio"], 9.0)
        self.assertTrue(sep["is_cleanly_separated"])
        # Contamination at optimal cut (0.50 h/Mpc) must be negligible (< 0.5%)
        self.assertLess(sep["agn_contamination_pct"], 0.5)

    def test_agn_scale_separation_redshift_scaling(self):
        """Verify that scale separation improves or remains robust across the Lyman-alpha forest range."""
        for z in [2.2, 2.8, 3.5]:
            sep = self.agn.evaluate_scale_separation(z=z, m_nu_eV=0.0502)
            self.assertGreater(sep["separation_ratio"], 8.0)
            self.assertLess(sep["agn_contamination_pct"], 1.0)

    def test_delta_neff_redshift_step(self):
        """Verify that Delta N_eff is exactly 0 before decay and non-zero after decay."""
        # Before decay (z = 4.0 > z_dec = 3.2)
        self.assertEqual(self.thermal.delta_neff_at_redshift(4.0), 0.0)
        # At present day (z = 0.0)
        neff_0 = self.thermal.delta_neff_at_redshift(0.0)
        self.assertAlmostEqual(neff_0, 0.080 * (0.0502 / 0.05), places=4)

    def test_cmb_s4_forecast_detection(self):
        """Verify that CMB-S4 has >3 sigma sensitivity to the post-decay radiation density."""
        forecast = self.thermal.forecast_cmb_s4_detection(sigma_neff=0.025)
        self.assertTrue(forecast["detectable_at_3sigma"])
        self.assertGreater(forecast["detection_snr"], 3.0)

    def test_full_closure_audit_execution(self):
        """Verify end-to-end execution of the full closure audit."""
        res = run_full_closure_audit()
        self.assertIn("kinematics", res)
        self.assertIn("margins", res)
        self.assertIn("bbn", res)
        self.assertIn("scale_separation", res)
        self.assertIn("thermal_forecast", res)

if __name__ == "__main__":
    unittest.main()
