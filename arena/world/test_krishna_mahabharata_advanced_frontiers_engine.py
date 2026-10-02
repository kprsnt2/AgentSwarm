"""
test_krishna_mahabharata_advanced_frontiers_engine.py

Unit test suite for the Advanced Epistemic Frontiers & Computational Engine
(krishna_mahabharata_advanced_frontiers_engine.py).
"""

import unittest
import math
from krishna_mahabharata_advanced_frontiers_engine import (
    EpistemicCategory,
    ProtocolViolation,
    ProtocolViolationError,
    ArchaeoastronomyMechanicsModel,
    BayesianDynasticActuarialModel,
    DemographicCarryingCapacityModel,
    CeramicAndMetallurgicalStratigraphyRegistry,
    KrishnaSyncreticTrajectoryRegistry,
    LateVedicEpistemicCorpusRegistry,
    AdvancedHistoricitySynthesisEngine
)


class TestArchaeoastronomyMechanicsModel(unittest.TestCase):
    def setUp(self):
        self.model = ArchaeoastronomyMechanicsModel()

    def test_precession_solstice_950_bce(self):
        res = self.model.calculate_winter_solstice_precession(950)
        self.assertEqual(res.target_year_bce, 950)
        self.assertTrue(res.matches_bhishma_textual_description)
        self.assertIn(res.associated_nakshatra, ["Shravana", "Dhanishtha"])
        self.assertEqual(res.epistemic_verdict, "ASTRONOMICALLY_CONGRUENT_WITH_LATE_VEDIC_EPIC_CORPUS")

    def test_precession_solstice_3102_bce(self):
        res = self.model.calculate_winter_solstice_precession(3102)
        self.assertEqual(res.target_year_bce, 3102)
        # At 3102 BCE, precession angle is (3102 + 285) * 50.29 / 3600 ~ 47.3 degrees
        # (270 + 47.3) % 360 = 317.3 degrees, which lands in Purva Bhadrapada or Shatabhisha
        self.assertFalse(res.matches_bhishma_textual_description)
        self.assertIn(res.associated_nakshatra, ["Shatabhisha", "Purva Bhadrapada"])
        self.assertIn(res.epistemic_verdict, ["DISCORDANT_EARLY_BRONZE_AGE_MISMATCH", "DIVERGENT_STELLAR_EPOCH"])

    def test_13_day_eclipse_degeneracy(self):
        analysis = self.model.calculate_13_day_eclipse_recurrence()
        self.assertEqual(analysis["mean_synodic_half_month_days"], 14.765)
        self.assertEqual(analysis["empirical_recurrence_interval_years"], 250)
        self.assertGreater(analysis["estimated_occurrences_in_5000_years"], 15)
        self.assertEqual(analysis["inverse_problem_status"], "HIGHLY_DEGENERATE_MULTIPLE_SOLUTIONS")


class TestBayesianDynasticActuarialModel(unittest.TestCase):
    def setUp(self):
        self.model = BayesianDynasticActuarialModel()

    def test_actuarial_evaluation_950_bce(self):
        res = self.model.evaluate_war_date(950)
        self.assertEqual(res.elapsed_years, 950 - 362)  # 588 years
        self.assertAlmostEqual(res.mean_reign_years, 19.6, places=1)
        self.assertLess(abs(res.z_score_vs_empirical_norm), 1.0)
        self.assertAlmostEqual(res.bayes_factor_vs_950bce, 1.0, places=3)
        self.assertGreater(res.tail_probability_p_value, 0.05)
        self.assertEqual(res.missing_kings_required_for_plausibility, 2)  # 588 / 18.5 ~ 31.78 -> 32 - 30 = 2
        self.assertEqual(res.actuarial_verdict, "HIGHLY_PLAUSIBLE_EMPIRICAL_CONCORDANCE")

    def test_actuarial_evaluation_3102_bce(self):
        res = self.model.evaluate_war_date(3102)
        self.assertEqual(res.elapsed_years, 3102 - 362)  # 2740 years
        self.assertAlmostEqual(res.mean_reign_years, 91.33, places=1)
        self.assertGreater(res.z_score_vs_empirical_norm, 30.0)
        self.assertLess(res.bayes_factor_vs_950bce, 1e-100)
        self.assertEqual(res.tail_probability_p_value, 0.0)
        # Missing kings: 2740 / 18.5 ~ 148 -> 148 - 30 = 118 kings missing!
        self.assertGreater(res.missing_kings_required_for_plausibility, 110)
        self.assertEqual(res.actuarial_verdict, "ACTUARIALLY_IMPOSSIBLE_REIGN_INFLATION")


