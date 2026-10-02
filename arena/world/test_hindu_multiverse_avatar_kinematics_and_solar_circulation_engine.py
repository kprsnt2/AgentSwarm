"""
test_hindu_multiverse_avatar_kinematics_and_solar_circulation_engine.py

Unit test suite for the Multi-Cosmic Avatara Kinematics and Solar Circulation Engine.
Tests:
1. Engine instantiation and default constants.
2. Solar circulation kinematics calculations and temporal scaling.
3. Demiurge morphology and head-scaling laws (CC Madhya 21).
4. Multi-cosmic administrative officer census across parallel universes.
5. Epistemic demarcation and Indological firewall scoring.
6. End-to-end comprehensive audit function execution.
"""

import unittest
from hindu_multiverse_avatar_kinematics_and_solar_circulation_engine import (
    AvatarKinematicsEngine,
    run_comprehensive_avatar_kinematics_audit
)


class TestAvatarKinematicsEngine(unittest.TestCase):

    def setUp(self):
        self.engine = AvatarKinematicsEngine()

    def test_initialization_and_constants(self):
        self.assertEqual(self.engine.TERRESTRIAL_LILA_DURATION_YEARS, 125.0)
        self.assertEqual(self.engine.multiverse_population, 1.0e14)
        self.assertAlmostEqual(self.engine.SECONDS_PER_SOLAR_YEAR, 31557600.0, places=1)
        self.assertEqual(self.engine.STANDARD_UNIVERSE_DIAMETER_YOJANAS, 5.0e8)

    def test_solar_circulation_kinematics(self):
        kinematics = self.engine.calculate_solar_circulation_kinematics()
        self.assertEqual(kinematics["multiverse_population"], 1.0e14)
        self.assertEqual(kinematics["terrestrial_lila_years"], 125.0)

        # Total seconds: 125 * 31,557,600 = 3,944,700,000 seconds
        expected_seconds = 125.0 * 31557600.0
        self.assertAlmostEqual(kinematics["total_lila_seconds"], expected_seconds, places=1)

        # Phase interval in seconds: 3,944,700,000 / 1e14 = 3.9447e-5 seconds
        self.assertAlmostEqual(kinematics["phase_interval_seconds"], 3.9447e-5, places=8)

        # Phase interval in microseconds: ~39.447 microseconds
        self.assertAlmostEqual(kinematics["phase_interval_microseconds"], 39.447, places=2)

        # Events per second: 1 / 3.9447e-5 ~ 25350.47 events/sec
        self.assertAlmostEqual(kinematics["events_per_second"], 1.0e14 / expected_seconds, places=2)

    def test_solar_circulation_custom_population(self):
        custom_n = 1000.0
        kinematics = self.engine.calculate_solar_circulation_kinematics(n_universes=custom_n)
        self.assertEqual(kinematics["multiverse_population"], 1000.0)
        # Phase interval in years: 125 / 1000 = 0.125 years
        self.assertAlmostEqual(kinematics["phase_interval_years"], 0.125, places=5)

    def test_demiurge_scaling_baseline_4_heads(self):
        res = self.engine.calculate_demiurge_scaling(4)
        self.assertEqual(res["heads"], 4)
        self.assertEqual(res["head_factor"], 1.0)
        self.assertEqual(res["diameter_yojanas"], 5.0e8)
        self.assertEqual(res["volume_relative_ratio"], 1.0)

    def test_demiurge_scaling_higher_heads(self):
        # 16-headed Brahma
        res_16 = self.engine.calculate_demiurge_scaling(16)
        self.assertEqual(res_16["heads"], 16)
        self.assertEqual(res_16["head_factor"], 4.0)
        self.assertEqual(res_16["diameter_yojanas"], 2.0e9)
        # Volume scales cubically: 4^3 = 64
        self.assertAlmostEqual(res_16["volume_relative_ratio"], 64.0, places=4)

        # 1,000,000-headed Brahma
        res_million = self.engine.calculate_demiurge_scaling(1000000)
        self.assertEqual(res_million["head_factor"], 250000.0)
        self.assertAlmostEqual(res_million["volume_relative_ratio"], 250000.0 ** 3, delta=1.0e6)

    def test_demiurge_scaling_invalid_heads(self):
        with self.assertRaises(ValueError):
            self.engine.calculate_demiurge_scaling(2)

    def test_demiurge_hierarchy_table(self):
        table = self.engine.generate_demiurge_hierarchy_table()
        self.assertEqual(len(table), 11)
        expected_heads = [4, 8, 16, 32, 64, 100, 500, 1000, 10000, 100000, 1000000]
        actual_heads = [row["heads"] for row in table]
        self.assertEqual(actual_heads, expected_heads)

    def test_administrative_census(self):
        census = self.engine.calculate_multiverse_administrative_census(n_universes=1.0e14)
        self.assertEqual(census["multiverse_population"], 1.0e14)
        self.assertEqual(census["total_local_brahmas"], 1.0e14)
        self.assertEqual(census["total_local_sivas"], 1.0e14)
        self.assertEqual(census["total_local_visnus"], 1.0e14)
        self.assertEqual(census["total_concurrent_trimurti_officers"], 3.0e14)
        self.assertEqual(census["total_indras_per_kalpa"], 1.4e15)
        self.assertEqual(census["total_indras_per_brahma_lifespan"], 5.04e19)
        self.assertEqual(census["supreme_origin_count"], 1)

    def test_epistemic_demarcation(self):
        audit = self.engine.evaluate_epistemic_demarcation()
        self.assertIn("concordist_demarcation_index", audit)
        self.assertIn("indological_fidelity_score", audit)
        # Concordist score must be minimal (< 0.05)
        self.assertLess(audit["concordist_demarcation_index"], 0.05)
        # Indological fidelity must be substantial (>= 0.30)
        self.assertGreaterEqual(audit["indological_fidelity_score"], 0.30)

    def test_end_to_end_audit(self):
        audit = run_comprehensive_avatar_kinematics_audit()
        self.assertIn("solar_kinematics", audit)
        self.assertIn("demiurge_hierarchy", audit)
        self.assertIn("admin_census", audit)
        self.assertIn("epistemic_audit", audit)


if __name__ == "__main__":
    unittest.main()
