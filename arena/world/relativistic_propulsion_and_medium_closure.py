"""
relativistic_propulsion_and_medium_closure.py

Quantitative analysis of relativistic flight constraints:
1. Generalized Stefan-Boltzmann Radiator Law (onboard thermal/electric/fusion/antimatter)
2. Gram-scale (1 g - 1 kg) beamed-sail relativistic physics (dust impact statistics, erosion, proton TID, shield scaling)
3. Medium interaction benchmarks across velocity regimes (beta = 0.10, 0.12, 0.20, 0.50, 0.90)
4. Formal FTL Causality Obstruction & Lorentz Antitelephone metric closure.

Author: Raman (Agent A002, Generation 0)
Domain: Travel at or near light speed (lightspeed)
Date: 2026-10-02
"""

import math

# Fundamental physical constants (exact SI values)
C = 299792458.0              # Speed of light (m/s)
SIGMA_SB = 5.670374419e-8    # Stefan-Boltzmann constant (W / (m^2 K^4))
M_P = 1.67262192369e-27      # Proton rest mass (kg)
M_E = 9.1093837015e-31       # Electron rest mass (kg)
E_CHARGE = 1.602176634e-19   # Elementary charge (C)
G0 = 9.80665                 # Standard gravitational acceleration (m/s^2)
LY_TO_M = 9.4607304725808e15 # Light-year to meters (m)
AU_TO_M = 1.495978707e11     # Astronomical unit to meters (m)
YEAR_TO_S = 31557600.0       # Julian year to seconds (s)

# Interstellar Medium (ISM) canonical parameters
N_H_ISM = 1.0e6              # Hydrogen atom number density (protons/m^3 = 1 cm^-3)
RHO_ISM = N_H_ISM * M_P      # Mass density of neutral ISM (kg/m^3)
D_PROXIMA_LY = 4.2465        # Distance to Proxima Centauri in ly
D_PROXIMA_M = D_PROXIMA_LY * LY_TO_M


def lorentz_gamma(beta: float) -> float:
    """Relativistic Lorentz factor gamma = 1 / sqrt(1 - beta^2)."""
    if beta >= 1.0 or beta < 0.0:
        raise ValueError(f"Beta must be in [0, 1), got {beta}")
    return 1.0 / math.sqrt(1.0 - beta * beta)


def kinetic_energy_per_kg(beta: float) -> float:
    """Relativistic kinetic energy per kg of rest mass: (gamma - 1) * c^2."""
    g = lorentz_gamma(beta)
    return (g - 1.0) * C * C


def proton_kinetic_energy_mev(beta: float) -> float:
    """Incoming ISM proton kinetic energy in MeV in spacecraft rest frame."""
    g = lorentz_gamma(beta)
    e_joules = (g - 1.0) * M_P * C * C
    return e_joules / (E_CHARGE * 1.0e6)


# ----------------------------------------------------------------------
# 1. GENERALIZED RADIATOR-PROPULSION COUPLING LAW
# ----------------------------------------------------------------------

def radiator_power_to_thrust_thermal(ve: float, eta_conversion: float) -> float:
    """
    Specific waste heat power per unit thrust for a thermal/electric rocket:
    P_waste / F = 0.5 * ve * (1 - eta) / eta  [W / N]
    where ve is exhaust velocity (m/s) and eta is efficiency of converting
    source thermal power to directed exhaust jet kinetic power.
    """
    if eta_conversion <= 0.0 or eta_conversion >= 1.0:
        raise ValueError("eta_conversion must be in (0, 1)")
    return 0.5 * ve * (1.0 - eta_conversion) / eta_conversion


def radiator_specific_mass(t_rad_k: float, sigma_panel: float = 5.0,
                           emissivity: float = 0.90, two_sided: bool = True) -> float:
    """
    Radiator specific mass alpha_rad = M_rad / P_waste [kg / W]
    Governed by Stefan-Boltzmann radiation:
    q_rad = (2 if two_sided else 1) * emissivity * SIGMA_SB * T^4  [W/m^2]
    alpha_rad = sigma_panel / q_rad  [kg/W]
    """
    sides = 2.0 if two_sided else 1.0
    q_rad = sides * emissivity * SIGMA_SB * (t_rad_k ** 4)
    return sigma_panel / q_rad


