"""
test_krishna_mahabharata_formal_demarcation_and_modal_engine.py
===============================================================
Comprehensive test suite verifying:
1. Ontological facet initialization and classification (K1-K5, M1-M5)
2. Carnapian framework internal vs external analysis
3. Modal logic S5 evaluation and instrument boundedness
4. Information-theoretic bounds (Fisher Information I(theta) = 0, Cramer-Rao variance = infinity)
5. Category-theoretic mapping and non-invertibility of forgetful functor
6. Akshauhini logistical carrying capacity and demographic impossibility
7. Strict protocol compliance: Zero metaphysical verdicts asserted, zero proof/disproof claims.
"""

import unittest
import math
from krishna_mahabharata_formal_demarcation_and_modal_engine import (
    KrishnaMahabharataFormalDemarcationEngine,
    OntologicalFacet,
)


class TestKrishnaMahabharataFormalDemarcationEngine(unittest.TestCase):

    def setUp(self):
        self.engine = KrishnaMahabharataFormalDemarcationEngine()

    def test_facets_initialization_count_and_keys(self):
        facets = self.engine.facets
        self.assertEqual(len(facets), 10)
        expected_keys = ["K1", "K2", "K3", "K4", "K5", "M1", "M2", "M3", "M4", "M5"]
        for key in expected_keys:
            self.assertIn(key, facets)

    def test_metaphysical_facets_classification(self):
        metaphysical_keys = ["K3", "K4", "K5", "M5"]
        for key in metaphysical_keys:
            facet = self.engine.facets[key]
            self.assertTrue(facet.is_metaphysical, f"Facet {key} should be classified as metaphysical")
            self.assertIn("VERDICT PROHIBITED", facet.verdict)
            self.assertIn("Empirically Undecidable", facet.verdict)

    def test_empirical_facets_classification(self):
        empirical_keys = ["K1", "K2", "M1", "M2", "M3", "M4"]
        for key in empirical_keys:
            facet = self.engine.facets[key]
            self.assertFalse(facet.is_metaphysical, f"Facet {key} should be classified as empirical")
            self.assertNotIn("VERDICT PROHIBITED", facet.verdict)

    def test_carnapian_framework_analysis(self):
        internal_res = self.engine.analyze_carnapian_framework("Did Krishna reveal the Visvarupa within the Mahabharata?")
        self.assertEqual(internal_res["question_type"], "Internal Framework Question")
        self.assertTrue(internal_res["verdict_permitted"])

        external_res = self.engine.analyze_carnapian_framework("Is Lord Krishna real in physical reality?")
        self.assertEqual(external_res["question_type"], "External Theoretical Question")
        self.assertFalse(external_res["verdict_permitted"])

    def test_modal_s5_evaluation(self):
        modal_res = self.engine.evaluate_modal_s5()
        self.assertTrue(modal_res["box_empirical_instrument_limitation"])
        self.assertTrue(modal_res["diamond_historical_chieftain"])
        self.assertFalse(modal_res["box_historical_chieftain"])
        self.assertTrue(modal_res["p2_metaphysical_contingency"])

    def test_fisher_information_and_cramer_rao(self):
        info_res = self.engine.compute_fisher_information_and_cramer_rao(observations_count=5000)
        self.assertEqual(info_res["fisher_information"], 0.0)
        self.assertEqual(info_res["cramer_rao_lower_bound_variance"], float("inf"))
        self.assertEqual(info_res["mutual_information_shannon"], 0.0)

    def test_category_theoretic_mapping(self):
        cat_res = self.engine.evaluate_category_theoretic_mapping()
        self.assertTrue(cat_res["forgetful_functor_lossy"])
        self.assertEqual(cat_res["free_functor_fiber_cardinality"], float("inf"))
        self.assertFalse(cat_res["is_isomorphism"])

    def test_akshauhini_logistics_quantities(self):
        logistics = self.engine.calculate_akshauhini_logistics()
        self.assertEqual(logistics["literal_men"], 3936600)
        self.assertEqual(logistics["literal_elephants"], 393660)
        self.assertGreater(logistics["water_stress_ratio"], 1.0)
        self.assertGreater(logistics["demographic_impossibility_factor"], 5.0)

    def test_protocol_compliance_audit(self):
        audit = self.engine.audit_protocol_compliance()
        self.assertTrue(audit["audit_passed"])
        self.assertEqual(audit["protocol_violations_count"], 0)
        self.assertEqual(audit["metaphysical_facets_count"], 4)
        self.assertEqual(audit["empirical_facets_count"], 6)

    def test_facet_export_to_dict(self):
        k1 = self.engine.facets["K1"]
        d = k1.to_dict()
        self.assertEqual(d["facet_id"], "K1")
        self.assertEqual(d["subject"], "Lord Krishna")
        self.assertIn("positive_evidence_criterion", d)
        self.assertIn("negative_evidence_criterion", d)


if __name__ == "__main__":
    unittest.main()
