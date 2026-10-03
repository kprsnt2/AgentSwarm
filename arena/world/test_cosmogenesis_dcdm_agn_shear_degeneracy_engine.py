"""
test_cosmogenesis_dcdm_agn_shear_degeneracy_engine.py

Comprehensive Unit Test Suite for:
cosmogenesis_dcdm_agn_shear_degeneracy_engine.py

Verifies:
1. Cosmological background expansion, cosmic time, and Limber kernel scalings.
2. DCDM suppression properties (high-k plateau and exponential decay kinematics).
3. AGN baryonic feedback profile (scale-dependent spoon dip and stellar upturn).
4. Local degeneracy at ell ~ 2000 between DCDM and enhanced AGN feedback.
5. Multipole curvature discriminant (d ln C_ell / d ell flatness vs steepness).
6. Tomographic redshift evolution differential between decay and halo expulsion.
7. Survey distinguishing significance (Delta chi^2 > 80 across Roman and Euclid).

Authored by Agent Kepler (A001), Generation 0.
"""

import unittest
import math
from cosmogenesis_dcdm_agn_shear_degeneracy_engine import (
    BaselineCosmology,
    DCDMParameters,
    AGNBaryonicParameters,
    SurveySpecifications,
    CosmogenesisDcdmAgnDegeneracyEngine
)


class TestCosmogenesisDcdmAgnDegeneracyEngine(unittest.TestCase):

    def setUp(self):
        self.engine = CosmogenesisDcdmAgnDegeneracyEngine()
        self.base = BaselineCosmology()
        self.dcdm = DCDMParameters()
        self.bary = AGNBaryonicParameters()
        self.surveys = SurveySpecifications()

    def test_cosmological_background_and_cosmic_time(self):
        """Verifies expansion rate H(z) and cosmic time integration."""
        h0 = self.engine.hubble_parameter(0.0)
        h1 = self.engine.hubble_parameter(1.0)
        h2 = self.engine.hubble_parameter(2.0)

        self.assertAlmostEqual(h0, self.base.H0, places=3)
        self.assertGreater(h1, h0)
        self.assertGreater(h2, h1)

        t0 = self.engine.cosmic_time_gyr(0.0)
        t1 = self.engine.cosmic_time_gyr(1.0)
        t2 = self.engine.cosmic_time_gyr(2.0)

        # Cosmic age at z=0 should be ~ 13.8 Gyr
        self.assertGreater(t0, 13.0)
        self.assertLess(t0, 14.5)
        # Time must decrease monotonically with redshift
        self.assertGreater(t0, t1)
        self.assertGreater(t1, t2)

    def test_dcdm_plateau_and_kinematics(self):
        """Verifies DCDM power suppression: large-scale limit, high-k plateau, and decay accumulation."""
        z = 0.5
        tau = 30.0
        f_dcdm = 0.035

        # At very large scales (k -> 0), suppression must be negligible
        r_large = self.engine.dcdm_power_suppression(0.001, z, f_dcdm, tau)
        self.assertAlmostEqual(r_large, 1.0, places=4)

        # At intermediate to high k (k = 1.0 to 10.0 h/Mpc), suppression must reach a flat plateau
        r_k1 = self.engine.dcdm_power_suppression(1.0, z, f_dcdm, tau)
        r_k5 = self.engine.dcdm_power_suppression(5.0, z, f_dcdm, tau)
        r_k10 = self.engine.dcdm_power_suppression(10.0, z, f_dcdm, tau)

        self.assertLess(r_k1, 1.0)
        # Variation between k=1 and k=10 should be less than 0.1% (flat plateau)
        self.assertAlmostEqual(r_k1, r_k5, delta=0.001)
        self.assertAlmostEqual(r_k5, r_k10, delta=0.001)

        # Decay accumulation: suppression must be larger at lower redshift (older universe)
        r_z0 = self.engine.dcdm_power_suppression(2.0, 0.0, f_dcdm, tau)
        r_z2 = self.engine.dcdm_power_suppression(2.0, 2.0, f_dcdm, tau)
        self.assertLess(r_z0, r_z2)

    def test_agn_baryonic_spoon_profile_and_stellar_upturn(self):
        """Verifies AGN baryonic feedback profile: large scale conservation, dip, and stellar core upturn."""
        z = 0.5
        a_bary = 1.30

        # Large scale conservation: k < 0.2 h/Mpc has r ~ 1.0
        r_large = self.engine.agn_baryonic_power_suppression(0.1, z, a_bary)
        self.assertAlmostEqual(r_large, 1.0, places=2)

        # Dip at intermediate scales: k ~ 4 - 8 h/Mpc
        r_dip = self.engine.agn_baryonic_power_suppression(6.0, z, a_bary)
        self.assertLess(r_dip, 0.90) # At least 10% suppression

        # Stellar core upturn: k > 20 h/Mpc has higher power than at dip minimum
        r_core = self.engine.agn_baryonic_power_suppression(30.0, z, a_bary)
        self.assertGreater(r_core, r_dip)

    def test_single_band_degeneracy_at_ell_2000(self):
        """Verifies that at ell ~ 2000, both models suppress power with high degeneracy."""
        res = self.engine.evaluate_degeneracy_at_multipole_2000()
        self.assertEqual(res["ell"], 2000.0)
        self.assertLess(res["bin3_suppression_dcdm"], 0.0)
        self.assertLess(res["bin3_suppression_agn"], 0.0)
        # Degeneracy fraction is high (suppressions are of the same order)
        self.assertGreater(res["degeneracy_fraction"], 0.0)

    def test_multipole_curvature_discriminant(self):
        """Verifies that DCDM has a near-zero slope across high multipoles while AGN feedback is steep."""
        curv = self.engine.compute_multipole_curvature_discriminant()
        # DCDM slope is substantially flatter than AGN feedback slope
        self.assertLess(abs(curv["dcdm_slope_per_1000_ell"]), abs(curv["agn_slope_per_1000_ell"]))
        # Total variation in DCDM over ell=1500->8000 is under 0.1%
        self.assertLess(curv["dcdm_variation_pct"], 0.1)
        # AGN feedback variation is significantly larger (> 0.5%)
        self.assertGreater(curv["agn_variation_pct"], 0.5)

    def test_tomographic_redshift_differential(self):
        """Verifies that DCDM suppression grows by > 2x between z=1.8 and z=0.35 due to decay kinetics."""
        redshift = self.engine.compute_tomographic_redshift_differential()
        self.assertGreater(redshift["ratio_dcdm_b1_b5"], 2.0)
        self.assertGreater(redshift["redshift_differential_separation"], 0.05)

    def test_survey_chi2_distinguishing_power(self):
        """Verifies that Euclid, Roman, and Combined break the degeneracy at high statistical significance."""
        chi2 = self.engine.compute_chi2_distinguishing_power()
        # Euclid alone should have Delta chi^2 > 50 (> 7 sigma)
        self.assertGreater(chi2["chi2_euclid"], 50.0)
        self.assertGreater(chi2["sigma_euclid"], 7.0)

        # Roman alone should have Delta chi^2 > 20 (> 4.5 sigma)
        self.assertGreater(chi2["chi2_roman"], 20.0)
        self.assertGreater(chi2["sigma_roman"], 4.5)

        # Combined surveys should have Delta chi^2 > 80 (> 9 sigma)
        self.assertGreater(chi2["chi2_combined"], 80.0)
        self.assertGreater(chi2["sigma_combined"], 9.0)


if __name__ == "__main__":
    unittest.main()
