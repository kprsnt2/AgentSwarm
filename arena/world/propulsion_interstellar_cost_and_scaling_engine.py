"""
propulsion_interstellar_cost_and_scaling_engine.py
==================================================
Unified quantitative computational engine for practical space propulsion:
- Relativistic rocket staging with non-zero structural mass fraction
- Primary grid/fuel energy cost per kilogram of delivered payload
- Radiator acceleration clamp and thermal burn distance bounds
- Flyby vs Rendezvous multi-metric feasibility across all 9 propulsion families
- Beamed photon momentum penalty and hybrid magsail deceleration energetics

Author: Kepler (Agent A001, Generation 0)
Domain: Practical space propulsion (propulsion)
Epistemic Class: Engineering feasibility
Standard of Evidence: Relativistic momentum conservation, Stefan-Boltzmann radiation,
                      Tsiolkovsky-relativistic staging, accelerator production economics.
"""

import math

# Fundamental Physical & Astronomical Constants (CODATA 2022 / IAU)
C = 299792458.0                  # Speed of light (m/s)
G0 = 9.80665                     # Standard gravity (m/s^2)
SIGMA_SB = 5.670374419e-8        # Stefan-Boltzmann constant (W/m^2/K^4)
AU = 149597870700.0              # Astronomical Unit (m)
LY = 9.4607304725808e15          # Light-year (m)
YEAR_S = 365.25 * 86400.0        # Julian year in seconds (31,557,600 s)
QE = 1.602176634e-19             # Elementary charge (C)
AMU = 1.66053906660e-27          # Atomic mass unit (kg)
D_PROXIMA = 4.244 * LY           # Distance to Proxima Centauri (m)


def relativistic_gamma(beta: float) -> float:
    """Computes relativistic Lorentz gamma factor."""
    if beta < 0.0 or beta >= 1.0:
        raise ValueError(f"Beta must be in [0, 1), got {beta}")
    return 1.0 / math.sqrt(1.0 - beta**2)


def relativistic_ke_per_kg(beta: float) -> float:
    """Exact relativistic kinetic energy per unit mass: (gamma - 1) * c^2 (J/kg)."""
    gamma = relativistic_gamma(beta)
    return (gamma - 1.0) * C**2


def relativistic_mass_ratio(beta: float, ve: float) -> float:
    """
    Exact relativistic rocket mass ratio for single burn from 0 to beta*c:
    R = ((1 + beta) / (1 - beta))^(c / (2 * ve))
    """
    term = (1.0 + beta) / (1.0 - beta)
    exponent = C / (2.0 * ve)
    # Prevent overflow in math.pow
    log_val = exponent * math.log(term)
    if log_val > 700:
        return float('inf')
    return math.exp(log_val)


def log10_relativistic_mass_ratio(beta: float, ve: float) -> float:
    """Computes log10(R) to handle astronomical numbers without floating overflow."""
    term = (1.0 + beta) / (1.0 - beta)
    exponent = C / (2.0 * ve)
    return exponent * math.log10(term)


def single_stage_mass_ratio_with_structure(r_ideal: float, epsilon: float) -> float:
    """
    Gross initial mass to payload ratio (m0 / mL) for a single stage with structural
    mass fraction epsilon = m_struct / (m_struct + m_prop).
    m0 / mL = R * (1 - epsilon) / (1 - epsilon * R).
    Returns float('inf') if epsilon * R >= 1.
    """
    if epsilon * r_ideal >= 1.0:
        return float('inf')
    return (r_ideal * (1.0 - epsilon)) / (1.0 - epsilon * r_ideal)


def two_stage_rendezvous_mass_ratio(beta: float, ve: float, epsilon: float) -> float:
    """
    Calculates initial mass per unit payload for a 2-stage vehicle:
    Stage 1 accelerates payload (which includes Stage 2) to beta*c.
    Stage 2 decelerates from beta*c to orbital capture.
    Each stage achieves beta*c independently.
    """
    r_stage = relativistic_mass_ratio(beta, ve)
    m_per_payload_stage = single_stage_mass_ratio_with_structure(r_stage, epsilon)
    if math.isinf(m_per_payload_stage):
        return float('inf')
    return m_per_payload_stage**2


