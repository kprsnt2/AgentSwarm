"""
test_krishna_mahabharata_grand_unified_engine.py

Unit tests for krishna_mahabharata_grand_unified_engine.py:
- Dwarka Marine Archaeology Engine
- Vrishni Apotheosis Engine
- Archaeometallurgy & Weaponry Engine
- Grand Unified 6D Bayesian Chrono Posterior Engine
- Master Historicity Synthesizer
"""

import unittest
from krishna_mahabharata_grand_unified_engine import (
    DwarkaMarineArchaeologyEngine,
    VrishniApotheosisEngine,
    ArchaeometallurgyWeaponryEngine,
    GrandUnifiedChronoPosteriorEngine,
    MasterHistoricitySynthesizer
)


class TestDwarkaMarineArchaeology(unittest.TestCase):
    def setUp(self):
        self.engine = DwarkaMarineArchaeologyEngine()

    def test_strata_count(self):
        self.assertGreaterEqual(len(self.engine.strata), 5)

    def test_dwarka_chronology_evaluation(self):
        res = self.engine.evaluate_dwarka_chronology()
        self.assertEqual(res["total_investigated_strata"], 5)
        # Protohistoric settlement at Bet Dwarka is c. 1400-1520 BCE
        self.assertGreaterEqual(res["earliest_material_settlement_bce"], 1350)
        self.assertIn("Indo-Arab", res["anchor_typology"])
        self.assertIn("primary_evidence", res["epistemic_verdict"])
        self.assertIn("scholarly_consensus", res["epistemic_verdict"])
        self.assertIn("devotional_claim", res["epistemic_verdict"])


class TestVrishniApotheosisEngine(unittest.TestCase):
    def setUp(self):
        self.engine = VrishniApotheosisEngine()

    def test_milestones_present(self):
        self.assertGreaterEqual(len(self.engine.milestones), 8)
        names = [m.name for m in self.engine.milestones]
        self.assertTrue(any("Chandogya" in n for n in names))
        self.assertTrue(any("Panini" in n for n in names))
        self.assertTrue(any("Agathocles" in n for n in names))
        self.assertTrue(any("Heliodorus" in n for n in names))
        self.assertTrue(any("Mora Well" in n for n in names))

    def test_apotheosis_index_monotonicity(self):
        # Index should increase monotonically as time progresses forward
        idx_700bce = self.engine.compute_deification_index(-700)
        idx_500bce = self.engine.compute_deification_index(-500)
        idx_200bce = self.engine.compute_deification_index(-200)
        idx_15ce = self.engine.compute_deification_index(15)
        idx_455ce = self.engine.compute_deification_index(455)

        self.assertLess(idx_700bce, idx_500bce)
        self.assertLess(idx_500bce, idx_200bce)
        self.assertLess(idx_200bce, idx_15ce)
        self.assertLess(idx_15ce, idx_455ce)
        # At inflection point -200 BCE, index should be 0.5
        self.assertAlmostEqual(idx_200bce, 0.5, places=2)

    def test_trajectory_evaluation(self):
        res = self.engine.evaluate_apotheosis_trajectory()
        self.assertIn("trajectory", res)
        self.assertEqual(len(res["trajectory"]), len(self.engine.milestones))


class TestArchaeometallurgyWeaponryEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ArchaeometallurgyWeaponryEngine()

    def test_metallurgical_cultures(self):
        self.assertEqual(len(self.engine.cultures), 4)

    def test_metallurgical_likelihood(self):
        p_3102 = self.engine.compute_metallurgical_likelihood(3102.0)
        p_950 = self.engine.compute_metallurgical_likelihood(950.0)
        p_1900 = self.engine.compute_metallurgical_likelihood(1900.0)

        self.assertAlmostEqual(p_3102, 0.0, places=4)
        self.assertLess(p_1900, 0.01)
        self.assertGreater(p_950, 0.8)

    def test_epic_weaponry_congruence(self):
        res_3102 = self.engine.evaluate_epic_weaponry_congruence(3102.0)
        res_950 = self.engine.evaluate_epic_weaponry_congruence(950.0)

        self.assertIn("Physically & Metallurgically Impossible", res_3102["physical_diagnosis"])
        self.assertEqual(res_3102["congruence_percentage"], "0.0%")
        self.assertIn("Exact Match", res_950["physical_diagnosis"])
        self.assertGreater(res_950["likelihood_score"], 0.8)


class TestGrandUnifiedChronoPosteriorEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GrandUnifiedChronoPosteriorEngine()

    def test_joint_log_likelihood_computation(self):
        res_950 = self.engine.compute_joint_log_likelihood(950.0)
        res_3102 = self.engine.compute_joint_log_likelihood(3102.0)

        self.assertIn("joint_log_l", res_950)
        self.assertIn("joint_log_l", res_3102)
        # 950 BCE log likelihood should be vastly higher (less negative) than 3102 BCE
        self.assertGreater(res_950["joint_log_l"], res_3102["joint_log_l"])
        self.assertGreater(res_950["joint_log_l"] - res_3102["joint_log_l"], 1000.0)

    def test_grid_search_map(self):
        grid_res = self.engine.run_grid_search(start_bce=3200.0, end_bce=600.0, step=20.0)
        self.assertIn("map_epoch_bce", grid_res)
        # MAP epoch should fall strictly between 900 and 1020 BCE
        self.assertGreaterEqual(grid_res["map_epoch_bce"], 900.0)
        self.assertLessEqual(grid_res["map_epoch_bce"], 1020.0)

        ci68 = grid_res["credible_interval_68_bce"]
        self.assertLessEqual(ci68[0], grid_res["map_epoch_bce"])
        self.assertGreaterEqual(ci68[1], grid_res["map_epoch_bce"])
        self.assertGreater(grid_res["delta_log_likelihood_950_vs_3102"], 1000.0)


class TestMasterHistoricitySynthesizer(unittest.TestCase):
    def setUp(self):
        self.synthesizer = MasterHistoricitySynthesizer()

    def test_full_synthesis(self):
        report = self.synthesizer.generate_full_synthesis()
        self.assertIn("dwarka_marine_archaeology", report)
        self.assertIn("vrishni_apotheosis_trajectory", report)
        self.assertIn("metallurgical_congruence_950", report)
        self.assertIn("metallurgical_congruence_3102", report)
        self.assertIn("bayesian_chrono_synthesis", report)


if __name__ == "__main__":
    unittest.main()
