"""
test_krishna_mahabharata_deep_frontier_engine.py
=================================================
Unit tests for the Deep Frontier Epistemic Engine covering:
1. Sanauli solid-disc cart vs Epic spoked war chariot dynamics.
2. Rakhigarhi to Iron Age archaeogenetics and Steppe / R1a-Z93 admixture.
3. Gana-Sangha factional sociometry and Shanti Parva 81 analysis.
4. BORI Critical Edition stemmatics and 3-stage textual expansion.
5. Four-strand syncretic timeline of Krishna.
6. 8-Dimensional Bayesian Chrono-Epistemic Joint Posterior.
"""

import unittest
import math
from krishna_mahabharata_deep_frontier_engine import (
    ArchaeoKinematicsEngine,
    ArchaeogeneticsEngine,
    GanaSanghaPoliticalEngine,
    BoriCriticalEditionStemmaticsEngine,
    FourStrandSyncretismEngine,
    Grand8DChronoEpistemicEngine,
)

class TestKrishnaMahabharataDeepFrontierEngine(unittest.TestCase):

    def test_wheel_dynamics_solid_vs_spoked(self):
        """Test moment of inertia calculation for solid disc vs spoked wheel."""
        solid = ArchaeoKinematicsEngine.compute_wheel_dynamics("solid_disc", radius_m=0.45, mass_kg=35.0)
        spoked = ArchaeoKinematicsEngine.compute_wheel_dynamics("spoked", radius_m=0.45, mass_kg=9.0)

        # Solid wheel: I = 0.5 * 35 * 0.45^2 = 3.54375
        self.assertAlmostEqual(solid["moment_of_inertia_kg_m2"], 3.5438, places=3)
        # Spoked wheel: I = 0.75 * 9 * 0.45^2 = 1.366875
        self.assertAlmostEqual(spoked["moment_of_inertia_kg_m2"], 1.3669, places=3)
        # Solid disc has substantially higher rotational inertia
        self.assertGreater(solid["moment_of_inertia_kg_m2"], spoked["moment_of_inertia_kg_m2"])

    def test_compare_vehicle_performance_sanauli_vs_ratha(self):
        """Test comparative kinematics between Sanauli cart and Epic spoked ratha."""
        perf = ArchaeoKinematicsEngine.compare_vehicle_performance()
        self.assertIn("sanauli_cart", perf)
        self.assertIn("epic_spoked_ratha", perf)
        self.assertGreater(perf["speed_advantage_factor"], 2.5)  # Ratha > 2.5x faster
        self.assertGreater(perf["agility_advantage_factor"], 1.5)  # Ratha > 1.5x more agile
        self.assertIn("Solid 3-piece", perf["sanauli_cart"]["wheel_type"])
        self.assertIn("Equus caballus", perf["epic_spoked_ratha"]["draft_animal"])

    def test_chariot_technology_likelihood(self):
        """Test likelihood of high-speed spoked horse-chariots across timelines."""
        l_3102 = ArchaeoKinematicsEngine.chariot_technology_likelihood(3102.0)
        l_1900 = ArchaeoKinematicsEngine.chariot_technology_likelihood(1900.0)
        l_950 = ArchaeoKinematicsEngine.chariot_technology_likelihood(950.0)

        self.assertLess(l_3102, 0.001)  # Zero spoked horse-chariots in 3102 BCE
        self.assertLess(l_1900, 0.05)   # Steppe inception, not in Gangetic plain
        self.assertGreater(l_950, 0.90)  # Prime Vedic PGW horizon

    def test_steppe_admixture_proportion(self):
        """Test Steppe pastoralist admixture fraction from 2500 BCE to Iron Age."""
        admix_2600 = ArchaeogeneticsEngine.steppe_admixture_proportion(2600.0)
        admix_1400 = ArchaeogeneticsEngine.steppe_admixture_proportion(1400.0)
        admix_950 = ArchaeogeneticsEngine.steppe_admixture_proportion(950.0)

        self.assertEqual(admix_2600, 0.0)  # Rakhigarhi 0% Steppe
        self.assertAlmostEqual(admix_1400, 0.11, places=2)  # Half-admixture
        self.assertGreater(admix_950, 0.18)  # Significant Iron Age presence
        self.assertLessEqual(admix_950, 0.22)

    def test_genetic_consistency_likelihood(self):
        """Test genetic likelihood of Indo-Aryan pastoral warrior elite presence."""
        l_gen_3102 = ArchaeogeneticsEngine.genetic_consistency_likelihood(3102.0)
        l_gen_1400 = ArchaeogeneticsEngine.genetic_consistency_likelihood(1400.0)
        l_gen_950 = ArchaeogeneticsEngine.genetic_consistency_likelihood(950.0)

        self.assertLess(l_gen_3102, 1e-4)
        self.assertGreater(l_gen_1400, 0.5)
        self.assertGreaterEqual(l_gen_950, 0.95)

    def test_gana_sangha_krishna_narada(self):
        """Test Gana-Sangha modeling of Shanti Parva 81."""
        analysis = GanaSanghaPoliticalEngine.evaluate_krishna_narada_dialogue()
        self.assertEqual(len(analysis["key_verses"]), 3)
        self.assertIn("Ayudhajivi Sangha", analysis["panini_corroboration"])
        self.assertIn("Shanti Parva", analysis["textual_source"])

        stability = GanaSanghaPoliticalEngine.gana_sangha_stability_index(krishna_soft_power=60.0, factional_rivalry=40.0)
        self.assertEqual(stability, 0.60)

    def test_bori_critical_edition_stemmatics(self):
        """Test BORI Critical Edition textual stratigraphy statistics."""
        data = BoriCriticalEditionStemmaticsEngine.get_textual_stratigraphy()
        self.assertEqual(data["manuscripts_collated"], 1259)
        self.assertEqual(data["critical_edition_verses"], 73784)
        self.assertEqual(data["vulgate_verses"], 100000)
        self.assertEqual(data["excised_verses"], 26216)
        self.assertAlmostEqual(data["excised_percentage"], 26.22, places=1)

        strata = data["strata"]
        self.assertEqual(strata["tier_1_jaya"]["nominal_verse_count"], 8800)
        self.assertEqual(strata["tier_2_bharata"]["nominal_verse_count"], 24000)
        self.assertEqual(strata["tier_3_mahabharata"]["critical_edition_verse_count"], 73784)

    def test_four_strand_syncretism(self):
        """Test four-strand historical syncretism tracking."""
        strands = FourStrandSyncretismEngine.get_four_strands()
        self.assertEqual(len(strands), 4)

        # 950 BCE: Only strand 1 active
        score_950 = FourStrandSyncretismEngine.syncretic_coalescence_score(950.0)
        self.assertEqual(score_950["strand_1_devakiputra"], 1.0)
        self.assertEqual(score_950["strand_2_vasudeva"], 0.0)
        self.assertEqual(score_950["strand_3_gopala"], 0.0)

        # 100 BCE: Strand 1 and 2 fully active, 3 and 4 emerging
        score_100 = FourStrandSyncretismEngine.syncretic_coalescence_score(100.0)
        self.assertEqual(score_100["strand_1_devakiputra"], 1.0)
        self.assertEqual(score_100["strand_2_vasudeva"], 1.0)
        self.assertGreater(score_100["strand_3_gopala"], 0.0)
        self.assertGreater(score_100["strand_4_narayana_vishnu"], 0.0)

    def test_grand_8d_likelihoods(self):
        """Test evaluation of all 8 independent empirical dimensions."""
        likes_950 = Grand8DChronoEpistemicEngine.evaluate_likelihoods(950.0)
        self.assertEqual(len(likes_950), 8)

        # All 8 dimensions must have high likelihood near 950 BCE
        for dim, val in likes_950.items():
            self.assertGreater(val, 0.1, f"Dimension {dim} unexpectedly low at 950 BCE: {val}")

        # At 3102 BCE, iron, astronomy, genetics, kinematics, dynasty must be near zero
        likes_3102 = Grand8DChronoEpistemicEngine.evaluate_likelihoods(3102.0)
        self.assertLess(likes_3102["iron_metallurgy"], 1e-10)
        self.assertLess(likes_3102["archaeo_kinematics"], 1e-3)
        self.assertLess(likes_3102["archaeogenetics"], 1e-4)

    def test_grand_8d_grid_search_map(self):
        """Test grid search finds MAP epoch in Early Iron Age (c. 950-960 BCE)."""
        res = Grand8DChronoEpistemicEngine.grid_search_posterior(start_bce=3200.0, end_bce=600.0, step=20.0)
        map_epoch = res["map_epoch_bce"]

        # MAP epoch must fall in the Early Iron Age PGW window (900-1000 BCE)
        self.assertGreaterEqual(map_epoch, 920.0)
        self.assertLessEqual(map_epoch, 1000.0)

        # Check massive log-likelihood delta against 3102 BCE
        self.assertGreater(res["delta_log_l_950_vs_3102"], 1500.0)

    def test_epistemic_invariants_preserved(self):
        """Verify protocol invariants: no scripture as lab data, no absence as disproof."""
        res = Grand8DChronoEpistemicEngine.grid_search_posterior(start_bce=1500.0, end_bce=800.0, step=50.0)
        self.assertIn("Maximum A Posteriori", res["epistemic_conclusion"])
        self.assertIn("Early Iron Age", res["epistemic_conclusion"])


if __name__ == "__main__":
    unittest.main()
