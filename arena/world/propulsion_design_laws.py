#!/usr/bin/env python3
"""
propulsion_design_laws.py
=========================
Design laws and system-level bounds for practical space propulsion.

Author : Hypatia (Agent A003, Generation 0)
Domain : Practical space propulsion
Standard of evidence: conservation of momentum/energy, thermodynamics,
                      special relativity, Tsiolkovsky rocket equation.

This module advances beyond the ranking in propulsion_analyzer.py by deriving
the *closed-form design laws* that bound every drive family:

  (1) ROCKET-EQUATION WALL
        dv = ve ln(MR)  =>  Isp_req = dv / (g0 ln MR)
      Direct-thrust drives with low exhaust velocity need astronomical MR.

  (2) SPECIFIC-POWER WALL (the new result)
        Any drive that must carry its own energy *as a power system* (fission,
        fusion-electric, antimatter-electric) has a hard trip-time floor set
        by the power system specific mass alpha = m_power/P [kg/W]:
             t_min  >=  (dv^2) / (2 * eta * sigma),   sigma = 1/alpha [W/kg]
        This is because the source can deliver only sigma watts per kg of
        itself, while reaching dv costs dv^2/2 joules per kg.
        For onboard-energy drives this is *independent of absolute power*.

  (3) STUHLINGER OPTIMUM for power-limited electric rockets:
        minimising t = mf (e^y - 1) ve^2 / (2 eta P), y = dv/ve
        gives e^y = 2/(2-y)  =>  y* = 1.59362426...,  ve* = 0.6275 dv.
        This is the Isp that minimises trip time for fixed final mass.

  (4) EXTERNAL-ENERGY ESCAPE: sails/beams carry no propellant and no onboard
        power system, so they evade (1) and (2) -- at the cost of launch-side
        infrastructure and (usually) flyby-only trajectories.

All numbers SI unless noted.  g0 = 9.80665 m/s^2, c = 299792458 m/s.
"""

from __future__ import annotations
import json
import math
from dataclasses import dataclass, asdict

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
G0 = 9.80665                 # m/s^2
C = 299_792_458.0            # m/s
YEAR = 3.155_760e7           # s
DAY = 86_400.0
AU = 1.495_978_707e11        # m
LY = 9.460_730_472_580_8e15  # m
SIGMA_SB = 5.670_374_419e-8  # W m^-2 K^-4
S0 = 1361.0                  # W/m^2 at 1 AU
R_GAS = 8.314_462_618        # J/mol/K
TNT_TON = 4.184e9            # J
WORLD_ENERGY = 6.0e20        # J/yr, order of world primary energy


# ---------------------------------------------------------------------------
# 1. Rocket-equation wall
# ---------------------------------------------------------------------------
def mass_ratio(dv: float, ve: float) -> float:
    return math.exp(dv / ve)


def isp_required(dv: float, mr: float) -> float:
    """Isp needed to reach dv at mass ratio mr:  dv/(g0 ln mr)."""
    return dv / (G0 * math.log(mr))


def ve_required(dv: float, mr: float) -> float:
    return dv / math.log(mr)


def exhaust_velocity(isp: float) -> float:
    return isp * G0


# ---------------------------------------------------------------------------
# 2. Specific-power wall
# ---------------------------------------------------------------------------
def specific_power_floor(dv: float, sigma: float, eta: float = 1.0) -> float:
    """Hard lower bound on trip time [s] for an onboard-power drive.

    t >= dv^2 / (2 eta sigma),  sigma = P/m_power [W/kg].
    Derivation: the power system can supply sigma watts per kg of itself;
    the vehicle must acquire dv^2/2 joules per kg of kinetic energy.
    """
    return dv * dv / (2.0 * eta * sigma)


def sigma_required(dv: float, t_seconds: float, eta: float = 1.0) -> float:
    """Specific power [W/kg] needed to reach dv in time t (source-dominated)."""
    return dv * dv / (2.0 * eta * t_seconds)


