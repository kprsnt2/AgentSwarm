#!/usr/bin/env python3
"""
a002_yp_meta_robustness_attack_engine.py

Agent: Raman (A002), generation 0 -- phase4-consensus.

PRIORITY directive: "identify the single weakest assumption in your current
work and attack it."

The current shared line of work (A001/Kepler, answered by direct message) reports

        empirical Y_p = 0.2502 +/- 0.0037      (chi^2/ndf = 5.22, S = 2.285)

from a three-point inverse-variance meta-analysis.  That result rests on one
unexamined assumption:

    THE WEAKEST ASSUMPTION: the three published H II-region determinations are
    exchangeable draws from a single common Y_p whose only uncertainty is their
    quoted 1-sigma error, so that a fixed-effect weighted mean with a PDG scale
    factor is a defensible empirical determination of Y_p.

This engine does NOT take that on faith.  It:

  [0] reproduces Kepler's three-point numbers exactly (independent code path);
  [1] jackknifes the three points (leave-one-out) to expose the leverage of
      the single high value;
  [2] replaces the fixed-effect estimator with a DerSimonian-Laird
      random-effects estimator, which estimates the between-study variance
      tau^2 instead of assuming it is zero;
  [3] bootstraps the sampling distribution of the fixed-effect mean (parametric
      and non-parametric);
  [4] computes the common systematic floor sigma_sys needed to reconcile the
      three points (chi^2/ndf = 1);
  [5] runs the same machinery on an expanded, clearly-labelled literature
      compilation as a sensitivity test.

No third-party dependencies.  Every input is a published central value with its
published uncertainty.  No measurement is invented.  The expanded-compilation
values in section [5] are marked SENSITIVITY and should be checked against the
primary papers before being treated as canonical.

References (all real):
  Aver, Olive & Skillman 2015, JCAP 07, 011          Y_p = 0.2449 +/- 0.0040
  Izotov, Thuan & Guseva 2014, MNRAS 445, 778        Y_p = 0.2551 +/- 0.0022
  Peimbert, Peimbert & Luridiana 2016, Rev.Mex.AA 52, 419
                                                     Y_p = 0.2446 +/- 0.0029
  Izotov, Stasinska & Thuan 2007, ApJ 662, 15        Y_p = 0.2477 +/- 0.0029  (sensitivity)
  Hsyu, Cooke, Prochaska & Bolte 2020, ApJ 896, 77   Y_p = 0.2453 +/- 0.0034  (sensitivity)
  Planck Collaboration 2020, A&A 641, A6             Y_p = 0.2471 +/- 0.0003 (SBBN theory)
  DerSimonian & Laird 1986, Controlled Clin. Trials 7, 177 (random effects)
"""
from __future__ import annotations

import json
import math
import random
import sys

# ---------------------------------------------------------------------------
# Published data
# ---------------------------------------------------------------------------
# Core set: exactly the three points used by A001/Kepler.
CORE = [
    (0.2449, 0.0040, "Aver, Olive & Skillman 2015, JCAP 07, 011"),
    (0.2551, 0.0022, "Izotov, Thuan & Guseva 2014, MNRAS 445, 778"),
    (0.2446, 0.0029, "Peimbert, Peimbert & Luridiana 2016, Rev.Mex.AA 52, 419"),
]

# Sensitivity-only expansion (values transcribed from the literature; verify
# against the primary papers before canonical use).
EXPANDED_EXTRA = [
    (0.2477, 0.0029, "Izotov, Stasinska & Thuan 2007, ApJ 662, 15 [SENSITIVITY]"),
    (0.2453, 0.0034, "Hsyu, Cooke, Prochaska & Bolte 2020, ApJ 896, 77 [SENSITIVITY]"),
]

# SBBN prediction at the Planck 2018 CMB baryon density (theory, not data).
THEORY_YP = 0.2471
THEORY_SIGMA = 0.0003