def radiator_mass_to_thrust(p_waste_over_f: float, alpha_rad: float) -> float:
    """
    Radiator mass per unit thrust:
    M_rad / F = alpha_rad * (P_waste / F)  [kg / N]
    """
    return alpha_rad * p_waste_over_f


def max_thermal_acceleration(m_rad_over_f: float) -> float:
    """
    Maximum acceleration clamped by radiator mass (even with 0 payload/tankage):
    a_max = F / M_rad = 1 / (M_rad / F)  [m/s^2]
    """
    return 1.0 / m_rad_over_f


def antimatter_radiator_limits(f_waste: float = 0.05, w_exhaust: float = 0.36 * C,
                               t_rad_k: float = 1800.0, sigma_panel: float = 5.0,
                               emissivity: float = 0.90) -> dict:
    """
    Antimatter annihilation rocket radiator parameters:
    P_waste / F = f_waste * c^2 / w_exhaust
    """
    p_waste_over_f = f_waste * (C ** 2) / w_exhaust
    alpha_rad = radiator_specific_mass(t_rad_k, sigma_panel, emissivity)
    m_rad_over_f = radiator_mass_to_thrust(p_waste_over_f, alpha_rad)
    a_max = max_thermal_acceleration(m_rad_over_f)
    return {
        "p_waste_over_f_W_per_N": p_waste_over_f,
        "p_waste_over_f_MW_per_N": p_waste_over_f / 1.0e6,
        "alpha_rad_kg_per_W": alpha_rad,
        "m_rad_over_f_kg_per_N": m_rad_over_f,
        "a_max_m_s2": a_max,
        "a_max_g0": a_max / G0
    }


def nep_radiator_limits(ve: float = 4.90e4, eta: float = 0.35,
                         t_rad_k: float = 900.0, sigma_panel: float = 8.0,
                         emissivity: float = 0.85) -> dict:
    """
    Nuclear Electric Propulsion radiator parameters.
    """
    p_waste_over_f = radiator_power_to_thrust_thermal(ve, eta)
    alpha_rad = radiator_specific_mass(t_rad_k, sigma_panel, emissivity)
    m_rad_over_f = radiator_mass_to_thrust(p_waste_over_f, alpha_rad)
    a_max = max_thermal_acceleration(m_rad_over_f)
    return {
        "ve_m_s": ve,
        "isp_s": ve / G0,
        "p_waste_over_f_W_per_N": p_waste_over_f,
        "p_waste_over_f_kW_per_N": p_waste_over_f / 1.0e3,
        "alpha_rad_kg_per_W": alpha_rad,
        "m_rad_over_f_kg_per_N": m_rad_over_f,
        "a_max_m_s2": a_max,
        "a_max_g0": a_max / G0
    }


def fusion_radiator_limits(ve: float = 1.03e7, eta: float = 0.50,
                           t_rad_k: float = 1500.0, sigma_panel: float = 5.0,
                           emissivity: float = 0.90) -> dict:
    """
    Fusion rocket (e.g. Daedalus / D-He3) radiator parameters.
    """
    p_waste_over_f = radiator_power_to_thrust_thermal(ve, eta)
    alpha_rad = radiator_specific_mass(t_rad_k, sigma_panel, emissivity)
    m_rad_over_f = radiator_mass_to_thrust(p_waste_over_f, alpha_rad)
    a_max = max_thermal_acceleration(m_rad_over_f)
    return {
        "ve_m_s": ve,
        "ve_over_c": ve / C,
        "p_waste_over_f_W_per_N": p_waste_over_f,
        "p_waste_over_f_MW_per_N": p_waste_over_f / 1.0e6,
        "alpha_rad_kg_per_W": alpha_rad,
        "m_rad_over_f_kg_per_N": m_rad_over_f,
        "a_max_m_s2": a_max,
        "a_max_g0": a_max / G0
    }


# ----------------------------------------------------------------------
# 2. GRAM-SCALE RELATIVISTIC PROBE DYNAMICS & INTERSTELLAR FLUX
# ----------------------------------------------------------------------

