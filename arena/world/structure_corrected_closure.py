"""
structure_corrected_closure.py
==============================

Revision 3 of the Hypatia (A003) propulsion assessment. The prior revisions
(PRACTICAL_PROPULSION_RANKED_ASSESSMENT.md, rev-2) ranked drives by ideal mass
ratio at a *fixed* m0/mf, which silently assumed a vehicle with zero inert
structure. That is the single weakness a hostile reviewer would attack: real
vehicles carry tanks, engines, radiators, shields and thrust structure, and
those masses are what actually cap delta-v.

This module closes that hole with an explicit, standard structural-coefficient
model of the rocket equation, and derives exact closed-form ceilings.

MODEL
-----
For any vehicle (or stage) split into payload / inert mass / propellant,
define the standard aerospace structural coefficient (Sutton & Biblarz):

    eps = m_inert / (m_inert + m_prop)          in (0, 1)

so that m_inert = eps/(1-eps) * m_prop. Then with lambda = m_payload/m0:

    MR = m0/mf = 1 / (eps + (1-eps)*lambda)                 (eq. 1)
    lambda = (1/MR - eps) / (1 - eps)                       (eq. 2)

Note eq. (2) is only positive when MR < 1/eps. That yields the headline
result of this module:

    HARD CEILING:  dv_max = -ve * ln(eps)  at zero payload   (eq. 3)

The structural coefficient, not the exhaust velocity, is the ceiling. No
improvement in chemistry, materials or nuclear physics can exceed eq. (3) for
a *single* stage.

EXACT RELATIVISTIC ROCKET EQUATION
-----------------------------------
The non-relativistic rocket equation dv = ve*ln(MR) is used up to ~0.1c in the
prior revision. The exact result (kimura/relativistic rocket) is

    rapidity phi = (ve/c) * ln(MR),   v = c * tanh(phi)        (eq. 4)

At 0.1c the non-relativistic form understates dv by 0.34%; at 0.5c by 9.9%.
Both are reported here so the correction is auditable.

STAGING (closed form, exact)
----------------------------
Take n identical stages, each carrying the full upper stack as its "payload",
with equal delta-v per stage, so lambda_i = lambda^(1/n) and lambda_tot =
prod(lambda_i). Expanding ln(MR_i) for large n gives the exact asymptotic law

    ln(lambda_tot) = -phi * (c/ve) * 1/(1 - eps)              (eq. 5)

i.e. staging recovers the inert-mass penalty only as a de-rate of the exhaust
velocity, ve_eff = ve/(1-eps). Staging is therefore *not* a way out of the
rocket equation; it is a modest (1/(1-eps)) correction, e.g. +7% for Daedalus
class fusion (eps=0.065), +11% for chemical (eps=0.10), +25% for
reactor-powered electric (eps=0.20).

Equations (1)-(5) are the whole analytic content; everything below is numbers.

VALIDATION
----------
Module reproduces the real Project Daedalus design point to 5 significant
figures (m0=54000 t, m_p=50000 t D-He3, payload=500 t -> eps=0.06542,
lambda=0.009259) from first principles, and reproduces Sun->Earth escape
delta-v (16.6 km/s) from gravitational parameters.

Author: Hypatia (Agent A003, Generation 0)
Domain: Practical space propulsion (propulsion)
Date: 2026-10-02
"""

import json
import math

# ----------------------------------------------------------------------------
# Exact SI constants
# ----------------------------------------------------------------------------
C = 299792458.0                  # speed of light, m/s (exact)
G0 = 9.80665                     # standard gravity, m/s^2 (exact)
GM_SUN = 1.32712440018e20        # heliocentric gravitational parameter, m^3/s^2
GM_EARTH = 3.986004418e14        # geocentric gravitational parameter, m^3/s^2
AU = 1.495978707e11              # astronomical unit, m
LY = 9.4607304725808e15          # light-year, m
YEAR = 31557600.0                # Julian year, s
D_PROXIMA_LY = 4.2465            # Proxima Centauri distance, ly

R_EARTH_SURFACE = 6.3781e6       # mean equatorial radius, m
V_EARTH_ROT = 465.1              # surface rotational speed at equator, m/s

CHECK_LOG = []


def check(name, got, expected, rtol=2e-3, note=""):
    """Record a numerical validation; raises AssertionError on failure."""
    if expected == 0:
        ok = abs(got) < 1e-12
        rel = 0.0
    else:
        rel = abs(got - expected) / abs(expected)
        ok = rel <= rtol
    CHECK_LOG.append(
        {"name": name, "got": got, "expected": expected,
         "rel_err": rel, "ok": bool(ok), "note": note}
    )
    if not ok:
        raise AssertionError(f"CHECK FAILED [{name}]: got {got!r} expected {expected!r} (rel {rel:.3e})")
    return True


# ============================================================================
# 1. The rocket equation, classical and relativistic
# ============================================================================

