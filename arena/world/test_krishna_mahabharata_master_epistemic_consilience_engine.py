"""
test_krishna_mahabharata_master_epistemic_consilience_engine.py
===============================================================
Unit test suite for the Master Epistemic Consilience & Multi-Dimensional
Historical Analysis Engine (krishna_mahabharata_master_epistemic_consilience_engine.py).

Verifies:
  1. Tripartite Demarcation for Krishna and Mahabharata historicity.
  2. BORI Critical Edition vs Vulgate textual metrics and parva accretion rates.
  3. Epigraphic Vrishni phylogeny and continuous apotheosis rate computation.
  4. Marine and terrestrial Dwarka stratigraphic adjudication.
  5. Archaeoastronomy combinatorial degrees of freedom and Aryabhata retro-calculation mechanics.
  6. 24-Dimensional Bayesian consilience computation, Bayes factors, and hypothesis adjudication.

Author: Kepler (A001), Swarm Research Agent (Gen 0)
Workspace: D:/AgentSwarm/arena/world
"""

import unittest
from krishna_mahabharata_master_epistemic_consilience_engine import (
    EpistemicPlane,
    MasterTripartiteDemarcator,
    TextualStratigraphyStemmatics,
    EpigraphicVrishniPhylogeny,
    MarineDwarkaStratigraphy,
    ArchaeoastronomyCombinatorialAnalyzer,
    Master24DBayesianConsilienceEngine,
    run_comprehensive_engine_evaluation
)


class TestMasterTripartiteDemarcator(unittest.TestCase):
    def test_krishna_historicity_demarcation(self):
        dem = MasterTripartiteDemarcator.get_demarcation("KRISHNA_HISTORICITY")
        self.assertIn("inquiry", dem)
        self.assertIn("primary_evidence", dem)
        self.assertIn("scholarly_consensus", dem)
        self.assertIn("devotional_claim", dem)
        self.assertTrue(len(dem["primary_evidence"]) >= 5)
        self.assertIn("Chandogya Upanishad", dem["primary_evidence"][0])
        self.assertIn("Svayam Bhagavan", dem["devotional_claim"])

    def test_mahabharata_war_demarcation(self):
        dem = MasterTripartiteDemarcator.get_demarcation("MAHABHARATA_WAR_HISTORICITY")
        self.assertIn("primary_evidence", dem)
        self.assertIn("scholarly_consensus", dem)
        self.assertIn("devotional_claim", dem)
        self.assertIn("PGW", dem["primary_evidence"][0])
        self.assertIn("15,000–30,000", dem["scholarly_consensus"])
        self.assertIn("18 Akshauhinis", dem["devotional_claim"])


class TestTextualStratigraphyStemmatics(unittest.TestCase):
    def test_textual_metrics_calculation(self):
        metrics = TextualStratigraphyStemmatics.calculate_textual_metrics()
        self.assertGreater(metrics["total_vulgate_verses"], metrics["total_bori_verses"])
        self.assertGreater(metrics["purged_spurious_verses"], 9000)
        self.assertGreater(metrics["vulgate_inflation_pct"], 10.0)
        self.assertIn("10_Sauptika", metrics["archaic_core_parvas"])
        self.assertIn("1_Adi", metrics["heavily_interpolated_parvas"])


class TestEpigraphicVrishniPhylogeny(unittest.TestCase):
    def test_epigraphic_record_and_apotheosis(self):
        res = EpigraphicVrishniPhylogeny.compute_apotheosis_rate()
        self.assertEqual(res["total_epigraphic_witnesses"], 9)
        self.assertEqual(res["time_span_years"], 1200)
        self.assertGreater(res["mean_apotheosis_rate_per_century"], 0.05)
        self.assertLess(res["mean_apotheosis_rate_per_century"], 0.15)
        self.assertIn("HELIODORUS", [w["id"] for w in EpigraphicVrishniPhylogeny.EPIGRAPHIC_RECORD])


class TestMarineDwarkaStratigraphy(unittest.TestCase):
    def test_marine_dwarka_evaluation(self):
        res = MarineDwarkaStratigraphy.evaluate_dwarka_claims()
        self.assertEqual(res["total_anchors_recorded"], 60)
        self.assertIn("Late Harappan", res["terrestrial_earliest_habitation_bet_dwarka"])
        self.assertIn("1st century BCE", res["terrestrial_earliest_habitation_dwarka_town"])
        self.assertIn("refute claims of a submerged 9,000-year-old", res["verdict"])


class TestArchaeoastronomyCombinatorialAnalyzer(unittest.TestCase):
    def test_alignment_collision_probability(self):
        res = ArchaeoastronomyCombinatorialAnalyzer.calculate_alignment_collision_probability(
            target_span_years=5000,
            nakshatra_tolerance=1,
            planets_tracked=5
        )
        self.assertGreater(res["expected_spurious_matches"], 1.0)
        self.assertGreater(res["probability_of_at_least_one_false_match"], 0.6)

    def test_aryabhata_deconstruction(self):
        res = ArchaeoastronomyCombinatorialAnalyzer.deconstruct_aryabhata_3102_bce()
        self.assertEqual(res["calculation_year_ce"], 499)
        self.assertEqual(res["implied_start_year_bce"], 3102)
        self.assertEqual(res["epistemic_classification"], EpistemicPlane.SCHOLARLY_HISTORICAL_CONSENSUS)


class TestMaster24DBayesianConsilienceEngine(unittest.TestCase):
    def test_bayesian_posterior_computation(self):
        res = Master24DBayesianConsilienceEngine.compute_bayesian_posterior()
        self.assertEqual(res["total_dimensions_evaluated"], 24)
        self.assertEqual(res["definitive_winner"], "H5_HISTORICAL_NUCLEUS")
        self.assertGreater(res["winning_posterior"], 0.99999999)
        self.assertLess(res["posterior_probabilities"]["H1_MYTHICISM"], 1e-15)
        self.assertLess(res["posterior_probabilities"]["H2_LITERALISM"], 1e-40)

    def test_run_comprehensive_engine_evaluation(self):
        full_res = run_comprehensive_engine_evaluation()
        self.assertIn("demarcation_krishna", full_res)
        self.assertIn("demarcation_war", full_res)
        self.assertIn("text_metrics", full_res)
        self.assertIn("apotheosis_metrics", full_res)
        self.assertIn("dwarka_metrics", full_res)
        self.assertIn("astro_alignment", full_res)
        self.assertIn("aryabhata_deconstruction", full_res)
        self.assertIn("bayesian_closure", full_res)


if __name__ == "__main__":
    unittest.main()
