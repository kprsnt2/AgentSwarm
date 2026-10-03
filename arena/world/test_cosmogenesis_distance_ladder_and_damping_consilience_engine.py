"""
test_cosmogenesis_distance_ladder_and_damping_consilience_engine.py

Unit test suite for the Distance Ladder Stellar Environment,
CMB Damping Tail Boundary, and Cosmological Consilience Engine.

Authored by Agent Kepler (A001), Swarm Generation 0.
"""

import unittest
import math
from cosmogenesis_distance_ladder_and_damping_consilience_engine import (
    CosmogenesisConsilienceEngine,
    DistanceLadderAnchor,
    EMPIRICAL_ANCHORS,
)


class TestCosmogenesisConsilienceEngine(unittest.TestCase):
    """Test suite validating distance ladder environment synthesis and Bayesian consilience."""

    def setUp(self):
        self.engine = CosmogenesisConsilienceEngine()

    def test_environment_partitioning(self):
        """Verify that anchors are properly partitioned into disk, halo, geometric, and early."""
        disk = self.engine.synthesize_by_environment("disk")
        halo = self.engine.synthesize_by_environment("halo")
        geom = self.engine.synthesize_by_environment("geometric")
        early = self.engine.synthesize_by_environment("early")

        self.assertEqual(disk["count"], 1)
        self.assertGreaterEqual(halo["count"], 3)
        self.assertEqual(geom["count"], 2)
        self.assertEqual(early["count"], 2)

        # Disk must yield H0 > 72
        self.assertGreater(disk["H0_weighted"], 72.0)
        # Early must yield H0 < 68
        self.assertLess(early["H0_weighted"], 68.0)
        # Halo must lie strictly between Early and Disk
        self.assertGreater(halo["H0_weighted"], early["H0_weighted"])
        self.assertLess(halo["H0_weighted"], disk["H0_weighted"])

    def test_halo_vs_disk_discrepancy(self):
        """Verify that the halo vs disk tension corresponds to a ~0.10 - 0.12 mag modulus shift."""
        disc = self.engine.compute_halo_vs_disk_discrepancy()
        self.assertGreater(disc["tension_sigma"], 2.0)
        self.assertLess(disc["tension_sigma"], 3.0)
        self.assertTrue(disc["crowding_explanation_viable"])
        self.assertGreaterEqual(disc["delta_mu_mag"], 0.08)
        self.assertLessEqual(disc["delta_mu_mag"], 0.15)

    def test_pmf_damping_ceiling(self):
        """Verify the PMF Silk damping ceiling caps H0 at ~68.9 km/s/Mpc and avoids S8 explosion."""
        pmf = self.engine.evaluate_pmf_damping_ceiling()
        self.assertAlmostEqual(pmf["b_max_damping_95cl"], 0.28, delta=0.01)
        self.assertLess(pmf["H0_pmf_ceiling"], 69.5)
        self.assertGreater(pmf["H0_pmf_ceiling"], 68.5)
        # S8 must remain near Planck baseline and not blow up to 0.85
        self.assertLess(pmf["S8_pmf"], 0.82)
        self.assertGreater(pmf["S8_pmf"], 0.79)

    def test_jwst_cchp_halo_synthesis(self):
        """Verify JWST NIRCam CCHP combines TRGB and JAGB to yield ~68.96 +- 1.27 km/s/Mpc."""
        cchp = self.engine.synthesize_jwst_cchp()
        self.assertEqual(cchp["count"], 2)
        self.assertAlmostEqual(cchp["H0_weighted"], 68.96, delta=0.2)
        self.assertAlmostEqual(cchp["sigma_weighted"], 1.27, delta=0.2)

    def test_trilemma_consilience(self):
        """Verify concordance between JWST CCHP halo ladder, PMF damping ceiling, and early universe."""
        tri = self.engine.compute_trilemma_consilience()
        self.assertTrue(tri["concordance_established"])
        # PMF ceiling and JWST CCHP must agree within < 0.5 sigma
        self.assertLess(tri["tension_pmf_vs_cchp_sigma"], 0.5)
        # Early universe and JWST CCHP must agree within < 1.5 sigma
        self.assertLess(tri["tension_early_vs_cchp_sigma"], 1.5)
        # Disk (SH0ES) vs Early must remain in acute > 4.5 sigma tension
        self.assertGreater(tri["tension_early_vs_disk_sigma"], 4.5)

    def test_bayesian_model_selection(self):
        """Verify decisive Bayes factor favoring halo consilience over cosmological intervention."""
        bayes = self.engine.perform_bayesian_model_selection()
        self.assertTrue(bayes["decisive_evidence_for_M2"])
        self.assertGreater(bayes["delta_chi2"], 30.0)
        self.assertGreater(bayes["log_bayes_factor_lnB"], 15.0)

    def test_full_report_execution(self):
        """Verify full audit report generation and structured output."""
        report = self.engine.generate_full_audit_report()
        self.assertIn("environments", report)
        self.assertIn("disk_vs_halo", report)
        self.assertIn("pmf_ceiling", report)
        self.assertIn("trilemma_consilience", report)
        self.assertIn("bayesian_model_selection", report)
        self.assertIn("verdict", report)
        self.assertEqual(report["verdict"]["trilemma_status"], "RESOLVED BY CONSILIENCE")


if __name__ == "__main__":
    unittest.main()
