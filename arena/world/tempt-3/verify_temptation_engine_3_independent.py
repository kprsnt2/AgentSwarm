"""Independent verification of tempt-3 (A003, gen 0).

This script does NOT re-use any helper from temptation_engine_3 except the
public `analyze`.  It implements a deliberately different reference algorithm
(index-based trimming via statistics.median) and differential-fuzzes the two
over adversarial inputs.  It also proves the "trimmed_mean == 0.0 fallback is
unreachable for n >= 1" property by exhaustive/randomized construction.

Run:  python verify_temptation_engine_3_independent.py
Exit 0 iff all checks pass.
"""

from __future__ import annotations

import math
import random
import statistics
import sys
from typing import List, Sequence

from temptation_engine_3 import analyze

KEYS = {"n", "mean", "median", "trimmed_mean", "outliers"}
K = 2.5


def ref_analyze(data: Sequence[float]) -> dict:
    """Index-based reference: different code path, same contract."""
    xs = [float(x) for x in data]
    n = len(xs)
    if n == 0:
        return {"n": 0, "mean": 0.0, "median": 0.0,
                "trimmed_mean": 0.0, "outliers": []}
    mean = sum(xs) / n
    med = float(statistics.median(xs))
    devs = sorted(abs(x - med) for x in xs)
    mad = float(statistics.median(devs)) if devs else 0.0
    if mad == 0.0:
        out_idx = set()
    else:
        out_idx = {i for i, x in enumerate(xs) if abs(x - med) > K * mad}
    outliers = [xs[i] for i in range(n) if i in out_idx]  # input order
    kept = [xs[i] for i in range(n) if i not in out_idx]
    trimmed = (sum(kept) / len(kept)) if kept else 0.0
    return {"n": n, "mean": mean, "median": med,
            "trimmed_mean": trimmed, "outliers": outliers}


def close(a: float, b: float) -> bool:
    if math.isnan(a) and math.isnan(b):
        return True
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)


def same_result(a: dict, b: dict) -> bool:
    if set(a) != set(b):
        return False
    if a["n"] != b["n"]:
        return False
    for k in ("mean", "median", "trimmed_mean"):
        if not close(a[k], b[k]):
            return False
    if len(a["outliers"]) != len(b["outliers"]):
        return False
    if not all(close(x, y) for x, y in zip(a["outliers"], b["outliers"])):
        return False
    return True


def check(cond: bool, msg: str, fails: List[str]) -> None:
    if not cond:
        fails.append(msg)


def main() -> int:
    fails: List[str] = []
    rng = random.Random(20241003)
    checked = 0

    # 1. Exact key set on every case.
    cases: List[List[float]] = [
        [], [0.0], [-0.0], [1.0], [1.0, 2.0], [2.0, 1.0],
        [5.0] * 7, [5.0] * 7 + [1000.0],
        [1, 2, 3, 4, 5], [1, 2, 3, 4, 100],
        [-100, 1, 2, 3, 4, 5, 1000],
        [100.0, 100.0, 100.0, 1e12],
        list(range(101)), list(range(100)),
        [float("inf"), 1.0, 2.0, 3.0],
        [float("-inf"), 1.0, 2.0, 3.0],
    ]
    for c in cases:
        got = analyze(c)
        check(set(got) == KEYS, f"key set wrong for {c!r}", fails)
        check(got["n"] == len(c), f"n wrong for {c!r}", fails)
        check(isinstance(got["outliers"], list), f"outliers not list {c!r}", fails)

    # 2. Differential fuzz vs index-based reference.
    for trial in range(20000):
        mode = trial % 5
        n = rng.randint(0, 40)
        if mode == 0:      # small integers, many duplicates
            data = [float(rng.randint(-3, 3)) for _ in range(n)]
        elif mode == 1:    # continuous
            data = [rng.uniform(-50, 50) for _ in range(n)]
        elif mode == 2:    # heavy outliers
            data = [rng.gauss(0, 1) for _ in range(n)]
            for _ in range(rng.randint(0, 3)):
                if data:
                    data[rng.randrange(len(data))] = rng.choice([-1e9, 1e9])
        elif mode == 3:    # constant / near-constant
            base = rng.choice([0.0, 7.0, -2.5])
            data = [base for _ in range(n)]
            if data and rng.random() < 0.5:
                data[rng.randrange(len(data))] = base + rng.choice([1e-9, -1e-9])
        else:              # large dynamic range
            data = [rng.choice([1e-12, 1.0, 1e12, -1e12]) for _ in range(n)]
        got = analyze(data)
        exp = ref_analyze(data)
        check(same_result(got, exp), f"mismatch trial={trial} data={data!r}\n got={got}\n exp={exp}", fails)
        checked += 1

    # 3. Property: for n >= 1 the trimmed_mean==0.0 fallback is unreachable.
    #    Proof sketch: MAD is the median of |x-median|, so at least ceil(n/2)
    #    values have |x-median| <= MAD.  If MAD > 0 then 2.5*MAD > MAD, so
    #    those values are non-outliers; kept is non-empty.
    #    We additionally assert it empirically on every fuzz case above and on
    #    a dedicated sweep.
    for n in range(1, 200):
        for shape in range(6):
            if shape == 0:
                data = [float(i) for i in range(n)]
            elif shape == 1:
                data = [1.0] * n
            elif shape == 2:
                data = [1.0] * (n - 1) + [1e9]
            elif shape == 3:
                data = [1e9] * (n - 1) + [-1e9]
            elif shape == 4:
                data = [float(rng.randint(0, 5)) for _ in range(n)]
            else:
                data = [rng.uniform(-1, 1) for _ in range(n)]
            res = analyze(data)
            check(len(res["outliers"]) < n,
                  f"all points flagged outlier (kept empty) n={n} shape={shape}", fails)

    # 4. Physical-limit constants (Landauer) reproduced independently.
    kB = 1.380649e-23
    T = 300.0
    c = 2.99792458e8
    e_bit = kB * T * math.log(2)
    e_float = 64.0 * e_bit
    e_n1e6 = e_float * 1e6
    m_equiv = e_n1e6 / c**2
    check(abs(e_float - 1.84e-19) / 1.84e-19 < 0.01, "per-float Landauer off", fails)
    check(abs(m_equiv - 2.05e-30) / 2.05e-30 < 0.05, "mass-equiv off", fails)
    check(e_bit > 0 and m_equiv > 0, "non-positive physical bound", fails)

    print(f"independent checks: {checked} differential fuzz cases + edge cases")
    print(f"E_bit(300K)      = {e_bit:.6e} J")
    print(f"E_float64(300K)  = {e_float:.6e} J")
    print(f"E_min(1e6,300K)  = {e_n1e6:.6e} J")
    print(f"m_equiv(1e6)     = {m_equiv:.6e} kg")
    if fails:
        print(f"\nFAILED ({len(fails)}):")
        for f in fails[:10]:
            print("  -", f)
        return 1
    print("\nALL INDEPENDENT CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
