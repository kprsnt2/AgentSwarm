"""
Unit and Verification Test Suite for Extraterrestrial Life Epistemic Engine
Agent: Agent5 (A006, Gen 0)
Ledger Reference: world/test_extraterrestrial_life_analyzer.py
"""

import math
import unittest

from extraterrestrial_life_analyzer import (
    C, G, K_B, SIGMA_SB, WIEN_B, AU, LIGHT_YEAR, L_SUN, T_EFF_SUN, R_SUN, R_EARTH, G_EARTH,
    BiogenesisBiosphereModel,
    TechnosignatureFermiModel,
    InterstellarVisitationModel,
    ExtraterrestrialEpistemicEngine,
    HabitableZoneBoundaries,
    ChemicalDisequilibriumResult,
    DrakeEquationMonteCarlo,
    CosmicHaystackFraction,
    RelativisticKinematicsResult,
    BayesianVisitationEvaluation,
)


class TestPhysicalConstantsAndBasics(unittest.TestCase):
    """Verifies fundamental physical and astronomical constants."""

    def test_constants_accuracy(self):
        self.assertAlmostEqual(C, 299792458.0, places=1)
        self.assertAlmostEqual(G, 6.67430e-11, delta=1e-15)
        self.assertAlmostEqual(K_B, 1.380649e-23, delta=1e-28)
        self.assertAlmostEqual(SIGMA_SB, 5.670374419e-8, delta=1e-14)
        self.assertAlmostEqual(WIEN_B, 2.897771955e-3, places=9)
        self.assertAlmostEqual(AU, 1.495978707e11, delta=100.0)
        self.assertAlmostEqual(LIGHT_YEAR, 9.460730472e15, delta=1e9)


