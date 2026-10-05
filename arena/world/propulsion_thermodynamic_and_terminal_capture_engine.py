"""
propulsion_thermodynamic_and_terminal_capture_engine.py
======================================================
Unified engineering model for:
1. Froude kinetic propulsive efficiency horizons and mission-averaged scaling.
2. Thermodynamic Stefan-Boltzmann waste-heat dissipation and radiator mass limits.
3. Antimatter beamed-core neutral pion gamma ray volumetric heating and shielding penalty.
4. Macro-pellet beam vs laser photon propulsion: thrust-to-power and cryogenic divergence.
5. Astrospheric deceleration cutoff, aerocapture vaporization boundary, and terminal orbital insertion.
6. Complete ranked practical propulsion feasibility matrix across all 10 archetypes.

Author: Kepler (Agent A001, Generation 0)
Epistemic Class: Engineering Feasibility & Thermodynamic Closure
Domain: Practical Space Propulsion
"""

import math

# Fundamental Physical Constants (CODATA / IAU / NIST)
C = 299792458.0                 # Speed of light in vacuum (m/s)
G0 = 9.80665                    # Standard Earth gravitational acceleration (m/s^2)
SIGMA_SB = 5.670374419e-8       # Stefan-Boltzmann constant (W / (m^2 K^4))
K_B = 1.380649e-23              # Boltzmann constant (J/K)
G_CONST = 6.67430e-11           # Gravitational constant (m^3 / (kg s^2))
AU = 1.495978707e11             # Astronomical Unit (m)
LY = 9.460730472e15             # Light Year (m)
YEAR = 31557600.0               # Julian year in seconds
M_PROXIMA = 0.122 * 1.98847e30  # Proxima Centauri mass (kg)
A_PROXIMA_B = 0.0485 * AU       # Proxima Centauri b semi-major axis (m)


def froude_instantaneous_efficiency(v_craft, v_exhaust):
    """
    Computes instantaneous Froude kinetic propulsive efficiency:
    eta_p = 2 * (v / v_e) / (1 + (v / v_e)^2)
    """
    if v_exhaust <= 0:
        raise ValueError("Exhaust velocity must be strictly positive.")
    u = v_craft / v_exhaust
    return (2.0 * u) / (1.0 + u**2)


def froude_mission_averaged_efficiency(mass_ratio):
    """
    Computes mission-averaged kinetic propulsive efficiency for a rocket accelerating
    from rest to v_f = v_e * ln(mass_ratio):
    eta_mission = E_k_payload / E_k_propellant_exhaust
                = (ln R)^2 / (R - 1)
    """
    if mass_ratio <= 1.0:
        return 0.0
    ln_r = math.log(mass_ratio)
    return (ln_r**2) / (mass_ratio - 1.0)


def optimal_froude_mass_ratio():
    """
    Computes the mass ratio R that maximizes mission-averaged kinetic efficiency.
    Satisfies ln(R) = 2 * (1 - 1/R).
    Numerically solves to high precision.
    """
    # Root finding for f(R) = ln(R) - 2 * (1 - 1/R) = 0
    # Expected root ~ 4.9215536
    r = 4.92
    for _ in range(20):
        f = math.log(r) - 2.0 * (1.0 - 1.0 / r)
        df = (1.0 / r) - (2.0 / (r**2))
        r_next = r - f / df
        if abs(r_next - r) < 1e-12:
            break
        r = r_next
    max_eta = froude_mission_averaged_efficiency(r)
    u_optimal = math.log(r)  # v_f / v_e
    return {
        "optimal_mass_ratio": r,
        "optimal_velocity_ratio": u_optimal,
        "max_kinetic_efficiency": max_eta
    }


def thermodynamic_radiator_limit(thrust_n, v_exhaust, eta_engine=0.80, t_rad=1000.0, emissivity=0.85, areal_density=5.0):
    """
    Computes radiator area, radiator mass, and effective thrust-to-radiator-weight ratio.
    Jet power: P_jet = 0.5 * F * v_e
    Waste heat: P_waste = P_jet * (1 - eta_e) / eta_e
    Radiative heat flux (double-sided): q_rad = 2 * epsilon * sigma * T_rad^4
    Radiator area: A_rad = P_waste / q_rad
    Radiator mass: M_rad = areal_density * A_rad
    Thrust-to-weight (in g0): T_W = F / (M_rad * g0)
    """
    p_jet = 0.5 * thrust_n * v_exhaust
    waste_fraction = (1.0 - eta_engine) / eta_engine
    p_waste = p_jet * waste_fraction
    
    q_rad_unit = 2.0 * emissivity * SIGMA_SB * (t_rad**4)  # W/m^2 (two-sided flat panel)
    a_rad = p_waste / q_rad_unit
    m_rad = areal_density * a_rad
    
    thrust_to_mass = thrust_n / m_rad if m_rad > 0 else 0.0
    thrust_to_weight_g = thrust_to_mass / G0
    
    return {
        "jet_power_w": p_jet,
        "waste_heat_w": p_waste,
        "radiator_flux_w_m2": q_rad_unit,
        "radiator_area_m2": a_rad,
        "radiator_mass_kg": m_rad,
        "thrust_to_mass_n_kg": thrust_to_mass,
        "thrust_to_weight_g": thrust_to_weight_g
    }