class TestDemographicCarryingCapacityModel(unittest.TestCase):
    def setUp(self):
        self.model = DemographicCarryingCapacityModel()

    def test_logistics_and_headcount(self):
        metrics = self.model.calculate_logistical_footprint()
        # 18 Akshauhinis
        self.assertEqual(metrics.infantry_count, 18 * 109350)  # 1,968,300
        self.assertEqual(metrics.cavalry_count, 18 * 65610)   # 1,180,980
        self.assertEqual(metrics.chariot_count, 18 * 21870)   # 393,660
        self.assertEqual(metrics.war_elephant_count, 18 * 21870) # 393,660
        # Total humans: 1968300 + 1180980 + 393660*2 + 393660*3 = 5,117,580
        self.assertEqual(metrics.total_combatants, 5117580)
        # Daily biomass is enormous (> 70,000 metric tons/day)
        self.assertGreater(metrics.total_daily_biomass_metric_tons, 60000.0)
        # Ratio of combatants to total regional population (1.5M) is > 3.0
        self.assertGreater(metrics.combatant_to_regional_population_ratio, 3.0)
        self.assertEqual(metrics.epistemic_logistical_status, "SYMBOLIC_POETIC_MAGNIFICATION_NON_LITERAL")


class TestCeramicAndMetallurgicalStratigraphyRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = CeramicAndMetallurgicalStratigraphyRegistry()

    def test_stratigraphic_sites_presence(self):
        self.assertIn("Hastinapura", self.registry.sites)
        self.assertIn("Bhagwanpura", self.registry.sites)
        self.assertIn("Atranjikhera", self.registry.sites)
        self.assertIn("Sinauli", self.registry.sites)
        self.assertIn("Kaushambi", self.registry.sites)

    def test_bhagwanpura_overlap(self):
        bhag = self.registry.sites["Bhagwanpura"]
        self.assertEqual(bhag.stratigraphic_levels[1][1], "Late Harappan & PGW Overlap (No Hiatus)")
        self.assertFalse(bhag.iron_metallurgy_presence)

    def test_metallurgical_chronology(self):
        res = self.registry.verify_metallurgical_chronology("Iron-tipped arrows and steel swords")
        self.assertFalse(res["bronze_age_3102bce_has_iron"])
        self.assertTrue(res["1000bce_pgw_has_iron"])


class TestKrishnaSyncreticTrajectoryRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = KrishnaSyncreticTrajectoryRegistry()

    def test_four_streams_presence(self):
        summary = self.registry.get_trajectory_summary()
        self.assertEqual(len(summary), 4)
        stream_names = [s["stream"] for s in summary]
        self.assertTrue(any("Krishna Devakiputra" in name for name in stream_names))
        self.assertTrue(any("Vasudeva of the Vrishnis" in name for name in stream_names))
        self.assertTrue(any("Gopala Krishna" in name for name in stream_names))
        self.assertTrue(any("Vedic Narayana" in name for name in stream_names))


class TestLateVedicEpistemicCorpusRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = LateVedicEpistemicCorpusRegistry()

    def test_primary_vedic_records(self):
        texts = [r.text_name for r in self.registry.records]
        self.assertIn("Atharvaveda Samhita", texts)
        self.assertIn("Shatapatha Brahmana", texts)
        self.assertIn("Aitareya Brahmana", texts)
        self.assertIn("Brihadaranyaka Upanishad", texts)
        self.assertIn("Rigveda Samhita", texts)


class TestAdvancedHistoricitySynthesisEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AdvancedHistoricitySynthesisEngine()

    def test_protocol_firewall_violations(self):
        with self.assertRaises(ProtocolViolationError):
            self.engine.audit_protocol("The Brahmashira was a 50-megaton nuclear blast", is_laboratory_assertion=True, is_absence_proof_assertion=False)

        with self.assertRaises(ProtocolViolationError):
            self.engine.audit_protocol("No 3000 BCE stone tablet proves Krishna never existed", is_laboratory_assertion=False, is_absence_proof_assertion=True)

    def test_execute_advanced_analysis(self):
        result = self.engine.execute_advanced_analysis()
        self.assertIn("precession_results", result)
        self.assertIn("eclipse_13_day_analysis", result)
        self.assertIn("actuarial_results", result)
        self.assertIn("logistics_18_akshauhinis", result)
        self.assertIn("overall_scholarly_verdict", result)
        self.assertTrue(result["overall_scholarly_verdict"]["historical_core_confirmed"])
        self.assertEqual(result["overall_scholarly_verdict"]["optimal_chronological_window_bce"], (1000, 850))


if __name__ == "__main__":
    unittest.main()
