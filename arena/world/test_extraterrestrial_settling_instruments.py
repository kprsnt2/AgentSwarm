"""
Unit tests for extraterrestrial_settling_instruments.py
Agent: Sagan (A006, Gen 0)

These tests pin down the quantitative claims that the deliverable
(FALSIFIABLE_PREDICTIONS_AND_SETTLING_OBSERVATIONS.md) makes, and re-verify
the three self-corrections recorded in the module docstring.
"""

import math
import unittest

from extraterrestrial_settling_instruments import (
    BiosignatureCensusDesign,
    TechnosignatureDecidability,
    VisitationExpansionConstraint,
    SettlingInstrumentSynthesis,
    DISH_AREA_M2,
    system_equivalent_flux_density,
)


class TestSelfCorrections(unittest.TestCase):
    """Re-verify the three self-corrections recorded during development."""

    def test_s1_parent_engine_prior_is_075_not_035_to_045(self):
        """[S1] The parent engine's own code gives P(N<1) ~ 0.75, not 0.35-0.45."""
        from extraterrestrial_life_analyzer import TechnosignatureFermiModel
        result = TechnosignatureFermiModel.drake_equation_monte_carlo(
            n_samples=120000, random_seed=42)
        self.assertGreater(result.p_alone_in_galaxy, 0.70)
        self.assertLess(result.p_alone_in_galaxy, 0.80)

    def test_s2_disk_fraction_limits(self):
        """[S2] Enclosed fraction must obey both limiting regimes."""
        # Spherical regime (r << h): fraction -> (2/3) r^3 / (R^2 h)
        r = 50.0
        got = TechnosignatureDecidability.enclosed_disk_fraction(r)
        expected = (2.0 / 3.0) * r ** 3 / (15000.0 ** 2 * 300.0)
        self.assertAlmostEqual(got, expected, delta=0.05 * expected)
        # Column regime (h << r << R): fraction -> r^2 / R^2
        r = 1000.0
        got = TechnosignatureDecidability.enclosed_disk_fraction(r)
        expected = r ** 2 / 15000.0 ** 2
        self.assertAlmostEqual(got, expected, delta=0.05 * expected)
        # Full containment
        self.assertAlmostEqual(
            TechnosignatureDecidability.enclosed_disk_fraction(20000.0), 1.0, places=6)

    def test_s3_sefd_no_double_counting(self):
        """[S3] SEFD = 2 k T / (eta A) must not discount efficiency twice."""
        area = math.pi * 50.0 ** 2
        expected = 2.0 * 1.380649e-23 * 20.0 / (0.7 * area)
        self.assertAlmostEqual(system_equivalent_flux_density(area), expected, relative=1e-12)
        # 100-m reference dish should be ~10 Jy (0.1e-24 W/m^2/Hz)
        self.assertTrue(0.5e-25 < system_equivalent_flux_density(DISH_AREA_M2) < 2e-25)


class TestBiosignatureCensus(unittest.TestCase):

    def test_census_volume_scaling(self):
        """Counts scale as r^3 between hosts and planets."""
        near = BiosignatureCensusDesign.census(10.0)
        far = BiosignatureCensusDesign.census(20.0)
        self.assertAlmostEqual(far["hz_earth_analogs_fgk"] / near["hz_earth_analogs_fgk"], 8.0, places=6)

    def test_transit_route_is_starved(self):
        """Transit route yields single-digit targets within 20 pc (2.5% probability)."""
        c = BiosignatureCensusDesign.census(20.0)
        self.assertGreater(c["transiting_quiet_m_characterizable"], 1.0)
        self.assertLess(c["transiting_quiet_m_characterizable"], 10.0)

    def test_upper_bound_monotone_in_targets(self):
        prev = 1.0
        for k in (3, 5, 10, 30, 100):
            bound = BiosignatureCensusDesign.upper_bound_on_f_l(k, 0.30)
            self.assertLess(bound, prev)
            prev = bound

    def test_upper_bound_known_values(self):
        # 1 - (1 - 0.3 f)^K = 0.05  ->  f = (1 - 0.05^(1/K))/0.3
        for k in (3, 7, 20, 60):
            self.assertAlmostEqual(
                BiosignatureCensusDesign.upper_bound_on_f_l(k, 0.30),
                (1.0 - 0.05 ** (1.0 / k)) / 0.30,
                places=12)

    def test_required_targets_inverts_the_bound(self):
        k = BiosignatureCensusDesign.required_targets(0.01, 0.30)
        bound = BiosignatureCensusDesign.upper_bound_on_f_l(k, 0.30)
        self.assertAlmostEqual(bound, 0.01, places=6)
        self.assertGreater(k, 10.0)
        self.assertLess(k, 30.0)

    def test_detection_probability_limits(self):
        self.assertAlmostEqual(BiosignatureCensusDesign.detection_probability(0.0, 100, 0.3), 0.0)
        self.assertAlmostEqual(BiosignatureCensusDesign.detection_probability(1.0, 100, 1.0), 1.0)
        self.assertTrue(
            BiosignatureCensusDesign.detection_probability(0.5, 30, 0.3) > 0.99)

    def test_coadded_transits_quadratic(self):
        self.assertAlmostEqual(
            BiosignatureCensusDesign.coadded_transits_for_snr(2.0, 8.0), 16.0)
        self.assertAlmostEqual(
            BiosignatureCensusDesign.coadded_transits_for_snr(1.0, 8.0), 64.0)

    def test_transmission_depth_m_dwarf(self):
        delta = BiosignatureCensusDesign.transiting_m_dwarf_signal()
        # ~77 ppm for an Earth-like annulus around a 0.12 R_sun star
        self.assertGreater(delta, 5.0e-5)
        self.assertLess(delta, 1.0e-4)


