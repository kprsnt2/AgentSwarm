"""
test_krishna_mahabharata_settlement_ecology_and_archaeoastronomy_engine.py

Unit test suite for the Settlement Ecology, Archaeoastronomy Deconstruction,
Game-Theoretic Bargaining, and Grand Meta-Epistemic Matrix Engine.

Authors: Kepler (A001), Swarm Research Agent (Gen 0)
Workspace: D:/AgentSwarm/arena/world
"""

import unittest
from krishna_mahabharata_settlement_ecology_and_archaeoastronomy_engine import (
    SettlementEcologyEngine,
    ArchaeoastronomyDeconstructionEngine,
    KuruBargainingGameTheoryEngine,
    GrandMetaEpistemicMatrixEngine,
    run_all_settlement_and_archaeoastronomy_analyses,
    EpistemicCategory
)


class TestSettlementEcologyEngine(unittest.TestCase):

    def test_pgw_carrying_capacity(self):
        result = SettlementEcologyEngine.calculate_pgw_carrying_capacity()
        self.assertGreater(result["total_settled_hectares"], 1500.0)
        self.assertGreater(result["estimated_regional_population"], 150000)
        self.assertLess(result["estimated_regional_population"], 350000)
        # Max sustainable army should be between 5,000 and 15,000 men
        self.assertGreaterEqual(result["max_sustainable_army_pgw"], 6000)
        self.assertLessEqual(result["max_sustainable_army_pgw"], 15000)
        # Epic claim of 3.94M combatants should be over 300x the capacity
        self.assertGreater(result["overstatement_factor"], 300.0)

    def test_rank_size_primacy(self):
        result = SettlementEcologyEngine.calculate_rank_size_primacy()
        # PGW primacy should be flatter than NBPW imperial primacy
        self.assertLess(result["pgw_primacy_ratio"], result["nbpw_primacy_ratio"])
        self.assertLess(result["pgw_zipf_slope_alpha"], result["nbpw_zipf_slope_alpha"])
        self.assertLess(result["pgw_primacy_ratio"], 2.0)
        self.assertGreater(result["nbpw_primacy_ratio"], 2.0)


class TestArchaeoastronomyDeconstructionEngine(unittest.TestCase):

    def test_astronomical_scatter(self):
        scatter = ArchaeoastronomyDeconstructionEngine.calculate_astronomical_scatter()
        # Dates span from 5561 BCE to 950 BCE -> spread > 4000 years
        self.assertGreater(scatter["spread_years"], 4000)
        self.assertEqual(scatter["earliest_claimed_date_bce"], 5561)
        self.assertGreater(scatter["standard_deviation_years"], 1000)

    def test_combinatorial_false_positives(self):
        result = ArchaeoastronomyDeconstructionEngine.calculate_combinatorial_false_positive_rate()
        self.assertEqual(result["search_window_years"], 5000)
        # Chance of an accidental match in 5000 years should be over 80%
        self.assertGreater(result["probability_of_accidental_match"], 0.80)
        # Expected number of false positive dates > 5.0
        self.assertGreater(result["expected_number_of_false_positive_dates"], 5.0)

    def test_bori_contradictions_presence(self):
        contradictions = ArchaeoastronomyDeconstructionEngine.BORI_TEXTUAL_CONTRADICTIONS
        self.assertGreaterEqual(len(contradictions), 4)
        refs = [c["verse_ref"] for c in contradictions]
        self.assertIn("MBh 5.141.7", refs)
        self.assertIn("MBh 6.2.23", refs)


class TestKuruBargainingGameTheoryEngine(unittest.TestCase):

    def test_bargaining_breakdown(self):
        model = KuruBargainingGameTheoryEngine.model_five_villages_bargaining()
        self.assertTrue(model["bargaining_collapse_condition_met"])
        self.assertGreater(model["duryodhana_expected_utility_war"], model["duryodhana_perceived_utility_peace"])
        self.assertEqual(model["pandava_demand_five_villages"], 0.05)
        self.assertEqual(model["duryodhana_offer"], 0.0)
        self.assertGreaterEqual(len(model["mechanisms_of_failure"]), 3)


class TestGrandMetaEpistemicMatrixEngine(unittest.TestCase):

    def test_bayesian_posterior(self):
        posterior_data = GrandMetaEpistemicMatrixEngine.compute_grand_bayesian_posterior()
        self.assertEqual(posterior_data["winning_hypothesis"], "H4_HISTORICAL_NUCLEUS_WITH_ACCRETION")
        p_h4 = posterior_data["normalized_posteriors"]["H4_HISTORICAL_NUCLEUS_WITH_ACCRETION"]
        self.assertGreater(p_h4, 0.999999)

        # Other hypotheses must have negligible posterior
        for h in ["H1_DEVOTIONAL_LITERALISM", "H2_PURE_MYTHICIST", "H3_LATE_PRIESTLY_INVENTION"]:
            self.assertLess(posterior_data["normalized_posteriors"][h], 1e-5)


class TestFullPipeline(unittest.TestCase):

    def test_run_all(self):
        all_results = run_all_settlement_and_archaeoastronomy_analyses()
        self.assertIn("carrying_capacity", all_results)
        self.assertIn("rank_size_primacy", all_results)
        self.assertIn("astronomical_scatter", all_results)
        self.assertIn("combinatorial_false_positives", all_results)
        self.assertIn("game_theory_kuru_crisis", all_results)
        self.assertIn("grand_bayesian_posterior", all_results)


if __name__ == "__main__":
    unittest.main()
