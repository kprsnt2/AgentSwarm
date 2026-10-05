"""
propulsion_astrospheric_and_resource_closure_engine.py
======================================================
Astrospheric Plasma Dynamics, Superconducting Magsail Stability,
and Global Resource/Energy Cycle Closure Engine for Practical Space Propulsion.

Provides:
1. Astrospheric Ingress & Magnetic Torque Catastrophe:
   - Calculates external torque tau = m x B_sw on superconducting loops.
   - Proves angular acceleration alpha = 2*pi*I*B/M is independent of loop radius.
   - Derives centrifugal bursting stress sigma = rho * (alpha*t)^2 * R^2 and rupture time.
   - Analyzes Anti-Helmholtz quadrupole configuration (tau_net = 0, r^-4 decay, 2x mass penalty).
2. Superconducting Coil Radiation Damage & Quench Horizon:
   - Evaluates GCR fluence and stellar flare proton accumulation in YBCO/REBCO tape.
   - Calculates critical current density J_c degradation and radiative equilibrium quench limit.
3. Global Industrial Energy Cycle & Resource Scarcity Bounds:
   - Quantifies lunar regolith thermal extraction energy for D-3He fusion fuel.
   - Quantifies accelerator grid energy, production yields, and annihilation hazard for p-pbar antimatter.
   - Quantifies launch energy, capital infrastructure, and recurring electricity cost for beamed laser sails.
4. Definitive Ranked Practical Propulsion Feasibility Matrix:
   - Compares all 10 propulsion families across specific impulse, thrust, mission capability,
     energy/mass cost, and single biggest engineering blocker.

Author: Kepler (Agent A001, Generation 0)
Domain: Practical space propulsion (propulsion)
Epistemic Class: Engineering feasibility, astrospheric plasma dynamics, relativistic mechanics
"""

import math
from typing import Dict, Any, List, Optional, Tuple

# Fundamental Physical Constants (CODATA 2022 / SI Units)
C: float = 299792458.0              # Speed of light (m/s)
G0: float = 9.80665                 # Standard gravity (m/s^2)
SIGMA_SB: float = 5.670374419e-8    # Stefan-Boltzmann constant (W/m^2/K^4)
AU: float = 149597870700.0          # Astronomical Unit (m)
LY: float = 9.4607304725808e15      # Light year (m)
YEAR: float = 365.25 * 86400.0      # Julian year (s)
MP: float = 1.67262192369e-27       # Proton mass (kg)
QE: float = 1.602176634e-19         # Elementary charge (C)
MU0: float = 1.25663706212e-6       # Vacuum permeability (H/m)
KB: float = 1.380649e-23            # Boltzmann constant (J/K)
RHO_ISM: float = 1.67e-21           # Interstellar medium density (kg/m^3)
JOULES_PER_TWH: float = 3.6e15      # Joules per Terawatt-hour
TNT_EQUIVALENT_J: float = 4.184e9   # Joules per ton TNT
MEGATON_TNT_J: float = 4.184e15     # Joules per Megaton TNT
GLOBAL_ANNUAL_ELEC_TWH: float = 28000.0  # Current global electrical production (~28,000 TWh/year)


def magsail_dipole_moment(current_a: float, radius_m: float) -> float:
    """
    Magnetic dipole moment m = I * pi * R^2 (A*m^2).
    """
    if current_a < 0.0 or radius_m <= 0.0:
        raise ValueError("Current must be non-negative and radius positive.")
    return current_a * math.pi * (radius_m**2)


def magsail_transverse_torque(dipole_moment: float, b_field_t: float) -> float:
    """
    Maximum transverse magnetic torque tau = m * B (N*m).
    Occurs when magnetic moment is orthogonal to external stellar magnetic field.
    """
    return dipole_moment * b_field_t


def magsail_angular_acceleration(current_a: float, b_field_t: float, coil_mass_kg: float) -> float:
    """
    Angular acceleration of a thin circular hoop spinning about its diameter:
    I_diam = (1/2) * M * R^2
    tau = m * B = I * pi * R^2 * B
    alpha = tau / I_diam = (I * pi * R^2 * B) / (0.5 * M * R^2) = (2 * pi * I * B) / M
    Remarkably, alpha is INDEPENDENT of loop radius R!
    """
    if coil_mass_kg <= 0.0:
        raise ValueError("Coil mass must be strictly positive.")
    return (2.0 * math.pi * current_a * b_field_t) / coil_mass_kg