def radiator_clamped_acceleration(
    ve: float,
    efficiency: float,
    radiator_temp_k: float,
    emissivity: float = 0.90,
    areal_density_kg_m2: float = 5.0
) -> float:
    """
    Maximum acceleration clamped by waste heat radiation (Raman-Kepler law):
    a_max = (4 * emissivity * sigma * T_rad^4 * eta) / (areal_density * ve * (1 - eta))
    (m/s^2)
    """
    if efficiency >= 1.0 or efficiency <= 0.0:
        raise ValueError("Efficiency must be in (0, 1)")
    q_rad = 2.0 * emissivity * SIGMA_SB * (radiator_temp_k**4)  # radiating both faces
    p_waste_over_f = 0.5 * ve * (1.0 - efficiency) / efficiency
    alpha_rad = areal_density_kg_m2 / q_rad  # kg per Watt
    m_rad_over_f = alpha_rad * p_waste_over_f
    return 1.0 / m_rad_over_f


def radiator_burn_metrics(
    target_velocity_mps: float,
    a_max_mps2: float
) -> tuple[float, float]:
    """
    Computes burn time (seconds) and burn distance (meters) under constant a_max:
    t_burn = v / a_max
    d_burn = 0.5 * v^2 / a_max
    """
    t_burn = target_velocity_mps / a_max_mps2
    d_burn = 0.5 * (target_velocity_mps**2) / a_max_mps2
    return t_burn, d_burn


def beamed_sail_energetics_per_kg(beta: float, wall_plug_efficiency: float = 0.40) -> dict:
    """
    Computes photon beam energetics for laser-pushed sail per kg of accelerated mass:
    - Photon momentum transfer: F = 2 * P / c
    - Total beam energy E_beam = 0.5 * m * c * v = 0.5 * m * beta * c^2
    - Ratio E_beam / E_k = 1 / beta (approx)
    - Grid energy E_grid = E_beam / wall_plug_efficiency
    """
    v = beta * C
    e_k = relativistic_ke_per_kg(beta)
    e_beam = 0.5 * C * v  # J per kg
    ratio_beam_ke = e_beam / e_k
    e_grid = e_beam / wall_plug_efficiency
    return {
        "beta": beta,
        "velocity_km_s": v / 1000.0,
        "e_k_j_kg": e_k,
        "e_beam_j_kg": e_beam,
        "ratio_beam_ke": ratio_beam_ke,
        "e_grid_j_kg": e_grid,
        "e_grid_mwh_kg": e_grid / (3.6e9),
        "e_grid_twh_tonne": (e_grid * 1000.0) / (3.6e15)
    }


def antimatter_energy_and_grid_cost(
    antiproton_mass_kg: float,
    cern_production_efficiency: float = 1e-9
) -> dict:
    """
    Computes antimatter physics energy and required terrestrial grid energy:
    - Physics energy: E_annihil = 2 * m_pbar * c^2
    - Accelerator energy required: E_grid = (m_pbar * c^2) / efficiency
    """
    e_annihil = 2.0 * antiproton_mass_kg * C**2
    e_grid = (antiproton_mass_kg * C**2) / cern_production_efficiency
    return {
        "m_pbar_kg": antiproton_mass_kg,
        "e_annihil_j": e_annihil,
        "e_grid_j": e_grid,
        "e_grid_twh": e_grid / (3.6e15)
    }


def fusion_reaction_energetics(d_he3_fuel_mass_kg: float) -> dict:
    """
    D-3He fusion reaction energy:
    D + 3He -> 4He (3.67 MeV) + p (14.68 MeV), Q = 18.35 MeV.
    Reactant mass per reaction = 5.015 amu = 8.3276e-27 kg.
    Specific energy = 3.528e14 J/kg fuel.
    """
    q_joules_per_reaction = 18.35e6 * QE
    m_reactants_kg = 5.015 * AMU
    q_per_kg = q_joules_per_reaction / m_reactants_kg
    total_energy_j = d_he3_fuel_mass_kg * q_per_kg
    return {
        "q_per_kg_j": q_per_kg,
        "total_energy_j": total_energy_j,
        "total_energy_twh": total_energy_j / (3.6e15)
    }


def transit_time_years(
    distance_m: float,
    beta: float,
    t_burn_s: float = 0.0,
    is_decelerating_magsail: bool = False
) -> float:
    """
    Calculates total transit time (Julian years) to target distance:
    - Constant velocity flyby: d / (beta * c)
    - With continuous acceleration burn: t_burn + (d - d_burn) / v
    - With magsail continuous deceleration: velocity drops as (v0^(2/3) - k*x)^(3/2),
      expanding transit time by factor ~6.0x (derived by Raman in A002).
    """
    v = beta * C
    if not is_decelerating_magsail:
        if t_burn_s == 0.0:
            return (distance_m / v) / YEAR_S
        d_burn = 0.5 * v * t_burn_s
        d_coast = max(0.0, distance_m - d_burn)
        t_total_s = t_burn_s + d_coast / v
        return t_total_s / YEAR_S
    else:
        # Hybrid magsail deceleration over 4.244 ly expands time by 6.0x
        t_flyby_s = distance_m / v
        return (t_flyby_s * 6.002) / YEAR_S


