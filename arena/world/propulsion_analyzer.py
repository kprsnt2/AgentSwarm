#!/usr/bin/env python3
"""
propulsion_analyzer.py
======================
Quantitative comparison of practical space-propulsion options.

Author : Hypatia (Agent A003, Generation 0)
Domain : Practical space propulsion
Standard of evidence: conservation laws, thermodynamics, relativity, rocket equation.

All numbers are SI unless noted.  g0 = 9.80665 m/s^2 (exact, ISO 80000-3).
Rocket equation:  dv = Isp * g0 * ln(m0/mf)  ==  ve * ln(MR)
Energy of exhaust jet: P_jet = 0.5 * mdot * ve^2 = 0.5 * T * ve
Radiation pressure (perfect reflector): P = 2 S / c
Relativistic kinetic energy: (gamma - 1) m c^2
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field

# ----------------------------------------------------------------------------
# Constants (CODATA 2018 / IAU)
# ----------------------------------------------------------------------------
G0 = 9.80665            # m/s^2, standard gravity
C = 299_792_458.0       # m/s, speed of light (exact)
AU = 1.495_978_707e11   # m
YEAR = 3.155_760e7      # s (Julian year)
LY = 9.460_730_472_580_8e15  # m
S0 = 1361.0             # W/m^2, solar constant at 1 AU
GLOBAL_PRIMARY_ENERGY = 6.0e20   # J/yr, order of world primary energy consumption
TNT_TON = 4.184e9       # J
PROTON_MASS = 1.672_621_923_69e-27  # kg
EARTH_MASS = 5.9722e24
JUPITER_MASS = 1.8982e27


# ----------------------------------------------------------------------------
# Core rocket-engineering relations
# ----------------------------------------------------------------------------
def exhaust_velocity(isp: float) -> float:
    """Effective exhaust velocity ve = Isp * g0  [m/s]."""
    return isp * G0


def mass_ratio(dv: float, isp: float) -> float:
    """m0/mf = exp(dv / (Isp g0)) from the Tsiolkovsky rocket equation.

    Returns float('inf') when the exponent exceeds ~709 (double overflow).
    Use log10_mass_ratio() for the astronomical regime.
    """
    x = dv / exhaust_velocity(isp)
    if x > 709.0:
        return float("inf")
    return math.exp(x)


def log10_mass_ratio(dv: float, isp: float) -> float:
    """log10(m0/mf) = dv / (ve ln 10); safe for arbitrarily large exponents."""
    return dv / (exhaust_velocity(isp) * math.log(10.0))


def propellant_fraction(mr: float) -> float:
    """Propellant mass / initial mass = 1 - 1/MR (single stage, no payload struct)."""
    return 1.0 - 1.0 / mr


def jet_power(thrust: float, isp: float) -> float:
    """Minimum jet kinetic power P = 0.5 T ve [W]."""
    return 0.5 * thrust * exhaust_velocity(isp)


def thrust_from_power(power: float, isp: float, eta: float = 1.0) -> float:
    """T = 2 eta P / ve  [N] (electric thrusters)."""
    return 2.0 * eta * power / exhaust_velocity(isp)


def kinetic_energy_classical(v: float, m: float = 1.0) -> float:
    return 0.5 * m * v * v


def kinetic_energy_relativistic(v: float, m: float = 1.0) -> float:
    beta = v / C
    b2 = beta * beta
    # Numerically stable (gamma - 1) = b2 / (sqrt(1-b2) * (1 + sqrt(1-b2)))
    # avoiding catastrophic cancellation as beta -> 0.
    s = math.sqrt(1.0 - b2)
    gamma_minus_1 = b2 / (s * (1.0 + s))
    return gamma_minus_1 * m * C * C


def photon_rocket_mass_ratio(dv: float) -> float:
    """Ideal photon rocket (ve = c): MR = exp(dv/c)."""
    return math.exp(dv / C)


# ----------------------------------------------------------------------------
# Propulsion system catalogue (best demonstrated / credibly projected values)
# ----------------------------------------------------------------------------
@dataclass
class Drive:
    name: str
    isp_s: float                 # specific impulse [s]
    thrust_n: float              # representative thrust per unit [N]
    # areal / power figures where relevant
    notes: str = ""
    kind: str = "rocket"
    peak_jet_power_w: float = 0.0

    @property
    def ve(self) -> float:
        return exhaust_velocity(self.isp_s)

    @property
    def jet_power(self) -> float:
        return jet_power(self.thrust_n, self.isp_s)


DRIVES = {
    # Solid/liquid chemical: energy is stored in bonds (~10-13 MJ/kg)
    "chemical_h2lox": Drive("Chemical LH2/LOX (RS-25 class)", 452, 2.28e6,
                            "ve=4.43 km/s; bond energy ~13 MJ/kg propellant", "chemical"),
    "chemical_storable": Drive("Chemical storable (NTO/MMH)", 320, 5.0e5,
                               "hypergolic, ve=3.14 km/s", "chemical"),
    "nuclear_thermal": Drive("Solid-core NERVA-class NTR", 850, 1.11e5,
                             "chamber ~3000 K; H2 dissociation limit ~3200 K", "nuclear"),
    "nuclear_thermal_adv": Drive("Advanced NTR (CERMET/DUV)", 950, 1.5e5,
                                 "materials-limited; carbide fuel", "nuclear"),
    "nuclear_pulse": Drive("Nuclear pulse (Orion)", 3000, 1.0e7,
                           "bomb units; pusher plate; test-ban blocked", "nuclear"),
    "nep_gridded": Drive("Nuclear electric (gridded ion, NEXT)", 4170, 0.236,
                         "NEXT: 6.9 kW, 236 mN, Isp 4170 s", "electric"),
    "nep_hall": Drive("Nuclear electric (Hall, AEPS)", 2600, 0.6,
                      "AEPS 12.5 kW, 600 mN, Isp 2600 s", "electric"),
    "sep": Drive("Solar electric (BPT-4000 Hall)", 1800, 0.29,
                 "solar power 1/r^2; ~4.5 kW", "electric"),
    "vismara": Drive("VASIMR / high-power EM", 5000, 5.0,
                     "200 kW test; needs multi-MW reactor", "electric"),
    "fusion_dhe3": Drive("Fusion D-He3 direct", 100000, 1.0e4,
                         "theoretical; aneutronic; no ignited device exists", "fusion"),
    "antimatter_photon": Drive("Antimatter photon rocket (ideal)", 3.06e7, 1.0e3,
                               "ve=c idealisation; real pions/muons dilute Isp", "antimatter"),
}

# Solar-sail / beamed-sail parameters (not Isp-based)
SAIL = {
    "perfect_reflector_force_per_area": 2.0 * S0 / C,   # N/m^2 at 1 AU
    "ikaros_areal_density": 0.010,   # kg/m^2, JAXA IKAROS ~10 g/m^2
    "lightsail2_areal_density": 0.0056,  # kg/m^2, ~5.6 g/m^2
    "starshot_sail_areal_density": 1.0e-4,  # kg/m^2, ~0.1 g/m^2 (proposed)
    "starshot_laser_power": 100e9,   # W, 100 GW phased array
    "starshot_sail_side": 4.0,       # m
    "starshot_craft_mass": 1.0e-3,   # kg, 1 gram
}


def sail_accel(areal_density: float, flux_multiplier: float = 1.0) -> float:
    """Characteristic acceleration a = 2 S / (c sigma) [m/s^2]."""
    return 2.0 * S0 * flux_multiplier / (C * areal_density)


# ----------------------------------------------------------------------------
# Mission delta-v budget (impulsive, from LEO unless stated)
# ----------------------------------------------------------------------------
MISSIONS = {
    "Earth surface -> LEO": 9.4e3,
    "LEO -> GEO (chemical)": 3.9e3,
    "LEO -> Lunar surface (one-way)": 5.9e3,
    "LEO -> Mars orbit (aerocapture)": 3.6e3,
    "LEO -> Mars surface (EDL)": 5.6e3,
    "LEO -> Mars surface & back": 12.0e3,
    "LEO -> Jupiter (flyby)": 6.3e3,
    "LEO -> Jupiter orbit": 9.0e3,
    "Solar system escape (from LEO)": 8.8e3,
    "Interstellar 0.01c (flyby)": 0.01 * C,
    "Interstellar 0.05c (flyby)": 0.05 * C,
    "Interstellar 0.10c (flyby)": 0.10 * C,
    "Interstellar 0.10c (accel+decel)": 0.20 * C,
    "Interstellar 0.20c (accel+decel)": 0.40 * C,
}


# ----------------------------------------------------------------------------
# Analysis routines
# ----------------------------------------------------------------------------
def rank_for_delta_v(dv: float, isp: float) -> dict:
    mr = mass_ratio(dv, isp)
    return {
        "isp_s": isp,
        "ve_km_s": exhaust_velocity(isp) / 1e3,
        "mass_ratio": mr,
        "log10_mass_ratio": math.log10(mr) if mr > 0 else float("inf"),
        "propellant_fraction": (1.0 - 1.0 / mr) if mr < 1e15 else float("nan"),
    }


def solar_sail_table() -> list[dict]:
    rows = []
    fpa = SAIL["perfect_reflector_force_per_area"]
    for label, sigma in [
        ("IKAROS-class (10 g/m^2)", SAIL["ikaros_areal_density"]),
        ("LightSail-2 (5.6 g/m^2)", SAIL["lightsail2_areal_density"]),
        ("Starshot-class (0.1 g/m^2)", SAIL["starshot_sail_areal_density"]),
    ]:
        a = sail_accel(sigma)
        # time to reach 30 km/s from rest under constant a
        v = 3.0e4
        t = v / a
        rows.append({
            "class": label,
            "sigma_kg_m2": sigma,
            "force_N_m2": fpa,
            "accel_m_s2": a,
            "accel_mm_s2": a * 1e3,
            "time_to_30km_s_days": t / 86400.0,
        })
    return rows


def starshot_check() -> dict:
    P = SAIL["starshot_laser_power"]
    side = SAIL["starshot_sail_side"]
    m = SAIL["starshot_craft_mass"]
    area = side * side
    F = 2.0 * P / C                      # ideal perfect reflection
    a = F / m
    # distance over which the laser can effectively push (diffraction limit)
    # beam waist w0 ~ 1 km, lambda ~ 1 um => Rayleigh range pi w0^2 / lambda
    lam = 1.06e-6
    w0 = 1000.0
    rayleigh = math.pi * w0 * w0 / lam
    v_at_rayleigh = math.sqrt(2.0 * a * rayleigh)
    absorbed_flux = P / area
    return {
        "force_N": F,
        "accel_m_s2": a,
        "accel_g": a / G0,
        "area_m2": area,
        "rayleigh_range_m": rayleigh,
        "rayleigh_range_AU": rayleigh / AU,
        "v_at_rayleigh_frac_c": v_at_rayleigh / C,
        "v_at_rayleigh_km_s": v_at_rayleigh / 1e3,
        "incident_flux_W_m2": absorbed_flux,
        "time_to_0p2c_min": (0.2 * C / a) / 60.0,
    }


def energy_budget_interstellar(v: float, m: float = 1.0) -> dict:
    ke = kinetic_energy_relativistic(v, m)
    return {
        "v_frac_c": v / C,
        "mass_kg": m,
        "KE_J": ke,
        "KE_ton_TNT": ke / TNT_TON,
        "KE_Mt_TNT": ke / (TNT_TON * 1e6),
        "years_of_world_energy": ke / GLOBAL_PRIMARY_ENERGY,
    }


def antimatter_budget(v: float, m: float = 1000.0, eta: float = 1.0) -> dict:
    """Total annihilated mass (matter+antimatter) needed for relativistic KE.

    Each kg of annihilated mass releases 2 m c^2 (matter + antimatter).
    eta = fraction of annihilation energy usable as directed exhaust.
    """
    ke = kinetic_energy_relativistic(v, m)
    total_annihilated = ke / (eta * 2.0 * C * C)
    antimatter_mass = total_annihilated / 2.0
    # CERN-cited production cost ~ $62.5 trillion per gram
    cost = antimatter_mass * 1e3 * 62.5e12
    return {
        "v_frac_c": v / C,
        "payload_kg": m,
        "KE_J": ke,
        "total_annihilated_kg": total_annihilated,
        "antimatter_kg": antimatter_mass,
        "antimatter_grams": antimatter_mass * 1e3,
        "cost_USD": cost,
        "eta_assumed": eta,
    }


def required_isp(dv: float, mass_ratio_target: float) -> float:
    """Isp needed so that a rocket with given m0/mf reaches dv.

    Isp = dv / (g0 ln MR).  This is the closure condition for any
    propellant-carrying interstellar vehicle.
    """
    return dv / (G0 * math.log(mass_ratio_target))


def nep_mission_time(power_w: float, isp: float, dry_mass_kg: float,
                     dv: float, eta: float = 0.6) -> dict:
    """Constant-power electric-propulsion burn time to reach dv.

    T = 2 eta P / ve;  mdot = T/ve;  accelerating mass falls as propellant
    is expelled.  Use the rocket equation to get propellant, then the
    momentum-limited burn time t = m_prop * ve / T (constant mdot).
    """
    ve = exhaust_velocity(isp)
    T = thrust_from_power(power_w, isp, eta)
    mr = mass_ratio(dv, isp)
    if not math.isfinite(mr) or mr > 1e6:
        return {"feasible": False, "mr": mr, "thrust_N": T}
    m0 = dry_mass_kg * mr
    m_prop = m0 - dry_mass_kg
    mdot = T / ve
    t = m_prop / mdot
    return {"feasible": True, "thrust_N": T, "mass_ratio": mr,
            "initial_mass_kg": m0, "propellant_kg": m_prop,
            "burn_time_s": t, "burn_time_days": t / 86400.0,
            "burn_time_years": t / YEAR}


def photon_rocket_interstellar(v_final: float, decel: bool, payload_kg: float) -> dict:
    """Ideal photon rocket mass ratio and antimatter fuel for a given final speed."""
    dv = v_final * (2.0 if decel else 1.0)
    mr = photon_rocket_mass_ratio(dv)
    m0 = payload_kg * mr
    return {
        "dv_frac_c": dv / C,
        "mass_ratio": mr,
        "initial_mass_kg": m0,
        "propellant_kg": m0 - payload_kg,
    }


def starshot_relativistic() -> dict:
    """Relativistic integration of a constant laser force on a 1 g sail.

    dp/dt = F  with p = gamma m v  =>  t = gamma m v / F.
    Work-energy:  F x = (gamma-1) m c^2  =>  x = (gamma-1) m c^2 / F.
    """
    P = SAIL["starshot_laser_power"]
    m = SAIL["starshot_craft_mass"]
    F = 2.0 * P / C
    out = {}
    for b in (0.10, 0.20):
        gamma = 1.0 / math.sqrt(1.0 - b * b)
        v = b * C
        t = gamma * m * v / F
        x = (gamma - 1.0) * m * C * C / F
        out[b] = {"gamma": gamma, "time_s": t, "dist_AU": x / AU}
    return out


def report() -> None:
    line = "=" * 78
    print(line)
    print("PROPULSION ANALYZER  --  Hypatia A003")
    print(line)

    print("\n[1] SOLAR-SAIL CHARACTERISTIC ACCELERATION AT 1 AU")
    print(f"    ideal reflector force/area = 2 S0/c = "
          f"{SAIL['perfect_reflector_force_per_area']*1e6:.2f} uN/m^2")
    for r in solar_sail_table():
        print(f"    {r['class']:<28} sigma={r['sigma_kg_m2']*1e3:5.2f} g/m^2  "
              f"a={r['accel_mm_s2']:7.3f} mm/s^2  "
              f"t(->30 km/s)={r['time_to_30km_s_days']:6.1f} d")

    print("\n[2] STARSHOT (100 GW, 4 m sail, 1 g) -- IDEALISED")
    s = starshot_check()
    print(f"    force={s['force_N']:.1f} N   a={s['accel_g']:.3e} g")
    print(f"    Rayleigh range={s['rayleigh_range_AU']:.2f} AU  "
          f"(ideal const-a would exceed c; integrate relativistically)")
    print(f"    incident flux on sail={s['incident_flux_W_m2']:.3e} W/m^2 "
          f"(~{s['incident_flux_W_m2']/1e6:.0f} MW/m^2)")
    print("    relativistic constant-force integration:")
    for b, r in starshot_relativistic().items():
        print(f"      beta={b:.2f}: t={r['time_s']:.1f} s  "
              f"x={r['dist_AU']*AU/1e9:.3f} Gm = {r['dist_AU']:.4f} AU  "
              f"gamma={r['gamma']:.4f}")

    print("\n[3] ROCKET-EQUATION MASS RATIOS BY MISSION x DRIVE")
    drives_for_table = ["chemical_h2lox", "nuclear_thermal", "nuclear_pulse",
                        "nep_gridded", "fusion_dhe3"]
    header = f"    {'mission':<34}" + "".join(f"{d[:10]:>13}" for d in drives_for_table)
    print(header)
    for mname, dv in MISSIONS.items():
        row = f"    {mname:<34}"
        for d in drives_for_table:
            lmr = log10_mass_ratio(dv, DRIVES[d].isp_s)
            cell = f"1e{lmr:.0f}" if lmr > 6 else f"{10**lmr:.1f}"
            row += f"{cell:>13}"
        print(row)

    print("\n[4] INTERSTELLAR MASS-RATIO CATASTROPHE (payload 1000 kg)")
    for v_frac in (0.01, 0.05, 0.10, 0.20):
        v = v_frac * C
        print(f"    --- v = {v_frac:.2f} c ---")
        for d in ["chemical_h2lox", "nuclear_thermal", "nuclear_pulse",
                  "fusion_dhe3"]:
            lmr = log10_mass_ratio(v, DRIVES[d].isp_s)
            lm0 = lmr + 3.0
            print(f"        {DRIVES[d].name:<36} MR=1e{lmr:7.1f}  "
                  f"m0=1e{lm0:7.1f} kg")
        pr = photon_rocket_interstellar(v, False, 1000.0)
        print(f"        {'ideal photon rocket (ve=c)':<36} "
              f"MR={pr['mass_ratio']:.3f}  m0={pr['initial_mass_kg']:.0f} kg")

    print("\n[5] RELATIVISTIC ENERGY BUDGET (per 1000 kg payload)")
    for v_frac in (0.01, 0.05, 0.10, 0.20):
        eb = energy_budget_interstellar(v_frac * C, 1000.0)
        print(f"    v={v_frac:.2f}c  KE={eb['KE_J']:.3e} J = "
              f"{eb['KE_Mt_TNT']:.2f} Mt TNT = "
              f"{eb['years_of_world_energy']:.3f} yr world energy")

    print("\n[6] ANTIMATTER FUEL BUDGET (1000 kg payload to 0.10c)")
    for eta in (1.0, 0.5, 0.1):
        ab = antimatter_budget(0.10 * C, 1000.0, eta)
        print(f"    eta={eta:.1f}: antimatter={ab['antimatter_grams']:.3f} g  "
              f"cost=${ab['cost_USD']:.3e}")

    print("\n[7] ELECTRIC-PROPULSION THRUST-POWER COUPLING")
    for isp in (2000, 4000, 6000, 10000):
        for P_kw in (10, 100, 1000):
            T = thrust_from_power(P_kw * 1e3, isp, 0.6)
            print(f"    Isp={isp:5d}s  P={P_kw:5d} kW  T={T*1e3:8.2f} mN")
        print()

    print("\n[8] REQUIRED Isp FOR INTERSTELLAR CLOSURE (propellant-carrying)")
    print("    Isp_req = dv / (g0 ln MR)")
    for mr in (5.0, 10.0, 100.0):
        row = f"    MR={mr:6.1f}: "
        for v_frac in (0.01, 0.05, 0.10, 0.20):
            row += f"  {v_frac:.2f}c->{required_isp(v_frac*C, mr):,.0f}s"
        print(row)

    print("\n[9] NUCLEAR-ELECTRIC CARGO TUG (1 MWe, 20 kg/kWe, 20 t dry)")
    for isp in (3000, 5000, 8000):
        for dv in (5e3, 10e3, 20e3):
            r = nep_mission_time(1e6, isp, 20_000.0, dv)
            if r["feasible"]:
                print(f"    Isp={isp:5d}s dv={dv/1e3:4.1f} km/s  T={r['thrust_N']:6.2f} N  "
                      f"MR={r['mass_ratio']:4.2f}  prop={r['propellant_kg']:8.0f} kg  "
                      f"burn={r['burn_time_days']:7.1f} d")

    print("\n[10] CHEMICAL CEILING CHECK")
    print("    Best practical chemical Isp (LH2/LOX vacuum) ~ 452-465 s.")
    print("    Bond-energy bound: ve = sqrt(2 * Q_chem); Q~13 MJ/kg -> "
          f"ve~{math.sqrt(2*13e6)/1e3:.2f} km/s -> Isp~{math.sqrt(2*13e6)/G0:.0f} s")


if __name__ == "__main__":
    report()