def alpha_required(dv: float, t_seconds: float, eta: float = 1.0) -> float:
    """Specific mass [kg/W] needed to reach dv in time t (source-dominated)."""
    return 1.0 / sigma_required(dv, t_seconds, eta)


# ---------------------------------------------------------------------------
# 3. Stuhlinger optimum (power-limited electric rocket)
# ---------------------------------------------------------------------------
def _stuhlinger_y_star() -> float:
    """Solve e^y = 2/(2-y) on (0,2) by bisection.  y* = 1.59362426..."""
    f = lambda y: math.exp(y) - 2.0 / (2.0 - y)
    lo, hi = 1e-12, 2.0 - 1e-12
    assert f(lo) < 0 < f(hi) or f(lo) > 0 > f(hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


Y_STAR = _stuhlinger_y_star()                       # 1.59362426...
H_STAR = (math.exp(Y_STAR) - 1.0) / Y_STAR ** 2     # 1.5441...
T_FACTOR = H_STAR / 2.0                             # 0.7720...


def stuhlinger_optimum(dv: float) -> dict:
    """Time-minimising exhaust velocity for a constant-power rocket.

    t(ve) = mf (e^y - 1) ve^2 / (2 eta P),  y = dv/ve.
    Minimum at y = y* => ve* = dv/y* = 0.6275 dv.
    """
    ve = dv / Y_STAR
    return {
        "dv_m_s": dv,
        "ve_opt_m_s": ve,
        "isp_opt_s": ve / G0,
        "y_star": Y_STAR,
        "h_star": H_STAR,
        "t_factor": T_FACTOR,   # t_min = t_factor * mf * dv^2 / (eta P)
        "ve_over_dv": 1.0 / Y_STAR,
    }


def stuhlinger_trip_time(dv: float, ve: float, mf: float, power: float,
                         eta: float = 0.6) -> dict:
    """Exact burn time for a constant-power, constant-ve rocket.

    t = mf (e^y - 1) ve^2 / (2 eta P),   y = dv/ve.
    """
    y = dv / ve
    if y > 700:
        return {"feasible": False, "y": y, "mass_ratio": float("inf")}
    t = mf * (math.exp(y) - 1.0) * ve * ve / (2.0 * eta * power)
    return {
        "feasible": True, "y": y, "mass_ratio": math.exp(y),
        "propellant_kg": mf * (math.exp(y) - 1.0),
        "initial_mass_kg": mf * math.exp(y),
        "burn_time_s": t, "burn_time_days": t / DAY, "burn_time_years": t / YEAR,
    }


# ---------------------------------------------------------------------------
# 4. Staging (does not beat the exponential)
# ---------------------------------------------------------------------------
def staged_payload_fraction(dv: float, ve: float, eps_struct: float,
                            n_stages: int) -> float:
    """Payload / initial mass for n equal stages, structural fraction eps.

    Each stage: MR = exp(dv/(n ve)), payload fraction per stage
    f = exp(-dv/(n ve)) - eps  (eps = structure/initial of that stage).
    Total payload fraction = f^n.  Negative => infeasible.
    """
    f = math.exp(-dv / (n_stages * ve)) - eps_struct
    return f ** n_stages if f > 0 else float("nan")


def optimal_staging(dv: float, ve: float, eps_struct: float = 0.1,
                    n_max: int = 200) -> dict:
    best = None
    for n in range(1, n_max + 1):
        lam = staged_payload_fraction(dv, ve, eps_struct, n)
        if math.isfinite(lam) and lam > 0:
            if best is None or lam > best[1]:
                best = (n, lam)
    if best is None:
        return {"feasible": False}
    return {"feasible": True, "n_stages": best[0],
            "payload_fraction": best[1],
            "payload_kg_per_1000t": best[1] * 1e6}


# ---------------------------------------------------------------------------
# 5. Physics limits per drive family
# ---------------------------------------------------------------------------
def chemical_ceiling(q_mj_per_kg: float = 13.0) -> dict:
    """Absolute Isp ceiling from chemical bond energy Q (J/kg)."""
    q = q_mj_per_kg * 1e6
    ve = math.sqrt(2.0 * q)
    return {"Q_J_kg": q, "ve_max_m_s": ve, "isp_max_s": ve / G0}


def ntr_isp(chamber_T: float, gamma: float = 1.4, molar_mass: float = 0.002,
            expansion_eff: float = 0.90) -> dict:
    """Ideal nozzle exhaust velocity for a hot-gas NTR.

    ve = expansion_eff * sqrt( 2 gamma R T / ((gamma-1) M) ),  M [kg/mol].
    H2: gamma=1.4, M=0.002 kg/mol.
    """
    ve_ideal = math.sqrt(2.0 * gamma * R_GAS * chamber_T /
                         ((gamma - 1.0) * molar_mass))
    ve = expansion_eff * ve_ideal
    return {"T_K": chamber_T, "ve_ideal_m_s": ve_ideal,
            "ve_m_s": ve, "isp_s": ve / G0}


def radiator_mass(waste_heat_w: float, T_rad: float, eps: float = 0.9,
                  areal_density: float = 5.0) -> dict:
    """Radiator area/mass to reject Q at T (two-sided Stefan-Boltzmann).

    A = Q / (2 eps sigma T^4);  m = A * areal_density.
    """
    A = waste_heat_w / (2.0 * eps * SIGMA_SB * T_rad ** 4)
    return {"Q_W": waste_heat_w, "T_K": T_rad, "area_m2": A,
            "mass_kg": A * areal_density, "areal_density_kg_m2": areal_density}


def beam_aperture(lam: float, range_m: float, sail_side: float) -> dict:
    """Diffraction-limited transmitter diameter to keep the spot on the sail.

    Spot size w ~ lam z / D  =>  D ~ lam z / d.
    """
    D = lam * range_m / sail_side
    return {"lambda_m": lam, "range_m": range_m, "sail_side_m": sail_side,
            "aperture_m": D}


def sail_equilibrium_temperature(flux_w_m2: float, absorptivity: float,
                                 emissivity: float = 0.9) -> float:
    """Two-sided radiative equilibrium T of a sail in flux.

    absorptivity*flux = 2 * emissivity * sigma * T^4.
    """
    return (absorptivity * flux_w_m2 /
            (2.0 * emissivity * SIGMA_SB)) ** 0.25


def constant_accel_transit(v_target: float, a: float) -> dict:
    """Time/distance to reach v_target from rest at constant a (non-rel)."""
    t = v_target / a
    x = 0.5 * a * t * t
    return {"a_m_s2": a, "t_s": t, "t_years": t / YEAR,
            "x_m": x, "x_AU": x / AU, "x_ly": x / LY}


# ---------------------------------------------------------------------------
# 6. Fusion direct-drive (charged products) -- corrected treatment
# ---------------------------------------------------------------------------
# D + He3 -> He4 (3.6 MeV) + p (14.7 MeV).  The 14.7 MeV proton has
# v = sqrt(2E/m_p) = 0.177c; the 3.6 MeV alpha ~ 0.044c.  A magnetic nozzle
# can in principle direct the charged products, so ve can be ~0.03-0.18c,
# far above the 1e5 s assumed in the first-pass ranking.
def fusion_product_velocity(energy_mev: float, mass_kg: float) -> dict:
    E = energy_mev * 1.602_176_634e-13  # J
    v = math.sqrt(2.0 * E / mass_kg)
    return {"energy_MeV": energy_mev, "v_m_s": v, "v_frac_c": v / C,
            "isp_s": v / G0}


def fusion_direct_mass_ratio(dv: float, ve: float) -> float:
    return mass_ratio(dv, ve)


def implied_specific_power(thrust: float, ve: float,
                           source_mass: float) -> float:
    """sigma = P_jet / m_source = (0.5 T ve) / m_source  [W/kg]."""
    return 0.5 * thrust * ve / source_mass


# ---------------------------------------------------------------------------
# 7. Master ranked table (near-term feasibility)
# ---------------------------------------------------------------------------
RANKED = [
    dict(rank=1, drive="Chemical LH2/LOX", isp_s="320-452", ve_km_s="3.1-4.4",
         thrust="0.5-2.3 MN/engine",
         frontier="LEO/Moon/Mars orbit; Mars round trip MR~15",
         blocker="Bond-energy ceiling: Q~13 MJ/kg caps Isp<=520 s (ve<=5.1 km/s); "
                 "propellant is the vehicle"),
    dict(rank=2, drive="Solar electric (Hall/ion)", isp_s="1800-4170",
         ve_km_s="18-41", thrust="0.24-0.6 N/kW-class",
         frontier="Inner-system cargo, station-keeping; Dawn-class",
         blocker="Solar flux falls as 1/r^2; array mass/area grows faster than thrust "
                 "beyond ~2-3 AU"),
    dict(rank=3, drive="Solar sail", isp_s="n/a (no propellant)", ve_km_s="n/a",
         thrust="9.08 uN/m^2 at 1 AU",
         frontier="Inner-system slow cruise; 30 km/s in 214-382 d",
         blocker="Photon pressure minuscule and 1/r^2; areal density/deployment"),
    dict(rank=4, drive="Nuclear thermal (solid core)", isp_s="850-950",
         ve_km_s="8.3-9.3", thrust="111-334 kN",
         frontier="Mars in ~3-4 months; single-stage dv<=19 km/s",
         blocker="Fuel-element/chamber thermal limit ~3000 K in hot H2; "
                 "corrosion and fuel retention"),
    dict(rank=5, drive="Nuclear electric (fission+ion)", isp_s="2600-8000",
         ve_km_s="25-78", thrust="15-41 N at 1 MWe",
         frontier="Outer-planet orbiters/cargo",
         blocker="Reactor specific mass ~20 kg/kW plus waste-heat radiators; "
                 "specific-power wall caps trip time"),
    dict(rank=6, drive="Laser-pushed sail (Starshot-class)", isp_s="n/a (external)",
         ve_km_s="n/a", thrust="667 N on 1 g sail (100 GW)",
         frontier="0.1-0.2c flyby of Proxima (~21-42 yr)",
         blocker="100 GW phased array + sail must survive GW/m^2 and 1e5 g; "
                 "flyby-only without target-side braking"),
    dict(rank=7, drive="Nuclear pulse (fission Orion)", isp_s="2000-10000",
         ve_km_s="20-98", thrust="1e7 N-class",
         frontier="Fast outer-system; marginal interstellar (MR>1e400 to 0.1c)",
         blocker="Pulse-unit production, pusher-plate ablation/neutron damage, "
                 "test-ban regime; fission Isp too low for 0.1c"),
    dict(rank=8, drive="Fusion direct (D-He3, Daedalus-class)", isp_s="0.8-5e6",
         ve_km_s="0.025c-0.17c", thrust="~1e6-1e7 N (conceptual)",
         frontier="0.1-0.12c flyby at MR~50-120; outer system solved if ignited",
         blocker="No ignited net-positive device; implied source specific power "
                 "~1e6 W/kg, ~5 orders above ITER (~20 W/kg); He3 scarcity"),
    dict(rank=9, drive="Antimatter (photon/pion)", isp_s="up to 3.06e7 (ve=c ideal)",
         ve_km_s="up to 3e5", thrust="~1e3 N (conceptual)",
         frontier="Only propellant drive that closes the rocket equation at MR~1.1-1.2",
         blocker="Production/storage: CERN makes nanograms/yr; macroscopic trapping "
                 "unsolved; cost ~$6e16/kg"),
]


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def _hr(ch="=", n=78):
    print(ch * n)


def report():
    _hr()
    print("PROPULSION DESIGN LAWS AND SYSTEM-LEVEL BOUNDS  --  Hypatia A003")
    _hr()

    print("\n[1] STUHLINGER OPTIMUM (power-limited electric rocket)")
    print(f"    y* = {Y_STAR:.8f}  (root of e^y = 2/(2-y))")
    print(f"    ve_opt = dv / y* = {1/Y_STAR:.4f} dv ;  Isp_opt = 0.6275 dv/g0")
    print(f"    h* = (e^y*-1)/y*^2 = {H_STAR:.5f} ;  t_min = {T_FACTOR:.4f} mf dv^2/(eta P)")
    for dv in (1e4, 2e4, 5e4, 1e5, 3e7):
        r = stuhlinger_optimum(dv)
        print(f"    dv={dv:>10.3e} m/s -> ve*={r['ve_opt_m_s']:>10.3e} m/s "
              f"Isp*={r['isp_opt_s']:>12,.0f} s")

    print("\n[2] SPECIFIC-POWER FLOOR TO 0.1c (t = dv^2/(2 eta sigma))")
    dv = 0.1 * C
    print(f"    dv = 0.1c = {dv:.3e} m/s")
    for sigma in (50, 1e3, 1e4, 1e5, 1e6, 1e7):
        t = specific_power_floor(dv, sigma, eta=1.0)
        print(f"    sigma={sigma:>10.1e} W/kg -> t_min={t:>10.3e} s = "
              f"{t/YEAR:>10.1f} yr")
    print("    (fission space reactor ~50 W/kg; ITER ~20 W/kg;")
    print("     advanced pulsed fusion (Daedalus-implied) ~1e6 W/kg)")

    print("\n[3] SPECIFIC POWER NEEDED FOR A GIVEN 0.1c TRANSIT TIME")
    for yrs in (1, 10, 40, 100, 1000):
        t = yrs * YEAR
        s = sigma_required(dv, t, eta=1.0)
        print(f"    t={yrs:>5} yr -> sigma_min={s:>10.3e} W/kg "
              f"(alpha={1/s:>10.3e} kg/W)")

    print("\n[4] FUSION DIRECT-DRIVE (charged products, corrected)")
    p = fusion_product_velocity(14.7, 1.672_621_923_69e-27)
    a = fusion_product_velocity(3.6, 6.644_657_33e-27)
    print(f"    D-He3 14.7 MeV proton : v={p['v_m_s']:.3e} m/s = "
          f"{p['v_frac_c']:.3f}c  Isp={p['isp_s']:.3e} s")
    print(f"    D-He3  3.6 MeV alpha  : v={a['v_m_s']:.3e} m/s = "
          f"{a['v_frac_c']:.3f}c  Isp={a['isp_s']:.3e} s")
    print("    mass ratio to 0.1c for representative ve:")
    for frac in (0.025, 0.05, 0.10, 0.15):
        ve = frac * C
        mr = fusion_direct_mass_ratio(dv, ve)
        print(f"      ve={frac:.3f}c -> MR={mr:8.3f}")
    # Daedalus cross-check
    m0, mpl, dv_d = 5.4e7, 4.5e5, 0.12 * C
    mr_d = m0 / mpl
    ve_d = dv_d / math.log(mr_d)
    print(f"    Daedalus cross-check: m0=5.4e7 kg payload=4.5e5 kg "
          f"MR={mr_d:.1f} dv=0.12c")
    print(f"      implied ve={ve_d:.3e} m/s = {ve_d/C:.4f}c "
          f"(Isp={ve_d/G0:.3e} s)")
    # implied specific power (stage-1 order of magnitude)
    for T, ms in ((6.6e6, 4.7e7),):
        s = implied_specific_power(T, ve_d, ms)
        print(f"      implied source specific power ~{s:.3e} W/kg "
              f"(T={T:.1e} N, m={ms:.1e} kg)")
    print(f"      ITER thermal: 5e8 W / 2.3e7 kg = {5e8/2.3e7:.1f} W/kg")

    print("\n[5] STAGING DOES NOT BEAT THE EXPONENTIAL")
    for dvx, ve in ((3e4, 4.43e3), (3e4, 8.34e3), (1e5, 3e4), (0.1*C, 0.05*C)):
        r = optimal_staging(dvx, ve, eps_struct=0.1, n_max=400)
        tag = f"dv={dvx:.3e} ve={ve:.3e}"
        if r["feasible"]:
            print(f"    {tag}: optimal N={r['n_stages']:>4}  "
                  f"payload fraction={r['payload_fraction']:.3e}  "
                  f"payload/1000 t={r['payload_kg_per_1000t']:.3e} kg")
        else:
            print(f"    {tag}: INFEASIBLE at eps=0.1 for N<=400")

    print("\n[6] THERMODYNAMIC / MATERIAL LIMITS")
    ch = chemical_ceiling(13.0)
    print(f"    Chemical ceiling: Q=13 MJ/kg -> ve_max={ch['ve_max_m_s']:.1f} m/s "
          f"Isp_max={ch['isp_max_s']:.1f} s")
    for T in (2500, 3000, 3500, 4000):
        n = ntr_isp(T)
        print(f"    NTR H2 T={T:>5} K -> ve={n['ve_m_s']:8.1f} m/s "
              f"Isp={n['isp_s']:7.1f} s")
    print("    Radiator mass to reject 0.67 MW (1 MWe @ 60% eff):")
    for T in (400, 600, 800, 1000):
        rm = radiator_mass(0.67e6, T, areal_density=5.0)
        print(f"      T={T:>4} K -> A={rm['area_m2']:8.1f} m^2  "
              f"m={rm['mass_kg']:8.1f} kg")
    print("    Sail radiative equilibrium (absorptivity a, flux 6.25 GW/m^2):")
    for ab in (1e-5, 1e-4, 1e-3, 1e-2):
        Ts = sail_equilibrium_temperature(6.25e9, ab)
        print(f"      absorptivity={ab:.0e} -> T_eq={Ts:8.0f} K "
              f"({'survivable' if Ts < 3000 else 'VAPORISES'})")

    print("\n[7] BEAM APERTURE (diffraction) AND ACCELERATION SCALING")
    for z_au in (0.01, 0.02, 0.1):
        b = beam_aperture(1.06e-6, z_au * AU, 4.0)
        print(f"    lambda=1.06 um, sail=4 m, z={z_au:>5.2f} AU -> "
              f"aperture D={b['aperture_m']/1e3:8.2f} km")
    for a in (9.80665, 1e-2, 1e-3, 1e-4, 1e-5):
        r = constant_accel_transit(0.1 * C, a)
        print(f"    a={a:>10.3e} m/s^2 -> t={r['t_years']:8.3f} yr  "
              f"x={r['x_AU']:8.4f} AU ({r['x_ly']:.3e} ly)")

    print("\n[8] MASTER RANKED TABLE (near-term feasibility)")
    for row in RANKED:
        print(f"    #{row['rank']} {row['drive']}")
        print(f"        Isp={row['isp_s']} s | ve={row['ve_km_s']} | "
              f"T={row['thrust']}")
        print(f"        frontier: {row['frontier']}")
        print(f"        blocker : {row['blocker']}")

    out = {
        "y_star": Y_STAR, "h_star": H_STAR, "t_factor": T_FACTOR,
        "ranked": RANKED,
    }
    with open("propulsion_design_laws.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\n    wrote propulsion_design_laws.json")


if __name__ == "__main__":
    report()
