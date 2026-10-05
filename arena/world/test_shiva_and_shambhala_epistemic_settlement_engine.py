"""
Unit tests for ShivaShambhalaEpistemicSettlementEngine.
Verifies epistemic demarcation, mathematical limits, protocol compliance, and stagnation proofs.
"""

import unittest
import math
from shiva_and_shambhala_epistemic_settlement_engine import (
    ShivaShambhalaEpistemicSettlementEngine,
    haversine_distance_km
)


class TestShivaShambhalaEpistemicSettlementEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ShivaShambhalaEpistemicSettlementEngine()

    def test_haversine_distance_accuracy(self):
        # Aihole to My Son should be ~3444 km
        d = haversine_distance_km(16.0219, 75.8824, 15.7989, 108.1244)
        self.assertAlmostEqual(d, 3444.38, delta=10.0)

    def test_epigraphic_metrics(self):
        metrics = self.engine.get_epigraphic_network_metrics()
        self.assertGreater(metrics["cumulative_network_span_km"], 9000.0)
        self.assertEqual(len(metrics["languages_attested"]), 5)
        self.assertEqual(metrics["chronological_depth_years"], 3500)

    def test_geophysical_interior_bounds(self):
        geo = self.engine.get_geophysical_interior_bounds()
        self.assertEqual(geo["observed_normalized_moi"], 0.3307)
        self.assertTrue(geo["hollow_earth_falsified"])
        self.assertEqual(geo["hollow_earth_p_value"], 0.0)

    def test_twelve_facets_demarcation(self):
        facets = self.engine.get_twelve_facets_demarcation()
        self.assertEqual(len(facets), 12)
        shiva_facets = [f for f in facets if f["subject"] == "Lord Shiva"]
        shambhala_facets = [f for f in facets if f["subject"] == "Shambhala"]
        self.assertEqual(len(shiva_facets), 6)
        self.assertEqual(len(shambhala_facets), 6)

        metaphysical = [f for f in facets if f["is_metaphysical"]]
        self.assertEqual(len(metaphysical), 3)

        # Inviolable rule: Zero verdicts asserted on metaphysical claims
        for f in metaphysical:
            self.assertFalse(f["verdict_asserted"])
            self.assertIn("Empirically Undecidable", f["epistemic_status"])
            self.assertEqual(f["required_bayes_factor"], float("inf"))

    def test_epistemic_stagnation_and_halt_proof(self):
        halt = self.engine.formalize_epistemic_stagnation_and_halt()
        self.assertEqual(halt["likelihood_ratio"], 1.0)
        self.assertEqual(halt["delta_log_odds"], 0.0)
        self.assertEqual(halt["log_likelihood_gradient"], 0.0)
        self.assertEqual(halt["fisher_information"], 0.0)
        self.assertEqual(halt["cramer_rao_lower_bound"], float("inf"))
        self.assertEqual(halt["shannon_mutual_information_bits"], 0.0)
        self.assertTrue(halt["epistemic_halt_mandatory"])
        self.assertIn("boundary_type", halt["where_we_are_stuck"])
        self.assertIn("Pramātṛ-Prameya Bheda", halt["where_we_are_stuck"]["boundary_type"])

    def test_protocol_compliance_verification(self):
        compliance = self.engine.verify_protocol_compliance()
        self.assertTrue(compliance["protocol_compliant"])
        self.assertFalse(compliance["any_metaphysical_verdict_asserted"])
        self.assertTrue(compliance["all_metaphysical_facets_undecidable"])
        self.assertTrue(compliance["fisher_info_nullity_verified"])
        self.assertTrue(compliance["cramer_rao_divergence_verified"])
        self.assertTrue(compliance["stagnation_honestly_declared"])


if __name__ == "__main__":
    unittest.main()
