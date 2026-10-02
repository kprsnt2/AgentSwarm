"""
test_hindu_multiverse_tripartite_engine.py

Unit test suite for hindu_multiverse_tripartite_engine.py.
Verifies all mathematical models, astronomical conversions,
philological database integrity, and epistemic demarcation rules.

Author: Kepler (A001)
"""

import unittest
import math
from hindu_multiverse_tripartite_engine import (
    HinduMultiverseTripartiteEngine,
    ArchitectureType,
    EpistemicCategory,
    KM_PER_YOJANA,
    KM_PER_AU,
    KM_PER_LIGHT_YEAR,
    MAHAKALPA_YEARS,
    KALPA_YEARS,
    CORE_BRAHMANDA_RADIUS_YOJANAS,
    CORE_BRAHMANDA_DIAMETER_YOJANAS
)

class TestHinduMultiverseTripartiteEngine(unittest.TestCase):

    def setUp(self):
        self.engine = HinduMultiverseTripartiteEngine()

    def test_core_planetary_scale(self):
        """Verify baseline inner inhabited Brahmāṇḍa matches 43.03 AU diameter."""
        self.assertAlmostEqual(self.engine.core_radius_km, 2.5e8 * KM_PER_YOJANA, places=2)
        diameter_au = self.engine.core_diameter_km / KM_PER_AU
        self.assertAlmostEqual(diameter_au, 43.03, delta=0.05)
        # Verify planetary solar system scale (between Uranus/Neptune and Kuiper Belt)
        self.assertGreater(diameter_au, 30.0)
        self.assertLess(diameter_au, 55.0)

    def test_concentric_sheath_dimensions_and_outer_envelope(self):
        """Verify the 7 exponential sheaths reach ~7,560 ly radius and 15,120 ly diameter."""
        sheaths = self.engine.calculate_concentric_sheaths()
        self.assertEqual(len(sheaths), 7)

        # Monotonicity test
        for i in range(len(sheaths) - 1):
            self.assertLess(sheaths[i].cumulative_radius_km, sheaths[i + 1].cumulative_radius_km)
            self.assertLess(sheaths[i].attenuation_impedance, sheaths[i + 1].attenuation_impedance)
            self.assertLess(sheaths[i].shell_volume_km3, sheaths[i + 1].shell_volume_km3)

        # Final outer boundary: Layer 7 (Mahat-tattva)
        outermost = sheaths[-1]
        self.assertEqual(outermost.layer_index, 7)
        self.assertEqual(outermost.element_sanskrit, "Mahat-tattva")
        self.assertAlmostEqual(outermost.cumulative_radius_ly, 7560.37, delta=1.0)
        self.assertAlmostEqual(outermost.cumulative_radius_ly * 2.0, 15120.74, delta=2.0)

    def test_causal_ocean_kinetics_and_packing(self):
        """Verify bubble nucleation rate and meta-ocean volume calculations."""
        kinetics = self.engine.calculate_causal_ocean_kinetics(
            total_universes=1.0e14,
            exhalation_years=MAHAKALPA_YEARS
        )
        self.assertAlmostEqual(kinetics.total_universes, 1.0e14)
        self.assertAlmostEqual(kinetics.exhalation_duration_years, 3.1104e14)
        
        # Nucleation rate: 1e14 / 3.1104e14 ≈ 0.3215 universes/year
        expected_rate_per_year = 1.0e14 / 3.1104e14
        self.assertAlmostEqual(kinetics.nucleation_rate_per_year, expected_rate_per_year, places=4)
        self.assertGreater(kinetics.nucleation_rate_per_second, 0.0)

        # Meta ocean volume: must account for packing fraction (< 1.0)
        expected_vol = (1.0e14 * kinetics.single_universe_volume_ly3) / kinetics.kepler_packing_fraction
        self.assertAlmostEqual(kinetics.required_meta_ocean_volume_ly3, expected_vol, delta=1.0e20)
        self.assertGreater(kinetics.equivalent_meta_ocean_radius_ly, 3.0e8)

    def test_cospatial_fractal_hierarchy(self):
        """Verify Yoga Vāsiṣṭha recursive nesting within atomic consciousness."""
        levels = 4
        fractal = self.engine.calculate_cospatial_fractal_hierarchy(levels=levels)
        self.assertEqual(len(fractal), levels + 1)
        self.assertEqual(fractal[0]["level"], 0)
        self.assertEqual(fractal[0]["scale_compression_ratio"], 1.0)

        # Scale compression should grow exponentially with levels
        for lvl in range(1, len(fractal)):
            self.assertGreater(fractal[lvl]["scale_compression_ratio"], fractal[lvl - 1]["scale_compression_ratio"])
            self.assertEqual(fractal[lvl]["ontological_status"], "Phenomenological / Cittākāśa")

    def test_kalpa_bheda_entropy(self):
        """Verify Kalpa-Bheda informational entropy and non-identical recurrence."""
        res = self.engine.model_kalpa_bheda_entropy(
            num_individual_jivas=1.0e10,
            karmic_degrees_of_freedom=64,
            historical_divergence_rate=0.08
        )
        self.assertGreater(res["information_entropy_bits"], 0.0)
        self.assertAlmostEqual(res["invariant_dharma_fraction"] + res["variant_historical_contingent_fraction"], 1.0)
        # Shannon entropy for 1e10 jivas * log2(64) = 6e10 bits
        self.assertAlmostEqual(res["information_entropy_bits"], 6.0e10, delta=1.0e8)

    def test_philological_timeline_integrity(self):
        """Verify all critical philological landmarks are present and accurate."""
        records = self.engine.get_philological_timeline()
        self.assertGreaterEqual(len(records), 7)

        # Ensure representation of all major cosmological architectures
        arch_types = {rec.cosmological_type for rec in records}
        self.assertIn(ArchitectureType.CYCLIC_TEMPORAL, arch_types)
        self.assertIn(ArchitectureType.BUBBLE_ARCHIPELAGO, arch_types)
        self.assertIn(ArchitectureType.COSPATIAL_FRACTAL, arch_types)

        # Verify key texts are present
        sources = " ".join([rec.source_corpus for rec in records])
        self.assertIn("Ṛgveda", sources)
        self.assertIn("Chāndogya", sources)
        self.assertIn("Bhāgavata Purāṇa 6.16.37", sources)
        self.assertIn("Bhāgavata Purāṇa 10.14.11", sources)
        self.assertIn("Yoga Vāsiṣṭha", sources)
        self.assertIn("Brahma-Saṁhitā", sources)
        self.assertIn("Matsya Purāṇa", sources)

    def test_epistemic_audit_compliance(self):
        """Verify compliance with protocol safeguards 1 and 2."""
        audit = self.engine.audit_epistemic_claims()
        self.assertGreaterEqual(len(audit), 5)
        for item in audit:
            self.assertTrue(item["protocol_compliance"].startswith("PASS"))
            self.assertIn(item["category"], [c.value for c in EpistemicCategory])

if __name__ == "__main__":
    unittest.main()
