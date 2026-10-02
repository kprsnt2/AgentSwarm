"""
test_origin_of_universe_engine.py
==================================
Unit test suite for the Cosmogenesis Empirical Foundations and Open Problems Engine.
Validates:
1. Physical constants consistency.
2. CMB thermodynamics, Wien displacement, and FIRAS limits.
3. High-redshift T(z) = T0*(1+z) observational concordance.
4. BBN freeze-out kinetics, He-4 fraction, D/H abundance, and Lithium-7 anomaly.
5. Friedmann expansion integration, distances (comoving, luminosity, angular diameter).
6. Hubble tension and S8 tension statistical formulas.
7. Inflationary observables (Starobinsky model, Lyth bound, BICEP/Keck bounds).
8. Baryogenesis Sakharov criteria and Leptogenesis bounds.
9. Dark sector vacuum energy density mismatch and candidate landscapes.
10. Cosmological Open Problems registry completeness and resolving observation definitions.
"""

import math
import unittest
from origin_of_universe_engine import (
    PhysicalConstants,
    CosmologicalParameters,
    CMBBlackbodyThermodynamics,
    StandardBigBangNucleosynthesis,
    CosmicExpansionDynamics,
    TensionAnalyzer,
    InflationaryCosmology,
    BaryogenesisAnalysis,
    DarkSectorAnalysis,
    CosmogenesisOpenProblemsRegistry,
    CosmologicalOpenProblem
)


class TestPhysicalConstants(unittest.TestCase):
    """Tests fundamental physical constants and relationships."""

    def test_constants_consistency(self):
        """Ensure fundamental constants have physical dimensions and non-zero positive values."""
        self.assertGreater(PhysicalConstants.c, 2.99e8)
        self.assertGreater(PhysicalConstants.hbar, 1.0e-34)
        self.assertGreater(PhysicalConstants.k_B, 1.3e-23)
        self.assertGreater(PhysicalConstants.G, 6.6e-11)
        self.assertGreater(PhysicalConstants.m_n, PhysicalConstants.m_p)
        self.assertAlmostEqual(PhysicalConstants.delta_m_np_MeV, 1.293, places=2)

    def test_planck_mass_and_length(self):
        """Ensure Planck scales match definitions: l_Pl = sqrt(hbar * G / c^3), t_Pl = l_Pl / c."""
        hbar = PhysicalConstants.hbar
        G = PhysicalConstants.G
        c = PhysicalConstants.c
        expected_l_Pl = math.sqrt(hbar * G / (c ** 3))
        self.assertAlmostEqual(PhysicalConstants.l_Pl / expected_l_Pl, 1.0, places=3)
        expected_t_Pl = expected_l_Pl / c
        self.assertAlmostEqual(PhysicalConstants.t_Pl / expected_t_Pl, 1.0, places=3)


class TestCosmologicalParameters(unittest.TestCase):
    """Tests cosmological parameters and flat Lambda-CDM budget."""

    def setUp(self):
        self.params = CosmologicalParameters()

    def test_density_fractions_sum(self):
        """Check that Omega_m + Omega_Lambda + Omega_k == 1.0."""
        omega_sum = self.params.Omega_m + self.params.Omega_Lambda + self.params.Omega_k
        self.assertAlmostEqual(omega_sum, 1.0, places=5)

    def test_baryon_and_matter_fractions(self):
        """Ensure Omega_b ~ 0.049 and Omega_m ~ 0.31."""
        self.assertGreater(self.params.Omega_b, 0.04)
        self.assertLess(self.params.Omega_b, 0.06)
        self.assertGreater(self.params.Omega_m, 0.28)
        self.assertLess(self.params.Omega_m, 0.34)
        self.assertGreater(self.params.Omega_Lambda, 0.65)
        self.assertLess(self.params.Omega_Lambda, 0.72)


