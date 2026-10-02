#!/usr/bin/env python3
"""
relativistic_flight_frontiers.py
================================
Quantitative Engine for Relativistic Interstellar Flight:
1. Relativistic Ackeret-Stefan-Boltzmann Engine Limits (Radiator Paradox)
2. Interstellar Dust Mechanics & The Failure of Active Electromagnetic Deflection
3. Sacrificial Hydrodynamic Ablation & Sail Furling Constraints
4. Exact 1g Proper-Time Trajectories & Forward CMB Radiative Flash
5. Mathematical Formulations of the FTL Causality Obstruction & Chronology Protection

Author: Raman (Agent A002, Generation 0)
Domain: Travel at or near light speed (lightspeed)
Epistemic Class: Engineering Feasibility & Relativistic Astrophysics
"""

import math
from typing import Dict, Any, List, Tuple

# ============================================================================
# FUNDAMENTAL PHYSICAL CONSTANTS (CODATA 2018 / SI Units)
# ============================================================================
C = 299792458.0                    # Speed of light in vacuum (m/s, exact)
G0 = 9.80665                       # Standard acceleration of gravity (m/s^2, exact)
YEAR = 365.25 * 86400.0            # Julian year in seconds (s)
LY = C * YEAR                      # Light-year in meters (m)
PC = 3.085677581491367e16          # Parsec in meters (m)
SIGMA_SB = 5.670374419e-8          # Stefan-Boltzmann constant (W/(m^2 K^4))
K_B = 1.380649e-23                 # Boltzmann constant (J/K)
H_PLANCK = 6.62607015e-34          # Planck constant (J s)
HBAR = H_PLANCK / (2.0 * math.pi)  # Reduced Planck constant (J s)
EPS_0 = 8.8541878128e-12           # Vacuum permittivity (F/m)
Q_E = 1.602176634e-19              # Elementary charge (C)
M_P = 1.67262192369e-27            # Proton mass (kg)
M_E = 9.1093837015e-31             # Electron mass (kg)
T_CMB = 2.7255                     # Cosmic Microwave Background temperature (K)
U_CMB = (4.0 * SIGMA_SB / C) * (T_CMB**4) # CMB energy density in rest frame (J/m^3)


# ============================================================================
# 1. RELATIVISTIC ACKERET-STEFAN-BOLTZMANN ROCKET DYNAMICS
# ============================================================================

def ackeret_mass_ratio(beta: float, w_exhaust: float) -> float:
    """
    Computes the exact relativistic mass ratio (m0 / mf) using Ackeret's formula.
    m0 / mf = ((1 + beta) / (1 - beta))^(c / (2 * w))
    """
    if beta <= 0.0 or beta >= 1.0:
        raise ValueError(f"Beta must be in (0, 1), got {beta}")
    if w_exhaust <= 0.0 or w_exhaust > C:
        raise ValueError(f"Exhaust velocity w must be in (0, c], got {w_exhaust}")
    
    ratio = (1.0 + beta) / (1.0 - beta)
    exponent = C / (2.0 * w_exhaust)
    return math.pow(ratio, exponent)

def radiator_specific_mass(t_rad: float, eps_rad: float = 0.90, sigma_panel: float = 5.0) -> float:
    """
    Computes radiator specific mass alpha_rad = M_rad / P_waste [kg/W].
    Assumes two-sided radiation: P_rad = 2 * eps * sigma_SB * T^4 * A.
    alpha_rad = sigma_panel / (2 * eps * sigma_SB * T^4).
    """
    if t_rad <= 0.0:
        raise ValueError("Radiator temperature must be positive.")
    flux_two_sided = 2.0 * eps_rad * SIGMA_SB * (t_rad**4)
    return sigma_panel / flux_two_sided

