"""
test_shiva_and_shambhala_formal_demarcation_and_modal_engine.py

Unit tests for ShivaAndShambhalaFormalDemarcationAndModalEngine.
Verifies:
1. Protocol safety invariants (no verdict, no proof, no disproof, no personal conviction).
2. Epistemic category classifications across all 12 facets.
3. Information-theoretic bounds (Fisher Information = 0, Cramér-Rao = inf for metaphysical claims).
4. Carnapian internal/external framework mappings.
5. Modal logic (Catuṣkoṭi and Syādvāda) assignments.
6. Empirical vs. Metaphysical demarcation firewall.
"""

import unittest
import math
from shiva_and_shambhala_formal_demarcation_and_modal_engine import (
    ShivaAndShambhalaFormalDemarcationAndModalEngine,
    EpistemicCategory,
    CarnapianType,
    CatuskotiValue,
    SyadvadaPredication
)


class TestShivaAndShambhalaFormalDemarcationAndModalEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ShivaAndShambhalaFormalDemarcationAndModalEngine()

    def test_total_facets_count(self):
        claims = self.engine.get_all_claims()
        self.assertEqual(len(claims), 12, "Should deconstruct exactly 12 facets (6 Shiva, 6 Shambhala).")

    def test_shiva_facets_count(self):
        shiva_claims = self.engine.get_shiva_claims()
        self.assertEqual(len(shiva_claims), 6, "Lord Shiva inquiry must contain 6 distinct facets.")

    def test_shambhala_facets_count(self):
        shambhala_claims = self.engine.get_shambhala_claims()
        self.assertEqual(len(shambhala_claims), 6, "Shambhala inquiry must contain 6 distinct facets.")

    def test_protocol_safety_audit(self):
        audit = self.engine.audit_protocol_safety()
        self.assertTrue(audit.is_fully_compliant, f"Protocol audit failed with violations: {audit.violations}")
        self.assertFalse(audit.verdict_asserted, "Protocol failure: verdict was asserted!")
        self.assertFalse(audit.proof_claimed, "Protocol failure: proof was claimed!")
        self.assertFalse(audit.disproof_claimed, "Protocol failure: disproof was claimed!")
        self.assertFalse(audit.personal_conviction_present, "Protocol failure: personal conviction present!")
        self.assertTrue(audit.all_evidence_criteria_defined, "All claims must have defined evidence criteria.")
        self.assertTrue(audit.all_resistance_mechanics_formalized, "All metaphysical claims must formalize resistance mechanics.")

    def test_metaphysical_claims_fisher_information(self):
        metaphysical_claims = self.engine.get_metaphysically_undecidable_claims()
        self.assertGreater(len(metaphysical_claims), 0)
        for c in metaphysical_claims:
            self.assertEqual(c.fisher_information, 0.0, f"{c.claim_id} should have zero Fisher Information.")
            self.assertTrue(math.isinf(c.cramer_rao_bound), f"{c.claim_id} should have infinite Cramér-Rao lower bound.")
            self.assertEqual(c.underdetermination_index, 1.0, f"{c.claim_id} should have underdetermination index 1.0.")
            self.assertEqual(c.testability_index, 0.0, f"{c.claim_id} should have testability index 0.0.")

    def test_empirical_claims_fisher_information(self):
        empirical_claims = self.engine.get_empirically_decidable_claims()
        self.assertGreater(len(empirical_claims), 0)
        for c in empirical_claims:
            self.assertGreater(c.fisher_information, 0.0, f"{c.claim_id} must have positive Fisher Information.")
            self.assertFalse(math.isinf(c.cramer_rao_bound), f"{c.claim_id} must have finite Cramér-Rao lower bound.")
            self.assertGreater(c.testability_index, 0.5, f"{c.claim_id} testability index must exceed 0.5.")
            self.assertLess(c.underdetermination_index, 0.5, f"{c.claim_id} underdetermination index must be below 0.5.")

    def test_carnapian_framework_partition(self):
        claims = self.engine.get_all_claims()
        # S4 and S3 and B3 must be External Metaphysical Ontological
        self.assertEqual(claims["S3_THEISTIC_ISHVARA"].carnapian_type, CarnapianType.EXTERNAL_METAPHYSICAL_ONTOLOGICAL)
        self.assertEqual(claims["S4_GROUND_OF_CONSCIOUSNESS"].carnapian_type, CarnapianType.EXTERNAL_METAPHYSICAL_ONTOLOGICAL)
        self.assertEqual(claims["B3_ESOTERIC_PURE_LAND"].carnapian_type, CarnapianType.EXTERNAL_METAPHYSICAL_ONTOLOGICAL)

        # S5 and B4 must be Internal Framework Analytic/Hermeneutic
        self.assertEqual(claims["S5_INTERNAL_YOGIC"].carnapian_type, CarnapianType.INTERNAL_FRAMEWORK_ANALYTIC)
        self.assertEqual(claims["B4_INTERNAL_MICROCOSM"].carnapian_type, CarnapianType.INTERNAL_FRAMEWORK_ANALYTIC)

        # S1, S2, B1, B2, B6 must be Empirical Synthetic
        self.assertEqual(claims["S1_EUHEMERISM"].carnapian_type, CarnapianType.EMPIRICAL_SYNTHETIC)
        self.assertEqual(claims["S2_HISTORICAL_CULTURE"].carnapian_type, CarnapianType.EMPIRICAL_SYNTHETIC)
        self.assertEqual(claims["B1_PURANIC_SAMBHAL"].carnapian_type, CarnapianType.EMPIRICAL_SYNTHETIC)
        self.assertEqual(claims["B2_PHYSICAL_KINGDOM"].carnapian_type, CarnapianType.EMPIRICAL_SYNTHETIC)
        self.assertEqual(claims["B6_HOLLOW_EARTH"].carnapian_type, CarnapianType.EMPIRICAL_SYNTHETIC)

    def test_information_gain_for_metaphysical_claims(self):
        # Delta I = log2(Lambda). For metaphysical claims, Lambda = 1.0, so Delta I = 0.0 bits
        delta_i_s3 = self.engine.compute_information_gain_bits("S3_THEISTIC_ISHVARA")
        delta_i_s4 = self.engine.compute_information_gain_bits("S4_GROUND_OF_CONSCIOUSNESS")
        delta_i_b3 = self.engine.compute_information_gain_bits("B3_ESOTERIC_PURE_LAND")
        self.assertEqual(delta_i_s3, 0.0)
        self.assertEqual(delta_i_s4, 0.0)
        self.assertEqual(delta_i_b3, 0.0)

    def test_catuskoti_mappings_validity(self):
        claims = self.engine.get_all_claims()
        for c in claims.values():
            self.assertIsInstance(c.catuskoti_mapping, CatuskotiValue)
            self.assertIsInstance(c.syadvada_mapping, SyadvadaPredication)

    def test_summary_report_generation(self):
        report = self.engine.generate_summary_report()
        self.assertEqual(report["total_facets"], 12)
        self.assertEqual(report["shiva_facets"], 6)
        self.assertEqual(report["shambhala_facets"], 6)
        self.assertEqual(report["empirically_decidable_count"], 9)
        self.assertEqual(report["metaphysically_undecidable_count"], 3)
        self.assertTrue(report["protocol_audit"]["is_compliant"])


if __name__ == "__main__":
    unittest.main()