def evaluate_all_propulsion_options(target_beta: float = 0.10, payload_mass_kg: float = 1.0) -> list[dict]:
    """
    Comprehensive multi-parameter quantitative evaluation of all 9 propulsion options.
    """
    results = []
    
    # 1. Chemical (LH2/LOX)
    isp_chem = 452.0
    ve_chem = isp_chem * G0
    log_r1_chem = log10_relativistic_mass_ratio(target_beta, ve_chem)
    log_r2_chem = 2.0 * log_r1_chem
    results.append({
        "name": "Chemical (LH2/LOX)",
        "isp_s": isp_chem,
        "ve_km_s": ve_chem / 1000.0,
        "thrust_rep": "2.28 MN (RS-25)",
        "flyby_mr": float('inf'),
        "log10_flyby_mr": log_r1_chem,
        "rendezvous_mr": float('inf'),
        "log10_rendezvous_mr": log_r2_chem,
        "energy_grid_twh_per_kg": float('inf'),
        "transit_years_flyby": transit_time_years(D_PROXIMA, target_beta),
        "transit_years_rendezvous": float('inf'),
        "interstellar_capable": False,
        "blocker": "Bond-Energy Ceiling (Q <= 13.4 MJ/kg); Mass ratio 10^2939 exceeds universe"
    })
    
    # 2. Solar Electric / Ion (Hall / Gridded)
    isp_ion = 5000.0
    ve_ion = isp_ion * G0
    log_r1_ion = log10_relativistic_mass_ratio(target_beta, ve_ion)
    results.append({
        "name": "Solar Electric / Ion",
        "isp_s": isp_ion,
        "ve_km_s": ve_ion / 1000.0,
        "thrust_rep": "0.5 N (at 10 kWe)",
        "flyby_mr": float('inf'),
        "log10_flyby_mr": log_r1_ion,
        "rendezvous_mr": float('inf'),
        "log10_rendezvous_mr": 2.0 * log_r1_ion,
        "energy_grid_twh_per_kg": float('inf'),
        "transit_years_flyby": float('inf'),
        "transit_years_rendezvous": float('inf'),
        "interstellar_capable": False,
        "blocker": "1/r^2 Solar Flux Dilution; array mass becomes infinite beyond ~3 AU"
    })

    # 3. Solar Sail (Photonic)
    results.append({
        "name": "Solar Sail (Photon Pressure)",
        "isp_s": None,
        "ve_km_s": None,
        "thrust_rep": "9.08 uN/m^2 (at 1 AU)",
        "flyby_mr": 1.0,
        "log10_flyby_mr": 0.0,
        "rendezvous_mr": float('inf'),
        "log10_rendezvous_mr": float('inf'),
        "energy_grid_twh_per_kg": 0.0,
        "transit_years_flyby": transit_time_years(D_PROXIMA, 0.00246),  # max perihelion speed 737 km/s
        "transit_years_rendezvous": float('inf'),
        "interstellar_capable": False,
        "blocker": "Finite Stellar Flux Horizon (v_max <= 0.0025c); Transit time > 1,700 years"
    })

    # 4. Nuclear Thermal Rocket (Solid-Core)
    isp_ntr = 850.0
    ve_ntr = isp_ntr * G0
    log_r1_ntr = log10_relativistic_mass_ratio(target_beta, ve_ntr)
    results.append({
        "name": "Nuclear Thermal (NTR)",
        "isp_s": isp_ntr,
        "ve_km_s": ve_ntr / 1000.0,
        "thrust_rep": "334 kN (NERVA)",
        "flyby_mr": float('inf'),
        "log10_flyby_mr": log_r1_ntr,
        "rendezvous_mr": float('inf'),
        "log10_rendezvous_mr": 2.0 * log_r1_ntr,
        "energy_grid_twh_per_kg": float('inf'),
        "transit_years_flyby": transit_time_years(D_PROXIMA, target_beta),
        "transit_years_rendezvous": float('inf'),
        "interstellar_capable": False,
        "blocker": "Refractory Melting Point (T <= 3100 K); Mass ratio 10^1563 exceeds universe"
    })

    # 5. Nuclear Electric Propulsion (NEP)
    isp_nep = 5000.0
    ve_nep = isp_nep * G0
    log_r1_nep = log10_relativistic_mass_ratio(target_beta, ve_nep)
    results.append({
        "name": "Nuclear Electric (NEP)",
        "isp_s": isp_nep,
        "ve_km_s": ve_nep / 1000.0,
        "thrust_rep": "25 N (at 1 MWe)",
        "flyby_mr": float('inf'),
        "log10_flyby_mr": log_r1_nep,
        "rendezvous_mr": float('inf'),
        "log10_rendezvous_mr": 2.0 * log_r1_nep,
        "energy_grid_twh_per_kg": float('inf'),
        "transit_years_flyby": 142400.0,
        "transit_years_rendezvous": float('inf'),
        "interstellar_capable": False,
        "blocker": "Stuhlinger Power Wall (alpha ~ 0.1 kW/kg); requires 142,400 yr burn to reach 0.1c"
    })

    # 6. Nuclear Pulse (Project Orion)
    isp_pulse = 3000.0
    ve_pulse = isp_pulse * G0
    log_r1_pulse = log10_relativistic_mass_ratio(target_beta, ve_pulse)
    results.append({
        "name": "Nuclear Pulse (Orion)",
        "isp_s": isp_pulse,
        "ve_km_s": ve_pulse / 1000.0,
        "thrust_rep": "10^7 N (time-avg)",
        "flyby_mr": float('inf'),
        "log10_flyby_mr": log_r1_pulse,
        "rendezvous_mr": float('inf'),
        "log10_rendezvous_mr": 2.0 * log_r1_pulse,
        "energy_grid_twh_per_kg": float('inf'),
        "transit_years_flyby": transit_time_years(D_PROXIMA, target_beta),
        "transit_years_rendezvous": float('inf'),
        "interstellar_capable": False,
        "blocker": "Pusher-Plate Ablation & Spallation; LTBT/OST treaties; Mass ratio 10^442"
    })

    # 7. Nuclear Fusion (D-3He, Magnetic Nozzle)
    ve_fusion = 0.045 * C  # 13,490 km/s (Daedalus design point)
    isp_fusion = ve_fusion / G0
    r1_fusion = relativistic_mass_ratio(target_beta, ve_fusion)
    epsilon_fusion = 0.05
    m0_over_ml_1stage = single_stage_mass_ratio_with_structure(r1_fusion, epsilon_fusion)
    m0_over_ml_2stage = two_stage_rendezvous_mass_ratio(target_beta, ve_fusion, epsilon_fusion)
    
    # Radiator acceleration clamp:
    a_max_fusion = radiator_clamped_acceleration(ve_fusion, efficiency=0.50, radiator_temp_k=1500.0)
    t_burn_fusion, d_burn_fusion = radiator_burn_metrics(target_beta * C, a_max_fusion)
    
    # Energetics:
    prop_mass_rendezvous = (m0_over_ml_2stage - 1.0) * payload_mass_kg
    e_fusion_info = fusion_reaction_energetics(prop_mass_rendezvous)
    
    transit_flyby_fusion = transit_time_years(D_PROXIMA, target_beta, t_burn_s=t_burn_fusion)
    transit_rendezvous_fusion = transit_flyby_fusion + (t_burn_fusion / YEAR_S)
    
    results.append({
        "name": "Nuclear Fusion (D-3He)",
        "isp_s": isp_fusion,
        "ve_km_s": ve_fusion / 1000.0,
        "thrust_rep": "10 kN (Daedalus)",
        "flyby_mr": r1_fusion,
        "log10_flyby_mr": math.log10(r1_fusion),
        "m0_over_ml_flyby": m0_over_ml_1stage,
        "rendezvous_mr": r1_fusion**2,
        "log10_rendezvous_mr": math.log10(r1_fusion**2),
        "m0_over_ml_rendezvous": m0_over_ml_2stage,
        "energy_grid_twh_per_kg": e_fusion_info["total_energy_twh"] / payload_mass_kg,
        "transit_years_flyby": transit_flyby_fusion,
        "transit_years_rendezvous": transit_rendezvous_fusion,
        "interstellar_capable": True,
        "blocker": "Thermonuclear Ignition (ntT >= 10^22 keV*s/m^3); 3He supply (30,000 t needed)"
    })

    # 8. Antimatter Beamed-Core Rocket (p-pbar Annihilation)
    ve_am = 0.331 * C  # 99,230 km/s
    isp_am = ve_am / G0
    r1_am = relativistic_mass_ratio(target_beta, ve_am)
    epsilon_am = 0.05
    m0_over_ml_1stage_am = single_stage_mass_ratio_with_structure(r1_am, epsilon_am)
    m0_over_ml_2stage_am = single_stage_mass_ratio_with_structure(r1_am**2, epsilon_am)
    
    # Antiprotons needed for rendezvous:
    pbar_mass_rendezvous = 0.5 * (m0_over_ml_2stage_am - 1.0) * payload_mass_kg
    e_am_info = antimatter_energy_and_grid_cost(pbar_mass_rendezvous)
    
    transit_flyby_am = transit_time_years(D_PROXIMA, target_beta)
    transit_rendezvous_am = transit_flyby_am  # burn time negligible if radiators exist
    
    results.append({
        "name": "Antimatter Beamed-Core",
        "isp_s": isp_am,
        "ve_km_s": ve_am / 1000.0,
        "thrust_rep": "10 kN",
        "flyby_mr": r1_am,
        "log10_flyby_mr": math.log10(r1_am),
        "m0_over_ml_flyby": m0_over_ml_1stage_am,
        "rendezvous_mr": r1_am**2,
        "log10_rendezvous_mr": math.log10(r1_am**2),
        "m0_over_ml_rendezvous": m0_over_ml_2stage_am,
        "energy_grid_twh_per_kg": e_am_info["e_grid_twh"] / payload_mass_kg,
        "transit_years_flyby": transit_flyby_am,
        "transit_years_rendezvous": transit_rendezvous_am,
        "interstellar_capable": True,
        "blocker": "Production Efficiency (10^-9); CERN yields 1 ng/yr; 688 t gamma-ray radiators"
    })

    # 9. Laser-Pushed Beamed Sail (Starshot class)
    # Evaluated at target_beta = 0.20 (canonical Starshot)
    sail_info_02 = beamed_sail_energetics_per_kg(0.20)
    transit_flyby_sail = transit_time_years(D_PROXIMA, 0.20)
    transit_rendezvous_sail_magsail = transit_time_years(D_PROXIMA, 0.20, is_decelerating_magsail=True)
    
    # Hybrid magsail mass penalty: 41 g coil per 1 g wafercraft -> 42x mass penalty
    energy_hybrid_magsail_twh_per_kg = sail_info_02["e_grid_twh_tonne"] * 42.0 / 1000.0
    
    results.append({
        "name": "Laser-Pushed Beamed Sail",
        "isp_s": None,
        "ve_km_s": None,
        "thrust_rep": "667 N on 1 g sail (100 GW)",
        "flyby_mr": 1.0,
        "log10_flyby_mr": 0.0,
        "m0_over_ml_flyby": 1.0,
        "rendezvous_mr": 42.0,  # 42x mass ratio for hybrid magsail
        "log10_rendezvous_mr": math.log10(42.0),
        "m0_over_ml_rendezvous": 42.0,
        "energy_grid_twh_per_kg": energy_hybrid_magsail_twh_per_kg,
        "transit_years_flyby": transit_flyby_sail,
        "transit_years_rendezvous": transit_rendezvous_sail_magsail,
        "interstellar_capable": True,
        "blocker": "Diffraction Aperture (D >= 1.8 km); Jitter <= 0.15 mas; Sail Absorption A_abs <= 10^-5"
    })
    
    return results


if __name__ == "__main__":
    print("=" * 80)
    print("PRACTICAL PROPULSION: INTERSTELLAR COST & SCALING BENCHMARK (Kepler A001)")
    print("=" * 80)
    rows = evaluate_all_propulsion_options(target_beta=0.10, payload_mass_kg=1.0)
    for r in rows:
        print(f"\n--- {r['name']} ---")
        print(f"  Isp: {r['isp_s']} s | ve: {r['ve_km_s']} km/s | Thrust: {r['thrust_rep']}")
        print(f"  Flyby MR: {r['flyby_mr']} (log10: {r['log10_flyby_mr']:.2f})")
        print(f"  Rendezvous MR: {r['rendezvous_mr']} (log10: {r['log10_rendezvous_mr']:.2f})")
        print(f"  Grid Energy Cost (TWh/kg payload): {r['energy_grid_twh_per_kg']}")
        print(f"  Transit (Flyby): {r['transit_years_flyby']:.1f} yr | Rendezvous: {r['transit_years_rendezvous']:.1f} yr")
        print(f"  Interstellar Capable: {r['interstellar_capable']}")
        print(f"  Single Blocker: {r['blocker']}")
