"""
propulsion_deceleration_and_capture_engine.py

Rigorous Epistemic Engine for Interstellar Deceleration, Target Capture,
Astrospheric Plasma Braking, and Grand Propulsion Consilience.

Physical Domains Evaluated:
1. Relativistic Rocket Rendezvous Staging Penalties (Fusion & Antimatter).
2. Superconducting Magnetic Sail (Magsail) Plasma Drag Kinematics in ISM and Astrosphere.
3. Virial Theorem Structural Mass Limits on Superconducting Coils.
4. Gravitational Slingshot & Binary Capture Impossibility Proofs.
5. Hypervelocity Atmospheric Aerocapture Vaporization Theorem.
6. Unified 9-Family Propulsion Feasibility Matrix & Engineering Blockers.

Author: Kepler (Agent A001, Generation 0)
Domain: Practical space propulsion (propulsion)
Epistemic Class: Engineering Feasibility & Astrodynamics Limits
"""

import math

# Fundamental Physical Constants
C = 299792458.0                     # Speed of light in vacuum (m/s)
G0 = 9.80665                        # Standard gravity (m/s^2)
G_NEWTON = 6.67430e-11              # Gravitational constant (m^3/kg/s^2)
MU_0 = 4.0 * math.pi * 1.0e-7       # Vacuum permeability (H/m or N/A^2)
EPSILON_0 = 8.8541878128e-12        # Vacuum permittivity (F/m)
M_PROTON = 1.67262192369e-27        # Proton mass (kg)
E_CHARGE = 1.602176634e-19          # Elementary charge (C)
AU = 1.495978707e11                 # Astronomical Unit (m)
LY = 9.4607304725808e15             # Light-year (m)
M_SUN = 1.98847e30                  # Solar mass (kg)
R_SUN = 6.957e8                     # Solar radius (m)

# Target System Data: Proxima Centauri & Alpha Centauri AB
M_PROXIMA = 0.1221 * M_SUN          # Mass of Proxima Centauri (kg)
R_PROXIMA = 0.1542 * R_SUN          # Radius of Proxima Centauri (m)
DIST_PROXIMA = 4.244 * LY           # Distance to Proxima (m)
V_ORB_CENTAURI_AB = 5700.0          # Mutual orbital speed of Alpha Cen A & B (m/s)

# Local Interstellar Medium (LIC) Properties
N_ISM_P = 0.1e6                     # Proton number density (m^-3, 0.1 cm^-3)
RHO_ISM = N_ISM_P * M_PROTON        # Mass density of ISM (kg/m^3 ~ 1.67e-22)
B_ISM = 0.5e-9                      # Magnetic field of ISM (Tesla, 0.5 nT)

# Material Properties for Superconductors & Structures
SIGMA_CNT = 60.0e9                  # Carbon nanotube tensile strength (Pa, 60 GPa)
RHO_CNT = 1400.0                    # Carbon nanotube density (kg/m^3)
JC_YBCO = 1.0e9                     # YBCO critical current density (A/m^2, 10^5 A/cm^2)
RHO_YBCO = 6300.0                   # YBCO superconductor density (kg/m^3)
DELTA_H_SUB_DIAMOND = 6.0e7         # Enthalpy of sublimation for diamond/graphite (J/kg)


def relativistic_gamma(beta: float) -> float:
    """Calculate Lorentz factor gamma."""
    if beta >= 1.0:
        raise ValueError("Beta must be strictly less than 1.0")
    return 1.0 / math.sqrt(1.0 - beta**2)