class TestQuestion1BiogenesisBiospheres(unittest.TestCase):
    """Verifies physical, chemical, and spectroscopic models for Question 1."""

    def test_solar_habitable_zone_boundaries(self):
        """Earth (1.0 AU) must lie strictly inside the Sun's conservative habitable zone."""
        hz = BiogenesisBiosphereModel.calculate_habitable_zone(
            stellar_teff_k=T_EFF_SUN,
            stellar_luminosity_solar=1.0
        )
        self.assertIsInstance(hz, HabitableZoneBoundaries)
        # Check ordering of boundaries: Recent Venus < Runaway Greenhouse < Maximum Greenhouse < Early Mars
        self.assertLess(hz.recent_venus_au, hz.runaway_greenhouse_au)
        self.assertLess(hz.runaway_greenhouse_au, hz.maximum_greenhouse_au)
        self.assertLess(hz.maximum_greenhouse_au, hz.early_mars_au)

        # Solar system baseline: 1.0 AU is inside Runaway GH (approx 0.95-0.99 AU) and Max GH (approx 1.67 AU)
        self.assertLess(hz.runaway_greenhouse_au, 1.0)
        self.assertGreater(hz.maximum_greenhouse_au, 1.0)
        self.assertGreater(hz.conservative_width_au, 0.5)

    def test_m_dwarf_habitable_zone(self):
        """An M-dwarf (e.g. TRAPPIST-1: Teff ~ 2566 K, L ~ 0.00055 L_sun) has an HZ much closer in."""
        hz_m = BiogenesisBiosphereModel.calculate_habitable_zone(
            stellar_teff_k=3000.0,
            stellar_luminosity_solar=0.01
        )
        self.assertLess(hz_m.runaway_greenhouse_au, 0.2)
        self.assertLess(hz_m.maximum_greenhouse_au, 0.3)

    def test_atmospheric_scale_height(self):
        """Earth atmosphere scale height should be approximately 8.0 - 8.5 km."""
        h_earth = BiogenesisBiosphereModel.atmospheric_scale_height(
            equilibrium_temp_k=288.15,
            mean_molecular_weight_amu=28.97,  # N2/O2 mix
            surface_gravity_m_s2=G_EARTH
        )
        self.assertGreater(h_earth, 7500.0)
        self.assertLess(h_earth, 9000.0)

    def test_transmission_spectroscopy_transit_depth(self):
        """Solid Earth transit is ~84 ppm; atmospheric annulus across 5 scale heights is ~1.1 ppm."""
        geom_depth = BiogenesisBiosphereModel.solid_planet_transit_depth(
            planet_radius_m=R_EARTH,
            stellar_radius_m=R_SUN
        )
        self.assertAlmostEqual(geom_depth, 8.39e-5, delta=1.0e-6)

        h_earth = 8400.0
        atm_depth_sun = BiogenesisBiosphereModel.transmission_spectroscopy_transit_depth(
            planet_radius_m=R_EARTH,
            stellar_radius_m=R_SUN,
            scale_height_m=h_earth,
            n_scale_heights=5.0
        )
        self.assertAlmostEqual(atm_depth_sun, 1.106e-6, delta=1.0e-7)

        # For an M-dwarf (e.g. R_* = 0.15 R_sun), the atmospheric signal is magnified by (1 / 0.15^2) ~ 44x
        atm_depth_mdwarf = BiogenesisBiosphereModel.transmission_spectroscopy_transit_depth(
            planet_radius_m=R_EARTH,
            stellar_radius_m=0.15 * R_SUN,
            scale_height_m=h_earth,
            n_scale_heights=5.0
        )
        self.assertGreater(atm_depth_mdwarf, 4.0e-5)
    def test_chemical_disequilibrium_ch4_o2(self):
        """Simultaneous presence of CH4 and O2 with low CO indicates strong biogenic disequilibrium."""
        res_bio = BiogenesisBiosphereModel.chemical_disequilibrium_ch4_o2(
            ch4_mixing_ratio=1.8e-6,      # Earth modern level ~ 1.8 ppm
            o2_mixing_ratio=0.2095,       # Earth modern level ~ 21%
            co2_mixing_ratio=4.15e-4,
            h2o_mixing_ratio=1.0e-2,
            co_mixing_ratio=1.0e-7        # Low CO due to biological consumption
        )
        self.assertTrue(res_bio.is_thermodynamically_disequilibrium)
        self.assertFalse(res_bio.abiotic_explanation_plausible)
        self.assertLess(res_bio.delta_g_actual_kj_per_mol, -700.0)
        self.assertGreater(res_bio.photochemical_flux_molecules_per_m2_s, 1.0e13)

    def test_abiotic_false_positive_co_photolysis(self):
        """High O2 accompanied by high CO (photolysis of CO2) flags an abiotic false positive."""
        res_abiotic = BiogenesisBiosphereModel.chemical_disequilibrium_ch4_o2(
            ch4_mixing_ratio=1.0e-8,
            o2_mixing_ratio=0.10,
            co_mixing_ratio=0.05          # Massive CO buildup indicates abiotic CO2 photolysis
        )
        self.assertTrue(res_abiotic.abiotic_explanation_plausible)
        self.assertIn("abiotic", res_abiotic.confidence_description.lower())