class TestTechnosignatureDecidability(unittest.TestCase):

    def test_detection_radius_scaling(self):
        """d_max ~ sqrt(EIRP) and ~ (dv t)^(1/4)."""
        d1, _ = TechnosignatureDecidability.detection_radius_pc(1e12, 30.0)
        d2, _ = TechnosignatureDecidability.detection_radius_pc(1e14, 30.0)
        self.assertAlmostEqual(d2 / d1, 10.0, places=2)
        d3, _ = TechnosignatureDecidability.detection_radius_pc(1e12, 30.0 * 10000.0)
        self.assertAlmostEqual(d3 / d1, 10.0, places=2)

    def test_null_bound_for_bright_beacons_is_decisive(self):
        """
        KEY RESULT: an Arecibo-radar-class or brighter isotropic beacon
        (EIRP ~1e16 W) is already detectable across ~45% of the Galaxy's
        civilizations, so the null bounds such transmitters to < 7.
        """
        row = TechnosignatureDecidability.null_bound(1e16, 30.0)
        self.assertGreater(row["enclosed_disk_fraction"], 0.40)
        self.assertLess(row["n_transmitters_upper_95"], 10.0)

    def test_null_bound_weak_for_faint_transmitters(self):
        row = Technossignature_faint = TechnosignatureDecidability.null_bound(1e12, 30.0)
        self.assertLess(row["enclosed_disk_fraction"], 1e-4)
        self.assertGreater(row["n_transmitters_upper_95"], 1e5)

    def test_poisson_limit(self):
        self.assertAlmostEqual(TechnosignatureDecidability.poisson_null_upper_limit(0.95),
                               2.9957, places=3)

    def test_posterior_only_moves_for_high_completeness(self):
        prior = TechnosignatureDecidability.drake_prior_samples(n_samples=40000)
        p_alone_prior = sum(1 for x in prior if x < 1.0) / len(prior)
        faint = TechnosignatureDecidability.enclosed_disk_fraction(
            TechnosignatureDecidability.detection_radius_pc(1e12, 30.0)[0])
        bright = TechnosignatureDecidability.enclosed_disk_fraction(
            TechnosignatureDecidability.detection_radius_pc(1e18, 30.0)[0])
        post_faint = TechnosignatureDecidability.posterior_alone_given_null(prior, faint)
        post_bright = TechnosignatureDecidability.posterior_alone_given_null(prior, bright)
        self.assertAlmostEqual(post_faint, p_alone_prior, delta=0.02)
        self.assertGreater(post_bright, post_faint)

    def test_radius_for_p_det_matches_analytic_regime(self):
        r = TechnosignatureDecidability.radius_for_p_det(0.30)
        # column regime: p ~ r^2/R^2 -> r ~ sqrt(0.3) R
        self.assertAlmostEqual(r, math.sqrt(0.3) * 15000.0, delta=50.0)

    def test_area_multiplier_quadratic(self):
        r_decisive = TechnosignatureDecidability.radius_for_p_det(0.30)
        m = TechnosignatureDecidability.collecting_area_multiplier(r_decisive, 1e12, 30.0)
        d_ref, _ = TechnosignatureDecidability.detection_radius_pc(1e12, 30.0)
        self.assertAlmostEqual(m, (r_decisive / d_ref) ** 2, places=6)
        self.assertTrue(1000.0 < m < 1e6)

    def test_decidability_table_monotone_in_eirp(self):
        rows = TechnosignatureDecidability.decidability_table(
            integration_time_s=30.0,
            prior_samples=TechnosignatureDecidability.drake_prior_samples(n_samples=20000))
        bounds = [row["n_upper_95"] for row in rows]
        self.assertEqual(bounds, sorted(bounds, reverse=True))


