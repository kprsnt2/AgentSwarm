"""
propulsion_engineering_synthesis.py
===================================
Rigorous quantitative calculations for space propulsion physics,
relativistic rocket equations, Stuhlinger specific-power bounds,
laser sail diffraction limits, antimatter thermal-gamma radiation bounds,
fusion charged-exhaust mechanics, and staging limits.

Author: Kepler (Agent A001, Generation 0)
Domain: Practical space propulsion (propulsion)
Epistemic Class: Engineering feasibility
"""

import math

# Fundamental Physical Constants (CODATA 2022 / SI)
C = 299792458.0              # Speed of light (m/s)
G0 = 9.80665                 # Standard gravitational acceleration (m/s^2)
SIGMA_SB = 5.670374419e-8    # Stefan-Boltzmann constant (W/m^2/K^4)
AU = 149597870700.0          # Astronomical Unit (m)
YEAR = 365.25 * 86400.0      # Julian year (s)
MP = 1.67262192369e-27       # Proton mass (kg)
ME = 9.1093837015e-31        # Electron mass (kg)
QE = 1.602176634e-19         # Elementary charge (C)
PI = math.pi


def relativistic_gamma(beta: float) -> float:
    """Lorentz gamma factor."""
    if beta >= 1.0 or beta < 0.0:
        raise ValueError("Beta must be in [0, 1)")
    return 1.0 / math.sqrt(1.0 - beta**2)


def relativistic_kinetic_energy(mass_kg: float, beta: float) -> float:
    """Exact relativistic kinetic energy E_k = (gamma - 1) * m * c^2."""
    gamma = relativistic_gamma(beta)
    return (gamma - 1.0) * mass_kg * C**2


def classical_kinetic_energy(mass_kg: float, velocity_mps: float) -> float:
    """Classical kinetic energy E_k = 0.5 * m * v^2."""
    return 0.5 * mass_kg * velocity_mps**2


def classical_mass_ratio(delta_v: float, ve: float) -> float:
    """Tsiolkovsky classical rocket equation m0/mf = exp(delta_v / ve)."""
    return math.exp(delta_v / ve)


def relativistic_mass_ratio(beta: float, ve: float) -> float:
    """
    Exact relativistic rocket equation for constant exhaust velocity ve (m/s):
    R = m0 / mf = ((1 + beta) / (1 - beta))^(c / (2 * ve))
    """
    term = (1.0 + beta) / (1.0 - beta)
    exponent = C / (2.0 * ve)
    return term**exponent


def continuous_staging_mass_ratio(delta_v: float, ve: float, epsilon: float) -> float:
    """
    Theoretical minimum mass ratio with infinite staging (continuous drop of inert mass):
    R_inf = exp( delta_v / (ve * (1 - epsilon)) )
    where epsilon is the inert structural fraction m_struct / (m_struct + m_prop).
    """
    return math.exp(delta_v / (ve * (1.0 - epsilon)))


def n_stage_mass_ratio(n: int, delta_v: float, ve: float, epsilon: float) -> float:
    """
    Mass ratio m0 / m_payload for an n-stage rocket with identical stage mass ratios
    and structural fraction epsilon:
    Each stage achieves delta_v_stage = delta_v / n.
    Stage mass ratio r = exp(delta_v_stage / ve).
    Payload fraction per stage lambda = (1 - epsilon * r) / (r - 1) ...
    Overall mass ratio R = ( (1 - epsilon) / (exp(-delta_v / (n * ve)) - epsilon) )^n
    Returns infinity if delta_v_stage exceeds the single-stage limit -ve * ln(epsilon).
    """
    dv_stage = delta_v / n
    dv_max_stage = -ve * math.log(epsilon)
    if dv_stage >= dv_max_stage:
        return float('inf')
    denom = math.exp(-dv_stage / ve) - epsilon
    if denom <= 0:
        return float('inf')
    stage_ratio = (1.0 - epsilon) / denom
    return stage_ratio**n


def stuhlinger_burn_time(delta_v: float, alpha: float, mass_ratio: float = 2.0) -> float:
    """
    Ernst Stuhlinger specific power relation for continuous electric propulsion:
    alpha = P_jet / m_powerplant (W/kg).
    Minimum burn time to achieve delta_v with mass ratio R = m0 / mf:
    t_b = (delta_v^2) / (2 * alpha * (R - 1) / R)
    For R ~ 2 (typical optimal payload trade):
    t_b ~ delta_v^2 / (2 * alpha).
    """
    return (delta_v**2) / (2.0 * alpha)


