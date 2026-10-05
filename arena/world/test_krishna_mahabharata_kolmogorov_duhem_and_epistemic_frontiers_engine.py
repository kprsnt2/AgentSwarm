"""
Unit tests for krishna_mahabharata_kolmogorov_duhem_and_epistemic_frontiers_engine.py.
Verifies Kolmogorov complexity bounds, Duhem-Quine holism, pramāṇa applicability,
comparative benchmarks, and protocol safety firewall.
"""

import unittest
from krishna_mahabharata_kolmogorov_duhem_and_epistemic_frontiers_engine import (
    KolmogorovComplexityDemarcator,
    DuhemQuineHolismAnalyzer,
    MultiValuedEpistemicLogic,
    ComparativeGlobalEpistemicBenchmark,
    SwarmEpistemicFirewall,
    EpistemicProtocolViolation,
    run_full_epistemic_audit,
)


class TestKolmogorovDuhemEngine(unittest.TestCase):

    def test_kolmogorov_model_complexity(self):
        k_hist = KolmogorovComplexityDemarcator.compute_model_complexity("naturalistic_chieftain", num_parameters=10)
        k_meta = KolmogorovComplexityDemarcator.compute_model_complexity("metaphysical_avatar", num_parameters=10)
        # Metaphysical model has larger ontology overhead (1024 vs 256)
        self.assertGreater(k_meta, k_hist)
        self.assertEqual(k_hist, 10 * 16 + 256.0)
        self.assertEqual(k_meta, 10 * 16 + 1024.0)

    def test_kolmogorov_data_log_loss(self):
        loss_90 = KolmogorovComplexityDemarcator.compute_data_log_loss(0.90)
        self.assertAlmostEqual(loss_90, 0.152, places=3)
        with self.assertRaises(ValueError):
            KolmogorovComplexityDemarcator.compute_data_log_loss(0.0)
        with self.assertRaises(ValueError):
            KolmogorovComplexityDemarcator.compute_data_log_loss(1.5)

    def test_mdl_evaluation(self):
        mdl = KolmogorovComplexityDemarcator.evaluate_mdl(400.0, 0.8)
        self.assertIn("model_complexity_bits", mdl)
        self.assertIn("data_loss_bits", mdl)
        self.assertIn("total_mdl_bits", mdl)
        self.assertEqual(mdl["model_complexity_bits"], 400.0)

    def test_duhem_quine_holism(self):
        aux = ["A1: Kenosis", "A2: Divya-caksu vision", "A3: Textual accretion"]
        res_refuted = DuhemQuineHolismAnalyzer.evaluate_conjunction(
            "HardCore: Svayam Bhagavan", aux, empirical_anomaly_observed=True
        )
        self.assertTrue(res_refuted["conjunction_refuted"])
        self.assertFalse(res_refuted["hard_core_isolated_refuted"])
        self.assertEqual(res_refuted["degrees_of_freedom_for_protective_adjustment"], 3)

        res_clean = DuhemQuineHolismAnalyzer.evaluate_conjunction(
            "HardCore: Svayam Bhagavan", aux, empirical_anomaly_observed=False
        )
        self.assertFalse(res_clean["conjunction_refuted"])
        self.assertEqual(res_clean["degrees_of_freedom_for_protective_adjustment"], 0)

    def test_multi_valued_epistemic_logic(self):
        p1 = MultiValuedEpistemicLogic.evaluate_proposition("P1_historical_chieftain")
        p2 = MultiValuedEpistemicLogic.evaluate_proposition("P2_demographic_hyperbole")
        p3 = MultiValuedEpistemicLogic.evaluate_proposition("P3_transcendent_avatar")
        p4 = MultiValuedEpistemicLogic.evaluate_proposition("P4_dharmic_teleology")

        self.assertEqual(p1["truth_value"], "T")
        self.assertEqual(p2["truth_value"], "F")
        self.assertEqual(p3["truth_value"], "U")
        self.assertEqual(p4["truth_value"], "U")

    def test_pramana_applicability(self):
        pratyaksa = MultiValuedEpistemicLogic.audit_pramana_applicability("pratyaksa")
        anumana = MultiValuedEpistemicLogic.audit_pramana_applicability("anumana")
        upamana = MultiValuedEpistemicLogic.audit_pramana_applicability("upamana")
        sabda = MultiValuedEpistemicLogic.audit_pramana_applicability("sabda")

        self.assertFalse(pratyaksa["valid_for_transcendent_godhead"])
        self.assertFalse(anumana["valid_for_transcendent_godhead"])
        self.assertFalse(upamana["valid_for_transcendent_godhead"])
        self.assertTrue(sabda["valid_for_transcendent_godhead"])
        self.assertFalse(sabda["valid_for_spatiotemporal_artifacts"])

    def test_comparative_global_benchmarks(self):
        benchmarks = ComparativeGlobalEpistemicBenchmark.get_benchmark_table()
        self.assertEqual(len(benchmarks), 5)
        for b in benchmarks:
            self.assertEqual(b["likelihood_ratio_metaphysical"], 1.0)
            self.assertIn("historical_core", b)
            self.assertIn("epic_hyperbole", b)
            self.assertIn("metaphysical_core", b)

    def test_swarm_firewall_blocks_forbidden_verdicts(self):
        forbidden_cases = [
            "We have proven true that Krishna is divine.",
            "Science has disproven the existence of God.",
            "It is definitely proven that Mahabharata was pure myth.",
            "Krishna is definitely real as God in the physical universe.",
        ]
        for statement in forbidden_cases:
            with self.assertRaises(EpistemicProtocolViolation):
                SwarmEpistemicFirewall.audit_assertion(statement)

    def test_swarm_firewall_permits_objective_demarcation(self):
        valid_statements = [
            "Proposition P1 is empirically corroborated by PGW archaeology.",
            "Proposition P2 is falsified by demographic carrying capacity bounds.",
            "The claim of divine incarnation is strictly not empirically decidable.",
            "Methodological naturalism remains neutral on transcendent ontology.",
        ]
        for statement in valid_statements:
            self.assertTrue(SwarmEpistemicFirewall.audit_assertion(statement))

    def test_full_pipeline_audit(self):
        res = run_full_epistemic_audit()
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(res["firewall_passed"])
        self.assertGreater(res["kolmogorov_complexity_gap_bits"], 0.0)
        self.assertTrue(res["all_benchmarks_likelihood_ratio_unity"])


if __name__ == "__main__":
    unittest.main()