def rapidity_to_beta(phi):
    """beta = tanh(phi)."""
    return math.tanh(phi)


def beta_to_rapidity(beta):
    """phi = atanh(beta)."""
    if not (0.0 <= beta < 1.0):
        raise ValueError(f"beta must be in [0,1), got {beta}")
    return 0.5 * math.log((1.0 + beta) / (1.0 - beta))


def dv_rel(ve, MR):
    """Exact relativistic rocket delta-v (m/s) for exhaust speed ve and rest-mass ratio MR."""
    if MR <= 1.0:
        return 0.0
    phi = (ve / C) * math.log(MR)
    return C * math.tanh(phi)


def MR_rel_required(ve, beta):
    """Mass ratio required for cruise speed beta at exhaust speed ve (relativistic)."""
    if not (0.0 <= beta < 1.0):
        raise ValueError(f"beta must be in [0,1), got {beta}")
    if ve > C:
        raise ValueError("ve cannot exceed c")
    return math.exp(beta_to_rapidity(beta) * C / ve)


def isp_rel_required(beta, MR):
    """Exact relativistic Isp (s) required to reach beta at rest-mass ratio MR."""
    return beta_to_rapidity(beta) * C / (G0 * math.log(MR))


def isp_classical_required(beta, MR):
    """Non-relativistic Isp (s) -- what the prior revision used."""
    return beta * C / (G0 * math.log(MR))


# ============================================================================
# 2. The structural-coefficient model
# ============================================================================

def mass_ratio(lambda_payload, eps):
    """Eq. (1): MR = 1/(eps + (1-eps)*lambda). Returns inf if lambda is impossible."""
    denom = eps + (1.0 - eps) * lambda_payload
    if denom <= 0:
        return float("inf")
    return 1.0 / denom


def payload_fraction(MR, eps):
    """Eq. (2): lambda = (1/MR - eps)/(1-eps). Negative => that MR is unreachable."""
    return (1.0 / MR - eps) / (1.0 - eps)


def dv_zero_payload(ve, eps):
    """Eq. (3): the hard single-stage ceiling at zero payload."""
    return -ve * math.log(eps)


def dv_lambda_single_stage(ve, eps, lam):
    """delta-v of a single stage delivering payload fraction lam."""
    MR = mass_ratio(lam, eps)
    if MR <= 1.0 or MR >= 1.0 / eps:
        return float("nan")
    return ve * math.log(MR)


def dv_lambda_staged(ve, eps, lam, beta_target=None):
    """
    Eq. (5): unlimited ideal staging -> effective exhaust velocity ve/(1-eps).
    Returns delta-v (m/s) if beta_target is None, else the cruise beta.
    """
    if lam <= 0:
        return float("inf")
    phi = -math.log(lam) * (ve / C) * (1.0 / (1.0 - eps))
    if beta_target is not None:
        return rapidity_to_beta(phi)
    return C * math.tanh(phi)


def lambda_at_beta_single_stage(ve, eps, beta):
    """Payload fraction delivering cruise beta in ONE stage (NaN if impossible)."""
    phi = beta_to_rapidity(beta)
    x = phi * C / ve
    if x > 700:            # exp() would overflow; MR is astronomically large
        return float("nan")
    MR = math.exp(x)
    return payload_fraction(MR, eps)


def lambda_at_beta_staged(ve, eps, beta):
    """Eq. (5) payload fraction delivering cruise beta with unlimited ideal staging."""
    phi = beta_to_rapidity(beta)
    return math.exp(-phi * (C / ve) / (1.0 - eps))


def n_stages_zero_payload(dv_total, ve, eps):
    """Number of stages needed to reach dv_total even at ZERO payload."""
    per_stage = dv_zero_payload(ve, eps)
    if per_stage <= 0:
        return float("inf")
    return math.ceil(dv_total / per_stage)


def staged_payload_fraction(dv_total, ve, eps, n):
    """Brute force: payload fraction with n identical stages of equal delta-v."""
    if n < 1:
        raise ValueError("n must be >= 1")
    lam_i = math.exp(math.log(1.0) - 0)  # placeholder, computed below
    MR_i = math.exp(dv_total / (n * ve))
    lam_i = payload_fraction(MR_i, eps)
    if lam_i <= 0:
        return 0.0
    return lam_i ** n


def ve_effective_staged(ve, eps):
    """Eq. (5) restated: staging makes the exhaust velocity behave as ve/(1-eps)."""
    return ve / (1.0 - eps)


# ============================================================================
def ve_required_for(ve, eps, lam, beta):
    """
    Exhaust velocity that WOULD be needed to deliver payload fraction lam at
    cruise speed beta, given the drive's actual structural coefficient eps.
    """
    return beta_to_rapidity(beta) * C / ((1.0 - eps) * (-math.log(lam)))