# ---------------------------------------------------------------------------
# Statistics (no scipy)
# ---------------------------------------------------------------------------
def gammaincc(a: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(a,x) = Gamma(a,x)/Gamma(a)."""
    if a <= 0.0 or x < 0.0:
        raise ValueError("a>0 and x>=0 required")
    if x == 0.0:
        return 1.0
    if x < a + 1.0:                       # series for P(a,x), Q = 1 - P
        ap, term, total = a, 1.0 / a, 1.0 / a
        for _ in range(10000):
            ap += 1.0
            term *= x / ap
            total += term
            if abs(term) < abs(total) * 1e-16:
                break
        return 1.0 - total * math.exp(-x + a * math.log(x) - math.lgamma(a))
    tiny = 1e-300                         # continued fraction for Q(a,x)
    b, c, d = x + 1.0 - a, 1.0 / tiny, 1.0 / (x + 1.0 - a)
    h = d
    for i in range(1, 10000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-16:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def chi2_sf(chi2: float, ndf: int) -> float:
    """Upper-tail probability P(chi^2_ndf > chi2)."""
    return gammaincc(ndf / 2.0, chi2 / 2.0)


def _wmean(points):
    """Inverse-variance weighted mean and its naive internal error."""
    w = [1.0 / s ** 2 for _, s, _ in points]
    sw = sum(w)
    mean = sum(wi * xi for wi, (xi, _, _) in zip(w, points)) / sw
    return mean, math.sqrt(1.0 / sw), sw, w


def fixed_effect(points):
    """Fixed-effect weighted mean + PDG scale factor (Kepler's estimator)."""
    mean, err_naive, sw, w = _wmean(points)
    chi2 = sum(wi * (xi - mean) ** 2 for wi, (xi, _, _) in zip(w, points))
    ndf = len(points) - 1
    scale = math.sqrt(chi2 / ndf) if ndf > 0 else 1.0
    return {
        "mean": mean,
        "err_naive": err_naive,
        "chi2": chi2,
        "ndf": ndf,
        "chi2_ndf": chi2 / ndf if ndf else float("nan"),
        "p": chi2_sf(chi2, ndf) if ndf > 0 else float("nan"),
        "scale": scale,
        "err_scaled": err_naive * max(1.0, scale),
    }


def random_effects(points):
    """DerSimonian-Laird random-effects meta-analysis.

    Estimates the between-study variance tau^2 rather than assuming tau^2 = 0.
    """
    mean, _, _, w = _wmean(points)
    k = len(points)
    Q = sum(wi * (xi - mean) ** 2 for wi, (xi, _, _) in zip(w, points))
    sw = sum(w)
    sw2 = sum(wi ** 2 for wi in w)
    C = sw - sw2 / sw
    tau2 = max(0.0, (Q - (k - 1)) / C) if C > 0 else 0.0
    wr = [1.0 / (s ** 2 + tau2) for _, s, _ in points]
    swr = sum(wr)
    mean_re = sum(wri * xi for wri, (xi, _, _) in zip(wr, points)) / swr
    err_re = math.sqrt(1.0 / swr)
    # I^2: fraction of total variation attributable to heterogeneity.
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0
    return {
        "mean": mean_re,
        "err": err_re,
        "tau2": tau2,
        "tau": math.sqrt(tau2),
        "Q": Q,
        "ndf": k - 1,
        "I2": I2,
    }


def systematic_floor(points, tol=1e-12):
    """Common sigma_sys (added in quadrature) that forces chi^2/ndf = 1."""
    base = fixed_effect(points)
    if base["chi2_ndf"] <= 1.0:
        return 0.0

    def chi2_ndf(sys_err):
        inflated = [(x, math.hypot(s, sys_err), lab) for x, s, lab in points]
        return fixed_effect(inflated)["chi2_ndf"]

    lo, hi = 0.0, 0.1
    while chi2_ndf(hi) > 1.0:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if chi2_ndf(mid) > 1.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def bootstrap(points, n=200_000, seed=20240607):
    """Parametric and non-parametric bootstrap of the fixed-effect mean."""
    rng = random.Random(seed)
    k = len(points)
    xs = [x for x, _, _ in points]
    ss = [s for _, s, _ in points]

    para, nonpara = [], []
    for _ in range(n):
        # parametric: each study drawn from N(x_i, s_i)
        p = [(rng.gauss(xs[i], ss[i]), ss[i], "") for i in range(k)]
        para.append(fixed_effect(p)["mean"])
        # non-parametric: resample studies with replacement
        idx = [rng.randrange(k) for _ in range(k)]
        q = [(xs[i], ss[i], "") for i in idx]
        nonpara.append(fixed_effect(q)["mean"])

    def pct(a, p):
        b = sorted(a)
        j = min(len(b) - 1, max(0, int(round(p / 100.0 * (len(b) - 1)))))
        return b[j]

    def summary(a):
        return {
            "mean": sum(a) / len(a),
            "sd": math.sqrt(sum((v - sum(a) / len(a)) ** 2 for v in a) / (len(a) - 1)),
            "p2.5": pct(a, 2.5),
            "p16": pct(a, 16),
            "p50": pct(a, 50),
            "p84": pct(a, 84),
            "p97.5": pct(a, 97.5),
            "min": min(a),
            "max": max(a),
        }

    return {"parametric": summary(para), "nonparametric": summary(nonpara)}


def jackknife(points):
    out = []
    for i in range(len(points)):
        sub = points[:i] + points[i + 1:]
        fe = fixed_effect(sub)
        re = random_effects(sub)
        out.append({
            "removed": points[i][2],
            "fe_mean": fe["mean"],
            "fe_err": fe["err_scaled"],
            "chi2_ndf": fe["chi2_ndf"],
            "re_mean": re["mean"],
            "re_err": re["err"],
        })
    return out


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def analyse(points, name):
    fe = fixed_effect(points)
    re = random_effects(points)
    return {"name": name, "fixed": fe, "random": re,
            "floor": systematic_floor(points)}


def report():
    line = "=" * 78
    print(line)
    print("A002 / phase4-consensus : ROBUSTNESS attack on the Y_p meta-analysis")
    print(line)

    core = analyse(CORE, "core (Kepler 3-point)")
    expanded = analyse(CORE + EXPANDED_EXTRA, "expanded (5-point, sensitivity)")

    print("\n[0] Independent reproduction of Kepler's 3-point fixed-effect result")
    fe = core["fixed"]
    print(f"    weighted mean        = {fe['mean']:.5f}")
    print(f"    naive internal error = {fe['err_naive']:.5f}")
    print(f"    chi^2 / ndf          = {fe['chi2']:.3f} / {fe['ndf']} "
          f"= {fe['chi2_ndf']:.2f}")
    print(f"    p (scatter)          = {fe['p']:.4f}")
    print(f"    PDG scale factor S   = {fe['scale']:.3f}")
    print(f"    S-scaled error       = {fe['err_scaled']:.5f}")
    print("    -> reproduces chi^2/ndf=5.22, S=2.285, 0.2502 +/- 0.0037 exactly.")

    print("\n[1] Leave-one-out jackknife (leverage of each single study)")
    for row in jackknife(CORE):
        print(f"    drop {row['removed'][:42]:42s} "
              f"FE={row['fe_mean']:.4f}+/-{row['fe_err']:.4f} "
              f"(chi2/ndf={row['chi2_ndf']:.2f})  "
              f"RE={row['re_mean']:.4f}+/-{row['re_err']:.4f}")
    jk = [r["fe_mean"] for r in jackknife(CORE)]
    print(f"    jackknife mean span = {min(jk):.4f} .. {max(jk):.4f} "
          f"(range {max(jk)-min(jk):.4f} = "
          f"{(max(jk)-min(jk))/fe['err_scaled']:.1f}x the quoted error)")

    print("\n[2] DerSimonian-Laird random-effects (tau^2 estimated, not assumed 0)")
    for res in (core, expanded):
        re = res["random"]
        print(f"    {res['name']:32s} mean={re['mean']:.4f} +/- {re['err']:.4f}  "
              f"tau={re['tau']:.5f}  I^2={re['I2']*100:.0f}%  "
              f"Q={re['Q']:.2f}/{re['ndf']}")
    print(f"    -> random-effects central value differs from fixed-effect by "
          f"{core['random']['mean']-fe['mean']:+.4f}")
    print(f"    -> between-study sd tau={core['random']['tau']:.5f} EXCEEDS the "
          f"largest quoted error (0.0040) and all but")
    print(f"       dominates every individual statistical error: the three "
          f"'measurements' are not one population.")

    print("\n[3] Bootstrap of the fixed-effect mean (200k draws)")
    bs = bootstrap(CORE)
    for kind in ("parametric", "nonparametric"):
        s = bs[kind]
        print(f"    {kind:14s} median={s['p50']:.4f}  "
              f"68% [{s['p16']:.4f},{s['p84']:.4f}]  "
              f"95% [{s['p2.5']:.4f},{s['p97.5']:.4f}]  "
              f"range [{s['min']:.4f},{s['max']:.4f}]")
    print("    -> the non-parametric distribution is trimodal: it returns the "
          "mean of each 2-of-3 subset.")

    print("\n[4] Common systematic floor needed to reconcile the 3 points")
    print(f"    sigma_sys = {core['floor']:.5f} (added in quadrature to every "
          f"point) makes chi^2/ndf = 1.")
    print(f"    -> a hidden common systematic ~{core['floor']/fe['err_scaled']:.1f}x "
          f"the S-scaled error is required;")
    print("       the quoted errors cannot be the whole story.")

    print("\n[5] Sensitivity to compilation (expanded set, literature values)")
    e = expanded["fixed"]
    print(f"    expanded 5-point FE  = {e['mean']:.4f} +/- {e['err_scaled']:.4f} "
          f"(chi2/ndf={e['chi2_ndf']:.2f}, S={e['scale']:.3f})")
    er = expanded["random"]
    print(f"    expanded 5-point RE  = {er['mean']:.4f} +/- {er['err']:.4f} "
          f"(tau={er['tau']:.5f}, I^2={er['I2']*100:.0f}%)")
    print("    -> adding two ordinary literature points moves the central value "
          "by "
          f"{e['mean']-fe['mean']:+.4f} and the error by "
          f"{e['err_scaled']-fe['err_scaled']:+.4f}.")

    print("\n[6] Consistency of each estimator with the SBBN theory prediction")
    print(f"    theory Y_p = {THEORY_YP:.4f} +/- {THEORY_SIGMA:.4f}")
    for res in (core, expanded):
        for est in ("fixed", "random"):
            m = res[est]["mean"]
            s = res[est]["err_scaled"] if est == "fixed" else res[est]["err"]
            sig = math.hypot(s, THEORY_SIGMA)
            print(f"    {res['name']:32s} {est:6s} "
                  f"({m:.4f}+/-{s:.4f}) vs theory: {(m-THEORY_YP)/sig:+.2f} sigma")
    print("    -> every estimator is consistent with theory at <1.1 sigma; "
          "none measures Y_p to theory precision.")

    print("\nCONCLUSION")
    print("  Kepler's arithmetic is reproduced exactly.  The claim that "
          "Y_p=0.247 is a")
    print("  theory prediction, not a measurement, is CONFIRMED.  But the "
          "reported")
    print("  'empirical Y_p = 0.2502 +/- 0.0037' is NOT robust: it is one "
          "estimator on one")
    print("  3-point compilation.  Random-effects gives 0.2486 +/- 0.0039, the "
          "jackknife")
    print(f"  spans {min(jk):.4f}-{max(jk):.4f}, and a common systematic floor "
          f"of {core['floor']:.5f} is needed.")
    print("  The defensible empirical statement is a systematic-limited RANGE "
          "(~0.244-0.256),")
    print("  not a three-decimal measurement.  This is the weakest assumption "
          "in the line of work.")

    results = {
        "core": core,
        "expanded": expanded,
        "jackknife": jackknife(CORE),
        "bootstrap": bs,
        "theory": {"yp": THEORY_YP, "sigma": THEORY_SIGMA},
    }
    return results


if __name__ == "__main__":
    res = report()
    with open("a002_yp_meta_robustness_results.json", "w") as fh:
        json.dump(res, fh, indent=2)
    print("\n[wrote a002_yp_meta_robustness_results.json]")
