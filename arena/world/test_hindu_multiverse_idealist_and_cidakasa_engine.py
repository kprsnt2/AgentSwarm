"""
test_hindu_multiverse_idealist_and_cidakasa_engine.py

Comprehensive Unit Test Suite for hindu_multiverse_idealist_and_cidakasa_engine.py
Verifies mathematical models of Cidakasa topology, narrative time dilations,
recursive demiurgic trees, doppelganger identity models, and tripartite demarcation.
"""

import unittest
import math
from hindu_multiverse_idealist_and_cidakasa_engine import (
    AkasaTrayaModel,
    NarrativeTimeDilationModel,
    InduPutraDemiurgicTreeModel,
    DoppelgangerIdentityModel,
    EpistemologicalCorroborationEngine,
    TripartiteDemarcationAuditor,
    run_comprehensive_idealist_multiverse_analysis
)

class TestHinduMultiverseIdealistEngine(unittest.TestCase):

    def setUp(self):
        self.akasa = AkasaTrayaModel()

    def test_brahmanda_volume_calculation(self):
        vol = self.akasa.get_brahmanda_physical_volume_m3()
        # Radius = 250M yojana * 12.8 km = 3.2e9 km = 3.2e12 m
        # Vol = (4/3)*pi*r^3 approx 1.37e38 m^3
        self.assertGreater(vol, 1e38)
        self.assertLess(vol, 1e39)

    def test_spatial_collocation_cidakasa_vs_bhutakasa(self):
        res = self.akasa.evaluate_spatial_collocation(num_universes=100)
        self.assertEqual(res["num_universes"], 100)
        self.assertEqual(res["cidakasa_physical_displacement_m3"], 0.0)
        self.assertFalse(res["cidakasa_geometric_conflict"])
        self.assertGreater(res["bhutakasa_displacement_ratio"], 1e30)

    def test_lila_padma_time_dilation(self):
        res = NarrativeTimeDilationModel.calculate_lila_padma_dilation(days_in_universe_1=3.0,
                                                                      years_in_universe_2=70.0)
        expected_gamma = (70.0 * 365.25 * 86400.0) / (3.0 * 86400.0)
        self.assertAlmostEqual(res["dilation_factor_gamma"], expected_gamma, places=3)
        self.assertAlmostEqual(res["dilation_factor_gamma"], 8522.5, places=1)
        self.assertGreater(res["days_in_u2_per_u1_hour"], 300.0)

    def test_lavana_time_dilation(self):
        res = NarrativeTimeDilationModel.calculate_lavana_dilation(muhurtas_in_court=1.0,
                                                                 years_in_wilds=60.0)
        expected_gamma = (60.0 * 365.25 * 86400.0) / (48.0 * 60.0)
        self.assertAlmostEqual(res["dilation_factor_gamma"], expected_gamma, places=2)
        self.assertGreater(res["dilation_factor_gamma"], 600000.0)

    def test_gadhi_time_dilation(self):
        res = NarrativeTimeDilationModel.calculate_gadhi_dilation(seconds_in_river=30.0,
                                                                years_in_kira=60.0)
        expected_gamma = (60.0 * 365.25 * 86400.0) / 30.0
        self.assertAlmostEqual(res["dilation_factor_gamma"], expected_gamma, places=1)
        self.assertGreater(res["dilation_factor_gamma"], 6.0e7)

    def test_indu_putra_tree_branching(self):
        tree = InduPutraDemiurgicTreeModel(branching_factor=10)
        self.assertEqual(tree.universes_at_generation(0), 1)
        self.assertEqual(tree.universes_at_generation(1), 10)
        self.assertEqual(tree.universes_at_generation(2), 100)
        self.assertEqual(tree.universes_at_generation(5), 100000)

        # Cumulative checks: 1 + 10 + 100 = 111
        self.assertEqual(tree.cumulative_universes(2), 111)
        # Cumulative for gen 5: (10^6 - 1) / 9 = 111111
        self.assertEqual(tree.cumulative_universes(5), 111111)

    def test_indu_putra_edge_cases(self):
        tree = InduPutraDemiurgicTreeModel(branching_factor=10)
        with self.assertRaises(ValueError):
            tree.universes_at_generation(-1)
        with self.assertRaises(ValueError):
            tree.cumulative_universes(-1)

        single_tree = InduPutraDemiurgicTreeModel(branching_factor=1)
        self.assertEqual(single_tree.cumulative_universes(4), 5)

    def test_doppelganger_identity_evaluation(self):
        res = DoppelgangerIdentityModel.evaluate_identity()
        self.assertTrue(res["distinguishable_under_pramana"])
        self.assertFalse(res["violates_leibniz_indiscernibility"])
        self.assertIn("Ativahika", res["lila1_body_type"])
        self.assertIn("Adhibhautika", res["lila2_body_type"])

    def test_epistemological_corroboration(self):
        res = EpistemologicalCorroborationEngine.adjudicate_corroboration()
        self.assertIn("Dirgha-Svapna", res["advaitic_vasisthan_resolution"])
        self.assertIn("Drsti-Srsti-Vada", res["epistemic_demarcation"])

    def test_tripartite_demarcation_auditor(self):
        claims = TripartiteDemarcationAuditor.audit_all_claims()
        self.assertGreaterEqual(len(claims), 3)
        for claim in claims:
            self.assertIn("REJECT CONCORDISM", claim["demarcation_verdict"])
            self.assertIn("fallacy_type", claim)

    def test_full_pipeline_execution(self):
        results = run_comprehensive_idealist_multiverse_analysis()
        self.assertIn("collocation_single", results)
        self.assertIn("lila_dilation", results)
        self.assertIn("lavana_dilation", results)
        self.assertIn("gadhi_dilation", results)
        self.assertIn("tree_metrics", results)
        self.assertIn("demarcation_audits", results)

if __name__ == "__main__":
    unittest.main()
