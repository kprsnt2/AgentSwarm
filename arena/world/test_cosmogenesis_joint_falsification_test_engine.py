"""
test_cosmogenesis_joint_falsification_test_engine.py

Comprehensive Verification Suite for the Euclid + Roman Joint Falsification
and Arbitration Test Engine.

Authored by Agent Raman (A002), Generation 0.
Collaborator: Agent Kepler (A001), Generation 0.
Domain: Ratified consensus: origin of the universe (phase4-consensus).
"""

import unittest
import math
from cosmogenesis_joint_falsification_test_engine import (
    CosmogenesisJointFalsificationEngine,
    BandpowerSpecification,
    ArbitrationResult,
)


class TestCosmogenesisJointFalsificationEngine(unittest.TestCase):
    """Test suite verifying the joint falsification framework."""

    def setUp(self):
        self.engine = CosmogenesisJointFalsificationEngine()

    def test_bandpower_specification_integrity(self):
        """Verifies the 10 tomographic bandpower intervals span ell = 100 to 13000."""
        self.assertEqual(len(self.engine.bandpowers), 10)
        # Check ascending order of multipole centers
        for i in range(len(self.engine.bandpowers) - 1):
            self.assertLess(
                self.engine.bandpowers[i].ell_center,
                self.engine.bandpowers[i + 1].ell_center,
            )
        # Check that Roman covers high multipoles ell > 5000
        roman_bands = [b for b in self.engine.bandpowers if b.survey == "Roman"]
        self.assertGreaterEqual(len(roman_bands), 4)
        self.assertGreater(roman_bands[-1].ell_max, 10000.0)

    def test_observable_1_curvature_spoon_discrimination(self):
        """
        Observable 1 (S_curv): Verifies DCDM has a flat plateau (S_curv ~ 0.992)
        while AGN feedback produces a distinct spoon dip (S_curv ~ 0.836).
        """
        s_curv_dcdm = self.engine.observable_1_curvature_spoon_index(
            f_dcdm=0.035, tau_gyr=30.0, A_bary=0.00
        )
        s_curv_agn = self.engine.observable_1_curvature_spoon_index(
            f_dcdm=0.000, tau_gyr=30.0, A_bary=1.30
        )

        # DCDM suppression must be scale-invariant across non-linear modes (> 0.985)
        self.assertGreater(s_curv_dcdm, 0.985)
        self.assertAlmostEqual(s_curv_dcdm, 0.992, delta=0.010)
        # AGN feedback must show significant spoon dip (< 0.860)
        self.assertLess(s_curv_agn, 0.860)
        # Delta S_curv between models must exceed 12%
        self.assertGreater(s_curv_dcdm - s_curv_agn, 0.12)

    def test_observable_2_tomographic_growth_ratio(self):
        """
        Observable 2 (G_tomo): Verifies that DCDM suppression accumulates
        monotonically with cosmic time, yielding G_tomo = 2.43 +/- 0.05 at fixed k,
        distinct from AGN feedback (G_tomo ~ 1.76).
        """
        t_z1 = self.engine.cosmic_time_gyr(0.35)  # ~ 9.65 Gyr
        t_z5 = self.engine.cosmic_time_gyr(1.80)  # ~ 3.57 Gyr
        expected_dcdm_ratio = (1.0 - math.exp(-t_z1 / 30.0)) / (1.0 - math.exp(-t_z5 / 30.0))

        # Test 1: Fixed physical wavenumber (3D reconstruction)
        g_tomo_dcdm = self.engine.observable_2_tomographic_growth_ratio(
            f_dcdm=0.035, tau_gyr=30.0, A_bary=0.00, match_physical_k=True, k_fixed=1.5
        )
        g_agn_k = self.engine.observable_2_tomographic_growth_ratio(
            f_dcdm=0.000, tau_gyr=30.0, A_bary=1.30, match_physical_k=True, k_fixed=1.5
        )

        self.assertAlmostEqual(g_tomo_dcdm, expected_dcdm_ratio, delta=0.02)
        self.assertGreater(g_tomo_dcdm, 2.38)
        self.assertLess(g_agn_k, 1.82)
        # Separation between DCDM and AGN is massive (> 0.60)
        self.assertGreater(g_tomo_dcdm - g_agn_k, 0.60)

        # Test 2: Fixed multipole band (Limber projected)
        g_dcdm_band = self.engine.observable_2_tomographic_growth_ratio(
            f_dcdm=0.035, tau_gyr=30.0, A_bary=0.00, match_physical_k=False, band_idx=3
        )
        self.assertAlmostEqual(g_dcdm_band, expected_dcdm_ratio, delta=0.10)

    def test_observable_3_roman_stellar_rebound(self):
        """
        Observable 3 (Delta_stellar): Verifies that Roman detects the high-ell
        stellar cusp rebound for AGN feedback (Delta_stellar > 0.05)
        while DCDM remains flat (Delta_stellar ~ 0.00).
        """
        delta_dcdm = self.engine.observable_3_stellar_rebound_cusp(
            f_dcdm=0.035, tau_gyr=30.0, A_bary=0.00
        )
        delta_agn = self.engine.observable_3_stellar_rebound_cusp(
            f_dcdm=0.000, tau_gyr=30.0, A_bary=1.30
        )

        self.assertAlmostEqual(delta_dcdm, 0.000, delta=0.005)
        self.assertGreater(delta_agn, 0.050)
        self.assertGreater(delta_agn - delta_dcdm, 0.050)

    def test_observable_4_tsz_pressure_discrimination(self):
        """
        Observable 4 (y_tsz): Verifies thermal Sunyaev-Zel'dovich cross-correlation
        remains unperturbed for DCDM (y_tsz ~ 1.00) and suppresses for AGN feedback (y_tsz ~ 0.82).
        """
        y_dcdm = self.engine.observable_4_tsz_cross_correlation_amplitude(A_bary=0.00)
        y_agn = self.engine.observable_4_tsz_cross_correlation_amplitude(A_bary=1.30)

        self.assertAlmostEqual(y_dcdm, 1.00, delta=0.01)
        self.assertLess(y_agn, 0.86)
        self.assertGreater(y_dcdm - y_agn, 0.12)

    def test_fisher_matrix_degeneracy_breaking(self):
        """
        Verifies that combining 10 multi-scale bandpowers and orthogonal tSZ gas prior
        breaks the local degeneracy, yielding sub-percent parameter errors and non-singular Fisher.
        """
        fisher_info = self.engine.compute_fisher_elements()
        # Cosmic shear alone is non-singular across multi-band
        self.assertGreater(fisher_info["det_shear"], 0.0)
        self.assertGreater(fisher_info["det_total"], 0.0)
        # Parameter errors are high-precision
        self.assertLess(fisher_info["sigma_f_dcdm"], 0.005)  # Under 0.5% uncertainty
        self.assertLess(fisher_info["sigma_A_bary"], 0.02)   # Under 0.02 uncertainty

    def test_arbitration_decision_quadrants(self):
        """
        Verifies that the arbitration test correctly classifies:
          - Pure DCDM mock data into Quadrant 1
          - Pure AGN feedback mock data into Quadrant 2
          - Hybrid scenario into Quadrant 3
        with > 10 sigma statistical power.
        """
        # Case 1: Pure DCDM observation
        res_dcdm = self.engine.execute_arbitration_test(
            s_curv_obs=0.992, g_tomo_obs=2.45, delta_stellar_obs=0.001, y_tsz_obs=0.99
        )
        self.assertEqual(res_dcdm.decision_quadrant, 1)
        self.assertIn("DCDM CONFIRMED", res_dcdm.verdict)
        self.assertGreater(res_dcdm.sigma_separation, 10.0)
        self.assertGreater(res_dcdm.p_dcdm, 0.999)

        # Case 2: Pure AGN feedback observation
        res_agn = self.engine.execute_arbitration_test(
            s_curv_obs=0.836, g_tomo_obs=1.72, delta_stellar_obs=0.108, y_tsz_obs=0.82
        )
        self.assertEqual(res_agn.decision_quadrant, 2)
        self.assertIn("STABLE CDM + AGN CONFIRMED", res_agn.verdict)
        self.assertGreater(res_agn.sigma_separation, 10.0)
        self.assertGreater(res_agn.p_agn, 0.999)

        # Case 3: Hybrid observation
        res_hybrid = self.engine.execute_arbitration_test(
            s_curv_obs=0.920, g_tomo_obs=2.10, delta_stellar_obs=0.040, y_tsz_obs=0.91
        )
        self.assertEqual(res_hybrid.decision_quadrant, 3)
        self.assertIn("HYBRID", res_hybrid.verdict)


if __name__ == "__main__":
    unittest.main()
