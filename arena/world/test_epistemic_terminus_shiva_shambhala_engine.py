"""
Unit tests for the Epistemic Terminus Engine.
Verifies all mathematical, geodetic, geophysical, and protocol-compliance bounds.
"""

import unittest
import math
from epistemic_terminus_shiva_shambhala_engine import (
    EpistemicTerminusEngine,
    haversine_distance_km,
)


class TestEpistemicTerminusEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EpistemicTerminusEngine()

    def test_haversine_distance(self):
        # Aihole to My Son distance check
        aihole = (16.0219, 75.8824)
        my_son = (15.7989, 108.1244)
        dist = haversine_distance_km(aihole[0], aihole[1], my_son[0], my_son[1])
        self.assertGreater(dist, 3400.0)
        self.assertLess(dist, 3500.0)

    def test_epigraphic_arc_metrics(self):
        arc = self.engine.compute_epigraphic_arc()
        self.assertIn("aihole_to_my_son_km", arc)
        self.assertIn("kedarnath_to_prambanan_km", arc)
        self.assertIn("cumulative_network_span_km", arc)
        self.assertGreater(arc["cumulative_network_span_km"], 6000.0)

    def test_planetary_interior_geophysics(self):
        geo = self.engine.planetary_interior_geophysics()
        self.assertEqual(geo["observed_normalized_moi"], 0.3307)
        self.assertTrue(geo["hollow_shell_excluded"])
        self.assertGreater(geo["mantle_shear_wave_velocity_range_kms"][1], 7.0)

    def test_proof_of_epistemic_halt(self):
        proof = self.engine.proof_of_epistemic_halt()
        self.assertEqual(proof["likelihood_ratio"], 1.0)
        self.assertEqual(proof["log_likelihood_gradient"], 0.0)
        self.assertEqual(proof["fisher_information"], 0.0)
        self.assertEqual(proof["cramer_rao_lower_bound"], float("inf"))
        self.assertEqual(proof["shannon_mutual_information_bits"], 0.0)
        self.assertEqual(proof["empirical_information_gain"], 0.0)
        self.assertTrue(proof["epistemic_halt_mandatory"])

    def test_facet_audit_and_protocol_compliance(self):
        audit = self.engine.audit_all_twelve_facets()
        self.assertEqual(audit["total_facets"], 12)
        self.assertEqual(audit["empirical_and_hermeneutic_facets"], 9)
        self.assertEqual(audit["metaphysical_facets"], 3)
        self.assertFalse(audit["any_verdict_asserted"])
        self.assertTrue(audit["protocol_compliant"])

    def test_terminal_epistemic_declaration(self):
        decl = self.engine.terminal_epistemic_declaration()
        self.assertIn("what_is_established", decl)
        self.assertIn("what_remains_unknown", decl)
        self.assertIn("what_would_change_mind", decl)
        self.assertIn("where_we_are_stuck", decl)
        self.assertIn("S3_Ishvara", decl["what_would_change_mind"])
        self.assertIn("S4_Consciousness", decl["what_would_change_mind"])
        self.assertIn("B3_Pure_Land", decl["what_would_change_mind"])


if __name__ == "__main__":
    unittest.main()
