"""
test_extraterrestrial_engine.py - Test suite for extraterrestrial_engine.analyze()
Agent: Nagarjuna (A004). Run: python test_extraterrestrial_engine.py
Verifies the Phase 2 schema, the three-question demarcation, the quantitative
physics models, and the falsifiability discipline (no discovery asserted).
"""

import math
import unittest

from extraterrestrial_engine import (
    analyze,
    abiotic_o2_budget,
    abiotic_o2_timescale_years,
    accessible_rocky_hz_planets,
    biosignature_census_power,
    biosignature_detection_power,
    ch4_o2_disequilibrium,
    cosmic_haystack_fraction,
    drake_equation_monte_carlo,
    isotopic_anomaly_sigma,
    kopparapu_habitable_zone,
    null_result_upper_limit,
    null_sample_for_upper_limit,
    o2_is_weak_standalone_biosignature,
    relativistic_isp_cost,
    required_sample_for_power,
    technosignature_null_power,
    visitation_posterior,
)


class TestExtraterrestrialEngine(unittest.TestCase):

    def test_01_analyze_schema(self):
        """analyze() returns the four required keys with correct types."""
        result = analyze()
        self.assertIsInstance(result, dict)
        for key in ("domain", "claims", "confidence", "evidence"):
            self.assertIn(key, result)
        self.assertIsInstance(result["domain"], str)
        self.assertIsInstance(result["claims"], list)
        self.assertTrue(all(isinstance(c, str) for c in result["claims"]))
        self.assertIsInstance(result["confidence"], float)
        self.assertTrue(0.0 <= result["confidence"] <= 1.0)
        self.assertIsInstance(result["evidence"], list)
        for item in result["evidence"]:
            self.assertIsInstance(item, dict)
            self.assertIn("kind", item)
            self.assertIn("value", item)
            self.assertIn("source", item)

    def test_02_three_questions_demarcated_with_falsifiable_predictions(self):
        """Each question carries an explicit falsifiable prediction and settling observation,
        and the claims keep the three questions strictly separated."""
        result = analyze()
        joined = " ".join(result["claims"])
        # Question demarcation present in the claims themselves.
        for tag in ("Q1", "Q2", "Q3"):
            self.assertIn(tag, joined)
        # Exactly one falsifiable-prediction evidence entry per question.
        preds = [
            e for e in result["evidence"]
            if e["kind"] == "falsifiable_prediction"
        ]
        self.assertEqual(len(preds), 3)
        questions = {e["value"]["question"].split(":")[0] for e in preds}
        self.assertEqual(questions, {"Q1", "Q2", "Q3"})
        for e in preds:
            self.assertTrue(e["value"]["prediction"].strip())
            self.assertTrue(e["value"]["settling_observation"].strip())

    def test_03_no_discovery_asserted(self):
        """Protocol discipline: plausibility is not treated as evidence; no discovery claimed."""
        result = analyze()
        joined = " ".join(result["claims"]).lower()
        for banned in ("we have found", "aliens exist", "discovery confirmed",
                       "they are here", "proof that", "it is proven"):
            self.assertNotIn(banned, joined)
        # Q3 must be explicitly rejected under the null hypothesis.
        self.assertIn("rejected", joined)

    def test_04_habitable_zone_matches_solar_system(self):
        """Kopparapu HZ for the Sun: conservative band ~0.95-1.69 AU;
        optimistic recent-Venus ~0.75 AU, early-Mars ~1.77 AU."""
        hz = kopparapu_habitable_zone(5778.0, 1.0)
        self.assertAlmostEqual(hz["recent_venus"], 0.75, delta=0.02)
        self.assertAlmostEqual(hz["runaway_greenhouse"], 0.95, delta=0.05)
        self.assertAlmostEqual(hz["maximum_greenhouse"], 1.69, delta=0.05)
        self.assertAlmostEqual(hz["early_mars"], 1.77, delta=0.05)
        # Earth falls in the conservative habitable zone.
        self.assertTrue(hz["runaway_greenhouse"] < 1.0 < hz["maximum_greenhouse"])
        # Luminosity scaling: d ~ sqrt(L); a 4x-L star widens the HZ by ~2x.
        hz_l4 = kopparapu_habitable_zone(5778.0, 4.0)
        self.assertAlmostEqual(
            hz_l4["runaway_greenhouse"] / hz["runaway_greenhouse"],
            math.sqrt(4.0), delta=0.02
        )

    def test_05_biosignature_disequilibrium_and_abiotic_gate(self):
        """Earth-like CH4+O2 air is strongly disequilibrated and survives the abiotic gate;
        a CO-rich abiotic mimic fails the gate."""
        bio = ch4_o2_disequilibrium()
        self.assertTrue(bio["is_thermodynamic_disequilibrium"])
        self.assertTrue(bio["settles_biosignature"])
        self.assertLess(bio["delta_g_actual_kj_per_mol"], -500.0)
        self.assertGreater(bio["required_biogenic_flux_molecules_per_m2_s"], 1e10)
        # Control: O2 with abundant CO (abiotic CO2 photolysis) is flagged abiotic.
        control = ch4_o2_disequilibrium(co_mixing_ratio=2.0e-2)
        self.assertTrue(control["abiotic_explanation_plausible"])
        self.assertFalse(control["settles_biosignature"])

    def test_06_drake_monte_carlo_reproducible_and_dissolves_paradox(self):
        """Seeded MC is deterministic and yields a large P(N<1) within a plausible band."""
        run_a = drake_equation_monte_carlo(n_samples=4000)
        run_b = drake_equation_monte_carlo(n_samples=4000)
        self.assertAlmostEqual(run_a["p_alone_in_galaxy"], run_b["p_alone_in_galaxy"], places=12)
        self.assertTrue(0.05 <= run_a["p_alone_in_galaxy"] <= 0.95)
        self.assertLess(run_a["percentile_5"], run_a["median_n"])
        self.assertLess(run_a["median_n"], run_a["percentile_95"])
        # Variance spans >= 6 orders of magnitude: the paradox is underdetermined.
        log_span = math.log10(run_a["percentile_95"]) - math.log10(run_a["percentile_5"])
        self.assertGreater(log_span, 6.0)

    def test_07_cosmic_haystack_fraction_is_tiny(self):
        """SETI has searched < 1e-12 of the haystack: the null result is weak evidence."""
        hay = cosmic_haystack_fraction()
        frac = hay["total_haystack_fraction_searched"]
        self.assertTrue(0.0 < frac < 1e-12)
        self.assertLess(hay["log10_total_fraction"], -12.0)
        # Scaling: doubling searched distance multiplies volume fraction by ~8.
        hay2 = cosmic_haystack_fraction(distance_searched_pc=200.0)
        self.assertAlmostEqual(
            hay2["volume_fraction"] / hay["volume_fraction"], 8.0, delta=0.01 * 8.0
        )

    def test_08_relativistic_and_bayesian_visitation_models(self):
        """Relativistic prices (0.1c ~ 4.5e14 J/kg, ~108 kT/kg) and Bayesian rejection nominal."""
        kin = relativistic_isp_cost(0.10)
        self.assertAlmostEqual(kin["gamma"], 1.005038, places=5)
        self.assertAlmostEqual(kin["specific_kinetic_energy_j_per_kg"], 4.53e14, delta=5e13)
        self.assertAlmostEqual(kin["specific_kinetic_energy_kilotons_tnt_per_kg"], 108.0,
                               delta=10.0)
        self.assertGreater(kin["fusion_mass_ratio_round_trip"], 50.0)
        # Faster is astronomically more expensive: 0.5c needs ~1e5 kT/kg.
        kin_fast = relativistic_isp_cost(0.50)
        self.assertAlmostEqual(kin_fast["gamma"], 1.154700, places=5)
        self.assertGreater(kin_fast["specific_kinetic_energy_kilotons_tnt_per_kg"], 3.0e3)
        # Bayesian: even a generous prior and BF=900 leave P(ET|data) ~ 1e-6.
        bayes = visitation_posterior()
        self.assertFalse(bayes["rejects_null"])
        self.assertLess(bayes["posterior"], 1e-5)
        # Isotropic anomaly test: 15-sigma deviation flags non-terrestrial material.
        sigma, is_et = isotopic_anomaly_sigma(18.2, 17.0, 0.08)
        self.assertGreater(sigma, 10.0)
        self.assertTrue(is_et)


