"""
test_krishna_mahabharata_mnemohistory_and_definitive_closure_engine.py

Comprehensive unit test suite for:
- VedicTextualAnchorEngine
- MnemoHistoryCulturalMemoryEngine
- GeospatialEpicNetworkEngine
- BhagavadGitaIntertextualityEngine
- Unified16DimensionalBayesianEngine
- MasterTripartiteAdjudication
"""

import unittest
import math
from krishna_mahabharata_mnemohistory_and_definitive_closure_engine import (
    VedicTextualAnchorEngine,
    MnemoHistoryCulturalMemoryEngine,
    GeospatialEpicNetworkEngine,
    BhagavadGitaIntertextualityEngine,
    Unified16DimensionalBayesianEngine,
    MasterTripartiteAdjudication,
    EpistemicCategory
)


class TestVedicTextualAnchorEngine(unittest.TestCase):
    def setUp(self):
        self.engine = VedicTextualAnchorEngine()

    def test_witness_count_and_primacy(self):
        result = self.engine.calculate_aggregate_anchor_strength()
        self.assertEqual(result["num_witnesses"], 6)
        self.assertTrue(result["all_primary_texts"])
        self.assertGreater(result["mean_significance_weight"], 0.90)

    def test_chronological_span(self):
        result = self.engine.calculate_aggregate_anchor_strength()
        span = result["chronological_window_bce"]
        self.assertLessEqual(span[0], -1000)
        self.assertGreaterEqual(span[1], -550)


class TestMnemoHistoryCulturalMemoryEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MnemoHistoryCulturalMemoryEngine()

    def test_growth_kinetics(self):
        kinetics = self.engine.compute_growth_kinetics()
        self.assertGreater(kinetics["expansion_factor"], 10.0)
        self.assertGreater(kinetics["formulaic_decay_ratio"], 3.0)
        self.assertGreater(kinetics["deification_growth_ratio"], 10.0)
        self.assertGreater(kinetics["annual_exponential_growth_rate"], 0.0)


class TestGeospatialEpicNetworkEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GeospatialEpicNetworkEngine()

    def test_site_network(self):
        stats = self.engine.compute_network_statistics()
        self.assertEqual(stats["total_sites_surveyed"], 10)
        self.assertTrue(stats["universal_pgw_presence"])
        self.assertGreater(stats["mean_pgw_stratum_thickness_meters"], 1.0)
        self.assertLessEqual(stats["aggregate_c14_chronology_bce"][0], -1000)


class TestBhagavadGitaIntertextualityEngine(unittest.TestCase):
    def setUp(self):
        self.engine = BhagavadGitaIntertextualityEngine()

    def test_intertextual_matrix(self):
        matrix = self.engine.evaluate_intertextuality_matrix()
        self.assertGreaterEqual(matrix["num_epigraphic_links"], 5)
        self.assertTrue(matrix["all_primary_material"])
        self.assertGreater(matrix["mean_concordance_confidence"], 0.95)


class TestUnified16DimensionalBayesianEngine(unittest.TestCase):
    def setUp(self):
        self.engine = Unified16DimensionalBayesianEngine()

    def test_16_dimensions_present(self):
        self.assertEqual(len(self.engine.dimensions), 16)

    def test_grand_posterior_probabilities(self):
        res = self.engine.compute_grand_posterior()
        posteriors = res["posterior_probabilities"]
        # H4 should dominate overwhelmingly
        self.assertGreater(posteriors["H4"], 0.999999)
        self.assertLess(posteriors["H1"], 1e-10)
        self.assertLess(posteriors["H2"], 1e-20)
        self.assertLess(posteriors["H3"], 1e-10)

    def test_bayes_factors(self):
        res = self.engine.compute_grand_posterior()
        bfs = res["bayes_factors"]
        self.assertGreater(bfs["BF_H4_over_H1"], 1e20)
        self.assertGreater(bfs["BF_H4_over_H2"], 1e40)
        self.assertGreater(bfs["BF_H4_over_H3"], 1e20)


class TestMasterTripartiteAdjudication(unittest.TestCase):
    def test_demarcation_table(self):
        table = MasterTripartiteAdjudication.get_master_demarcation_table()
        self.assertEqual(len(table), 5)
        for row in table:
            self.assertIn("domain", row)
            self.assertIn("primary_evidence", row)
            self.assertIn("scholarly_consensus", row)
            self.assertIn("devotional_claim", row)

    def test_falsifiability_criteria(self):
        criteria = MasterTripartiteAdjudication.get_falsifiability_criteria()
        self.assertEqual(len(criteria), 4)
        for c in criteria:
            self.assertIn("potential_discovery", c)
            self.assertIn("impact_on_model", c)


if __name__ == "__main__":
    unittest.main()
