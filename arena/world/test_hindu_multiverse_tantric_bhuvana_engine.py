"""
test_hindu_multiverse_tantric_bhuvana_engine.py

Unit test suite for the Tantric Bhuvana Engine and Pan-Darśana Epistemic Adjudication.
Author: Kepler (A001) - Generation 0 Research Agent
"""

import unittest
from hindu_multiverse_tantric_bhuvana_engine import (
    TantricMultiverseEngine,
    TOTAL_TATTVAS,
    CANONICAL_BHUVANAS,
    ANDA_SPECIFICATION,
    KANCUKAS,
    DARSANA_MULTIVERSE_DATABASE,
)


class TestTantricMultiverseEngine(unittest.TestCase):

    def setUp(self):
        self.engine = TantricMultiverseEngine()

    def test_canonical_bhuvana_and_tattva_sum(self):
        res = self.engine.verify_canonical_bhuvana_sum()
        self.assertEqual(res["total_tattvas"], 36, "Total Tattvas must equal 36")
        self.assertEqual(res["total_bhuvanas"], 224, "Total Bhuvanas must equal 224")
        self.assertTrue(res["is_bhuvana_canonical"])
        self.assertTrue(res["is_tattva_canonical"])

        # Check individual andas
        self.assertEqual(res["breakdown"]["Parthiva_Anda"]["bhuvanas"], 108)
        self.assertEqual(res["breakdown"]["Prakrta_Anda"]["bhuvanas"], 56)
        self.assertEqual(res["breakdown"]["Mayiya_Anda"]["bhuvanas"], 28)
        self.assertEqual(res["breakdown"]["Sakta_Anda"]["bhuvanas"], 32)

    def test_kancuka_entropy_reduction(self):
        res = self.engine.compute_kancuka_entropy_reduction(n_degrees_of_freedom=100)
        self.assertGreater(res["s_unbounded_nats"], res["s_contracted_nats"])
        self.assertLess(res["cumulative_contraction_factor"], 1.0e-5)
        self.assertGreater(res["entropy_reduction_delta"], 0.0)

    def test_pan_darsana_adjudication(self):
        res = self.engine.evaluate_pan_darsana_adjudication()
        self.assertEqual(res["total_schools_evaluated"], 6)
        self.assertEqual(res["strictly_rejects_count"], 1)  # Mīmāṃsā rejects
        self.assertEqual(res["accepts_multiverse_count"], 5)
        self.assertEqual(res["school_verdicts"]["Purva_Mimamsa"], "Rejected")
        self.assertIn("Mīmāṃsā", res["mimamsa_rejection_significance"])

    def test_string_theory_category_error(self):
        res = self.engine.evaluate_string_theory_category_error()
        self.assertTrue(res["violates_protocol"])
        self.assertEqual(len(res["category_differences"]), 4)
        self.assertIn("CATEGORY ERROR", res["verdict"])


if __name__ == "__main__":
    unittest.main()
