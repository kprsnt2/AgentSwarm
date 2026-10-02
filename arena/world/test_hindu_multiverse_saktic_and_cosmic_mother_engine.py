"""
test_hindu_multiverse_saktic_and_cosmic_mother_engine.py
========================================================
Unit and regression test suite for the Shakta Multiverse and Cosmic Mother Engine.
"""

import unittest
import math
from hindu_multiverse_saktic_and_cosmic_mother_engine import (
    TrimurtiDemotionEngine,
    ManidvipaTopographyEngine,
    TripadVibhutiPartitionEngine,
    DarpanaNyayaMirrorEngine,
    SaktaEpistemicDemarcationEngine,
    ShaktaMultiverseMasterSuite,
    BASE_ENSEMBLE_SCALE_KOTI_KOTI
)


class TestTrimurtiDemotionEngine(unittest.TestCase):
    def test_demographic_census_base(self):
        census = TrimurtiDemotionEngine.compute_demographics(scale_factor_k=1.0)
        self.assertEqual(census.ensemble_universes, 1.0e14)
        self.assertEqual(census.total_brahmas, 1.0e14)
        self.assertEqual(census.total_visnus, 1.0e14)
        self.assertEqual(census.total_rudras, 1.0e14)
        self.assertEqual(census.total_trimurti_officers, 3.0e14)
        # Indras: 36,000 day kalpas * 14 manvantaras = 504,000 per universe
        self.assertEqual(census.indras_per_universe_lifetime, 504000.0)
        self.assertEqual(census.total_indras_ensemble, 5.04e19)

    def test_demographic_census_scaling(self):
        census = TrimurtiDemotionEngine.compute_demographics(scale_factor_k=5.0)
        self.assertEqual(census.ensemble_universes, 5.0e14)
        self.assertEqual(census.total_trimurti_officers, 1.5e15)

    def test_invalid_scale_factor(self):
        with self.assertRaises(ValueError):
            TrimurtiDemotionEngine.compute_demographics(scale_factor_k=0.0)
        with self.assertRaises(ValueError):
            TrimurtiDemotionEngine.compute_demographics(scale_factor_k=-2.5)

    def test_theological_hierarchy(self):
        hier = TrimurtiDemotionEngine.get_theological_status_hierarchy()
        self.assertEqual(len(hier), 4)
        traditions = [h["tradition"] for h in hier]
        self.assertTrue(any("Shakta" in t for t in traditions))
        self.assertTrue(any("Vaisnava" in t for t in traditions))


class TestManidvipaTopographyEngine(unittest.TestCase):
    def test_ramparts_count_and_order(self):
        ramparts = ManidvipaTopographyEngine.get_ramparts_catalog()
        self.assertEqual(len(ramparts), 18)
        for idx, r in enumerate(ramparts, start=1):
            self.assertEqual(r.enclosure_number, idx)
            self.assertTrue(len(r.sanskrit_name) > 0)
            self.assertTrue(len(r.material_substance) > 0)

    def test_first_and_last_ramparts(self):
        ramparts = ManidvipaTopographyEngine.get_ramparts_catalog()
        # First rampart is Iron (Ayasa)
        self.assertIn("Ayasa", ramparts[0].sanskrit_name)
        # 18th rampart is Manikya (Ruby)
        self.assertIn("Manikya", ramparts[17].sanskrit_name)

    def test_central_sanctum_architecture(self):
        sanctum = ManidvipaTopographyEngine.get_central_sanctum_architecture()
        self.assertEqual(sanctum["mansion_name"], "Cintamani-grha (House of Wish-Fulfilling Gems)")
        cs = sanctum["central_structure"]
        self.assertEqual(len(cs["legs_of_throne"]), 4)
        # Check that Brahma, Visnu, Rudra, Isvara are the 4 legs
        legs = [leg["deity"] for leg in cs["legs_of_throne"]]
        self.assertListEqual(legs, ["Brahma", "Visnu", "Rudra", "Isvara"])
        # Check seat plank is Sadasiva
        self.assertEqual(cs["seat_plank"]["deity"], "Sadasiva")


class TestTripadVibhutiPartitionEngine(unittest.TestCase):
    def test_partition_shares(self):
        partitions = TripadVibhutiPartitionEngine.compute_partition_metrics()
        self.assertEqual(len(partitions), 2)
        total_share = sum(p.fractional_share for p in partitions)
        self.assertAlmostEqual(total_share, 1.0, places=5)
        # Material is 0.25 (Ekapad), Transcendent is 0.75 (Tripad)
        self.assertEqual(partitions[0].fractional_share, 0.25)
        self.assertEqual(partitions[1].fractional_share, 0.75)
        # Material is dissolution susceptible; Transcendent is not
        self.assertTrue(partitions[0].dissolution_susceptibility)
        self.assertFalse(partitions[1].dissolution_susceptibility)

    def test_dark_energy_concordism_audit(self):
        audit = TripadVibhutiPartitionEngine.evaluate_dark_energy_concordism()
        self.assertEqual(audit["textual_ratio"], 0.75)
        self.assertAlmostEqual(audit["astrophysical_dark_energy_share"], 0.6837, places=4)
        self.assertIn("Fatal Category Error", audit["epistemic_verdict"])


class TestDarpanaNyayaMirrorEngine(unittest.TestCase):
    def test_stone_multiverse_metrics(self):
        metrics = DarpanaNyayaMirrorEngine.evaluate_stone_multiverse(stone_volume_m3=1.0)
        self.assertEqual(metrics.apparent_universe_diameter_ly, 15120.0)
        self.assertGreater(metrics.apparent_universe_volume_m3, 1.0e60)
        self.assertGreater(metrics.volumetric_ratio, 1.0e60)
        # Schwarzschild radius for solar mass is ~2953 m, which is >> 0.62 m (radius of 1 m^3 stone)
        self.assertTrue(metrics.is_gravitationally_collapsed)
        self.assertIn("Abhasavada", metrics.ontological_verdict)


class TestSaktaEpistemicDemarcationEngine(unittest.TestCase):
    def test_source_matrix_classifications(self):
        sources = SaktaEpistemicDemarcationEngine.get_source_matrix()
        classes = {s["classification"] for s in sources}
        self.assertIn("Primary Text", classes)
        self.assertIn("Scholarly Indological Consensus", classes)
        self.assertIn("Devotional / Apologetic Claim", classes)

    def test_concordism_penalty(self):
        pen = SaktaEpistemicDemarcationEngine.compute_concordism_penalty()
        self.assertLess(pen["concordance_score_percent"], 0.1)  # Less than 0.1%
        self.assertGreater(pen["firewall_rigor_percent"], 90.0)  # > 90%


class TestShaktaMultiverseMasterSuite(unittest.TestCase):
    def test_master_suite_execution(self):
        suite = ShaktaMultiverseMasterSuite(scale_k=2.0)
        report = suite.generate_full_report()
        self.assertEqual(report["demographic_census"]["ensemble_universes"], 2.0e14)
        self.assertEqual(report["total_ramparts"], 18)
        self.assertEqual(len(report["vibhuti_partition"]), 2)
        self.assertIn("concordance_score_percent", report["concordism_penalty"])


if __name__ == "__main__":
    unittest.main()