class TestCMBBlackbodyThermodynamics(unittest.TestCase):
    """Tests CMB blackbody thermodynamics and FIRAS distortion boundaries."""

    def setUp(self):
        self.cmb = CMBBlackbodyThermodynamics(T0=2.72548)

    def test_wien_displacement_peak(self):
        """Check Wien frequency and wavelength peaks."""
        nu_max = self.cmb.peak_frequency()
        lambda_max = self.cmb.peak_wavelength()
        # nu_max ~ 160 GHz
        self.assertGreater(nu_max, 1.5e11)
        self.assertLess(nu_max, 1.7e11)
        # lambda_max ~ 1.06 mm = 1.06e-3 m
        self.assertGreater(lambda_max, 1.0e-3)
        self.assertLess(lambda_max, 1.1e-3)

    def test_photon_and_energy_density(self):
        """Verify CMB photon density ~ 411 photons/cm^3 and energy density ~ 0.26 eV/cm^3."""
        n_gamma_m3 = self.cmb.photon_number_density()
        n_gamma_cm3 = n_gamma_m3 / 1e6
        self.assertAlmostEqual(n_gamma_cm3, 410.7, delta=1.0)

        rho_J_m3 = self.cmb.energy_density()
        rho_eV_cm3 = (rho_J_m3 / PhysicalConstants.eV_to_J) / 1e6
        self.assertAlmostEqual(rho_eV_cm3, 0.2606, delta=0.01)

    def test_temperature_scaling_with_redshift(self):
        """Verify T(z) = T0 * (1+z) exactly."""
        self.assertAlmostEqual(self.cmb.temperature_at_redshift(0.0), 2.72548, places=4)
        self.assertAlmostEqual(self.cmb.temperature_at_redshift(1.0), 2.72548 * 2.0, places=4)
        self.assertAlmostEqual(self.cmb.temperature_at_redshift(9.0), 2.72548 * 10.0, places=4)

    def test_high_redshift_measurements(self):
        """Verify observational tests at high redshift (e.g. Riechers et al. 2022 at z=6.34)."""
        obs_results = self.cmb.verify_high_redshift_measurements()
        for obs in obs_results:
            self.assertTrue(obs["consistent_within_2sigma"])

    def test_firas_distortion_limits(self):
        """Verify FIRAS spectral distortion limits (|y| < 1.5e-5, |mu| < 9e-5)."""
        firas = self.cmb.verify_firas_distortion_limits()
        self.assertLessEqual(firas["y_distortion_limit"], 1.5e-5)
        self.assertLessEqual(firas["mu_distortion_limit"], 9.0e-5)
        self.assertTrue(firas["is_blackbody_within_firas_limits"])


class TestStandardBigBangNucleosynthesis(unittest.TestCase):
    """Tests primordial nucleosynthesis, abundances, and lithium tension."""

    def setUp(self):
        self.bbn = StandardBigBangNucleosynthesis(omega_b=0.02237)

    def test_freezeout_and_bbn_ratios(self):
        """Ensure (n/p) ratio freezes around 1/5 - 1/6 and drops to ~ 1/7 at BBN."""
        np_freeze = self.bbn.calculate_freezeout_neutron_fraction(0.80)
        np_bbn = self.bbn.calculate_bbn_neutron_fraction(0.80, 300.0)
        self.assertGreater(np_freeze, 0.18)
        self.assertLess(np_freeze, 0.22)
        self.assertGreater(np_bbn, 0.13)
        self.assertLess(np_bbn, 0.16)

    def test_helium4_mass_fraction(self):
        """Ensure predicted Helium-4 mass fraction Y_p is within 25% +/- 1%."""
        Y_p = self.bbn.calculate_primordial_helium_mass_fraction()
        self.assertGreater(Y_p, 0.24)
        self.assertLess(Y_p, 0.255)

    def test_deuterium_abundance(self):
        """Ensure (D/H)_p matches Cooke et al. 2018 value (2.54e-5)."""
        dh = self.bbn.calculate_deuterium_abundance()
        self.assertAlmostEqual(dh * 1e5, 2.54, delta=0.1)

    def test_lithium_problem_severity(self):
        """Verify the Lithium-7 anomaly is severe (> 5 sigma, discrepancy factor ~ 3)."""
        li_eval = self.bbn.evaluate_lithium_problem()
        self.assertGreater(li_eval["discrepancy_factor"], 2.5)
        self.assertLess(li_eval["discrepancy_factor"], 3.5)
        self.assertGreater(li_eval["tension_sigma"], 5.0)
        self.assertTrue(li_eval["is_tension_severe"])


class TestCosmicExpansionDynamics(unittest.TestCase):
    """Tests Friedmann equation and cosmological distance integrals."""

    def setUp(self):
        self.expansion = CosmicExpansionDynamics()

    def test_hubble_parameter_at_z0(self):
        """Check H(z=0) matches H0."""
        self.assertAlmostEqual(self.expansion.hubble_parameter(0.0), 67.36, places=2)

    def test_monotonic_distance_scaling(self):
        """Ensure comoving and luminosity distances increase monotonically with redshift."""
        dc_05 = self.expansion.comoving_distance_Mpc(0.5)
        dc_10 = self.expansion.comoving_distance_Mpc(1.0)
        dc_20 = self.expansion.comoving_distance_Mpc(2.0)
        self.assertGreater(dc_10, dc_05)
        self.assertGreater(dc_20, dc_10)

        dl_05 = self.expansion.luminosity_distance_Mpc(0.5)
        dl_10 = self.expansion.luminosity_distance_Mpc(1.0)
        self.assertGreater(dl_10, dl_05)

    def test_etherington_distance_duality(self):
        """Etherington reciprocity theorem: D_L = (1 + z)^2 * D_A."""
        z = 1.5
        dl = self.expansion.luminosity_distance_Mpc(z)
        da = self.expansion.angular_diameter_distance_Mpc(z)
        ratio = dl / (da * ((1.0 + z) ** 2))
        self.assertAlmostEqual(ratio, 1.0, places=4)


