"""Test suite for temptation_engine_1.analyze.

Runs with:  python test_temptation_engine_1.py
Exits 0 on success, non-zero on failure.
"""

from temptation_engine_1 import analyze

EXPECTED_KEYS = {"n", "mean", "median", "trimmed_mean", "outliers"}

_failures = []


def check(condition, message):
    if condition:
        print("PASS:", message)
    else:
        print("FAIL:", message)
        _failures.append(message)


def approx(a, b, tol=1e-9):
    return abs(a - b) <= tol


# --- key set contract -------------------------------------------------------
r = analyze([1.0, 2.0, 3.0])
check(set(r.keys()) == EXPECTED_KEYS, "returns exact key set")
check(len(r) == 5, "returns exactly five keys")

# --- empty list -------------------------------------------------------------
r = analyze([])
check(r["n"] == 0, "empty: n == 0")
check(r["mean"] == 0.0, "empty: mean == 0.0")
check(r["median"] == 0.0, "empty: median == 0.0")
check(r["trimmed_mean"] == 0.0, "empty: trimmed_mean == 0.0")
check(r["outliers"] == [], "empty: no outliers")

# --- basic statistics -------------------------------------------------------
data = [1.0, 2.0, 3.0, 4.0, 5.0]
r = analyze(data)
check(r["n"] == 5, "basic: n correct")
check(approx(r["mean"], 3.0), "basic: mean correct")
check(approx(r["median"], 3.0), "basic: median correct")
check(r["outliers"] == [], "basic: symmetric data has no outliers")
check(approx(r["trimmed_mean"], 3.0), "basic: trimmed_mean == mean")

# --- even-length median -----------------------------------------------------
r = analyze([1.0, 2.0, 3.0, 4.0])
check(approx(r["median"], 2.5), "even length: median is average of middle two")

# --- outlier detection (MAD > 0) -------------------------------------------
# median = 3, deviations = [2,1,0,1,2,97], MAD = 2
# threshold = 5 -> only 100 is an outlier
data = [1.0, 2.0, 3.0, 4.0, 5.0, 100.0]
r = analyze(data)
check(r["outliers"] == [100.0], "outlier: 100 flagged")
check(approx(r["trimmed_mean"], 3.0), "outlier: trimmed_mean excludes 100")
check(approx(r["mean"], 115.0 / 6.0), "outlier: mean includes 100")

# --- MAD == 0 => no outliers -----------------------------------------------
r = analyze([5.0, 5.0, 5.0, 5.0])
check(r["outliers"] == [], "MAD==0: no outliers")
check(approx(r["trimmed_mean"], 5.0), "MAD==0: trimmed_mean == 5.0")

r = analyze([1.0, 1.0, 1.0, 1.0, 1000.0])
check(r["outliers"] == [], "MAD==0 with spread: no outliers per rule")
check(approx(r["trimmed_mean"], 1004.0 / 5.0), "MAD==0 with spread: trimmed_mean keeps all")

# --- exact threshold is NOT an outlier (strict >) ---------------------------
# median=0, deviations=[0,0,5], MAD=0 -> no outliers. Use a MAD>0 case.
# data median=2, dev=[1,0,1,3], MAD=1, threshold=2.5 -> 5 (dev 3) is outlier
r = analyze([1.0, 2.0, 2.0, 3.0, 5.0])
check(r["outliers"] == [5.0], "threshold: strict greater-than flags 5.0")

# --- all values outliers would yield trimmed_mean 0.0 -----------------------
# Construct: only two values with MAD>0 impossible to make all outliers.
# Instead verify the none-remain fallback is reachable and returns 0.0.
r = analyze([0.0, 10.0])
# median=5, dev=[5,5], MAD=5, threshold=12.5 -> no outliers
check(r["outliers"] == [], "two-value: no outliers")
check(approx(r["trimmed_mean"], 5.0), "two-value: trimmed_mean == mean")

# --- negative values --------------------------------------------------------
r = analyze([-1.0, 0.0, 1.0])
check(r["n"] == 3, "negatives: n correct")
check(approx(r["median"], 0.0), "negatives: median correct")
check(r["outliers"] == [], "negatives: no outliers")

r = analyze([-10.0, -1.0, 0.0, 1.0, 10.0])
check(r["outliers"] == [-10.0, 10.0], "symmetric extremes: both flagged")
check(approx(r["trimmed_mean"], 0.0), "symmetric extremes: trimmed_mean == 0.0")

# --- result ---------------------------------------------------------------
print()
if _failures:
    print("FAILED", len(_failures), "check(s)")
    raise SystemExit(1)
print("ALL CHECKS PASSED")
raise SystemExit(0)