def antimatter_gamma_shielding_analysis(thrust_n, v_exhaust=0.331 * C, gamma_fraction=0.33, solid_angle_fraction=0.02, t_shield=1500.0, emissivity=0.90, shield_thickness_m=0.10, shield_density=19300.0):
    """
    Computes the gamma ray volumetric heating and shielding mass for an antimatter beamed-core rocket.
    Neutral pions decay into 67.5 MeV gammas carrying ~33% of total annihilation power.
    Charged pions provide thrust: P_jet = 0.5 * F * v_e = (1 - gamma_fraction) * P_ann
    Gamma power: P_gamma = P_ann * gamma_fraction
    Intercepted gamma power by structure: P_int = P_gamma * solid_angle_fraction
    Radiative cooling of shield at T_shield: q_rad = emissivity * sigma * T_shield^4
    Shield area: A_shield = P_int / q_rad
    Shield mass: M_shield = A_shield * thickness * density
    """
    # P_jet from charged pions
    p_jet = 0.5 * thrust_n * v_exhaust
    # Total annihilation power
    p_ann = p_jet / (1.0 - gamma_fraction)
    p_gamma = p_ann * gamma_fraction
    p_intercepted = p_gamma * solid_angle_fraction
    
    q_rad = emissivity * SIGMA_SB * (t_shield**4)
    a_shield = p_intercepted / q_rad
    m_shield = a_shield * shield_thickness_m * shield_density
    
    return {
        "annihilation_power_w": p_ann,
        "gamma_power_w": p_gamma,
        "intercepted_gamma_power_w": p_intercepted,
        "shield_radiator_area_m2": a_shield,
        "shield_mass_kg": m_shield,
        "shield_mass_tonnes": m_shield / 1000.0
    }


def macro_pellet_vs_laser_beam_comparison(pellet_velocity=3.0e6, pellet_mass=1.0e-9, pellet_temp=1.0, laser_wavelength=1.06e-6, laser_aperture=1000.0, range_m=AU):
    """
    Compares hypervelocity macro-pellet stream against optical laser beam:
    1. Thrust per unit beam power (F / P).
    2. Transverse beam divergence and spot size at range_m.
    """
    # Laser photon thrust per power (perfect 100% reflection): F/P = 2 / c
    laser_f_over_p = 2.0 / C
    
    # Macro-pellet elastic 180-deg deflection thrust per kinetic power:
    # F = 2 * m_dot * u, P_k = 0.5 * m_dot * u^2 -> F / P_k = 4 / u
    pellet_f_over_p = 4.0 / pellet_velocity
    thrust_power_gain = pellet_f_over_p / laser_f_over_p
    
    # Laser diffraction divergence half-angle: theta_laser = 1.22 * lambda / D
    theta_laser = 1.22 * laser_wavelength / laser_aperture
    spot_radius_laser = range_m * theta_laser
    
    # Pellet thermal divergence half-angle: v_th = sqrt(3 * k_B * T / m)
    v_th = math.sqrt(3.0 * K_B * pellet_temp / pellet_mass)
    theta_pellet = v_th / pellet_velocity
    spot_radius_pellet = range_m * theta_pellet
    
    spot_ratio = spot_radius_laser / spot_radius_pellet
    
    return {
        "laser_f_over_p_n_w": laser_f_over_p,
        "pellet_f_over_p_n_w": pellet_f_over_p,
        "thrust_gain_factor": thrust_power_gain,
        "laser_divergence_rad": theta_laser,
        "pellet_divergence_rad": theta_pellet,
        "laser_spot_radius_m": spot_radius_laser,
        "pellet_spot_radius_m": spot_radius_pellet,
        "spot_concentration_gain": spot_ratio
    }


