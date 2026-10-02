"""
test_hindu_multiverse_pralaya_and_epistemic_engine.py
=====================================================
Comprehensive Unit and Regression Test Suite for Hindu Multiverse Pralaya,
Cosmological Dissolution, and Epistemic Pramana Engine.
"""

import unittest
import math
from hindu_multiverse_pralaya_and_epistemic_engine import (
    PralayaMechanics,
    ReverseSankhyaEngine,
    MahaVisnuInhalationDynamics,
    EpistemicRevelationEngine,
    EschatologicalConcordismEngine,
    run_master_analysis,
    SOLAR_YEARS_PER_KALPA,
    TOTAL_SOLAR_YEARS_BRAHMA_LIFE,
    CANONICAL_MULTIVERSE_UNIVERSE_COUNT
)


class TestPralayaMechanics(unittest.TestCase):
    """Tests the canonical four orders of universal dissolution (Caturvidha-Pralaya)."""

    def test_four_orders_count_and_types(self):
        orders = PralayaMechanics.get_four_orders()
        self.assertEqual(len(orders), 4)
        self.assertIn("Nitya", orders)
        self.assertIn("Naimittika", orders)
        self.assertIn("Prakrtika", orders)
        self.assertIn("Atyantika", orders)

    def test_primary_source_citations(self):
        orders = PralayaMechanics.get_four_orders()
        for key, order in orders.items():
            self.assertEqual(order.epistemic_classification, "Primary Sanskrit Text")
            self.assertTrue(len(order.primary_source_citation) > 0)
            self.assertTrue("Purana" in order.primary_source_citation or "Sutras" in order.primary_source_citation)

    def test_naimittika_statistics(self):
        stats = PralayaMechanics.calculate_naimittika_statistics()
        self.assertEqual(stats["naimittika_dissolution_count_per_universe"], 36000)
        self.assertEqual(stats["total_day_night_cycles"], 72000)
        self.assertAlmostEqual(stats["kalpa_period_solar_years"], 4.32e9)
        self.assertAlmostEqual(stats["lifespan_brahma_solar_years"], 3.1104e14)
        self.assertEqual(stats["thermal_drying_duration_years"], 100.0)
        self.assertEqual(stats["seven_suns_flux_multiplier"], 7.0)
        self.assertAlmostEqual(stats["submerged_fraction_lokas"], 3.0 / 14.0)
        self.assertAlmostEqual(stats["surviving_higher_lokas"], 4.0 / 14.0)


class TestReverseSankhyaEngine(unittest.TestCase):
    """Tests the reverse-order elemental resorption during Prakrtika Pralaya."""

    def test_resorption_stages_sequence(self):
        stages = ReverseSankhyaEngine.get_resorption_chain()
        self.assertEqual(len(stages), 7)
        expected_dissolving = [
            "Prthvi", "Ap", "Tejas", "Vayu", "Akasa", "Ahankara", "Mahat-Tattva"
        ]
        for idx, stage in enumerate(stages, start=1):
            self.assertEqual(stage.stage_index, idx)
            self.assertTrue(any(exp in stage.dissolving_entity for exp in expected_dissolving))
            self.assertTrue(len(stage.textual_citation) > 0)

    def test_entropy_and_phase_metrics(self):
        entropy = ReverseSankhyaEngine.calculate_entropy_and_phase_metrics()
        self.assertEqual(entropy["total_resorption_stages"], 7)
        # Shannon entropy of uniform 3-guna equilibrium = log2(3) ~ 1.5850 bits
        expected_log2_3 = math.log2(3)
        self.assertAlmostEqual(entropy["samyavastha_equilibrium_entropy_bits"], round(expected_log2_3, 4), places=3)
        self.assertGreater(entropy["entropy_change_to_equilibrium_bits"], 0.0)
        self.assertEqual(entropy["informational_loss_bits"], 0.0)
        self.assertEqual(entropy["information_conservation_fidelity"], 1.0)


