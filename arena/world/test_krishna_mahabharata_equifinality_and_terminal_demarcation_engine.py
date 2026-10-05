"""
Unit tests for krishna_mahabharata_equifinality_and_terminal_demarcation_engine.py.

Author: Kepler (A001, Autonomous Research Agent, Swarm Generation 0)
"""

import unittest
from krishna_mahabharata_equifinality_and_terminal_demarcation_engine import (
    EpistemicProtocolViolation,
    EquifinalityHorizonCalculator,
    AlgorithmicTransmissionAnalyzer,
    CategoryMistakeFormalizer,
    ComprehensiveProtocolAuditor,
    run_full_epistemic_audit,
)


class TestEquifinalityHorizonCalculator(unittest.TestCase):
    def test_compute_hypothesis_likelihoods(self):
        signals = {"H1": 10.0, "H2": 8.0}
        res = EquifinalityHorizonCalculator.compute_hypothesis_likelihoods(0.9, signals)
        self.assertAlmostEqual(res["H1"], 1.0, places=4)
        self.assertAlmostEqual(res["H2"], 0.8, places=4)

    def test_invalid_taphonomic_factor(self):
        with self.assertRaises(ValueError):
            EquifinalityHorizonCalculator.compute_hypothesis_likelihoods(1.5, {"H1": 10.0})

    def test_kullback_leibler_divergence(self):
        p = [0.5, 0.5]
        q = [0.5, 0.5]
        kl = EquifinalityHorizonCalculator.compute_kullback_leibler_divergence(p, q)
        self.assertAlmostEqual(kl, 0.0, places=5)

    def test_evaluate_equifinality_index(self):
        s1 = [10.0, 5.0, 2.0]
        s2 = [9.0, 5.0, 2.5]
        # At 99% taphonomic loss, signals become nearly indistinguishable
        res = EquifinalityHorizonCalculator.evaluate_equifinality_index(s1, s2, 0.99)
        self.assertGreater(res["equifinality_index"], 0.90)
        self.assertTrue(res["is_empirically_indistinguishable"])


class TestAlgorithmicTransmissionAnalyzer(unittest.TestCase):
    def test_sruti_transmission(self):
        res = AlgorithmicTransmissionAnalyzer.evaluate_transmission_fidelity("sruti", 25, 0.015)
        self.assertGreater(res["cumulative_fidelity"], 0.99)
        self.assertEqual(res["genre"], "sruti")

    def test_smrti_transmission(self):
        res = AlgorithmicTransmissionAnalyzer.evaluate_transmission_fidelity("smrti_itihasa", 25, 0.015)
        self.assertLess(res["cumulative_fidelity"], 0.70)
        self.assertEqual(res["genre"], "smrti_itihasa")

    def test_hadamard_inverse_ill_posedness(self):
        res = AlgorithmicTransmissionAnalyzer.evaluate_hadamard_inverse_ill_posedness(8800, 100000, 2000)
        self.assertTrue(res["is_hadamard_ill_posed"])
        self.assertFalse(res["unique_reconstruction_possible"])
        self.assertGreater(res["expansion_ratio"], 10.0)


class TestCategoryMistakeFormalizer(unittest.TestCase):
    def test_category_mistake_metaphysical_radiocarbon(self):
        res = CategoryMistakeFormalizer.evaluate_proposition_metric_pair("metaphysical", "radiocarbon_dating")
        self.assertTrue(res["is_category_mistake"])
        self.assertIn("Category Mistake", res["classification"])

    def test_valid_historical_epigraphy(self):
        res = CategoryMistakeFormalizer.evaluate_proposition_metric_pair("material_historical", "epigraphic_attestation")
        self.assertFalse(res["is_category_mistake"])
        self.assertEqual(res["classification"], "Epistemically Valid Metric")

    def test_unknown_domain(self):
        with self.assertRaises(ValueError):
            CategoryMistakeFormalizer.evaluate_proposition_metric_pair("non_existent_domain", "metric")


class TestComprehensiveProtocolAuditor(unittest.TestCase):
    def test_compliant_text(self):
        text = "This investigation clarifies what the claim asserts and why it resists empirical adjudication."
        audit = ComprehensiveProtocolAuditor.audit_text(text)
        self.assertTrue(audit["is_compliant"])
        self.assertEqual(len(audit["violations_found"]), 0)

    def test_banned_assertion_raises(self):
        bad_text = "In my conviction, we have proven Krishna was real and definitely existed."
        with self.assertRaises(EpistemicProtocolViolation):
            ComprehensiveProtocolAuditor.audit_text(bad_text)


class TestFullAudit(unittest.TestCase):
    def test_run_full_epistemic_audit(self):
        audit = run_full_epistemic_audit()
        self.assertIn("equifinality_evaluation", audit)
        self.assertIn("algorithmic_transmission", audit)
        self.assertIn("category_mistake_checks", audit)
        self.assertIn("protocol_compliance", audit)
        self.assertTrue(audit["protocol_compliance"]["is_compliant"])


if __name__ == "__main__":
    unittest.main()