def gram_scale_dust_interaction(craft_mass_g: float = 1.0, beta: float = 0.20,
                                distance_ly: float = D_PROXIMA_LY,
                                sail_areal_mass_g_m2: float = 0.10,
                                wafer_area_cm2: float = 1.0) -> dict:
    """
    Calculate dust impact rates, kinetic energy per impact, and survival
    for a gram-scale probe with face-on sail vs edge-on sail vs wafer-only bumper.
    """
    craft_mass_kg = craft_mass_g / 1000.0
    v = beta * C
    distance_m = distance_ly * LY_TO_M
    g = lorentz_gamma(beta)

    # Sail dimensions assuming sail mass is half the total mass
    sail_mass_g = craft_mass_g * 0.5
    sail_area_m2 = (sail_mass_g / sail_areal_mass_g_m2) # e.g. 0.5 g / 0.1 g/m^2 = 5 m^2
    sail_radius_m = math.sqrt(sail_area_m2 / math.pi)
    sail_thickness_m = (sail_areal_mass_g_m2 / 1000.0) / 2500.0 # rho ~ 2.5 g/cm^3 = 2500 kg/m^3 -> 40 nm

    # Frontal areas:
    # 1. Face-on sail
    a_face_on = sail_area_m2
    # 2. Edge-on sail
    a_edge_on = 2.0 * sail_radius_m * sail_thickness_m
    # 3. Wafer payload (1 cm^2)
    a_wafer = wafer_area_cm2 * 1.0e-4

    # Dust grain densities (MRN distribution in local interstellar cloud)
    # Small grains: a >= 0.1 um, n ~ 1e-6 m^-3
    # Medium grains: a >= 1.0 um, n ~ 1e-12 m^-3
    # Large grains: a >= 10 um, n ~ 1e-17 m^-3
    n_dust_0_1_um = 1.0e-6
    n_dust_1_0_um = 1.0e-12
    n_dust_10_um = 1.0e-17

    # Grain masses and kinetic energies at beta
    # m = (4/3)*pi*r^3 * rho (rho = 2500 kg/m^3)
    def grain_mass(radius_m):
        return (4.0 / 3.0) * math.pi * (radius_m ** 3) * 2500.0

    m_0_1 = grain_mass(0.1e-6)   # ~1.05e-17 kg
    m_1_0 = grain_mass(1.0e-6)   # ~1.05e-14 kg
    m_10  = grain_mass(10.0e-6)  # ~1.05e-11 kg

    ke_0_1 = (g - 1.0) * m_0_1 * C * C
    ke_1_0 = (g - 1.0) * m_1_0 * C * C
    ke_10  = (g - 1.0) * m_10 * C * C

    vol_face_on = a_face_on * distance_m
    vol_wafer = a_wafer * distance_m

    hits_face_on_0_1 = vol_face_on * n_dust_0_1_um
    hits_wafer_0_1 = vol_wafer * n_dust_0_1_um
    hits_wafer_1_0 = vol_wafer * n_dust_1_0_um
    hits_wafer_10 = vol_wafer * n_dust_10_um

    return {
        "sail_area_m2": sail_area_m2,
        "sail_thickness_nm": sail_thickness_m * 1.0e9,
        "a_face_on_m2": a_face_on,
        "a_wafer_m2": a_wafer,
        "ke_0_1_um_J": ke_0_1,
        "ke_1_0_um_J": ke_1_0,
        "ke_10_um_J": ke_10,
        "hits_face_on_0_1_um": hits_face_on_0_1,
        "total_energy_face_on_0_1_um_J": hits_face_on_0_1 * ke_0_1,
        "hits_wafer_0_1_um": hits_wafer_0_1,
        "hits_wafer_1_0_um": hits_wafer_1_0,
        "hits_wafer_10_um": hits_wafer_10,
        "prob_hit_10_um_wafer": 1.0 - math.exp(-hits_wafer_10)
    }


