"""
test_propulsion_mission_capability_and_erosion_engine.py
========================================================
Verification suite for propulsion mission capability, dust erosion physics,
laser sail thermal absorption limits, and Liquid Droplet Radiator scaling.

Author: Kepler (Agent A001, Generation 0)
Domain: Practical space propulsion (propulsion)
Epistemic Class: Engineering feasibility
"""

import math
import sys
from propulsion_mission_capability_and_erosion_engine import (
    relativistic_gamma,
    thrust_to_jet_power_ratio,
    laser_sail_thrust_per_beam_power,
    laser_sail_critical_absorption,
    laser_sail_equilibrium_temperature,
    interstellar_gas_sputtering_thickness,
    dust_grain_kinetic_energy,
    dust_collision_probability,
    ldr_burn_characteristics,
    sgl_550au_transit_time_years,
    get_complete_mission_capability_database,
    C, D_PROXIMA, LY
)


def run_all_tests():
    passed = 0
    failed = 0

    def check(name: str, cond: bool, msg: str = ""):
        nonlocal passed, failed
        if cond:
            print(f"PASS: {name} {msg}")
            passed += 1
        else:
            print(f"FAIL: {name} {msg}")
            failed += 1

    # 1. Lorentz Gamma
    gamma_02 = relativistic_gamma(0.20)
    check("gamma_02", math.isclose(gamma_02, 1.0206207, rel_tol=1e-5), f"gamma = {gamma_02:.7f}")

    # 2. Thrust per Jet Power Duality
    f_p_chem = thrust_to_jet_power_ratio(4432.0)
    check("thrust_per_power_chem", 440.0 < f_p_chem < 460.0, f"F/P chem = {f_p_chem:.1f} N/MW")

    f_p_fusion = thrust_to_jet_power_ratio(13488000.0)
    check("thrust_per_power_fusion", 0.14 < f_p_fusion < 0.16, f"F/P fusion = {f_p_fusion:.3f} N/MW")

    f_p_photon = laser_sail_thrust_per_beam_power()
    check("thrust_per_power_laser", math.isclose(f_p_photon, 6.67128, rel_tol=1e-4), f"F/P laser = {f_p_photon:.3f} N/GW")

    # 3. Laser Sail Thermal Absorption Limit
    i_laser = 6.25e9  # 6.25 GW/m^2
    a_abs_crit = laser_sail_critical_absorption(i_laser, max_temp_k=1000.0, emissivity=0.50)
    check("laser_sail_critical_absorption", 8.5e-6 < a_abs_crit < 9.5e-6, f"A_abs_crit = {a_abs_crit:.2e}")

    # 4. Laser Sail Equilibrium Temperatures
    t_safe = laser_sail_equilibrium_temperature(i_laser, absorption=9.07e-6, emissivity=0.50)
    check("laser_sail_temp_safe", 990.0 < t_safe < 1010.0, f"T_safe = {t_safe:.1f} K")

    t_melt = laser_sail_equilibrium_temperature(i_laser, absorption=1.0e-4, emissivity=0.50)
    check("laser_sail_temp_melt", 1800.0 < t_melt < 1850.0, f"T_melt = {t_melt:.1f} K")

    # 5. Interstellar Gas Sputtering
    e_p, fluence, thickness_m = interstellar_gas_sputtering_thickness(0.20, D_PROXIMA)
    check("proton_impact_energy", 18.0 < e_p < 20.0, f"E_p = {e_p:.2f} MeV")
    check("proton_fluence", 3.5e21 < fluence < 4.5e21, f"Fluence = {fluence:.2e} m^-2")
    check("sputtering_thickness_sub_nanometer", thickness_m < 1e-9, f"Thickness = {thickness_m*1e9:.3f} nm")

    # 6. Dust Grain Energetics at 0.20c
    m_1um, ke_1um = dust_grain_kinetic_energy(1e-6, 0.20)
    check("ke_1micron_grain", 15.0 < ke_1um < 22.0, f"KE 1um = {ke_1um:.2f} J")

    m_10um, ke_10um = dust_grain_kinetic_energy(10e-6, 0.20)
    check("ke_10micron_grain_kilojoules", 15000.0 < ke_10um < 22000.0, f"KE 10um = {ke_10um/1000.0:.2f} kJ")

    # 7. Dust Collision Probabilities
    # Broadside 4cm x 4cm wafercraft: A = 1.6e-3 m^2
    hits_broad, surv_broad = dust_collision_probability(1.6e-3, D_PROXIMA)
    check("dust_broadside_hits", 2.8 < hits_broad < 3.6, f"Hits broadside = {hits_broad:.2f}")
    check("dust_broadside_survival_low", surv_broad < 0.06, f"Survival broadside = {surv_broad*100:.1f}%")

    # Edge-on wafercraft: 4cm x 0.4mm: A = 1.6e-5 m^2 (100x smaller)
    hits_edge, surv_edge = dust_collision_probability(1.6e-5, D_PROXIMA)
    check("dust_edge_hits", hits_edge < 0.05, f"Hits edge-on = {hits_edge:.3f}")
    check("dust_edge_survival_high", surv_edge > 0.95, f"Survival edge-on = {surv_edge*100:.1f}%")

    # 8. Liquid Droplet Radiator (LDR) Fusion Decoupling
    a_max_ldr, t_burn_ldr, d_burn_ldr = ldr_burn_characteristics(
        beta=0.10, ve=13490000.0, efficiency=0.50, radiator_temp_k=1500.0, areal_density_kg_m2=0.50
    )
    check("ldr_acceleration_10x", 0.14 < a_max_ldr < 0.17, f"a_max LDR = {a_max_ldr:.4f} m/s^2")
    check("ldr_burn_time_years", 5.5 < t_burn_ldr < 7.0, f"Burn time LDR = {t_burn_ldr:.2f} yr")
    check("ldr_burn_dist_ly", 0.25 < d_burn_ldr < 0.35, f"Burn distance LDR = {d_burn_ldr:.2f} ly")

    # 9. SGL 550 AU Flight Times
    t_voyager = sgl_550au_transit_time_years(17.0)
    check("sgl_voyager_decades", 145.0 < t_voyager < 160.0, f"Voyager 550 AU = {t_voyager:.1f} yr")

    t_sail = sgl_550au_transit_time_years(120.0)
    check("sgl_solar_sail_feasible", 20.0 < t_sail < 23.0, f"Solar Sail 550 AU = {t_sail:.1f} yr")

    t_laser = sgl_550au_transit_time_years(0.20 * C / 1000.0)
    check("sgl_laser_sail_days", t_laser * 365.25 < 20.0, f"Starshot 550 AU = {t_laser * 365.25:.1f} days")

    # 10. Master Mission Database
    db = get_complete_mission_capability_database()
    check("database_all_9_families", len(db) == 9, f"Evaluated {len(db)} propulsion families")
    interstellar_count = sum(1 for v in db.values() if v["interstellar_capable"])
    check("interstellar_trilemma", interstellar_count == 3, f"Exactly {interstellar_count} families interstellar capable")

    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 50)
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
