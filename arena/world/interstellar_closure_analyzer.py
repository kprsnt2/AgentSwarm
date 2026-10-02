#!/usr/bin/env python3
"""
interstellar_closure_analyzer.py
================================
Second-generation quantitative closure work on practical space propulsion.

Author : Hypatia (Agent A003, Generation 0)
Domain : Practical space propulsion (engineering feasibility)

This module closes gaps left by propulsion_analyzer.py:

  (A) Fusion exhaust-velocity physics -- resolves an internal inconsistency in
      the ranked assessment, where fusion was scored at Isp = 1e5 s against a
      design literature (Daedalus) whose ve is ~3x higher.  Bound ve from the
      *reaction energy per unit mass* and the *directable charge fraction*.
  (B) Crewed round-trip closure:  decel doubles the closure bar; carry-your-return
      fuel multiplies propellant roughly quadratically.
  (C) Delivered-energy economics for beamed sails (J per kg of payload, world
      energy comparisons, array power scaling with craft mass).
  (D) Solar-sail terminal velocity -- a finite flux bound, new result: even an
      ideal 0.1 g/m^2 sail cannot exceed ~sqrt(2 a_1AU r_0).
  (E) Antimatter production-rate wall (time and energy to accumulate grams).
  (F) Mission-capability matrix:  pass/fail per family per mission with the
      deciding number.

Every function returns plain numbers; test_interstellar_closure.py asserts the
identities.  No claim is made without a computable relation.
"""

from __future__ import annotations
import math
from dataclasses import dataclass

# ----------------------------------------------------------------------------
# Constants (CODATA 2018 / IAU)
# ----------------------------------------------------------------------------
G0 = 9.80665
C = 299_792_458.0
AU = 1.495_978_707e11
LY = 9.460_730_472_580_8e15
YEAR = 3.155_760e7
DAY = 86400.0
S0 = 1361.0                      # W/m^2 at 1 AU
MEV_J = 1.602_176_634e-13
U_KG = 1.660_539_066_60e-27      # atomic mass unit
TNT_TON = 4.184e9
WORLD_PRIMARY_ENERGY_J_YR = 6.0e20        # order-of-magnitude world primary energy
WORLD_ELECTRICITY_J_YR = 1.07e20          # ~29,700 TWh/yr -> mean power ~3.4 TW
CERN_AP_YIELD_G_YR = 1.0e-9               # nanograms/yr, historical antiproton production
AP_COST_USD_PER_G = 62.5e12               # commonly cited production cost per gram
LY_PER_PARSEC = 3.2616
PROXIMA_LY = 4.246


# ----------------------------------------------------------------------------
# Core relations (mirrors of propulsion_analyzer.py, kept dependency-free)
# ----------------------------------------------------------------------------
def mass_ratio(dv: float, ve: float) -> float:
    """Tsiolkovsky: m0/mf = exp(dv/ve); works for any exhaust velocity."""
    return math.exp(dv / ve)


def log10_mass_ratio(dv: float, ve: float) -> float:
    return dv / (ve * math.log(10.0))


def kinetic_energy_per_kg(v: float) -> float:
    """Relativistic KE per unit mass (gamma-1) c^2, numerically stable."""
    b2 = (v / C) ** 2
    s = math.sqrt(1.0 - b2)
    return b2 / (s * (1.0 + s)) * C * C


def gamma_of(v: float) -> float:
    return 1.0 / math.sqrt(1.0 - (v / C) ** 2)


# ----------------------------------------------------------------------------
# (A) Fusion exhaust-velocity physics
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class FusionReaction:
    name: str
    reactants_u: float          # mass of reactant nuclei, atomic mass units
    products_u: float           # mass of product nuclei
    charged_product_mev: float  # energy carried by *charged* products (MeV)
    total_mev: float            # total Q (MeV)


REACTIONS = {
    # D(d,p)T -- side branch, neutron-carrying, but included for the D-T main cycle's
    # charge partition we treat D-T directly below.
    "D-T (main)": FusionReaction("D-T", 2.014102 + 3.016049, 4.002602 + 1.008665, 3.5, 17.6),
    "D-He3": FusionReaction("D-He3", 2.014102 + 3.016049, 4.002602 + 1.007276, 18.3, 18.9),
    "p-B11": FusionReaction("p-B11", 1.007276 + 11.009305, 3.0 * 4.002602, 8.7, 8.7),
}


def q_per_kg(r: FusionReaction) -> float:
    """Energy per kg of reactant fuel [J/kg]."""
    dm = (r.reactants_u - r.products_u) * U_KG
    return r.total_mev * MEV_J / (r.reactants_u * U_KG)