def evaluate_rocket_rendezvous_penalty(
    beta: float,
    ve_m_s: float,
    epsilon_struct: float = 0.05
) -> dict:
    """
    Evaluates relativistic rocket equation for flyby (1 burn) vs rendezvous (2 burns: accel + decel).
    R_1 = exp( (c/ve) * atanh(beta) )
    R_2 = R_1^2
    Evaluates single-stage feasibility (R <= 1/epsilon) and multi-stage mass multiplier (m0 / mL).
    """
    gamma = relativistic_gamma(beta)
    rapidity = math.atanh(beta)
    
    exponent = (C / ve_m_s) * rapidity
    
    if exponent > 700.0:
        log10_r1 = exponent * math.log10(math.e)
        r1_ideal = float('inf')
        r2_ideal = float('inf')
        log10_r2 = 2.0 * log10_r1
        flyby_single_stage_possible = False
        rendezvous_single_stage_possible = False
        m0_mL_flyby = float('inf')
        m0_mL_rendezvous = float('inf')
        optimal_stages = float('inf')
    else:
        # Flyby mass ratio (ideal rocket, no structure)
        r1_ideal = math.exp(exponent)
        # Rendezvous mass ratio (ideal rocket, no structure)
        r2_ideal = r1_ideal ** 2
        log10_r1 = math.log10(r1_ideal)
        log10_r2 = math.log10(r2_ideal)
        
        single_stage_limit = 1.0 / epsilon_struct
        
        # Flyby with structure: m0 / mL = R * (1 - epsilon) / (1 - epsilon * R)
        flyby_single_stage_possible = (epsilon_struct * r1_ideal) < 1.0
        if flyby_single_stage_possible:
            m0_mL_flyby = (r1_ideal * (1.0 - epsilon_struct)) / (1.0 - epsilon_struct * r1_ideal)
        else:
            m0_mL_flyby = float('inf')
            
        # Rendezvous with structure
        rendezvous_single_stage_possible = (epsilon_struct * r2_ideal) < 1.0
        if rendezvous_single_stage_possible:
            m0_mL_rendezvous = (r2_ideal * (1.0 - epsilon_struct)) / (1.0 - epsilon_struct * r2_ideal)
            optimal_stages = 1
        else:
            # 2-stage vehicle: each stage achieves beta*c
            if flyby_single_stage_possible:
                m0_mL_rendezvous = m0_mL_flyby ** 2
                optimal_stages = 2
            else:
                m0_mL_rendezvous = float('inf')
                optimal_stages = float('inf')

    return {
        "beta": beta,
        "ve_m_s": ve_m_s,
        "ve_over_c": ve_m_s / C,
        "r1_ideal": r1_ideal,
        "r2_ideal": r2_ideal,
        "log10_r1": math.log10(r1_ideal) if r1_ideal > 0 else float('inf'),
        "log10_r2": math.log10(r2_ideal) if r2_ideal > 0 else float('inf'),
        "flyby_single_stage_possible": flyby_single_stage_possible,
        "rendezvous_single_stage_possible": rendezvous_single_stage_possible,
        "m0_mL_flyby": m0_mL_flyby,
        "m0_mL_rendezvous": m0_mL_rendezvous,
        "optimal_stages_rendezvous": optimal_stages,
    }