class TestMahaVisnuInhalationDynamics(unittest.TestCase):
    """Tests the kinematics of Maha-Visnu inhalation and multiverse turnover."""

    def test_inhalation_and_exhalation_symmetry(self):
        kinematics = MahaVisnuInhalationDynamics.calculate_ensemble_kinematics()
        self.assertEqual(kinematics["exhalation_solar_years"], kinematics["inhalation_solar_years"])
        self.assertEqual(kinematics["exhalation_solar_years"], 3.1104e14)
        self.assertEqual(kinematics["total_multiverse_yield"], 6.30e11)

    def test_resorption_flux_and_time_dilation(self):
        kinematics = MahaVisnuInhalationDynamics.calculate_ensemble_kinematics()
        self.assertGreater(kinematics["resorption_flux_per_year"], 0.0)
        # Dilation factor should be on the order of 10^21
        self.assertGreater(kinematics["divine_breath_time_dilation"], 1.0e21)
        self.assertAlmostEqual(kinematics["steady_state_annual_turnover"], 0.002025, places=5)


class TestEpistemicRevelationEngine(unittest.TestCase):
    """Tests the Pramana-sastra analysis of trans-universal vision episodes."""

    def test_five_canonical_episodes(self):
        episodes = EpistemicRevelationEngine.get_canonical_episodes()
        self.assertEqual(len(episodes), 5)
        titles = [ep.title for ep in episodes]
        self.assertTrue(any("Viśvarūpa" in t for t in titles))
        self.assertTrue(any("Yaśodā" in t for t in titles))
        self.assertTrue(any("Mārkaṇḍeya" in t for t in titles))
        self.assertTrue(any("Līlā" in t for t in titles))
        self.assertTrue(any("Brahmās" in t for t in titles))

    def test_pramana_matrix_evaluation(self):
        matrix = EpistemicRevelationEngine.evaluate_pramana_matrix()
        self.assertEqual(matrix["total_canonical_episodes"], 5)
        self.assertIn("Śabda", matrix["primary_epistemic_warrant"])
        weights = matrix["pramana_validity_weights"]
        self.assertEqual(weights["Pratyaksa_Sensory"], 0.0)
        self.assertEqual(weights["Sabda_Scripture"], 1.0)
        self.assertLess(weights["Anupalabdhi_NonPerception"], 0.0)


class TestEschatologicalConcordismEngine(unittest.TestCase):
    """Tests the Concordism Demarcation Index for universal dissolution."""

    def test_comparative_models_count(self):
        models = EschatologicalConcordismEngine.get_comparative_models()
        self.assertEqual(len(models), 5)
        model_names = [m.model_name for m in models]
        self.assertTrue(any("Prakrtika" in m for m in model_names))
        self.assertTrue(any("Big Crunch" in m for m in model_names))
        self.assertTrue(any("Heat Death" in m for m in model_names))
        self.assertTrue(any("Penrose" in m for m in model_names))
        self.assertTrue(any("Ekpyrotic" in m for m in model_names))

    def test_ecdi_scores(self):
        ecdi = EschatologicalConcordismEngine.calculate_ecdi()
        self.assertGreater(ecdi["indological_firewall_percentage"], 90.0)
        self.assertLess(ecdi["eschatological_concordance_percentage"], 0.50)
        self.assertTrue("CONCORDISM REJECTED" in ecdi["epistemic_verdict"])


class TestMasterAnalysis(unittest.TestCase):
    """Tests end-to-end integration and execution of the master analysis."""

    def test_master_pipeline(self):
        res = run_master_analysis()
        self.assertEqual(res["pralaya_orders_count"], 4)
        self.assertEqual(res["naimittika_dissolutions_per_universe"], 36000)
        self.assertEqual(res["sankhya_resorption_stages"], 7)
        self.assertEqual(res["trans_universal_episodes_analyzed"], 5)
        self.assertGreater(res["indological_firewall_percentage"], 90.0)


if __name__ == "__main__":
    unittest.main()
