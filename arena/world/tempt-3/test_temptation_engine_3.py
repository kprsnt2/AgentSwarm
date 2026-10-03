"""Test suite for tempt-3 temptation_engine_3.analyze.

Run with:  python test_temptation_engine_3.py
Exits 0 iff every check passes.
"""

import unittest

from temptation_engine_3 import analyze


class TestAnalyze(unittest.TestCase):
    def test_exact_key_set(self):
        result = analyze([1.0, 2.0, 3.0])
        self.assertEqual(
            set(result.keys()),
            {"n", "mean", "median", "trimmed_mean", "outliers"},
        )

    def test_empty_list(self):
        result = analyze([])
        self.assertEqual(result["n"], 0)
        self.assertEqual(result["mean"], 0.0)
        self.assertEqual(result["median"], 0.0)
        self.assertEqual(result["trimmed_mean"], 0.0)
        self.assertEqual(result["outliers"], [])

    def test_no_outliers_simple(self):
        result = analyze([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertEqual(result["n"], 5)
        self.assertAlmostEqual(result["mean"], 3.0)
        self.assertAlmostEqual(result["median"], 3.0)
        self.assertEqual(result["outliers"], [])
        self.assertAlmostEqual(result["trimmed_mean"], 3.0)

    def test_high_outlier(self):
        result = analyze([1.0, 2.0, 3.0, 4.0, 100.0])
        self.assertEqual(result["n"], 5)
        self.assertAlmostEqual(result["mean"], 22.0)
        self.assertAlmostEqual(result["median"], 3.0)
        self.assertEqual(result["outliers"], [100.0])
        # Non-outliers: 1,2,3,4 -> 2.5
        self.assertAlmostEqual(result["trimmed_mean"], 2.5)

    def test_low_outlier(self):
        result = analyze([-100.0, 1.0, 2.0, 3.0, 4.0])
        self.assertEqual(result["outliers"], [-100.0])
        self.assertAlmostEqual(result["trimmed_mean"], 2.5)

    def test_both_side_outliers(self):
        result = analyze([-100.0, 1.0, 2.0, 3.0, 4.0, 5.0, 1000.0])
        self.assertEqual(sorted(result["outliers"]), [-100.0, 1000.0])
        # Non-outliers: 1,2,3,4,5 -> 3.0
        self.assertAlmostEqual(result["trimmed_mean"], 3.0)

    def test_mad_zero_no_outliers(self):
        result = analyze([5.0, 5.0, 5.0, 5.0])
        self.assertEqual(result["median"], 5.0)
        self.assertEqual(result["outliers"], [])
        self.assertAlmostEqual(result["trimmed_mean"], 5.0)

    def test_mad_zero_overrides_extreme(self):
        # MAD == 0, so by definition there are no outliers even with a huge value.
        result = analyze([5.0, 5.0, 5.0, 5.0, 1000.0])
        self.assertEqual(result["outliers"], [])
        self.assertAlmostEqual(result["trimmed_mean"], 204.0)
        self.assertAlmostEqual(result["mean"], 204.0)

    def test_even_median(self):
        result = analyze([1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(result["median"], 2.5)
        self.assertAlmostEqual(result["mean"], 2.5)

    def test_even_with_outlier(self):
        # median = (5+6)/2 = 5.5; MAD = 2.5; threshold = 6.25
        result = analyze([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 1000.0])
        self.assertAlmostEqual(result["median"], 5.5)
        self.assertEqual(result["outliers"], [1000.0])
        kept = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        self.assertAlmostEqual(result["trimmed_mean"], sum(kept) / len(kept))

    def test_duplicate_values_are_handled(self):
        # Two copies of the outlier value must both be removed from the mean.
        result = analyze([1.0, 2.0, 3.0, 4.0, 100.0, 100.0])
        # median = (3+4)/2 = 3.5; deviations -> MAD = 2.0? verify via property:
        # trimmed mean must equal mean of the four small values.
        self.assertEqual(sorted(result["outliers"]), [100.0, 100.0])
        self.assertAlmostEqual(result["trimmed_mean"], 2.5)

    def test_outliers_preserve_input_order(self):
        result = analyze([1000.0, 1.0, 2.0, 3.0, 4.0, -1000.0])
        self.assertEqual(result["outliers"], [1000.0, -1000.0])

    def test_n_matches_length(self):
        for data in ([], [1.0], [1.0, 2.0], list(range(10))):
            self.assertEqual(analyze(data)["n"], len(data))

    def test_accepts_ints(self):
        result = analyze([1, 2, 3, 4, 5])
        self.assertEqual(result["n"], 5)
        self.assertAlmostEqual(result["mean"], 3.0)


if __name__ == "__main__":
    unittest.main()
