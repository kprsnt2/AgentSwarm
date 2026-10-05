"""
test_shiva_and_shambhala_unified_meta_epistemology_engine.py

Comprehensive Unit Test Suite for ShivaAndShambhalaUnifiedMetaEpistemologyEngine.
Validates protocol compliance, 12-facet categorization, information-theoretic bounds,
Carnapian semantics, and multi-valued modal mappings.
"""

import unittest
import math
from shiva_and_shambhala_unified_meta_epistemology_engine import (
    ShivaAndShambhalaUnifiedMetaEpistemologyEngine,
    EpistemicCategory,
    CarnapianType,
    CatuskotiValue,
    SyadvadaPredication,
)


class TestShivaAndShambhalaUnifiedMetaEpistemologyEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ShivaAndShambhalaUnifiedMetaEpistemologyEngine()

    def test_total_facets_count(self):
        facets = self.engine.get_all_facets()
        self.assertEqual(len(facets), 12)

    def test_shiva_and_shambhala_split(self):
        shiva_facets = [f for f in self.engine.get_all_facets() if f.target_subject == "Lord Shiva"]
        shambhala_facets = [f for f in self.engine.get_all_facets() if f.target_subject == "Shambhala"]
        self.assertEqual(len(shiva_facets), 6)
        self.assertEqual(len(shambhala_facets), 6)

    def test_empirical_vs_metaphysical_counts(self):
        empirical = self.engine.get_empirical_facets()
        metaphysical = self.engine.get_metaphysical_facets()
        self.assertEqual(len(empirical), 9)
        self.assertEqual(len(metaphysical), 3)

    def test_metaphysical_facet_ids(self):
        meta_ids = {f.claim_id for f in self.engine.get_metaphysical_facets()}
        self.assertEqual(meta_ids, {"S3", "S4", "B3"})

    def test_fisher_information_and_cramer_rao_bounds(self):
        for f in self.engine.get_metaphysical_facets():
            self.assertEqual(self.engine.compute_fisher_information(f.claim_id), 0.0)
            self.assertTrue(math.isinf(self.engine.compute_cramer_rao_lower_bound(f.claim_id)))
            self.assertEqual(self.engine.compute_shannon_information_gain_bits(f.claim_id), 0.0)
            self.assertEqual(self.engine.compute_kolmogorov_complexity_differential(f.claim_id), 0.0)

        for f in self.engine.get_empirical_facets():
            self.assertGreater(self.engine.compute_fisher_information(f.claim_id), 0.0)
            self.assertFalse(math.isinf(self.engine.compute_cramer_rao_lower_bound(f.claim_id)))
            self.assertGreater(self.engine.compute_shannon_information_gain_bits(f.claim_id), 0.0)

    def test_carnapian_types(self):
        # S3, S4, B3 are External Metaphysical Ontological
        for meta_id in ["S3", "S4", "B3"]:
            facet = self.engine.get_facet(meta_id)
            self.assertEqual(facet.carnapian_type, CarnapianType.EXTERNAL_METAPHYSICAL_ONTOLOGICAL)

        # S5 and B4 are Internal Framework Analytic / Hermeneutic
        for internal_id in ["S5", "B4"]:
            facet = self.engine.get_facet(internal_id)
            self.assertEqual(facet.carnapian_type, CarnapianType.INTERNAL_FRAMEWORK_ANALYTIC)

        # S1, S2, S6, B1, B2, B5, B6 are Empirical Synthetic
        for synth_id in ["S1", "S2", "S6", "B1", "B2", "B5", "B6"]:
            facet = self.engine.get_facet(synth_id)
            self.assertEqual(facet.carnapian_type, CarnapianType.EMPIRICAL_SYNTHETIC)

    def test_catuskoti_mappings(self):
        # Asti: S2, S5, S6, B1, B4, B5
        for asti_id in ["S2", "S5", "S6", "B1", "B4", "B5"]:
            self.assertEqual(self.engine.get_facet(asti_id).catuskoti_mapping, CatuskotiValue.ASTI)

        # Nasti: S1, B2, B6
        for nasti_id in ["S1", "B2", "B6"]:
            self.assertEqual(self.engine.get_facet(nasti_id).catuskoti_mapping, CatuskotiValue.NASTI)

        # Ubhayam: S4
        self.assertEqual(self.engine.get_facet("S4").catuskoti_mapping, CatuskotiValue.UBHAYAM)

        # Anubhayam: S3, B3
        for anubhayam_id in ["S3", "B3"]:
            self.assertEqual(self.engine.get_facet(anubhayam_id).catuskoti_mapping, CatuskotiValue.ANUBHAYAM)

    def test_syadvada_mappings(self):
        self.assertEqual(self.engine.get_facet("S1").syadvada_mapping, SyadvadaPredication.SYAD_NASTI)
        self.assertEqual(self.engine.get_facet("S2").syadvada_mapping, SyadvadaPredication.SYAD_ASTI)
        self.assertEqual(self.engine.get_facet("S3").syadvada_mapping, SyadvadaPredication.SYAD_AVAKTAVYA)
        self.assertEqual(self.engine.get_facet("S4").syadvada_mapping, SyadvadaPredication.SYAD_ASTI_AVAKTAVYA)
        self.assertEqual(self.engine.get_facet("B2").syadvada_mapping, SyadvadaPredication.SYAD_NASTI)
        self.assertEqual(self.engine.get_facet("B3").syadvada_mapping, SyadvadaPredication.SYAD_AVAKTAVYA)

    def test_euhemerism_posterior(self):
        posterior = self.engine.compute_euhemerism_posterior()
        self.assertLess(posterior, 0.0001)
        self.assertAlmostEqual(posterior, 5.29e-5, delta=1e-6)

    def test_epigraphic_arc_and_geodesy(self):
        self.assertAlmostEqual(self.engine.compute_epigraphic_arc_km(), 6857.73, delta=0.1)
        self.assertEqual(self.engine.compute_geodetic_coverage_percent(), 100.0)

    def test_protocol_safety_audit(self):
        audit = self.engine.run_protocol_safety_audit()
        self.assertTrue(audit.is_fully_compliant)
        self.assertFalse(audit.verdict_asserted)
        self.assertFalse(audit.proof_claimed)
        self.assertFalse(audit.disproof_claimed)
        self.assertFalse(audit.personal_conviction_present)
        self.assertTrue(audit.all_evidence_criteria_defined)
        self.assertTrue(audit.all_resistance_mechanics_formalized)
        self.assertTrue(audit.zero_fisher_info_on_metaphysical)
        self.assertTrue(audit.infinite_cramer_rao_on_metaphysical)
        self.assertEqual(len(audit.violations), 0)


if __name__ == "__main__":
    unittest.main()