def antimatter_engine_limits(
    f_waste: float = 0.05,
    w_eff: float = 0.60 * C,
    t_rad: float = 1800.0,
    eps_rad: float = 0.90,
    sigma_panel: float = 5.0
) -> Dict[str, float]:
    """
    Evaluates the thermal radiator limits for an onboard matter-antimatter rocket.
    In p-pbar annihilation:
    - 33% neutral pions -> 2 gamma (200 MeV unreflectable gamma rays)
    - 67% charged pions -> magnetic nozzle collimation (w_eff ~ 0.6c)
    f_waste: fraction of total reaction power converted to waste heat in spacecraft structure.
    Returns:
    - p_waste_per_newton (W/N)
    - alpha_rad (kg/W)
    - m_rad_per_newton (kg/N)
    - max_acceleration (m/s^2 and g0)
    - time_to_0_2c (years)
    - distance_to_0_2c (light-years)
    """
    # Charged pions carry ~60% of mass; collimated at w_eff:
    # Thrust F = 0.6 * m_dot * w_eff
    # Total reaction power: P_rxn = m_dot * c^2
    # Waste heat: P_waste = f_waste * P_rxn = f_waste * m_dot * c^2
    # P_waste / F = (f_waste * c^2) / (0.6 * w_eff)
    p_waste_per_newton = (f_waste * (C**2)) / (0.6 * w_eff)
    
    alpha = radiator_specific_mass(t_rad, eps_rad, sigma_panel)
    m_rad_per_newton = alpha * p_waste_per_newton
    
    # Maximum acceleration if craft were 100% radiator mass:
    a_max = 1.0 / m_rad_per_newton
    a_max_g0 = a_max / G0
    
    # Kinematics to reach beta = 0.20 at constant acceleration a_max:
    v_target = 0.20 * C
    # Relativistic time to reach beta: tau = (c / a) * atanh(beta)
    tau_accel = (C / a_max) * math.atanh(0.20)
    t_coord_accel = (C / a_max) * (0.20 / math.sqrt(1.0 - 0.20**2))
    # Distance: d = (c^2 / a) * (gamma - 1)
    gamma_02 = 1.0 / math.sqrt(1.0 - 0.20**2)
    d_accel = (C**2 / a_max) * (gamma_02 - 1.0)
    
    return {
        "p_waste_per_newton_W_N": p_waste_per_newton,
        "alpha_rad_kg_W": alpha,
        "m_rad_per_newton_kg_N": m_rad_per_newton,
        "a_max_m_s2": a_max,
        "a_max_g0": a_max_g0,
        "tau_accel_years": tau_accel / YEAR,
        "t_coord_accel_years": t_coord_accel / YEAR,
        "d_accel_ly": d_accel / LY
    }


# ============================================================================
# 2. INTERSTELLAR DUST DYNAMICS & FAILURE OF ACTIVE DEFLECTION
# ============================================================================

def dust_charge_to_mass(
    radius_m: float,
    u_potential_v: float = 3.0,
    rho_grain: float = 2500.0
) -> float:
    """
    Computes equilibrium charge-to-mass ratio (q/m) for a spherical dust grain:
    q = 4 * pi * eps_0 * a * U
    m = (4/3) * pi * rho * a^3
    q / m = 3 * eps_0 * U / (rho * a^2)
    """
    return (3.0 * EPS_0 * u_potential_v) / (rho_grain * (radius_m**2))

def dust_field_emission_charge_to_mass(
    radius_m: float,
    e_crit_v_m: float = 1.0e9,
    rho_grain: float = 2500.0
) -> float:
    """
    Computes theoretical maximum charge-to-mass ratio bounded by field ion emission:
    E_surf = U / a = E_crit
    q_max = 4 * pi * eps_0 * a^2 * E_crit
    q_max / m = 3 * eps_0 * E_crit / (rho * a)
    """
    return (3.0 * EPS_0 * e_crit_v_m) / (rho_grain * radius_m)

def dust_magnetic_gyroradius(
    radius_m: float,
    beta: float,
    b_field_tesla: float = 5.0,
    u_potential_v: float = 3.0,
    rho_grain: float = 2500.0,
    use_field_emission_limit: bool = False,
    e_crit_v_m: float = 1.0e9
) -> float:
    """
    Computes relativistic gyroradius r_g = (gamma * m * v) / (q * B) = (gamma * v) / ((q/m) * B).
    """
    gamma = 1.0 / math.sqrt(1.0 - beta**2)
    v = beta * C
    if use_field_emission_limit:
        qm = dust_field_emission_charge_to_mass(radius_m, e_crit_v_m, rho_grain)
    else:
        qm = dust_charge_to_mass(radius_m, u_potential_v, rho_grain)
    return (gamma * v) / (qm * b_field_tesla)

def dust_lateral_deflection(
    radius_m: float,
    beta: float,
    l_field_m: float = 10.0,
    b_field_tesla: float = 5.0,
    u_potential_v: float = 3.0,
    rho_grain: float = 2500.0,
    use_field_emission_limit: bool = False,
    e_crit_v_m: float = 1.0e9
) -> float:
    """
    Computes lateral displacement Delta y of a dust grain passing through field of length L:
    Delta y = (q * B * L^2) / (2 * gamma * m * v) = ((q/m) * B * L^2) / (2 * gamma * v).
    """
    gamma = 1.0 / math.sqrt(1.0 - beta**2)
    v = beta * C
    if use_field_emission_limit:
        qm = dust_field_emission_charge_to_mass(radius_m, e_crit_v_m, rho_grain)
    else:
        qm = dust_charge_to_mass(radius_m, u_potential_v, rho_grain)
    return (qm * b_field_tesla * (l_field_m**2)) / (2.0 * gamma * v)


