"""
test_hindu_multiverse_epistemology_and_eka_jiva_engine.py

Unit testing and epistemic validation suite for:
- HinduMultiverseEpistemologyEngine
- Advaita Vedānta Eka-Jīva vs. Nānā-Jīva ontology
- Classical Darśana Pramāṇa matrix and Yogipratyakṣa scope
- Kumārila Bhaṭṭa's anti-multiverse skepticism
- Jīva Gosvāmin's Doṣa-Catuṣṭaya attenuation
- Patañjali Saṁyama spatial reaches
"""

import unittest
import math
from hindu_multiverse_epistemology_and_eka_jiva_engine import (
    HinduMultiverseEpistemologyEngine,
    DarsanaEpistemicProfile,
    AdvaitaModelProfile
)


class TestHinduMultiverseEpistemologyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = HinduMultiverseEpistemologyEngine()

    def test_darsana_tensor_initialization(self):
        """Ensure all primary darśanic profiles are registered and populated."""
        darsanas = self.engine.darsanas
        expected_keys = [
            "Carvaka", "Purva_Mimamsa", "Nyaya_Vaisesika",
            "Sankhya_Yoga", "Advaita_Vedanta_Eka_Jiva",
            "Advaita_Vedanta_Nana_Jiva", "Gaudya_Vaisnava_Vedanta"
        ]
        for key in expected_keys:
            self.assertIn(key, darsanas)
            p = darsanas[key]
            self.assertIsInstance(p, DarsanaEpistemicProfile)
            self.assertTrue(len(p.accepted_pramanas) >= 1)
            self.assertTrue(-1.0 <= p.multiverse_assertion_score <= 1.0)

    def test_kumarila_bhatta_skepticism(self):
        """Verify Kumārila's strict anti-multiverse and anti-yogipratyaksa logic."""
        mimamsa = self.engine.darsanas["Purva_Mimamsa"]
        self.assertEqual(mimamsa.multiverse_assertion_score, -1.0)
        self.assertFalse(mimamsa.yogipratyaksa_accepted)
        self.assertEqual(mimamsa.ontological_status_of_multiverse, "Arthavāda (Mythic Eulogy, not Fact)")

        skepticism_eval = self.engine.evaluate_kumarila_skepticism()
        self.assertEqual(skepticism_eval["philosopher"], "Kumārila Bhaṭṭa")
        self.assertIn("Indriya-svabhāva-niyama", skepticism_eval["core_argument"])
        self.assertIn("pratijna", skepticism_eval["syllogism"])

    def test_carvaka_rejection(self):
        """Verify Cārvāka's single-pramāṇa rejection of the multiverse."""
        carvaka = self.engine.darsanas["Carvaka"]
        self.assertEqual(carvaka.accepted_pramanas, ["Pratyakṣa"])
        self.assertEqual(carvaka.multiverse_assertion_score, -1.0)
        self.assertEqual(carvaka.ontological_status_of_multiverse, "Fictitious / Non-Existent")

    def test_advaita_eka_jiva_vs_nana_jiva_differentiation(self):
        """Verify the profound ontological divergence between Eka-Jīva and Nānā-Jīva."""
        comp = self.engine.compare_eka_jiva_vs_nana_jiva()
        ejv = comp["Eka_Jiva_Vada"]
        njv = comp["Nana_Jiva_Vada"]

        self.assertEqual(ejv["observer_count"], 1)
        self.assertIn("Prātibhāsika", ejv["ontological_tier"])
        self.assertEqual(njv["observer_count"], math.inf)
        self.assertIn("Vyāvahārika", njv["ontological_tier"])

    def test_dosa_catustaya_attenuation_defaults(self):
        """Verify Jīva Gosvāmin's four defects calculation."""
        res = self.engine.calculate_dosa_catustaya_attenuation()
        # default defects: 0.25, 0.20, 0.15, 0.35
        # product of (1 - d) = 0.75 * 0.80 * 0.85 * 0.65 = 0.3315
        expected_certainty = 0.75 * 0.80 * 0.85 * 0.65
        self.assertAlmostEqual(res["net_empirical_fidelity"], expected_certainty, places=4)
        self.assertAlmostEqual(res["epistemic_attenuation"], 1.0 - expected_certainty, places=4)
        self.assertTrue(res["transcendental_necessity_score"] > 1.0)

    def test_dosa_catustaya_custom_bounds(self):
        """Test defect attenuation with extreme bounds."""
        # Zero defect case (ideal perception)
        ideal = {"bhrama": 0.0, "pramada": 0.0, "vipralipsa": 0.0, "karanapatava": 0.0}
        res_ideal = self.engine.calculate_dosa_catustaya_attenuation(ideal)
        self.assertEqual(res_ideal["net_empirical_fidelity"], 1.0)
        self.assertEqual(res_ideal["epistemic_attenuation"], 0.0)

        # Total corruption
        total_fail = {"bhrama": 1.0, "pramada": 0.0, "vipralipsa": 0.0, "karanapatava": 0.0}
        res_fail = self.engine.calculate_dosa_catustaya_attenuation(total_fail)
        self.assertEqual(res_fail["net_empirical_fidelity"], 0.0)
        self.assertEqual(res_fail["epistemic_attenuation"], 1.0)

        # Invalid bounds
        invalid = {"bhrama": 1.5}
        with self.assertRaises(ValueError):
            self.engine.calculate_dosa_catustaya_attenuation(invalid)

    def test_samyama_cosmic_reach_surya(self):
        """Verify Patanjali YS 3.26 solar samyama parameters."""
        surya = self.engine.compute_yogic_samyama_cosmic_reach("Surya")
        self.assertEqual(surya["max_radius_yojanas"], 250000000)
        self.assertFalse(surya["trans_cosmic_penetration"])
        # Radius in AU should be ~21.5 AU
        self.assertAlmostEqual(surya["max_radius_au"], 21.51, places=1)

    def test_samyama_cosmic_reach_taraka(self):
        """Verify Patanjali YS 3.54 Taraka-jnana infinite scope."""
        taraka = self.engine.compute_yogic_samyama_cosmic_reach("Taraka")
        self.assertEqual(taraka["max_radius_yojanas"], math.inf)
        self.assertTrue(taraka["trans_cosmic_penetration"])
        self.assertEqual(taraka["max_radius_au"], math.inf)

    def test_samyama_invalid_target(self):
        """Ensure invalid focus points raise KeyError."""
        with self.assertRaises(KeyError):
            self.engine.compute_yogic_samyama_cosmic_reach("Mars")

    def test_tensor_summary_generation(self):
        """Verify tensor summary data structure."""
        summary = self.engine.generate_darsana_tensor_summary()
        self.assertEqual(len(summary), len(self.engine.darsanas))
        for row in summary:
            self.assertIn("school", row)
            self.assertIn("multiverse_score", row)
            self.assertIn("status", row)


if __name__ == "__main__":
    unittest.main()