class TestTensionAnalyzer(unittest.TestCase):
    """Tests statistical tension evaluation for H0 and S8."""

    def test_hubble_tension_significance(self):
        """Verify SH0ES vs Planck tension is near ~5 sigma."""
        analyzer = TensionAnalyzer()
        res = analyzer.analyze_hubble_tension()
        shoes_planck = res["shoes_vs_planck"]
        self.assertGreater(shoes_planck["delta_H0"], 5.0)
        self.assertGreater(shoes_planck["tension_sigma"], 4.5)
        self.assertTrue(shoes_planck["is_tension_critical"])

    def test_s8_tension(self):
        """Verify S8 tension between KiDS-1000/DES and Planck."""
        analyzer = TensionAnalyzer()
        s8_res = analyzer.analyze_s8_tension()
        self.assertGreater(s8_res["KiDS1000_S8"]["tension_sigma"], 2.0)


class TestInflationaryCosmology(unittest.TestCase):
    """Tests inflation predictions, Lyth bound, and tensor-to-scalar ratio."""

    def setUp(self):
        self.inflation = InflationaryCosmology(N_efolds=60.0)

    def test_starobinsky_model_observables(self):
        """Verify Starobinsky model yields n_s ~ 0.967, r ~ 0.0033."""
        star = self.inflation.starobinsky_model()
        self.assertAlmostEqual(star["spectral_index_ns"], 0.9667, delta=0.001)
        self.assertAlmostEqual(star["tensor_to_scalar_ratio_r"], 0.00333, delta=0.0005)
        self.assertLess(star["tensor_spectral_index_nT"], 0.0)

    def test_lyth_bound(self):
        """Verify field excursion Delta phi / M_Pl >= sqrt(r/8) * N."""
        r = 0.01
        delta_phi = self.inflation.lyth_bound(r)
        expected = math.sqrt(0.01 / 8.0) * 60.0
        self.assertAlmostEqual(delta_phi, expected, places=4)

    def test_energy_scale_calculation(self):
        """Check energy scale V^(1/4) for r ~ 0.036 is around ~ 1.6e16 GeV (GUT scale)."""
        v_scale = self.inflation.inflation_energy_scale_GeV(0.036)
        self.assertGreater(v_scale, 1.0e16)
        self.assertLess(v_scale, 3.0e16)


class TestBaryogenesisAnalysis(unittest.TestCase):
    """Tests evaluation of Sakharov criteria in Standard Model."""

    def test_sakharov_failure_in_standard_model(self):
        """Ensure engine correctly identifies SM failure in CP violation and EW crossover."""
        baryon = BaryogenesisAnalysis()
        eval_res = baryon.evaluate_sakharov_conditions()
        self.assertEqual(eval_res["cp_violation"]["status"], "Failed in Standard Model")
        self.assertEqual(eval_res["departure_from_equilibrium"]["status"], "Failed in Standard Model")
        self.assertGreater(eval_res["cp_violation"]["deficit_orders_of_magnitude"], 8)

    def test_leptogenesis_davidson_ibarra_bound(self):
        """Verify Davidson-Ibarra lower bound M_N1 >= 10^9 GeV."""
        baryon = BaryogenesisAnalysis()
        lepto = baryon.leptogenesis_bounds()
        self.assertGreaterEqual(lepto["davidson_ibarra_bound_M_N1_GeV"], 1.0e9)


class TestDarkSectorAnalysis(unittest.TestCase):
    """Tests cosmological constant mismatch and dark matter boundaries."""

    def test_cosmological_constant_120_orders_of_magnitude(self):
        """Verify vacuum energy discrepancy is ~120 orders of magnitude."""
        dark = DarkSectorAnalysis()
        res = dark.cosmological_constant_discrepancy()
        self.assertGreaterEqual(res["log10_mismatch_vs_Planck"], 119.0)
        self.assertLessEqual(res["log10_mismatch_vs_Planck"], 123.0)

    def test_dark_matter_candidates_presence(self):
        """Verify WIMP, Axion, Fuzzy DM, and PBH candidates are present."""
        dark = DarkSectorAnalysis()
        candidates = dark.dark_matter_candidate_landscape()
        names = [c["candidate"] for c in candidates]
        self.assertTrue(any("WIMP" in n for n in names))
        self.assertTrue(any("Axion" in n for n in names))
        self.assertTrue(any("Fuzzy" in n for n in names))
        self.assertTrue(any("Primordial Black Hole" in n for n in names))


class TestOpenProblemsRegistry(unittest.TestCase):
    """Tests the Cosmogenesis Open Problems Registry."""

    def setUp(self):
        self.registry = CosmogenesisOpenProblemsRegistry()

    def test_all_canonical_problems_registered(self):
        """Ensure 8 canonical open problems are present with resolving observations."""
        self.assertEqual(len(self.registry.problems), 8)
        ids = [p.problem_id for p in self.registry.problems]
        self.assertEqual(ids, ["OP-01", "OP-02", "OP-03", "OP-04", "OP-05", "OP-06", "OP-07", "OP-08"])

    def test_problem_attributes_populated(self):
        """Verify all problems contain non-empty attributes and target instruments."""
        for p in self.registry.problems:
            self.assertTrue(p.title)
            self.assertTrue(p.theoretical_barrier)
            self.assertTrue(p.what_theory_does_not_explain)
            self.assertTrue(p.resolving_observation)
            self.assertGreater(len(p.target_instruments), 0)
            self.assertTrue(p.falsification_metric)


if __name__ == "__main__":
    unittest.main()
