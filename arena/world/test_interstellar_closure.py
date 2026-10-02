#!/usr/bin/env python3
"""
test_interstellar_closure.py
============================
Verification suite for interstellar_closure_analyzer.py (Hypatia, A003).

Every check is either an identity guaranteed by the governing physics
(rocket equation, photon momentum transfer, energy conservation) or an
anchor to literature values (Starshot 100 GW, Daedalus mass ratio,
chemical bond-energy ceiling, antimatter energy density).
"""

from __future__ import annotations
import math

import interstellar_closure_analyzer as ic

PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {name}" + (f"   [{detail}]" if detail else ""))
    else:
        FAIL += 1
        print(f"  FAIL  {name}   [{detail}]")


def close(a: float, b: float, rel: float = 1e-6) -> bool:
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-300)


print("=" * 78)
print("TEST SUITE: interstellar closure (Hypatia A003)")
print("=" * 78)

# ---------------------------------------------------------------- rocket eq
print("\n[1] Rocket-equation identities")
check("MR to 0.1c at 452 s Isp ~ 1e2937",
      close(ic.log10_mass_ratio(0.10 * ic.C, 452 * ic.G0), 2936.6, 1e-3))
check("photon rocket ve=c: MR = e^0.1 = 1.10517",
      close(ic.mass_ratio(0.10 * ic.C, ic.C), math.exp(0.1), 1e-12))
check("Isp closure: dv/(g0 ln10) = 1.328e6 s at 0.1c",
      close(ic.required_isp(0.10 * ic.C, 10.0), 1_327_652, 1e-4))
check("relativistic KE 0.1c per kg = 4.527e14 J (gamma-1 = 0.005038)",
      close(ic.kinetic_energy_per_kg(0.10 * ic.C), 4.5268e14, 1e-3))
check("KE reduces to 0.5 v^2 at low speed (rel=1e-3 at 1000 km/s)",
      close(ic.kinetic_energy_per_kg(1e6), 0.5e12, 2e-3))

# ------------------------------------------------------------- fusion physics
print("\n[2] Fusion exhaust-velocity physics")
dt = ic.REACTIONS["D-T (main)"]
dhe3 = ic.REACTIONS["D-He3"]
check("D-T energy density = 3.38e14 J/kg (literature)",
      close(ic.q_per_kg(dt), 3.38e14, 3e-2), f"{ic.q_per_kg(dt):.3e}")
check("D-He3 energy density = 3.63e14 J/kg",
      close(ic.q_per_kg(dhe3), 3.63e14, 3e-2), f"{ic.q_per_kg(dhe3):.3e}")
check("D-T charged fraction ~0.20 (neutrons carry 80%)",
      close(ic.charged_fraction(dt), 0.199, 2e-2))
check("D-T directed ve ceiling <= 0.05c",
      0.035 < ic.max_directed_exhaust_velocity(dt) / ic.C < 0.05)
check("D-He3 directed ve ceiling ~0.088c",
      close(ic.max_directed_exhaust_velocity(dhe3) / ic.C, 0.0884, 2e-2))
check("fusion MR to 0.1c spans 3-20 across realistic regimes",
      3.0 <= ic.fusion_closure_scan(0.10)[0]["MR_to_beta"] <= 20.0)
scan = {r["regime"]: r for r in ic.fusion_closure_scan(0.10)}
check("Daedalus-design ve gives MR=18.4 to 0.1c (NOT 1e13)",
      close(scan["Daedalus design point (lit.)"]["MR_to_beta"], 18.37, 5e-3))

d = ic.daedalus_anchor()
check("Daedalus implied ve = beta c / ln MR ~ 0.045c",
      close(d["implied_ve_over_c"], 0.0451, 5e-2))
check("Daedalus mass ratio ~14 (50,000 t / 3,500 t)",
      close(d["mass_ratio"], 50_000 / 3_500, 1e-9))

h = ic.he3_requirement(1000.0, 1.03e7, 0.10)
check("He-3 for 1 t probe to 0.1c is ~1.3 t, i.e. MORE than the payload",
      1000 < h["he3_kg"] < 2000, f"{h['he3_kg']:.0f} kg")

# -------------------------------------------------------------- round trips
print("\n[3] Crewed round-trip closure")
rows = {r["beta_cruise"]: r for r in ic.crewed_roundtrip_table()}
check("0.1c crewed: Isp_req(MR=10) = 2.655e6 s",
      close(rows[0.10]["isp_req_MR10"], 2_655_305, 1e-4))
check("0.1c photon round-trip MR = e^0.2 = 1.2214",
      close(rows[0.10]["photon_rocket_MR"], math.exp(0.2), 1e-9))
check("0.05c crewed cruise to Proxima = 84.9 yr",
      close(rows[0.05]["crew_years_one_way_PC"], 84.85, 2e-3))
cr = ic.carried_return_fuel_doubling(1.0, 0.10, 1.03e7)
check("carried-return squares the per-leg MR (18.4 -> 337)",
      close(cr["mr_carry_return"], cr["mr_per_leg"] ** 2, 1e-9))

