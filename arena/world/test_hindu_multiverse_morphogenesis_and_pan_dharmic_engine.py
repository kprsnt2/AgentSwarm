"""
UNIT TEST SUITE FOR HINDU MULTIVERSE MORPHOGENESIS & PAN-DHARMIC ENGINE
=======================================================================
Author: Kepler (A001) - Generation 0 Research Agent
Verifies:
1. 6-stage morphogenetic timeline progression and metrics
2. Yathāpūrvam hermeneutic matrix across 6 schools and demarcation
3. Pan-Dharmic comparative cosmography (Hindu vs. Buddhist vs. Jain)
4. Formal axiomatic classifier and protocol violation demarcation
"""

import unittest
import math
from hindu_multiverse_morphogenesis_and_pan_dharmic_engine import (
    VedicToPuranicMorphogenesis,
    YathapurvamHermeneuticMatrix,
    PanDharmicMultiverseComparison,
    HinduMultiverseAxiomaticEngine,
    run_comprehensive_adjudication
)


class TestVedicToPuranicMorphogenesis(unittest.TestCase):

    def test_strata_count_and_order(self):
        strata = VedicToPuranicMorphogenesis.get_strata_summary()
        self.assertEqual(len(strata), 6)
        self.assertEqual(strata[0]["stratum_id"], 1)
        self.assertEqual(strata[-1]["stratum_id"], 6)

    def test_early_vedic_singularism(self):
        stratum_1 = VedicToPuranicMorphogenesis.STRATA[0]
        self.assertEqual(stratum_1["spatial_universe_count"], 1)
        self.assertFalse(stratum_1["is_multiverse_spatial"])
        self.assertTrue(stratum_1["is_multiverse_temporal"])
        self.assertIn("10.129", stratum_1["primary_texts"][0])

    def test_puranic_spatial_rupture(self):
        stratum_4 = VedicToPuranicMorphogenesis.STRATA[3]
        self.assertTrue(stratum_4["is_multiverse_spatial"])
        self.assertGreaterEqual(stratum_4["spatial_universe_count"], 1.0e14)
        self.assertIn("Bhāgavata Purāṇa", stratum_4["primary_texts"][1])

    def test_trajectory_computation(self):
        traj = VedicToPuranicMorphogenesis.compute_morphogenetic_trajectory()
        self.assertEqual(traj["total_strata"], 6)
        self.assertEqual(traj["spatial_rupture_stratum"], 4)
        self.assertEqual(traj["fractal_rupture_stratum"], 5)
        # Check monotonic increase in complexity
        complexities = [s["complexity_bits"] for s in traj["trajectory"]]
        self.assertEqual(complexities, sorted(complexities))


class TestYathapurvamHermeneuticMatrix(unittest.TestCase):

    def test_verse_identification(self):
        self.assertIn("sūryācandramasau dhātā yathāpūrvamakalpayat", YathapurvamHermeneuticMatrix.VERSE_TEXT)

    def test_all_schools_evaluated(self):
        schools = YathapurvamHermeneuticMatrix.evaluate_schools()
        self.assertGreaterEqual(len(schools), 6)
        school_ids = [s["school_id"] for s in schools]
        self.assertIn("vedic_ritual", school_ids)
        self.assertIn("purva_mimamsa", school_ids)
        self.assertIn("advaita_vedanta", school_ids)
        self.assertIn("modern_concordism", school_ids)
        self.assertIn("modern_indology", school_ids)

    def test_demarcation_audit(self):
        audit = YathapurvamHermeneuticMatrix.get_demarcation_audit()
        self.assertFalse(audit["supports_spatial_parallel_universes"])
        self.assertTrue(audit["supports_temporal_cyclicality"])
        self.assertTrue(audit["concordist_distortion_present"])
        self.assertIn("HISTORICALLY INVALID CONCORDISM", audit["philological_verdict"])


class TestPanDharmicMultiverseComparison(unittest.TestCase):

    def test_tradition_retrieval(self):
        puranic = PanDharmicMultiverseComparison.get_tradition_data("puranic_hindu")
        self.assertEqual(puranic["cosmos_unit_name"], "Brahmāṇḍa (Cosmic Egg)")
        self.assertEqual(puranic["total_worlds"], 1.0e14)

        buddhist_nikaya = PanDharmicMultiverseComparison.get_tradition_data("buddhist_abhidharma")
        self.assertEqual(buddhist_nikaya["total_worlds"], 1.0e9)

        jain = PanDharmicMultiverseComparison.get_tradition_data("jain_classical")
        self.assertEqual(jain["total_worlds"], 1)

    def test_jain_singular_outlier(self):
        comparison = PanDharmicMultiverseComparison.compare_structural_parameters()
        self.assertEqual(comparison["traditions_analyzed"], 4)
        for t in comparison["comparison"]:
            if t["tradition_key"] == "jain_classical":
                self.assertFalse(t["has_spatial_multiverse"])
                self.assertEqual(t["total_worlds"], 1)
            elif t["tradition_key"] in ["puranic_hindu", "buddhist_abhidharma", "buddhist_mahayana"]:
                self.assertTrue(t["has_spatial_multiverse"])


class TestHinduMultiverseAxiomaticEngine(unittest.TestCase):

    def test_detect_protocol_violation_laboratory_concordism(self):
        res = HinduMultiverseAxiomaticEngine.classify_claim(
            text_source="Internet Apologetics blog on RV 10.190.3",
            claim_description="Vedas predicted Einstein's General Relativity and quantum multiverse",
            is_primary_sanskrit=False,
            claims_modern_physics_equivalence=True,
            asserts_spatial_plurality=True,
            asserts_temporal_plurality=True
        )
        self.assertFalse(res["is_valid_academic_claim"])
        self.assertEqual(res["epistemic_class"], "Apologetic / Concordist Fallacy")
        self.assertTrue(any("PROTOCOL VIOLATION" in v for v in res["protocol_violations"]))

    def test_valid_primary_text_classification(self):
        res = HinduMultiverseAxiomaticEngine.classify_claim(
            text_source="Bhāgavata Purāṇa 10.14.11",
            claim_description="Crores of cosmic eggs floating in pores like dust particles",
            is_primary_sanskrit=True,
            claims_modern_physics_equivalence=False,
            asserts_spatial_plurality=True,
            asserts_temporal_plurality=True
        )
        self.assertTrue(res["is_valid_academic_claim"])
        self.assertEqual(res["epistemic_class"], "Primary Textual Evidence")
        self.assertEqual(res["multiverse_topology"], "Type 2/3: Spatial Bubble & Asynchronous Temporal Multiverse")

    def test_full_pipeline_execution(self):
        res = run_comprehensive_adjudication()
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("morphogenetic_trajectory", res)
        self.assertIn("yathapurvam_audit", res)
        self.assertIn("pan_dharmic_comparison", res)


if __name__ == "__main__":
    unittest.main()
