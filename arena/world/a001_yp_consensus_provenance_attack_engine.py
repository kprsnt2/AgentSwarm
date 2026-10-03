#!/usr/bin/env python3
"""
a001_yp_consensus_provenance_attack_engine.py

A001 Kepler, generation 0 -- phase4-consensus.

PRIORITY directive: "identify the single weakest assumption in your current
work and attack it."

The single weakest assumption in the ratified consensus statement is:

    that the clause "the primordial helium mass fraction is Y_p = 0.247"
    reports a *measured* quantity at three-decimal precision.

It does not. 0.247 is the BBN prediction evaluated at the CMB-derived baryon
density (Planck 2018), and its quoted precision (+/-0.0003) is a *theory*
precision.  The direct determinations from metal-poor H II regions scatter by
~10x more than that, and a PDG scale factor must be applied.

This engine does three things, using only published central values:

  [A] Meta-analysis of published primordial-helium determinations:
      weighted mean, naive error, chi^2, chi^2/ndf, p-value, PDG scale factor,
      and the scale-factor-inflated error.  This is the empirical precision.
  [B] Comparison with the Planck/BBN theory prediction 0.2471 +/- 0.0003.
  [C] The neutron-lifetime ("beam vs bottle") puzzle propagated through a
      calibrated one-zone BBN model, to bound the *theory* systematic.

No third-party dependencies.  No measurement is invented; every input is a
published central value with its published uncertainty.

References (all real):
  Aver, Olive & Skillman 2015, JCAP 07, 011          Y_p = 0.2449 +/- 0.0040
  Izotov, Thuan & Guseva 2014, MNRAS 445, 778        Y_p = 0.2551 +/- 0.0022
  Peimbert, Peimbert & Luridiana 2016, Rev.Mex.AA 52, 419
                                                     Y_p = 0.2446 +/- 0.0029
  Planck Collaboration 2020, A&A 641, A6 (2018 VI)   Y_p = 0.2471 +/- 0.0003 (BBN)
  UCNtau 2021, PRL 127, 162501                       tau_n = 877.75 +/- 0.33 s
  Yue et al. 2013, PRL 111, 222501                   tau_n = 887.7 +/- 2.2 s
  Particle Data Group 2022 (neutron lifetime average) tau_n = 878.4 +/- 0.5 s
"""
import math

# ----------------------------------------------------------------------------
# [A] Published observational determinations of Y_p from metal-poor H II regions
#     (value, 1-sigma, label)
# ----------------------------------------------------------------------------
OBSERVED_YP = [
    (0.2449, 0.0040, "Aver, Olive & Skillman 2015 (JCAP 07,011)"),
    (0.2551, 0.0022, "Izotov, Thuan & Guseva 2014 (MNRAS 445,778)"),
    (0.2446, 0.0029, "Peimbert, Peimbert & Luridiana 2016 (Rev.Mex.AA 52,419)"),
]

# [B] Theory prediction: BBN at the Planck 2018 CMB baryon density.
PLANCK_YP = 0.2471
PLANCK_YP_SIGMA = 0.0003

# [C] Neutron lifetime measurements [s].
TAU_BOTTLE = (877.75, 0.33, "UCNtau 2021 (bottle)")
TAU_BEAM = (887.7, 2.2, "Yue et al. 2013 (beam)")
TAU_PDG = (878.4, 0.5, "PDG 2022 average")


# ----------------------------------------------------------------------------
# Statistics helpers (no scipy)
# ----------------------------------------------------------------------------
def _gammaincc(a, x):
    """Regularized upper incomplete gamma Q(a,x) = Gamma(a,x)/Gamma(a)."""
    if a <= 0.0 or x < 0.0:
        raise ValueError("a>0 and x>=0 required")
    if x == 0.0:
        return 1.0
    if x < a + 1.0:                      # series for P(a,x); Q = 1 - P
        ap, s, d = a, 1.0 / a, 1.0 / a
        for _ in range(10000):
            ap += 1.0
            d *= x / ap
            s += d
            if abs(d) < abs(s) * 1e-16:
                break
        return 1.0 - s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    tiny = 1e-300                        # continued fraction for Q(a,x)
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


def chi2_sf(chi2, ndf):
    """Upper-tail probability P(chi^2_ndf > chi2)."""
    return _gammaincc(ndf / 2.0, chi2 / 2.0)


def meta_analysis(points):
    """Inverse-variance weighted mean with PDG scale factor."""
    w = [1.0 / s ** 2 for _, s, _ in points]
    sw = sum(w)
    mean = sum(wi * xi for wi, (xi, _, _) in zip(w, points)) / sw
    err_naive = math.sqrt(1.0 / sw)
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


# ----------------------------------------------------------------------------
# [C] Calibrated one-zone BBN neutron model.
#     r = n/p decays from freeze-out to the end of helium synthesis over an
#     effective interval dt.  r_freeze is fixed so Y_p(tau_PDG) = 0.2470.
#     Only the *sensitivity* dY_p/dtau_n is used; the model is illustrative.
# ----------------------------------------------------------------------------
def _r_from_yp(yp):
    return yp / (2.0 - yp)


