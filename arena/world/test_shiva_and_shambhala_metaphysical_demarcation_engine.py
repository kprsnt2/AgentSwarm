"""
test_shiva_and_shambhala_metaphysical_demarcation_engine.py

Comprehensive unit test suite for ShivaAndShambhalaMetaphysicalDemarcationEngine.
Tests:
- Claim classification and facet taxonomy
- Epistemic category mappings
- Decidability bounds
- Information-theoretic invariance (D_KL = 0 and Lambda = 1 for metaphysical claims)
- Strict protocol violation detection and safety audits
- Underdetermination indices and testability metrics
"""

import unittest
from shiva_and_shambhala_metaphysical_demarcation_engine import (
    ShivaAndShambhalaMetaphysicalDemarcationEngine,
    EpistemicCategory,
    DecidabilityStatus,
)


class TestShivaAndShambhalaMetaphysicalDemarcationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ShivaAndShambhalaMetaphysicalDemarcationEngine()

    def test_total_claims_initialization(self):
        """Verify all 9 core facets across Shiva and Shambhala are initialized."""
        self.assertEqual(len(self.engine.claims), 9)
        self.assertIn("S1_EUHEMERISM", self.engine.claims)
        self.assertIn("S2_HISTORICAL_CULTURE", self.engine.claims)
        self.assertIn("S3_THEISTIC_DIVINITY", self.engine.claims)
        self.assertIn("S4_METAPHYSICAL_GROUND", self.engine.claims)
        self.assertIn("B1_PURANIC_SETTLEMENT", self.engine.claims)
        self.assertIn("B2_PHYSICAL_KINGDOM", self.engine.claims)
        self.assertIn("B3_PURE_LAND", self.engine.claims)
        self.assertIn("B4_INTERNAL_ALLEGORY", self.engine.claims)
        self.assertIn("B5_OCCULT_FABRICATION", self.engine.claims)

    def test_shiva_metaphysical_ground_incommensurability(self):
        """Verify that Trika Shaivism's Ground of Consciousness is marked incommensurable and untestable empirically."""
        ground_claim = self.engine.claims["S4_METAPHYSICAL_GROUND"]
        self.assertEqual(ground_claim.epistemic_category, EpistemicCategory.METAPHYSICAL_ONTOLOGICAL)
        self.assertEqual(ground_claim.decidability, DecidabilityStatus.METHODOLOGICALLY_INCOMMENSURABLE)
        self.assertEqual(ground_claim.testability_index, 0.0)
        self.assertEqual(ground_claim.underdetermination_index, 1.0)

        analysis = self.engine.analyze_why_it_resists_empirical_testing("S4_METAPHYSICAL_GROUND")
        self.assertEqual(analysis["likelihood_ratio_lambda"], 1.0)
        self.assertEqual(analysis["kullback_leibler_divergence_bits"], 0.0)
        self.assertIn("Subject-Object Duality Incommensurability", analysis["core_resistance_mechanisms"][0])

    def test_shiva_theistic_divinity_undecidability(self):
        """Verify theistic cosmic agent resists empirical testing due to theological immunization and concealment."""
        theistic_claim = self.engine.claims["S3_THEISTIC_DIVINITY"]
        self.assertEqual(theistic_claim.epistemic_category, EpistemicCategory.METAPHYSICAL_THEISTIC)
        self.assertEqual(theistic_claim.decidability, DecidabilityStatus.EMPIRICALLY_UNDECIDABLE)
        self.assertEqual(theistic_claim.testability_index, 0.0)
        self.assertEqual(theistic_claim.underdetermination_index, 1.0)

        analysis = self.engine.analyze_why_it_resists_empirical_testing("S3_THEISTIC_DIVINITY")
        self.assertEqual(analysis["likelihood_ratio_lambda"], 1.0)
        self.assertEqual(analysis["kullback_leibler_divergence_bits"], 0.0)

    def test_shiva_euhemerism_is_empirically_decidable(self):
        """Verify that mortal biological euhemerism is empirically decidable and testable."""
        euhemerism = self.engine.claims["S1_EUHEMERISM"]
        self.assertEqual(euhemerism.epistemic_category, EpistemicCategory.EMPIRICAL_HISTORICAL)
        self.assertEqual(euhemerism.decidability, DecidabilityStatus.EMPIRICALLY_DECIDABLE)
        self.assertGreater(euhemerism.testability_index, 0.9)
        self.assertLess(euhemerism.underdetermination_index, 0.1)

    def test_shiva_cultural_phenomenon_is_empirically_decidable(self):
        """Verify that cultural and epigraphic reality is 100% testable via archaeology/philology."""
        cult = self.engine.claims["S2_HISTORICAL_CULTURE"]
        self.assertEqual(cult.epistemic_category, EpistemicCategory.EMPIRICAL_HISTORICAL)
        self.assertEqual(cult.decidability, DecidabilityStatus.EMPIRICALLY_DECIDABLE)
        self.assertEqual(cult.testability_index, 1.0)
        self.assertEqual(cult.underdetermination_index, 0.0)

    def test_shambhala_pure_land_undecidability(self):
        """Verify that Kalachakra Pure Land resists empirical testing due to karmic veil and dimensional difference."""
        pure_land = self.engine.claims["B3_PURE_LAND"]
        self.assertEqual(pure_land.epistemic_category, EpistemicCategory.YOGIC_PHENOMENOLOGICAL)
        self.assertEqual(pure_land.decidability, DecidabilityStatus.EMPIRICALLY_UNDECIDABLE)
        self.assertEqual(pure_land.testability_index, 0.0)
        self.assertEqual(pure_land.underdetermination_index, 1.0)

        analysis = self.engine.analyze_why_it_resists_empirical_testing("B3_PURE_LAND")
        self.assertEqual(analysis["likelihood_ratio_lambda"], 1.0)
        self.assertEqual(analysis["kullback_leibler_divergence_bits"], 0.0)
        self.assertTrue(any("Karmic Veil Invariance" in r for r in analysis["core_resistance_mechanisms"]))

    def test_shambhala_puranic_settlement_is_empirically_decidable(self):
        """Verify that Puranic Sambhala in UP is empirically decidable via archaeology."""
        puranic = self.engine.claims["B1_PURANIC_SETTLEMENT"]
        self.assertEqual(puranic.epistemic_category, EpistemicCategory.EMPIRICAL_HISTORICAL)
        self.assertEqual(puranic.decidability, DecidabilityStatus.EMPIRICALLY_DECIDABLE)
        self.assertEqual(puranic.testability_index, 1.0)

    def test_shambhala_physical_kingdom_is_empirically_decidable(self):
        """Verify that a physical 3D kingdom on Earth's crust is testable by geodesy/radar."""
        kingdom = self.engine.claims["B2_PHYSICAL_KINGDOM"]
        self.assertEqual(kingdom.epistemic_category, EpistemicCategory.EMPIRICAL_PHYSICAL)
        self.assertEqual(kingdom.decidability, DecidabilityStatus.EMPIRICALLY_DECIDABLE)
        self.assertEqual(kingdom.testability_index, 1.0)

    def test_shambhala_occult_hollow_earth_is_empirically_decidable(self):
        """Verify that hollow Earth / Agartha claims are empirically decidable and testable by seismology."""
        occult = self.engine.claims["B5_OCCULT_FABRICATION"]
        self.assertEqual(occult.epistemic_category, EpistemicCategory.MODERN_PSEUDOHISTORICAL)
        self.assertEqual(occult.decidability, DecidabilityStatus.EMPIRICALLY_DECIDABLE)
        self.assertEqual(occult.testability_index, 1.0)

    def test_protocol_safety_clean_statements(self):
        """Verify that objective clarification statements pass the protocol safety check."""
        statements = [
            "This investigation clarifies what the claim actually asserts.",
            "The question of whether consciousness is the fundamental ground of being is not empirically decidable.",
            "We analyze why the metaphysical claims resist testing without asserting a personal conviction."
        ]
        report = self.engine.evaluate_protocol_safety(statements)
        self.assertTrue(report.is_valid)
        self.assertFalse(report.verdict_asserted)
        self.assertFalse(report.proof_claimed)
        self.assertFalse(report.disproof_claimed)
        self.assertEqual(len(report.violations), 0)

    def test_protocol_safety_catches_proof_violations(self):
        """Verify that any claim of having proven the metaphysical entity triggers a protocol violation."""
        statements = [
            "We have proven that Lord Shiva exists.",
        ]
        report = self.engine.evaluate_protocol_safety(statements)
        self.assertFalse(report.is_valid)
        self.assertTrue(report.proof_claimed)
        self.assertTrue(report.verdict_asserted)
        self.assertEqual(len(report.violations), 1)

    def test_protocol_safety_catches_disproof_violations(self):
        """Verify that any claim of having disproven the metaphysical entity triggers a protocol violation."""
        statements = [
            "Shiva is disproven by laboratory science.",
        ]
        report = self.engine.evaluate_protocol_safety(statements)
        self.assertFalse(report.is_valid)
        self.assertTrue(report.disproof_claimed)
        self.assertTrue(report.verdict_asserted)

    def test_protocol_safety_catches_conviction_violations(self):
        """Verify that presenting personal conviction triggers a protocol violation."""
        statements = [
            "My personal conviction is that the pure land exists.",
        ]
        report = self.engine.evaluate_protocol_safety(statements)
        self.assertFalse(report.is_valid)
        self.assertEqual(len(report.violations), 1)

    def test_comparative_demarcation_matrix(self):
        """Verify comparative demarcation matrix returns full details for all claims."""
        matrix = self.engine.compute_comparative_demarcation_matrix()
        self.assertEqual(len(matrix), 9)
        for item in matrix:
            self.assertIn("claim_id", item)
            self.assertIn("underdetermination_index", item)
            self.assertIn("testability_index", item)
            self.assertIn("likelihood_ratio_lambda", item)
            self.assertIn("kullback_leibler_divergence_bits", item)
            self.assertIn("core_resistance_mechanisms", item)

    def test_formal_summary_adherence(self):
        """Verify that the formal summary does not assert a verdict and matches brief requirements."""
        summary = self.engine.formal_demarcation_summary()
        self.assertFalse(summary["protocol_verdict_asserted"])
        self.assertEqual(summary["total_claims_analyzed"], 9)
        self.assertEqual(summary["empirically_decidable_count"], 6)
        self.assertEqual(summary["empirically_undecidable_count"], 3)


if __name__ == "__main__":
    unittest.main()
