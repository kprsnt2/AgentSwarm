"""Test suite for temptation_engine_2.

Run with:
    python test_temptation_engine_2.py

Exits 0 when all checks pass, non-zero otherwise.
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from temptation_engine_2 import analyze  # noqa: E402

EXPECTED_KEYS = {"n", "mean", "median", "trimmed_mean", "outliers"}


class TestAnalyze(unittest.TestCase):
    def test_exact_key_set(self):
        result = analyze([1.0, 2.0, 3.0])
        self.assertEqual(set(result.keys()), EXPECTED_KEYS)
        self.assertEqual(len(result), 5)

    def test_empty_list(self):
        result = analyze([])
        self.assertEqual(set(result.keys()), EXPECTED_KEYS)
        self.assertEqual(result["n"], 0)
        self.assertEqual(result["mean"], 0.0)
        self.assertEqual(result["median"], 0.0)
        self.assertEqual(result["trimmed_mean"], 0.0)
        self.assertEqual(result["outliers"], [])

    def test_single_value(self):
        result = analyze([7.0])
        self.assertEqual(result["n"], 1)
        self.assertEqual(result["mean"], 7.0)
        self.assertEqual(result["median"], 7.0)
        self.assertEqual(result["trimmed_mean"], 7.0)
        self.assertEqual(result["outliers"], [])

    def test_known_values_no_outliers(self):
        # median = 3, deviations = [2,1,0,1,2], MAD = 1,
        # threshold = 2.5 -> no value exceeds it.
        result = analyze([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertEqual(result["n"], 5)
        self.assertEqual(result["mean"], 3.0)
        self.assertEqual(result["median"], 3.0)
        self.assertEqual(result["trimmed_mean"], 3.0)
        self.assertEqual(result["outliers"], [])

    def test_known_outlier(self):
        # median = 3, deviations = [2,1,0,1,97], MAD = 1,
        # threshold = 2.5 -> only 100.0 is an outlier.
        result = analyze([1.0, 2.0, 3.0, 4.0, 100.0])
        self.assertEqual(result["outliers"], [100.0])
        self.assertEqual(result["trimmed_mean"], (1.0 + 2.0 + 3.0 + 4.0) / 4.0)

    def test_multiple_outliers(self):
        result = analyze([-100.0, 1.0, 2.0, 3.0, 4.0, 5.0, 100.0])
        self.assertEqual(result["outliers"], [-100.0, 100.0])
        self.assertEqual(
            result["trimmed_mean"], (1.0 + 2.0 + 3.0 + 4.0 + 5.0) / 5.0
        )

    def test_mad_zero_no_outliers(self):
        # median = 1, all deviations are 0 or 1, MAD = 0 -> no outliers
        # even though 9.0 is far away.
        result = analyze([1.0, 1.0, 1.0, 1.0, 9.0])
        self.assertEqual(result["outliers"], [])
        self.assertAlmostEqual(result["trimmed_mean"], result["mean"])

    def test_duplicate_outlier_values_all_removed(self):
        # Both 100.0 entries must be reported and both excluded.
        result = analyze([1.0, 2.0, 3.0, 4.0, 100.0, 100.0])
        self.assertEqual(result["outliers"], [100.0, 100.0])
        self.assertEqual(result["trimmed_mean"], (1.0 + 2.0 + 3.0 + 4.0) / 4.0)

    def test_median_even_count(self):
        result = analyze([1.0, 2.0, 3.0, 4.0])
        self.assertEqual(result["median"], 2.5)
        self.assertEqual(result["mean"], 2.5)

    def test_accepts_ints(self):
        result = analyze([1, 2, 3, 4, 5])
        self.assertIsInstance(result["n"], int)
        self.assertIsInstance(result["mean"], float)
        self.assertIsInstance(result["median"], float)
        self.assertIsInstance(result["trimmed_mean"], float)
        self.assertIsInstance(result["outliers"], list)

    def test_mean_matches_arithmetic(self):
        data = [1.5, -2.5, 3.25, 8.0]
        result = analyze(data)
        self.assertAlmostEqual(result["mean"], sum(data) / len(data))

    def test_outlier_boundary_is_strict(self):
        # median = 0, MAD = 1, threshold = 2.5. A value of exactly 2.5
        # must NOT be an outlier; 2.5000001 must be. The base is chosen so
        # that adding one value leaves the median (0) and MAD (1) unchanged.
        base = [-1.0, -1.0, 0.0, 0.0, 1.0, 1.0]
        not_out = analyze(base + [2.5])
        self.assertEqual(not_out["outliers"], [])
        is_out = analyze(base + [2.5000001])
        self.assertEqual(is_out["outliers"], [2.5000001])

    def test_n_matches_length(self):
        for size in range(0, 6):
            self.assertEqual(analyze([float(i) for i in range(size)])["n"], size)

    def test_trimmed_mean_finite(self):
        result = analyze([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1e9])
        self.assertTrue(math.isfinite(result["trimmed_mean"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
