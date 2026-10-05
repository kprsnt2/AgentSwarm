"""
test_propulsion_engineering_synthesis.py
========================================
Test suite for Kepler's propulsion engineering synthesis.
Verifies all physics relations, relativistic rocket equations,
staging bounds, Stuhlinger specific power limits, diffraction bounds,
antimatter gamma-radiator scaling, and fusion ceilings.
"""

import math
import sys
from propulsion_engineering_synthesis import (
    C, G0, YEAR, AU, PI,
    relativistic_gamma,
    relativistic_kinetic_energy,
    classical_kinetic_energy,
    classical_mass_ratio,
    relativistic_mass_ratio,
    continuous_staging_mass_ratio,
    n_stage_mass_ratio,
    stuhlinger_burn_time,
    required_specific_power,
    laser_sail_diffraction_aperture,
    laser_sail_pointing_accuracy_rad,
    laser_sail_equilibrium_temp,
    antimatter_pion_exhaust_velocity,
    antimatter_gamma_power_and_radiator_mass,
    fusion_exhaust_velocity_theoretical
)

def run_tests():
    passed = 0
    failed = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"PASS: {name} {detail}")
            passed += 1
        else:
            print(f"FAIL: {name} {detail}")
            failed += 1

    # 1. Relativistic energy and gamma tests
    gamma_01 = relativistic_gamma(0.10)
    check("gamma_at_0.1c", math.isclose(gamma_01, 1.0050378, rel_tol=1e-5), f"gamma = {gamma_01}")
    ke_rel_01 = relativistic_kinetic_energy(1.0, 0.10)
    check("ke_rel_0.1c_per_kg", math.isclose(ke_rel_01, 4.527756e14, rel_tol=1e-4), f"KE = {ke_rel_01:.3e} J")
    ke_class_01 = classical_kinetic_energy(1.0, 0.10 * C)
    check("rel_ke_higher_than_classical", ke_rel_01 > ke_class_01, f"{ke_rel_01} > {ke_class_01}")

    # 2. Relativistic vs Classical Rocket Equation
    # At ve = c, photon rocket: R = sqrt((1+beta)/(1-beta))
    r_photon_01 = relativistic_mass_ratio(0.10, C)
    r_photon_expected = math.sqrt(1.10 / 0.90)  # ~1.10554
    check("photon_rocket_0.1c", math.isclose(r_photon_01, r_photon_expected, rel_tol=1e-4), f"R = {r_photon_01:.5f}")

    # Fusion at ve = 0.05c
    r_fusion_rel_01 = relativistic_mass_ratio(0.10, 0.05 * C)
    check("fusion_mass_ratio_0.1c", math.isclose(r_fusion_rel_01, 7.4388, rel_tol=1e-3), f"R = {r_fusion_rel_01:.4f}")

    # 3. Staging and structural fraction limits
    # Chemical: ve = 4432 m/s, delta_v = 0.01c = 2.9979e6 m/s, epsilon = 0.05
    # Continuous staging limit:
    # ln(R) = delta_v / (ve * (1 - epsilon)) = 2.9979e6 / (4432.4 * 0.95) = 712.0
    r_inf_chem_001c_log10 = (0.01 * C) / (452.0 * G0 * 0.95) / math.log(10)
    check("chem_infinite_staging_log10_exceeds_300", r_inf_chem_001c_log10 > 300, f"log10(R) = {r_inf_chem_001c_log10:.1f}")

    # 5-stage chemical cannot reach 0.01c:
    r_5_stage = n_stage_mass_ratio(5, 0.01 * C, 452.0 * G0, 0.05)
    check("chem_5_stage_impossible", math.isinf(r_5_stage), "5-stage delta-v exceeds structural limit per stage")

    # 4. Stuhlinger specific power limit
    # At alpha = 100 W/kg (optimistic space fission), burn time to 0.1c (3e7 m/s):
    tb_01c_100w = stuhlinger_burn_time(0.10 * C, 100.0)
    tb_years = tb_01c_100w / YEAR
    check("stuhlinger_burn_time_nep_exceeds_100kyr", tb_years > 140000, f"Burn time = {tb_years:.1f} years")

    # Specific power required for 20-year burn to 0.1c:
    alpha_req_20yr = required_specific_power(0.10 * C, 20.0 * YEAR)
    check("alpha_required_for_20yr_exceeds_500kw_kg", alpha_req_20yr > 700000.0, f"alpha_req = {alpha_req_20yr:.1f} W/kg")

    # 5. Laser sail diffraction limit
    # Wavelength 1.06 um, L = 0.0186 AU, sail diameter = 4 m
    dist_starshot = 0.0186 * AU
    d_laser = laser_sail_diffraction_aperture(1.06e-6, dist_starshot, 4.0)
    check("laser_array_diameter_starshot_approx_1.8km", math.isclose(d_laser, 1798.0, rel_tol=0.05), f"D = {d_laser:.1f} m")

    pointing_tol_rad = laser_sail_pointing_accuracy_rad(4.0, dist_starshot)
    pointing_mas = pointing_tol_rad * (180.0 / PI) * 3600.0 * 1000.0
    check("laser_pointing_sub_milliarcsecond", pointing_mas < 0.2, f"Pointing tol = {pointing_mas:.3f} mas")

    # Sail thermal equilibrium
    flux_starshot = 100e9 / 16.0  # 6.25 GW/m^2
    t_sail_pure = laser_sail_equilibrium_temp(flux_starshot, absorption=1e-5, emissivity=0.5)
    check("sail_temp_pure_dielectric_survives", 900 < t_sail_pure < 1100, f"T = {t_sail_pure:.1f} K")
    t_sail_impure = laser_sail_equilibrium_temp(flux_starshot, absorption=1e-4, emissivity=0.5)
    check("sail_temp_impure_sublimates", t_sail_impure > 1800, f"T = {t_sail_impure:.1f} K")

    # 6. Antimatter pion exhaust velocity & radiator mass
    ve_antimatter = antimatter_pion_exhaust_velocity(mean_cos_theta=0.85)
    check("antimatter_ve_approx_0.33c", math.isclose(ve_antimatter / C, 0.323, rel_tol=0.05), f"ve/c = {ve_antimatter/C:.3f}")

    p_jet, p_gamma, m_rad = antimatter_gamma_power_and_radiator_mass(
        thrust_n=10000.0,
        ve=0.33 * C,
        gamma_fraction=0.38,
        solid_angle_fraction=0.005,
        radiator_temp_k=600.0,
        radiator_areal_density_kg_m2=3.0,
        emissivity=0.9
    )
    check("antimatter_p_jet_gigawatt_scale", p_jet > 4e11, f"P_jet = {p_jet:.2e} W")
    check("antimatter_radiator_mass_hundreds_of_tonnes", m_rad > 500000.0, f"M_rad = {m_rad:.1f} kg")

    # 7. Fusion theoretical ceiling
    # D-T: Q = 17.59 MeV, reactants = 2 + 3 = 5 u, f_ch = 0.20
    ve_dt = fusion_exhaust_velocity_theoretical(17.59, 5.0, 0.20)
    check("fusion_dt_ve_approx_0.039c", math.isclose(ve_dt / C, 0.0388, rel_tol=0.02), f"ve/c = {ve_dt/C:.4f}")

    # D-He3: Q = 18.35 MeV, reactants = 2 + 3 = 5 u, f_ch = 0.968
    ve_dhe3 = fusion_exhaust_velocity_theoretical(18.35, 5.0, 0.968)
    check("fusion_dhe3_ve_approx_0.088c", math.isclose(ve_dhe3 / C, 0.0884, rel_tol=0.02), f"ve/c = {ve_dhe3/C:.4f}")

    print("\n" + "="*50)
    print(f"TOTAL: {passed} passed, {failed} failed")
    print("="*50)
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