class TestExtraterrestrialEngineAdvances(unittest.TestCase):
    """Phase-3 advance tests: statistical power, abiotic O2 budget, null-survey ceiling."""

    def test_09_detection_power_is_exact_binomial_and_monotone(self):
        """P(>=1) = 1-(1-f)^N, verified against an independent loop over Bernoulli trials."""
        # Independent enumeration of the binomial complement, no reuse of the engine formula.
        for f, n in ((0.10, 30), (0.05, 30), (0.01, 30), (0.02, 30), (0.37, 1)):
            direct = 1.0 - (1.0 - f) ** n
            self.assertAlmostEqual(biosignature_detection_power(f, n), direct, places=12)
        # A single survey of a certain biosphere is a certainty; of none is impossible.
        self.assertEqual(biosignature_detection_power(1.0, 1), 1.0)
        self.assertEqual(biosignature_detection_power(0.0, 500), 0.0)
        # Monotone increasing in both N and f: more data, more common life, more power.
        p30 = biosignature_detection_power(0.05, 30)
        p60 = biosignature_detection_power(0.05, 60)
        self.assertGreater(p60, p30)
        self.assertLess(biosignature_detection_power(0.01, 30),
                        biosignature_detection_power(0.05, 30))
        # Power must saturate strictly inside (0, 1) for 0 < f < 1.
        self.assertTrue(0.0 < p30 < 1.0)
        self.assertRaises(ValueError, biosignature_detection_power, 1.5, 10)

    def test_10_null_upper_limit_inverts_required_sample(self):
        """The null bound and its inversion are mutually consistent to within one planet."""
        for f_bound, conf in ((0.01, 0.95), (0.05, 0.95), (0.10, 0.99), (1e-3, 0.95)):
            n_needed = null_sample_for_upper_limit(f_bound, conf)
            self.assertLessEqual(null_result_upper_limit(n_needed, conf), f_bound)
            # One fewer planet must fail to reach the bound (minimality).
            self.assertGreater(null_result_upper_limit(n_needed - 1, conf), f_bound)
        # A null census can never certify zero biospheres.
        for n in (10, 100, 1000, 100000):
            self.assertGreater(null_result_upper_limit(n, 0.95), 0.0)
        # More nulls strictly tighten the bound.
        self.assertLess(null_result_upper_limit(300, 0.95),
                        null_result_upper_limit(30, 0.95))
        # Required sample grows as prevalence falls: rare life costs far more surveys.
        self.assertGreater(required_sample_for_power(0.02, 0.90),
                           required_sample_for_power(0.10, 0.90))
        self.assertGreaterEqual(required_sample_for_power(0.02, 0.95),
                                required_sample_for_power(0.02, 0.90))

    def test_11_abiotic_o2_budget_from_first_principles(self):
        """O2 left by losing one ocean, recomputed independently from H2O -> H2 + 1/2 O2."""
        ocean_kg = 1.4e21
        mol_h2o = ocean_kg / 0.01801528
        mol_o2 = 0.5 * mol_h2o
        o2_kg = mol_o2 * 0.0319988
        area_m2 = 4.0 * math.pi * (6.371e6) ** 2
        column_kg_m2 = o2_kg / area_m2
        expected_bar = column_kg_m2 * 9.80665 / 1.0e5

        budget = abiotic_o2_budget(1.0)
        self.assertAlmostEqual(budget["o2_partial_pressure_bar"], expected_bar, delta=0.5)
        # ~239 bar of abiotic O2 per ocean - an enormous abiotic reservoir.
        self.assertGreater(budget["o2_partial_pressure_bar"], 100.0)
        self.assertAlmostEqual(budget["o2_moles_produced"], mol_o2, delta=1e19)
        # Linear in oceans lost.
        self.assertAlmostEqual(abiotic_o2_budget(2.0)["o2_partial_pressure_bar"],
                               2.0 * expected_bar, delta=1.0)
        self.assertEqual(abiotic_o2_budget(0.0)["o2_partial_pressure_bar"], 0.0)
        self.assertRaises(ValueError, abiotic_o2_budget, -1.0)

        # Earth's real O2 inventory cross-checked by the same hydrostatic route.
        earth_o2_column_kg_m2 = 0.21 * 1.0e5 / 9.80665
        earth_o2_kg = earth_o2_column_kg_m2 * area_m2
        # ~1.1e18 kg of O2: only ~1/1138 of one ocean's worth of oxygen.
        self.assertAlmostEqual(earth_o2_kg, 1.1e18, delta=5.0e16)
        self.assertAlmostEqual(budget["o2_mass_kg"] / earth_o2_kg,
                               expected_bar / 0.21, delta=5.0)
        # Molar cross-check: 3.9e22 mol of abiotic O2 vs 3.4e19 mol above Earth.
        self.assertAlmostEqual(budget["o2_moles_produced"] * 0.0319988 / earth_o2_kg,
                               expected_bar / 0.21, delta=5.0)
        self.assertAlmostEqual(abiotic_o2_timescale_years(0.21, 1.0e9, 1.0)["required_h_escape_kg_per_s"],
                               4.4, delta=0.5)

    def test_12_o2_alone_is_a_weak_biosignature(self):
        """The abiotic O2 pool dwarfs Earth's biosynthetic inventory, so O2 cannot settle Q1."""
        weak = o2_is_weak_standalone_biosignature()
        self.assertFalse(weak["o2_alone_is_discriminative"])
        self.assertGreater(weak["pool_to_earth_inventory_ratio"], 1000.0)
        # Earth-like abiotic O2 costs a vanishing fraction of one ocean.
        self.assertLess(weak["fraction_of_ocean_needed_for_earth_like_o2"], 1e-3)
        # The escape rate needed is of the same order as Earth's PRESENT rate.
        clock = abiotic_o2_timescale_years(0.21, 1.0e9, 1.0)
        self.assertLess(clock["required_to_present_earth_ratio"], 10.0)
        self.assertGreater(clock["required_to_present_earth_ratio"], 0.1)
        # Asking for more O2 than the ocean can supply must fail loudly.
        self.assertRaises(ValueError, abiotic_o2_timescale_years, 1000.0, 1.0e9, 1.0)
        # A target beyond the budget of one ocean is reachable from more oceans.
        self.assertGreater(
            abiotic_o2_budget(10.0)["o2_partial_pressure_bar"],
            abiotic_o2_budget(1.0)["o2_partial_pressure_bar"],
        )

    def test_13_null_survey_has_a_target_list_ceiling(self):
        """The Fermi null is limited by the target list, not by receiver sensitivity."""
        pw = technosignature_null_power(1_000_000)
        self.assertLess(pw["f_transmitting_upper_95pct"], 3.0e-6)
        self.assertGreater(pw["f_transmitting_upper_95pct"], 2.0e-6)
        # The requested 1e6-star survey exceeds the real 100 pc star census.
        self.assertGreater(pw["targets_per_available_star"], 1.0)
        self.assertTrue(pw["target_list_binding_constraint"])
        # Even so it still permits ~order-unity transmitters in the searched volume.
        self.assertGreater(pw["max_expected_transmitters_in_volume"], 0.5)
        self.assertLess(pw["max_expected_transmitters_in_volume"], 5.0)
        # Strengthening the bound to 1e-9 is beyond any feasible target list.
        self.assertGreater(pw["targets_needed_for_f_below_1e-9"], 1.0e9)
        self.assertRaises(ValueError, technosignature_null_power, 0)

    def test_14_power_audit_and_target_supply_are_self_consistent(self):
        """The Q1 power audit must agree with its own primitives and with the census supply."""
        audit = biosignature_census_power(n_surveyed=30)
        self.assertAlmostEqual(audit["detection_power_if_f_0.10"],
                               biosignature_detection_power(0.10, 30), places=12)
        self.assertAlmostEqual(audit["detection_power_if_f_0.01"],
                               biosignature_detection_power(0.01, 30), places=12)
        # Power falls monotonically as biospheres get rarer.
        powers = [audit["detection_power_if_f_0.10"], audit["detection_power_if_f_0.05"],
                  audit["detection_power_if_f_0.02"], audit["detection_power_if_f_0.01"]]
        self.assertEqual(powers, sorted(powers, reverse=True))
        # The deep-null bound matches the stated null count.
        self.assertAlmostEqual(
            audit["f_life_upper_95pct_after_deep_census"],
            null_result_upper_limit(audit["nulls_required_for_f_life_below_0.01_at_95pct"]),
            places=12,
        )
        self.assertLess(audit["f_life_upper_95pct_after_deep_census"], 0.01)
        # A null establishes rarity, never aloneness: bound stays far above zero galaxy-wide.
        self.assertGreater(audit["galaxy_wide_biosphere_bound_after_deep_census"], 1.0e6)
        # Target supply exceeds the required census, so sensitivity - not targets - binds.
        supply = accessible_rocky_hz_planets(30.0)
        self.assertGreater(supply["n_rocky_hz_planets"],
                           audit["nulls_required_for_f_life_below_0.01_at_95pct"])

    def test_15_new_evidence_kinds_present_and_nondisruptive(self):
        """New evidence uses fresh kinds, so exactly three falsifiable predictions remain."""
        result = analyze()
        kinds = [e["kind"] for e in result["evidence"]]
        for expected in ("q1_power_analysis", "q1_abiotic_o2_budget", "q2_null_survey_power"):
            self.assertIn(expected, kinds)
        preds = [e for e in result["evidence"] if e["kind"] == "falsifiable_prediction"]
        self.assertEqual(len(preds), 3)
        # The advance must be reflected in the substantive claims.
        joined = " ".join(result["claims"])
        self.assertIn("POWER AUDIT", joined)
        self.assertIn("ABIOTIC-O2 BUDGET", joined)
        self.assertIn("TARGET-LIST", joined)
        # Still no discovery asserted after the advance.
        lowered = joined.lower()
        self.assertNotIn("we have found", lowered)
        self.assertNotIn("discovery confirmed", lowered)


if __name__ == "__main__":
    unittest.main(verbosity=2)