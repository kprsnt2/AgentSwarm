"""
test_krishna_mahabharata_textual_epigraphy_and_metallurgy_engine.py

Unit test suite for krishna_mahabharata_textual_epigraphy_and_metallurgy_engine.py.
Verifies Vrishni hero cult theogeny, BORI stemmatics, archaeo-metallurgy kinematics,
maritime geopolitics, and 10-domain Bayesian joint posterior inference.

Authors: Kepler (A001), Swarm Research Agent (Gen 0)
Workspace: D:/AgentSwarm/arena/world
"""

import unittest
from krishna_mahabharata_textual_epigraphy_and_metallurgy_engine import (
    EpistemicCategory,
    VrishniHeroCultTheogenyEngine,
    BORITextualStemmaticsEngine,
    ArchaeoMetallurgyAndWeaponryEngine,
    DvarakaMaritimeGeopoliticsEngine,
    ComprehensiveBayesianJointInferenceEngine,
    FalsificationAndCounterfactualEngine
)


class TestVrishniHeroCultTheogeny(unittest.TestCase):
    def test_epigraphic_corpus_completeness(self):
        corpus = VrishniHeroCultTheogenyEngine.EPIGRAPHIC_CORPUS
        self.assertGreaterEqual(len(corpus), 8)
        self.assertIn("Chandogya_Upanisad_3_17_6", corpus)
        self.assertIn("Mora_Well_Inscription_Mathura", corpus)
        self.assertIn("Heliodoros_Column_Besnagar", corpus)
        self.assertIn("Agathocles_Drachms_Ai_Khanoum", corpus)

        for name, entry in corpus.items():
            self.assertEqual(entry["category"], EpistemicCategory.PRIMARY_DATA)
            self.assertIn("attestation", entry)
            self.assertIn("epistemic_status", entry)

    def test_hero_cult_transition_and_samba(self):
        transition = VrishniHeroCultTheogenyEngine.HERO_CULT_TRANSITION
        self.assertEqual(len(transition["pancaviras"]), 5)
        samba = next(h for h in transition["pancaviras"] if h["name"] == "Samba")
        self.assertEqual(samba["status"], "EXCISED")
        self.assertEqual(len(transition["samba_exclusion_reasons"]), 4)

    def test_theogeny_timeline_and_stages(self):
        timeline = VrishniHeroCultTheogenyEngine.get_theogeny_timeline()
        self.assertGreaterEqual(len(timeline), 8)
        accretion = VrishniHeroCultTheogenyEngine.evaluate_hero_to_god_accretion()
        self.assertEqual(accretion["num_stages"], 5)
        self.assertIn("historical accretion", accretion["epistemic_verdict"])


class TestBORITextualStemmatics(unittest.TestCase):
    def test_textual_accretion_metrics(self):
        accretion = BORITextualStemmaticsEngine.calculate_textual_accretion_rate()
        self.assertEqual(accretion["initial_jaya_verses"], 8800.0)
        self.assertEqual(accretion["final_ce_verses"], 73784.0)
        self.assertAlmostEqual(accretion["expansion_factor"], 8.385, places=2)
        self.assertAlmostEqual(accretion["annual_compounded_growth_pct"], 0.1934, places=2)
        self.assertEqual(accretion["bori_pruned_spurious_verses"], 21216.0)
        self.assertAlmostEqual(accretion["bori_pruning_percentage"], 22.33, places=1)

    def test_parva_entropy_and_composition(self):
        composition = BORITextualStemmaticsEngine.calculate_parva_entropy_and_composition()
        total_parva_sum = sum(BORITextualStemmaticsEngine.PARVA_VERSE_COUNTS_BORI.values())
        self.assertEqual(composition["total_critical_edition_verses"], total_parva_sum)
        self.assertGreater(composition["shannon_entropy_bits"], 3.0)
        # Santi + Anusasana didactic verses (13716 + 6702 = 20418)
        self.assertEqual(composition["didactic_encyclopedic_verses"], 13716 + 6702)
        self.assertAlmostEqual(composition["didactic_encyclopedic_percentage"], 26.57, places=1)
        # Battle parvas (Bhisma, Drona, Karna, Salya, Sauptika)
        self.assertAlmostEqual(composition["battle_parvas_percentage"], 28.85, places=1)