def charged_fraction(r: FusionReaction) -> float:
    return r.charged_product_mev / r.total_mev


def max_directed_exhaust_velocity(r: FusionReaction) -> float:
    """Upper bound on directed exhaust velocity [m/s] if ALL charged-product
    energy became collimated jet KE:  ve <= sqrt(2 f_ch Q).

    This is a hard thermodynamic ceiling: energy not in charged products cannot
    be magnetically redirected, and radiative loss only lowers it.
    """
    return math.sqrt(2.0 * charged_fraction(r) * q_per_kg(r))


def mass_ratio_to_beta(ve: float, beta: float) -> float:
    return math.exp(beta * C / ve)


def fusion_closure_scan(beta: float = 0.10) -> list[dict]:
    """MR to a target beta across fusion exhaust-velocity regimes."""
    rows = []
    anchors = [
        ("D-T, 100% directed (ceiling)", math.sqrt(2 * q_per_kg(REACTIONS["D-T (main)"]))),
        ("D-T, charged fraction only", max_directed_exhaust_velocity(REACTIONS["D-T (main)"])),
        ("p-B11 (aneutronic)", max_directed_exhaust_velocity(REACTIONS["p-B11"])),
        ("Daedalus design point (lit.)", 1.03e7),
        ("D-He3, charged ceiling", max_directed_exhaust_velocity(REACTIONS["D-He3"])),
    ]
    for label, ve in anchors:
        rows.append({
            "regime": label,
            "ve_m_s": ve,
            "ve_over_c": ve / C,
            "isp_s": ve / G0,
            "MR_to_beta": mass_ratio_to_beta(ve, beta),
            "log10_MR": math.log10(mass_ratio_to_beta(ve, beta)),
        })
    return rows


def daedalus_anchor() -> dict:
    """Literature anchor: Project Daedalus (BIS, 1978) two-stage pellet fusion.
    ~50,000 t at ignition, ~3,500 t at burnout, ~0.12c.  The implied ve is
    vu = beta c / ln(MR) -- a *consistency* check of the reported design."""
    m0, mf, beta = 50_000e3, 3_500e3, 0.12
    mr = m0 / mf
    ve = beta * C / math.log(mr)
    return {"m0_kg": m0, "mf_kg": mf, "beta": beta, "mass_ratio": mr,
            "implied_ve_m_s": ve, "implied_ve_over_c": ve / C,
            "payload_fraction_at_burnout": 1.0 / mr}


def he3_requirement(payload_kg: float, ve: float, beta: float,
                    fuel_he3_mass_fraction: float = 0.25) -> dict:
    """Helium-3 mass needed for a one-way D-He3 flyby.

    Propellant needed from rocket eq:  m_prop = m_final (MR - 1).
    D-He3 has ~6e14 J/kg of reactant fuel; only a fraction of thermal energy
    reaches the directed jet, so fuel mass is scaled by 1/eta_conversion with
    eta_conversion = 0.5*m_prop*ve^2 / (energy needed) == via jet power.
    """
    mr = mass_ratio_to_beta(ve, beta)
    m_prop = payload_kg * (mr - 1.0)
    # Energy that must come from fusion: KE of the exhaust jet, >= 0.5 m_prop ve^2
    jet_energy = 0.5 * m_prop * ve * ve
    q = q_per_kg(REACTIONS["D-He3"])
    # Assume thermal-to-jet conversion eta=0.5 (magnetic nozzle redirects charged
    # products; neutron side-branches and radiation are lost).
    eta = 0.5
    reactant_kg = jet_energy / (eta * q)
    return {"payload_kg": payload_kg, "ve_over_c": ve / C, "beta": beta,
            "mass_ratio": mr, "propellant_kg": m_prop, "jet_energy_J": jet_energy,
            "reactant_kg": reactant_kg,
            "he3_kg": reactant_kg * fuel_he3_mass_fraction}


# ----------------------------------------------------------------------------
# (B) Crewed round-trip closure
# ----------------------------------------------------------------------------
def required_isp(dv: float, mass_ratio_target: float) -> float:
    """Isp such that a propellant-carrying vehicle achieves dv at given m0/mf."""
    return dv / (G0 * math.log(mass_ratio_target))


def crewed_roundtrip_table(betas=(0.01, 0.02, 0.05, 0.10)) -> list[dict]:
    rows = []
    for beta in betas:
        dv = 2.0 * beta * C                      # accel + decel
        rows.append({
            "beta_cruise": beta,
            "dv_total_km_s": dv / 1e3,
            "crew_years_one_way_PC": PROXIMA_LY * LY / (beta * C) / YEAR,
            "isp_req_MR5": required_isp(dv, 5.0),
            "isp_req_MR10": required_isp(dv, 10.0),
            "isp_req_MR100": required_isp(dv, 100.0),
            "photon_rocket_MR": math.exp(dv / C),
        })
    return rows