# ------------------------------------------------------------- sail economics
print("\n[4] Beamed-sail energy economics and array scaling")
e10 = ic.sail_energy_per_kg(0.10)
check("delivered beam energy floor at 0.1c = KE = 4.527e14 J/kg",
      close(e10["KE_J_per_kg"], 4.5268e14, 1e-3))
check("0.1c/kg = 2.2 min of world electricity output (at eta=1)",
      1.5 < e10["world_electricity_minutes_per_kg"] < 3.0,
      f"{e10['world_electricity_minutes_per_kg']:.1f} min")
star = ic.sail_array_scaling(1e-3, 0.20, beam_distance_au=0.0186)
check("1 g sail to 0.2c over 0.0186 AU reproduces 100 GW literature array",
      close(star["required_array_GW"], 100.0, 5e-3),
      f"{star['required_array_GW']:.1f} GW")
big = ic.sail_array_scaling(1e3, 0.20)
one = ic.sail_array_scaling(1.0, 0.20)
check("array power scales linearly with sail mass",
      close(big["required_array_GW"] / one["required_array_GW"], 1000.0, 1e-9))
check("tonne-scale sail needs ~37 TW array (off by 5e5 vs Starshot)",
      close(big["required_array_GW"], 3.71e7, 5e-3))
check("beam energy >= craft KE (photon momentum tax)",
      star["beam_energy_over_KE"] >= 1.0)

p = ic.photon_rocket_cost(0.10, 1000.0, 0.3, False)
check("antimatter at eta=0.3: 4.2 g anti per kg payload (0.4%) to 0.1c",
      close(p["antimatter_over_payload"], 4.198e-3, 5e-3))
check("antimatter at eta=1: 1.26 kg per tonne payload (original finding)",
      close(ic.photon_rocket_cost(0.10, 1000.0, 1.0, False)["antimatter_kg"], 1.2624, 5e-3))
check("antimatter cost 1 t to 0.1c = $2.6e17 (eta=0.3)",
      close(p["cost_USD"], 2.62e17, 5e-3))
check("photon round-trip KE doubles antimatter mass",
      close(ic.photon_rocket_cost(0.10, 1000.0, 0.3, True)["antimatter_kg"] /
            p["antimatter_kg"], 2.0, 1e-9))

# --------------------------------------------------------- solar-sail ceiling
print("\n[5] Solar-sail terminal velocity (finite solar flux)")
check("ideal 0.1 g/m^2 sail from 0.5 AU caps below 0.001c",
      ic.solar_sail_terminal_velocity(1e-4, 0.5)["v_max_over_c"] < 1e-3)
check("v_max^2 = 2 a_1AU AU^2 / r0 identity",
      close(ic.solar_sail_terminal_velocity(1e-4, 0.5)["v_max_over_c"], 7.78e-4, 2e-3))
check("closer perihelion raises terminal velocity (integral of 1/r^2)",
      ic.solar_sail_terminal_velocity(1e-4, 0.05)["v_max_over_c"] >
      ic.solar_sail_terminal_velocity(1e-4, 0.5)["v_max_over_c"])
check("even 1 g/m^2 sail from 0.05 AU stays < 1e-3 c",
      ic.solar_sail_terminal_velocity(1e-3, 0.05)["v_max_over_c"] < 1e-3)
check("Proxima by solar sail: >= 1700 yr even at 0.1 g/m^2, 0.05 AU",
      ic.solar_sail_terminal_velocity(1e-4, 0.05)["years_to_PROXIMA"] > 1700)

# ------------------------------------------------------------ antiproton wall
print("\n[6] Antimatter production wall")
w = ic.antiproton_wall(2.5)
check("2.5 kg at CERN nanogram/yr rate needs ~2.5e12 yr",
      close(w["production_years_at_current_rate"], 2.5e12, 1e-9))
check("even 1e6x rate improvement: ~2.5e6 yr",
      close(w["production_years_1e6x_rate"], 2.5e6, 1e-9))

# --------------------------------------------------------------- capability
print("\n[7] Mission capability matrix")
mat = {r["family"]: r for r in ic.capability_matrix()}
check("chemical dv at MR=10 = 10.2 km/s (can't do Mars-and-back)",
      close(mat["chemical"]["dv_at_MR10_km_s"], 10.2, 2e-3))
check("NTR clears Mars-and-back with headroom",
      "LEO->Mars&back" in mat["NTR"]["clears"])
check("fusion at Daedalus ve clears 0.05c but not 0.1c at MR<=10",
      "0.05c flyby" in mat["fusion"]["clears"] and
      "0.10c flyby" in mat["fusion"]["blocked_by"])
check("ideal antimatter clears every mission at MR<=10",
      len(mat["antimatter"]["blocked_by"]) == 0)
check("no propellant family below 1e6 s clears 0.1c at MR<=10",
      all("0.10c flyby" in mat[f]["blocked_by"]
          for f in ("chemical", "NTR", "SEP/ion", "NEP", "pulse")))

# ------------------------------------------------------------------- summary
print("\n" + "=" * 78)
print(f"RESULT: {PASS} passed, {FAIL} failed")
print("=" * 78)
raise SystemExit(1 if FAIL else 0)
