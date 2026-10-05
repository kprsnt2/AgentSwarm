"""
test_shiva_shambhala_epistemic_limits_engine.py
================================================
Unit tests verifying the EpistemicLimitsEngine implementation.
Ensures zero protocol violations, exact mathematical bounds, and adherence to scientific brief.
"""

import unittest
import math
from shiva_shambhala_epistemic_limits_engine import EpistemicLimitsEngine


class TestEpistemicLimitsEngine(unittest.TestCase):

    def setUp(self):
        self.engine = EpistemicLimitsEngine()

    def test_facet_decomposition_and_count(self):
        """Verify exactly 12 facets: 6 Shiva (S1-S6) and 6 Shambhala (B1-B6)."""
        facets = self.engine.facets
        self.assertEqual(len(facets), 12)
        shiva_keys = [f"S{i}" for i in range(1, 7)]
        shambhala_keys = [f"B{i}" for i in range(1, 7)]
        for k in shiva_keys:
            self.assertIn(k, facets)
            self.assertEqual(facets[k]["subject"], "Lord Shiva")
        for k in shambhala_keys:
            self.assertIn(k, facets)
            self.assertEqual(facets[k]["subject"], "Shambhala")

    def test_metaphysical_demarcation_and_invariants(self):
        """Verify exactly 3 metaphysical facets (S3, S4, B3) with zero verdicts and infinite bounds."""
        metaphysical_keys = ["S3", "S4", "B3"]
        for k in metaphysical_keys:
            facet = self.engine.facets[k]
            self.assertTrue(facet["is_metaphysical"])
            self.assertEqual(facet["status"], "Undecidable (Metaphysical Boundary)")
            self.assertEqual(facet["bayes_factor_threshold"], math.inf)
            self.assertEqual(self.engine.calculate_likelihood_ratio(k), 1.0)
            self.assertEqual(self.engine.calculate_fisher_information(k), 0.0)
            self.assertEqual(self.engine.calculate_cramer_rao_variance_bound(k), math.inf)
            self.assertEqual(self.engine.calculate_algorithmic_mutual_information(k), 0.0)
            self.assertEqual(self.engine.calculate_transduction_cross_section(k), 0.0)

    def test_decidable_facets_classification(self):
        """Verify 9 decidable facets: 3 refuted and 6 corroborated."""
        facets = self.engine.facets
        decidable = [k for k, v in facets.items() if not v["is_metaphysical"]]
        self.assertEqual(len(decidable), 9)

        refuted = [k for k, v in facets.items() if v["status"] == "Decidable & Refuted"]
        self.assertEqual(set(refuted), {"S1", "B2", "B6"})

        corroborated = [k for k, v in facets.items() if v["status"] == "Decidable & Corroborated"]
        self.assertEqual(set(corroborated), {"S2", "S5", "S6", "B1", "B4", "B5"})

    def test_geodetic_and_epigraphic_metrics(self):
        """Verify epigraphic arc calculations across Eurasia."""
        arc = self.engine.get_shiva_epigraphic_arc()
        self.assertGreater(arc["aihole_to_myson_km"], 3400.0)
        self.assertLess(arc["aihole_to_myson_km"], 3600.0)
        self.assertGreater(arc["kedarnath_to_prambanan_km"], 5100.0)
        self.assertLess(arc["kedarnath_to_prambanan_km"], 5500.0)
        self.assertEqual(len(arc["languages"]), 5)

    def test_geophysical_hollow_earth_refutation(self):
        """Verify moment of inertia and seismic constraints on hollow Earth."""
        geo = self.engine.evaluate_geophysical_hollow_earth()
        self.assertAlmostEqual(geo["observed_moment_of_inertia"], 0.3307, places=4)
        self.assertAlmostEqual(geo["hollow_shell_moment_of_inertia"], 0.6667, places=4)
        self.assertGreater(geo["relative_discrepancy_percent"], 50.0)
        self.assertEqual(geo["mantle_shear_wave_velocity_kms"], [3.2, 7.3])

    def test_protocol_compliance_audit(self):
        """Ensure full compliance with the Metaphysical brief and absence of protocol violations."""
        audit = self.engine.verify_protocol_compliance()
        self.assertTrue(audit["metaphysical_facet_count_correct"])
        self.assertTrue(audit["status_strictly_undecidable"])
        self.assertTrue(audit["fisher_information_zero"])
        self.assertTrue(audit["likelihood_ratio_unity"])
        self.assertTrue(audit["zero_metaphysical_verdicts"])
        self.assertTrue(audit["protocol_fully_compliant"])


if __name__ == "__main__":
    unittest.main()