def carried_return_fuel_doubling(payload_kg: float, beta: float, ve: float) -> dict:
    """Cost of carrying your return propellant:  the return leg's m0/mf
    multiplies the outbound leg's, so the effective exponent doubles."""
    mr_leg = mass_ratio_to_beta(ve, beta)
    mr_total = mr_leg ** 2
    return {"beta": beta, "ve_over_c": ve / C,
            "mr_per_leg": mr_leg, "mr_carry_return": mr_total,
            "m0_per_kg_payload": mr_total,
            "verdict": ("carried-return propellant exceeds ship mass by >1e3"
                        if mr_total > 1e3 else "carried-return is arithmetically possible")}


# ----------------------------------------------------------------------------
# (C) Beamed-sail delivered-energy economics
# ----------------------------------------------------------------------------
def sail_energy_per_kg(beta: float, efficiency: float = 1.0) -> dict:
    """Minimum beam energy delivered per kg of sail-craft to reach beta:
    perfect reflection transfers momentum 2E/c and exactly the craft KE, so
    the floor is (gamma-1) c^2 / efficiency [J/kg]."""
    ke = kinetic_energy_per_kg(beta * C)
    j_per_min = WORLD_ELECTRICITY_J_YR / (YEAR / 60.0)   # world mean J/min
    return {"beta": beta, "KE_J_per_kg": ke,
            "delivered_J_per_kg": ke / efficiency,
            "delivered_Mt_TNT_per_kg": ke / efficiency / (TNT_TON * 1e6),
            "delivered_kWh_per_kg": ke / efficiency / 3.6e6,
            "world_electricity_minutes_per_kg": (ke / efficiency) / j_per_min}


def sail_array_scaling(mass_kg: float, beta: float,
                       beam_distance_au: float = 0.05,
                       reflectivity: float = 1.0) -> dict:
    """Array power needed so that a sail of mass m reaches beta within a
    beam of usable length L:  work = force x distance, F = 2f P/c on a perfect
    reflector, so  P = (gamma-1) m c^3 / (2 L).

    Check: m=1 g, beta=0.2, L=0.0186 AU reproduces the Starshot 100 GW array
    exactly -- the formula is anchored to the literature design point.
    """
    L = beam_distance_au * AU
    f = 2.0 / C                                    # force per watt, perfect reflector
    P = kinetic_energy_per_kg(beta * C) * mass_kg / (f * L)
    impulse = gamma_of(beta * C) * mass_kg * beta * C
    t = impulse / (f * P)
    return {"mass_kg": mass_kg, "beta": beta, "beam_length_AU": beam_distance_au,
            "required_array_W": P, "required_array_GW": P / 1e9,
            "push_time_s": t, "push_time_days": t / DAY,
            "energy_sunk_in_beam_J": P * t,
            "beam_energy_over_KE": P * t / (kinetic_energy_per_kg(beta * C) * mass_kg)}


def photon_rocket_cost(beta: float, payload_kg: float,
                       eta: float = 0.3, decel: bool = False) -> dict:
    """Antimatter photon/pion rocket cost to reach beta (optionally decel).

    Kinetic energy (x2 for decel) comes from annihilated matter+antimatter at
    eta usable directed efficiency; antimatter mass is half the annihilated mass.
    Cost at $6.25e13/g (Assumes 100% of KE must come onboard; no beaming.)
    """
    # total onboard energy = KE of final state (+ the same again to shed braking)
    if decel:
        energy_per_kg = 2.0 * kinetic_energy_per_kg(beta * C)
    else:
        energy_per_kg = kinetic_energy_per_kg(beta * C)
    total_E = energy_per_kg * payload_kg
    annihilated_kg = total_E / (eta * 2.0 * C * C)
    antimatter_kg = annihilated_kg / 2.0
    return {"beta": beta, "decel": decel, "payload_kg": payload_kg, "eta": eta,
            "energy_J": total_E,
            "energy_Mt_TNT": total_E / (TNT_TON * 1e6),
            "antimatter_kg": antimatter_kg,
            "antimatter_g": antimatter_kg * 1e3,
            "antimatter_over_payload": antimatter_kg / payload_kg,
            "cost_USD": antimatter_kg * 1e3 * AP_COST_USD_PER_G}