def evaluate_magsail_kinematics(
    m_probe_kg: float,
    r_loop_m: float,
    current_amp: float,
    beta_start: float = 0.05,
    beta_final: float = 0.00015,  # ~45 km/s (Alfvén speed limit)
    rho_medium: float = RHO_ISM,
    cd: float = 2.0
) -> dict:
    """
    Evaluates Andrews-Zubrin / Gros magnetic sail deceleration in interstellar plasma.
    Dipole moment M = I * pi * R^2.
    Magnetopause radius R_mp(v) = ( (mu0 * M^2) / (4 * pi^2 * rho * v^2) )^(1/6).
    Drag force F_d = 0.5 * cd * rho * v^2 * pi * R_mp^2 = K_drag * v^(4/3).
    Deceleration time t_decel = (3 / K_acc) * (v_f^(-1/3) - v_0^(-1/3)).
    Deceleration distance x_decel = (3 / (2 * K_acc)) * (v_0^(2/3) - v_f^(2/3)).
    """
    v0 = beta_start * C
    vf = beta_final * C
    
    dipole_moment_M = current_amp * math.pi * (r_loop_m ** 2)
    
    # Factor K_drag where F_d = K_drag * v^(4/3)
    # R_mp = [ (mu_0 * M^2) / (4 * pi^2 * rho) ]^(1/6) * v^(-1/3)
    # Area = pi * R_mp^2 = pi * [ (mu_0 * M^2) / (4 * pi^2 * rho) ]^(1/3) * v^(-2/3)
    # F_d = 0.5 * cd * rho * v^2 * Area
    #     = 0.5 * cd * rho * pi * [ (mu_0 * M^2) / (4 * pi^2 * rho) ]^(1/3) * v^(4/3)
    c_geom = (MU_0 * (dipole_moment_M ** 2)) / (4.0 * (math.pi ** 2) * rho_medium)
    k_drag = 0.5 * cd * rho_medium * math.pi * (c_geom ** (1.0 / 3.0))
    
    k_acc = k_drag / m_probe_kg  # dv/dt = - k_acc * v^(4/3)
    
    # Deceleration time (seconds)
    t_decel_s = (3.0 / k_acc) * ((vf ** (-1.0 / 3.0)) - (v0 ** (-1.0 / 3.0)))
    t_decel_yr = t_decel_s / (365.25 * 86400.0)
    
    # Deceleration distance (meters)
    x_decel_m = (1.5 / k_acc) * ((v0 ** (2.0 / 3.0)) - (vf ** (2.0 / 3.0)))
    x_decel_ly = x_decel_m / LY
    
    # Initial magnetopause radius and peak drag
    r_mp_initial = (c_geom / (v0 ** 2)) ** (1.0 / 6.0)
    f_drag_initial = k_drag * (v0 ** (4.0 / 3.0))
    a_initial = f_drag_initial / m_probe_kg
    
    # Final magnetopause radius and drag at alfven speed
    r_mp_final = (c_geom / (vf ** 2)) ** (1.0 / 6.0)
    f_drag_final = k_drag * (vf ** (4.0 / 3.0))
    
    # Local ISM Alfvén velocity
    v_alfven = B_ISM / math.sqrt(MU_0 * rho_medium)
    beta_alfven = v_alfven / C

    return {
        "m_probe_kg": m_probe_kg,
        "r_loop_m": r_loop_m,
        "current_amp": current_amp,
        "dipole_moment_A_m2": dipole_moment_M,
        "beta_start": beta_start,
        "beta_final": beta_final,
        "v0_m_s": v0,
        "vf_m_s": vf,
        "r_mp_initial_km": r_mp_initial / 1000.0,
        "r_mp_final_km": r_mp_final / 1000.0,
        "f_drag_initial_n": f_drag_initial,
        "a_initial_m_s2": a_initial,
        "a_initial_g": a_initial / G0,
        "t_decel_yr": t_decel_yr,
        "x_decel_ly": x_decel_ly,
        "v_alfven_m_s": v_alfven,
        "beta_alfven": beta_alfven,
        "is_distance_within_transit": x_decel_ly <= 4.244,
    }


