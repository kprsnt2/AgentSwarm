"""
test_krishna_mahabharata_cross_tradition_engine.py

Unit test suite for krishna_mahabharata_cross_tradition_engine.py.
Tests deification trajectory, cross-tradition concordance, Gita stratigraphy,
Iron Age ballistics, and 6D Bayesian historicity posteriors.
"""

import unittest
from krishna_mahabharata_cross_tradition_engine import (
    DeificationTrajectoryModel,
    CrossTraditionConcordanceEngine,
    BhagavadGitaStratigraphyModel,
    IronAgeBallisticsAndLogisticsEngine,
    ComprehensiveBayesianHistoricityEngine
)


class TestDeificationTrajectoryModel(unittest.TestCase):
    def test_stages_exist_and_complete(self):
        self.assertEqual(len(DeificationTrajectoryModel.STAGES), 4)
        stage_ids = [s["stage_id"] for s in DeificationTrajectoryModel.STAGES]
        self.assertIn("VIRA_VADA", stage_ids)
        self.assertIn("DVI_VYUHA", stage_ids)
        self.assertIn("CHATUR_VYUHA", stage_ids)
        self.assertIn("AVATARA_VADA", stage_ids)

    def test_stage_lookup(self):
        stage = DeificationTrajectoryModel.get_stage_by_id("DVI_VYUHA")
        self.assertIn("Ai-Khanoum Coins", stage["primary_evidence"][0])
        self.assertEqual(stage["deification_index"], 0.55)

    def test_prominence_sums_to_one(self):
        for yr in [1000, 600, 400, 200, 100, 0, -200, -500, -800]:
            prom = DeificationTrajectoryModel.compute_trajectory_prominence(yr)
            total = sum(prom.values())
            self.assertAlmostEqual(total, 1.0, places=3)

    def test_historical_evolution_direction(self):
        # In 600 BCE, Vira-vada should dominate
        early = DeificationTrajectoryModel.compute_trajectory_prominence(600)
        self.assertGreater(early["VIRA_VADA"], early["AVATARA_VADA"])
        self.assertEqual(early["AVATARA_VADA"], 0.0)

        # In 500 CE (-500), Avatara-vada should dominate
        late = DeificationTrajectoryModel.compute_trajectory_prominence(-500)
        self.assertGreater(late["AVATARA_VADA"], late["VIRA_VADA"])


class TestCrossTraditionConcordanceEngine(unittest.TestCase):
    def test_traditions_data_present(self):
        data = CrossTraditionConcordanceEngine.TRADITIONS_DATA
        self.assertIn("Brahmanical", data)
        self.assertIn("Buddhist", data)
        self.assertIn("Jaina", data)
        self.assertIn("Greco_Roman", data)

    def test_concordance_statistics(self):
        stats = CrossTraditionConcordanceEngine.compute_concordance_statistics()
        self.assertTrue(stats["core_unanimous"])
        self.assertIn("name_and_clan", stats["core_motifs"])
        self.assertIn("brother_baladeva", stats["core_motifs"])
        self.assertIn("mathura_to_dvaraka", stats["core_motifs"])
        self.assertIn("internal_clan_strife", stats["core_motifs"])
        self.assertIn("death_by_hunter_arrow", stats["core_motifs"])

    def test_joint_fabrication_probability_infinitesimal(self):
        stats = CrossTraditionConcordanceEngine.compute_concordance_statistics()
        p_fab = stats["composite_fabrication_probability"]
        self.assertLess(p_fab, 1e-10)


class TestBhagavadGitaStratigraphyModel(unittest.TestCase):
    def test_metrical_distribution_sum(self):
        dist = BhagavadGitaStratigraphyModel.get_metrical_distribution()
        self.assertEqual(dist["total_verses"], 700)
        self.assertEqual(dist["anustubh_verses"] + dist["tristubh_verses"], 700)
        self.assertEqual(dist["tristubh_verses"], 56)
        self.assertAlmostEqual(dist["anustubh_percentage"] + dist["tristubh_percentage"], 100.0, places=1)

    def test_chapter_11_has_highest_tristubh_concentration(self):
        dist = BhagavadGitaStratigraphyModel.get_metrical_distribution()
        tristubh_by_ch = dist["tristubh_distribution"]
        self.assertEqual(tristubh_by_ch[11], 41)
        self.assertGreater(tristubh_by_ch[11], max(v for k, v in tristubh_by_ch.items() if k != 11))

    def test_recitation_kinetics(self):
        kinetics = BhagavadGitaStratigraphyModel.calculate_recitation_kinetics(16.0)
        self.assertAlmostEqual(kinetics["duration_minutes"], 43.75, places=1)
        self.assertAlmostEqual(kinetics["duration_hours"], 0.73, places=2)


class TestIronAgeBallisticsAndLogisticsEngine(unittest.TestCase):
    def test_arrow_ballistics(self):
        ballistics = IronAgeBallisticsAndLogisticsEngine.compute_arrow_ballistics()
        self.assertGreater(ballistics["kinetic_energy_joules"], 50.0)
        self.assertGreater(ballistics["launch_velocity_ms"], 40.0)
        self.assertTrue(ballistics["lethal_to_unarmored"])
        self.assertTrue(ballistics["pierces_leather_cuirass"])
        self.assertTrue(ballistics["pierces_iron_plate"])

    def test_demographics_and_logistics_inflation(self):
        logistics = IronAgeBallisticsAndLogisticsEngine.evaluate_battlefield_demographics_and_logistics()
        self.assertGreater(logistics["epic_inflation_factor"], 100.0)
        self.assertGreater(logistics["daily_grain_requirement_epic_tonnes"], 1000.0)
        self.assertLess(logistics["max_feasible_mobilized_army"], 50000)


class TestComprehensiveBayesianHistoricityEngine(unittest.TestCase):
    def test_hypotheses_integrity(self):
        hypotheses = ComprehensiveBayesianHistoricityEngine.HYPOTHESES
        self.assertEqual(len(hypotheses), 4)
        for h_id, data in hypotheses.items():
            self.assertEqual(len(data["likelihoods"]), 6)
            self.assertEqual(data["prior"], 0.25)

    def test_posterior_computation(self):
        post = ComprehensiveBayesianHistoricityEngine.compute_joint_posteriors()
        norm_post = post["normalized_posteriors"]
        self.assertAlmostEqual(sum(norm_post.values()), 1.0, places=5)
        self.assertEqual(post["best_hypothesis"], "H4_IRON_AGE_HISTORICAL_EMERGENCE")
        self.assertGreater(norm_post["H4_IRON_AGE_HISTORICAL_EMERGENCE"], 0.999)

    def test_bayes_factors(self):
        post = ComprehensiveBayesianHistoricityEngine.compute_joint_posteriors()
        bfs = post["bayes_factors"]
        self.assertGreater(bfs["H4_over_H1_Myth"], 1e7)
        self.assertGreater(bfs["H4_over_H2_Literalism_3102BCE"], 1e12)
        self.assertGreater(bfs["H4_over_H3_Sanauli_1900BCE"], 1e5)


if __name__ == "__main__":
    unittest.main()