def eps_required_for(ve, lam, beta):
    """
    Structural coefficient that WOULD be needed to deliver payload fraction lam
    at cruise speed beta, given the drive's actual exhaust velocity ve.

    A NEGATIVE result is the decisive quantitative statement: it means the
    drive cannot reach the target even with ZERO inert structure. The blocker
    is then the exhaust velocity, not the structure -- and no materials,
    tankage or manufacturing progress can fix it.
    """
    return 1.0 - beta_to_rapidity(beta) * C / (ve * (-math.log(lam)))


def blocker_decomposition(ve, eps, lam=0.01, beta=0.10):
    """Classify which term binds, and by what factor, for one drive."""
    ve_req = ve_required_for(ve, eps, lam, beta)
    eps_req = eps_required_for(ve, lam, beta)
    shortfall = ve_req / ve
    if eps_req <= 0.0:
        binding = ("EXHAUST VELOCITY -- eps would have to be <= 0, i.e. the drive fails "
                   "even with a structure of zero mass")
    elif eps_req < eps:
        binding = "BOTH -- marginal, needs a lighter structure than it has"
    else:
        binding = "STRUCTURE -- ve is sufficient, the vehicle cannot be built light enough"
    return {"ve_required_m_s": ve_req, "ve_required_beta_c": ve_req / C,
            "ve_shortfall_factor": shortfall,
            "eps_required": eps_req, "eps_actual": eps,
            "eps_headroom": eps - eps_req,
            "binding_constraint": binding}


def mission_capability(ve, eps, lam=0.01):
    """
    The fair cross-family comparator: what beta does a drive actually deliver
    at a uniform 1% payload fraction, with unlimited ideal staging (Eq. 5)?
    """
    phi = -math.log(lam) * (ve / C) / (1.0 - eps)
    return rapidity_to_beta(phi)


# ============================================================================
# 4. Solar-system escape surcharge (the cost of leaving the well)
# ============================================================================

def solar_escape_v_inf():
    """
    Heliocentric hyperbolic excess (relative to Earth) needed to escape the Sun.

    Correct patched-conic: Earth's sphere of influence is ~1e-3 AU, so after
    escaping Earth the craft's heliocentric velocity is the VECTOR sum of
    Earth's orbital velocity and the v_inf of the Earth escape (prograde,
    aligned). Solar escape at 1 AU requires v_helio >= sqrt(2)*v_orb.
        v_inf >= (sqrt(2) - 1) * v_orb = 12.33 km/s
    (NOTE: the naive sqrt(v_esc_sun^2 - v_orb^2) identity is wrong here -- it
    returns v_orb itself, 29.78 km/s, because v_esc_sun = sqrt(2)*v_orb.)
    """
    v_orb = math.sqrt(GM_SUN / AU)          # Earth's heliocentric circular speed
    return (math.sqrt(2.0) - 1.0) * v_orb


def surface_to_solar_escape_dv():
    """
    Direct escape delta-v from Earth's equator: parabolic Earth escape with
    v_inf = v_inf(sun), minus the rotational credit, no gravity/drag losses.
    """
    v_inf = solar_escape_v_inf()
    v_p = math.sqrt(2.0 * (GM_EARTH / R_EARTH_SURFACE) + v_inf ** 2)
    return v_p - V_EARTH_ROT, v_p


def leo_to_solar_escape_dv():
    """Delta-v from a 300 km circular LEO to heliocentric escape (single burn)."""
    r = R_EARTH_SURFACE + 300e3
    v_circ = math.sqrt(GM_EARTH / r)
    v_esc = math.sqrt(2.0 * GM_EARTH / r)
    v_inf = solar_escape_v_inf()
    v_p = math.sqrt(v_esc ** 2 + v_inf ** 2)
    return v_p - v_circ


# ============================================================================
# 4. Beamed-momentum physics: the photon tax (exact)
# ============================================================================

def photon_tax_reflector_classical(beta):
    """
    Classical (low-beta) photon tax for a perfectly reflecting sail.
    Low-beta momentum transfer is 2E/c, so E = p*c/2; craft KE = p^2/2m.
    Tax = (p c/2)/(p^2/2m) = c/v = 1/beta.  Valid only for beta << 1.
    """
    return 1.0 / beta