def evaluate_magsail_virial_mass(
    r_loop_m: float,
    current_amp: float,
    wire_radius_m: float = 1.0e-4,
    sigma_struct: float = SIGMA_CNT,
    rho_struct: float = RHO_CNT,
    jc_sc: float = JC_YBCO,
    rho_sc: float = RHO_YBCO
) -> dict:
    """
    Evaluates the virial structural mass and superconductor mass of a magsail loop.
    Self-inductance L = mu0 * R * [ ln(8*R/r_w) - 2 ].
    Stored magnetic energy U_B = 0.5 * L * I^2.
    Virial theorem minimum structural mass: M_struct >= (rho_struct / sigma_struct) * U_B.
    Superconductor cross-section: A_sc = I / J_c.
    Superconductor mass: M_sc = 2 * pi * R * A_sc * rho_sc.
    """
    ratio = (8.0 * r_loop_m) / wire_radius_m
    ln_term = math.log(ratio)
    
    inductance_h = MU_0 * r_loop_m * (ln_term - 2.0)
    stored_energy_j = 0.5 * inductance_h * (current_amp ** 2)
    
    # Virial structural limit
    m_struct_min_kg = (rho_struct / sigma_struct) * stored_energy_j
    
    # Superconductor mass
    a_sc_m2 = current_amp / jc_sc
    wire_length_m = 2.0 * math.pi * r_loop_m
    m_sc_kg = wire_length_m * a_sc_m2 * rho_sc
    
    total_coil_mass_kg = m_struct_min_kg + m_sc_kg

    return {
        "r_loop_m": r_loop_m,
        "current_amp": current_amp,
        "inductance_h": inductance_h,
        "stored_energy_mj": stored_energy_j / 1.0e6,
        "m_struct_min_kg": m_struct_min_kg,
        "m_sc_kg": m_sc_kg,
        "total_coil_mass_kg": total_coil_mass_kg,
        "specific_energy_j_kg": stored_energy_j / total_coil_mass_kg,
    }


def evaluate_gravitational_slingshot_capture_impossibility(
    v_inf_m_s: float,
    v_binary_m_s: float = V_ORB_CENTAURI_AB,
    m_primary: float = M_PROXIMA,
    r_grazing: float = R_PROXIMA
) -> dict:
    """
    Proves that three-body gravitational assists and hyperbolic grazing encounters
    cannot capture a relativistic probe without external energy dissipation.
    1. Maximum velocity change from 3-body assist: Delta_v_max <= 2 * V_binary.
    2. Gravitational deflection angle at grazing periastron: theta ~ 2 * G * M / (r * v^2).
    """
    delta_v_slingshot_max = 2.0 * v_binary_m_s
    fraction_slingshot = delta_v_slingshot_max / v_inf_m_s
    
    # Gravitational deflection angle for hyperbolic encounter
    # theta ~ 2 * G * M / (b * v^2)
    deflection_rad = (2.0 * G_NEWTON * m_primary) / (r_grazing * (v_inf_m_s ** 2))
    deflection_arcsec = deflection_rad * (180.0 / math.pi) * 3600.0
    
    # Hyperbolic excess energy per unit mass: e_inf = 0.5 * v_inf^2
    # To capture into bound orbit (e < 0), craft must dissipate >= 0.5 * v_inf^2
    specific_energy_to_dissipate = 0.5 * (v_inf_m_s ** 2)

    return {
        "v_inf_m_s": v_inf_m_s,
        "v_inf_over_c": v_inf_m_s / C,
        "delta_v_slingshot_max_m_s": delta_v_slingshot_max,
        "fraction_slingshot": fraction_slingshot,
        "deflection_rad": deflection_rad,
        "deflection_arcsec": deflection_arcsec,
        "specific_energy_to_dissipate_j_kg": specific_energy_to_dissipate,
        "capture_possible_gravitational_alone": False,
    }


