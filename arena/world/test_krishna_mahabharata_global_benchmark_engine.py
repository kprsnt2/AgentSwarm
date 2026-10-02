"""
test_krishna_mahabharata_global_benchmark_engine.py

Unit test suite for the Global Historiographical Benchmark & Epistemic Closure Engine:
Lord Krishna and the Mahabharata War.
"""

import unittest
from krishna_mahabharata_global_benchmark_engine import (
    HistoricalEvidenceIndex,
    NicaksuFloodModel,
    SiddhanticEpochAnalyzer,
    MultiTraditionConcordance,
    TextualGrowthKinetics,
    GrandEpistemicAdjudicator
)

class TestKrishnaMahabharataGlobalBenchmarkEngine(unittest.TestCase):

    def test_hei_computation_and_rankings(self):
        """Test calculation of Historical Evidence Index and cohort ordering."""
        rankings = HistoricalEvidenceIndex.rank_all_profiles()
        self.assertEqual(len(rankings), 8)
        names = [r["name"] for r in rankings]

        # Fully documented figures should top the list
        self.assertIn("Socrates", names[:2])
        self.assertIn("Gautama_Buddha", names[:2])

        # King David and Krishna should occupy middle-high tier (strong historic core)
        self.assertIn(names[2], ["King_David", "Krishna_Vasudeva"])
        self.assertIn(names[3], ["King_David", "Krishna_Vasudeva"])

        # Legendary/folkloric figures should rank lower
        self.assertIn("Achilles", names[4:])
        self.assertIn("King_Arthur", names[4:])
        self.assertIn("Romulus", names[4:])
        self.assertIn("Moses", names[4:])

    def test_krishna_hei_score_bounds(self):
        """Verify Krishna Vasudeva's HEI score is rigorously bounded."""
        rankings = HistoricalEvidenceIndex.rank_all_profiles()
        krishna = next(r for r in rankings if r["name"] == "Krishna_Vasudeva")
        self.assertGreaterEqual(krishna["hei_score"], 7.5)
        self.assertLessEqual(krishna["hei_score"], 8.5)

        # Krishna score must exceed Arthur, Achilles, Romulus, Moses
        for comp in ["Achilles", "King_Arthur", "Romulus", "Moses"]:
            comp_profile = next(r for r in rankings if r["name"] == comp)
            self.assertGreater(krishna["hei_score"], comp_profile["hei_score"])

    def test_nicaksu_flood_relocation(self):
        """Verify dynastic actuarial calculation matches Hastinapura flood stratum."""
        flood_eval = NicaksuFloodModel.compute_concordance_z_score(950.0)
        # 5 generations * 18.5 = 92.5 years -> 950 - 92.5 = 857.5 BCE
        self.assertAlmostEqual(flood_eval["predicted_flood_bce"], 857.5, delta=1.0)
        # Discrepancy with C-14 mean (850 BCE) should be < 10 years
        self.assertLess(abs(flood_eval["discrepancy_years"]), 10.0)
        # Z-score should be tiny (< 0.3)
        self.assertLess(abs(flood_eval["z_score"]), 0.3)
        self.assertGreater(flood_eval["concordance_p_value"], 0.8)

    def test_siddhantic_zero_conjunction(self):
        """Verify Siddhantic mathematical model defines all mean longitudes as 0.0 at t=0."""
        mean_longs = SiddhanticEpochAnalyzer.verify_siddhantic_zero_conjunction()
        for planet, longitude in mean_longs.items():
            self.assertEqual(longitude, 0.0)

    def test_de431_celestial_scatter_3102_bce(self):
        """Verify real astronomical longitudes in 3102 BCE were widely dispersed."""
        scatter = SiddhanticEpochAnalyzer.evaluate_real_celestial_scatter_3102_bce()
        self.assertGreater(scatter["angular_span_deg"], 40.0)
        self.assertFalse(scatter["is_exact_conjunction"])
        self.assertFalse(scatter["is_single_sign_cluster"])
        self.assertGreater(scatter["max_distance_from_mesha_zero_deg"], 60.0)

    def test_multi_tradition_concordance(self):
        """Verify multi-tradition cross-attestation across all four ancient corpora."""
        metrics = MultiTraditionConcordance.compute_concordance_metrics()
        self.assertEqual(metrics["total_core_attributes"], 8)
        self.assertGreater(metrics["overall_cross_tradition_coverage"], 0.6)
        # Mathura, Vrishni, Statesman, Non-monarchical governance should be triply or quadruply attested
        self.assertIn("Mathura_homeland", metrics["triply_attested_attributes"])
        self.assertIn("Vrishni_clan_affiliation", metrics["triply_attested_attributes"])
        self.assertIn("Non_monarchical_republican_structure", metrics["triply_attested_attributes"])

    def test_textual_growth_kinetics(self):
        """Verify verse accumulation rates and BORI pruning metrics."""
        rates = TextualGrowthKinetics.calculate_growth_rates()
        self.assertEqual(len(rates), 3)

        # Doubling times show early rapid growth and late medieval deceleration (logistic curve)
        self.assertAlmostEqual(rates[0]["doubling_time_years"], 310.8, delta=5.0)  # Jaya -> Bharata
        self.assertAlmostEqual(rates[1]["doubling_time_years"], 524.6, delta=5.0)  # Bharata -> Critical Ed
        self.assertAlmostEqual(rates[2]["doubling_time_years"], 3009.4, delta=10.0) # Critical Ed -> Vulgate (saturation)

        # BORI pruning ratio
        prune = TextualGrowthKinetics.bori_critical_edition_pruning_ratio()
        self.assertAlmostEqual(prune["interpolation_percentage"], 26.22, delta=0.5)

    def test_grand_epistemic_adjudication(self):
        """Verify comprehensive output of the final adjudication."""
        adj = GrandEpistemicAdjudicator.get_definitive_adjudication()
        self.assertIn("krishna_historicity", adj)
        self.assertIn("mahabharata_war_historicity", adj)
        self.assertIn("mythological_amplification", adj)
        self.assertIn("theological_plane", adj)

        self.assertGreater(adj["krishna_historicity"]["confidence_probability"], 0.95)
        self.assertGreater(adj["mahabharata_war_historicity"]["confidence_probability"], 0.95)
        self.assertEqual(adj["krishna_historicity"]["hei_rank_in_cohort"], 4)


if __name__ == "__main__":
    unittest.main()
