"""
Unit test suite for hindu_multiverse_al_biruni_and_transmission_engine.py.

Verifies:
1. Al-Biruni geodetic accuracy and comparison with Aryabhata and Brahmagupta.
2. Metaphor metrics calculation (wood-apple seeds, mustard seed packing in pot and warehouse).
3. Sphere packing calculations (Kepler optimal FCC vs Random Close Packing).
4. Comparative traditions registry consistency.
5. Epistemic demarcation audit logic.
"""

import math
import unittest

from hindu_multiverse_al_biruni_and_transmission_engine import (
    AlBiruniComparativeEngine,
    CosmologicalTradition,
    EpistemicCategory,
    run_comprehensive_analysis,
)


class TestAlBiruniComparativeEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AlBiruniComparativeEngine()

    def test_textual_passages_integrity(self):
        self.assertGreaterEqual(len(self.engine.textual_passages), 5)
        categories = {p.category for p in self.engine.textual_passages}
        self.assertIn(EpistemicCategory.HISTORICAL_SCHOLARSHIP, categories)
        self.assertIn(EpistemicCategory.PRIMARY_TEXT, categories)

    def test_geodetic_accuracies(self):
        # Al-Biruni Nandana measurement should have relative error < 1.0%
        biruni_geo = self.engine.geodetic_comparisons[0]
        self.assertEqual(biruni_geo.source_name, "Al-Bīrūnī (Nandana Fort Trigonometric Horizon Dip)")
        self.assertLess(biruni_geo.relative_error_percent, 1.0)

        # Aryabhata Earth circumference error should be < 1.0%
        aryabhata_geo = self.engine.geodetic_comparisons[1]
        self.assertLess(aryabhata_geo.relative_error_percent, 1.0)

        # Brahmagupta Earth circumference error should be < 1.0%
        brahmagupta_geo = self.engine.geodetic_comparisons[2]
        self.assertLess(brahmagupta_geo.relative_error_percent, 1.0)

        # Puranic flat disc should have astronomical relative error > 1000%
        puranic_geo = self.engine.geodetic_comparisons[3]
        self.assertGreater(puranic_geo.relative_error_percent, 1000.0)

    def test_metaphor_metrics(self):
        metrics_dict = {m.name: m for m in self.engine.metaphor_metrics}
        self.assertIn("Wood-Apple Seeds in Pulp", metrics_dict)
        self.assertIn("Mustard Seeds in a Domestic Pot", metrics_dict)
        self.assertIn("Mustard Seeds in a Grain Storehouse", metrics_dict)

        # Wood-apple should have hundreds of seeds
        kavittha = metrics_dict["Wood-Apple Seeds in Pulp"]
        self.assertTrue(200 <= kavittha.calculated_universe_count <= 600)

        # 10L pot of mustard seeds should yield millions of universes
        pot = metrics_dict["Mustard Seeds in a Domestic Pot"]
        self.assertTrue(1.0e6 <= pot.calculated_universe_count <= 1.0e7)

        # 1 cubic meter storehouse should yield hundreds of millions
        storehouse = metrics_dict["Mustard Seeds in a Grain Storehouse"]
        self.assertTrue(1.0e8 <= storehouse.calculated_universe_count <= 1.0e9)

    def test_sphere_packing(self):
        # Packing radius: container 10, universe 1
        res_fcc = self.engine.compute_sphere_packing(10.0, 1.0, "kepler_optimal")
        self.assertAlmostEqual(res_fcc["packing_fraction"], math.pi / (3.0 * math.sqrt(2.0)), places=5)
        # Volume ratio is 10^3 = 1000. Count should be 1000 * 0.74048 ~ 740.48
        self.assertAlmostEqual(res_fcc["universes_packed"], 1000.0 * (math.pi / (3.0 * math.sqrt(2.0))), places=2)

        res_rcp = self.engine.compute_sphere_packing(10.0, 1.0, "random_close_packing")
        self.assertAlmostEqual(res_rcp["packing_fraction"], 0.64, places=2)
        self.assertAlmostEqual(res_rcp["universes_packed"], 640.0, places=1)

        # Invalid cases
        with self.assertRaises(ValueError):
            self.engine.compute_sphere_packing(-1.0, 1.0)

        # Universe larger than container
        res_zero = self.engine.compute_sphere_packing(1.0, 10.0)
        self.assertEqual(res_zero["universes_packed"], 0)

    def test_comparative_traditions(self):
        traditions = self.engine.evaluate_comparative_traditions()
        self.assertEqual(len(traditions), 6)
        names = [t["tradition"] for t in traditions]
        self.assertIn(CosmologicalTradition.HINDU_PURANIC.value, names)
        self.assertIn(CosmologicalTradition.HINDU_SIDDHANTIC.value, names)
        self.assertIn(CosmologicalTradition.ISLAMIC_KALAM.value, names)
        self.assertIn(CosmologicalTradition.ARISTOTELIAN_PTOLEMAIC.value, names)
        self.assertIn(CosmologicalTradition.GRECO_ROMAN_ATOMISM.value, names)
        self.assertIn(CosmologicalTradition.BUDDHIST_MAHAYANA.value, names)

    def test_demarcation_audit(self):
        audit = self.engine.run_epistemic_demarcation_audit()
        self.assertEqual(len(audit), 4)
        for claim in audit:
            self.assertIn("claim_id", claim)
            self.assertIn("epistemic_verdict", claim)
            self.assertIn("historical_reality", claim)
            self.assertIn("primary_evidence", claim)

    def test_comprehensive_analysis_runner(self):
        results = run_comprehensive_analysis()
        self.assertEqual(results["textual_passages_count"], 6)
        self.assertGreater(results["karanodaka_fcc_count"], 1.0e10)
        self.assertGreater(results["karanodaka_rcp_count"], 1.0e10)


if __name__ == "__main__":
    unittest.main()
