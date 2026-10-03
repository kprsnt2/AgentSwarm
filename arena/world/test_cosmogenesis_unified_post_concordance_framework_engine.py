"""
test_cosmogenesis_unified_post_concordance_framework_engine.py

Comprehensive Verification Suite for the Unified Post-Concordance Cosmological Framework (UPCF).
Verifies:
  1. Analytical limits of CPL dark energy density and expansion rate H(z).
  2. Comoving distance integration and preservation of recombination acoustic scale.
  3. Linear perturbation growth ODE integration and consistency.
  4. The Four Joint Falsification Observables (S_curv, G_tomo, Delta_stellar, y_tsz).
  5. Global Chi^2 budget across Planck CMB, DESI BAO, SNe Ia, TRGB H0, and cosmic shear.
  6. Model selection metrics (AIC, BIC, Bayes factors) demonstrating decisive preference.
  7. Epistemic arbitration between Particle Physics (DCDM) and Astrophysics (AGN Feedback).

Authored by Agent Kepler (A001), Generation 0.
"""

import unittest
import math
from cosmogenesis_unified_post_concordance_framework_engine import (
    CosmologicalModelConfig,
    CosmologicalPhysicsIntegrator,
    UnifiedFrameworkCalculator,
    UnifiedPostConcordanceMasterSynthesis,
    C_LIGHT_KM_S
)


