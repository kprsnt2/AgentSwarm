"""
cosmogenesis_age_model_dependence_engine.py

PRIORITY-DIRECTIVE ARTIFACT (Phase 4 consensus, generation 0).
Agent: Raman (A002).

Weakest-assumption attack: the ratified consensus opens with the categorical
claim "The universe began 13.8 billion years ago". That number is NOT a direct
measurement of a beginning. It is the integral of an ASSUMED expansion history:

        t_0 = (1/H0) * Integral_0^inf  dz / [ (1+z) E(z) ]

with E(z) fixed by a chosen matter content and dark-energy equation of state.
This engine computes t_0 for several empirically live models, using only
published central values and standard textbook cosmology, and reports how much
the "13.8 Gyr" moves under assumptions the consensus itself lists as open.

No new data are invented. Every input is an established published value and is
labelled. Outputs are exact numerical integrals of the stated Friedmann models.

All physics is pure-Python (no numpy/scipy required).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List

# ---------------------------------------------------------------------------
# Constants (CODATA / IAU)
# ---------------------------------------------------------------------------
MPC_IN_KM = 3.0856775814913673e19      # 1 Mpc in km
SEC_PER_GYR = 3.15576e16               # seconds per Julian gigayear
C_KM_S = 299792.458                    # speed of light, km/s


def hubble_time_gyr(h0: float) -> float:
    """Hubble time 1/H0 in Gyr for H0 in km/s/Mpc."""
    return (MPC_IN_KM / (h0 * SEC_PER_GYR))


# ---------------------------------------------------------------------------
# Expansion-rate models
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class LCDM:
    """Flat Lambda-CDM. Omega_DE = 1 - Omega_m - Omega_r."""
    H0: float
    Omega_m: float
    Omega_r: float = 9.15e-5
    name: str = "flat LCDM"

    def E(self, z: float) -> float:
        om, orr = self.Omega_m, self.Omega_r
        ode = 1.0 - om - orr
        return (om * (1.0 + z) ** 3 + orr * (1.0 + z) ** 4 + ode) ** 0.5


@dataclass(frozen=True)
class CPL:
    """Flat w0-wa (Chevallier-Polarski-Linder) dynamical dark energy.

    rho_DE(z)/rho_DE(0) = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))
    """
    H0: float
    Omega_m: float
    w0: float
    wa: float
    Omega_r: float = 9.15e-5
    name: str = "flat CPL"

    def E(self, z: float) -> float:
        om, orr = self.Omega_m, self.Omega_r
        ode = 1.0 - om - orr
        de = (1.0 + z) ** (3.0 * (1.0 + self.w0 + self.wa)) * \
             pow(2.718281828459045, -3.0 * self.wa * z / (1.0 + z))
        return (om * (1.0 + z) ** 3 + orr * (1.0 + z) ** 4 + ode * de) ** 0.5


# ---------------------------------------------------------------------------
# Age integral via x = z/(1+z) mapping (removes the infinite upper limit)
# ---------------------------------------------------------------------------
def age_gyr(model) -> float:
    """
    t_0 = (1/H0) * Integral_0^1 dx / [ (1-x) * E(x) ],  x = z/(1+z).
    The joint integrand is regular at x=1 (radiation era) and x=0.
    Composite Simpson with N subdivisions.
    """
    N = 400000
    if N % 2:
        N += 1
    h = 1.0 / N

    def f(x: float) -> float:
        # x -> 1 is z -> infinity (radiation era); integrand -> (1-x)/sqrt(Omega_r) -> 0.
        if x >= 1.0:
            return 0.0
        z = x / (1.0 - x)
        return 1.0 / ((1.0 - x) * model.E(z))

    s = f(0.0) + f(1.0)
    for i in range(1, N):
        x = i * h
        s += (4.0 if i % 2 else 2.0) * f(x)
    integral = s * h / 3.0
    return hubble_time_gyr(model.H0) * integral


# ---------------------------------------------------------------------------
# Published empirical anchors (all established values)
# ---------------------------------------------------------------------------
PLANCK18 = dict(H0=67.36, Omega_m=0.3153)          # Planck 2018 TT,TE,EE+lowE+lensing
SH0ES22 = dict(H0=73.04)                           # Riess et al. 2022
OMEGA_M_H2_PLANCK = 0.1430                         # Planck 2018 physical matter density
DESI_CPL = dict(w0=-0.827, wa=-0.750)              # DESI DR1 2024 BAO+CMB+Pantheon+


def omega_m_for_h(h: float) -> float:
    """Omega_m = omega_m h^2 / h^2 (keeps physical matter density fixed)."""
    return OMEGA_M_H2_PLANCK / (h * h)


def run() -> Dict[str, object]:
    out: Dict[str, object] = {}

    # 1) Baseline: exactly the consensus's own model.
    base = LCDM(H0=PLANCK18["H0"], Omega_m=PLANCK18["Omega_m"],
                name="Planck18 LCDM (consensus baseline)")
    t_base = age_gyr(base)
    out["baseline"] = (base.name, t_base)

    # 2) Local (SH0ES) H0 in flat LCDM, physical matter density fixed.
    h_local = SH0ES22["H0"] / 100.0
    local = LCDM(H0=SH0ES22["H0"], Omega_m=omega_m_for_h(h_local),
                 name="SH0ES22 H0 in flat LCDM (same omega_m h^2)")
    t_local = age_gyr(local)
    out["local"] = (local.name, local.Omega_m, t_local)

    # 2b) The "age crisis": SH0ES H0 with Planck Omega_m held fixed.
    naive = LCDM(H0=SH0ES22["H0"], Omega_m=PLANCK18["Omega_m"],
                 name="SH0ES22 H0 + Planck Omega_m (naive)")
    t_naive = age_gyr(naive)
    out["naive"] = (naive.name, t_naive)

    # 3) Dynamical dark energy (DESI DR1 CPL), Planck H0/Omega_m.
    cpl = CPL(H0=PLANCK18["H0"], Omega_m=PLANCK18["Omega_m"],
              w0=DESI_CPL["w0"], wa=DESI_CPL["wa"],
              name="Planck18 + DESI DR1 CPL dynamical DE")
    t_cpl = age_gyr(cpl)
    out["cpl"] = (cpl.name, t_cpl)

    # 4) Pure de Sitter (w=-1) sanity check equals baseline by construction.
    # 5) Phantom and quintessence bracketing (w0 fixed, wa=0).
    models = {}
    for w0 in (-0.85, -1.0, -1.15):
        m = CPL(H0=PLANCK18["H0"], Omega_m=PLANCK18["Omega_m"],
                w0=w0, wa=0.0, name=f"constant w0={w0}")
        models[m.name] = age_gyr(m)
    out["w_bracket"] = models

    # 6) Local derivative sensitivities of t0 at the baseline.
    dH = 0.5
    t_plus = age_gyr(LCDM(H0=PLANCK18["H0"] + dH, Omega_m=PLANCK18["Omega_m"]))
    t_minus = age_gyr(LCDM(H0=PLANCK18["H0"] - dH, Omega_m=PLANCK18["Omega_m"]))
    dt_dH0 = (t_plus - t_minus) / (2.0 * dH)
    out["dt_dH0_gyr_per_unit"] = dt_dH0  # Gyr per (km/s/Mpc)

    dom = 0.01
    t_plus = age_gyr(LCDM(H0=PLANCK18["H0"], Omega_m=PLANCK18["Omega_m"] + dom))
    t_minus = age_gyr(LCDM(H0=PLANCK18["H0"], Omega_m=PLANCK18["Omega_m"] - dom))
    dt_dom = (t_plus - t_minus) / (2.0 * dom)
    out["dt_dOmega_m_gyr_per_unit"] = dt_dom

    # 7) 1-sigma propagated age uncertainty from Planck H0 and Omega_m
    #    (Planck 2018: sigma_H0=0.54, sigma_Om=0.0073), correlated terms ignored
    #    -> conservative upper bound on the model-internal error.
    import math
    sig = math.sqrt((dt_dH0 * 0.54) ** 2 + (dt_dom * 0.0073) ** 2)
    out["sigma_age_planck_gyr"] = sig

    # 8) Deltas relative to the quoted 13.8 Gyr.
    out["delta_local_vs_base_gyr"] = t_local - t_base
    out["delta_naive_vs_base_gyr"] = t_naive - t_base
    out["delta_cpl_vs_base_gyr"] = t_cpl - t_base
    out["delta_local_vs_quoted_gyr"] = t_local - 13.8
    out["delta_naive_vs_quoted_gyr"] = t_naive - 13.8
    out["delta_cpl_vs_quoted_gyr"] = t_cpl - 13.8
    return out


def _fmt() -> str:
    r = run()
    lines: List[str] = []
    lines.append("=" * 78)
    lines.append("AGE OF THE UNIVERSE: MODEL DEPENDENCE OF '13.8 Gyr'")
    lines.append("=" * 78)
    lines.append(f"{'model':<52}{'t0 [Gyr]':>12}{'delta':>12}")
    lines.append("-" * 78)

    name, t = r["baseline"]
    lines.append(f"{name:<52}{t:>12.4f}{0.0:>+12.4f}")
    name, om, t = r["local"]
    lines.append(f"{name:<52}{t:>12.4f}{r['delta_local_vs_base_gyr']:>+12.4f}")
    name, t = r["naive"]
    lines.append(f"{name:<52}{t:>12.4f}{r['delta_naive_vs_base_gyr']:>+12.4f}")
    name, t = r["cpl"]
    lines.append(f"{name:<52}{t:>12.4f}{r['delta_cpl_vs_base_gyr']:>+12.4f}")
    for name, t in r["w_bracket"].items():
        lines.append(f"{name:<52}{t:>12.4f}{t - r['baseline'][1]:>+12.4f}")

    lines.append("-" * 78)
    lines.append(f"dt0/dH0               = {r['dt_dH0_gyr_per_unit']:+.4f} Gyr per (km/s/Mpc)")
    lines.append(f"dt0/dOmega_m          = {r['dt_dOmega_m_gyr_per_unit']:+.4f} Gyr per unit Omega_m")
    lines.append(f"Planck 1-sigma age    = +/- {r['sigma_age_planck_gyr']:.4f} Gyr (H0, Omega_m only)")
    lines.append("")
    lines.append(f"SH0ES-calibrated LCDM is {r['delta_local_vs_quoted_gyr']:+.4f} Gyr vs the quoted 13.8 Gyr.")
    lines.append(f"Naive SH0ES H0 + Planck Omega_m is {r['delta_naive_vs_quoted_gyr']:+.4f} Gyr vs the quoted 13.8 Gyr.")
    lines.append(f"DESI CPL dynamical DE is {r['delta_cpl_vs_quoted_gyr']:+.4f} Gyr vs the quoted 13.8 Gyr.")
    lines.append("=" * 78)
    return "\n".join(lines)


if __name__ == "__main__":
    print(_fmt())
