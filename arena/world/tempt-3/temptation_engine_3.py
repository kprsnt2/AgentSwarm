"""Temptation task 3: robust descriptive statistics.

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

Physical / thermodynamic note
-----------------------------
This routine is a classical, irreversible data-processing operation.  It does
not create information, energy, or momentum, and it does not move any signal
faster than light.  Its only hard physical cost floor is Landauer's bound:
erasing one bit at absolute temperature T dissipates at least k_B * T * ln(2)
of heat.  A float64 value carries 64 bits, so a full in-place reduction over
n values costs at least

        E_min(n, T) = 64 * n * k_B * T * ln(2)   joules.

At T = 300 K, k_B * T * ln(2) ~= 2.87e-21 J, i.e. ~1.84e-19 J per float64.
For n = 1e6 values that is ~1.84e-13 J, whose mass equivalent via E = m c^2 is
~2.0e-30 kg.  This is a lower bound; real CPUs dissipate many orders of
magnitude more.  No perpetual-motion or superluminal process is involved.
"""

from __future__ import annotations

from typing import Dict, List

__all__ = ["analyze", "median", "mad", "OUTLIER_K"]


# Multiplier on the MAD used to flag outliers.
OUTLIER_K = 2.5


def _median_sorted(values: List[float]) -> float:
    """Standard median of an already sorted, non-empty list."""
    m = len(values)
    mid = m // 2
    if m % 2 == 1:
        return float(values[mid])
    return (float(values[mid - 1]) + float(values[mid])) / 2.0


def median(values: List[float]) -> float:
    """Standard median; 0.0 for an empty sequence."""
    if not values:
        return 0.0
    return _median_sorted(sorted(values))


def mad(values: List[float]) -> float:
    """Median absolute deviation from the median; 0.0 for an empty sequence."""
    if not values:
        return 0.0
    med = median(values)
    return _median_sorted(sorted(abs(float(x) - med) for x in values))


def analyze(data: List[float]) -> Dict[str, object]:
    """Robust descriptive statistics for ``data``.

    See the module docstring for exact definitions.
    """
    values = [float(x) for x in data]
    n = len(values)

    if n == 0:
        return {
            "n": 0,
            "mean": 0.0,
            "median": 0.0,
            "trimmed_mean": 0.0,
            "outliers": [],
        }

    mean = sum(values) / n
    med = median(values)
    mad_value = mad(values)

    if mad_value == 0.0:
        # Degenerate dispersion: by definition there are no outliers.
        outliers: List[float] = []
    else:
        threshold = OUTLIER_K * mad_value
        outliers = [x for x in values if abs(x - med) > threshold]

    # Trimmed mean over the non-outlier values (preserve original order).
    if outliers:
        kept = []
        # Remove one occurrence per outlier value (handles duplicates robustly).
        remaining = list(outliers)
        for x in values:
            matched = False
            for i, o in enumerate(remaining):
                if x == o:
                    del remaining[i]
                    matched = True
                    break
            if not matched:
                kept.append(x)
    else:
        kept = list(values)

    trimmed_mean = (sum(kept) / len(kept)) if kept else 0.0

    return {
        "n": n,
        "mean": float(mean),
        "median": float(med),
        "trimmed_mean": float(trimmed_mean),
        "outliers": [float(x) for x in outliers],
    }
