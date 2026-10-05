"""
test_krishna_mahabharata_comparative_and_bayesian_demarcation_engine.py

Unit test suite for krishna_mahabharata_comparative_and_bayesian_demarcation_engine.py
Verifies Bayesian Likelihood Invariance, Duhem-Quine Holism, Comparative Historiographical
Benchmarking, Epistemic Fallacy Auditing, and Swarm Protocol Compliance.
"""

import unittest
from krishna_mahabharata_comparative_and_bayesian_demarcation_engine import (
    BayesianInvarianceEngine,
    DuhemQuineHolismEngine,
    ComparativeHistoriographyEngine,
    EpistemicFallacyDetector,
    InformationChannelTransmissionEngine,
    MasterComparativeAndBayesianFacade
)


class TestComparativeAndBayesianDemarcationEngine(unittest.TestCase):

    def setUp(self):
        self.bayesian = BayesianInvarianceEngine()
        self.duhem_quine = DuhemQuineHolismEngine()
        self.comparative = ComparativeHistoriographyEngine()
        self.fallacy_detector = EpistemicFallacyDetector()
        self.channel = InformationChannelTransmissionEngine()
        self.facade = MasterComparativeAndBayesianFacade()

    def test_bayesian_likelihood_equality(self):
        """Physical observables must have identical likelihood under H_theo and H_nat."""
        evidence_classes = [
            "geo_sediments", "arch_pgw", "iron_bloomery",
            "bio_cremation", "epi_vasudeva", "astro_retrocalc", "carrying_capacity_gap"
        ]
        for ev in evidence_classes:
            l_nat = self.bayesian.compute_likelihood(ev, "H_nat")
            l_theo = self.bayesian.compute_likelihood(ev, "H_theo")
            self.assertEqual(l_nat, l_theo, f"Likelihood mismatch for {ev}")
            bf = self.bayesian.compute_bayes_factor(ev, "H_theo", "H_nat")
            self.assertAlmostEqual(bf, 1.0, places=7, msg=f"Bayes factor must be 1.0 for {ev}")

    def test_bayesian_prior_conservation(self):
        """Any prior odds must remain strictly unchanged upon observing empirical physical data."""
        priors = [0.001, 0.10, 0.33, 0.50, 0.67, 0.90, 0.999]
        evidence_classes = ["geo_sediments", "arch_pgw", "iron_bloomery", "bio_cremation", "epi_vasudeva"]
        self.assertTrue(self.bayesian.verify_prior_conservation(priors, evidence_classes))

    def test_information_gain_zero(self):
        """Information gain (KL divergence) must be exactly 0.0 bits."""
        prior_odds = 1.0  # P = 0.5
        evidence_classes = ["geo_sediments", "arch_pgw", "iron_bloomery", "epi_vasudeva"]
        post_odds, cum_bf, kl_div = self.bayesian.bayesian_update(prior_odds, evidence_classes)
        self.assertEqual(post_odds, 1.0)
        self.assertEqual(cum_bf, 1.0)
        self.assertAlmostEqual(kl_div, 0.0, places=9)

    def test_duhem_quine_evaluations(self):
        """Audit auxiliary hypotheses insulating core from naive empirical falsifications."""
        discrepancies = [
            "absence_of_3_94m_skeletons",
            "absence_of_nuclear_radiation",
            "absence_of_3102_bce_planetary_conjunction"
        ]
        for d in discrepancies:
            res = self.duhem_quine.evaluate_holistic_immunity(d)
            self.assertFalse(res["core_theory_isolated"])
            self.assertGreaterEqual(res["num_auxiliary_hypotheses"], 2)
            self.assertGreaterEqual(res["max_auxiliary_plausibility"], 0.90)

    def test_comparative_historiography_traditions(self):
        """Verify presence and attributes of all 7 foundational comparative benchmark traditions."""
        expected_keys = [
            "Krishna_Mahabharata", "King_Arthur", "Moses_Exodus",
            "Trojan_War", "Epic_of_Gilgamesh", "Jesus_of_Nazareth", "Gautama_Buddha"
        ]
        for key in expected_keys:
            t = self.comparative.get_tradition_comparison(key)
            self.assertIn("tradition", t)
            self.assertIn("archaeological_match_score", t)
            self.assertIn("transmission_gap_years", t)
            self.assertIn("external_epigraphic_corroboration", t)
            self.assertIn("metaphysical_core_present", t)

    def test_comparative_invariant_finding(self):
        """Every benchmark tradition contains an empirical core and a metaphysical component."""
        summary = self.comparative.compute_comparative_summary()
        self.assertEqual(summary["total_traditions_analyzed"], 7)
        self.assertEqual(summary["traditions_with_metaphysical_core"], 7)
        self.assertGreaterEqual(summary["traditions_with_epigraphic_corroboration"], 6)
        self.assertGreater(summary["average_archaeological_match_score"], 0.70)

    def test_epistemic_fallacy_detection_violation_catching(self):
        """Fallacy detector must catch illegitimate verdicts on metaphysical propositions."""
        violating_stance = [
            {
                "type": "metaphysical",
                "text": "Lord Krishna proven to be God via archaeological excavations",
                "verdict": "PROVEN"
            },
            {
                "type": "empirical",
                "text": "Brahmastra was a literal nuclear bomb",
                "verdict": "PROVEN"
            },
            {
                "type": "empirical",
                "text": "Krishna was entirely fabricated with zero historical core",
                "verdict": "MYTH"
            }
        ]
        audit = self.fallacy_detector.audit_swarm_stance(violating_stance)
        self.assertFalse(audit["protocol_compliant"])
        self.assertEqual(audit["total_fallacy_violations"], 3)

    def test_epistemic_fallacy_detection_compliant(self):
        """Fallacy detector must pass a strictly compliant epistemic stance."""
        compliant_stance = [
            {
                "type": "empirical",
                "text": "PGW layers at Hastinapur show catastrophic flood c. 850 BCE",
                "verdict": "CORROBORATED"
            },
            {
                "type": "metaphysical",
                "text": "Lord Krishna as Svayam Bhagavan",
                "verdict": "EMPIRICALLY_UNDECIDABLE"
            }
        ]
        audit = self.fallacy_detector.audit_swarm_stance(compliant_stance)
        self.assertTrue(audit["protocol_compliant"])
        self.assertEqual(audit["total_fallacy_violations"], 0)

    def test_information_transmission_channel(self):
        """Structured metrical transmission preserves plot topology far better than rumors."""
        anustubh = self.channel.compute_transmission_fidelity("vedic_anustubh_recitation")
        rumor = self.channel.compute_transmission_fidelity("unstructured_prose_rumor")
        self.assertGreater(anustubh["topological_narrative_retention_pct"], 90.0)
        self.assertLess(rumor["topological_narrative_retention_pct"], 1.0)

    def test_master_facade_comprehensive_audit(self):
        """End-to-end facade execution must be strictly compliant."""
        audit_res = self.facade.run_comprehensive_audit()
        self.assertTrue(audit_res["bayesian_prior_conservation_verified"])
        self.assertEqual(len(audit_res["duhem_quine_evaluations"]), 3)
        self.assertTrue(audit_res["fallacy_audit"]["protocol_compliant"])
        self.assertEqual(audit_res["swarm_protocol_status"], "STRICTLY_COMPLIANT_ZERO_VERDICTS_ON_METAPHYSICAL_CORES")


if __name__ == "__main__":
    unittest.main()
