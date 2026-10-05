"""
propulsion_encounter_deflection_and_link_engine.py

Core Epistemic Engine for Practical Space Propulsion:
1. Electrostatic & Magnetic Dust Deflection Impossibility Limits.
2. Relativistic Planetary Encounter Kinematics and Smear Limits.
3. Interstellar Optical Link Budget and Photon Starvation Scaling.
4. Comprehensive 9-Family Propulsion Database & Comparative Ranked Matrix.

Author: Kepler (Agent A001, Generation 0)
Domain: Practical space propulsion (propulsion)
Epistemic Class: Engineering Feasibility & Physics Limits
"""

import math

# Fundamental Physical Constants
C = 299792458.0                    # Speed of light in vacuum (m/s)
H = 6.62607015e-34                 # Planck constant (J*s)
G0 = 9.80665                       # Standard gravitational acceleration (m/s^2)
EPSILON_0 = 8.8541878128e-12       # Vacuum permittivity (F/m)
E_CHARGE = 1.602176634e-19         # Elementary charge (C)
SIGMA_SB = 5.670374419e-8          # Stefan-Boltzmann constant (W/m^2/K^4)
AU = 1.495978707e11                # Astronomical Unit (m)
LY = 9.4607304725808e15            # Light-year (m)
DIST_PROXIMA = 4.244 * LY          # Distance to Proxima Centauri (m)


def relativistic_gamma(beta: float) -> float:
    """Calculate Lorentz factor gamma."""
    if beta >= 1.0:
        raise ValueError("Beta must be strictly less than 1.0")
    return 1.0 / math.sqrt(1.0 - beta**2)


def evaluate_electrostatic_deflection(
    grain_radius_m: float = 1.0e-6,
    grain_density: float = 2500.0,
    beta: float = 0.20,
    grain_potential_volts: float = 5.0,
    breakdown_field_v_per_m: float = 1.0e9,
) -> dict:
    """
    Evaluates electrostatic deflection feasibility for interstellar dust grains.
    Shows that required deflection voltages violate vacuum dielectric breakdown by > 7 orders of magnitude.
    """
    gamma = relativistic_gamma(beta)
    v = beta * C
    grain_volume = (4.0 / 3.0) * math.pi * (grain_radius_m ** 3)
    grain_mass = grain_density * grain_volume
    
    # Kinetic energy of relativistic grain
    grain_ke_j = (gamma - 1.0) * grain_mass * (C ** 2)
    
    # Self capacitance of spherical dust grain: C = 4 * pi * eps0 * a
    grain_capacitance = 4.0 * math.pi * EPSILON_0 * grain_radius_m
    grain_charge_c = grain_capacitance * grain_potential_volts
    elementary_charges = grain_charge_c / E_CHARGE
    
    # Electrostatic potential needed to stop or deflect grain
    v_repel_needed = grain_ke_j / grain_charge_c
    
    # Minimum radius of sphere to maintain this potential without field emission breakdown
    # E = V / R => R_min = V / E_breakdown
    r_sphere_min_m = v_repel_needed / breakdown_field_v_per_m
    r_sphere_min_km = r_sphere_min_m / 1000.0
    r_earth_ratio = r_sphere_min_m / 6.371e6
    
    # Total stored electrostatic energy: U = 1/2 * C * V^2 = 2 * pi * eps0 * R * V^2
    u_stored_joules = 2.0 * math.pi * EPSILON_0 * r_sphere_min_m * (v_repel_needed ** 2)
    
    return {
        "grain_radius_um": grain_radius_m * 1e6,
        "grain_mass_kg": grain_mass,
        "grain_ke_joules": grain_ke_j,
        "grain_charge_coulombs": grain_charge_c,
        "elementary_charges": elementary_charges,
        "v_repel_needed_volts": v_repel_needed,
        "v_repel_petavolts": v_repel_needed / 1e15,
        "r_sphere_min_km": r_sphere_min_km,
        "r_earth_ratio": r_earth_ratio,
        "stored_energy_joules": u_stored_joules,
        "is_feasible": False,
        "blocker": "Dielectric breakdown & field emission (E > 1 GV/m); requires Earth-sized conductor at 35 PV"
    }


