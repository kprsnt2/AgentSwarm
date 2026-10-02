"""
test_dharmic_epistemic_demarcation.py

Comprehensive test suite verifying the Epistemic Demarcation Framework,
Firewall Enforcement, Information Theory calculations, and Planetary Synchronization.
"""

import unittest
import math
from dharmic_epistemic_demarcation import (
    ProtocolViolationError,
    EpistemicCategory,
    Pramana,
    AdjudicationStatus,
    FormalDharmicClaim,
    VedicInformationTheoryModel,
    PuranicPlanetarySynchronizationModel,
    BayesianMetaphysicalInvarianceModel,
    ComprehensiveDharmicTaxonomyRegistry
)


class TestEpistemicFirewallEnforcement(unittest.TestCase):

    def setUp(self):
        self.registry = ComprehensiveDharmicTaxonomyRegistry()

    def test_firewall_raises_on_class_b_verdict(self):
        """Invariant: Attempting to assert a true/false verdict on any Class B claim MUST raise ProtocolViolationError."""
        class_b_claims = self.registry.get_claims_by_category(EpistemicCategory.CLASS_B_METAPHYSICAL_ONTOLOGICAL)
        self.assertGreater(len(class_b_claims), 0)

        for claim in class_b_claims:
            with self.assertRaises(ProtocolViolationError):
                claim.attempt_verdict_assertion("TRUE")
            with self.assertRaises(ProtocolViolationError):
                claim.attempt_verdict_assertion("FALSE")
            with self.assertRaises(ProtocolViolationError):
                claim.attempt_verdict_assertion("PROVEN")
            with self.assertRaises(ProtocolViolationError):
                claim.attempt_verdict_assertion("DISPROVEN")

    def test_class_b_claims_have_zero_discriminative_bayes_power(self):
        """Invariant: Metaphysical claims cannot possess empirical Bayes factor discriminative power."""
        class_b_claims = self.registry.get_claims_by_category(EpistemicCategory.CLASS_B_METAPHYSICAL_ONTOLOGICAL)
        for claim in class_b_claims:
            self.assertEqual(claim.bayes_factor_discriminative_power, 0.0)
            self.assertIsNone(claim.empirical_investigation_method)
            self.assertIsNotNone(claim.epistemic_insulation_mechanism)
            self.assertEqual(claim.adjudication_status, AdjudicationStatus.EMPIRICALLY_UNDECIDABLE)

    def test_class_a_claims_are_decidable(self):
        """Invariant: Historical claims must have empirical investigation methods and non-zero discriminative power."""
        class_a_claims = self.registry.get_claims_by_category(EpistemicCategory.CLASS_A_HISTORICAL_TEXTUAL)
        self.assertGreater(len(class_a_claims), 0)
        for claim in class_a_claims:
            self.assertEqual(claim.adjudication_status, AdjudicationStatus.EMPIRICALLY_DECIDABLE)
            self.assertIsNotNone(claim.empirical_investigation_method)
            self.assertIsNone(claim.epistemic_insulation_mechanism)
            self.assertGreater(claim.bayes_factor_discriminative_power, 0.0)

    def test_registry_firewall_audit(self):
        """Audit function must confirm zero violations across entire registry."""
        audit = self.registry.verify_firewall_integrity()
        self.assertTrue(audit["firewall_intact"])
        self.assertEqual(audit["violations_count"], 0)
        self.assertEqual(audit["total_claims"], 12)


class TestVedicInformationTheory(unittest.TestCase):

    def test_redundancy_scaling(self):
        # Test 10-word verse segment
        res = VedicInformationTheoryModel.calculate_patha_redundancy(10)
        self.assertEqual(res["pada_tokens"], 10)
        self.assertEqual(res["krama_tokens"], 18)
        self.assertEqual(res["jata_tokens"], 54)
        # Ghana tokens: (10 - 2) * 13 + 6 = 8 * 13 + 6 = 104 + 6 = 110
        self.assertEqual(res["ghana_tokens"], 110)
        self.assertEqual(res["redundancy_factors"]["ghana"], 11.0)
        self.assertEqual(res["internal_word_repetition_multiplicity"], 13)
        self.assertGreater(res["error_suppression_rate"], 0.999999)

    def test_word_count_validation(self):
        with self.assertRaises(ValueError):
            VedicInformationTheoryModel.calculate_patha_redundancy(2)


class TestPuranicPlanetarySynchronization(unittest.TestCase):

    def test_mahayuga_arithmetic(self):
        sync = PuranicPlanetarySynchronizationModel
        self.assertEqual(sync.MAHAYUGA_YEARS, 4_320_000)
        self.assertEqual(sync.KALPA_YEARS, 4_320_000_000)
        self.assertEqual(sync.BRAHMA_NYCTHEMERON_YEARS, 8_640_000_000)
        self.assertEqual(sync.BRAHMA_LIFETIME_YEARS, 311_040_000_000_000)

    def test_planetary_periods(self):
        periods = PuranicPlanetarySynchronizationModel.get_astronomical_periods()
        # Sun orbital period in solar years must be exactly 1.0
        self.assertAlmostEqual(periods["Sun"], 1.0, places=5)
        # Mars orbital period: 4,320,000 / 2,296,832 = 1.88085 yr (~687 days)
        self.assertAlmostEqual(periods["Mars"], 1.88085, places=3)
        # Jupiter orbital period: 4,320,000 / 364,220 = 11.86096 yr (~11.86 years)
        self.assertAlmostEqual(periods["Jupiter"], 11.86096, places=3)
        # Saturn orbital period: 4,320,000 / 146,568 = 29.47437 yr (~29.46 years)
        self.assertAlmostEqual(periods["Saturn"], 29.47437, places=3)

    def test_earth_age_congruence_delta(self):
        congruence = PuranicPlanetarySynchronizationModel.analyze_cosmological_congruence()
        self.assertAlmostEqual(congruence["kalpa_duration_gyr"], 4.32, places=2)
        self.assertAlmostEqual(congruence["earth_age_radiometric_gyr"], 4.543, places=3)
        self.assertTrue(4.0 < congruence["earth_age_difference_pct"] < 6.0)


class TestBayesianMetaphysicalInvariance(unittest.TestCase):

    def test_likelihood_invariance_produces_zero_bits(self):
        res = BayesianMetaphysicalInvarianceModel.evaluate_bayes_factor(
            empirical_evidence_type="Fine-Tuning",
            prob_evidence_given_naturalism=0.4,
            prob_evidence_given_theism_or_brahman=0.4
        )
        self.assertAlmostEqual(res["bayes_factor"], 1.0, places=5)
        self.assertAlmostEqual(res["log_bayes_factor"], 0.0, places=5)
        self.assertAlmostEqual(res["discriminative_power_bits"], 0.0, places=5)
        self.assertTrue(res["is_empirically_invariant"])

    def test_discriminative_evidence_detection(self):
        res = BayesianMetaphysicalInvarianceModel.evaluate_bayes_factor(
            empirical_evidence_type="Hypothetical Direct Physical Sign",
            prob_evidence_given_naturalism=0.01,
            prob_evidence_given_theism_or_brahman=0.8
        )
        self.assertFalse(res["is_empirically_invariant"])
        self.assertGreater(res["bayes_factor"], 1.0)
        self.assertGreater(res["discriminative_power_bits"], 0.0)


if __name__ == "__main__":
    unittest.main()