def required_specific_power(delta_v: float, burn_time_s: float) -> float:
    """
    Required powerplant specific power alpha (W/kg) to provide delta_v in burn_time_s:
    alpha >= delta_v^2 / (2 * burn_time_s).
    """
    return (delta_v**2) / (2.0 * burn_time_s)


def laser_sail_diffraction_aperture(wavelength_m: float, distance_m: float, sail_diameter_m: float) -> float:
    """
    Diffraction-limited transmitter aperture diameter D_opt:
    D_opt = 2.44 * wavelength * distance / sail_diameter
    """
    return 2.44 * wavelength_m * distance_m / sail_diameter_m


def laser_sail_pointing_accuracy_rad(sail_diameter_m: float, distance_m: float) -> float:
    """Angular pointing accuracy tolerance (radians)."""
    return sail_diameter_m / (2.0 * distance_m)


def laser_sail_equilibrium_temp(flux_w_m2: float, absorption: float, emissivity: float = 0.5) -> float:
    """
    Equilibrium temperature of a laser sail:
    Absorbed flux = 2 * emissivity * sigma * T^4 (radiating from both faces).
    T = ( (absorption * flux) / (2 * emissivity * sigma) )^(1/4)
    """
    p_rad_face = (absorption * flux_w_m2) / (2.0 * emissivity * SIGMA_SB)
    return p_rad_face**0.25


def antimatter_pion_exhaust_velocity(mean_cos_theta: float = 0.85, nozzle_efficiency: float = 0.70) -> float:
    """
    Effective directed exhaust velocity of a beamed-core proton-antiproton rocket.
    Total reactant mass = 2 * m_p (1876.5 MeV/c^2).
    Charged pions (average 3.0 per annihilation, rest mass 139.6 MeV/c^2, T_k ~ 236 MeV):
    gamma_pi = 1 + 236 / 139.6 = 2.69
    p_pi = gamma_pi * m_pi * v_pi ~ 348 MeV/c.
    Total charged pion momentum = 3 * 348 = 1045 MeV/c.
    Axial momentum = 1045 * mean_cos_theta * nozzle_efficiency MeV/c.
    Effective exhaust velocity ve = P_axial / (2 * m_p):
    For mean_cos_theta = 0.85 and nozzle_efficiency = 0.70:
    ve ~ (1045 * 0.85 * 0.70 / 1876.5) * c ~ 0.331 * c.
    """
    p_total_charged_mev_c = 1045.0
    two_mp_mev_c2 = 1876.54
    ve_fraction = (p_total_charged_mev_c * mean_cos_theta * nozzle_efficiency) / two_mp_mev_c2
    return ve_fraction * C


def antimatter_gamma_power_and_radiator_mass(
    thrust_n: float,
    ve: float,
    gamma_fraction: float = 0.38,
    solid_angle_fraction: float = 0.005,
    radiator_temp_k: float = 600.0,
    radiator_areal_density_kg_m2: float = 3.0,
    emissivity: float = 0.9
) -> tuple[float, float, float]:
    """
    Computes:
    - Total jet power P_jet = 0.5 * T * ve
    - Total uncollimated gamma-ray power P_gamma = P_jet * (gamma_fraction / (1 - gamma_fraction))
    - Intercepted gamma power absorbed P_abs = P_gamma * solid_angle_fraction
    - Radiator area A_rad = P_abs / (emissivity * sigma * T^4)
    - Radiator mass M_rad = A_rad * areal_density
    """
    p_jet = 0.5 * thrust_n * ve
    p_annihil_total = p_jet / (1.0 - gamma_fraction)
    p_gamma = p_annihil_total * gamma_fraction
    p_absorbed = p_gamma * solid_angle_fraction
    flux_rejection = emissivity * SIGMA_SB * (radiator_temp_k**4)
    a_rad = p_absorbed / flux_rejection
    m_rad = a_rad * radiator_areal_density_kg_m2
    return p_jet, p_gamma, m_rad


def fusion_exhaust_velocity_theoretical(q_mev: float, mass_reactants_u: float, charged_fraction: float) -> float:
    """
    Theoretical maximum exhaust velocity for fusion reaction:
    ve = sqrt(2 * f_ch * Q / m_kg).
    """
    q_joules = q_mev * 1e6 * QE
    m_kg = mass_reactants_u * 1.66053906660e-27
    q_per_kg = q_joules / m_kg
    return math.sqrt(2.0 * charged_fraction * q_per_kg)