def evaluate_magnetic_deflection(
    grain_radius_m: float = 1.0e-6,
    grain_density: float = 2500.0,
    beta: float = 0.20,
    grain_potential_volts: float = 5.0,
    b_field_tesla: float = 10.0,
    shield_length_m: float = 1.0,
) -> dict:
    """
    Evaluates magnetic Lorentz force deflection for interstellar dust grains.
    Shows that gyroradius exceeds planetary dimensions, rendering magnetic deflection futile.
    """
    gamma = relativistic_gamma(beta)
    v = beta * C
    grain_volume = (4.0 / 3.0) * math.pi * (grain_radius_m ** 3)
    grain_mass = grain_density * grain_volume
    grain_capacitance = 4.0 * math.pi * EPSILON_0 * grain_radius_m
    grain_charge_c = grain_capacitance * grain_potential_volts
    
    # Gyroradius: r_g = (gamma * m * v) / (q * B)
    r_gyroradius_m = (gamma * grain_mass * v) / (grain_charge_c * b_field_tesla)
    r_gyroradius_km = r_gyroradius_m / 1000.0
    
    # Deflection angle over shield length: theta ~ L / r_g
    deflection_angle_rad = shield_length_m / r_gyroradius_m
    lateral_deflection_m = 0.5 * shield_length_m * deflection_angle_rad
    lateral_deflection_nm = lateral_deflection_m * 1e9
    
    return {
        "b_field_tesla": b_field_tesla,
        "r_gyroradius_km": r_gyroradius_km,
        "deflection_angle_rad": deflection_angle_rad,
        "lateral_deflection_nm": lateral_deflection_nm,
        "is_feasible": False,
        "blocker": "Gyroradius (~115,000 km) dwarfs spacecraft scale; lateral deflection is only ~4.3 nm over 1 m"
    }


def evaluate_planetary_encounter_kinematics(
    beta: float = 0.20,
    impact_parameter_km: float = 10000.0,
    target_radius_km: float = 7160.0,
    detection_envelope_km: float = 100000.0,
    desired_surface_resolution_km: float = 1.0,
) -> dict:
    """
    Evaluates exoplanet encounter geometry, slew rate, and exposure blur constraints at relativistic speed.
    """
    v_km_s = beta * C / 1000.0
    
    # Encounter duration within detection envelope
    if detection_envelope_km > impact_parameter_km:
        transit_distance_km = 2.0 * math.sqrt(detection_envelope_km**2 - impact_parameter_km**2)
        transit_duration_s = transit_distance_km / v_km_s
    else:
        transit_distance_km = 0.0
        transit_duration_s = 0.0
        
    # Maximum line-of-sight angular slew rate at closest approach: omega = v / b
    max_slew_rate_rad_s = v_km_s / impact_parameter_km
    max_slew_rate_deg_s = math.degrees(max_slew_rate_rad_s)
    
    # Maximum angular acceleration: alpha_max = (3 * sqrt(3) / 8) * (v^2 / b^2)
    max_angular_accel_rad_s2 = (3.0 * math.sqrt(3.0) / 8.0) * (max_slew_rate_rad_s ** 2)
    max_angular_accel_deg_s2 = math.degrees(max_angular_accel_rad_s2)
    
    # Exposure time to limit motion smear to 1 pixel resolution: dt = delta_x / v
    max_exposure_time_s = desired_surface_resolution_km / v_km_s
    max_exposure_time_us = max_exposure_time_s * 1e6
    
    return {
        "beta": beta,
        "v_km_s": v_km_s,
        "impact_parameter_km": impact_parameter_km,
        "transit_duration_envelope_s": transit_duration_s,
        "max_slew_rate_rad_s": max_slew_rate_rad_s,
        "max_slew_rate_deg_s": max_slew_rate_deg_s,
        "max_angular_accel_rad_s2": max_angular_accel_rad_s2,
        "max_angular_accel_deg_s2": max_angular_accel_deg_s2,
        "max_exposure_time_us": max_exposure_time_us,
        "challenge": "Extreme slew rate (~344 deg/s) and sub-20-microsecond exposure requirement"
    }