class TestQuestion2TechnosignaturesAndFermi(unittest.TestCase):
    """Verifies Drake equation, Monte Carlo, and Cosmic Haystack models for Question 2."""

    def test_drake_equation_point_estimate(self):
        """Standard Drake point estimate with textbook optimistic parameters."""
        n_est = TechnosignatureFermiModel.drake_equation_point_estimate(
            r_star=2.0, f_p=1.0, n_e=0.2, f_l=0.5, f_i=0.1, f_c=0.1, l_years=10000.0
        )
        self.assertAlmostEqual(n_est, 20.0, places=3)

    def test_drake_equation_monte_carlo_distribution(self):
        """Demonstrates that realistic epistemic uncertainty produces P(N < 1) > 0."""
        mc = TechnosignatureFermiModel.drake_equation_monte_carlo(n_samples=5000, random_seed=42)
        self.assertIsInstance(mc, DrakeEquationMonteCarlo)
        self.assertGreater(mc.p_alone_in_galaxy, 0.10)
        self.assertLess(mc.p_alone_in_galaxy, 0.90)
        self.assertGreater(mc.sample_size, 0)
        # Percentiles must be strictly monotonic
        self.assertLessEqual(mc.percentile_5, mc.median_n)
        self.assertLessEqual(mc.median_n, mc.percentile_95)

    def test_cosmic_haystack_fraction(self):
        """Historic and current SETI searches cover only a minute fraction (< 10^-14) of the 8D parameter space."""
        haystack = TechnosignatureFermiModel.cosmic_haystack_fraction(
            distance_searched_pc=50.0,
            bandwidth_searched_hz=5.0e8,
            eirp_detection_limit_w=1.0e14,
            sky_fraction_searched=0.01,
            duty_cycle_coverage=1.0e-4
        )
        self.assertIsInstance(haystack, CosmicHaystackFraction)
        self.assertLess(haystack.total_haystack_fraction_searched, 1.0e-12)
        self.assertLess(haystack.log10_haystack_fraction, -12.0)

    def test_dyson_sphere_waste_heat(self):
        """A complete Dyson sphere (alpha = 1.0) around a Sun-like star reradiates ~L_sun in mid-IR."""
        # 1. At 1 AU (outer-surface radiating shell: T = (L / 4*pi*R^2*sigma)^(1/4) ~ 393.6 K)
        p_waste_1au, t_waste_1au, lambda_peak_1au = TechnosignatureFermiModel.dyson_sphere_waste_heat(
            stellar_luminosity_w=L_SUN,
            interception_fraction_alpha=1.0,
            dyson_radius_m=AU
        )
        self.assertAlmostEqual(p_waste_1au, L_SUN, delta=1e20)
        self.assertAlmostEqual(t_waste_1au, 393.6, delta=2.0)
        self.assertAlmostEqual(lambda_peak_1au, 7.36, delta=0.2)

        # 2. At 2.0 AU, equilibrium temperature drops to comfortable room temperature (~278 K)
        _, t_waste_2au, lambda_peak_2au = TechnosignatureFermiModel.dyson_sphere_waste_heat(
            stellar_luminosity_w=L_SUN,
            interception_fraction_alpha=1.0,
            dyson_radius_m=2.0 * AU
        )
        self.assertAlmostEqual(t_waste_2au, 278.3, delta=2.0)
        self.assertAlmostEqual(lambda_peak_2au, 10.4, delta=0.5)

