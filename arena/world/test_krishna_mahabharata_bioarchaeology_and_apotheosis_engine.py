"""
test_krishna_mahabharata_bioarchaeology_and_apotheosis_engine.py

Unit test suite verifying the quantitative validity and epistemic rigor of
krishna_mahabharata_bioarchaeology_and_apotheosis_engine.py.
"""

import unittest
import math
from krishna_mahabharata_bioarchaeology_and_apotheosis_engine import (
    EpistemicCategory,
    BioarchaeologyTaphonomyEngine,
    ApotheosisKineticsEngine,
    OralFormulaicEntropyEngine,
    CausalBayesianDemarcationEngine
)


class TestBioarchaeologyTaphonomy(unittest.TestCase):

    def test_bone_diagenesis_half_life_ordering(self):
        t_unburied_uncremated = BioarchaeologyTaphonomyEngine.calculate_bone_diagenesis_half_life(is_cremated=False, buried=False)
        t_buried_uncremated = BioarchaeologyTaphonomyEngine.calculate_bone_diagenesis_half_life(is_cremated=False, buried=True)
        t_unburied_cremated = BioarchaeologyTaphonomyEngine.calculate_bone_diagenesis_half_life(is_cremated=True, buried=False)
        t_buried_cremated = BioarchaeologyTaphonomyEngine.calculate_bone_diagenesis_half_life(is_cremated=True, buried=True)

        self.assertLess(t_unburied_uncremated, t_buried_uncremated)
        self.assertLess(t_buried_uncremated, t_unburied_cremated)
        self.assertLess(t_unburied_cremated, t_buried_cremated)
        self.assertAlmostEqual(t_unburied_uncremated, 45.0, places=2)

    def test_skeletal_recovery_probability(self):
        res = BioarchaeologyTaphonomyEngine.calculate_skeletal_recovery_probability(
            casualties=8000, cremation_fraction=0.95, years_elapsed=2950.0
        )
        self.assertIn("casualties_total", res)
        self.assertEqual(res["casualties_total"], 8000)
        self.assertGreater(res["p_zero_skeletons_given_battle"], 0.90)
        self.assertLess(res["surviving_uncremated_equivalent_skeletons"], 1.0)
        self.assertIn("verdict", res)

    def test_battlefield_benchmarks_integrity(self):
        benchmarks = BioarchaeologyTaphonomyEngine.BATTLEFIELD_BENCHMARKS
        self.assertGreaterEqual(len(benchmarks), 5)
        names = [b["battle"] for b in benchmarks]
        self.assertTrue(any("Kurukshetra" in n for n in names))
        self.assertTrue(any("Waterloo" in n for n in names))
        self.assertTrue(any("Cannae" in n for n in names))
        self.assertTrue(any("Marathon" in n for n in names))
        self.assertTrue(any("Towton" in n for n in names))


class TestApotheosisKinetics(unittest.TestCase):

    def test_apotheosis_index_bounds(self):
        idx_zero = ApotheosisKineticsEngine.calculate_apotheosis_index(1.0, 0.0, 0.0)
        self.assertAlmostEqual(idx_zero, 0.0, places=3)

        idx_full = ApotheosisKineticsEngine.calculate_apotheosis_index(0.0, 0.5, 0.5)
        self.assertAlmostEqual(idx_full, 0.50, places=2)

        idx_max = ApotheosisKineticsEngine.calculate_apotheosis_index(0.0, 1.0, 1.0)
        self.assertGreater(idx_max, 0.45)
        self.assertLessEqual(idx_max, 1.0)

    def test_syncretism_shannon_entropy(self):
        # Pure single stream should have zero entropy
        h_pure = ApotheosisKineticsEngine.calculate_syncretism_shannon_entropy(1.0, 0.0, 0.0)
        self.assertAlmostEqual(h_pure, 0.0, places=4)

        # Equal tripartite blend should achieve maximum entropy log2(3) = 1.58496 bits
        h_equal = ApotheosisKineticsEngine.calculate_syncretism_shannon_entropy(1.0, 1.0, 1.0)
        self.assertAlmostEqual(h_equal, math.log2(3.0), places=3)

    def test_chronological_apotheosis_trajectory(self):
        traj = ApotheosisKineticsEngine.evaluate_chronological_apotheosis_trajectory()
        self.assertEqual(len(traj), 9)

        # Verify earliest benchmark is Chandogya Upanishad with lowest apotheosis index
        first = traj[0]
        self.assertIn("Chandogya", first["source"])
        self.assertEqual(first["apotheosis_index"], 0.0)
        self.assertEqual(first["dominant_component"], "Vrishni Chieftain (Historical Human)")

        # Verify later benchmarks show progressive increase in apotheosis index
        last = traj[-1]
        self.assertIn("Bhagavata", last["source"])
        self.assertGreater(last["apotheosis_index"], first["apotheosis_index"])


class TestOralFormulaicEntropy(unittest.TestCase):

    def test_parva_metrics_comparison(self):
        comp = OralFormulaicEntropyEngine.compare_oral_vs_didactic_strata()
        self.assertGreater(comp["enrichment_ratio_formulaic"], 3.5)
        self.assertGreater(comp["enrichment_ratio_vedicisms"], 5.0)
        self.assertGreater(comp["battle_core_mean_formulaic_density"], 30.0)
        self.assertLess(comp["didactic_mean_formulaic_density"], 10.0)
        self.assertGreater(comp["battle_core_lexical_entropy"], comp["didactic_lexical_entropy"])


class TestCausalBayesianDemarcation(unittest.TestCase):

    def test_bayesian_posterior_closure(self):
        res = CausalBayesianDemarcationEngine.compute_joint_posterior_probabilities()
        posts = res["posteriors"]
        bf = res["bayes_factors"]

        self.assertGreater(posts["H4_Stratified_Historical_Core"], 0.999999)
        self.assertLess(posts["H1_Absolute_Mythicism"], 1e-15)
        self.assertLess(posts["H2_Devotional_Literalism"], 1e-25)
        self.assertLess(posts["H3_Solar_Astronomical_Allegory"], 1e-12)

        self.assertGreater(bf["BF_H4_over_H1_Mythicism"], 1e15)
        self.assertGreater(bf["BF_H4_over_H2_Literalism"], 1e30)
        self.assertGreater(bf["BF_H4_over_H3_SolarAllegory"], 1e12)

    def test_epistemic_categories_demarcation(self):
        allowed = {
            EpistemicCategory.PRIMARY_MATERIAL_OR_TEXT,
            EpistemicCategory.SCHOLARLY_CONSENSUS,
            EpistemicCategory.DEVOTIONAL_CLAIM
        }
        for bench in ApotheosisKineticsEngine.CHRONOSEQUENCE_BENCHMARKS:
            self.assertIn(bench["epistemic_status"], allowed)

        for text_k, text_data in BioarchaeologyTaphonomyEngine.MORTUARY_PRIMARY_TEXTS.items():
            self.assertIn(text_data["epistemic_status"], allowed)


if __name__ == "__main__":
    unittest.main()
