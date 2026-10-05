"""
Unit tests for Epistemic Demarcation Engine (Shiva and Shambhala).

Validates:
- Epistemic firewall integrity (zero verdicts on metaphysical hypotheses).
- Mathematical formalization of resistance to testing (Fisher info, Likelihood ratio, KL divergence).
- Geodetic and geophysical calculations.
"""

import unittest
import math
from epistemic_demarcation_shiva_shambhala_engine import (
    EpistemicDemarcationEngine,
    haversine_distance_km,
    analyze,
)


class TestEpistemicDemarcationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EpistemicDemarcationEngine()

    def test_haversine_distance_calculation(self):
        # Aihole to My Son distance check
        aihole = self.engine.coordinates["aihole_karnataka"]
        my_son = self.engine.coordinates["my_son_vietnam"]
        d = haversine_distance_km(aihole[0], aihole[1], my_son[0], my_son[1])
        self.assertGreater(d, 3400.0)
        self.assertLess(d, 3600.0)

    def test_epigraphic_span_computation(self):
        span = self.engine.compute_epigraphic_span()
        self.assertIn("aihole_to_my_son_km", span)
        self.assertIn("kedarnath_to_prambanan_km", span)
        self.assertIn("cumulative_network_span_km", span)
        self.assertGreater(span["cumulative_network_span_km"], 6000.0)

    def test_geophysical_planetary_bounds(self):
        geo = self.engine.planetary_structure_bounds()
        self.assertEqual(geo["earth_normalized_moi_factor"], 0.3307)
        self.assertTrue(geo["hollow_shell_refuted"])
        self.assertLess(geo["earth_normalized_moi_factor"], geo["uniform_density_sphere_factor"])

    def test_metaphysical_resistance_formalism(self):
        metrics = self.engine.metaphysical_resistance_metrics()
        self.assertEqual(metrics["likelihood_ratio"], 1.0)
        self.assertEqual(metrics["delta_log_posterior_odds"], 0.0)
        self.assertEqual(metrics["kl_divergence_nats"], 0.0)
        self.assertEqual(metrics["fisher_information"], 0.0)
        self.assertTrue(math.isinf(metrics["cramer_rao_variance_bound"]))
        self.assertEqual(metrics["algorithmic_mutual_info_bits"], 0.0)
        self.assertTrue(metrics["resists_empirical_testing"])

    def test_facet_taxonomy_structure(self):
        facets = self.engine.get_facet_taxonomy()
        self.assertEqual(len(facets), 12)
        shiva_facets = [f for f in facets if f["subject"] == "Shiva"]
        shambhala_facets = [f for f in facets if f["subject"] == "Shambhala"]
        self.assertEqual(len(shiva_facets), 6)
        self.assertEqual(len(shambhala_facets), 6)

        # Check required fields
        required_keys = {
            "facet_id", "subject", "facet_name", "epistemic_class",
            "status", "established", "unknown", "reversal_evidence",
            "reversal_bayes_factor", "is_empirically_decidable", "verdict_asserted"
        }
        for f in facets:
            self.assertTrue(required_keys.issubset(f.keys()))

    def test_epistemic_firewall_audit(self):
        audit = self.engine.audit_epistemic_firewall()
        self.assertEqual(audit["total_facets"], 12)
        self.assertEqual(audit["metaphysical_facet_count"], 3)
        self.assertFalse(audit["verdicts_asserted_on_metaphysical"])
        self.assertTrue(audit["firewall_intact"])

    def test_top_level_analyze(self):
        result = analyze()
        self.assertEqual(result["domain"], "what-about-lord-shiva-and")
        self.assertIn("taxonomy", result)
        self.assertIn("epigraphic_span", result)
        self.assertIn("geophysical_bounds", result)
        self.assertIn("resistance_formalism", result)
        self.assertIn("epistemic_audit", result)
        self.assertTrue(result["epistemic_audit"]["firewall_intact"])


if __name__ == "__main__":
    unittest.main()