class TestQuestion3InterstellarVisitationAndArtefacts(unittest.TestCase):
    """Verifies relativistic flight physics, ISM impact energetics, and Bayesian evaluation for Question 3."""

    def test_relativistic_kinematics_at_01c(self):
        """At 0.1c, Lorentz factor is ~1.005, kinetic energy is ~4.5e14 J/kg (~108 MT TNT/kg)."""
        res = InterstellarVisitationModel.relativistic_kinematics(beta=0.1)
        self.assertIsInstance(res, RelativisticKinematicsResult)
        self.assertAlmostEqual(res.beta, 0.1, places=5)
        self.assertGreater(res.gamma, 1.004)
        self.assertLess(res.gamma, 1.006)
        self.assertGreater(res.kinetic_energy_per_kg, 4.0e14)
        self.assertGreater(res.tnt_kilotons_per_kg, 90.0)
        self.assertLess(res.tnt_kilotons_per_kg, 120.0)
        self.assertGreater(res.tnt_megatons_per_kg, 0.09)
        self.assertLess(res.tnt_megatons_per_kg, 0.12)
        # One-way trip to Proxima Centauri (~4.25 ly) takes ~42.5 years
        self.assertAlmostEqual(res.travel_time_proxima_years, 42.465, delta=0.5)

    def test_relativistic_kinematics_invalid_beta(self):
        """Invalid beta (< 0 or >= 1) must raise ValueError."""
        with self.assertRaises(ValueError):
            InterstellarVisitationModel.relativistic_kinematics(beta=0.0)
        with self.assertRaises(ValueError):
            InterstellarVisitationModel.relativistic_kinematics(beta=1.0)
        with self.assertRaises(ValueError):
            InterstellarVisitationModel.relativistic_kinematics(beta=1.5)

    def test_bayesian_visitation_extraordinary_evidence(self):
        """Extraordinary data (likelihood ratio > 10^11) can overcome even 10^-9 prior."""
        eval_high = InterstellarVisitationModel.evaluate_visitation_claim_bayes(
            prior_p_visit=1.0e-9,
            likelihood_data_given_et=0.99,
            likelihood_data_given_mundane=1.0e-12
        )
        self.assertGreater(eval_high.posterior_probability, 0.95)
        self.assertIn("supported", eval_high.epistemic_conclusion.lower())

    def test_isotopic_anomaly_invalid_sigma(self):
        """Non-positive standard deviation must raise ValueError."""
        with self.assertRaises(ValueError):
            InterstellarVisitationModel.isotopic_anomaly_sigma(1.0, 1.0, 0.0)
        with self.assertRaises(ValueError):
            InterstellarVisitationModel.isotopic_anomaly_sigma(1.0, 1.0, -0.5)

    def test_dust_impact_energetics_at_02c(self):
        """At 0.2c, even a 1-micron dust grain delivers significant kinetic energy."""
        res_02 = InterstellarVisitationModel.relativistic_kinematics(beta=0.2)
        self.assertGreater(res_02.micro_dust_impact_energy_j, 15.0)

    def test_relativistic_rocket_mass_ratio(self):
        """At 0.1c, fusion rocket (ve=0.05c) requires mass ratio > 7, while antimatter requires < 1.15."""
        res = InterstellarVisitationModel.relativistic_kinematics(beta=0.1)
        self.assertGreater(res.fusion_mass_ratio_one_way, 7.0)
        self.assertLess(res.fusion_mass_ratio_one_way, 8.0)
        self.assertGreater(res.antimatter_mass_ratio_one_way, 1.10)
        self.assertLess(res.antimatter_mass_ratio_one_way, 1.15)

    def test_bayesian_visitation_evaluation(self):
        """With prior P(ET) = 1e-9 and mundane likelihood = 1e-3, posterior remains negligible."""
        eval_res = InterstellarVisitationModel.evaluate_visitation_claim_bayes(
            prior_p_visit=1.0e-9,
            likelihood_data_given_et=0.90,
            likelihood_data_given_mundane=1.0e-3
        )
        self.assertIsInstance(eval_res, BayesianVisitationEvaluation)
        self.assertLess(eval_res.posterior_probability, 1.0e-5)
        self.assertIn("unsubstantiated", eval_res.epistemic_conclusion.lower())

    def test_isotopic_anomaly_sigma(self):
        """Tests 10-sigma threshold for physical non-terrestrial artefact demarcation."""
        sigma_5, is_anom_5 = InterstellarVisitationModel.isotopic_anomaly_sigma(
            measured_ratio=1.05, terrestrial_mean_ratio=1.00, terrestrial_std_dev=0.01
        )
        self.assertAlmostEqual(sigma_5, 5.0, places=2)
        self.assertFalse(is_anom_5)

        sigma_12, is_anom_12 = InterstellarVisitationModel.isotopic_anomaly_sigma(
            measured_ratio=1.12, terrestrial_mean_ratio=1.00, terrestrial_std_dev=0.01
        )
        self.assertAlmostEqual(sigma_12, 12.0, places=2)
        self.assertTrue(is_anom_12)


class TestSynthesisAndEpistemicRoadmap(unittest.TestCase):
    """Verifies that all three distinct questions possess falsifiable predictions and settling observations."""

    def test_three_questions_structure(self):
        synthesis = ExtraterrestrialEpistemicEngine.get_three_question_synthesis()
        self.assertIn("question_1_life_elsewhere", synthesis)
        self.assertIn("question_2_intelligent_life", synthesis)
        self.assertIn("question_3_visitation", synthesis)

        for q_key, q_data in synthesis.items():
            self.assertIn("question", q_data)
            self.assertIn("epistemic_status", q_data)
            self.assertIn("established_ground_truth", q_data)
            self.assertIn("falsifiable_prediction", q_data)
            self.assertIn("settling_observation", q_data)
            self.assertIn("falsification_condition", q_data)

            # Ensure none of the fields are empty or trivial placeholders
            self.assertGreater(len(q_data["falsifiable_prediction"]), 50)
            self.assertGreater(len(q_data["settling_observation"]), 50)
            self.assertGreater(len(q_data["falsification_condition"]), 50)


if __name__ == "__main__":
    unittest.main()
