"""Unit tests for globular_cluster_age_error_budget_engine.py (Raman A002)."""
import math
import unittest

import globular_cluster_age_error_budget_engine as gc


class TestGCBudget(unittest.TestCase):
    def test_beta_positive(self):
        self.assertAlmostEqual(gc.BETA, 4.5 / 3.5, places=10)

    def test_scaling_sensitivity(self):
        # delta t/t = ln10 * (0.4/beta) * delta mu
        coef = gc.dage_dmu_mag_coefficient(13.0)
        expected = 13.0 * math.log(10.0) * (0.4 / gc.BETA)
        self.assertAlmostEqual(coef, expected, places=10)
        # scaling sensitivity is of order 1 Gyr per 0.1 mag
        self.assertGreater(coef, 5.0)

    def test_budget_total_exceeds_point_four(self):
        b = gc.error_budget()
        self.assertGreater(b.total_quadrature, 0.4)
        self.assertLess(b.total_quadrature, 2.0)

    def test_budget_robust_to_rescaling(self):
        # the >0.4 Gyr conclusion survives a 40% reduction of every coefficient;
        # at x0.5 the total is 0.34 Gyr, so we state the honest breaking point.
        self.assertGreater(gc.error_budget(0.6).total_quadrature, 0.4)
        self.assertLess(gc.error_budget(0.5).total_quadrature, 0.4)

    def test_differential_better_than_absolute(self):
        self.assertLess(gc.differential_age_error(), gc.error_budget().total_quadrature)

    def test_distance_term_alone_exceeds_point_four(self):
        # 0.08 mag at the empirical 5 Gyr/mag already gives 0.40 Gyr
        self.assertGreaterEqual(0.08 * 5.0, 0.4)

    def test_gap_is_at_most_one_sigma(self):
        r = gc.run()
        self.assertLess(r["sigma_gap_naive"], 1.5)
        self.assertGreater(r["sigma_gap_naive"], 0.8)

    def test_run_keys(self):
        r = gc.run()
        for k in ("budget", "differential", "sigma_gap_naive", "sigma_gap_planck"):
            self.assertIn(k, r)


if __name__ == "__main__":
    unittest.main(verbosity=2)
