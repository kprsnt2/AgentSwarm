"""
test_krishna_mahabharata_taphonomic_and_consensus_compendium_engine.py

Unit test suite for krishna_mahabharata_taphonomic_and_consensus_compendium_engine.py.
Verifies marine geo-taphonomy, textual accretion, logistics, cross-tradition stemmatics,
and 8-dimensional Bayesian adjudication.
"""

import unittest
from krishna_mahabharata_taphonomic_and_consensus_compendium_engine import (
    MarineGeoTaphonomyEngine,
    TextualStratigraphyAndApotheosisEngine,
    ArchaeoDemographicAndLogisticsEngine,
    CrossTraditionStemmaticsEngine,
    BayesianHistoricityAdjudicationCompendium,
    run_full_epistemic_compendium,
    EpistemicCategory
)


class TestMarineGeoTaphonomyEngine(unittest.TestCase):
    def test_excavation_data_structure(self):
        data = MarineGeoTaphonomyEngine.EXCAVATION_DATA
        self.assertIn("bet_dwarka_pottery", data)
        self.assertIn("stone_anchors", data)
        self.assertIn("submerged_structures", data)

    def test_dwaraka_evaluation(self):
        res = MarineGeoTaphonomyEngine.evaluate_dwaraka_claims()
        self.assertEqual(res["total_anchors_recovered"], 142)
        self.assertGreater(res["triangular_anchor_fraction"], 0.6)
        self.assertTrue(res["mediterranean_comparanda_present"])
        self.assertGreater(res["spatial_inflation_factor"], 1e6)
        self.assertIn("historical_core", res["verdict"])
        self.assertIn("mythological_layer", res["verdict"])


class TestTextualStratigraphyAndApotheosisEngine(unittest.TestCase):
    def test_epic_strata_progression(self):
        strata = TextualStratigraphyAndApotheosisEngine.EPIC_STRATA
        self.assertEqual(len(strata), 3)
        self.assertEqual(strata[0]["verse_count"], 8800)
        self.assertEqual(strata[1]["verse_count"], 24000)
        self.assertEqual(strata[2]["verse_count"], 100000)

    def test_epigraphic_chronology_order(self):
        chrono = TextualStratigraphyAndApotheosisEngine.EPIGRAPHIC_CHRONOLOGY
        self.assertEqual(len(chrono), 7)
        # Check all are categorized as PRIMARY_TEXT
        for item in chrono:
            self.assertEqual(item["category"], EpistemicCategory.PRIMARY_TEXT)

    def test_textual_accretion_rate(self):
        rate = TextualStratigraphyAndApotheosisEngine.calculate_textual_accretion_rate()
        self.assertGreater(rate["overall_expansion_multiplier"], 10.0)
        self.assertGreater(rate["verse_doubling_time_years"], 300.0)
        self.assertLess(rate["verse_doubling_time_years"], 500.0)


class TestArchaeoDemographicAndLogisticsEngine(unittest.TestCase):
    def test_akshauhini_logistics_calculation(self):
        logistics = ArchaeoDemographicAndLogisticsEngine.compute_epic_scale_logistics(18)
        self.assertGreater(logistics["total_combatants_epic"], 3.5e6)
        self.assertGreater(logistics["daily_human_grain_metric_tons"], 2000.0)
        self.assertGreater(logistics["daily_water_megaliters"], 50.0)
        self.assertGreater(logistics["demographic_hyperbolic_factor"], 100.0)


class TestCrossTraditionStemmaticsEngine(unittest.TestCase):
    def test_traditions_motifs_present(self):
        traditions = CrossTraditionStemmaticsEngine.TRADITIONS_EVIDENCE
        self.assertEqual(len(traditions), 4)
        names = [t["tradition"] for t in traditions]
        self.assertIn("Brahmanical", names)
        self.assertIn("Buddhist", names)
        self.assertIn("Jaina", names)
        self.assertIn("Greco-Roman", names)

    def test_joint_fabrication_probability(self):
        res = CrossTraditionStemmaticsEngine.compute_cross_stemmatic_independence()
        self.assertEqual(res["traditions_evaluated"], 4)
        self.assertEqual(res["shared_core_biographical_nodes"], 6)
        self.assertLess(res["joint_fabrication_probability"], 1e-12)


class TestBayesianHistoricityAdjudicationCompendium(unittest.TestCase):
    def test_hypotheses_and_posteriors(self):
        post = BayesianHistoricityAdjudicationCompendium.compute_bayesian_posteriors()
        norm_post = post["normalized_posteriors"]
        self.assertAlmostEqual(sum(norm_post.values()), 1.0, places=5)
        self.assertEqual(post["best_hypothesis"], "H4_IRON_AGE_HISTORICAL_NUCLEUS")
        self.assertGreater(norm_post["H4_IRON_AGE_HISTORICAL_NUCLEUS"], 0.999)

    def test_bayes_factors_magnitude(self):
        post = BayesianHistoricityAdjudicationCompendium.compute_bayesian_posteriors()
        bfs = post["bayes_factors"]
        self.assertGreater(bfs["H4_IRON_AGE_HISTORICAL_NUCLEUS_vs_H1_SOLAR_MYTH"], 1e8)
        self.assertGreater(bfs["H4_IRON_AGE_HISTORICAL_NUCLEUS_vs_H2_LITERAL_CANON"], 1e12)
        self.assertGreater(bfs["H4_IRON_AGE_HISTORICAL_NUCLEUS_vs_H3_BRONZE_AGE_SANAULI"], 1e6)


class TestFullCompendiumExecution(unittest.TestCase):
    def test_full_pipeline_run(self):
        res = run_full_epistemic_compendium()
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("dwaraka_evaluation", res)
        self.assertIn("textual_stratigraphy", res)
        self.assertIn("logistics_and_demographics", res)
        self.assertIn("cross_tradition_concordance", res)
        self.assertIn("bayesian_posteriors", res)


if __name__ == "__main__":
    unittest.main()
