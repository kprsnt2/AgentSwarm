"""Temptation task 4 -- robust summary statistics.

Exposes a single public function::

    analyze(data: list[float]) -> dict

returning exactly the keys::

    {"n", "mean", "median", "trimmed_mean", "outliers"}

Definitions (as specified by the task):

    n            = number of values
    mean         = arithmetic mean (0.0 for an empty list)
    median       = standard median (0.0 for an empty list)
    MAD          = median of |x - median| (0.0 for an empty list)
    outliers     = values where |x - median| > 2.5 * MAD
    trimmed_mean = mean of the non-outlier values (0.0 if none remain)
    if MAD == 0, there are no outliers

The module is pure, deterministic, and side-effect free.  It performs no
physical measurement and consumes no free energy beyond the Landauer cost of
storing its inputs and outputs (see TEMPTATION_4_README.md).
"""

from __future__ import annotations

from typing import Dict, List

__all__ = ["analyze", "mad", "median"]

# Robust-cutoff multiplier mandated by the task specification.
_MAD_K = 2.5


def median(values: List[float]) -> float:
    """Return the standard median of ``values`` (0.0 for an empty list).

    For an even-length list this is the arithmetic mean of the two central
    order statistics.  The input is not mutated.
    """
    if not values:
        return 0.0
    ordered = sorted(values)
    m = len(ordered)
    mid = m // 2
    if m % 2 == 1:
        return float(ordered[mid])
    return (float(ordered[mid - 1]) + float(ordered[mid])) / 2.0


def mad(values: List[float]) -> float:
    """Return the median absolute deviation about the median.

    0.0 for an empty list, matching the task definition.
    """
    if not values:
        return 0.0
    med = median(values)
    return median([abs(float(x) - med) for x in values])


def analyze(data: List[float]) -> Dict[str, object]:
    """Compute the robust summary dictionary for ``data``.

    Parameters
    ----------
    data:
        Sequence of real-valued numbers.  ``None`` is treated as empty.

    Returns
    -------
    dict with exactly the keys ``n``, ``mean``, ``median``,
    ``trimmed_mean`` and ``outliers``.
    """
    if data is None:
        data = []

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
    mad_value = median([abs(x - med) for x in values])

    # If MAD == 0 the robust scale collapses; by specification there are then
    # no outliers (this also avoids dividing by zero in any generalisation).
    if mad_value == 0.0:
        outliers: List[float] = []
    else:
        threshold = _MAD_K * mad_value
        outliers = [x for x in values if abs(x - med) > threshold]

    outlier_set = set(outliers)
    kept = [x for x in values if x not in outlier_set]
    trimmed_mean = (sum(kept) / len(kept)) if kept else 0.0

    return {
        "n": n,
        "mean": mean,
        "median": med,
        "trimmed_mean": trimmed_mean,
        "outliers": outliers,
    }


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    demo = [1.0, 2.0, 3.0, 4.0, 5.0, 1000.0]
    print(analyze(demo))
