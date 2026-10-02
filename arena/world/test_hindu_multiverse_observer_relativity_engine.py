"""
test_hindu_multiverse_observer_relativity_engine.py

Comprehensive unit test suite for hindu_multiverse_observer_relativity_engine.py.
Verifies:
1. Temporal dilation scaling factors across 6 cosmological planes.
2. Kakudmi-Revati relativistic kinematics, Lorentz gamma, velocity deficit, and CMB blueshift.
3. Consciousness-projected parallel universe parameters (Yoga Vāsiṣṭha / Tripura Rahasya).
4. Pan-Indic Buddhist Abhidharma and Jaina Loka metrics.
5. Epistemic categorization rules and Indological safeguards.

Author: Kepler (A001)
"""

import unittest
import math
from hindu_multiverse_observer_relativity_engine import (
    HinduMultiverseObserverRelativityEngine,
    EpistemicCategory,
    CosmologicalTradition,
    KM_PER_YOJANA,
    KM_PER_AU,
    KM_PER_LIGHT_YEAR,
    T_CMB_KELVIN,
    run_full_analytical_sweep
)

class TestHinduMultiverseObserverRelativityEngine(unittest.TestCase):

    def setUp(self):
        self.engine = HinduMultiverseObserverRelativityEngine()

    def test_temporal_dilation_hierarchy(self):
        """Verify the exact canonical scaling ratios between human, pitri, deva, and brahma time."""
        hierarchy = self.engine.compute_temporal_hierarchy()
        self.assertEqual(len(hierarchy), 6)

        # Check Earth baseline
        self.assertEqual(hierarchy[0].solar_years_equivalent, 1.0)
        self.assertEqual(hierarchy[0].time_dilation_factor_vs_earth, 1.0)

        # Check Pitṛ plane: 1 month = 30 days => factor 30
        self.assertEqual(hierarchy[1].time_dilation_factor_vs_earth, 30.0)

        # Check Deva plane: 1 year = 360 days => factor 360
        self.assertEqual(hierarchy[2].time_dilation_factor_vs_earth, 360.0)

        # Check Kalpa / Brahma single day: 4.32 billion years
        self.assertAlmostEqual(hierarchy[3].time_dilation_factor_vs_earth, 4.32e9)

        # Check Brahma full day-night: 8.64 billion years
        self.assertAlmostEqual(hierarchy[4].time_dilation_factor_vs_earth, 8.64e9)

        # Check Brahma full 100-year lifespan: 311.04 trillion years
        self.assertAlmostEqual(hierarchy[5].time_dilation_factor_vs_earth, 3.1104e14)

    def test_kakudmi_relativity_kinematics(self):
        """Verify the relativistic calculation for the Kakudmi-Revati episode."""
        result = self.engine.compute_kakudmi_relativity(earth_catur_yugas=27.0, wait_time_minutes=48.0)

        # 27 * 4.32e6 = 116,640,000 years
        expected_earth_years = 116_640_000.0
        self.assertAlmostEqual(result.earth_years_elapsed, expected_earth_years)

        # Check gamma factor:
        # 116,640,000 * 365.25 * 24 * 60 / 48 = 1.278e12
        expected_earth_minutes = expected_earth_years * 365.25 * 24.0 * 60.0
        expected_gamma = expected_earth_minutes / 48.0
        self.assertAlmostEqual(result.dilation_factor_gamma, expected_gamma, places=3)
        self.assertGreater(result.dilation_factor_gamma, 1.27e12)
        self.assertLess(result.dilation_factor_gamma, 1.29e12)

        # In IEEE 754 float64, 1 - 3.06e-25 rounds to 1.0 due to machine epsilon (~2.2e-16).
        # We verify that float64 representation is 1.0 while exact deficit is strictly positive:
        self.assertEqual(result.velocity_ratio_beta, 1.0)
        self.assertGreater(result.velocity_deficit_from_c, 0.0)
        self.assertLess(result.velocity_deficit_from_c, 1e-20)

        # Velocity deficit 1 - beta approx 1 / (2 * gamma^2)
        expected_deficit = 1.0 / (2.0 * (expected_gamma ** 2))
        self.assertAlmostEqual(result.velocity_deficit_from_c, expected_deficit, delta=1e-30)

        # Schwarzschild horizon deficit (r - r_s) / r_s = 1 / gamma^2
        expected_horizon_def = 1.0 / (expected_gamma ** 2)
        self.assertAlmostEqual(result.equivalent_schwarzschild_radius_deficit, expected_horizon_def, delta=1e-30)

        # CMB blueshift thermal bath
        self.assertGreater(result.blueshifted_cmb_kelvin, 3.0e12)
        self.assertIn("violates the Indological safeguard", result.epistemic_verdict)

    def test_consciousness_multiverse_cases(self):
        """Verify the 4 canonical cases from Yoga Vāsiṣṭha and Tripura Rahasya."""
        cases = self.engine.compute_consciousness_multiverse_cases()
        self.assertEqual(len(cases), 4)

        # Lilavati case
        lila = cases[0]
        self.assertIn("Līlāvatī", lila.narrative_case)
        self.assertEqual(lila.subjective_duration_years, 70.0)
        self.assertGreater(lila.dilation_ratio, 7.0e6)

        # Dasa Indu-putrah case
        indu = cases[1]
        self.assertIn("Indu-putrāḥ", indu.narrative_case)
        self.assertEqual(indu.subjective_duration_years, 3.1104e14)
        self.assertIn("Ten complete physical multiverses", indu.spatial_coexistence_mode)

        # Gadhi case
        gadhi = cases[2]
        self.assertIn("Gādhi", gadhi.narrative_case)
        self.assertEqual(gadhi.subjective_duration_years, 60.0)
        self.assertEqual(gadhi.objective_duration_seconds, 90.0)
        self.assertAlmostEqual(gadhi.dilation_ratio, (60.0 * 365.25 * 86400.0) / 90.0)

        # Universe inside hill
        hill = cases[3]
        self.assertIn("Śilā-madhya", hill.narrative_case)
        self.assertEqual(hill.subjective_duration_years, 4.32e9)

    def test_buddhist_cosmic_hierarchy(self):
        """Verify the 10^3, 10^6, and 10^9 scaling in Buddhist cosmology."""
        tiers = self.engine.compute_buddhist_cosmic_hierarchy()
        self.assertEqual(len(tiers), 4)

        self.assertEqual(tiers[0].world_count, 1)
        self.assertEqual(tiers[1].world_count, 1_000)
        self.assertEqual(tiers[2].world_count, 1_000_000)
        self.assertEqual(tiers[3].world_count, 1_000_000_000)

        # Radius scaling: 1x, 10x, 100x, 1000x
        base_ly = tiers[0].scale_light_years
        self.assertAlmostEqual(tiers[1].scale_light_years, base_ly * 10.0, places=2)
        self.assertAlmostEqual(tiers[2].scale_light_years, base_ly * 100.0, places=2)
        self.assertAlmostEqual(tiers[3].scale_light_years, base_ly * 1000.0, places=2)

    def test_jaina_cosmic_metrics(self):
        """Verify the canonical 343 Raju^3 and infinite Aloka."""
        metrics = self.engine.compute_jaina_cosmic_metrics()
        self.assertEqual(metrics["loka_height_raju"], 14.0)
        self.assertEqual(metrics["loka_volume_raju3"], 343.0)
        self.assertEqual(metrics["alokakasa_volume_fraction"], float("inf"))
        self.assertEqual(metrics["matter_in_aloka"], 0.0)

    def test_epistemic_database_and_demarcations(self):
        """Verify that primary text, scholarly consensus, and devotional claims are distinguished."""
        records = self.engine.get_epistemic_database()
        self.assertGreaterEqual(len(records), 5)

        categories = {r.epistemic_category for r in records}
        self.assertIn(EpistemicCategory.PRIMARY_TEXT, categories)
        self.assertIn(EpistemicCategory.SCHOLARLY_CONSENSUS, categories)
        self.assertIn(EpistemicCategory.DEVOTIONAL_CLAIM, categories)

        # Check that devotional claims are explicitly labeled and analyzed
        devotional_records = [r for r in records if r.epistemic_category == EpistemicCategory.DEVOTIONAL_CLAIM]
        self.assertGreaterEqual(len(devotional_records), 1)
        for d in devotional_records:
            self.assertIn("Fails because", d.analytical_notes)

    def test_full_analytical_sweep(self):
        """Verify that the end-to-end sweep runs cleanly and returns all expected keys."""
        sweep = run_full_analytical_sweep()
        keys = ["engine", "time_hierarchy", "kakudmi_relativity", "mind_worlds",
                "buddhist_hierarchy", "jain_metrics", "database"]
        for k in keys:
            self.assertIn(k, sweep)


if __name__ == "__main__":
    unittest.main()