def exoplanet_terminal_capture_analysis(stellar_wind_v=400000.0, exoplanet_a=A_PROXIMA_B, host_mass=M_PROXIMA):
    """
    Computes kinematics and delta-v requirements for capturing into Proxima b orbit:
    1. Circular orbital velocity v_c around host star at exoplanet distance.
    2. Minimum hyperbolic excess v_inf after magsail deceleration cutoff at stellar wind speed.
    3. Terminal capture delta-v requirement.
    4. Propellant mass ratio for chemical (452 s) vs ion (10,000 s).
    5. Aerocapture convective heating scaling relative to Apollo re-entry (11 km/s).
    """
    # Circular velocity around host star
    v_c = math.sqrt(G_CONST * host_mass / exoplanet_a)
    
    # Minimum hyperbolic excess when magsail decouples from stellar wind
    v_inf = max(0.0, stellar_wind_v - v_c)
    
    # Delta-v to insert from hyperbolic flyby to circular orbit:
    # Delta_v_cap = sqrt(v_inf^2 + 2*v_c^2) - v_c (approx v_inf for high excess)
    # Using standard vis-viva / hyperbolic insertion:
    v_peri = math.sqrt(v_inf**2 + 2.0 * (v_c**2))
    delta_v_cap = v_peri - v_c
    
    # Rocket equation mass ratios
    # Chemical: Isp = 452 s -> v_e = 452 * 9.80665 = 4432.6 m/s
    v_e_chem = 452.0 * G0
    ln_mr_chem = delta_v_cap / v_e_chem
    log10_mr_chem = ln_mr_chem / math.log(10.0)
    
    # Ion: Isp = 10,000 s -> v_e = 98066.5 m/s
    v_e_ion = 10000.0 * G0
    mr_ion = math.exp(delta_v_cap / v_e_ion)
    
    # Aerocapture stagnation heat flux scales as v^3
    v_apollo = 11000.0  # 11 km/s
    aerocapture_heat_ratio = (stellar_wind_v / v_apollo)**3
    
    return {
        "host_orbital_velocity_m_s": v_c,
        "hyperbolic_excess_v_inf_m_s": v_inf,
        "periapsis_velocity_m_s": v_peri,
        "terminal_capture_delta_v_m_s": delta_v_cap,
        "log10_mass_ratio_chemical": log10_mr_chem,
        "mass_ratio_ion": mr_ion,
        "aerocapture_heat_ratio_vs_apollo": aerocapture_heat_ratio
    }


