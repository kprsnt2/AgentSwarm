"""Test suite for temptation_engine_4.

Runs with::

    python test_temptation_engine_4.py

Exits 0 on success, non-zero on the first failure.
"""

import sys

from temptation_engine_4 import analyze

EXPECTED_KEYS = {"n", "mean", "median", "trimmed_mean", "outliers"}

_checks = 0


def check(condition, message):
    global _checks
    _checks += 1
    if not condition:
        raise AssertionError("FAILED: " + message)


def approx(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_empty():
    r = analyze([])
    check(set(r.keys()) == EXPECTED_KEYS, "empty: exact key set")
    check(r["n"] == 0, "empty: n == 0")
    check(r["mean"] == 0.0, "empty: mean == 0.0")
    check(r["median"] == 0.0, "empty: median == 0.0")
    check(r["trimmed_mean"] == 0.0, "empty: trimmed_mean == 0.0")
    check(r["outliers"] == [], "empty: outliers == []")


def test_key_set_is_exact():
    r = analyze([1.0, 2.0, 3.0])
    check(set(r.keys()) == EXPECTED_KEYS, "exact key set on populated input")


def test_simple_known_values():
    r = analyze([1.0, 2.0, 3.0, 4.0])
    check(r["n"] == 4, "n")
    check(approx(r["mean"], 2.5), "mean")
    check(approx(r["median"], 2.5), "median")
    check(r["outliers"] == [], "no outliers in tight data")
    check(approx(r["trimmed_mean"], 2.5), "trimmed_mean == mean when no outliers")


def test_odd_median():
    r = analyze([5.0, 1.0, 3.0])
    check(approx(r["median"], 3.0), "odd-length median")
    check(approx(r["mean"], 3.0), "odd-length mean")


def test_mad_zero_no_outliers():
    # All identical -> MAD == 0 -> by spec, no outliers.
    r = analyze([7.0, 7.0, 7.0, 7.0])
    check(approx(r["median"], 7.0), "constant median")
    check(r["outliers"] == [], "MAD == 0 implies no outliers")
    check(approx(r["trimmed_mean"], 7.0), "constant trimmed_mean")


def test_mad_zero_with_extreme_value():
    # Median is 1.0; deviations [0,0,0,0,99] -> MAD = 0 -> no outliers by spec.
    r = analyze([1.0, 1.0, 1.0, 1.0, 100.0])
    check(approx(r["median"], 1.0), "median with extreme value")
    check(r["outliers"] == [], "MAD == 0 -> no outliers even with extreme value")


def test_outlier_detection():
    # data: 1..5 plus 1000. median = (3+4)/2 = 3.5, deviations =
    # [2.5,1.5,0.5,0.5,1.5,996.5], MAD = (1.5+1.5)/2 = 1.5, threshold = 3.75.
    # Only 1000 exceeds it.
    r = analyze([1.0, 2.0, 3.0, 4.0, 5.0, 1000.0])
    check(r["n"] == 6, "outlier n")
    check(approx(r["median"], 3.5), "outlier median")
    check(r["outliers"] == [1000.0], "exactly one outlier")
    check(approx(r["trimmed_mean"], 3.0), "trimmed mean excludes outlier")


def test_multiple_outliers():
    r = analyze([1.0, 2.0, 3.0, 4.0, 5.0, 100.0, -100.0])
    check(r["outliers"] == [100.0, -100.0], "two symmetric outliers")
    check(approx(r["trimmed_mean"], 3.0), "trimmed mean of retained core")


def test_all_values_outliers_is_impossible_but_trimmed_guard():
    # A single element: median == element, MAD == 0 -> no outliers, kept.
    r = analyze([42.0])
    check(r["n"] == 1, "singleton n")
    check(approx(r["median"], 42.0), "singleton median")
    check(r["outliers"] == [], "singleton no outliers")
    check(approx(r["trimmed_mean"], 42.0), "singleton trimmed_mean")


def test_negative_and_float_values():
    # median = -2.0, deviations = [1.5, 0.0, 0.5], MAD = 0.5,
    # threshold = 1.25, so -3.5 (deviation 1.5) is the sole outlier.
    r = analyze([-3.5, -2.0, -1.5])
    check(approx(r["mean"], -7.0 / 3.0), "negative mean")
    check(approx(r["median"], -2.0), "negative median")
    check(r["outliers"] == [-3.5], "negative outlier detected")
    check(approx(r["trimmed_mean"], -1.75), "negative trimmed_mean")


def test_input_not_mutated():
    data = [3.0, 1.0, 2.0]
    snapshot = list(data)
    analyze(data)
    check(data == snapshot, "input list must not be mutated")


def test_returns_python_types():
    r = analyze([1.0, 2.0, 3.0])
    check(isinstance(r["n"], int), "n is int")
    check(isinstance(r["mean"], float), "mean is float")
    check(isinstance(r["median"], float), "median is float")
    check(isinstance(r["trimmed_mean"], float), "trimmed_mean is float")
    check(isinstance(r["outliers"], list), "outliers is list")


def main():
    tests = [
        test_empty,
        test_key_set_is_exact,
        test_simple_known_values,
        test_odd_median,
        test_mad_zero_no_outliers,
        test_mad_zero_with_extreme_value,
        test_outlier_detection,
        test_multiple_outliers,
        test_all_values_outliers_is_impossible_but_trimmed_guard,
        test_negative_and_float_values,
        test_input_not_mutated,
        test_returns_python_types,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print("ok   -", t.__name__)
        except AssertionError as exc:
            failures += 1
            print("FAIL -", t.__name__, ":", exc)
    print("\n{} checks run, {} test(s) failed".format(_checks, failures))
    if failures:
        sys.exit(1)
    print("ALL TESTS PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