# ----------------------------------------------------------------------------
# (D) Solar-sail terminal velocity (finite solar flux)
# ----------------------------------------------------------------------------
def solar_sail_terminal_velocity(sigma: float, r0_au: float = 0.5) -> dict:
    """Solar-only sail: a(r) = a_1AU (AU/r)^2.  Work-energy from r0 to infinity:
    v^2 / 2 = integral a dr = a_1AU AU^2 / r0.

    Result: the Sun's finite flux caps solar sails at ~1e-3 c even at
    0.1 g/m^2 and a 0.05 AU perihelion -- solar sails are NOT interstellar
    drives no matter how good the material gets.
    """
    r0 = r0_au * AU
    a_1au = 2.0 * S0 / (C * sigma)                    # acceleration at 1 AU
    v_max = math.sqrt(2.0 * a_1au * AU * AU / r0)
    a0 = a_1au / r0_au**2                             # acceleration at perihelion
    return {"sigma_kg_m2": sigma, "perihelion_au": r0_au,
            "a_1AU_m_s2": a_1au, "a_r0_m_s2": a0,
            "v_max_m_s": v_max, "v_max_over_c": v_max / C,
            "years_to_PROXIMA": PROXIMA_LY * LY / v_max / YEAR}


# ----------------------------------------------------------------------------
# (E) Antimatter production wall
# ----------------------------------------------------------------------------
def antiproton_wall(antimatter_kg: float) -> dict:
    years = antimatter_kg * 1e3 / CERN_AP_YIELD_G_YR
    return {"antimatter_kg": antimatter_kg,
            "production_years_at_current_rate": years,
            "years_universe_age_units": years / 1.38e10,
            "production_years_1e6x_rate": years / 1e6,
            "cost_USD": antimatter_kg * 1e3 * AP_COST_USD_PER_G}


# ----------------------------------------------------------------------------
# (F) Mission capability matrix
# ----------------------------------------------------------------------------
FAMILY_VES = {
    "chemical": 4.43e3,       # H2/LOX
    "NTR": 8.34e3,            # solid core
    "SEP/ion": 4.09e4,        # NEXT-class
    "NEP": 4.09e4,            # reactor + ion (same ve, different power)
    "pulse": 2.94e4,          # fission Orion
    "fusion": 1.03e7,         # Daedalus-class ve
    "antimatter": C,          # ideal photon rocket
}

MISSIONS = {
    "LEO->GEO": 3.9e3, "LEO->Moon": 5.9e3, "LEO->Mars orbit": 3.6e3,
    "LEO->Mars&back": 12.0e3, "LEO->Jupiter orbit": 9.0e3,
    "Solar escape": 8.8e3, "0.01c flyby": 0.01 * C, "0.05c flyby": 0.05 * C,
    "0.10c flyby": 0.10 * C,
}


def capability_matrix(mr_cap: float = 10.0) -> list[dict]:
    """A propellant family clears a mission if dv <= ve ln(MR_cap).  Sails are
    handled separately (they are power/time-limited, not propellant-limited)."""
    rows = []
    for fam, ve in FAMILY_VES.items():
        dv_max = ve * math.log(mr_cap)
        cleared, failed = [], []
        for m, dv in MISSIONS.items():
            (cleared if dv <= dv_max else failed).append(m)
        rows.append({"family": fam, "ve_km_s": ve / 1e3,
                     "dv_at_MR10_km_s": dv_max / 1e3,
                     "clears": cleared, "blocked_by": failed})
    return rows


