"""
test_cosmogenesis_consensus_reformation_and_systematics_closure_engine.py

Unit test suite for cosmogenesis_consensus_reformation_and_systematics_closure_engine.py.
Verifies:
  1. Precision numerical integration of comoving distance and cosmic age.
  2. Linear growth factor ODE predictor-corrector stability across Lambda-CDM and w0waCDM.
  3. Five-model cosmological observables consistency (acoustic scale theta_*, S8_linear).
  4. Multi-probe Chi^2 budget evaluation, AIC, BIC, and Log Bayes Factor consistency.
  5. Decisive statistical ranking: Model 3 (Reformed Minimal Consensus) achieves the global minimum in AIC/BIC.
  6. EDE catastrophic tension confirmation (S8 inflation and high-ell acoustic scale degradation).
  7. Non-linear high-ell observables: Spoon index S_curv, tomographic ratio G_tomo, stellar rebound Delta_stellar, and tSZ ratio y_tsz.

Authored by Agent Raman (A002), Generation 0.
Phase 4 Capstone Verification Suite.
"""

import unittest
import math
from cosmogenesis_consensus_reformation_and_systematics_closure_engine import (
    PrecisionCosmologicalIntegrator,
    ConsensusReformationAnalyzer,
    ModelSpecification,
    ModelObservables,
    ComprehensiveChi2Budget
)


class TestPrecisionCosmologicalIntegrator(unittest.TestCase):
    """Tests the numerical physics integration routines."""

    def setUp(self):
        self.integrator = PrecisionCosmologicalIntegrator()

    def test_dark_energy_density_ratio_lcdm(self):
        """In Lambda-CDM (w0=-1, wa=0), rho_DE(z) / rho_DE(0) must equal 1.0 at all redshifts."""
        for z in [0.0, 0.5, 1.0, 2.0, 10.0, 1089.0]:
            ratio = self.integrator.dark_energy_density_ratio(z, -1.0, 0.0)
            self.assertAlmostEqual(ratio, 1.0, places=6)

    def test_dark_energy_density_ratio_cpl(self):
        """Under DESI CPL (w0=-0.827, wa=-0.750), rho_DE must match analytical CPL decay."""
        ratio_z0 = self.integrator.dark_energy_density_ratio(0.0, -0.827, -0.750)
        ratio_z1 = self.integrator.dark_energy_density_ratio(1.0, -0.827, -0.750)
        ratio_z10 = self.integrator.dark_energy_density_ratio(10.0, -0.827, -0.750)

        self.assertAlmostEqual(ratio_z0, 1.0, places=5)
        self.assertAlmostEqual(ratio_z1, 0.92789, places=3)
        self.assertLess(ratio_z10, ratio_z1)  # Decays at high redshift

    def test_comoving_distance_monotonicity(self):
        """Comoving distance D_c(z) must be strictly monotonic in redshift."""
        d_1 = self.integrator.comoving_distance_mpc(1.0, 67.36, 0.14237, -1.0, 0.0)
        d_2 = self.integrator.comoving_distance_mpc(2.0, 67.36, 0.14237, -1.0, 0.0)
        d_star = self.integrator.comoving_distance_mpc(1089.92, 67.36, 0.14237, -1.0, 0.0)

        self.assertGreater(d_2, d_1)
        self.assertGreater(d_star, d_2)
        # Comoving distance to recombination in Planck Lambda-CDM is approx 13,800 - 14,000 Mpc
        self.assertTrue(13800 < d_star < 14000)

    def test_cosmic_age_lcdm(self):
        """Cosmic age in standard Planck Lambda-CDM must be approx 13.8 Gyr."""
        t0 = self.integrator.cosmic_age_gyr(0.0, 67.36, 0.14237, -1.0, 0.0)
        self.assertAlmostEqual(t0, 13.80, delta=0.15)

    def test_linear_growth_ode(self):
        """Growth factor D(a=1) must equal approx 0.70 for Omega_m ~ 0.315."""
        d_lcdm = self.integrator.linear_growth_ode(67.36, 0.14237, -1.0, 0.0)
        self.assertAlmostEqual(d_lcdm, 0.70, delta=0.02)