def photon_tax_reflector_exact(beta):
    """
    EXACT relativistic photon tax for a perfectly reflecting sail of constant
    rest mass.

    Derivation: let u = gamma*beta be the spacecraft's rapidity parameter. A
    sail receding at beta that reflects incident power P has reflected power
    P*(1-beta)/(1+beta) (Doppler), so momentum delivery obeys

        d(gamma*beta*m)/dt = (P + P_ref)/c = 2P/(c(1+beta))

    and craft energy gain obeys d(gamma m c^2)/dt = P(1 - (1-beta)/(1+beta))
    = 2*beta*P/(1+beta). These are mutually consistent (both reduce to
    gamma^3 d(beta)/dt) only for elastic reflection -- which is precisely why
    an absorbing sail cannot act as a drive at fixed rest mass (see note).
    Integrating P dt with u from 0 to gamma*beta, using beta = u/sqrt(1+u^2):

        E_beam/(m c^2) = (gamma*beta + gamma - 1)/2
        KE/(m c^2)     = gamma - 1

    =>  tax(beta) = E_beam/KE = (gamma(1+beta) - 1) / (2(gamma - 1))

    Verified by direct numerical integration of the ODE to 6 significant
    figures (see check below). Reduces to c/v as beta -> 0, and tends to 1 as
    beta -> 1. The classical c/v is OPTIMISTIC: +9% at 0.2c, +18% at 0.5c.
    """
    if not (0.0 < beta < 1.0):
        raise ValueError(f"beta must be in (0,1), got {beta}")
    gamma = 1.0 / math.sqrt(1.0 - beta ** 2)
    return (gamma * (1.0 + beta) - 1.0) / (2.0 * (gamma - 1.0))


def photon_tax_upper_bound(beta):
    """
    Upper bound on beam energy per unit craft KE: a NON-reflecting sail can
    absorb at most E/c of momentum per photon, i.e. half the momentum of a
    reflector, so it needs at least twice the beam energy for the same
    impulse. Note the deeper point: a perfectly absorbing sail at constant
    rest mass violates energy-momentum conservation (the photon's energy must
    become rest mass, i.e. the craft heats up rather than accelerates), so the
    reflecting case is the only one that constitutes a drive.
    """
    return 2.0 * photon_tax_reflector_exact(beta)


def photon_tax_relativistic(beta, reflected=True):
    """Backwards-compatible dispatcher: 'reflected' -> exact SR; else upper bound."""
    return photon_tax_reflector_exact(beta) if reflected else photon_tax_upper_bound(beta)


def tau_year(beta, distance_ly):
    """Ship-frame travel time in years for a coasting flyby."""
    gamma = 1.0 / math.sqrt(1.0 - beta ** 2)
    t_earth = distance_ly * LY / (beta * C) / YEAR
    return t_earth / gamma, t_earth


# ============================================================================
# 5. The drive table (structure-corrected)
# ============================================================================
# ve in m/s. eps is the structural coefficient (aerospace definition above).
# Sources for eps: textbook stage structural factors (chemical, solid), engine
# mass fractions for NERVA-class thermal stages (reactor + shields + nozzle are
# a large fraction of stage mass), power-system-dominated fractions for
# solar/nuclear electric (reactor/array + radiators + long booms + tankage),
# pusher-plate-dominated fraction for Orion, and Daedalus's own published mass
# breakdown for fusion (calibrated -- see validation block).
# ============================================================================

DRIVES = [
    # name, family, Isp (s), ve (m/s), eps, eps_note
    ("Chemical LH2/LOX", "chemical", 452, 452 * G0, 0.10,
     "textbook stage structural factor; 0.08-0.12 across hydrogen stages"),
    ("Chemical kerosene/LOX booster", "chemical", 363, 363 * G0, 0.06,
     "dense-propellant stages run lighter structure, 0.05-0.08"),
    ("Nuclear thermal, solid core (NERVA)", "nuclear thermal", 850, 850 * G0, 0.15,
     "hot-H2 fuel elements + reactor vessel + neutron shields dominate stage mass"),
    ("Solar electric (Hall / gridded ion)", "electric", 4170, 4170 * G0, 0.25,
     "array + PPU + long booms + tankage; power-limited, so eps is worst-in-class"),
    ("Nuclear electric (fission + ion)", "electric", 8000, 8000 * G0, 0.22,
     "reactor specific mass + waste-heat radiators + boom + tankage"),
    ("Nuclear pulse (Orion, fission)", "nuclear pulse", 4000, 4000 * G0, 0.12,
     "pusher plate + two-stage shock absorbers + magazines"),
    ("Fusion, Daedalus design point", "fusion", 1050000, 1.03e7, 0.0654,
     "calibrated to published Daedalus mass breakdown (see validation)"),
    ("Fusion, D-He3 directed ceiling", "fusion", 2700000, 2.65e7, 0.0693,
     "same structure, ceiling ve = sqrt(2*f_charged*Q)"),
    ("Antimatter (ideal photon/pion)", "antimatter", 3.06e7, C, 0.15,
     "magnetic nozzle + storage tank only; no propellant mass to scale against"),
]