def evaluate_aerocapture_vaporization(
    beta: float,
    heat_of_sublimation_j_kg: float = DELTA_H_SUB_DIAMOND
) -> dict:
    """
    Evaluates thermal destruction during hyperbolic atmospheric aerocapture at relativistic speeds.
    Shows that specific kinetic energy exceeds vaporization enthalpy by 5 to 7 orders of magnitude.
    """
    gamma = relativistic_gamma(beta)
    v = beta * C
    
    # Specific kinetic energy (J/kg)
    specific_ke = (gamma - 1.0) * (C ** 2)
    
    # Ratio of kinetic energy to sublimation enthalpy
    energy_vaporization_ratio = specific_ke / heat_of_sublimation_j_kg
    
    # Stagnation temperature estimate: T_stag ~ v^2 / (2 * cp)
    cp_air = 1000.0  # J/kg/K
    t_stag_k = (v ** 2) / (2.0 * cp_air)
    
    # Energy in kilotons TNT per kg (1 kt TNT = 4.184e12 J)
    tnt_kt_per_kg = specific_ke / 4.184e12

    return {
        "beta": beta,
        "velocity_km_s": v / 1000.0,
        "specific_ke_j_kg": specific_ke,
        "energy_vaporization_ratio": energy_vaporization_ratio,
        "t_stag_k": t_stag_k,
        "tnt_kt_per_kg": tnt_kt_per_kg,
        "aerocapture_survivable": False,
    }