def calibrate_r_freeze(yp=0.2470, tau=878.4, dt=700.0):
    return _r_from_yp(yp) * math.exp(dt / tau)


def dyp_dtau(tau, r_freeze, dt):
    """dY_p/dtau_n for the one-zone model [per second]."""
    r = r_freeze * math.exp(-dt / tau)
    return 2.0 * r * dt / ((1.0 + r) ** 2 * tau ** 2)


def neutron_lifetime_scan(dts=(200.0, 500.0, 700.0, 1000.0), yp=0.2470):
    tau_pdg = TAU_PDG[0]
    out = []
    for dt in dts:
        rf = calibrate_r_freeze(yp, tau_pdg, dt)
        sens = dyp_dtau(tau_pdg, rf, dt)
        dtau_beam_bottle = TAU_BEAM[0] - TAU_BOTTLE[0]
        out.append({
            "dt": dt,
            "r_freeze": rf,
            "sens": sens,                                   # per s
            "dY_beam_bottle": sens * dtau_beam_bottle,
            "dY_pdg_1sigma": sens * TAU_PDG[1],
        })
    return out


def report():
    line = "=" * 74
    print(line)
    print("A001 / phase4-consensus : provenance attack on 'Y_p = 0.247'")
    print(line)

    # [A] empirical precision
    ma = meta_analysis(OBSERVED_YP)
    print("\n[A] Published H II-region determinations of Y_p")
    for x, s, lab in OBSERVED_YP:
        print(f"    {x:.4f} +/- {s:.4f}   {lab}")
    print(f"    inverse-variance mean      = {ma['mean']:.5f}")
    print(f"    naive error                = {ma['err_naive']:.5f}")
    print(f"    chi^2 / ndf                = {ma['chi2']:.3f} / {ma['ndf']} "
          f"= {ma['chi2_ndf']:.2f}")
    print(f"    p-value (scatter by chance)= {ma['p']:.4f}")
    print(f"    PDG scale factor S         = {ma['scale']:.3f}")
    print(f"    empirical error (S-scaled) = {ma['err_scaled']:.5f}")
    print(f"    => EMPIRICAL Y_p = {ma['mean']:.4f} +/- {ma['err_scaled']:.4f}")

    # [B] theory precision and consistency
    print("\n[B] Theory prediction (BBN at Planck 2018 CMB baryon density)")
    print(f"    Y_p(theory) = {PLANCK_YP:.4f} +/- {PLANCK_YP_SIGMA:.4f}")
    diff = ma["mean"] - PLANCK_YP
    sig = math.hypot(ma["err_scaled"], PLANCK_YP_SIGMA)
    print(f"    empirical - theory = {diff:+.5f}  ({diff/sig:+.2f} sigma)")
    print(f"    empirical error / theory error = {ma['err_scaled']/PLANCK_YP_SIGMA:.1f}x")
    print("    => the 0.247 value and its 0.0003 precision are THEORY, not measurement.")

    # [C] neutron-lifetime theory systematic
    print("\n[C] Neutron-lifetime puzzle propagated through a calibrated BBN model")
    print(f"    bottle {TAU_BOTTLE[0]} +/- {TAU_BOTTLE[1]} s ; "
          f"beam {TAU_BEAM[0]} +/- {TAU_BEAM[1]} s ; "
          f"PDG {TAU_PDG[0]} +/- {TAU_PDG[1]} s")
    print(f"    beam - bottle = {TAU_BEAM[0]-TAU_BOTTLE[0]:+.1f} s "
          f"(~{(TAU_BEAM[0]-TAU_BOTTLE[0])/math.hypot(TAU_BOTTLE[1],TAU_BEAM[1]):.1f} sigma)")
    print(f"    {'dt_eff [s]':>10s} {'r_freeze':>10s} {'dY/dtau [/s]':>14s} "
          f"{'dY(beam-bottle)':>16s} {'dY(PDG 1sig)':>13s}")
    for row in neutron_lifetime_scan():
        print(f"    {row['dt']:10.0f} {row['r_freeze']:10.4f} {row['sens']:14.3e} "
              f"{row['dY_beam_bottle']:16.5f} {row['dY_pdg_1sigma']:13.5f}")
    print("    => lifetime theory systematic is O(0.001), sub-dominant to the")
    print("       ~0.004 empirical H II-region systematic, but NOT negligible.")

    print("\nCONCLUSION")
    print("  The consensus clause 'Y_p = 0.247' is a BBN prediction at CMB baryon")
    print("  density, quoted at theory precision. Empirically Y_p is known only to")
    print(f"  ~+/-{ma['err_scaled']:.4f}. The two agree at {abs(diff)/sig:.1f} sigma. "
          "The statement is correct;")
    print("  its epistemic label ('measured') is the weakest assumption.")
    return ma


if __name__ == "__main__":
    report()