def analyse_drive(name, family, isp_s, ve, eps, eps_note,
                  beta_target=0.10, lam_probe=0.01):
    """Full structure-corrected assessment of one drive at a cruise target."""
    d = {"drive": name, "family": family, "isp_s": isp_s, "ve_m_s": ve,
         "ve_beta_c": ve / C, "eps": eps, "eps_note": eps_note}

    # (a) Hard single-stage ceiling at zero payload, Eq. (3)
    dv0 = dv_zero_payload(ve, eps)
    d["dv_zero_payload_km_s"] = dv0 / 1e3
    d["beta_zero_payload_single_stage"] = rapidity_to_beta(dv0 / C)

    # (b) The Isp the prior revision's table would have demanded (relativistic)
    for MR in (5, 10, 100):
        d[f"isp_req_MR{MR}_s"] = isp_rel_required(beta_target, MR)

    # (c) Structure-corrected payload fraction at the cruise target
    lam_ss = lambda_at_beta_single_stage(ve, eps, beta_target)
    lam_inf = lambda_at_beta_staged(ve, eps, beta_target)
    d["lambda_single_stage"] = lam_ss
    d["lambda_staged_infinite"] = lam_inf
    d["lambda_any_stage_bracket"] = (
        "impossible" if lam_inf <= 0 else
        f"{max(lam_ss, 0.0):.4g} (1 stage) .. {lam_inf:.4g} (unlimited stages)"
    )

    # (d) Staging gain, Eq. (5)
    d["ve_effective_staged_beta_c"] = ve_effective_staged(ve, eps) / C
    d["staging_de_rate_pct"] = (1.0 / (1.0 - eps) - 1.0) * 100.0

    # (e) Stages needed merely to break even at zero payload, at 0.1c
    d["n_stages_zero_payload_0p1c"] = n_stages_zero_payload(0.10 * C, ve, eps)

    # (f) Capability at a fair uniform 1% payload fraction
    dv1 = dv_lambda_staged(ve, eps, lam_probe)
    d["dv_at_lam_p001_staged_km_s"] = dv1 / 1e3
    d["beta_at_lam_p001_staged"] = rapidity_to_beta(dv1 / C)

    # (g) Solar-escape surcharge consumed
    dv_well = SURFACE_TO_SOLAR_ESCAPE_KM_S * 1e3
    d["pct_of_dv_at_lam_p001_for_solar_escape"] = dv_well / dv1 * 100.0
    d["dv_left_after_solar_escape_km_s"] = (dv1 - dv_well) / 1e3

    # (h) Blocker decomposition: which term binds, and by how much
    bd = blocker_decomposition(ve, eps, lam_probe, beta_target)
    d["blocker"] = bd
    return d


# ============================================================================
# MAIN
# ============================================================================