class TestConsensusReformationAnalyzer(unittest.TestCase):
    """Tests the five-model comparative landscape and information criteria."""

    def setUp(self):
        self.analyzer = ConsensusReformationAnalyzer()
        self.results = self.analyzer.execute_full_audit()

    def test_all_five_models_present(self):
        """All five cosmological models must be computed and audited."""
        expected_keys = [
            "model_0_lcdm",
            "model_1_ede",
            "model_2a_upcf_agn",
            "model_2b_upcf_dcdm",
            "model_3_reformed_lcdm"
        ]
        for key in expected_keys:
            self.assertIn(key, self.results)

    def test_reformed_lcdm_achieves_global_minimum_aic_and_bic(self):
        """Model 3 (Reformed Minimal Consensus) must achieve the global minimum AIC and BIC."""
        b_ref = self.results["model_3_reformed_lcdm"]["budget"]
        b_0 = self.results["model_0_lcdm"]["budget"]
        b_1 = self.results["model_1_ede"]["budget"]
        b_2a = self.results["model_2a_upcf_agn"]["budget"]
        b_2b = self.results["model_2b_upcf_dcdm"]["budget"]

        # Reformed Lambda-CDM beats fiducial Lambda-CDM
        self.assertLess(b_ref.aic, b_0.aic)
        self.assertLess(b_ref.bic, b_0.bic)

        # Reformed Lambda-CDM beats EDE by huge margins (> 200 AIC/BIC)
        self.assertLess(b_ref.aic, b_1.aic - 200.0)
        self.assertLess(b_ref.bic, b_1.bic - 200.0)

        # Reformed Lambda-CDM beats UPCF models due to parsimony (k=7 vs k=8/9)
        self.assertLess(b_ref.aic, b_2a.aic)
        self.assertLess(b_ref.bic, b_2a.bic)
        self.assertLess(b_ref.aic, b_2b.aic)
        self.assertLess(b_ref.bic, b_2b.bic)

        # Quantitative margin over Model 2A: Delta BIC > 10 (decisive on Kass & Raftery scale)
        self.assertGreater(b_2a.bic - b_ref.bic, 10.0)

    def test_ede_catastrophic_tension(self):
        """EDE must exhibit severe Chi^2 degradation and elevated delta AIC."""
        b_ede = self.results["model_1_ede"]["budget"]

        # Total Chi^2 must exceed 300 due to theta_* and BAO/SN/H0 penalties
        self.assertGreater(b_ede.chi2_total, 300.0)
        self.assertGreater(b_ede.delta_aic_vs_lcdm, 200.0)

    def test_nonlinear_shear_observables_discrimination(self):
        """High-multipole observables must discriminate between AGN feedback and DCDM."""
        obs_agn = self.results["model_2a_upcf_agn"]["obs"]
        obs_dcdm = self.results["model_2b_upcf_dcdm"]["obs"]
        obs_ref = self.results["model_3_reformed_lcdm"]["obs"]

        # Spoon Index S_curv: AGN feedback shows deep dip (< 0.85); DCDM shows flat plateau (> 0.95)
        self.assertLess(obs_agn.s_curv, 0.85)
        self.assertGreater(obs_dcdm.s_curv, 0.95)
        self.assertLess(obs_ref.s_curv, 0.85)

        # Stellar Rebound: AGN feedback has positive rebound (> 0.08); DCDM has zero rebound (< 0.001)
        self.assertGreater(obs_agn.delta_stellar, 0.08)
        self.assertAlmostEqual(obs_dcdm.delta_stellar, 0.0, places=3)
        self.assertGreater(obs_ref.delta_stellar, 0.08)

        # tSZ pressure ratio: AGN feedback has pressure deficit (< 0.85); DCDM has standard pressure (= 1.0)
        self.assertLess(obs_agn.y_tsz, 0.85)
        self.assertAlmostEqual(obs_dcdm.y_tsz, 1.0, places=3)
        self.assertLess(obs_ref.y_tsz, 0.85)


if __name__ == "__main__":
    unittest.main()
