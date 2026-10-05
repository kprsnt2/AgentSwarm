"""
test_shiva_and_shambhala_epistemic_horizon_engine.py

Unit test suite for Shiva and Shambhala Epistemic Horizon Engine.
Verifies:
1. Exact facet partition: 12 facets total (9 empirical, 3 metaphysical).
2. Protocol compliance audit: zero verdicts, zero proof/disproof claims.
3. Mathematical metrics for metaphysical facets:
   - Likelihood ratio == 1.0
   - Fisher Information == 0.0
   - Cramér-Rao lower bound == inf
   - Algorithmic Mutual Information == 0.0 bits
   - Kullback-Leibler divergence == 0.0 nats
4. Pramāṇa matrix mappings and category error detection.
5. Tripartite evidentiary disclosures across all facets.
"""

import unittest
import math
from shiva_and_shambhala_epistemic_horizon_engine import (
    ShivaAndShambhalaEpistemicHorizonEngine,
    EpistemicClass,
    PramanaType,
    PramanaOperation
)


class TestShivaAndShambhalaEpistemicHorizonEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ShivaAndShambhalaEpistemicHorizonEngine()

    def test_facet_counts_and_demarcation(self):
        """Verify 12 total facets correctly partitioned into 9 empirical and 3 metaphysical."""
        audit = self.engine.audit_protocol_compliance()
        self.assertEqual(audit.total_facets, 12)
        self.assertEqual(audit.empirical_facets, 9)
        self.assertEqual(audit.metaphysical_facets, 3)
        self.assertEqual(set(self.engine.get_metaphysical_facet_ids()), {"S3", "S4", "B3"})

    def test_protocol_compliance_invariants(self):
        """Verify strict adherence to scientific brief: zero verdicts, zero proofs/disproofs."""
        audit = self.engine.audit_protocol_compliance()
        self.assertTrue(audit.is_compliant)
        self.assertFalse(audit.verdict_asserted)
        self.assertFalse(audit.proof_claimed)
        self.assertFalse(audit.disproof_claimed)
        self.assertFalse(audit.personal_conviction_present)

    def test_metaphysical_invariance_metrics(self):
        """
        Verify that core metaphysical facets (S3, S4, B3) exhibit:
        - Likelihood ratio LR == 1.0 (no evidence differential)
        - Fisher Information I_F == 0.0 (no parameter sensitivity)
        - Cramér-Rao Bound == inf (unbounded estimation variance)
        - Algorithmic Mutual Information I(D:H) == 0.0 bits
        - Kullback-Leibler Divergence D_KL == 0.0 nats
        """
        for fid in ["S3", "S4", "B3"]:
            m = self.engine.metrics[fid]
            self.assertEqual(m.likelihood_ratio, 1.0)
            self.assertEqual(m.fisher_information, 0.0)
            self.assertTrue(math.isinf(m.cramer_rao_lower_bound))
            self.assertEqual(m.algorithmic_mutual_info_bits, 0.0)
            self.assertEqual(m.kullback_leibler_divergence, 0.0)
            self.assertLess(m.net_compression_gain_bits, 0.0)

    def test_pramana_category_errors(self):
        """
        Verify that for metaphysical facets, Pratyakṣa (sensory perception) is
        marked as INAPPLICABLE_CATEGORY_ERROR because the knower/unconditioned reality
        cannot be an observed sensory object.
        """
        for fid in ["S3", "S4", "B3"]:
            op = self.engine.pramana_matrix[fid][PramanaType.PRATYAKSA]
            self.assertEqual(op, PramanaOperation.INAPPLICABLE_CATEGORY_ERROR)

    def test_falsified_empirical_facets_anupalabdhi(self):
        """
        Verify that physical 3D kingdom (B2) and Hollow Earth (B6) have Anupalabdhi
        (valid non-perception) as operative corroborating the absence.
        """
        self.assertEqual(
            self.engine.pramana_matrix["B2"][PramanaType.ANUPALABDHI],
            PramanaOperation.OPERATIVE_CORROBORATING
        )
        self.assertEqual(
            self.engine.pramana_matrix["B6"][PramanaType.ANUPALABDHI],
            PramanaOperation.OPERATIVE_CORROBORATING
        )

    def test_evidentiary_disclosures_completeness(self):
        """Verify that every facet has non-trivial tripartite disclosures."""
        for fid, facet in self.engine.facets.items():
            self.assertTrue(len(facet.what_is_established) > 15, f"{fid} established missing")
            self.assertTrue(len(facet.what_remains_unknown) > 15, f"{fid} unknown missing")
            self.assertTrue(len(facet.evidence_to_change_mind) > 15, f"{fid} evidence missing")
            self.assertTrue(len(facet.resistance_mechanism) > 15, f"{fid} resistance missing")

    def test_bayes_factor_calculation(self):
        """Verify posterior calculation from prior and Bayes factor."""
        # Uninformative / underdetermined
        self.assertAlmostEqual(self.engine.calculate_posterior_odds(0.5, 1.0), 0.5)
        # Infinite Bayes factor gives 1.0
        self.assertEqual(self.engine.calculate_posterior_odds(0.01, float('inf')), 1.0)
        # Moderate update
        post = self.engine.calculate_posterior_odds(0.1, 9.0)
        self.assertAlmostEqual(post, 0.5)


if __name__ == '__main__':
    unittest.main()