def gram_scale_proton_radiation_dose(beta: float = 0.20, distance_ly: float = D_PROXIMA_LY,
                                     wafer_area_cm2: float = 1.0,
                                     wafer_mass_g: float = 0.5) -> dict:
    """
    Calculate ISM proton fluence, unshielded Total Ionizing Dose (TID),
    and required forward bumper shield mass for a 1 g-class wafer probe.
    """
    v = beta * C
    distance_m = distance_ly * LY_TO_M
    g = lorentz_gamma(beta)
    e_p_mev = proton_kinetic_energy_mev(beta)

    # Fluence: F = n_H * L (protons/m^2)
    fluence_p_m2 = N_H_ISM * distance_m
    fluence_p_cm2 = fluence_p_m2 * 1.0e-4

    # Stopping power in silicon (Bethe-Bloch approximation around 19 MeV)
    # dE/rho dx ~ 20.5 MeV cm^2 / g = 3.28e-10 J m^2 / kg
    # For general MeV: dE/dx scales roughly as 1 / beta^2 (non-relativistic)
    # At beta = 0.20 (19.35 MeV): ~ 20.5 MeV cm^2 / g
    dedx_mev_cm2_g = 20.5 * (0.20 / beta) ** 1.7 # empirical Bethe-Bloch scaling
    dedx_j_m2_kg = dedx_mev_cm2_g * (E_CHARGE * 1.0e6) * 10.0

    # Unshielded Dose = Fluence * (dE / rho dx) [J / kg = Gray]
    unshielded_dose_gray = fluence_p_m2 * dedx_j_m2_kg
    unshielded_dose_rad = unshielded_dose_gray * 100.0

    # Shield mass calculation:
    # Bragg peak range of 19.35 MeV proton in beryllium: ~0.45 g/cm^2
    # In carbon/diamond: ~0.46 g/cm^2
    # Range scales roughly with E_p^1.75
    areal_density_shield_g_cm2 = 0.46 * (e_p_mev / 19.35) ** 1.75
    shield_mass_g = areal_density_shield_g_cm2 * wafer_area_cm2
    shield_thickness_beryllium_mm = (areal_density_shield_g_cm2 / 1.85) * 10.0 # rho_Be = 1.85 g/cm^3
    shield_thickness_diamond_mm = (areal_density_shield_g_cm2 / 3.52) * 10.0   # rho_C = 3.52 g/cm^3

    return {
        "beta": beta,
        "e_p_mev": e_p_mev,
        "fluence_p_cm2": fluence_p_cm2,
        "unshielded_dose_gray": unshielded_dose_gray,
        "unshielded_dose_rad": unshielded_dose_rad,
        "areal_density_shield_g_cm2": areal_density_shield_g_cm2,
        "shield_mass_g": shield_mass_g,
        "shield_thickness_beryllium_mm": shield_thickness_beryllium_mm,
        "shield_thickness_diamond_mm": shield_thickness_diamond_mm,
        "shield_mass_fraction": shield_mass_g / (shield_mass_g + wafer_mass_g)
    }


# ----------------------------------------------------------------------
# 3. INTERSTELLAR MEDIUM BENCHMARKS (beta = 0.10, 0.12, 0.20, 0.50, 0.90)
# ----------------------------------------------------------------------

def medium_interaction_benchmark(beta: float) -> dict:
    """
    Calculate all physical interaction metrics with ISM at velocity beta:
    - Proton kinetic energy (MeV)
    - Particle flux J (protons / (m^2 s))
    - Thermal power flux (W / m^2)
    - Momentum drag per unit area (N / m^2)
    - Penetration Bragg range in graphite (g/cm^2 and mm)
    - Surface atomic sputtering rate (m/s)
    - Erosion depth over 4.2465 ly (microns)
    """
    v = beta * C
    g = lorentz_gamma(beta)
    e_p_j = (g - 1.0) * M_P * C * C
    e_p_mev = e_p_j / (E_CHARGE * 1.0e6)

    # Flux
    flux_j = N_H_ISM * v # protons / (m^2 s)
    thermal_power_flux_w_m2 = flux_j * e_p_j

    # Relativistic momentum per proton: p = gamma * m_p * v
    # Drag force per unit area if completely stopped: F/A = J * p
    p_proton = g * M_P * v
    drag_force_per_m2 = flux_j * p_proton

    # Bragg penetration range in graphite (rho = 2.26 g/cm^3)
    # Using Bethe-Bloch integral parametrization:
    # R_areal ~ 0.050 g/cm^2 at 4.73 MeV (beta=0.10)
    # R_areal ~ 0.095 g/cm^2 at 6.85 MeV (beta=0.12)
    # R_areal ~ 0.460 g/cm^2 at 19.35 MeV (beta=0.20)
    # R_areal ~ 10.4 g/cm^2 at 145 MeV (beta=0.50)
    # R_areal ~ 321.0 g/cm^2 at 1.215 GeV (beta=0.90)
    # Semi-empirical fit:
    if e_p_mev < 100.0:
        r_areal_g_cm2 = 0.0042 * (e_p_mev ** 1.58)
    else:
        r_areal_g_cm2 = 0.155 * (e_p_mev ** 1.07)

    rho_graphite = 2.26 # g/cm^3
    range_mm = (r_areal_g_cm2 / rho_graphite) * 10.0

    # Sputtering yield Y (atoms / proton)
    # Maximum around a few keV, drops at high relativistic energies ~ 0.015 - 0.001
    sputtering_yield = max(0.001, 0.020 / (1.0 + (beta / 0.10) ** 2))
    # Atomic density of carbon: ~ 1.13e29 atoms/m^3
    n_carbon = 1.13e29
    erosion_rate_m_s = (flux_j * sputtering_yield) / n_carbon
    transit_time_s = D_PROXIMA_M / v
    erosion_depth_um = (erosion_rate_m_s * transit_time_s) * 1.0e6

    return {
        "beta": beta,
        "gamma": g,
        "proton_ke_mev": e_p_mev,
        "proton_flux_m2_s": flux_j,
        "thermal_flux_w_m2": thermal_power_flux_w_m2,
        "momentum_drag_n_m2": drag_force_per_m2,
        "bragg_range_g_cm2": r_areal_g_cm2,
        "bragg_range_graphite_mm": range_mm,
        "erosion_depth_4_2_ly_um": erosion_depth_um,
        "transit_time_yr": transit_time_s / YEAR_TO_S
    }