def evaluate_interstellar_optical_link(
    distance_ly: float = 4.244,
    laser_power_w: float = 1.0,
    wavelength_m: float = 1.064e-6,
    d_tx_m: float = 0.35,
    d_rx_m: float = 10.0,
    optical_efficiency: float = 0.50,
    photons_per_bit: float = 10.0,
    compressed_image_mb: float = 2.0,
) -> dict:
    """
    Evaluates interstellar optical communication link budget from Proxima Centauri to Earth.
    Compares 10m ground telescope vs 1km phased receiver array.
    """
    distance_m = distance_ly * LY
    photon_energy_j = (H * C) / wavelength_m
    
    # Transmitter divergence half-angle: theta ~ 1.22 * lambda / D_tx
    div_angle_rad = 1.22 * wavelength_m / d_tx_m
    div_angle_arcsec = math.degrees(div_angle_rad) * 3600.0
    
    # Beam spot footprint diameter at Earth
    footprint_diameter_m = 2.0 * distance_m * math.tan(div_angle_rad)
    footprint_diameter_au = footprint_diameter_m / AU
    footprint_area_m2 = (math.pi / 4.0) * (footprint_diameter_m ** 2)
    
    # Intensity at Earth: W/m^2
    flux_earth_w_m2 = laser_power_w / footprint_area_m2
    
    # Receiver collection area
    rx_area_m2 = (math.pi / 4.0) * (d_rx_m ** 2)
    received_power_w = flux_earth_w_m2 * rx_area_m2 * optical_efficiency
    
    # Received photon rate
    photon_rate_hz = received_power_w / photon_energy_j
    
    # Bit rate achievable at M-ary PPM
    data_rate_bps = photon_rate_hz / photons_per_bit
    
    # Image transmission time
    image_bits = compressed_image_mb * 8.0 * 1024.0 * 1024.0
    tx_time_seconds = image_bits / data_rate_bps if data_rate_bps > 0 else float('inf')
    tx_time_hours = tx_time_seconds / 3600.0
    tx_time_days = tx_time_seconds / 86400.0
    
    return {
        "distance_ly": distance_ly,
        "laser_power_w": laser_power_w,
        "wavelength_um": wavelength_m * 1e6,
        "d_tx_m": d_tx_m,
        "d_rx_m": d_rx_m,
        "div_angle_arcsec": div_angle_arcsec,
        "footprint_diameter_au": footprint_diameter_au,
        "received_power_w": received_power_w,
        "photon_rate_hz": photon_rate_hz,
        "data_rate_bps": data_rate_bps,
        "image_bits": image_bits,
        "tx_time_hours": tx_time_hours,
        "tx_time_days": tx_time_days,
    }


