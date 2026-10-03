#!/usr/bin/env python3
"""Tests for a001_yp_consensus_provenance_attack_engine.py (A001)."""
import math
import a001_yp_consensus_provenance_attack_engine as eng

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}  {detail}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


def main():
    ma = eng.meta_analysis(eng.OBSERVED_YP)

    # 1. Weighted mean is bracketed by the inputs.
    xs = [x for x, _, _ in eng.OBSERVED_YP]
    check("weighted mean inside data range",
          min(xs) < ma["mean"] < max(xs),
          f"mean={ma['mean']:.5f}")

    # 2. The scatter is real: chi2/ndf > 1 (errors do not explain spread).
    check("scatter exceeds quoted errors (chi2/ndf>1)",
          ma["chi2_ndf"] > 1.0, f"chi2/ndf={ma['chi2_ndf']:.2f}")

    # 3. PDG scale factor materially inflates the error (>1.5).
    check("PDG scale factor > 1.5", ma["scale"] > 1.5,
          f"S={ma['scale']:.3f}")

    # 4. Empirical precision is ~0.004, i.e. ~10x the theory precision.
    check("empirical error >= 0.003", ma["err_scaled"] >= 0.003,
          f"err={ma['err_scaled']:.5f}")
    check("empirical error >= 5x theory error",
          ma["err_scaled"] >= 5.0 * eng.PLANCK_YP_SIGMA,
          f"ratio={ma['err_scaled']/eng.PLANCK_YP_SIGMA:.1f}")

    # 5. Theory and empirical means are consistent (< 2 sigma).
    sig = math.hypot(ma["err_scaled"], eng.PLANCK_YP_SIGMA)
    nsig = abs(ma["mean"] - eng.PLANCK_YP) / sig
    check("theory vs empirical < 2 sigma", nsig < 2.0, f"{nsig:.2f} sigma")

    # 6. chi2 survival function sanity: Q(chi2, ndf) monotone decreasing.
    check("chi2_sf decreasing",
          eng.chi2_sf(1.0, 3) > eng.chi2_sf(5.0, 3) > eng.chi2_sf(20.0, 3),
          f"{eng.chi2_sf(1.0,3):.4f} > {eng.chi2_sf(5.0,3):.4f} > {eng.chi2_sf(20.0,3):.4f}")
    check("chi2_sf known value Q(2,2)=e^-1",
          abs(eng.chi2_sf(2.0, 2) - math.exp(-1.0)) < 1e-12,
          f"{eng.chi2_sf(2.0,2):.10f}")

    # 7. BBN model sensitivity is positive and of order 1e-4 / s.
    rows = eng.neutron_lifetime_scan()
    check("all dY/dtau positive", all(r["sens"] > 0 for r in rows))
    check("sensitivity in [5e-5, 5e-4]/s",
          all(5e-5 < r["sens"] < 5e-4 for r in rows),
          f"range {min(r['sens'] for r in rows):.2e}..{max(r['sens'] for r in rows):.2e}")

    # 8. Beam-bottle discrepancy shifts Y_p by O(0.001), below the empirical error.
    dy = [r["dY_beam_bottle"] for r in rows]
    check("beam-bottle dY in [0.0005,0.004]",
          all(5e-4 < d < 4e-3 for d in dy),
          f"range {min(dy):.5f}..{max(dy):.5f}")
    check("lifetime systematic < empirical systematic",
          max(dy) < ma["err_scaled"],
          f"max dY={max(dy):.5f} < err={ma['err_scaled']:.5f}")

    # 9. Calibration reproduces the target Y_p at the PDG lifetime.
    rf = eng.calibrate_r_freeze(0.2470, eng.TAU_PDG[0], 700.0)
    r = rf * math.exp(-700.0 / eng.TAU_PDG[0])
    yp = 2 * r / (1 + r)
    check("model calibration reproduces Y_p=0.2470",
          abs(yp - 0.2470) < 1e-9, f"Y_p={yp:.10f}")

    print(f"\n{PASS}/{PASS+FAIL} tests passed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
