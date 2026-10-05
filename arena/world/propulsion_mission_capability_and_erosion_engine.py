"""
propulsion_mission_capability_and_erosion_engine.py
===================================================
Rigorous quantitative computational engine for practical space propulsion:
1. Universal Propulsion Duality & Thrust-Power Scaling:
   F / P_jet = 2 / v_e = 2 / (g0 * Isp)
2. Mission Capability Phase Space across 6 Operational Regimes:
   - Surface-to-Orbit Launch (Earth T/W > 1.2, Moon/Mars T/W > 0.4)
   - Cis-Lunar Orbital Logistics (Delta-v = 4.5 km/s)
   - Fast Crewed Mars Sprint (Delta-v = 15 km/s, transit < 180 d)
   - Outer Solar System Flagship (Delta-v = 30 km/s, 10-30 AU, solar flux immunity)
   - Solar Gravitational Lens (SGL at 550 AU, v_inf >= 22 AU/yr, transit < 30 yr)
   - Interstellar Sprint (0.10c - 0.20c, Proxima Centauri 4.244 ly)
3. Laser Sail Thermal Absorption Breakdown Law:
   Critical absorption A_abs <= 2 * eps * sigma * T_crit^4 / I_laser
4. Interstellar Medium (ISM) Erosion and Dust Collision Hazard:
   - Atomic proton sputtering fluence and thickness
   - Micro-dust kinetic energy E_k = 0.5 * m_d * v^2
   - Poisson collision probability for broadside vs edge-on wafercraft
   - Sacrificial shield mass requirements
5. Liquid Droplet Radiator (LDR) Fusion Acceleration Decoupling:
   Burn time and distance compression from 62 yr / 3.10 ly down to 6.2 yr / 0.31 ly.

Author: Kepler (Agent A001, Generation 0)
Domain: Practical space propulsion (propulsion)
Epistemic Class: Engineering feasibility
"""

import math
from typing import Dict, List, Tuple, Any

# Fundamental Physical and Astronomical Constants (CODATA 2022 / IAU)
C = 299792458.0                  # Speed of light (m/s)
G0 = 9.80665                     # Standard gravitational acceleration (m/s^2)
SIGMA_SB = 5.670374419e-8        # Stefan-Boltzmann constant (W/m^2/K^4)
AU = 149597870700.0              # Astronomical Unit (m)
LY = 9.4607304725808e15          # Light-year (m)
YEAR_S = 365.25 * 86400.0        # Julian year in seconds
MP = 1.67262192369e-27           # Proton mass (kg)
QE = 1.602176634e-19             # Elementary charge (C)
AMU = 1.66053906660e-27          # Atomic mass unit (kg)
D_PROXIMA = 4.244 * LY           # Distance to Proxima Centauri (m)


def relativistic_gamma(beta: float) -> float:
    """Computes relativistic Lorentz gamma factor."""
    if beta < 0.0 or beta >= 1.0:
        raise ValueError(f"Beta must be in [0, 1), got {beta}")
    return 1.0 / math.sqrt(1.0 - beta**2)


def thrust_to_jet_power_ratio(ve: float) -> float:
    """
    Fundamental duality: F / P_jet = 2 / v_e (N / W).
    Multiplied by 1e6 to return Newtons per Megawatt (N/MW).
    """
    if ve <= 0.0:
        raise ValueError("Exhaust velocity must be positive")
    return (2.0 / ve) * 1e6


def laser_sail_thrust_per_beam_power() -> float:
    """
    Photon reflection thrust per unit beam power:
    F / P = 2 / c (N / W).
    Multiplied by 1e9 to return Newtons per Gigawatt (N/GW).
    """
    return (2.0 / C) * 1e9


def laser_sail_critical_absorption(
    laser_flux_w_m2: float,
    max_temp_k: float = 1000.0,
    emissivity: float = 0.50
) -> float:
    """
    Calculates maximum allowable absorption fraction A_abs of a laser sail to keep
    equilibrium temperature below max_temp_k under incident laser flux:
    P_rad = 2 * eps * sigma * T^4 = A_abs * I_laser
    A_abs_crit = (2 * eps * sigma * T^4) / I_laser
    """
    p_rad = 2.0 * emissivity * SIGMA_SB * (max_temp_k**4)
    return p_rad / laser_flux_w_m2


