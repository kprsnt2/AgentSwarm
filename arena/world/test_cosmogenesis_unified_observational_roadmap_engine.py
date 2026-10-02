"""Unit tests for Cosmogenesis Unified Observational Roadmap & Bayesian Discrimination Engine.

Agent: Kepler (A001) | Generation: 0 | Domain: Origin of the Universe (Cosmogenesis)
Date: October 2026
"""

import unittest
import math
from cosmogenesis_unified_observational_roadmap_engine import (
    CosmicConstants,
    HotBigBangPillars,
    CanonicalOpenProblemsMatrix,
    BayesianCosmogenesisDiscrimination,
    run_comprehensive_analysis
)


class TestCosmicConstants(unittest.TestCase):
    """Test physical constants and derived scales."""

    def test_fundamental_constants(self):
        self.assertAlmostEqual(CosmicConstants.C, 299792458.0, places=1)
        self.assertGreater(CosmicConstants.H_BAR, 1.054e-34)
        self.assertLess(CosmicConstants.H_BAR, 1.055e-34)
        self.assertGreater(CosmicConstants.K_B, 1.380e-23)
        self.assertLess(CosmicConstants.K_B, 1.381e-23)
        self.assertGreater(CosmicConstants.G, 6.674e-11)
        self.assertLess(CosmicConstants.G, 6.675e-11)

    def test_planck_scales(self):
        # Planck mass ~ 2.176e-8 kg
        self.assertAlmostEqual(CosmicConstants.M_PL_SI * 1e8, 2.1764, delta=0.01)
        # Planck time ~ 5.391e-44 s
        self.assertAlmostEqual(CosmicConstants.T_PL_SI * 1e44, 5.3912, delta=0.01)
        # Planck density ~ 5.155e96 kg/m^3
        self.assertAlmostEqual(CosmicConstants.RHO_PL_SI * 1e-96, 5.155, delta=0.01)


class TestHotBigBangPillars(unittest.TestCase):
    """Test the quantitative evaluations of the 5 empirical pillars."""

    def test_cmb_thermodynamics(self):
        res = HotBigBangPillars.cmb_thermodynamics()
        self.assertAlmostEqual(res["T0_K"], 2.72548, places=4)
        # Peak frequency ~ 160.2 GHz
        self.assertAlmostEqual(res["nu_max_GHz"], 160.23, delta=0.5)
        # Peak wavelength ~ 1.063 mm
        self.assertAlmostEqual(res["lambda_max_mm"], 1.063, delta=0.01)
        # Photon number density ~ 411 cm^-3
        self.assertAlmostEqual(res["n_gamma_cm3"], 410.7, delta=1.0)
        # Energy density ~ 0.26 eV/cm^3
        self.assertAlmostEqual(res["rho_rad_eV_cm3"], 0.2606, delta=0.01)
        # FIRAS limits
        self.assertEqual(res["compton_distortion_y_limit"], 1.5e-5)
        self.assertEqual(res["chemical_potential_mu_limit"], 9.0e-5)
        self.assertEqual(res["max_spectral_deviation_ppm"], 50.0)

    def test_sbbn_kinetics(self):
        res = HotBigBangPillars.sbbn_kinetics()
        # Freeze-out ratio ~ 0.1986
        self.assertAlmostEqual(res["np_freeze"], 0.1986, delta=0.005)
        # Bottleneck ratio ~ 0.1412
        self.assertAlmostEqual(res["np_bbn"], 0.1412, delta=0.005)
        # Theoretical Y_p ~ 0.2474
        self.assertAlmostEqual(res["Y_p_sbbn"], 0.2474, delta=0.005)
        # Concordance with observed Y_p (0.245 +- 0.003) within 1 sigma
        self.assertLess(res["Y_p_concordance_sigma"], 1.0)
        # Primordial Lithium-7 deficit factor ~ 2.97x
        self.assertAlmostEqual(res["Li7_deficit_factor"], 2.96, delta=0.05)
        # Lithium tension > 9 sigma
        self.assertGreater(res["Li7_tension_sigma"], 9.0)

    def test_metric_expansion_dilation(self):
        res = HotBigBangPillars.metric_expansion_dilation(z=6.34)
        self.assertAlmostEqual(res["scale_factor_a"], 1.0 / 7.34, places=4)
        self.assertAlmostEqual(res["T_z_K"], 2.72548 * 7.34, places=2)
        self.assertAlmostEqual(res["time_dilation_factor"], 7.34, places=2)

    def test_acoustic_sound_horizon(self):
        res = HotBigBangPillars.acoustic_sound_horizon()
        self.assertAlmostEqual(res["r_s_Mpc"], 147.21, delta=0.1)
        self.assertAlmostEqual(res["theta_star_rad"] * 1e2, 1.041, delta=0.01)
        self.assertAlmostEqual(res["first_acoustic_peak_multipole"], 220.6, delta=2.0)

    def test_primordial_tilt_significance(self):
        res = HotBigBangPillars.primordial_tilt_significance()
        self.assertAlmostEqual(res["n_s"], 0.9649, places=4)
        # Scale invariance excluded at > 8 sigma
        self.assertGreater(res["exclusion_sigma"], 8.0)

    def test_hubble_tension_significance(self):
        res = HotBigBangPillars.hubble_tension_significance()
        self.assertAlmostEqual(res["Delta_H0"], 5.68, delta=0.05)
        self.assertAlmostEqual(res["tension_sigma"], 4.85, delta=0.1)

    def test_cosmological_constant_discrepancy(self):
        res = HotBigBangPillars.cosmological_constant_discrepancy()
        self.assertGreater(res["log10_mismatch"], 120.0)
        self.assertLess(res["log10_mismatch"], 124.0)