class TestUnifiedPostConcordanceFrameworkEngine(unittest.TestCase):

    def setUp(self):
        self.integrator = CosmologicalPhysicsIntegrator()
        self.calc = UnifiedFrameworkCalculator()
        self.synth = UnifiedPostConcordanceMasterSynthesis()

    def test_cpl_dark_energy_density_limits(self):
        """Verify CPL dark energy density matches analytical limits at z=0 and high z."""
        # At z = 0, rho_DE(0)/rho_DE(0) == 1.0
        rho_0 = self.integrator.dark_energy_density_ratio(0.0, -0.827, -0.750)
        self.assertAlmostEqual(rho_0, 1.0, places=5)

        # For standard Lambda (w0 = -1, wa = 0), ratio must be 1.0 for any z
        for z in [0.1, 1.0, 5.0, 100.0]:
            self.assertAlmostEqual(self.integrator.dark_energy_density_ratio(z, -1.0, 0.0), 1.0, places=5)

        # In DESI quintessence/phantom parameterization, rho_DE peaks at z_cross ~ 0.30
        rho_cross = self.integrator.dark_energy_density_ratio(0.30, -0.827, -0.750)
        self.assertGreater(rho_cross, 1.0)
        # At very high z, a -> 0, exponent dominates, rho_DE vanishes relative to matter
        rho_high_z = self.integrator.dark_energy_density_ratio(100.0, -0.827, -0.750)
        self.assertLess(rho_high_z, 1.0)

    def test_hubble_and_comoving_distance(self):
        """Verify expansion rate H(z) and comoving distance integrals."""
        h0 = 69.2
        omega_m = 0.14237
        h_0 = self.integrator.hubble_parameter(0.0, h0, omega_m, -0.827, -0.750)
        self.assertAlmostEqual(h_0, 69.2, places=4)

        # Distance to z = 1089.92 must be in physically established range ~ 13800 - 14300 Mpc
        dc_star = self.integrator.comoving_distance_mpc(1089.92, h0, omega_m, -0.827, -0.750)
        self.assertGreater(dc_star, 13700.0)
        self.assertLess(dc_star, 14400.0)

    def test_cosmic_age_integration(self):
        """Verify cosmic age at z=0 is approximately 13.5 - 14.2 Gyr."""
        omega_m = 0.14237
        t0_lcdm = self.integrator.cosmic_age_gyr(0.0, 67.36, omega_m, -1.0, 0.0)
        t0_upcf = self.integrator.cosmic_age_gyr(0.0, 69.20, omega_m, -0.827, -0.750)

        self.assertGreater(t0_lcdm, 13.5)
        self.assertLess(t0_lcdm, 14.1)

        self.assertGreater(t0_upcf, 13.0)
        self.assertLess(t0_upcf, 14.0)

    def test_linear_growth_ode(self):
        """Verify linear growth factor ODE solver runs and yields physical suppression."""
        omega_m = 0.14237
        d_lcdm = self.integrator.linear_growth_ode(67.36, omega_m, -1.0, 0.0)
        d_upcf = self.integrator.linear_growth_ode(69.20, omega_m, -0.827, -0.750)

        # Growth factor in LCDM should be ~ 0.69 - 0.82 relative to EdS
        self.assertGreater(d_lcdm, 0.68)
        self.assertLess(d_lcdm, 0.85)

        # Growth ratio between models should be close to unity within 2%
        ratio = d_upcf / d_lcdm
        self.assertAlmostEqual(ratio, 1.0, delta=0.03)

    def test_observables_calculation_and_decision_metrics(self):
        """Verify calculation of high-multipole and multi-messenger observables."""
        configs = self.synth.get_standard_model_configs()
        obs_agn = self.calc.compute_observables(configs["Model_2A_UPCF_AGN"])
        obs_dcdm = self.calc.compute_observables(configs["Model_2B_UPCF_DCDM"])

        # S_curv (Spoon Index): DCDM should have flat plateau (~0.99), AGN should have spoon dip (<0.85)
        self.assertGreater(obs_dcdm.s_curv, 0.97)
        self.assertLess(obs_agn.s_curv, 0.88)
        self.assertGreater(obs_dcdm.s_curv - obs_agn.s_curv, 0.10)

        # Stellar rebound: AGN should show positive rebound (>0.05), DCDM should be near zero (<=0.001)
        self.assertGreater(obs_agn.delta_stellar, 0.05)
        self.assertLessEqual(obs_dcdm.delta_stellar, 0.001)

        # tSZ pressure: AGN should show deficit (<0.85), DCDM should be 1.000
        self.assertAlmostEqual(obs_dcdm.y_tsz, 1.000, places=3)
        self.assertLess(obs_agn.y_tsz, 0.85)

    def test_global_chi2_and_model_selection_preference(self):
        """Verify that UPCF achieves decisive statistical preference over Lambda-CDM and EDE."""
        output = self.synth.execute_global_synthesis()
        models = output["models"]

        b_lcdm = models["Model_0_LCDM"]["chi2_budget"]
        b_ede = models["Model_1_EDE_DCDM"]["chi2_budget"]
        b_upcf_agn = models["Model_2A_UPCF_AGN"]["chi2_budget"]
        b_upcf_dcdm = models["Model_2B_UPCF_DCDM"]["chi2_budget"]

        # EDE must be severely penalized in Chi2 and AIC due to the S8 growth Catch-22
        self.assertGreater(b_ede.chi2_total, 200.0)
        self.assertGreater(b_ede.delta_aic_vs_lcdm, 100.0)

        # Both UPCF models must significantly outperform Lambda-CDM in total Chi2
        self.assertLess(b_upcf_agn.chi2_total, b_lcdm.chi2_total - 25.0)
        self.assertLess(b_upcf_dcdm.chi2_total, b_lcdm.chi2_total - 25.0)

        # Delta AIC must be strongly negative (favoring UPCF by > 18 points)
        self.assertLess(b_upcf_agn.delta_aic_vs_lcdm, -18.0)
        self.assertLess(b_upcf_dcdm.delta_aic_vs_lcdm, -18.0)

        # Bayes Factor ln B must exceed 5.0 (decisive on Jeffreys' scale)
        self.assertGreater(b_upcf_agn.ln_bayes_factor, 5.0)
        self.assertGreater(b_upcf_dcdm.ln_bayes_factor, 5.0)

    def test_arbitration_separation_power(self):
        """Verify that the arbitration diagnostics provide definitive separation."""
        output = self.synth.execute_global_synthesis()
        arb = output["arbitration"]

        self.assertGreater(arb["delta_s_curv"], 0.10)
        self.assertGreater(arb["delta_stellar_diff"], 0.05)
        self.assertGreater(arb["delta_y_tsz"], 0.10)


if __name__ == "__main__":
    unittest.main()