class TestArchaeoMetallurgyAndWeaponry(unittest.TestCase):
    def test_cakra_kinematics(self):
        sim = ArchaeoMetallurgyAndWeaponryEngine.simulate_cakra_kinematics(
            mass_kg=0.85, outer_radius_m=0.14, v_release_ms=24.0, omega_spin_rads=85.0
        )
        self.assertEqual(sim["weapon_mass_kg"], 0.85)
        self.assertEqual(sim["release_velocity_kmh"], 86.4)
        self.assertGreater(sim["total_kinetic_energy_joules"], 240.0)
        self.assertGreater(sim["estimated_effective_range_m"], 40.0)
        self.assertLess(sim["estimated_effective_range_m"], 65.0)
        self.assertGreater(sim["impact_pressure_mpa"], 100.0)

    def test_gada_impact_mechanics(self):
        sim = ArchaeoMetallurgyAndWeaponryEngine.simulate_gada_impact_mechanics(
            mace_mass_kg=6.5, swing_velocity_ms=18.0
        )
        self.assertAlmostEqual(sim["kinetic_energy_joules"], 1053.0, places=1)
        self.assertAlmostEqual(sim["fracture_excess_ratio"], 5.85, places=1)
        self.assertGreater(sim["peak_impact_force_kn"], 9.0)

    def test_metallurgical_stratigraphy(self):
        strat = ArchaeoMetallurgyAndWeaponryEngine.METALLURGICAL_STRATIGRAPHY
        self.assertIn("Early_Iron_Age_PGW", strat)
        self.assertIn("Middle_Iron_Age_NBPW", strat)
        self.assertIn("Classical_Crucible_Steel", strat)
        self.assertIn("bloomery", strat["Early_Iron_Age_PGW"]["alloy"].lower())


class TestDvarakaMaritimeGeopolitics(unittest.TestCase):
    def test_maritime_anchors_and_strata(self):
        data = DvarakaMaritimeGeopoliticsEngine.UNDERWATER_ARCHAEOLOGICAL_DATA
        self.assertEqual(data["stone_anchors_discovered"], 142)
        self.assertEqual(data["lustrous_red_ware_strata"]["c14_date_range_bce"], (1520, 1050))
        self.assertEqual(data["submerged_structures"]["jetty_length_m"], 580.0)

    def test_transit_capacity(self):
        transit = DvarakaMaritimeGeopoliticsEngine.evaluate_transit_and_carrying_capacity()
        self.assertEqual(transit["migration_distance_km"], 1120.0)
        self.assertAlmostEqual(transit["estimated_transit_duration_days"], 62.2, places=1)
        self.assertAlmostEqual(transit["estimated_transit_months"], 2.1, places=1)


class TestComprehensiveBayesianJointInference(unittest.TestCase):
    def test_bayesian_posterior_decisiveness(self):
        res = ComprehensiveBayesianJointInferenceEngine.compute_joint_posterior()
        self.assertEqual(res["dominant_hypothesis"], "H4_Historical_Core")
        # Historical Core posterior should exceed 99.9%
        self.assertGreater(res["posteriors"]["H4_Historical_Core"], 0.999)
        self.assertLess(res["posteriors"]["H1_Complete_Myth"], 1e-5)
        self.assertLess(res["posteriors"]["H5_Devotional_Inerrancy"], 1e-5)

    def test_evidential_domains_count(self):
        domains = ComprehensiveBayesianJointInferenceEngine.EVIDENTIAL_DOMAINS
        self.assertEqual(len(domains), 10)
        for dom_id, dom_data in domains.items():
            self.assertEqual(len(dom_data["likelihoods"]), 5)


class TestFalsificationMatrix(unittest.TestCase):
    def test_falsification_conditions(self):
        matrix = FalsificationAndCounterfactualEngine.get_falsification_matrix()
        self.assertEqual(len(matrix), 3)
        targets = [c["target_hypothesis"] for c in matrix]
        self.assertTrue(any("H4" in t for t in targets))
        self.assertTrue(any("H1" in t for t in targets))
        self.assertTrue(any("H5" in t for t in targets))


if __name__ == "__main__":
    unittest.main()
