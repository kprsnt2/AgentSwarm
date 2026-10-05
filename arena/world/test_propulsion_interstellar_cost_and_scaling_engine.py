"""
test_propulsion_interstellar_cost_and_scaling_engine.py
=======================================================
Verification suite for propulsion_interstellar_cost_and_scaling_engine.py.
Tests relativistic kinematics, staging physics, Stefan-Boltzmann radiator clamps,
beamed-energy photon momentum penalties, and production energy economics.
"""

import math
import sys
from propulsion_interstellar_cost_and_scaling_engine import (
    C,
    G0,
    D_PROXIMA,
    YEAR_S,
    relativistic_gamma,
    relativistic_ke_per_kg,
    relativistic_mass_ratio,
    log10_relativistic_mass_ratio,
    single_stage_mass_ratio_with_structure,
    two_stage_rendezvous_mass_ratio,
    radiator_clamped_acceleration,
    radiator_burn_metrics,
    beamed_sail_energetics_per_kg,
    antimatter_energy_and_grid_cost,
    fusion_reaction_energetics,
    transit_time_years,
    evaluate_all_propulsion_options
)


def run_all_tests():
    passed = 0
    failed = 0

    def check(name: str, condition: bool, msg: str = ""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"PASS: {name} {msg}")
        else:
            failed += 1
            print(f"FAIL: {name} {msg}")

    # 1. Relativistic Gamma and KE
    g_01 = relativistic_gamma(0.10)
    check("gamma_01", abs(g_01 - 1.0050378) < 1e-6, f"gamma = {g_01}")
    ke_01 = relativistic_ke_per_kg(0.10)
    check("ke_01_joules", abs(ke_01 - 4.5278e14) < 1e12, f"KE = {ke_01:.3e} J/kg")

    # 2. Relativistic Mass Ratio
    # Fusion at 0.045c
    r_fusion = relativistic_mass_ratio(0.10, 0.045 * C)
    check("fusion_mass_ratio_flyby", abs(r_fusion - 9.30) < 0.05, f"R = {r_fusion:.2f}")
    # Antimatter at 0.331c
    r_am = relativistic_mass_ratio(0.10, 0.331 * C)
    check("am_mass_ratio_flyby", abs(r_am - 1.354) < 0.01, f"R = {r_am:.3f}")

    # 3. Chemical and NTR Mass Ratio Log10 check
    log_chem = log10_relativistic_mass_ratio(0.10, 452.0 * G0)
    check("chem_log10_mass_ratio", 2940 < log_chem < 2960, f"log10(R) = {log_chem:.1f}")
    log_ntr = log10_relativistic_mass_ratio(0.10, 850.0 * G0)
    check("ntr_log10_mass_ratio", 1560 < log_ntr < 1580, f"log10(R) = {log_ntr:.1f}")

    # 4. Structural Mass Fraction & Staging Bounds
    # Single-stage with epsilon=0.05 fails if R >= 20
    check("single_stage_fusion_flyby_feasible",
          not math.isinf(single_stage_mass_ratio_with_structure(r_fusion, 0.05)),
          "Flyby clears single stage")
    check("single_stage_fusion_rendezvous_impossible",
          math.isinf(single_stage_mass_ratio_with_structure(r_fusion**2, 0.05)),
          "Rendezvous (R=86.4) strictly exceeds 1/epsilon = 20")

    # Two-stage rendezvous mass ratio
    m0_rendezvous_fusion = two_stage_rendezvous_mass_ratio(0.10, 0.045 * C, 0.05)
    check("two_stage_rendezvous_fusion",
          250.0 < m0_rendezvous_fusion < 300.0,
          f"m0/mL = {m0_rendezvous_fusion:.1f} kg per kg payload")

    # 5. Radiator Clamped Acceleration
    a_clamp_fusion = radiator_clamped_acceleration(0.045 * C, 0.50, 1500.0)
    check("fusion_radiator_acceleration_clamp",
          0.010 < a_clamp_fusion < 0.020,
          f"a_max = {a_clamp_fusion:.4f} m/s^2")
    t_burn_f, d_burn_f = radiator_burn_metrics(0.10 * C, a_clamp_fusion)
    t_burn_yr = t_burn_f / YEAR_S
    d_burn_ly = d_burn_f / (9.4607304725808e15)
    check("fusion_burn_time_decades",
          50.0 < t_burn_yr < 80.0,
          f"Burn time = {t_burn_yr:.1f} yr, Burn dist = {d_burn_ly:.2f} ly")

    # 6. Beamed Sail Photon Momentum Penalty
    sail_metrics = beamed_sail_energetics_per_kg(0.20)
    check("photon_momentum_ratio_approx_5",
          abs(sail_metrics["ratio_beam_ke"] - 4.85) < 0.1,
          f"E_beam / E_k = {sail_metrics['ratio_beam_ke']:.2f}")
    check("grid_energy_twh_per_tonne_starshot",
          6000.0 < sail_metrics["e_grid_twh_tonne"] < 6500.0,
          f"Grid energy = {sail_metrics['e_grid_twh_tonne']:.2f} TWh/tonne")

    # 7. Antimatter Accelerator Production Energy Penalty
    # For rendezvous, ~0.42 kg of antiprotons needed per kg payload
    am_info = antimatter_energy_and_grid_cost(0.4285)
    check("antimatter_grid_cost_planetary_scale",
          am_info["e_grid_twh"] > 1e10,
          f"Antimatter grid cost = {am_info['e_grid_twh']:.2e} TWh/kg")

    # 8. Hybrid Magsail Transit Time Expansion
    t_flyby = transit_time_years(D_PROXIMA, 0.20)
    t_magsail = transit_time_years(D_PROXIMA, 0.20, is_decelerating_magsail=True)
    check("magsail_transit_time_expansion",
          abs(t_magsail / t_flyby - 6.002) < 0.01,
          f"Flyby: {t_flyby:.1f} yr, Magsail rendezvous: {t_magsail:.1f} yr")

    # 9. All Propulsion Options Comprehensive Evaluation
    all_rows = evaluate_all_propulsion_options(0.10, 1.0)
    check("total_propulsion_options_count", len(all_rows) == 9, f"Evaluated {len(all_rows)} options")
    capable = [r["name"] for r in all_rows if r["interstellar_capable"]]
    check("interstellar_capable_options",
          set(capable) == {"Nuclear Fusion (D-3He)", "Antimatter Beamed-Core", "Laser-Pushed Beamed Sail"},
          f"Capable: {capable}")

    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 50)
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
