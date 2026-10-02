"""
test_hindu_multiverse_karmic_information_engine.py

Unit test suite for the Karmic Information Conservation, Trans-Universal Insulation,
and Vedantic Multiverse Ontologies Engine.
Author: Kepler (A001) - Generation 0 Research Agent
"""

import unittest
from hindu_multiverse_karmic_information_engine import (
    KarmicInformationEngine,
    STANDARD_BRAHMANDA_DIAMETER_YOJANAS,
    SHEATH_MULTIPLIERS,
)


class TestKarmicInformationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = KarmicInformationEngine()

    def test_karmic_information_entropy_computation(self):
        res = self.engine.compute_karmic_information_entropy(
            n_jivas=1.0e14, samskaras_per_jiva=10000, states_per_samskara=256
        )
        self.assertEqual(res["n_jivas"], 1.0e14)
        self.assertEqual(res["bits_per_jiva"], 80000)
        self.assertEqual(res["total_karmic_entropy_bits"], 8.0e18)
        self.assertEqual(res["total_karmic_entropy_bytes"], 1.0e18)
        self.assertEqual(res["total_karmic_entropy_petabytes"], 1000.0)
        self.assertAlmostEqual(res["information_preservation_ratio_mahapralaya"], 1.0)
        self.assertAlmostEqual(res["information_loss_ratio"], 0.0)
        self.assertIn("Brahma Sūtras 2.1.34-36", res["primary_sutra_basis"])

    def test_brahmanda_insulation_and_crossing(self):
        res = self.engine.evaluate_brahmanda_insulation_and_crossing(base_model="diameter_base")
        self.assertEqual(res["envelope_sheath_count"], 7)
        self.assertEqual(res["envelope_cumulative_factor"], 11111110)
        self.assertAlmostEqual(res["material_tattva_penetration_probability"], 0.0)
        self.assertTrue(res["transcendental_consciousness_crossing"])
        self.assertGreater(res["total_envelope_diameter_ly"], 15000.0)
        self.assertLess(res["total_envelope_diameter_ly"], 16000.0)
        self.assertIn("10.89", res["crossing_narrative_primary_citation"])

        # Test radius_base model
        res_r = self.engine.evaluate_brahmanda_insulation_and_crossing(base_model="radius_base")
        self.assertGreater(res_r["total_envelope_diameter_ly"], 7500.0)
        self.assertLess(res_r["total_envelope_diameter_ly"], 7600.0)

    def test_vedantic_multiverse_ontologies(self):
        res = self.engine.model_vedantic_multiverse_ontologies()
        self.assertEqual(res["total_schools_evaluated"], 4)
        schools = res["schools"]
        
        # Check Eka-Jiva-Vada
        self.assertEqual(schools["Eka_Jiva_Vada"]["jiva_count"], 1)
        self.assertFalse(schools["Eka_Jiva_Vada"]["objective_reality"])
        self.assertIn("Prātibhāsika", schools["Eka_Jiva_Vada"]["brahmanda_status"])
        
        # Check Advaita Nana-Jiva-Vada
        self.assertTrue(schools["Advaita_Nana_Jiva_Vada"]["objective_reality"])
        self.assertIn("Vyāvahārika", schools["Advaita_Nana_Jiva_Vada"]["brahmanda_status"])
        
        # Check Visistadvaita
        self.assertTrue(schools["Visistadvaita"]["objective_reality"])
        self.assertIn("Pāramārthika", schools["Visistadvaita"]["brahmanda_status"])
        
        # Check Dvaita
        self.assertTrue(schools["Dvaita"]["objective_reality"])
        self.assertIn("Pāramārthika", schools["Dvaita"]["brahmanda_status"])

    def test_kalpa_bheda_hermeneutics_and_demarcation(self):
        res = self.engine.evaluate_kalpa_bheda_hermeneutics()
        self.assertEqual(res["reconciliation_efficiency"], 1.0)
        self.assertEqual(len(res["demarcation_points"]), 4)
        for point in res["demarcation_points"]:
            self.assertFalse(point["is_concordant"])
        self.assertIn("category error", res["hermeneutic_verdict"].lower())

    def test_tripartite_demarcation_catalog(self):
        res = self.engine.verify_tripartite_demarcation_catalog()
        self.assertEqual(res["primary_count"], 2)
        self.assertEqual(res["scholarly_count"], 2)
        self.assertEqual(res["devotional_count"], 2)
        self.assertEqual(res["total_items"], 6)


if __name__ == "__main__":
    unittest.main()