# ----------------------------------------------------------------------
# 4. FTL CAUSALITY OBSTRUCTION & LORENTZ ANTITELEPHONE CLOSURE
# ----------------------------------------------------------------------

def antitelephone_boost_condition(ftl_speed_u_over_c: float) -> float:
    """
    For a signal propagating at FTL speed U > c in frame S,
    find the minimum subluminal boost velocity v_boost / c such that
    the signal travels backward in coordinate time (dt' < 0) in frame S':
    dt' = gamma * dt * (1 - v * U / c^2)
    Condition dt' < 0 requires: v * U / c^2 > 1  =>  v / c > c / U.
    """
    if ftl_speed_u_over_c <= 1.0:
        raise ValueError(f"U must be > c, got {ftl_speed_u_over_c}c")
    return 1.0 / ftl_speed_u_over_c


def antitelephone_closed_loop_return_boost(ftl_speed_u_over_c: float) -> float:
    """
    For a two-way FTL exchange between two observers in relative motion v,
    where both use symmetric FTL communication at speed U relative to their own frames,
    the total round-trip time delta t_total in the emitter frame is:
    delta t_total = (2 * L / U) * [1 - (v / c) * (U / c)] / [1 - (v / c)^2]
    Wait, for round-trip return to arrive strictly before departure:
    v_boost > 2 * c^2 * U / (U^2 + c^2).
    """
    u = ftl_speed_u_over_c
    return (2.0 * u) / (u * u + 1.0)


def antitelephone_event_coordinates(x_target_ly: float, ftl_speed_u_over_c: float,
                                     v_boost_over_c: float) -> dict:
    """
    Explicit Lorentz transform showing negative time arrival:
    Event 0 (Emit): (t0 = 0, x0 = 0)
    Event 1 (Receive): (t1 = x_target / U, x1 = x_target)
    Boosted observer moving at +v:
    t1' = gamma * (t1 - v * x1 / c^2) = gamma * x_target * (1/U - v/c^2)
    """
    u = ftl_speed_u_over_c * C
    v = v_boost_over_c * C
    x1 = x_target_ly * LY_TO_M
    t1 = x1 / u

    g = lorentz_gamma(v_boost_over_c)
    t1_prime = g * (t1 - (v / (C * C)) * x1)
    x1_prime = g * (x1 - v * t1)

    return {
        "x_target_ly": x_target_ly,
        "u_over_c": ftl_speed_u_over_c,
        "v_over_c": v_boost_over_c,
        "t1_emitter_yr": t1 / YEAR_TO_S,
        "t1_boosted_yr": t1_prime / YEAR_TO_S,
        "dt_negative": t1_prime < 0.0,
        "invariant_interval_s2": (C * t1) ** 2 - x1 ** 2  # Spacelike: s^2 < 0
    }