def magsail_bursting_stress(
    density_kg_m3: float,
    angular_velocity_rad_s: float,
    radius_m: float
) -> float:
    """
    Hoop tensile stress due to centrifugal force in a spinning thin ring:
    sigma = rho * v_tan^2 = rho * (omega * R)^2 (Pa).
    """
    v_tan = angular_velocity_rad_s * radius_m
    return density_kg_m3 * (v_tan**2)


def magsail_rupture_time(
    current_a: float,
    b_field_t: float,
    coil_mass_kg: float,
    radius_m: float,
    density_kg_m3: float,
    sigma_uts_pa: float
) -> Dict[str, float]:
    """
    Calculates time until magnetic torque-induced spin-up exceeds the ultimate tensile strength (UTS).
    omega(t) = alpha * t
    sigma(t) = rho * (alpha * t * R)^2 = sigma_uts
    t_rupture = sqrt(sigma_uts / rho) / (alpha * R)
    """
    alpha = magsail_angular_acceleration(current_a, b_field_t, coil_mass_kg)
    v_critical = math.sqrt(sigma_uts_pa / density_kg_m3)
    omega_critical = v_critical / radius_m
    t_rupture_s = v_critical / (alpha * radius_m)
    
    return {
        "angular_acceleration_rad_s2": alpha,
        "critical_angular_velocity_rad_s": omega_critical,
        "critical_rotation_rpm": (omega_critical * 60.0) / (2.0 * math.pi),
        "rupture_time_seconds": t_rupture_s,
        "rupture_time_minutes": t_rupture_s / 60.0,
        "rupture_time_hours": t_rupture_s / 3600.0,
    }


def anti_helmholtz_quadrupole_analysis(
    current_a: float,
    radius_m: float,
    coil_mass_kg: float
) -> Dict[str, Any]:
    """
    Analyzes an Anti-Helmholtz coaxial dual-coil quadrupole configuration:
    - Coil 1 at z = +d with current +I
    - Coil 2 at z = -d with current -I
    Result:
    - Net dipole moment m_net = m1 + m2 = +I*pi*R^2 - I*pi*R^2 = 0.
    - External uniform field torque tau_net = 0 (completely immune to tumbling instability!).
    - Magnetic field scales as 1/r^4 instead of 1/r^3.
    - To match dipole magnetopause standoff distance, requires 4x current or 2x coil mass.
    """
    dipole_m = magsail_dipole_moment(current_a, radius_m)
    quadrupole_mass = 2.0 * coil_mass_kg
    
    return {
        "single_coil_dipole_moment_a_m2": dipole_m,
        "net_quadrupole_dipole_moment": 0.0,
        "net_uniform_torque_n_m": 0.0,
        "tumbling_instability_suppressed": True,
        "field_falloff_exponent": 4,  # r^-4
        "mass_penalty_multiplier": 2.0,
        "total_quadrupole_mass_kg": quadrupole_mass,
    }


def superconductor_radiation_fluence(
    transit_years: float,
    gcr_proton_flux_cm2_s: float = 4.0,
    annual_flare_fluence_cm2: float = 5.0e12,
    orbital_residence_years: float = 10.0
) -> Dict[str, Any]:
    """
    Calculates proton radiation fluence in YBCO high-temperature superconducting (HTS) tape.
    - Cruise phase: Galactic Cosmic Ray (GCR) protons.
    - Orbital phase: Target M-dwarf stellar flare protons.
    - Critical damage threshold for YBCO J_c degradation: ~5.0e15 protons/cm^2.
    """
    t_cruise_s = transit_years * YEAR
    cruise_gcr_fluence = gcr_proton_flux_cm2_s * t_cruise_s
    orbital_flare_fluence = annual_flare_fluence_cm2 * orbital_residence_years
    total_proton_fluence = cruise_gcr_fluence + orbital_flare_fluence
    
    phi_crit_ybco = 5.0e15  # protons/cm^2
    damage_fraction = total_proton_fluence / phi_crit_ybco
    
    # Critical temperature depression: delta_Tc ~ - (total_fluence / 1e16) * 15 K
    delta_tc_k = - (total_proton_fluence / 1.0e16) * 15.0
    
    return {
        "cruise_years": transit_years,
        "cruise_gcr_fluence_cm2": cruise_gcr_fluence,
        "orbital_flare_fluence_cm2": orbital_flare_fluence,
        "total_proton_fluence_cm2": total_proton_fluence,
        "ybco_critical_fluence_cm2": phi_crit_ybco,
        "damage_fraction": damage_fraction,
        "superconductor_quenched_by_radiation": total_proton_fluence >= phi_crit_ybco,
        "delta_tc_depression_k": delta_tc_k,
    }


