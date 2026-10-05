"""
test_krishna_mahabharata_meta_epistemic_axiomatics_engine.py

Unit test suite for krishna_mahabharata_meta_epistemic_axiomatics_engine.py.
Verifies axiomatic properties, algorithmic information invariance, model-theoretic equivalence,
Aumann disagreement preservation, Sellarsian category classification, and protocol safety firewalls.
"""

import unittest
from krishna_mahabharata_meta_epistemic_axiomatics_engine import (
    SafetyFirewall,
    ProtocolViolationError,
    AlgorithmicComplexityAnalyzer,
    ModelTheoreticValidator,
    AumannDisagreementSimulator,
    SellarsianImageDualism,
    MasterEpistemicAuditEngine
)


class TestSafetyFirewall(unittest.TestCase):
    def test_forbidden_verdicts_raise_violation(self):
        forbidden = ["PROVEN", "DISPROVEN", "TRUE", "FALSE", "CONFIRMED", "REFUTED"]
        for domain in SafetyFirewall.METAPHYSICAL_DOMAINS:
            for verdict in forbidden:
                with self.assertRaises(ProtocolViolationError):
                    SafetyFirewall.audit_assertion(domain, verdict)

    def test_permitted_assertions_pass(self):
        for domain in SafetyFirewall.METAPHYSICAL_DOMAINS:
            self.assertTrue(SafetyFirewall.audit_assertion(domain, None))
        # Non-metaphysical domains can have evaluations
        self.assertTrue(SafetyFirewall.audit_assertion("K1_HISTORICAL_CHIEFTAIN", "CORROBORATED"))


class TestAlgorithmicComplexityAnalyzer(unittest.TestCase):
    def test_description_length_calculation(self):
        l_tot = AlgorithmicComplexityAnalyzer.calculate_description_length(100.0, 50.0)
        self.assertEqual(l_tot, 150.0)

    def test_mdl_empirical_invariance(self):
        res = AlgorithmicComplexityAnalyzer.evaluate_mdl_invariance()
        self.assertTrue(res["is_empirically_invariant"])
        self.assertEqual(res["empirical_information_gain_bits"], 0.0)
        self.assertGreater(res["delta_mdl_bits"], 0.0)  # Occam penalty for added metaphysical axioms


class TestModelTheoreticValidator(unittest.TestCase):
    def test_physical_sentences_elementary_equivalent(self):
        res = ModelTheoreticValidator.test_elementary_equivalence(
            sentence="contains_bloomery_iron(Hastinapur_Period_II)",
            language="L_phys"
        )
        self.assertTrue(res["elementary_equivalent"])
        self.assertTrue(res["truth_in_M_nat"])
        self.assertTrue(res["truth_in_M_theo"])

    def test_theological_sentences_external_to_physics(self):
        res = ModelTheoreticValidator.test_elementary_equivalence(
            sentence="is_svayam_bhagavan(Krishna)",
            language="L_theo"
        )
        self.assertFalse(res["elementary_equivalent"])
        self.assertIsNone(res["truth_in_M_nat"])

    def test_reduct_isomorphism(self):
        res = ModelTheoreticValidator.verify_reduct_isomorphism()
        self.assertTrue(res["reduct_isomorphism"])
        self.assertFalse(res["physical_signatures_distinguishable"])


class TestAumannDisagreementSimulator(unittest.TestCase):
    def test_bayesian_consensus_conservation(self):
        sim = AumannDisagreementSimulator.simulate_bayesian_consensus()
        self.assertTrue(sim["disagreement_conserved"])
        self.assertAlmostEqual(sim["prior_variance"], sim["posterior_variance"], places=10)
        self.assertAlmostEqual(sim["variance_delta"], 0.0, places=10)

        # Ensure all individual agents have identical prior and posterior
        for agent_name, stats in sim["agent_trajectories"].items():
            self.assertAlmostEqual(stats["prior"], stats["posterior"], places=10)
            self.assertAlmostEqual(stats["delta_belief"], 0.0, places=10)
            self.assertAlmostEqual(stats["cumulative_bayes_factor"], 1.0, places=10)


class TestSellarsianImageDualism(unittest.TestCase):
    def test_category_error_detection(self):
        mixed_claim = "Brahmastra was an atomic bomb with radioactive carbon-14 fallout"
        res = SellarsianImageDualism.evaluate_claim_category(mixed_claim)
        self.assertTrue(res["is_category_error"])

    def test_pure_manifest_classification(self):
        manifest_claim = "Lord Krishna is the supreme avatar who reveals dharma and grants moksha"
        res = SellarsianImageDualism.evaluate_claim_category(manifest_claim)
        self.assertFalse(res["is_category_error"])
        self.assertTrue(res["has_manifest_tokens"])
        self.assertFalse(res["has_scientific_tokens"])

    def test_pure_scientific_classification(self):
        scientific_claim = "Hastinapur period II contains PGW stratum and iron arrowheads"
        res = SellarsianImageDualism.evaluate_claim_category(scientific_claim)
        self.assertFalse(res["is_category_error"])
        self.assertFalse(res["has_manifest_tokens"])
        self.assertTrue(res["has_scientific_tokens"])


class TestMasterEpistemicAuditEngine(unittest.TestCase):
    def test_full_audit_execution(self):
        audit = MasterEpistemicAuditEngine.generate_full_audit()
        self.assertEqual(audit["status"], "STRICTLY_COMPLIANT_ZERO_METAPHYSICAL_VERDICTS")
        self.assertGreaterEqual(len(audit["established_facts"]), 5)
        self.assertGreaterEqual(len(audit["genuine_unknowns"]), 3)
        self.assertIn("evidence_regarding_metaphysical_core", audit["falsification_thresholds"])


if __name__ == "__main__":
    unittest.main()
