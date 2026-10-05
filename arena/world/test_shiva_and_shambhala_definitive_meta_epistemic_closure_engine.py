"""
test_shiva_and_shambhala_definitive_meta_epistemic_closure_engine.py

Unit test suite for Shiva and Shambhala Definitive Meta-Epistemic Closure Engine.
Verifies:
1. Exact facet counts (12 total: 9 empirical, 3 metaphysical).
2. Algorithmic Information Invariance on metaphysical facets (I(D:H) == 0, Joint K(D|H) == K(D)).
3. Classical Pramāṇa-Śāstra mappings across all 6 pramāṇas.
4. Evidentiary conditions: what is established, what remains unknown, what evidence changes mind.
5. Strict protocol safety compliance (zero verdicts on metaphysical facets, zero proof/disproof claims).
"""

import unittest
import math
from shiva_and_shambhala_definitive_meta_epistemic_closure_engine import (
    ShivaAndShambhalaDefinitiveMetaEpistemicClosureEngine,
    EpistemicCategory,
    PramanaType,
    PramanaStatus
)


class TestShivaAndShambhalaDefinitiveMetaEpistemicClosureEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ShivaAndShambhalaDefinitiveMetaEpistemicClosureEngine()

    def test_facet_counts_and_partition(self):
        """Verify 12 total facets correctly partitioned into 9 empirical and 3 metaphysical."""
        audit = self.engine.audit_protocol_compliance()
        self.assertEqual(audit.total_facets, 12)
        self.assertEqual(audit.empirical_facets, 9)
        self.assertEqual(audit.metaphysical_facets, 3)
        self.assertEqual(set(self.engine.get_metaphysical_facet_ids()), {"S3", "S4", "B3"})

    def test_algorithmic_information_invariance(self):
        """
        Verify that metaphysical hypotheses have:
        - 0.0 mutual information with physical data: I(D : H) == 0.0
        - Conditional complexity equals raw data complexity: K(D | H) == K(D)
        - Negative compression gain equal to program overhead: -L(H)
        """
        self.assertTrue(self.engine.verify_algorithmic_invariance_on_metaphysical_facets())
        for fid in ["S3", "S4", "B3"]:
            metric = self.engine.algorithmic_metrics[fid]
            self.assertEqual(metric.algorithmic_mutual_information, 0.0)
            self.assertEqual(metric.joint_complexity_bits, metric.empirical_data_length_bits)
            self.assertEqual(metric.compression_gain_bits, -metric.description_length_bits)

    def test_pramana_mappings_completeness_and_category_errors(self):
        """
        Verify that for S4 (Ground of Being / Prakāśa-Vimarśa), Pratyakṣa and Anumāna
        are marked as INAPPLICABLE_CATEGORY_ERROR because the foundational knower (pramātṛ)
        cannot be an observed object (prameya).
        """
        s4_mapping = self.engine.pramana_mappings["S4"]
        self.assertEqual(s4_mapping.pratyaksa_status, PramanaStatus.INAPPLICABLE_CATEGORY_ERROR)
        self.assertEqual(s4_mapping.anumana_status, PramanaStatus.INAPPLICABLE_CATEGORY_ERROR)
        self.assertEqual(s4_mapping.primary_governing_pramana, PramanaType.ARTHAPATTI)

    def test_pramana_anupalabdhi_for_falsified_empirical_facets(self):
        """
        Verify that B2 (3D Geopolitical Kingdom) and B6 (Hollow Earth)
        have Anupalabdhi (non-perception via reliable instruments) as operative and validating.
        """
        b2_mapping = self.engine.pramana_mappings["B2"]
        b6_mapping = self.engine.pramana_mappings["B6"]
        self.assertEqual(b2_mapping.anupalabdhi_status, PramanaStatus.OPERATIVE_VALID)
        self.assertEqual(b6_mapping.anupalabdhi_status, PramanaStatus.OPERATIVE_VALID)
        self.assertEqual(b2_mapping.primary_governing_pramana, PramanaType.ANUPALABDHI)
        self.assertEqual(b6_mapping.primary_governing_pramana, PramanaType.ANUPALABDHI)

    def test_evidentiary_conditions_completeness(self):
        """Verify that every facet specifies what is established, what remains unknown, and evidence to change mind."""
        for fid, cond in self.engine.evidentiary_conditions.items():
            self.assertTrue(len(cond.established_status) > 10, f"Facet {fid} missing established status.")
            self.assertTrue(len(cond.remaining_unknown) > 10, f"Facet {fid} missing remaining unknown.")
            self.assertTrue(len(cond.positive_evidence_to_change_mind) > 10, f"Facet {fid} missing positive evidence.")
            self.assertTrue(len(cond.negative_evidence_to_change_mind) > 10, f"Facet {fid} missing negative evidence.")
            self.assertTrue(len(cond.resistance_mechanism) > 10, f"Facet {fid} missing resistance mechanism.")

    def test_bayesian_posterior_calculation(self):
        """Verify Bayes factor posterior odds calculation."""
        # When Bayes factor is 1.0 (underdetermined), posterior equals prior
        prior = 0.5
        post = self.engine.calculate_bayes_factor_posterior(prior, 1.0)
        self.assertAlmostEqual(post, 0.5)

        # Extreme positive evidence
        post_strong = self.engine.calculate_bayes_factor_posterior(0.01, 1000.0)
        self.assertGreater(post_strong, 0.9)

    def test_protocol_safety_audit(self):
        """Verify protocol compliance audit passes with zero violations."""
        audit = self.engine.audit_protocol_compliance()
        self.assertTrue(audit.is_fully_compliant)
        self.assertFalse(audit.verdict_asserted)
        self.assertFalse(audit.proof_claimed)
        self.assertFalse(audit.disproof_claimed)
        self.assertFalse(audit.personal_conviction_present)
        self.assertEqual(len(audit.violations), 0)

    def test_summary_generation(self):
        """Verify definitive synthesis summary generation."""
        summary = self.engine.generate_definitive_synthesis_summary()
        self.assertTrue(summary["protocol_audit"]["is_fully_compliant"])
        self.assertEqual(len(summary["algorithmic_bounds"]), 3)
        self.assertEqual(len(summary["pramana_primary_governance"]), 12)


if __name__ == "__main__":
    unittest.main()
