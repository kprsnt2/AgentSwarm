"""
Unit Test Suite for Shiva and Shambhala Epistemic Audit Engine
Author: Kepler (A001, Autonomous Research Agent, Swarm Generation 0)
Workspace: D:\\AgentSwarm\\arena\\world
Date: October 5, 2026
"""

import unittest
import math
from shiva_and_shambhala_epistemic_audit_engine import ShivaShambhalaEpistemicAuditEngine


class TestShivaShambhalaEpistemicAuditEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ShivaShambhalaEpistemicAuditEngine()

    def test_total_facets_and_demarcation(self):
        summary = self.engine.summarize_audit()
        self.assertEqual(summary["total_facets"], 12)
        self.assertEqual(summary["empirical_decidable_facets"], 9)
        self.assertEqual(summary["metaphysical_undecidable_facets"], 3)
        self.assertEqual(summary["verdicts_asserted_on_metaphysical"], 0)

    def test_protocol_compliance_checks(self):
        checks = self.engine.verify_protocol_compliance()
        for check_name, passed in checks.items():
            self.assertTrue(passed, f"Protocol compliance check failed: {check_name}")

    def test_metaphysical_invariance_metrics(self):
        metrics = self.engine.calculate_epistemic_stagnation_metrics()
        self.assertEqual(metrics["metaphysical_total_fisher_info"], 0.0)
        self.assertEqual(metrics["metaphysical_total_info_gain_bits"], 0.0)
        self.assertTrue(metrics["is_empirically_stuck"])

    def test_infinite_cramer_rao_variance(self):
        for fid in ["S3", "S4", "B3"]:
            facet = self.engine.facets[fid]
            self.assertTrue(math.isinf(facet.cramer_rao_variance))
            self.assertEqual(facet.likelihood_ratio, 1.0)
            self.assertEqual(facet.fisher_information, 0.0)
            self.assertFalse(facet.verdict_asserted)

    def test_empirical_refutations_and_corroborations(self):
        # S1 (Human Euhemerism) is refuted
        s1 = self.engine.facets["S1"]
        self.assertLess(s1.likelihood_ratio, 1e-4)

        # B2 (Macroscopic 3D Kingdom) is refuted
        b2 = self.engine.facets["B2"]
        self.assertEqual(b2.likelihood_ratio, 0.0)

        # B6 (Hollow Earth) is refuted
        b6 = self.engine.facets["B6"]
        self.assertEqual(b6.likelihood_ratio, 0.0)

        # S2 and B1 are corroborated
        s2 = self.engine.facets["S2"]
        self.assertGreater(s2.likelihood_ratio, 1e5)
        b1 = self.engine.facets["B1"]
        self.assertGreater(b1.likelihood_ratio, 1e2)

    def test_counterfactual_evidence_definitions(self):
        for fid, facet in self.engine.facets.items():
            self.assertGreater(len(facet.falsifying_or_confirming_evidence), 10)
            self.assertGreater(len(facet.what_remains_unknown), 10)
            self.assertGreater(len(facet.established_finding), 10)


if __name__ == "__main__":
    unittest.main()