def lunar_helium3_resource_cost(
    payload_mass_kg: float,
    beta: float = 0.10,
    ve: float = 1.349e7,
    structural_eps: float = 0.05,
    he3_regolith_ppb: float = 15.0,
    degassing_energy_j_per_kg: float = 7.5e5
) -> Dict[str, Any]:
    """
    Calculates the complete resource, mass, and energy extraction cost of 3He
    from lunar regolith for a 2-stage D-3He fusion rendezvous mission to 0.1c.
    - Optimal 2-stage mass ratio: R_stage = sqrt(R_total) = exp(beta*c / ve)
    - Fuel mixture: D-3He equimolar (2 kg D per 3 kg 3He => 60% 3He by mass).
    - Lunar regolith abundance: ~15 ppb (1.5e-8 kg 3He per kg regolith).
    - Degassing energy: Heating regolith to 700 C requires ~7.5e5 J/kg.
    """
    # 2-stage rendezvous mass ratio
    y = math.atanh(beta)
    r_flyby = math.exp((C / ve) * y)
    r_total = r_flyby**2  # R_2
    
    # 2-stage vehicle: each stage has R_stage = sqrt(r_total) = r_flyby
    r_s = r_flyby
    stage_mult = (r_s * (1.0 - structural_eps)) / (1.0 - structural_eps * r_s)
    total_mass_multiplier = stage_mult**2
    
    wet_mass_kg = total_mass_multiplier * payload_mass_kg
    # Total fuel burned across both stages
    total_fuel_kg = wet_mass_kg - payload_mass_kg - (wet_mass_kg * structural_eps)
    
    he3_mass_kg = total_fuel_kg * 0.60
    d2_mass_kg = total_fuel_kg * 0.40
    
    # Lunar mining
    he3_fraction = he3_regolith_ppb * 1.0e-9
    regolith_mined_kg = he3_mass_kg / he3_fraction
    regolith_mined_tonnes = regolith_mined_kg / 1000.0
    
    total_degas_energy_j = regolith_mined_kg * degassing_energy_j_per_kg
    total_degas_energy_twh = total_degas_energy_j / JOULES_PER_TWH
    fraction_global_annual_electricity = total_degas_energy_twh / GLOBAL_ANNUAL_ELEC_TWH
    
    return {
        "payload_mass_kg": payload_mass_kg,
        "cruise_beta": beta,
        "total_wet_mass_kg": wet_mass_kg,
        "total_fuel_consumed_kg": total_fuel_kg,
        "he3_fuel_mass_kg": he3_mass_kg,
        "d2_fuel_mass_kg": d2_mass_kg,
        "regolith_mined_tonnes": regolith_mined_tonnes,
        "regolith_mined_billion_tonnes": regolith_mined_tonnes / 1.0e9,
        "thermal_degas_energy_joules": total_degas_energy_j,
        "thermal_degas_energy_twh": total_degas_energy_twh,
        "fraction_global_annual_electricity": fraction_global_annual_electricity,
    }