# ============================================================================
# 3. SACRIFICIAL SHIELDING, ABLATION & SAIL FURLING
# ============================================================================

# Target material properties: density (kg/m^3), volumetric vaporization/sublimation enthalpy H_v (J/m^3)
SHIELD_MATERIALS = {
    "Graphite": {
        "rho": 2260.0,
        "Q_subl": 5.96e7,
        "H_v": 2260.0 * 5.96e7 # 1.347e11 J/m^3
    },
    "Beryllium": {
        "rho": 1850.0,
        "Q_vap": 3.24e7,
        "H_v": 1850.0 * 3.24e7 # 5.994e10 J/m^3
    },
    "Silicon Carbide": {
        "rho": 3210.0,
        "Q_subl": 3.10e7,
        "H_v": 3210.0 * 3.10e7 # 9.951e10 J/m^3
    },
    "Tungsten": {
        "rho": 19300.0,
        "Q_vap": 4.35e7,
        "H_v": 19300.0 * 4.35e7 # 8.396e11 J/m^3
    }
}

def cumulative_dust_ablation_thickness(
    beta: float,
    distance_m: float,
    material: str = "Graphite",
    rho_dust: float = 1.6726e-23, # 1% of gas mass in ISM
    eta_coupling: float = 0.30
) -> Dict[str, float]:
    """
    Computes total continuous ablation thickness and mass loss per unit area
    due to swept nanograin ISM dust fluence.
    E_dep = rho_dust * distance * (gamma - 1) * c^2
    x_abl = eta_coupling * E_dep / H_v
    """
    mat = SHIELD_MATERIALS[material]
    gamma = 1.0 / math.sqrt(1.0 - beta**2)
    spec_ke = (gamma - 1.0) * (C**2)
    swept_dust_mass_per_m2 = rho_dust * distance_m
    deposited_energy_per_m2 = swept_dust_mass_per_m2 * spec_ke
    
    x_ablation = (eta_coupling * deposited_energy_per_m2) / mat["H_v"]
    mass_ablation_per_m2 = x_ablation * mat["rho"]
    
    return {
        "swept_dust_mass_kg_m2": swept_dust_mass_per_m2,
        "deposited_energy_J_m2": deposited_energy_per_m2,
        "ablation_depth_m": x_ablation,
        "ablation_depth_mm": x_ablation * 1000.0,
        "mass_lost_kg_m2": mass_ablation_per_m2
    }

def single_grain_crater_depth(
    grain_radius_m: float,
    beta: float,
    material: str = "Graphite",
    rho_grain: float = 2500.0,
    eta_coupling: float = 0.30
) -> Dict[str, float]:
    """
    Computes hemispherical explosive crater penetration depth p_c for a single relativistic grain:
    p_c = ( (3 * eta * E_k) / (2 * pi * H_v) )^(1/3)
    """
    mat = SHIELD_MATERIALS[material]
    gamma = 1.0 / math.sqrt(1.0 - beta**2)
    spec_ke = (gamma - 1.0) * (C**2)
    m_grain = (4.0 / 3.0) * math.pi * rho_grain * (grain_radius_m**3)
    e_k = m_grain * spec_ke
    
    vol_crater = (eta_coupling * e_k) / mat["H_v"]
    p_c = math.pow((3.0 * vol_crater) / (2.0 * math.pi), 1.0 / 3.0)
    
    return {
        "m_grain_kg": m_grain,
        "e_k_joules": e_k,
        "tnt_equivalent_grams": e_k / 4184.0,
        "crater_depth_m": p_c,
        "crater_depth_mm": p_c * 1000.0
    }

def sail_furling_comparison(
    beta: float = 0.20,
    distance_m: float = 4.244 * LY,
    sail_area_face_on: float = 16.0, # 4m x 4m
    chip_area_edge_on: float = 1.0e-4, # 1 cm^2
    material: str = "Graphite"
) -> Dict[str, float]:
    """
    Compares the sacrificial shield mass required for a face-on sail vs. a furled edge-on probe.
    """
    abl = cumulative_dust_ablation_thickness(beta, distance_m, material)
    mass_per_m2 = abl["mass_lost_kg_m2"]
    
    shield_mass_face_on = mass_per_m2 * sail_area_face_on
    shield_mass_edge_on = mass_per_m2 * chip_area_edge_on
    
    return {
        "mass_per_m2_kg": mass_per_m2,
        "shield_mass_face_on_kg": shield_mass_face_on,
        "shield_mass_edge_on_grams": shield_mass_edge_on * 1000.0,
        "mass_reduction_factor": shield_mass_face_on / shield_mass_edge_on
    }