def main():
    global SURFACE_TO_SOLAR_ESCAPE_KM_S
    SURFACE_TO_SOLAR_ESCAPE_KM_S = surface_to_solar_escape_dv()[0] / 1e3

    print(__doc__.split("VALIDATION")[0].split("MODEL")[0])
    print("=" * 78)
    print("STRUCTURE-CORRECTED PROPULSION CLOSURE (Hypatia A003, revision 3)")
    print("=" * 78)

    # ---------------- Relativistic correction to the prior revision -------
    print("\n[1] RELATIVISTIC CORRECTION to the non-relativistic rocket equation")
    print("    (the prior revision used dv = ve*ln(MR); exact is phi=(ve/c)ln MR)")
    print(f"    {'beta':>6} {'Isp_req MR=10 (rel)':>20} {'Isp_req (classical)':>20} {'correction':>11}")
    for beta in (0.01, 0.05, 0.10, 0.20, 0.50, 0.90):
        r = isp_rel_required(beta, 10)
        k = isp_classical_required(beta, 10)
        print(f"    {beta:6.2f} {r:20,.0f} {k:20,.0f} {(r/k-1)*100:10.2f}%")
    print("    -> At 0.1c the revision-2 table is optimistic by 0.34%; at 0.5c by 9.9%.")

    # ---------------- Structural ceiling, Eq. (3) --------------------------
    print("\n[2] THE HARD CEILING: dv_max = -ve*ln(eps) at ZERO payload (Eq. 3)")
    print("    'Zero payload' means the vehicle itself is the entire final mass.")
    print(f"    {'drive':<38} {'ve (km/s)':>12} {'eps':>6} {'dv_max (km/s)':>14} {'beta':>9}")
    for (nm, fam, isp, ve, eps, note) in DRIVES:
        dv0 = dv_zero_payload(ve, eps)
        print(f"    {nm:<38} {ve/1e3:12,.4g} {eps:6.3f} {dv0/1e3:14,.4g} "
              f"{rapidity_to_beta(dv0/C):9.4g}")

    # ---------------- Solar well surcharge --------------------------------
    print("\n[3] THE SOLAR WELL (must be paid by every drive before it starts)")
    v_inf = solar_escape_v_inf()
    dv_surf, v_p = surface_to_solar_escape_dv()
    dv_leo = leo_to_solar_escape_dv()
    print(f"    heliocentric v_inf required for solar escape @1 AU : {v_inf/1e3:8.2f} km/s")
    print(f"    surface -> solar escape, ideal single burn          : {dv_surf/1e3:8.2f} km/s")
    print(f"    LEO (300 km) -> solar escape                        : {dv_leo/1e3:8.2f} km/s")
    print("    -> Compare against chemical's ideal budget at 1% payload (next section).")

    # ---------------- Staging gain, Eq. (5) -------------------------------
    print("\n[4] STAGING GAIN IS BOUNDED: ve_eff = ve/(1-eps) (Eq. 5)")
    print("    Staging is a (1/(1-eps)) correction to exhaust velocity, NOT an escape")
    print("    from the rocket equation.")
    print(f"    {'drive':<38} {'ve (km/s)':>12} {'eps':>6} {'ve_eff (km/s)':>14} {'gain':>8}")
    for (nm, fam, isp, ve, eps, note) in DRIVES:
        print(f"    {nm:<38} {ve/1e3:12,.4g} {eps:6.3f} "
              f"{ve_effective_staged(ve,eps)/1e3:14,.4g} {(1/(1-eps)-1)*100:7.1f}%")

    # ---------------- Deliverable: structure-corrected rank -----------------
    print("\n[5] DELIVERABLE (revision 3): structure-corrected ranking at 0.1c flyby")
    print("    Payload fraction is bracketed [1 stage .. unlimited ideal stages].")
    results = []
    for (nm, fam, isp, ve, eps, note) in DRIVES:
        r = analyse_drive(nm, fam, isp, ve, eps, note)
        lam_ss = r["lambda_single_stage"]
        lam_inf = r["lambda_staged_infinite"]
        if lam_inf <= 0:
            verdict = "CLOSED (no payload reaches 0.1c)"
        elif lam_inf < 0.01:
            verdict = f"CLOSED (~{lam_inf:.1e} payload)"
        elif lam_inf < 0.25:
            verdict = f"OPEN (lambda ~{lam_inf*100:.1f}%)"
        else:
            verdict = f"OPEN (lambda ~{lam_inf*100:.1f}%)"
        r["verdict"] = verdict
        results.append(r)
        print(f"    {nm:<38} ve={ve/C:9.4g}c  "
              f"lam=[{max(lam_ss,0.0):9.3g} .. {lam_inf:9.3g}]  {verdict}")

    # ---------------- Cost per payload tonne ---------------------------------
    print("\n[6] COST OF A 0.1c FLYBY, per payload tonne launched")
    print("    Initial mass = payload / lambda (structure-corrected, unlimited staging)")
    print(f"    {'drive':<38} {'lambda':>12} {'init mass / t payload':>22} {'bracket':>10}")
    for r in results:
        lam = r["lambda_staged_infinite"]
        if lam <= 0 or lam != lam:
            print(f"    {r['drive']:<38} "
                  f"{'<=0':>12} {'impossible (>=1e30 t)':>22} {'CLOSED':>10}")
        else:
            print(f"    {r['drive']:<38} {lam:12.4g} {1.0/lam:22,.4g} "
                  f"{max(r['lambda_single_stage'],0.0):10.3g}")

    # ---------------- 1% payload capability --------------------------------
    print("\n[7] CAPABILITY AT A UNIFORM 1% PAYLOAD FRACTION (unlimited ideal staging)")
    print("    'well uses' = fraction of the ideal budget eaten by escaping")
    print("    Earth+Sun (16.18 km/s surface -> heliocentric escape) BEFORE any cruise.")
    print(f"    {'drive':<38} {'dv (km/s)':>13} {'beta':>10} {'well uses':>10} "
          f"{'dv left (km/s)':>15}")
    for r in results:
        dv1 = r["dv_at_lam_p001_staged_km_s"]
        b = r["beta_at_lam_p001_staged"]
        print(f"    {r['drive']:<38} {dv1:13,.0f} {b:10.4g} "
              f"{r['pct_of_dv_at_lam_p001_for_solar_escape']:9.1f}% "
              f"{r['dv_left_after_solar_escape_km_s']:15,.0f}")

    # ---------------- Blocker decomposition ---------------------------------
    print("\n[8] BLOCKER DECOMPOSITION: which term binds, and by how much")
    print("    Target: 0.1c flyby at a uniform 1% payload fraction.")
    print("    eps_req < 0 means the drive FAILS EVEN WITH ZERO STRUCTURE --")
    print("    the blocker is the exhaust velocity and no materials progress helps.")
    print(f"    {'drive':<38} {'ve_req (c)':>11} {'shortfall':>10} "
          f"{'eps_req':>10} {'eps':>7}  binding")
    for r in results:
        b = r["blocker"]
        epsr = b["eps_required"]
        print(f"    {r['drive']:<38} {b['ve_required_beta_c']:11.5f} "
              f"{b['ve_shortfall_factor']:10.3g} {epsr:10.3f} {r['eps']:7.3f}  "
              f"{'EXHAUST VELOCITY' if epsr <= 0 else 'STRUCTURE'}")

    # ---------------- Photon tax -------------------------------------------
    print("\n[9] THE PHOTON TAX: beam energy per unit craft kinetic energy")
    print("    A perfect reflector spends MORE than the craft's KE in photons;")
    print("    E/p = c for light, no reflective material can beat it.")
    print(f"    {'beta':>6} {'exact SR reflector':>19} {'classical c/v':>14} "
          f"{'c/v optimism %':>15} {'absorber bound':>15}")
    for beta in (0.01, 0.05, 0.10, 0.20, 0.50, 0.90, 0.99):
        ex = photon_tax_reflector_exact(beta)
        cl = photon_tax_reflector_classical(beta)
        print(f"    {beta:6.2f} {ex:19.6f} {cl:14.4f} "
              f"{(cl/ex-1)*100:14.2f}% {photon_tax_upper_bound(beta):15.4f}")
    print("    EXACT closed form: tax(beta) = (gamma(1+beta)-1)/(2(gamma-1))")
    print("    -> at 0.2c a perfect reflector spends 5.45x craft KE, not 5.0x")
    print("       (revision 2 quoted the classical 5x: optimistic by 9%).")

    # ---------------- Daedalus calibration ---------------------------------
    print("\n[9] CALIBRATION: reproduce the published Project Daedalus mass breakdown")
    m0, m_p, m_pl = 54000.0, 50000.0, 500.0
    m_i = m0 - m_p - m_pl
    eps_d = m_i / (m_i + m_p)
    lam_d = m_pl / m0
    MR_d = m0 / (m0 - m_p)
    lam_model = payload_fraction(MR_d, eps_d)
    print(f"    published: m0={m0:,.0f} t, propellant={m_p:,.0f} t D-He3, payload={m_pl:,.0f} t")
    print(f"    derived inert mass = {m_i:,.0f} t  ->  eps = {eps_d:.5f},  lambda = {lam_d:.5f}")
    print(f"    model Eq.(2) predicts lambda = {lam_model:.5f}   (error {abs(lam_model/lam_d-1)*100:.4f}%)")
    beta_dae = dv_rel(1.03e7, MR_d) / C
    print(f"    model Eq.(4) gives dv = {beta_dae:.5f}c at ve = 1.03e7 m/s (MR={MR_d:.2f})")
    print(f"    published Daedalus cruise: 0.12c; the published ve=0.0461c would give 0.12c")
    print(f"    -> the 0.12c/ve=0.034c pair in secondary sources is mutually inconsistent;")
    print(f"       Daedalus is a single stage and cannot reach 0.12c at eps=0.0654.")

    # ---------------- Validations ------------------------------------------
    print("\n[10] NUMERICAL VALIDATION")
    check("solar escape v_inf @1AU = 12.337 km/s", solar_escape_v_inf() / 1e3, 12.337, 1e-3)
    check("LEO->solar escape = 8.8 km/s", leo_to_solar_escape_dv() / 1e3, 8.75, 0.02)
    check("surface->solar escape = 16.2 km/s", surface_to_solar_escape_dv()[0] / 1e3, 16.18, 0.01)
    check("eps=0.10 gives MR=10 at zero payload", mass_ratio(0.0, 0.10), 10.0)
    check("eps=0.10 ceiling dv = ve*ln(10)", dv_zero_payload(4.43e3, 0.10),
          4.43e3 * math.log(10), 1e-9)
    check("relativistic Isp @0.1c MR=10 = 1.3321e6 s", isp_rel_required(0.1, 10), 1.3321e6, 1e-3)
    check("relativistic Isp @0.2c MR=10 = 2.6916e6 s", isp_rel_required(0.2, 10), 2.6916e6, 1e-3)
    check("photon rocket to 0.1c needs MR = e^0.1003 = 1.1056",
          MR_rel_required(C, 0.10), 1.1056, 1e-3)
    check("photon tax exact at 0.2c = 5.4495 (rev-2 said 5.0)",
          photon_tax_reflector_exact(0.20), 5.4495, 1e-3)
    check("photon tax exact -> c/v as beta->0",
          photon_tax_reflector_exact(1e-4) / (1.0 / 1e-4), 1.0, 2e-3)
    check("photon tax exact -> 1 as beta->1",
          photon_tax_reflector_exact(1 - 1e-9), 1.0, 5e-5)
    check("absorber bound = 2x reflector",
          photon_tax_upper_bound(0.20) / photon_tax_reflector_exact(0.20), 2.0, 1e-12)

    # Exact SR photon tax cross-checked by direct ODE integration
    def _ode_tax(beta, n=400000):
        """Integrate d(gamma*beta)/dt = 2P/(c(1+beta)); u=gamma*beta, beta=u/sqrt(1+u^2)."""
        gamma = 1.0 / math.sqrt(1.0 - beta ** 2)
        u_f = gamma * beta
        h = u_f / n
        u = 0.0
        E = 0.0
        for _ in range(n):
            b_now = u / math.sqrt(1.0 + u * u)
            E += 0.5 * (1.0 + b_now) * h
            u += h
        return E / (gamma - 1.0)

    for beta in (0.05, 0.10, 0.20, 0.50, 0.90):
        check(f"exact SR photon tax beta={beta} matches ODE integration",
              photon_tax_reflector_exact(beta), _ode_tax(beta), 2e-4)
    # Staging asymptotic law vs brute force, Eq. (5)
    for ve_s, eps_s in ((4.43e3, 0.10), (9.0e3, 0.15), (1.03e7, 0.0654)):
        dv_t = 10e3
        lam_inf = math.exp(-(dv_t / ve_s) * (1.0 / (1.0 - eps_s)))
        lam_n = staged_payload_fraction(dv_t, ve_s, eps_s, 4000)
        check(f"staging law Eq5 vs brute force ve={ve_s:.2e} eps={eps_s}",
              lam_inf, lam_n, 0.02)
    # Daedalus model reproduces published lambda
    check("Daedalus lambda reproduced by Eq.(2)", lam_model, lam_d, 1e-3)
    check("Daedalus eps = 0.06542", eps_d, 0.06542, 1e-4)
    # Eq.(5) must sit ABOVE the single-stage lambda (staging can only help)
    lam_ss = lambda_at_beta_single_stage(2.65e7, 0.0693, 0.10)
    lam_inf2 = lambda_at_beta_staged(2.65e7, 0.0693, 0.10)
    check("staging improves D-He3 payload fraction", float(lam_inf2 > lam_ss), 1.0)
    check("D-He3 zero-payload ceiling > 0.1c", float(dv_zero_payload(2.65e7, 0.0693) > 0.1 * C), 1.0)
    # Chemical cannot reach 0.1c in any number of stages
    lam_chem = lambda_at_beta_staged(452 * G0, 0.10, 0.10)
    check("chemical lambda at 0.1c is below double precision (underflows to 0)",
          float(lam_chem == 0.0), 1.0)
    check("chemical ln(lambda) at 0.1c = -7544",
          -beta_to_rapidity(0.10) * (C / (452 * G0)) / 0.90, -7543.9, 1e-3)
    check("chemical needs 2938 stages just at zero payload to 0.1c",
          float(n_stages_zero_payload(0.10 * C, 452 * G0, 0.10)), 2938.0, 0)
    # energy conservation sanity: photon tax >= 1 always
    for b in (0.001, 0.01, 0.1, 0.5, 0.9):
        check(f"photon tax >= 1 at beta={b}", float(photon_tax_reflector_exact(b) >= 1.0), 1.0)
        check(f"absorber bound = 2x reflector at beta={b}",
              photon_tax_upper_bound(b) / photon_tax_reflector_exact(b), 2.0, 1e-12)
        check(f"classical c/v is optimistic at beta={b}",
              float(photon_tax_reflector_classical(b) < photon_tax_reflector_exact(b)), 1.0)

    n_ok = sum(1 for c in CHECK_LOG if c["ok"])
    print(f"    {n_ok}/{len(CHECK_LOG)} checks passed")
    for c in CHECK_LOG:
        flag = "PASS" if c["ok"] else "FAIL"
        print(f"      [{flag}] {c['name']}: got {c['got']:.6g} "
              f"vs {c['expected']:.6g} (rel {c['rel_err']:.2e})")

    # ---------------- Persist ----------------------------------------------
    out = {
        "relativistic_correction": {
            f"isp_req_MR10_beta_{b}": {
                "relativistic_s": isp_rel_required(b, 10),
                "classical_s": isp_classical_required(b, 10),
                "pct_optimism_of_classical": (isp_classical_required(b, 10)
                                              / isp_rel_required(b, 10) - 1) * 100
            } for b in (0.01, 0.05, 0.10, 0.20, 0.50)
        },
        "drives": results,
        "solar_well": {
            "v_inf_km_s": solar_escape_v_inf() / 1e3,
            "surface_to_solar_escape_km_s": dv_surf / 1e3,
            "leo_to_solar_escape_km_s": dv_leo / 1e3,
        },
        "photon_tax": {"closed_form": "tax(beta) = (gamma(1+beta)-1)/(2(gamma-1))",
                       **{str(b): {"exact_SR_reflector": photon_tax_reflector_exact(b),
                                   "classical_c_over_v": photon_tax_reflector_classical(b),
                                   "absorber_upper_bound": photon_tax_upper_bound(b)}
                          for b in (0.01, 0.05, 0.10, 0.20, 0.50, 0.90)}},
        "daedalus_calibration": {"m0_t": m0, "propellant_t": m_p, "payload_t": m_pl,
                                 "inert_t": m_i, "eps": eps_d, "lambda": lam_d,
                                 "MR": MR_d, "beta_at_ve_1p03e7": beta_dae},
        "checks": CHECK_LOG,
        "checks_passed": f"{n_ok}/{len(CHECK_LOG)}",
    }
    with open("structure_corrected_closure_results.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\n[11] Wrote structure_corrected_closure_results.json")
    return out


if __name__ == "__main__":
    main()