class TestCanonicalOpenProblemsMatrix(unittest.TestCase):
    """Test the complete matrix of 8 open problems."""

    def test_open_problems_count_and_keys(self):
        matrix = CanonicalOpenProblemsMatrix.get_matrix()
        self.assertEqual(len(matrix), 8)
        required_keys = {
            "id", "name", "theoretical_failure", "ground_truth_benchmark",
            "resolving_observation", "instrument", "falsification_metric", "threshold"
        }
        for item in matrix:
            self.assertTrue(required_keys.issubset(item.keys()))
            self.assertTrue(item["id"].startswith("OP-0"))
            self.assertGreater(len(item["name"]), 5)
            self.assertGreater(len(item["theoretical_failure"]), 20)
            self.assertGreater(len(item["resolving_observation"]), 20)
            self.assertGreater(len(item["instrument"]), 5)


class TestBayesianCosmogenesisDiscrimination(unittest.TestCase):
    """Test Bayesian model comparison across competitive cosmogenetic paradigms."""

    def setUp(self):
        self.bayes = BayesianCosmogenesisDiscrimination()

    def test_priors_normalization(self):
        self.assertEqual(len(self.bayes.priors), 4)
        self.assertAlmostEqual(sum(self.bayes.priors.values()), 1.0, places=5)
        for p in self.bayes.priors.values():
            self.assertAlmostEqual(p, 0.25, places=3)

    def test_standard_model_confirmation(self):
        dataset = {
            "r": (0.0033, 0.0005),
            "n_T": (-0.00041, 0.00010),
            "H0": (67.4, 0.5),
            "w0": (-1.00, 0.02),
            "wa": (0.00, 0.02),
            "Li7_gas": (4.68, 0.30)
        }
        res = self.bayes.evaluate_dataset(dataset)
        self.assertEqual(res["favored_model"], "M1_Singular_Inflationary_LambdaCDM")
        self.assertGreater(res["favored_posterior"], 0.95)
        self.assertGreater(res["entropy_reduction_bits"], 1.5)
        self.assertGreater(res["kl_divergence_bits"], 1.5)

    def test_quantum_bounce_discovery(self):
        dataset = {
            "r": (0.0020, 0.0005),
            "n_T": (0.035, 0.005),      # Strong blue tilt
            "H0": (67.4, 0.5),
            "w0": (-1.00, 0.02)
        }
        res = self.bayes.evaluate_dataset(dataset)
        # Should heavily disfavor standard inflation (which requires n_T < 0)
        self.assertLess(res["posteriors"]["M1_Singular_Inflationary_LambdaCDM"], 1e-10)
        # Should favor M2 (Bounce) or M3 (String gas)
        favored = res["favored_model"]
        self.assertIn(favored, ["M2_NonSingular_Quantum_Bounce", "M3_String_Gas_Emergent"])

    def test_early_dark_energy_discovery(self):
        dataset = {
            "H0": (73.0, 0.5),          # High H0 confirmed
            "w0": (-0.83, 0.05),        # Dynamical dark energy
            "wa": (-0.75, 0.15),
            "Li7_gas": (1.58, 0.10)     # Low primordial 7Li in gas
        }
        res = self.bayes.evaluate_dataset(dataset)
        self.assertEqual(res["favored_model"], "M4_Early_Dark_Energy_Modified_Gravity")
        self.assertGreater(res["favored_posterior"], 0.99)

    def test_end_to_end_analysis(self):
        res = run_comprehensive_analysis()
        self.assertIn("pillars", res)
        self.assertIn("canonical_open_problems", res)
        self.assertIn("scenarios", res)
        self.assertEqual(len(res["canonical_open_problems"]), 8)


if __name__ == "__main__":
    unittest.main()