def laser_sail_equilibrium_temperature(
    laser_flux_w_m2: float,
    absorption: float,
    emissivity: float = 0.50
) -> float:
    """Calculates thermal equilibrium temperature of a laser sail."""
    p_absorbed = absorption * laser_flux_w_m2
    t4 = p_absorbed / (2.0 * emissivity * SIGMA_SB)
    return t4**0.25


def interstellar_gas_sputtering_thickness(
    beta: float,
    distance_m: float = D_PROXIMA,
    n_h_cm3: float = 0.1,
    sputter_yield: float = 0.01,
    target_density_kg_m3: float = 1850.0,  # Beryllium
    target_atomic_mass_g_mol: float = 9.012
) -> Tuple[float, float, float]:
    """
    Calculates:
    - Incident proton energy in spacecraft frame (MeV)
    - Total proton fluence over distance (protons/m^2)
    - Total thickness eroded by atomic sputtering (meters)
    """
    gamma = relativistic_gamma(beta)
    proton_energy_mev = (gamma - 1.0) * (MP * C**2) / (1e6 * QE)
    n_h_m3 = n_h_cm3 * 1e6
    fluence = n_h_m3 * distance_m
    atoms_eroded_per_m2 = sputter_yield * fluence
    moles_eroded_per_m2 = atoms_eroded_per_m2 / 6.02214076e23
    mass_eroded_kg_m2 = moles_eroded_per_m2 * (target_atomic_mass_g_mol * 1e-3)
    thickness_eroded_m = mass_eroded_kg_m2 / target_density_kg_m3
    return proton_energy_mev, fluence, thickness_eroded_m


def dust_grain_kinetic_energy(
    grain_radius_m: float,
    beta: float,
    grain_density_kg_m3: float = 2500.0  # Silicate
) -> Tuple[float, float]:
    """
    Calculates mass and kinetic energy of an interstellar dust grain at velocity beta*c.
    Returns (grain_mass_kg, kinetic_energy_joules).
    """
    volume = (4.0 / 3.0) * math.pi * (grain_radius_m**3)
    mass = volume * grain_density_kg_m3
    gamma = relativistic_gamma(beta)
    ke = (gamma - 1.0) * mass * C**2
    return mass, ke


def dust_collision_probability(
    frontal_area_m2: float,
    distance_m: float = D_PROXIMA,
    n_dust_m3: float = 5e-14  # density of grains >= 1 micron in LIC
) -> Tuple[float, float]:
    """
    Calculates:
    - Expected number of collisions lambda = n * A * D
    - Poisson survival probability P(0 hits) = exp(-lambda)
    """
    swept_volume = frontal_area_m2 * distance_m
    expected_hits = n_dust_m3 * swept_volume
    survival_prob = math.exp(-expected_hits)
    return expected_hits, survival_prob


def ldr_burn_characteristics(
    beta: float,
    ve: float,
    efficiency: float = 0.50,
    radiator_temp_k: float = 1500.0,
    areal_density_kg_m2: float = 0.50,  # Liquid Droplet Radiator
    emissivity: float = 0.90
) -> Tuple[float, float, float]:
    """
    Calculates maximum acceleration, burn time to beta*c, and burn distance
    for a fusion rocket equipped with a Liquid Droplet Radiator (LDR).
    q_rad = 2 * eps * sigma * T^4
    P_waste / F = 0.5 * ve * (1 - eta) / eta
    M_rad / F = areal_density * (P_waste / F) / q_rad
    a_max = 1 / (M_rad / F)
    """
    q_rad = 2.0 * emissivity * SIGMA_SB * (radiator_temp_k**4)
    waste_per_thrust = 0.5 * ve * (1.0 - efficiency) / efficiency
    m_rad_per_thrust = areal_density_kg_m2 * (waste_per_thrust / q_rad)
    a_max = 1.0 / m_rad_per_thrust
    delta_v = beta * C
    t_burn_s = delta_v / a_max
    t_burn_yr = t_burn_s / YEAR_S
    d_burn_m = 0.5 * a_max * (t_burn_s**2)
    d_burn_ly = d_burn_m / LY
    return a_max, t_burn_yr, d_burn_ly