# ============================================================================
# 4. EXACT 1G PROPER-TIME TRAJECTORIES & FORWARD CMB FLASH
# ============================================================================

def hyperbolic_trajectory_1g(distance_m: float, proper_accel: float = G0) -> Dict[str, float]:
    """
    Computes exact relativistic kinematic parameters for a symmetrical 1g flight:
    acceleration at a0 for d/2, followed by deceleration at a0 for d/2.
    """
    d_half = distance_m / 2.0
    # cosh(a0 * tau_half / c) = 1 + a0 * d_half / c^2
    cosh_val = 1.0 + (proper_accel * d_half) / (C**2)
    tau_half = (C / proper_accel) * math.acosh(cosh_val)
    tau_total = 2.0 * tau_half
    
    sinh_val = math.sqrt(cosh_val**2 - 1.0)
    t_half = (C / proper_accel) * sinh_val
    t_total = 2.0 * t_half
    
    gamma_peak = cosh_val
    beta_peak = sinh_val / cosh_val
    v_peak = beta_peak * C
    
    # Aberration half-angle of the forward sky: theta_half ~ 1 / gamma
    theta_half_rad = 1.0 / gamma_peak
    theta_half_arcsec = theta_half_rad * (180.0 / math.pi) * 3600.0
    
    return {
        "distance_ly": distance_m / LY,
        "tau_total_years": tau_total / YEAR,
        "t_total_years": t_total / YEAR,
        "gamma_peak": gamma_peak,
        "beta_peak": beta_peak,
        "v_peak_km_s": v_peak / 1000.0,
        "aberration_cone_rad": theta_half_rad,
        "aberration_cone_arcsec": theta_half_arcsec
    }

def cmb_forward_radiation_state(gamma: float, beta: float) -> Dict[str, float]:
    """
    Computes the transformed CMB radiation properties in the spacecraft rest frame:
    - Poynting flux vector along x: S' = (4/3) * gamma^2 * beta * c * u_CMB
    - Forward Doppler temperature: T_forward = gamma * (1 + beta) * T_CMB
    - Wien peak wavelength: lambda_peak = b_Wien / T_forward
    - Peak photon energy: E_peak = 4.965 * k_B * T_forward (in eV)
    """
    if gamma < 1.0:
        raise ValueError("Gamma must be >= 1.0")
    
    # Energy flux density hitting the front of the craft (W/m^2)
    flux_x = (4.0 / 3.0) * (gamma**2) * beta * C * U_CMB
    
    # Forward Doppler temperature
    t_forward = gamma * (1.0 + beta) * T_CMB
    
    # Wien displacement constant: b = 2.897771955e-3 m K
    b_wien = 2.897771955e-3
    lambda_peak = b_wien / t_forward
    
    # Photon peak energy: E = 4.96511423 * k_B * T
    e_peak_joules = 4.96511423 * K_B * t_forward
    e_peak_ev = e_peak_joules / Q_E
    
    return {
        "flux_W_m2": flux_x,
        "t_forward_K": t_forward,
        "lambda_peak_m": lambda_peak,
        "e_peak_eV": e_peak_ev
    }


# ============================================================================
# 5. CAUSALITY OBSTRUCTION & CHRONOLOGY PROTECTION FORMULATIONS
# ============================================================================

def tolman_antitelephone_boost_velocity(u_signal: float) -> float:
    """
    Given a hypothetical superluminal signal speed U > c in frame S:
    Finds the minimum subluminal frame boost velocity v < c such that
    the return signal arrives at the transmitter BEFORE the departure of the initial signal.
    Condition for dt' < 0: 1 - (v * U / c^2) < 0  =>  v > c^2 / U.
    Symmetric round-trip closed timelike loop condition:
    v_thresh = (2 * c^2 * U) / (U^2 + c^2).
    """
    if u_signal <= C:
        raise ValueError(f"Signal speed must be superluminal (U > c), got {u_signal}")
    return (2.0 * (C**2) * u_signal) / ((u_signal**2) + (C**2))

def cauchy_horizon_divergence_scaling(t_approach: float) -> float:
    """
    Models the scaling of the renormalized vacuum stress-energy tensor <T_mu_nu>_ren
    as a Cauchy horizon is approached (Hawking Chronology Protection Conjecture):
    <T_00> ~ hbar * c / (t_approach)^4
    t_approach: time interval before horizon crossing (s).
    """
    if t_approach <= 0.0:
        raise ValueError("t_approach must be positive.")
    return (HBAR * C) / math.pow(t_approach, 4)
