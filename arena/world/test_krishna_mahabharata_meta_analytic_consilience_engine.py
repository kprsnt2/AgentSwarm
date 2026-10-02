"""
test_krishna_mahabharata_meta_analytic_consilience_engine.py

Unit tests for krishna_mahabharata_meta_analytic_consilience_engine.py
Verifies:
- ArchaeogeneticsSubstrateEngine
- DemographicEnergeticCarryingEngine
- PhilologicalStratigraphyEntropyEngine
- NumismaticEpigraphicChronologyEngine
- Master20DimensionalBayesianClosureEngine
- DefinitiveTripartiteAdjudicationCompendium
"""

import unittest
import math
from krishna_mahabharata_meta_analytic_consilience_engine import (
    EpistemicPlane,
    ArchaeogeneticsSubstrateEngine,
    DemographicEnergeticCarryingEngine,
    PhilologicalStratigraphyEntropyEngine,
    NumismaticEpigraphicChronologyEngine,
    Master20DimensionalBayesianClosureEngine,
    DefinitiveTripartiteAdjudicationCompendium,
)


class TestArchaeogeneticsSubstrateEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ArchaeogeneticsSubstrateEngine()

    def test_genetic_continuity_and_refutations(self):
        res = self.engine.evaluate_paleogenomic_continuity()
        self.assertTrue(res["refutes_catastrophic_invasion"])
        self.assertTrue(res["refutes_isolated_static_myth"])
        self.assertGreater(res["steppe_mlba_percentage"], 15.0)
        self.assertGreater(res["indus_periphery_percentage"], 70.0)
        self.assertEqual(res["genetic_admixture_stabilization_bce"], 1000)


class TestDemographicEnergeticCarryingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DemographicEnergeticCarryingEngine()

    def test_literal_demographic_impossibility(self):
        literal = self.engine.compute_literal_demographic_footprint()
        # 18 Akshauhinis = 3.9366 million combatants
        self.assertAlmostEqual(literal["total_combatants"], 3936600.0, places=1)
        # Millions of liters of water daily
        self.assertGreater(literal["daily_water_millions_liters"], 50.0)
        # Consumes massive grain surplus (> 1.0 ratio of entire annual surplus of the realm)
        self.assertGreater(literal["surplus_exhaustion_ratio"], 1.0)

    def test_historical_chieftain_feasibility(self):
        hist = self.engine.compute_historical_chieftain_footprint()
        self.assertEqual(hist["total_humans"], 20000.0)
        self.assertEqual(hist["logistical_feasibility"], 1.0)
        # Grain requirement over 18 days is negligible fraction of annual regional surplus
        self.assertLess(hist["surplus_exhaustion_ratio"], 0.01)


class TestPhilologicalStratigraphyEntropyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PhilologicalStratigraphyEntropyEngine()

    def test_stratigraphic_gradients(self):
        gradients = self.engine.compute_stratigraphic_gradients()
        self.assertGreater(gradients["verse_expansion_factor"], 10.0)
        self.assertGreater(gradients["archaic_loss_ratio"], 10.0)
        self.assertGreater(gradients["formulaic_decay_ratio"], 3.0)


class TestNumismaticEpigraphicChronologyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = NumismaticEpigraphicChronologyEngine()

    def test_epigraphic_span_and_integrity(self):
        span = self.engine.evaluate_epigraphic_span()
        self.assertEqual(span["num_primary_witnesses"], 7)
        self.assertTrue(span["all_primary_evidence"])
        self.assertEqual(span["earliest_date_bce"], 700)
        self.assertEqual(span["latest_date_ce"], 15)
        self.assertGreater(span["span_years"], 700)


class TestMaster20DimensionalBayesianClosureEngine(unittest.TestCase):
    def setUp(self):
        self.engine = Master20DimensionalBayesianClosureEngine()

    def test_dimensions_count(self):
        self.assertEqual(len(self.engine.dimensions), 20)

    def test_bayesian_posterior_closure(self):
        res = self.engine.compute_grand_meta_posterior()
        posteriors = res["posterior_probabilities"]
        # H4 (Stratified Historical Nucleus) must overwhelmingly dominate
        self.assertGreater(posteriors["H4"], 0.9999999)
        self.assertLess(posteriors["H1"], 1e-15)
        self.assertLess(posteriors["H2"], 1e-30)
        self.assertLess(posteriors["H3"], 1e-25)

    def test_bayes_factors(self):
        res = self.engine.compute_grand_meta_posterior()
        bfs = res["bayes_factors"]
        self.assertGreater(bfs["BF_H4_over_H1"], 1e20)
        self.assertGreater(bfs["BF_H4_over_H2"], 1e40)
        self.assertGreater(bfs["BF_H4_over_H3"], 1e30)


class TestDefinitiveTripartiteAdjudicationCompendium(unittest.TestCase):
    def test_master_demarcation_table(self):
        table = DefinitiveTripartiteAdjudicationCompendium.get_master_demarcation_table()
        self.assertEqual(len(table), 4)
        for row in table:
            self.assertIn("topic", row)
            self.assertIn("primary_evidence", row)
            self.assertIn("scholarly_consensus", row)
            self.assertIn("devotional_claim", row)

    def test_falsifiability_conditions(self):
        conditions = DefinitiveTripartiteAdjudicationCompendium.get_epistemic_falsifiability_conditions()
        self.assertEqual(len(conditions), 4)
        for c in conditions:
            self.assertIn("contingent_discovery", c)
            self.assertIn("impact_on_model", c)


if __name__ == "__main__":
    unittest.main()