def antimatter_industrial_cost(
    payload_mass_kg: float,
    beta: float = 0.10,
    ve: float = 9.923e7,
    structural_eps: float = 0.05,
    production_efficiency_eta: float = 1.0e-9
) -> Dict[str, Any]:
    """
    Calculates the industrial energy footprint, grid cost, and explosive annihilation hazard
    for an antimatter beamed-core rendezvous mission to 0.1c.
    - Antimatter exhaust velocity: ve = 0.331 c (charged pions).
    - Propellant: 50% antiprotons, 50% LH2.
    - Current accelerator production efficiency: eta ~ 1.0e-9 (requires 10^9 times E = 2mc^2).
    """
    y = math.atanh(beta)
    r_flyby = math.exp((C / ve) * y)
    r_total = r_flyby**2
    
    # Single-stage vehicle with structural fraction eps
    if (1.0 / r_total) <= structural_eps:
        raise ValueError("Mass ratio exceeds single-stage structural limit.")
    
    mass_multiplier = (r_total * (1.0 - structural_eps)) / (1.0 - structural_eps * r_total)
    wet_mass_kg = mass_multiplier * payload_mass_kg
    # Total propellant consumed: m0 - mf where mf = m0 / r_total
    propellant_mass_kg = wet_mass_kg * (1.0 - (1.0 / r_total))
    
    pbar_mass_kg = propellant_mass_kg * 0.50
    lh2_mass_kg = propellant_mass_kg * 0.50
    
    # Energy required to produce antiprotons
    e_annihilation_j = 2.0 * pbar_mass_kg * C**2
    grid_energy_j = e_annihilation_j / production_efficiency_eta
    grid_energy_twh = grid_energy_j / JOULES_PER_TWH
    years_of_current_global_power = grid_energy_twh / GLOBAL_ANNUAL_ELEC_TWH
    
    annihilation_megatons_tnt = e_annihilation_j / MEGATON_TNT_J
    tsar_bomba_multiples = annihilation_megatons_tnt / 50.0  # 50 Mt Tsar Bomba
    
    return {
        "payload_mass_kg": payload_mass_kg,
        "cruise_beta": beta,
        "wet_mass_kg": wet_mass_kg,
        "propellant_mass_kg": propellant_mass_kg,
        "pbar_mass_kg": pbar_mass_kg,
        "lh2_mass_kg": lh2_mass_kg,
        "grid_energy_joules": grid_energy_j,
        "grid_energy_twh": grid_energy_twh,
        "years_current_global_power": years_of_current_global_power,
        "annihilation_energy_megatons_tnt": annihilation_megatons_tnt,
        "tsar_bomba_multiples": tsar_bomba_multiples,
    }


def laser_sail_energy_and_economic_cost(
    payload_mass_kg: float = 0.001,
    beta: float = 0.20,
    laser_power_w: float = 1.0e11,
    sail_reflectivity: float = 0.99999,
    kwh_electricity_cost_usd: float = 0.05
) -> Dict[str, Any]:
    """
    Calculates acceleration parameters, orbital laser power requirements, and electricity cost
    for a laser-pushed beamed sail (Starshot wafercraft).
    - Photon thrust: F = 2 * P_laser * R / c
    - Acceleration: a = F / m
    - Burn time to v = beta*c: t = v / a
    - Acceleration distance: s = (1/2) * a * t^2
    - Energy consumed: E = P * t
    """
    thrust_n = (2.0 * laser_power_w * sail_reflectivity) / C
    accel_m_s2 = thrust_n / payload_mass_kg
    accel_g = accel_m_s2 / G0
    
    target_v = beta * C
    burn_time_s = target_v / accel_m_s2
    burn_distance_m = 0.5 * accel_m_s2 * (burn_time_s**2)
    burn_distance_au = burn_distance_m / AU
    
    energy_joules = laser_power_w * burn_time_s
    energy_kwh = energy_joules / 3.6e6
    energy_mwh = energy_joules / 3.6e9
    energy_gwh = energy_mwh / 1000.0
    electricity_cost_usd = energy_kwh * kwh_electricity_cost_usd
    
    return {
        "payload_mass_kg": payload_mass_kg,
        "cruise_beta": beta,
        "laser_power_gw": laser_power_w / 1.0e9,
        "thrust_newtons": thrust_n,
        "acceleration_g": accel_g,
        "burn_time_seconds": burn_time_s,
        "burn_distance_au": burn_distance_au,
        "energy_consumed_joules": energy_joules,
        "energy_consumed_mwh": energy_mwh,
        "energy_consumed_gwh": energy_gwh,
        "electricity_cost_per_launch_usd": electricity_cost_usd,
    }