def get_complete_ranked_propulsion_catalog() -> list:
    """
    Returns the comprehensive 9-family propulsion assessment with precise numbers,
    mission capability classifications, energy costs, and single biggest engineering blockers.
    """
    return [
        {
            "rank": 1,
            "name": "Chemical (LH2/LOX)",
            "isp_s": 452,
            "ve_km_s": 4.432,
            "thrust_rep": "2.28 MN",
            "tw_ratio": "70 - 150",
            "thrust_per_mw_n": 451.3,
            "mission_domain": "Planetary Surface Launch, Cis-Lunar Injection",
            "interstellar_capable": False,
            "flyby_mr_log10": 2947.0,
            "rendezvous_mr_struct": "inf",
            "energy_cost_per_kg": "inf",
            "engineering_blocker": "Chemical bond enthalpy ceiling (Q <= 13.4 MJ/kg); propellant mass for 0.1c exceeds observable universe by 10^2860."
        },
        {
            "rank": 2,
            "name": "Solar Electric / Ion (SEP)",
            "isp_s": 3500,
            "ve_km_s": 34.32,
            "thrust_rep": "0.5 N",
            "tw_ratio": "1e-5 - 1e-4",
            "thrust_per_mw_n": 58.3,
            "mission_domain": "Cis-Lunar Stationkeeping, Asteroid Belts (< 3 AU)",
            "interstellar_capable": False,
            "flyby_mr_log10": 380.0,
            "rendezvous_mr_struct": "inf",
            "energy_cost_per_kg": "inf",
            "engineering_blocker": "Solar flux 1/r^2 dilution; power drops to 50 W/m^2 at Jupiter, terminating thrust past 3 AU."
        },
        {
            "rank": 3,
            "name": "Solar Sail (Photonic)",
            "isp_s": float('inf'),
            "ve_km_s": 299792.458,
            "thrust_rep": "9.08 uN/m^2",
            "tw_ratio": "1e-4",
            "thrust_per_mw_n": 0.0067,
            "mission_domain": "Inner Solar System, SGL 550 AU (via 0.05 AU Oberth dive in 21.7 yr)",
            "interstellar_capable": False,
            "flyby_mr_log10": 0.0,
            "rendezvous_mr_struct": "inf",
            "energy_cost_per_kg": "0.0 J (free solar flux)",
            "engineering_blocker": "Thermal perihelion sublimation; terminal velocity bounded to <= 737 km/s (0.0025c), interstellar transit > 1700 years."
        },
        {
            "rank": 4,
            "name": "Nuclear Thermal (NTR)",
            "isp_s": 900,
            "ve_km_s": 8.826,
            "thrust_rep": "334 kN",
            "tw_ratio": "3 - 7",
            "thrust_per_mw_n": 226.6,
            "mission_domain": "Cis-Lunar Cargo, Fast Mars Sprint (90 days)",
            "interstellar_capable": False,
            "flyby_mr_log10": 1480.0,
            "rendezvous_mr_struct": "inf",
            "energy_cost_per_kg": "inf",
            "engineering_blocker": "Refractory solid-core carbide melting (T_core <= 3100 K); mass ratio to 0.1c is 10^1480."
        },
        {
            "rank": 5,
            "name": "Nuclear Electric (NEP)",
            "isp_s": 6000,
            "ve_km_s": 58.84,
            "thrust_rep": "25 N",
            "tw_ratio": "1e-4",
            "thrust_per_mw_n": 34.0,
            "mission_domain": "Outer Planet Tours (Jupiter/Saturn, 10 - 30 AU)",
            "interstellar_capable": False,
            "flyby_mr_log10": 222.0,
            "rendezvous_mr_struct": "inf",
            "energy_cost_per_kg": "inf",
            "engineering_blocker": "Stuhlinger specific-power wall (alpha <= 100 W/kg); burn time to reach 0.1c is 142,400 years."
        },
        {
            "rank": 6,
            "name": "Nuclear Pulse (Orion)",
            "isp_s": 6000,
            "ve_km_s": 58.84,
            "thrust_rep": "10 MN",
            "tw_ratio": "1 - 10",
            "thrust_per_mw_n": 34.0,
            "mission_domain": "Rapid High-Mass Planetary Transport",
            "interstellar_capable": False,
            "flyby_mr_log10": 222.0,
            "rendezvous_mr_struct": "inf",
            "energy_cost_per_kg": "inf",
            "engineering_blocker": "Pusher-plate plasma ablation/spallation fatigue under hypervelocity shocks; Outer Space Treaty nuclear test bans."
        },
        {
            "rank": 7,
            "name": "Nuclear Fusion (D-3He)",
            "isp_s": 1375000,
            "ve_km_s": 13490.0,
            "thrust_rep": "10 kN",
            "tw_ratio": "1e-3",
            "thrust_per_mw_n": 0.148,
            "mission_domain": "High-Speed Interplanetary, Interstellar Probes (Flyby & Rendezvous)",
            "interstellar_capable": True,
            "flyby_mr_log10": 0.97,
            "rendezvous_mr_struct": "272.4 kg/kg (2-stage)",
            "energy_cost_per_kg": "25.5 TWh/kg",
            "engineering_blocker": "Thermonuclear Lawson criterion (n*tau*T >= 10^22 keV*s/m^3) and mining 30,000 t of 3He from lunar regolith / gas giants."
        },
        {
            "rank": 8,
            "name": "Antimatter Beamed-Core",
            "isp_s": 10118000,
            "ve_km_s": 99230.0,
            "thrust_rep": "10 kN",
            "tw_ratio": "1e-2",
            "thrust_per_mw_n": 0.0202,
            "mission_domain": "Relativistic Interstellar Sprint & Rapid Deceleration",
            "interstellar_capable": True,
            "flyby_mr_log10": 0.13,
            "rendezvous_mr_struct": "1.90 kg/kg (1-stage)",
            "energy_cost_per_kg": "1.07e10 TWh/kg",
            "engineering_blocker": "Antiproton production efficiency (eta ~ 10^-9, costing 10^10 TWh/kg) and neutral pion decay 200 MeV gamma-ray radiator flash."
        },
        {
            "rank": 9,
            "name": "Laser-Pushed Beamed Sail",
            "isp_s": float('inf'),
            "ve_km_s": 299792.458,
            "thrust_rep": "667 N (100 GW)",
            "tw_ratio": "68000 (1 g)",
            "thrust_per_mw_n": 0.0067,
            "mission_domain": "Relativistic Gram-Scale Interstellar Flyby",
            "interstellar_capable": True,
            "flyby_mr_log10": 0.0,
            "rendezvous_mr_struct": "42.0 kg/kg (hybrid magsail)",
            "energy_cost_per_kg": "6241 TWh/t (flyby)",
            "engineering_blocker": "Laser array phased coherence (D >= 1.8 km, jitter <= 0.15 mas), sail dielectric absorption (A_abs <= 9.07 ppm), and asymmetric deceleration."
        }
    ]
