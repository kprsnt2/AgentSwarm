"""
test_cosmogenesis_desi_trgb_minimal_concordance_engine.py

Comprehensive Unit Test Suite for:
cosmogenesis_desi_trgb_minimal_concordance_engine.py

Verifies:
1. Physical constants and baseline values.
2. Comoving distance integration and CPL dark energy density evolution.
3. Acoustic angular scale preservation under w0waCDM + TRGB.
4. Linear perturbation growth ODE integration and S_8 tension alleviation.
5. Akaike Information Criterion (AIC) decisive preference over EDE+DCDM.
6. Quantitative attack on the weakest assumption (Cepheid vs TRGB bias).

Authored by Agent Raman (A002), Generation 0.
"""

import unittest
import math
from cosmogenesis_desi_trgb_minimal_concordance_engine import (
    BaselineCosmology,
    EmpiricalObservables,
    CosmologicalExpansionModel,
    EpicycleVsConcordanceSynthesis
)


class TestDesiTrgbMinimalConcordanceEngine(unittest.TestCase):

    def setUp(self):
        self.synth = EpicycleVsConcordanceSynthesis()
        self.base = BaselineCosmology()
        self.obs = EmpiricalObservables()
        self.model = CosmologicalExpansionModel()

    def test_dark_energy_density_evolution_cpl(self):
        """Test that CPL dark energy density matches analytical limits."""
        # At z=0, a=1, rho_DE(0)/rho_DE(0) must equal 1.0
        ratio_0 = self.model.dark_energy_density_ratio(0.0, -0.827, -0.750)
        self.assertAlmostEqual(ratio_0, 1.0, places=5)

        # In standard Lambda-CDM (w0=-1, wa=0), rho_DE must be constant for all z
        for z in [0.5, 1.0, 2.0, 10.0]:
            ratio_lcdm = self.model.dark_energy_density_ratio(z, -1.0, 0.0)
            self.assertAlmostEqual(ratio_lcdm, 1.0, places=5)

        # For DESI (w0=-0.827, wa=-0.750), at z=0.30, rho_DE peaks above 1.0
        ratio_desi_peak = self.model.dark_energy_density_ratio(0.30, -0.827, -0.750)
        self.assertGreater(ratio_desi_peak, 1.0)

    def test_hubble_parameter_monotonicity(self):
        """Test that H(z) increases monotonically with redshift."""
        h_0 = self.model.hubble_parameter(0.0, 69.0, self.base.omega_m, self.base.omega_r, -0.827, -0.750)
        h_1 = self.model.hubble_parameter(1.0, 69.0, self.base.omega_m, self.base.omega_r, -0.827, -0.750)
        h_star = self.model.hubble_parameter(self.base.z_star, 69.0, self.base.omega_m, self.base.omega_r, -0.827, -0.750)

        self.assertAlmostEqual(h_0, 69.0, places=4)
        self.assertGreater(h_1, h_0)
        self.assertGreater(h_star, h_1)

    def test_comoving_distance_and_acoustic_scale(self):
        """Test comoving distance calculation and angular acoustic scale preservation."""
        dm_star = self.model.comoving_distance_integral(
            z_max=self.base.z_star,
            H0=self.obs.H0_trgb,
            omega_m=self.base.omega_m,
            omega_r=self.base.omega_r,
            w0=self.obs.w0_desi,
            wa=self.obs.wa_desi
        )
        # Comoving distance to recombination is approx 13,800 - 14,200 Mpc
        self.assertGreater(dm_star, 13500.0)
        self.assertLess(dm_star, 14500.0)

        theta_inferred, theta_pull = self.synth.evaluate_angular_acoustic_scale(
            H0=self.obs.H0_trgb,
            w0=self.obs.w0_desi,
            wa=self.obs.wa_desi,
            r_s_star=self.base.r_s_star_planck
        )
        # Acoustic scale theta_* matches Planck within 2% without changing r_s
        self.assertAlmostEqual(theta_inferred, self.base.theta_star, delta=0.0003)

    def test_s8_growth_suppression_and_alleviation(self):
        """Test exact ODE growth factor integration and S_8 tension evaluation."""
        res = self.synth.calculate_s8_alleviation(
            H0=self.obs.H0_trgb,
            w0=self.obs.w0_desi,
            wa=self.obs.wa_desi
        )
        # Omega_m at H0=69.0 should be lower than Planck Lambda-CDM (0.315 -> approx 0.299)
        self.assertLess(res["Omega_m"], 0.305)
        self.assertGreater(res["Omega_m"], 0.295)

        # Growth ratio from ODE integration should be close to 0.999
        self.assertAlmostEqual(res["growth_ratio"], 0.999, delta=0.005)

        # S_8 drops from Planck LCDM (0.832) to approx 0.809
        self.assertLess(res["S8"], 0.815)
        self.assertGreater(res["S8"], 0.800)

        # Tension with KiDS/DES (0.766) drops from 3.45 sigma to approx 2.8 sigma
        self.assertLess(res["S8_tension_sigma"], 3.0)
        self.assertGreater(res["S8_tension_sigma"], 2.0)

    def test_model_selection_decisive_preference(self):
        """Test that w0waCDM + TRGB decisively beats EDE + DCDM under AIC."""
        comp = self.synth.evaluate_model_selection()

        # Epicycle model has 11 parameters, Concordance has 8 parameters
        self.assertEqual(comp["k_epicycle"], 11)
        self.assertEqual(comp["k_concordance"], 8)

        # AIC difference should strongly favor Concordance (Delta AIC <= -10)
        self.assertLessEqual(comp["delta_aic_vs_epicycle"], -10.0)
        self.assertEqual(comp["bayesian_preference"], "Decisive (Delta AIC < -10)")

    def test_weakest_assumption_attack_quantification(self):
        """Test quantitative boundary of the weakest assumption (Cepheid vs TRGB bias)."""
        attack = self.synth.attack_weakest_assumption()

        # Delta H0 between SH0ES and TRGB is 4.04 km/s/Mpc
        self.assertAlmostEqual(attack["delta_H0"], 4.04, places=2)

        # Distance modulus discrepancy Delta mu ~ 0.12 mag
        self.assertAlmostEqual(attack["delta_mu_mag"], 0.123, places=2)

        # Residual S8 tension is quantified around 2.83 sigma
        self.assertGreater(attack["residual_s8_tension"], 2.5)


if __name__ == "__main__":
    unittest.main()