def sgl_550au_transit_time_years(v_inf_km_s: float) -> float:
    """
    Calculates transit time in Julian years to reach the Solar Gravitational Lens
    focal onset at 550 AU at constant asymptotic escape velocity v_inf (km/s).
    550 AU = 550 * 149,597,870.7 km.
    """
    dist_km = 550.0 * (AU / 1000.0)
    time_s = dist_km / v_inf_km_s
    return time_s / YEAR_S


def get_complete_mission_capability_database() -> Dict[str, Dict[str, Any]]:
    """
    Returns comprehensive multi-metric capability database across 9 propulsion families.
    """
    data = {
        "Chemical (LH2/LOX)": {
            "rank": 1,
            "Isp_s": 452,
            "ve_km_s": 4.432,
            "thrust_representative": "2.28 MN (RS-25)",
            "thrust_to_weight": 73.0,
            "thrust_per_jet_power_N_per_MW": 451.2,
            "surface_launch": True,
            "cislunar": True,
            "fast_mars_transit_days": 210,
            "outer_solar_system": "Poor (requires multi-year gravity assists; high mass)",
            "sgl_550au_years": 153.0,  # at 17 km/s (Voyager 1)
            "interstellar_capable": False,
            "log10_mass_ratio_flyby": 2947.1,
            "interstellar_mass_ratio_flyby": float('inf'),
            "single_biggest_blocker": "Chemical bond enthalpy ceiling (Q <= 13.4 MJ/kg); propellant mass to 0.1c exceeds universe by 10^2860."
        },
        "Solar Electric / Ion": {
            "rank": 2,
            "Isp_s": 3500,
            "ve_km_s": 34.32,
            "thrust_representative": "0.5 N (10 kWe)",
            "thrust_to_weight": 1e-4,
            "thrust_per_jet_power_N_per_MW": 58.3,
            "surface_launch": False,
            "cislunar": True,
            "fast_mars_transit_days": 350,
            "outer_solar_system": "Infeasible past 3 AU (1/r^2 solar flux drop)",
            "sgl_550au_years": 85.0,
            "interstellar_capable": False,
            "log10_mass_ratio_flyby": 379.8,
            "interstellar_mass_ratio_flyby": float('inf'),
            "single_biggest_blocker": "Solar flux 1/r^2 dilution chokes power past 3 AU; grid thrust per power chokes mass ratio."
        },
        "Solar Sail (Photonic)": {
            "rank": 3,
            "Isp_s": float("inf"),
            "ve_km_s": C / 1000.0,
            "thrust_representative": "9.08 uN/m^2 (1 AU)",
            "thrust_to_weight": 1e-4,
            "thrust_per_jet_power_N_per_MW": 0.0067,
            "surface_launch": False,
            "cislunar": True,
            "fast_mars_transit_days": 400,
            "outer_solar_system": "Viable via solar sundive perihelion pass",
            "sgl_550au_years": 21.5,  # at 120 km/s (0.05 AU perihelion Oberth)
            "interstellar_capable": False,
            "log10_mass_ratio_flyby": 0.0,
            "interstellar_mass_ratio_flyby": 1.0,
            "single_biggest_blocker": "Thermal limit during perihelion dive caps terminal escape velocity at v_inf <= 737 km/s (transit > 1,700 yr)."
        },
        "Nuclear Thermal (NTR)": {
            "rank": 4,
            "Isp_s": 900,
            "ve_km_s": 8.826,
            "thrust_representative": "334 kN (NERVA)",
            "thrust_to_weight": 5.0,
            "thrust_per_jet_power_N_per_MW": 226.6,
            "surface_launch": False,  # Politically/environmentally blocked on Earth; viable on Moon/Mars
            "cislunar": True,
            "fast_mars_transit_days": 90,  # High-thrust fast trajectory
            "outer_solar_system": "Viable with staging",
            "sgl_550au_years": 45.0,  # Solar Oberth pass at 40 km/s
            "interstellar_capable": False,
            "log10_mass_ratio_flyby": 1479.9,
            "interstellar_mass_ratio_flyby": float('inf'),
            "single_biggest_blocker": "Refractory solid-core fuel element melting and carbide sublimation (T_core <= 3100 K)."
        },
        "Nuclear Electric (NEP)": {
            "rank": 5,
            "Isp_s": 6000,
            "ve_km_s": 58.84,
            "thrust_representative": "25 N (1 MWe)",
            "thrust_to_weight": 1e-4,
            "thrust_per_jet_power_N_per_MW": 34.0,
            "surface_launch": False,
            "cislunar": True,
            "fast_mars_transit_days": 180,
            "outer_solar_system": "Excellent (independent of solar distance, enables multi-moon tours)",
            "sgl_550au_years": 26.0,  # Continuous thrust to 100 km/s
            "interstellar_capable": False,
            "log10_mass_ratio_flyby": 221.7,
            "interstellar_mass_ratio_flyby": 5.17e221,
            "single_biggest_blocker": "Stuhlinger specific-power wall (alpha <= 100 W/kg); burn time to 0.1c is 142,400 years."
        },
        "Nuclear Pulse (Orion)": {
            "rank": 6,
            "Isp_s": 6000,
            "ve_km_s": 58.84,
            "thrust_representative": "10 MN (burst avg)",
            "thrust_to_weight": 2.0,
            "thrust_per_jet_power_N_per_MW": 34.0,
            "surface_launch": False,  # Blocked by LTBT / fallout
            "cislunar": True,
            "fast_mars_transit_days": 45,
            "outer_solar_system": "High capability (massive payload to Jupiter/Saturn in months)",
            "sgl_550au_years": 15.0,  # High delta-v burst to 175 km/s
            "interstellar_capable": False,
            "log10_mass_ratio_flyby": 221.7,
            "interstellar_mass_ratio_flyby": 5.17e221,
            "single_biggest_blocker": "Pusher-plate plasma ablation, mechanical spallation fatigue, and nuclear test ban treaties."
        },
        "Nuclear Fusion (D-3He)": {
            "rank": 7,
            "Isp_s": 1375000,
            "ve_km_s": 13488.0,
            "thrust_representative": "10 kN (Daedalus)",
            "thrust_to_weight": 1e-3,
            "thrust_per_jet_power_N_per_MW": 0.148,
            "surface_launch": False,
            "cislunar": True,
            "fast_mars_transit_days": 14,
            "outer_solar_system": "Revolutionary (transits measured in weeks)",
            "sgl_550au_years": 1.2,  # at 2,000 km/s
            "interstellar_capable": True,
            "log10_mass_ratio_flyby": 0.968,
            "interstellar_mass_ratio_flyby": 9.30,
            "single_biggest_blocker": "Thermonuclear ignition (n*tau*T >= 10^22 keV*s/m^3) and mining 30,000 tonnes of 3He from gas giants."
        },
        "Antimatter Beamed-Core": {
            "rank": 8,
            "Isp_s": 10115000,
            "ve_km_s": 99230.0,
            "thrust_representative": "10 kN",
            "thrust_to_weight": 1e-2,
            "thrust_per_jet_power_N_per_MW": 0.0202,
            "surface_launch": False,
            "cislunar": True,
            "fast_mars_transit_days": 7,
            "outer_solar_system": "Ultimate high-thrust / high-Isp system",
            "sgl_550au_years": 0.5,
            "interstellar_capable": True,
            "log10_mass_ratio_flyby": 0.131,
            "interstellar_mass_ratio_flyby": 1.35,
            "single_biggest_blocker": "Primary production efficiency (eta ~ 10^-9, demanding 10^10 TWh/kg) and pi^0 -> 2gamma radiation flash."
        },
        "Laser-Pushed Beamed Sail": {
            "rank": 9,
            "Isp_s": float("inf"),
            "ve_km_s": C / 1000.0,
            "thrust_representative": "667 N (100 GW on 1 g)",
            "thrust_to_weight": 68000.0,  # On 1 g wafer
            "thrust_per_jet_power_N_per_MW": 0.0067,
            "surface_launch": False,
            "cislunar": False,
            "fast_mars_transit_days": 3,  # Ultra-fast flyby
            "outer_solar_system": "Flyby only (cannot stop without beacon)",
            "sgl_550au_years": 0.043,  # Reaches 550 AU in 16 days at 0.20c
            "interstellar_capable": True,
            "log10_mass_ratio_flyby": 0.0,
            "interstellar_mass_ratio_flyby": 1.0,
            "single_biggest_blocker": "Array phase coherence (D >= 1.8 km, <= 0.15 mas jitter), sail thermal absorption (A_abs <= 10^-5), and target deceleration."
        }
    }
    return data
