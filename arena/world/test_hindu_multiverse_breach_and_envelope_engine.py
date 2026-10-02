"""
Unit test suite for hindu_multiverse_breach_and_envelope_engine.py.
Verifies all mathematical scalings, envelope thicknesses, trans-cosmic voyaging kinematics,
Tantric four eggs, and epistemic demarcation audits using standard unittest.
"""

import unittest
import math
from hindu_multiverse_breach_and_envelope_engine import (
    CosmicEnvelopeEngine,
    TrivikramaBreachEngine,
    ArjunaTransCosmicVoyageEngine,
    TantricEggCosmographyEngine,
    EpistemicDemarcationFramework,
)


class TestCosmicEnvelopeEngine(unittest.TestCase):
    def test_core_initialization(self):
        env = CosmicEnvelopeEngine(yojana_km=12.8748, core_diameter_yojanas=5.0e8)
        self.assertEqual(env.core_diameter_yojanas, 5.0e8)
        self.assertEqual(env.core_radius_yojanas, 2.5e8)
        # Check core radius in light years (~0.00034 ly, ~2.98 light hours)
        self.assertTrue(0.00033 < env.core_radius_ly < 0.00035)
        expected_vol = (4.0 / 3.0) * math.pi * (2.5e8 ** 3)
        self.assertTrue(math.isclose(env.core_volume_yojanas3, expected_vol, rel_tol=1e-5))

    def test_geometric_sheaths(self):
        env = CosmicEnvelopeEngine()
        sheaths = env.compute_geometric_sheaths()
        self.assertEqual(len(sheaths), 8)

        # First sheath (Earth): 5e9 yojanas
        self.assertEqual(sheaths[0]["name"], "Pṛthvī")
        self.assertEqual(sheaths[0]["thickness_yojanas"], 5.0e9)

        # Last sheath (Pradhāna): 5e16 yojanas
        self.assertEqual(sheaths[7]["name"], "Pradhāna / Prakṛti")
        self.assertEqual(sheaths[7]["thickness_yojanas"], 5.0e16)

        # Cumulative thickness: 5.5555555e16 yojanas
        total_thickness = sheaths[-1]["cumulative_thickness_yojanas"]
        self.assertTrue(5.5555e16 < total_thickness < 5.5556e16)

        # Check outer radius in light years (~75,604 ly)
        outer_r_ly = sheaths[-1]["outer_radius_ly"]
        self.assertTrue(75000 < outer_r_ly < 76500)

    def test_linear_sheaths(self):
        env = CosmicEnvelopeEngine()
        sheaths = env.compute_linear_sheaths()
        self.assertEqual(len(sheaths), 8)
        for s in sheaths:
            self.assertEqual(s["thickness_yojanas"], 5.0e9)

        # Total linear thickness: 8 * 5e9 = 4e10 yojanas
        total_thickness = sheaths[-1]["cumulative_thickness_yojanas"]
        self.assertEqual(total_thickness, 4.0e10)
        total_r_ly = sheaths[-1]["outer_radius_ly"]
        self.assertTrue(0.054 < total_r_ly < 0.056)

    def test_envelope_metrics(self):
        env = CosmicEnvelopeEngine()
        metrics = env.get_envelope_metrics()

        geom = metrics["geometric_progression_model"]
        # Diameter ~ 151,208 ly
        self.assertTrue(150000 < geom["outer_diameter_ly"] < 153000)
        # Volume ratio ~ 1.097e25
        self.assertTrue(1.0e25 < geom["envelope_to_core_volume_ratio"] < 1.2e25)
        # Core fraction of envelope ~ 9.11e-26
        self.assertTrue(8.0e-26 < geom["core_fraction_of_envelope"] < 1.0e-25)
        # Ratio to Milky Way diameter (~1.51)
        self.assertTrue(1.4 < geom["ratio_to_milky_way_diameter"] < 1.6)


class TestTrivikramaBreachEngine(unittest.TestCase):
    def test_puncture_and_conduit(self):
        engine = TrivikramaBreachEngine()
        res = engine.compute_puncture_and_conduit(nail_width_ratio=1.0e-5)
        
        self.assertEqual(res["aperture_diameter_yojanas"], 5000.0)
        self.assertEqual(res["aperture_radius_yojanas"], 2500.0)
        self.assertTrue(res["conduit_length_ly"] > 75000)
        self.assertEqual(len(res["descent_stages"]), 6)
        self.assertEqual(res["descent_stages"][0]["station"], "Brahmāṇḍa-Kaṭāha Aperture")
        self.assertEqual(res["descent_stages"][5]["station"], "Bhārata-varṣa (Earth)")
        self.assertIn("Brahmāṇḍa-bahir-varti-dravya", res["theological_designation"])


