"""
Unit test suite for hindu_multiverse_advanced_frontiers_engine.py
Verifies concentric sheath metrics, hierarchical time dilation calculations,
multiverse heterogeneity distributions, comparative taxonomy, and protocol safeguards.
"""

import unittest
import math
from hindu_multiverse_advanced_frontiers_engine import (
    ConcentricSheathEngine,
    RelativisticCosmologicalTimeDilationEngine,
    MultiverseHeterogeneityEngine,
    GlobalCosmologicalTaxonomyEngine,
    EpistemicSafeguardValidator,
    ProtocolViolationType,
    YOJANA_KM_STANDARD,
    PURANIC_BRAHMANDA_DIAMETER_YOJANAS,
    PURANIC_BRAHMANDA_RADIUS_YOJANAS
)


class TestHinduMultiverseAdvancedFrontiersEngine(unittest.TestCase):

    def test_concentric_sheath_diameter_base(self):
        data = ConcentricSheathEngine.calculate_sheath_dimensions("diameter_base")
        self.assertEqual(len(data["layers"]), 7)

        # Inner Brahmanda radius in AU is ~21.52 AU
        self.assertGreater(data["inner_brahmanda_radius_au"], 21.0)
        self.assertLess(data["inner_brahmanda_radius_au"], 22.0)

        # Check exponential sheath thicknesses:
        # Layer 1 = 5e9 yojanas
        # Layer 7 = 5e15 yojanas
        layer1 = data["layers"][0]
        layer7 = data["layers"][6]
        self.assertEqual(layer1.element_sanskrit, "Prithvi")
        self.assertEqual(layer1.thickness_yojanas, 5_000_000_000.0)
        self.assertEqual(layer7.element_sanskrit, "Mahat-tattva")
        self.assertEqual(layer7.thickness_yojanas, 5_000_000_000_000_000.0)

        # Total envelope outer radius:
        # R_total = 2.5e8 + 5e9 * (1 + 10 + ... + 10^6) = 2.5e8 + 5e9 * 1,111,111 = 5.55555525e15 yojanas
        self.assertGreater(data["total_envelope_radius_ly"], 7000.0)
        self.assertLess(data["total_envelope_radius_ly"], 8000.0)
        self.assertGreater(data["total_envelope_diameter_ly"], 14000.0)
        self.assertLess(data["total_envelope_diameter_ly"], 16000.0)

        # Volume expansion factor should exceed 10^21
        self.assertGreater(data["volume_expansion_ratio"], 1e21)
        self.assertGreater(data["log10_volume_expansion"], 21.0)

        # Milky Way fraction (~15% of 100,000 ly)
        self.assertGreater(data["milky_way_scale_percentage"], 10.0)
        self.assertLess(data["milky_way_scale_percentage"], 20.0)

    def test_concentric_sheath_radius_base(self):
        data = ConcentricSheathEngine.calculate_sheath_dimensions("radius_base")
        self.assertEqual(len(data["layers"]), 7)
        # With radius base, total envelope radius is ~3,780 light-years
        self.assertGreater(data["total_envelope_radius_ly"], 3500.0)
        self.assertLess(data["total_envelope_radius_ly"], 4000.0)

    def test_concentric_sheath_equal_diameter_base(self):
        data = ConcentricSheathEngine.calculate_sheath_dimensions("equal_diameter_base")
        self.assertEqual(len(data["layers"]), 7)
        # Total envelope radius is ~756 light-years
        self.assertGreater(data["total_envelope_radius_ly"], 700.0)
        self.assertLess(data["total_envelope_radius_ly"], 800.0)

    def test_kakudmi_revati_time_dilation(self):
        res = RelativisticCosmologicalTimeDilationEngine.calculate_kakudmi_revati_time_dilation(1.0)
        # Earth elapsed time: 27 Mahayugas = 116.64 million years
        self.assertEqual(res["earth_elapsed_years"], 116_640_000.0)
        # 1 muhurta = 48 min = 9.125e-5 years
        # Gamma should be ~1.278e12
        self.assertGreater(res["gamma_time_dilation_factor"], 1e12)
        self.assertLess(res["gamma_time_dilation_factor"], 2e12)
        self.assertGreater(res["log10_gamma"], 12.0)
        self.assertLess(res["log10_gamma"], 13.0)

    def test_brahma_lifespan_time_scaling(self):
        res = RelativisticCosmologicalTimeDilationEngine.calculate_brahma_lifespan_time_scaling()
        self.assertEqual(res["kalpa_solar_years"], 4.32e9)
        self.assertEqual(res["brahma_year_solar_years"], 3.1104e12)
        self.assertEqual(res["maha_kalpa_solar_years"], 3.1104e14)
        # 1 second of Brahma = 100,000 solar years
        self.assertEqual(res["one_second_of_brahma_in_human_years"], 100_000.0)

    def test_yoga_vasistha_idealist_time_dilation(self):
        res = RelativisticCosmologicalTimeDilationEngine.calculate_yoga_vasistha_idealist_time_dilation()
        self.assertEqual(len(res["scenarios"]), 3)
        # Check Lila's scenario: 100 years vs 72 hours
        lila = res["scenarios"][0]
        self.assertGreater(lila["time_ratio"], 10000.0)

    def test_multiverse_heterogeneity(self):
        dist = MultiverseHeterogeneityEngine.generate_multiverse_scale_distribution(5)
        self.assertEqual(len(dist), 6)
        # First entry: 4 heads, base diameter 500M yojanas ~ 43.03 AU
        self.assertEqual(dist[0]["brahma_heads"], 4)
        self.assertAlmostEqual(dist[0]["universe_diameter_au"], 43.03, delta=0.5)
        self.assertEqual(dist[0]["volume_ratio_to_our_brahmanda"], 1.0)

        # 8-headed Brahma (rank 1): 2x diameter, 8x volume
        self.assertEqual(dist[1]["brahma_heads"], 8)
        self.assertAlmostEqual(dist[1]["universe_diameter_au"], 86.06, delta=1.0)
        self.assertEqual(dist[1]["volume_ratio_to_our_brahmanda"], 8.0)

        # 128-headed Brahma (rank 5): 32x diameter, 32^3 = 32,768x volume
        self.assertEqual(dist[5]["brahma_heads"], 128)
        self.assertEqual(dist[5]["volume_ratio_to_our_brahmanda"], 32768.0)

    def test_global_cosmological_taxonomy(self):
        corpus = GlobalCosmologicalTaxonomyEngine.get_master_comparative_corpus()
        self.assertEqual(len(corpus), 8)
        traditions = [c["tradition"] for c in corpus]
        self.assertTrue(any("Puranic" in t for t in traditions))
        self.assertTrue(any("Yoga Vasistha" in t for t in traditions))
        self.assertTrue(any("Buddhist" in t for t in traditions))
        self.assertTrue(any("Jain" in t for t in traditions))
        self.assertTrue(any("Greek" in t for t in traditions))
        self.assertTrue(any("Islamic" in t for t in traditions))
        self.assertTrue(any("European" in t for t in traditions))
        self.assertTrue(any("Theoretical Physics" in t for t in traditions))

    def test_epistemic_safeguard_auditing(self):
        # Case 1: Scripture as laboratory data violation
        v1, msg1 = EpistemicSafeguardValidator.audit_proposition(
            "Bhagavata Purana measured cosmic inflation with telescope precision",
            treats_scripture_as_lab_data=True,
            treats_absence_as_proof_of_falsehood=False
        )
        self.assertEqual(v1, ProtocolViolationType.SCRIPTURE_AS_LAB_DATA)
        self.assertIn("VIOLATION", msg1)

        # Case 2: Absence as proof of falsehood violation
        v2, msg2 = EpistemicSafeguardValidator.audit_proposition(
            "Ancient India lacked calculus, therefore all descriptions of multiple worlds are invalid",
            treats_scripture_as_lab_data=False,
            treats_absence_as_proof_of_falsehood=True
        )
        self.assertEqual(v2, ProtocolViolationType.ABSENCE_AS_PROOF_OF_FALSEHOOD)
        self.assertIn("VIOLATION", msg2)

        # Case 3: Compliant audit
        v3, msg3 = EpistemicSafeguardValidator.audit_proposition(
            "Puranic texts historically formulate a 7-sheath cosmological model",
            treats_scripture_as_lab_data=False,
            treats_absence_as_proof_of_falsehood=False
        )
        self.assertEqual(v3, ProtocolViolationType.NONE)
        self.assertIn("COMPLIANT", msg3)


if __name__ == "__main__":
    unittest.main()