class TestVisitationExpansionConstraint(unittest.TestCase):

    def test_filling_time_short_compared_to_galaxy_age(self):
        for speed in (0.01, 0.1, 0.3):
            t = VisitationExpansionConstraint.filling_time_years(speed)
            self.assertLess(t, 1.0e7)
        self.assertAlmostEqual(
            VisitationExpansionConstraint.filling_time_years(0.1),
            VisitationExpansionConstraint.filling_time_years(0.01) / 10.0, places=3)

    def test_probe_throughput_requires_self_replication(self):
        probes = VisitationExpansionConstraint.probes_per_decade(0.2, 1000.0)
        self.assertTrue(10.0 < probes < 30.0)
        # Blanketing 1e11 stars without self-replication is impossible
        decades_needed = 1e11 / probes
        self.assertGreater(decades_needed, 1e9)

    def test_kinetic_energy_matches_parent_engine(self):
        got = VisitationExpansionConstraint.kinetic_energy_per_kg(0.1)
        self.assertAlmostEqual(got, 4.5278e14, delta=1e12)  # 108 kT TNT/kg

    def test_expansion_constraint_forces_small_q(self):
        ec = VisitationExpansionConstraint.expansion_constraint(n_samples=40000)
        # Median prior says ~1e5 technological species ever arose
        self.assertGreater(ec.n_ever_median, 1e4)
        # ... so the null forces q <= ~1e-4
        self.assertLess(ec.q_max_median, 1e-3)
        # ... and rarity alone (N_ever <= 3) explains < 1% of the prior mass
        self.assertLess(ec.prob_rarity_suffices, 0.01)

    def test_q_max_scales_inversely_with_window(self):
        rows = VisitationExpansionConstraint.q_max_sensitivity(n_samples=20000)
        q = {row["civilisation_window_yr"]: row["q_max_median"] for row in rows}
        self.assertGreater(q[1.0e9], q[1.0e10])
        self.assertAlmostEqual(q[1.0e9] / q[1.0e10], 10.0, delta=1.0)

    def test_archaeological_windows(self):
        w = VisitationExpansionConstraint.archaeological_window_years()
        self.assertAlmostEqual(w["lunar_exposure_1m_object_yr"] / 1e9, 1.0, delta=0.1)
        self.assertAlmostEqual(w["lunar_exposure_0.1m_object_yr"] / 1e8, 1.0, delta=0.1)
        self.assertLess(w["earth_industrial_isotope_record_yr"],
                        w["earth_sedimentary_record_yr"])


class TestSynthesis(unittest.TestCase):
    """End-to-end sanity of the assembled deliverable."""

    @classmethod
    def setUpClass(cls):
        cls.report = SettlingInstrumentSynthesis.build(
            census_distance_pc=20.0, detection_efficiency=0.30, eirp_w=1e12)

    def test_all_three_questions_present(self):
        keys = set(self.report.keys())
        self.assertEqual(
            keys,
            {"question_1_biosignature_census",
             "question_2_technosignature_decidability",
             "question_3_visitation_constraint"})

    def test_q1_deliverable_numbers(self):
        q1 = self.report["question_1_biosignature_census"]
        self.assertLess(q1["upper_bound_f_l_95_zero_detections"], 0.01)
        self.assertGreater(q1["detection_probability_if_f_l_0.5"], 0.99)
        self.assertGreater(q1["required_targets_to_exclude_f_l_0.01"], 10.0)
        self.assertGreater(len(q1["distance_table"]), 3)
        self.assertGreater(len(q1["coadded_transit_table"]), 3)

    def test_q2_deliverable_numbers(self):
        q2 = self.report["question_2_technosignature_decidability"]
        self.assertAlmostEqual(q2["audited_prior_p_alone"], 0.75, delta=0.02)
        self.assertLess(q2["p_alone_given_null"], 0.80)
        self.assertGreater(q2["collecting_area_multiplier_for_decisive"], 1000.0)
        self.assertEqual(len(q2["decidability_table"]), 5)

    def test_q3_deliverable_numbers(self):
        q3 = self.report["question_3_visitation_constraint"]
        self.assertLess(q3["q_max_median"], 1e-3)
        self.assertLess(q3["prob_rarity_suffices"], 0.01)
        self.assertGreater(q3["probes_per_decade_0.2c_1tonne"], 10.0)
        self.assertLess(q3["filling_time_yr_0.1c"], 1e6)
        self.assertEqual(len(q3["q_max_sensitivity"]), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