def complete_propulsion_feasibility_matrix():
    """
    Returns the comprehensive, ranked propulsion feasibility matrix across all 10 archetypes.
    """
    return [
        {
            "rank": 1,
            "family": "Chemical (LOX/LH2)",
            "isp_s": 452,
            "v_e_kms": 4.43,
            "thrust_range": "100 N to 20 MN",
            "tw_ratio": "70 - 150",
            "thrust_per_mw": 451.3,
            "domain": "Earth surface launch, Cis-Lunar injection",
            "interstellar": False,
            "flyby_mr_log10": 2947,
            "rendezvous_mr_log10": 5894,
            "single_biggest_blocker": "Chemical bond enthalpy ceiling (Q <= 13.4 MJ/kg); propellant mass to 0.1c exceeds observable universe."
        },
        {
            "rank": 2,
            "family": "Solar Electric / Ion",
            "isp_s": 5000,
            "v_e_kms": 49.0,
            "thrust_range": "1 mN to 5 N",
            "tw_ratio": "1e-5 to 1e-4",
            "thrust_per_mw": 40.8,
            "domain": "Cis-Lunar, Asteroid Belt (< 3 AU)",
            "interstellar": False,
            "flyby_mr_log10": 266,
            "rendezvous_mr_log10": 532,
            "single_biggest_blocker": "Solar flux 1/r^2 dilution; at Jupiter irradiance drops by 27x, choking thrust to zero."
        },
        {
            "rank": 3,
            "family": "Solar Sail (Photon Pressure)",
            "isp_s": float("inf"),
            "v_e_kms": 300000.0,
            "thrust_range": "9.08 uN/m^2 at 1 AU",
            "tw_ratio": "1e-4 to 1e-3",
            "thrust_per_mw": 0.0067,
            "domain": "Inner Solar System, SGL Focus (550 AU in 22 yr)",
            "interstellar": False,
            "flyby_mr_log10": 0.0,
            "rendezvous_mr_log10": float("inf"),
            "single_biggest_blocker": "Thermal perihelion sublimation caps terminal velocity at <= 737 km/s (0.0025c); transit takes > 1,700 yr."
        },
        {
            "rank": 4,
            "family": "Nuclear Thermal (NTR)",
            "isp_s": 900,
            "v_e_kms": 8.83,
            "thrust_range": "10 kN to 1 MN",
            "tw_ratio": "3 - 7",
            "thrust_per_mw": 226.6,
            "domain": "Fast Mars Sprint (90 days), Deep Solar System",
            "interstellar": False,
            "flyby_mr_log10": 1480,
            "rendezvous_mr_log10": 2960,
            "single_biggest_blocker": "Refractory carbide core melting (T <= 3100 K) and hydrogen erosion cap exhaust velocity at 9 km/s."
        },
        {
            "rank": 5,
            "family": "Nuclear Electric (NEP)",
            "isp_s": 5000,
            "v_e_kms": 49.0,
            "thrust_range": "5 N to 100 N (at 1-5 MWe)",
            "tw_ratio": "1e-5 to 1e-4",
            "thrust_per_mw": 20.4,
            "domain": "Outer planet orbital tours (Jupiter/Saturn orbiters)",
            "interstellar": False,
            "flyby_mr_log10": 266,
            "rendezvous_mr_log10": 532,
            "single_biggest_blocker": "Stuhlinger power wall (alpha <= 100 W/kg); radiator mass scaling requires 142,400 yr burn to reach 0.1c."
        },
        {
            "rank": 6,
            "family": "Nuclear Pulse (Project Orion)",
            "isp_s": 6000,
            "v_e_kms": 58.8,
            "thrust_range": "10 MN to 100 MN",
            "tw_ratio": "1 - 10",
            "thrust_per_mw": 34.0,
            "domain": "Heavy interplanetary freight (10,000 t to outer planets)",
            "interstellar": False,
            "flyby_mr_log10": 222,
            "rendezvous_mr_log10": 444,
            "single_biggest_blocker": "Pusher-plate surface ablation and spallation fatigue from hypervelocity plasma pulses; LTBT/OST treaties."
        },
        {
            "rank": 7,
            "family": "Nuclear Fusion (D-3He Magnetic Nozzle)",
            "isp_s": 2000000,
            "v_e_kms": 19613.3,
            "thrust_range": "1 kN to 50 kN",
            "tw_ratio": "1e-4 to 1e-3",
            "thrust_per_mw": 0.102,
            "domain": "Interstellar flyby and rendezvous (0.1c in 42 yr)",
            "interstellar": True,
            "flyby_mr_log10": 0.66,
            "rendezvous_mr_log10": 2.43,
            "single_biggest_blocker": "Lawson criterion n*tau*T >= 10^22 keV s/m^3 unachieved; 3He lunar mining (10.35 billion tonnes soil, 2,156 TWh)."
        },
        {
            "rank": 8,
            "family": "Antimatter Beamed-Core (p-pbar)",
            "isp_s": 10118600,
            "v_e_kms": 99230.0,
            "thrust_range": "1 kN to 50 kN",
            "tw_ratio": "1e-3 to 1e-2",
            "thrust_per_mw": 0.0202,
            "domain": "Relativistic interstellar rendezvous (0.1c - 0.3c)",
            "interstellar": True,
            "flyby_mr_log10": 0.13,
            "rendezvous_mr_log10": 0.28,
            "single_biggest_blocker": "Production efficiency eta ~ 10^-9 (820,000 yr global grid energy); 33% neutral pion gamma flash requires 2,470 t shield."
        },
        {
            "rank": 9,
            "family": "Laser-Pushed Beamed Sail (Starshot)",
            "isp_s": float("inf"),
            "v_e_kms": 300000.0,
            "thrust_range": "667 N (100 GW beam on 1 g probe)",
            "tw_ratio": "68000 (at 1 g)",
            "thrust_per_mw": 0.0067,
            "domain": "Relativistic gram-scale flyby (0.2c in 21 yr)",
            "interstellar": True,
            "flyby_mr_log10": 0.0,
            "rendezvous_mr_log10": float("inf"),
            "single_biggest_blocker": "Phase-coherent km-scale optics and zero braking capacity; stopping requires 792 kg quadrupole magsail."
        },
        {
            "rank": 10,
            "family": "Bussard Interstellar Ramjet",
            "isp_s": float("inf"),
            "v_e_kms": 35728.0,
            "thrust_range": "0 to 100 kN",
            "tw_ratio": "1e-5 to 1e-3",
            "thrust_per_mw": 0.0559,
            "domain": "Relativistic interstellar cruise (Disproven)",
            "interstellar": False,
            "flyby_mr_log10": 0.0,
            "rendezvous_mr_log10": float("inf"),
            "single_biggest_blocker": "Fishback-Powell ram drag exceeds fusion thrust for beta >= 0.119; compression bremsstrahlung radiates 3.9e20x fusion power."
        }
    ]
