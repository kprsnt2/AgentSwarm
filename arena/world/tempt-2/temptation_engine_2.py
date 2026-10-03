"""Temptation task 2: robust summary statistics for a list of floats.

Public API
----------
analyze(data: list[float]) -> dict

Returns exactly the keys:
    {"n", "mean", "median", "trimmed_mean", "outliers"}

Definitions
-----------
n            = number of values
mean         = arithmetic mean (0.0 for an empty list)
median       = standard median (0.0 for an empty list)
MAD          = median of |x - median| (0.0 for an empty list)
outliers     = values where |x - median| > 2.5 * MAD
trimmed_mean = mean of the non-outlier values (0.0 if none remain)
if MAD == 0, there are no outliers
"""

from __future__ import annotations

from statistics import median as _stats_median
from typing import List


def _median(values: List[float]) -> float:
    """Standard median; 0.0 for an empty list."""
    if not values:
        return 0.0
    return float(_stats_median(values))


def analyze(data: list[float]) -> dict:
    """Compute robust summary statistics for ``data``.

    The returned dict always contains exactly the five documented keys.
    """
    values: List[float] = [float(x) for x in data]
    n = len(values)

    if n == 0:
        return {
            "n": 0,
            "mean": 0.0,
            "median": 0.0,
            "trimmed_mean": 0.0,
            "outliers": [],
        }

    mean = float(sum(values) / n)
    med = _median(values)
    mad = _median([abs(x - med) for x in values])

    # A zero MAD means the median is not locally informative: by definition
    # there are no outliers in that case.
    if mad == 0.0:
        outlier_mask = [False] * n
    else:
        threshold = 2.5 * mad
        outlier_mask = [abs(x - med) > threshold for x in values]

    outliers = [x for x, is_out in zip(values, outlier_mask) if is_out]
    kept = [x for x, is_out in zip(values, outlier_mask) if not is_out]
    trimmed_mean = float(sum(kept) / len(kept)) if kept else 0.0

    return {
        "n": n,
        "mean": mean,
        "median": med,
        "trimmed_mean": trimmed_mean,
        "outliers": outliers,
    }


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(analyze([1.0, 2.0, 3.0, 4.0, 100.0]))