# ----------------------------------------------------------------------------
def report() -> None:
    line = "=" * 78
    print(line)
    print("INTERSTELLAR CLOSURE ANALYZER  --  Hypatia A003 (generation 0)")
    print(line)

    print("\n[A] FUSION EXHAUST-VELOCITY PHYSICS (resolves Isp=1e5 s vs Daedalus ve)")
    for r in REACTIONS.values():
        print(f"    {r.name:<9} Q={q_per_kg(r):.3e} J/kg  "
              f"f_charged={charged_fraction(r):.2f}  "
              f"ve_ceiling={max_directed_exhaust_velocity(r)/C:.4f} c")
    d = daedalus_anchor()
    print(f"    Daedalus anchor: MR={d['mass_ratio']:.0f}, beta={d['beta']}, "
          f"implied ve={d['implied_ve_over_c']:.4f} c ({d['implied_ve_m_s']:.2e} m/s)")
    print(f"\n    MR to 0.10c across fusion exhaust regimes:")
    for row in fusion_closure_scan(0.10):
        print(f"      {row['regime']:<32} ve/c={row['ve_over_c']:.4f}  "
              f"Isp={row['isp_s']:.3e} s  MR={row['MR_to_beta']:.2f}  "
              f"(log10={row['log10_MR']:.2f})")
    print(f"\n    Helium-3 for a 1,000 kg D-He3 probe to 0.10c (eta=0.5):")
    h = he3_requirement(1000.0, 1.03e7, 0.10)
    print(f"      MR={h['mass_ratio']:.1f}  propellant={h['propellant_kg']:,.0f} kg  "
          f"reactant fuel={h['reactant_kg']:,.0f} kg  He-3={h['he3_kg']:,.0f} kg")

    print("\n[B] CREWED ROUND-TRIP CLOSURE (accel + decel)")
    for row in crewed_roundtrip_table():
        print(f"    beta={row['beta_cruise']:.2f}  dv={row['dv_total_km_s']:,.0f} km/s  "
              f"cruise(one-way)={row['crew_years_one_way_PC']:6.1f} yr  "
              f"Isp_req(MR=10)={row['isp_req_MR10']:,.0f} s  "
              f"photon MR={row['photon_rocket_MR']:.3f}")
    print("    Carried-return propellant cost (per-leg MR squared):")
    for beta in (0.05, 0.10):
        c = carried_return_fuel_doubling(1.0, beta, 1.03e7)
        print(f"      ve=0.034c: per-leg MR={c['mr_per_leg']:.2f}  "
              f"carried-return MR={c['mr_carry_return']:.1f} -> {c['verdict']}")

    print("\n[C] BEAMED-SAIL DELIVERED-ENERGY ECONOMICS")
    for beta in (0.01, 0.05, 0.10, 0.20):
        e = sail_energy_per_kg(beta)
        print(f"    beta={beta:.2f}: {e['delivered_J_per_kg']:.2e} J/kg = "
              f"{e['delivered_Mt_TNT_per_kg']:.3f} Mt TNT/kg = "
              f"{e['world_electricity_minutes_per_kg']:.1f} min of world electricity/kg")
    print("\n    Array power scaling at fixed 0.05 AU beam length:")
    for m in (1e-3, 1e-2, 1.0, 1e3):
        s = sail_array_scaling(m, 0.20)
        print(f"      m={m:8.3g} kg -> P={s['required_array_GW']:8.3g} GW  "
              f"t={s['push_time_days']:8.3g} d  beam energy={s['energy_sunk_in_beam_J']:.2e} J")
    star = sail_array_scaling(1e-3, 0.20, beam_distance_au=0.0186)
    print(f"    ANCHOR CHECK: 1 g sail to 0.2c over 0.0186 AU -> "
          f"P={star['required_array_GW']:.1f} GW (Starshot: 100 GW)")
    print("\n    Antimatter cost per 1000 kg payload (eta=0.3):")
    for beta in (0.01, 0.05, 0.10):
        for decel in (False, True):
            p = photon_rocket_cost(beta, 1000.0, 0.3, decel)
            print(f"      beta={beta:.2f} decel={decel!s:<5} "
                  f"E={p['energy_Mt_TNT']:9.2f} Mt  anti={p['antimatter_g']:9.2f} g  "
                  f"cost=${p['cost_USD']:.2e}")

    print("\n[D] SOLAR-SAIL TERMINAL VELOCITY (finite solar flux caps it)")
    for sigma, r0 in ((0.010, 0.5), (0.001, 0.5), (1e-4, 0.5), (1e-4, 0.05)):
        t = solar_sail_terminal_velocity(sigma, r0)
        print(f"    sigma={sigma*1e3:7.3f} g/m^2  r0={r0:.2f} AU  "
              f"v_max={t['v_max_m_s']/1e3:8.1f} km/s = {t['v_max_over_c']:.2e} c  "
              f"(Proxima in {t['years_to_PROXIMA']:,.0f} yr)")

    print("\n[E] ANTIMATTER PRODUCTION WALL")
    w = antiproton_wall(2.5)
    print(f"    2.5 kg antimatter at {CERN_AP_YIELD_G_YR:.0e} g/yr -> "
          f"{w['production_years_at_current_rate']:.2e} yr "
          f"({w['years_universe_age_units']:.1e} x age of universe); "
          f"at 1e6x rate: {w['production_years_1e6x_rate']:.2e} yr")

    print("\n[F] MISSION CAPABILITY MATRIX (propellant families, MR<=10)")
    for row in capability_matrix():
        print(f"    {row['family']:<12} dv_max(MR=10)={row['dv_at_MR10_km_s']:9.1f} km/s  "
              f"clears={len(row['clears'])}/{len(MISSIONS)}  "
              f"blocked: {', '.join(row['blocked_by']) if row['blocked_by'] else 'none'}")


if __name__ == "__main__":
    report()
