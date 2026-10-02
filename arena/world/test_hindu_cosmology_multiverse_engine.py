"""
Test suite for hindu_cosmology_multiverse_engine.py using Python unittest
Verifies primary textual records, scholarly demarcations, devotional claim classifications,
quantitative solar-system scale calculations, and epistemic firewall protocol rules.
"""

import unittest
import math
from hindu_cosmology_multiverse_engine import (
    HinduMultiverseRegistry,
    PuranicDimensionalCalculator,
    EpistemicFirewallAdjudicator,
    EpistemicSourceCategory,
    CosmologicalScaleModel,
    ProtocolViolationType,
    compare_hindu_multiverse_to_modern_physics
)


class TestHinduCosmologyMultiverseEngine(unittest.TestCase):

    def test_registry_initialization(self):
        registry = HinduMultiverseRegistry()
        self.assertGreaterEqual(len(registry.primary_texts), 7)
        self.assertGreaterEqual(len(registry.scholarly_records), 3)
        self.assertGreaterEqual(len(registry.devotional_records), 3)

    def test_primary_text_citations(self):
        registry = HinduMultiverseRegistry()
        
        # Test Bhagavata Purana 10.14.11
        sb10 = registry.primary_texts["SB_10_14_11"]
        self.assertIn("kvāhaṁ", sb10.transliteration_iast)
        self.assertTrue("avigaṇitāṇḍa" in sb10.transliteration_iast or "parāṇu" in sb10.transliteration_iast)
        self.assertEqual(sb10.scale_model, CosmologicalScaleModel.PURANIC_EGG_MULTIVERSE)
        
        # Test Bhagavata Purana 6.16.37
        sb6 = registry.primary_texts["SB_6_16_37"]
        self.assertIn("kṣity-ādibhir", sb6.transliteration_iast)
        self.assertIn("saptabhir daśa-guṇottarair", sb6.transliteration_iast)
        
        # Test Brahma Samhita 5.35 & 5.48
        bs35 = registry.primary_texts["BS_5_35"]
        self.assertIn("jagad-aṇḍa-koṭiṁ", bs35.transliteration_iast)
        self.assertIn("paramāṇu", bs35.transliteration_iast)
        
        bs48 = registry.primary_texts["BS_5_48"]
        self.assertIn("loma-vilajā", bs48.transliteration_iast)
        
        # Test Yoga Vasistha
        yv = registry.primary_texts["YV_UTPATTI_LILA"]
        self.assertIn("paramāṇau paramāṇau", yv.transliteration_iast)
        self.assertEqual(yv.scale_model, CosmologicalScaleModel.YOGA_VASISTHA_IDEALIST)

        # Test Rigveda 10.129 baseline
        rv = registry.primary_texts["RV_10_129"]
        self.assertIn("nāsad āsīn", rv.transliteration_iast)
        self.assertEqual(rv.scale_model, CosmologicalScaleModel.VEDIC_TRIPARTITE)

    def test_puranic_dimensional_calculations(self):
        calc = PuranicDimensionalCalculator()
        dims = calc.calculate_brahmanda_dimensions()
        
        # Diameter is 500 million yojanas
        self.assertEqual(dims["diameter_yojanas"], 500_000_000.0)
        self.assertEqual(dims["radius_yojanas"], 250_000_000.0)
        
        # At standard 12.8748 km/yojana:
        # 500M * 12.8748 = 6.4374e9 km
        self.assertTrue(math.isclose(dims["diameter_km"], 6.4374e9, rel_tol=1e-3))
        
        # In Astronomical Units:
        # 6.4374e9 km / 149597870.7 km/AU ≈ 43.03 AU
        self.assertGreater(dims["diameter_au"], 40.0)
        self.assertLess(dims["diameter_au"], 45.0)
        self.assertGreater(dims["radius_au"], 20.0)
        self.assertLess(dims["radius_au"], 23.0)

    def test_astrophysical_comparison_solar_system_scale(self):
        calc = PuranicDimensionalCalculator()
        comparison = calc.compare_with_astrophysical_structures()
        
        # The Puranic Brahmanda radius (~21.5 AU) is comparable to Uranus/Neptune
        # and Pluto (aphelion 49.3 AU)
        self.assertLess(comparison["ratio_brahmanda_radius_to_neptune"], 1.0)
        self.assertGreater(comparison["ratio_brahmanda_radius_to_kuiper_outer"], 0.4)
        self.assertLess(comparison["ratio_brahmanda_radius_to_kuiper_outer"], 0.5)
        
        # Discrepancy between Brahmanda and Modern Observable Universe:
        # Ratio is ~ 1.3e14 (14 orders of magnitude!)
        self.assertGreater(comparison["log10_scale_discrepancy_universe_vs_brahmanda"], 13.0)
        self.assertLess(comparison["log10_scale_discrepancy_universe_vs_brahmanda"], 15.0)

    def test_puranic_multiverse_aggregate_volume(self):
        calc = PuranicDimensionalCalculator()
        # If there are 10 million (1 koti) Brahmandas
        res = calc.puranic_multiverse_aggregate_volume(num_universes=1e7)
        
        # Effective radius of 10 million packed Brahmandas:
        self.assertGreater(res["effective_aggregate_radius_au"], 4000.0)
        self.assertLess(res["effective_aggregate_radius_au"], 5000.0)
        # In light-years: ~0.073 light-years (well within the Oort Cloud!)
        self.assertGreater(res["effective_aggregate_radius_light_years"], 0.05)
        self.assertLess(res["effective_aggregate_radius_light_years"], 0.10)

    def test_epistemic_firewall_protocols(self):
        adj = EpistemicFirewallAdjudicator()
        
        # Check violation 1: Scripture as laboratory data
        v1 = adj.evaluate_protocol_compliance(
            "Bhagavata Purana predicted quantum entanglement",
            treats_scripture_as_lab_data=True,
            treats_absence_as_proof_of_falsehood=False
        )
        self.assertEqual(v1, ProtocolViolationType.SCRIPTURE_AS_LAB_DATA)
        
        # Check violation 2: Absence of evidence as proof of falsehood
        v2 = adj.evaluate_protocol_compliance(
            "Ancient texts do not describe physical general relativity, therefore they never discussed multiple worlds",
            treats_scripture_as_lab_data=False,
            treats_absence_as_proof_of_falsehood=True
        )
        self.assertEqual(v2, ProtocolViolationType.ABSENCE_AS_PROOF_OF_FALSEHOOD)
        
        # Compliant evaluation
        v3 = adj.evaluate_protocol_compliance(
            "Puranic texts historically document a theological multi-universe concept",
            treats_scripture_as_lab_data=False,
            treats_absence_as_proof_of_falsehood=False
        )
        self.assertEqual(v3, ProtocolViolationType.NONE)

    def test_source_classification(self):
        adj = EpistemicFirewallAdjudicator()
        c1 = adj.classify_claim_source(EpistemicSourceCategory.PRIMARY_TEXT)
        self.assertIn("Philological analysis", c1["valid_investigation"])
        
        c2 = adj.classify_claim_source(EpistemicSourceCategory.SCHOLARLY_CONSENSUS)
        self.assertIn("Peer-reviewed critical editions", c2["valid_investigation"])
        
        c3 = adj.classify_claim_source(EpistemicSourceCategory.DEVOTIONAL_CLAIM)
        self.assertIn("Must NOT present theological claims as scientifically verified", c3["invalid_treatment"])

    def test_modern_physics_comparison_matrix(self):
        matrix = compare_hindu_multiverse_to_modern_physics()
        self.assertEqual(len(matrix), 4)
        framework_names = [m["framework"] for m in matrix]
        self.assertTrue(any("Level I" in f for f in framework_names))
        self.assertTrue(any("Level II" in f for f in framework_names))
        self.assertTrue(any("Level III" in f for f in framework_names))
        self.assertTrue(any("Level IV" in f for f in framework_names))


if __name__ == "__main__":
    unittest.main()