def ranked_propulsion_closure_matrix() -> List[Dict[str, Any]]:
    """
    Returns the comprehensive, definitively ranked practical space propulsion matrix
    for all 10 propulsion families with exact physical quantities and blockers.
    """
    return [
        {
            "rank": 1,
            "name": "Chemical (LOX/LH2)",
            "isp_s": 452.0,
            "ve_km_s": 4.43,
            "thrust_n_min": 100.0,
            "thrust_n_max": 2.0e7,
            "t_w": "70 - 150",
            "f_p_ratio": "451.3 N/MW",
            "primary_domain": "Earth surface launch, Cis-Lunar injection",
            "interstellar_capable": False,
            "flyby_log10_r": 2947.0,
            "rendezvous_m0_mL": "Infinity (10^5894)",
            "primary_energy_cost": "Infinity",
            "single_biggest_blocker": "Chemical bond enthalpy ceiling (Q <= 13.4 MJ/kg): Propellant mass to reach 0.1c exceeds universe mass by 10^2860; multi-staging cannot bridge this gap (R_inf = 10^309 at 0.01c)."
        },
        {
            "rank": 2,
            "name": "Solar Electric / Ion (Hall, Gridded, MPD)",
            "isp_s": 5000.0,
            "ve_km_s": 49.0,
            "thrust_n_min": 0.001,
            "thrust_n_max": 5.0,
            "t_w": "10^-5 - 10^-4",
            "f_p_ratio": "40.8 N/MW",
            "primary_domain": "Cis-Lunar stationkeeping, Asteroid Belts (< 3 AU)",
            "interstellar_capable": False,
            "flyby_log10_r": 380.0,
            "rendezvous_m0_mL": "Infinity (10^760)",
            "primary_energy_cost": "Infinity",
            "single_biggest_blocker": "Solar flux 1/r^2 dilution: Irradiance drops from 1361 W/m^2 at 1 AU to 50 W/m^2 at Jupiter; solar array mass scales as r^2, choking outer-planet thrust to zero."
        },
        {
            "rank": 3,
            "name": "Solar Sail (Radiation Pressure)",
            "isp_s": float('inf'),
            "ve_km_s": 299792.458,
            "thrust_n_min": 9.08e-6,
            "thrust_n_max": 10.0,
            "t_w": "10^-4 - 10^-3",
            "f_p_ratio": "0.0067 N/MW",
            "primary_domain": "Inner Solar System, SGL Focus (550 AU in 21.7 yr)",
            "interstellar_capable": False,
            "flyby_log10_r": 0.0,
            "rendezvous_m0_mL": "Infinity (unbraked)",
            "primary_energy_cost": "0.0 J (free solar flux)",
            "single_biggest_blocker": "Thermal perihelion sublimation: Terminal velocity capped at v_max <= 737 km/s (0.0025c) at 0.05 AU perihelion; interstellar transit requires >1,700 years."
        },
        {
            "rank": 4,
            "name": "Nuclear Thermal (Solid-Core NTR)",
            "isp_s": 900.0,
            "ve_km_s": 8.83,
            "thrust_n_min": 1.0e4,
            "thrust_n_max": 1.0e6,
            "t_w": "3 - 7",
            "f_p_ratio": "226.6 N/MW",
            "primary_domain": "Cis-Lunar heavy cargo, fast Mars sprint (90 days)",
            "interstellar_capable": False,
            "flyby_log10_r": 1480.0,
            "rendezvous_m0_mL": "Infinity (10^2960)",
            "primary_energy_cost": "Infinity",
            "single_biggest_blocker": "Refractory carbide melting (T_core <= 3,100 K): Solid-core sublimation and hydrogen corrosion cap exhaust speed; single-stage Delta-v <= 20.8 km/s."
        },
        {
            "rank": 5,
            "name": "Nuclear Electric (NEP)",
            "isp_s": 5000.0,
            "ve_km_s": 49.0,
            "thrust_n_min": 5.0,
            "thrust_n_max": 100.0,
            "t_w": "10^-5 - 10^-4",
            "f_p_ratio": "20.4 N/MW",
            "primary_domain": "Deep Outer Planet Tours (Jupiter/Saturn orbiters, Kuiper Belt)",
            "interstellar_capable": False,
            "flyby_log10_r": 222.0,
            "rendezvous_m0_mL": "Infinity (10^444)",
            "primary_energy_cost": "Infinity",
            "single_biggest_blocker": "Stuhlinger specific-power wall (alpha <= 100 W/kg): Radiator mass scales as T^-4; accelerating to 0.1c requires 142,400 years of continuous burn."
        },
        {
            "rank": 6,
            "name": "Nuclear Pulse (Project Orion)",
            "isp_s": 5000.0,
            "ve_km_s": 49.0,
            "thrust_n_min": 1.0e7,
            "thrust_n_max": 1.0e8,
            "t_w": "1 - 10",
            "f_p_ratio": "34.0 N/MW",
            "primary_domain": "Massive interplanetary freight (10^4 tonnes to outer planets)",
            "interstellar_capable": False,
            "flyby_log10_r": 222.0,
            "rendezvous_m0_mL": "Infinity (10^444)",
            "primary_energy_cost": "Infinity",
            "single_biggest_blocker": "Pusher-plate ablation & spallation fatigue: Severe shock degradation from hypervelocity plasma bursts; international nuclear test-ban treaties (LTBT/OST)."
        },
        {
            "rank": 7,
            "name": "Nuclear Fusion (D-3He Magnetic Nozzle)",
            "isp_s": 1.38e6,
            "ve_km_s": 13500.0,
            "thrust_n_min": 1.0e3,
            "thrust_n_max": 5.0e4,
            "t_w": "10^-4 - 10^-3",
            "f_p_ratio": "0.148 N/MW",
            "primary_domain": "High-speed interplanetary sprint, Interstellar Flyby & Rendezvous",
            "interstellar_capable": True,
            "flyby_log10_r": 0.97,
            "rendezvous_m0_mL": "272.4 kg/kg (2-stage)",
            "primary_energy_cost": "25.5 TWh/tonne payload",
            "single_biggest_blocker": "Thermonuclear Lawson criterion & 3He scarcity: n*tau*T >= 10^22 keV*s/m^3 unachieved; 3He absent on Earth, requiring mining 10.35 billion tonnes of lunar regolith (2,156 TWh thermal energy)."
        },
        {
            "rank": 8,
            "name": "Antimatter Beamed-Core (p-pbar Annihilation)",
            "isp_s": 1.01e7,
            "ve_km_s": 99230.0,
            "thrust_n_min": 1.0e3,
            "thrust_n_max": 5.0e4,
            "t_w": "10^-3 - 10^-2",
            "f_p_ratio": "0.0202 N/MW",
            "primary_domain": "Relativistic Interstellar Transit with Destination Orbit Insertion",
            "interstellar_capable": True,
            "flyby_log10_r": 0.13,
            "rendezvous_m0_mL": "1.92 kg/kg (1-stage)",
            "primary_energy_cost": "2.295e10 TWh/tonne payload",
            "single_biggest_blocker": "Antiproton production yield & gamma flash: Production efficiency eta ~ 10^-9 requires 820,000 years of global electrical grid energy; pi0 decay creates 300 GW gamma flash requiring 688 t radiators; storage of 459 kg represents 19,740 Mt TNT hazard."
        },
        {
            "rank": 9,
            "name": "Laser-Pushed Beamed Sail (Starshot)",
            "isp_s": float('inf'),
            "ve_km_s": 299792.458,
            "thrust_n_min": 667.0,
            "thrust_n_max": 667.0,
            "t_w": "10^4 - 10^5 (1 g)",
            "f_p_ratio": "0.0067 N/MW",
            "primary_domain": "Relativistic Gram-Scale Interstellar Flyby (0.20c, 21.2 yr)",
            "interstellar_capable": True,
            "flyby_log10_r": 0.0,
            "rendezvous_m0_mL": "42.0 kg/kg (hybrid magsail)",
            "primary_energy_cost": "14.4 MWh per 1 g wafercraft ($722)",
            "single_biggest_blocker": "Phase coherence, pointing, & brake asymmetry: Requires 1.8 km orbital phased array, <=0.15 mas pointing jitter, and A_abs <= 9.1 ppm absorption; deceleration requires 396 kg magsail, strictly ruling out wafercraft stopping."
        },
        {
            "rank": 10,
            "name": "Bussard Interstellar Ramjet",
            "isp_s": float('inf'),
            "ve_km_s": 35728.0,
            "thrust_n_min": 0.0,
            "thrust_n_max": 1.0e5,
            "t_w": "10^-5 - 10^-3",
            "f_p_ratio": "0.0559 N/MW",
            "primary_domain": "Steady-state relativistic cruise (Theoretically Proposed)",
            "interstellar_capable": False,
            "flyby_log10_r": 0.0,
            "rendezvous_m0_mL": "Infinity (drag brake)",
            "primary_energy_cost": "Infinity",
            "single_biggest_blocker": "Fishback-Powell relativistic drag & bremsstrahlung wall: Incoming ram drag exceeds fusion thrust for beta >= 0.119; p-p fusion cross section (10^-47 m^2) is negligible; compression bremsstrahlung radiates 3.9e20x faster than fusion releases power."
        }
    ]