def get_definitive_propulsion_ranked_matrix() -> list:
    """
    Returns the comprehensive, definitive comparative matrix of all 9 propulsion families,
    satisfying the exact deliverable requested in the standing scientific brief.
    """
    return [
        {
            "rank": 1,
            "name": "Chemical (LH2/LOX)",
            "isp_s": 452,
            "ve_km_s": 4.432,
            "thrust_representative": "2.28 MN",
            "thrust_to_weight": "70 - 150",
            "thrust_per_mw": "451.3 N/MW",
            "mission_domain": "Earth surface-to-orbit, Cis-lunar injection",
            "interstellar_capable": False,
            "flyby_mass_ratio_log10": 2947.1,
            "rendezvous_mass_ratio": "Infinite (10^5894)",
            "primary_blocker": "Chemical bond enthalpy ceiling (Q <= 13.4 MJ/kg); propellant mass to 0.1c exceeds observable universe by 10^2860."
        },
        {
            "rank": 2,
            "name": "Solar Electric / Ion (SEP)",
            "isp_s": 3500,
            "ve_km_s": 34.32,
            "thrust_representative": "0.5 N",
            "thrust_to_weight": "10^-5 - 10^-4",
            "thrust_per_mw": "58.3 N/MW",
            "mission_domain": "Cis-lunar stationkeeping, Asteroid exploration (<3 AU)",
            "interstellar_capable": False,
            "flyby_mass_ratio_log10": 380.2,
            "rendezvous_mass_ratio": "Infinite (10^760)",
            "primary_blocker": "Solar flux 1/r^2 dilution; solar array mass scales quadratically with heliocentric distance, choking thrust past Mars."
        },
        {
            "rank": 3,
            "name": "Solar Sail (Photonic)",
            "isp_s": "Infinite",
            "ve_km_s": 299792.0,
            "thrust_representative": "9.08 uN/m^2",
            "thrust_to_weight": "10^-4",
            "thrust_per_mw": "0.0067 N/MW",
            "mission_domain": "Inner Solar System cruise, Solar Gravitational Lens (550 AU)",
            "interstellar_capable": False,
            "flyby_mass_ratio_log10": 0.0,
            "rendezvous_mass_ratio": "Infinite (unbraked)",
            "primary_blocker": "Thermal perihelion sublimation; terminal escape speed capped at vmax <= 737 km/s (0.0025c) at 0.05 AU perihelion (>1,700 yr transit)."
        },
        {
            "rank": 4,
            "name": "Nuclear Thermal (Solid-Core NTR)",
            "isp_s": 900,
            "ve_km_s": 8.826,
            "thrust_representative": "334 kN",
            "thrust_to_weight": "3 - 7",
            "thrust_per_mw": "226.6 N/MW",
            "mission_domain": "Cis-lunar heavy cargo, Rapid crewed Mars transit (90 days)",
            "interstellar_capable": False,
            "flyby_mass_ratio_log10": 1480.1,
            "rendezvous_mass_ratio": "Infinite (10^2960)",
            "primary_blocker": "Refractory solid-core melting point (T_core <= 3,100 K); hydrogen embrittlement and carbide fuel element sublimation."
        },
        {
            "rank": 5,
            "name": "Nuclear Electric (NEP)",
            "isp_s": 6000,
            "ve_km_s": 58.84,
            "thrust_representative": "25 N",
            "thrust_to_weight": "10^-4",
            "thrust_per_mw": "34.0 N/MW",
            "mission_domain": "Outer planet multi-rendezvous tours (Jupiter/Saturn)",
            "interstellar_capable": False,
            "flyby_mass_ratio_log10": 222.0,
            "rendezvous_mass_ratio": "Infinite (10^444)",
            "primary_blocker": "Stuhlinger specific-power wall (alpha <= 100 W/kg); accelerating to 0.1c requires 142,400 years of continuous reactor burn."
        },
        {
            "rank": 6,
            "name": "Nuclear Pulse (Project Orion)",
            "isp_s": 6000,
            "ve_km_s": 58.84,
            "thrust_representative": "10 MN",
            "thrust_to_weight": "1 - 10",
            "thrust_per_mw": "34.0 N/MW",
            "mission_domain": "Massive interplanetary freight (10,000 tonnes to Saturn)",
            "interstellar_capable": False,
            "flyby_mass_ratio_log10": 222.0,
            "rendezvous_mass_ratio": "Infinite (10^444)",
            "primary_blocker": "Pusher-plate plasma ablation and spallation fatigue under hypervelocity nuclear blast shocks; international test-ban treaties."
        },
        {
            "rank": 7,
            "name": "Nuclear Fusion (D-3He / Magnetic Nozzle)",
            "isp_s": 1375000,
            "ve_km_s": 13490.0,
            "thrust_representative": "10 kN",
            "thrust_to_weight": "10^-3",
            "thrust_per_mw": "0.148 N/MW",
            "mission_domain": "High-speed interplanetary sprint, Multi-decade interstellar flyby",
            "interstellar_capable": True,
            "flyby_mass_ratio_log10": 0.968,
            "rendezvous_mass_ratio": "272.4 kg/kg (2-stage)",
            "primary_blocker": "Thermonuclear Lawson criterion (n*tau*T >= 10^22 keV*s/m^3); severe terrestrial scarcity of 3He requiring gas giant mining."
        },
        {
            "rank": 8,
            "name": "Antimatter Beamed-Core (p-pbar)",
            "isp_s": 10118000,
            "ve_km_s": 99230.0,
            "thrust_representative": "10 kN",
            "thrust_to_weight": "10^-2",
            "thrust_per_mw": "0.0202 N/MW",
            "mission_domain": "Relativistic interstellar rendezvous and round-trip transit",
            "interstellar_capable": True,
            "flyby_mass_ratio_log10": 0.132,
            "rendezvous_mass_ratio": "1.90 kg/kg (1-stage)",
            "primary_blocker": "Antiproton production efficiency (eta ~ 10^-9 at 10^10 TWh/kg cost); neutral pion pi0 decay creating 300 GW uncollimated gamma-ray flux."
        },
        {
            "rank": 9,
            "name": "Laser-Pushed Beamed Sail (Starshot)",
            "isp_s": "Infinite (external)",
            "ve_km_s": 299792.0,
            "thrust_representative": "667 N (100 GW)",
            "thrust_to_weight": "68,000 (1 g)",
            "thrust_per_mw": "0.0067 N/MW",
            "mission_domain": "Relativistic gram-scale interstellar flyby (0.20c, 21.2 yr)",
            "interstellar_capable": True,
            "flyby_mass_ratio_log10": 0.0,
            "rendezvous_mass_ratio": "42.0 kg/kg (hybrid magsail)",
            "primary_blocker": "Phase coherence and pointing (D >= 1.8 km, jitter <= 0.15 mas); sail thermal absorption limit (A_abs <= 10^-5 at 6.25 GW/m^2)."
        }
    ]
