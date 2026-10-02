"""test_hindu_multiverse_grand_unified_compendium_engine.py

Unit and integration tests for the Grand Unified Hindu Multiverse Engine.
Investigated by Kepler (A001), Generation 0.
"""

import unittest
import math
from hindu_multiverse_grand_unified_compendium_engine import (
    GrandUnifiedHinduMultiverseEngine,
    PhilologicalStratum,
    DarsanaPosition,
    MultiverseTypologyModel,
    ConcordistCritique,
)


class TestGrandUnifiedHinduMultiverseEngine(unittest.TestCase):

    def setUp(self):
        self.engine = GrandUnifiedHinduMultiverseEngine()

    def test_strata_completeness(self):
        """Verify that all major chronological strata from 1500 BCE to 1600 CE are represented."""
        expected_strata = [
            "vedic_samhita",
            "upanishadic",
            "epic_early_puranic",
            "high_bhagavata",
            "tantric_kashmir_shaiva",
            "late_saktic",
            "bengal_vaishnava",
        ]
        for s_key in expected_strata:
            self.assertIn(s_key, self.engine.strata)
            stratum = self.engine.strata[s_key]
            self.assertIsInstance(stratum, PhilologicalStratum)
            self.assertTrue(len(stratum.primary_texts) > 0)
            self.assertTrue(len(stratum.sanskrit_key_terms) > 0)
            self.assertTrue(len(stratum.scholarly_consensus) > 20)
            self.assertTrue(len(stratum.concordist_distortion) > 20)

    def test_darsana_positions_orthodoxy_and_heterodoxy(self):
        """Verify that Astika, Nastika, and Tantric schools are rigorously represented."""
        positions = self.engine.darsana_positions
        self.assertEqual(len(positions), 9)

        # Test Purva Mimamsa's strict rejection
        mimamsa = positions["purva_mimamsa"]
        self.assertEqual(mimamsa.multiverse_verdict, "STRICT REJECTION")
        self.assertIn("Na kadācid anīdṛśaṁ jagat", mimamsa.ontological_mechanism)
        self.assertIn("Kumārila Bhaṭṭa", mimamsa.foundational_authors)

        # Test Carvaka's radical materialist rejection
        carvaka = positions["carvaka_lokayata"]
        self.assertEqual(carvaka.multiverse_verdict, "ABSOLUTE REJECTION")
        self.assertIn("Pratyakṣa", carvaka.ontological_mechanism)

        # Test Jainism's rejection of parallel universes (single Lokapurusha)
        jainism = positions["jainism"]
        self.assertEqual(jainism.multiverse_verdict, "REJECTED (Single Eternal Cosmic Person: Lokapuruṣa)")
        self.assertIn("343", jainism.ontological_mechanism)

        # Test Advaita's dual-level verdict
        advaita = positions["kevaladvaita_vedanta"]
        self.assertIn("EMPIRICALLY AFFIRMED / TRANSCENDENTALLY NEGATED", advaita.multiverse_verdict)
        self.assertIn("Śaṅkara", advaita.foundational_authors)

        # Test Visistadvaita and Dvaita real affirmation
        visistadvaita = positions["visistadvaita_vedanta"]
        self.assertEqual(visistadvaita.multiverse_verdict, "REAL ONTOLOGICAL AFFIRMATION")
        dvaita = positions["dvaita_vedanta"]
        self.assertEqual(dvaita.multiverse_verdict, "REAL ONTOLOGICAL AFFIRMATION (Absolute Fivefold Difference)")

    def test_typologies_five_models(self):
        """Verify the 5 distinct typological models of the Hindu multiverse."""
        typologies = self.engine.typologies
        self.assertEqual(len(typologies), 5)
        
        expected_keys = [
            "type_1_temporal_ensemble",
            "type_2_spatial_bubble",
            "type_3_phenomenological",
            "type_4_tattvic_hierarchical",
            "type_5_fractal_infinitesimal",
        ]
        for key in expected_keys:
            self.assertIn(key, typologies)
            model = typologies[key]
            self.assertIsInstance(model, MultiverseTypologyModel)
            self.assertTrue(
                any(model.physical_analog_status.startswith(prefix) for prefix in ["NON_EQUIVALENT", "PARTIAL_ANALOGY", "METAPHORICAL"]),
                f"Unexpected status: {model.physical_analog_status}"
            )

    def test_concordist_critiques_registry(self):
        """Verify the registry of modern concordist critiques and their falsification."""
        critiques = self.engine.concordist_critiques
        self.assertEqual(len(critiques), 5)

        for c_id, crit in critiques.items():
            self.assertIsInstance(crit, ConcordistCritique)
            self.assertTrue(crit.verdict.startswith("REJECTED"))
            self.assertTrue(len(crit.scientific_demarcation_failure) > 30)
            self.assertTrue(len(crit.scholarly_historical_reality) > 30)

    def test_puranic_egg_geometry_computations(self):
        """Verify mathematical modeling of the 7-sheathed Puranic cosmic egg."""
        geom = self.engine.compute_puranic_egg_geometry(inner_radius_yojanas=2.5e8)
        
        # Inner radius = 2.50e8 yojanas (50 crore yojana diameter / 2)
        self.assertEqual(geom["inner_radius_yojanas"], 2.5e8)
        
        # Sheath progression:
        # r0 = 2.5e8
        # Sheath 1 (Water): 2.5e9
        # Sheath 2 (Fire): 2.5e10
        # Sheath 3 (Air): 2.5e11
        # Sheath 4 (Ether): 2.5e12
        # Sheath 5 (Ahankara): 2.5e13
        # Sheath 6 (Mahat): 2.5e14
        # Sheath 7 (Pradhana): 2.5e15
        # Cumulative = 2.5e8 * (1 + 10 + 100 + ... + 10^7) = 2.5e8 * 11,111,111 = 2.77777775e15
        # Note: If each sheath is 10x preceding cumulative thickness or 10^i of inner radius:
        self.assertTrue(geom["outer_envelope_radius_yojanas"] > 2.5e15)
        self.assertTrue(geom["outer_envelope_radius_ly"] > 3000.0)  # Galactic scale (~3,000 to ~15,000 ly)
        self.assertTrue(geom["inner_radius_au"] > 20.0)  # Solar system scale (> 20 AU)

    def test_siddhantic_kha_kaksha_computations(self):
        """Verify Siddhāntic Kha-kakṣā radius and galactic scale convergence."""
        kha = self.engine.compute_siddhantic_kha_kaksha()
        
        circumference = 18712080864000000.0
        expected_radius_yojanas = circumference / (2.0 * math.pi)
        
        self.assertAlmostEqual(kha["circumference_yojanas"], circumference, places=1)
        self.assertAlmostEqual(kha["radius_yojanas"], expected_radius_yojanas, places=1)
        self.assertTrue(3500.0 < kha["radius_ly"] < 4500.0)  # ~4,051 light years

    def test_demiurge_scaling_power_law(self):
        """Verify Brahmā head count scaling laws."""
        # 4 heads baseline
        scale_4 = self.engine.compute_demiurge_scaling(head_count=4)
        self.assertEqual(scale_4["linear_scale_factor"], 1.0)
        self.assertEqual(scale_4["volume_scale_factor"], 1.0)
        
        # 16 heads
        scale_16 = self.engine.compute_demiurge_scaling(head_count=16)
        self.assertEqual(scale_16["linear_scale_factor"], 4.0)
        self.assertEqual(scale_16["volume_scale_factor"], 64.0)
        
        # 100 heads
        scale_100 = self.engine.compute_demiurge_scaling(head_count=100)
        self.assertEqual(scale_100["linear_scale_factor"], 25.0)
        self.assertEqual(scale_100["volume_scale_factor"], 15625.0)

        # Invalid head count (< 4)
        with self.assertRaises(ValueError):
            self.engine.compute_demiurge_scaling(head_count=3)

    def test_hierarchical_time_dilation_tiers(self):
        """Verify hierarchical time dilation factors across the 5 cosmic tiers."""
        dilation = self.engine.compute_hierarchical_time_dilation()
        
        self.assertEqual(dilation["tier_1_earth"], 1.0)
        self.assertEqual(dilation["tier_2_deva"], 360.0)
        self.assertTrue(dilation["tier_3_brahma"] > 1.0e12)
        self.assertTrue(dilation["tier_4_mahavishnu"] > 1.0e21)
        self.assertEqual(dilation["tier_5_brahman"], float("inf"))


if __name__ == "__main__":
    unittest.main()