class TestArjunaTransCosmicVoyageEngine(unittest.TestCase):
    def test_waypoints(self):
        engine = ArjunaTransCosmicVoyageEngine()
        self.assertEqual(len(engine.WAYPOINTS), 7)
        self.assertEqual(engine.WAYPOINTS[0]["name"], "Dvārakā Departure")
        self.assertEqual(engine.WAYPOINTS[2]["name"], "Lokāloka Mountain Ridge")
        self.assertEqual(engine.WAYPOINTS[3]["name"], "Tamoloka (Abyss of Primordial Darkness)")
        self.assertEqual(engine.WAYPOINTS[4]["name"], "Sudarśana Cakra Tunneling Activation")
        self.assertEqual(engine.WAYPOINTS[6]["name"], "Kāraṇārṇava Arrival & Mahā-Kāla Vision")

    def test_apparent_kinematics(self):
        engine = ArjunaTransCosmicVoyageEngine(trip_duration_earth_days=1.0)
        res = engine.compute_apparent_kinematics()
        
        # Distance ~ 151,208 ly round trip in 1 day
        self.assertEqual(res["trip_duration_earth_days"], 1.0)
        self.assertTrue(150000 < res["round_trip_distance_ly"] < 153000)
        # Apparent velocity beta > 50 million c
        self.assertTrue(5.0e7 < res["apparent_velocity_over_c"] < 6.0e7)
        self.assertEqual(len(res["physical_impossibilities"]), 4)
        self.assertTrue("visionary" in res["indological_resolution"] or "darśana" in res["indological_resolution"])


class TestTantricEggCosmographyEngine(unittest.TestCase):
    def test_four_eggs_structure(self):
        engine = TantricEggCosmographyEngine()
        summary = engine.get_tantric_cosmography_summary()

        self.assertEqual(summary["total_tattvas"], 36)
        self.assertEqual(summary["encompassed_in_four_eggs"], 34)
        self.assertEqual(summary["transcendent_tattvas"], 2)

        eggs = summary["four_eggs"]
        self.assertEqual(len(eggs), 4)
        self.assertEqual(eggs[0]["egg_name"], "Pārthiva Aṇḍa (Egg of Earth)")
        self.assertEqual(eggs[0]["ruling_deity"], "Brahmā")
        self.assertEqual(eggs[0]["tattvas_encompassed"], 1)

        self.assertEqual(eggs[1]["egg_name"], "Prākṛta Aṇḍa (Egg of Nature)")
        self.assertEqual(eggs[1]["ruling_deity"], "Viṣṇu")
        self.assertEqual(eggs[1]["tattvas_encompassed"], 23)

        self.assertEqual(eggs[2]["egg_name"], "Māyīya Aṇḍa (Egg of Māyā)")
        self.assertEqual(eggs[2]["ruling_deity"], "Rudra")
        self.assertEqual(eggs[2]["tattvas_encompassed"], 7)

        self.assertEqual(eggs[3]["egg_name"], "Śākta Aṇḍa (Egg of Śakti)")
        self.assertEqual(eggs[3]["ruling_deity"], "Sadāśiva")
        self.assertEqual(eggs[3]["tattvas_encompassed"], 3)

        self.assertEqual(len(summary["granthis"]), 3)


class TestEpistemicDemarcationFramework(unittest.TestCase):
    def test_audit_records(self):
        records = EpistemicDemarcationFramework.get_audit()
        self.assertEqual(len(records), 4)
        for r in records:
            self.assertIn("topic", r)
            self.assertIn("primary_text", r)
            self.assertIn("scholarly_consensus", r)
            self.assertIn("concordist_claim", r)
            self.assertIn("demarcation_verdict", r)
            verdict = r["demarcation_verdict"]
            self.assertTrue(
                "CATEGORY ERROR" in verdict or
                "FALSE EQUIVALENCE" in verdict or
                "SUPERFICIAL ANALOGY" in verdict
            )


if __name__ == "__main__":
    unittest.main()
