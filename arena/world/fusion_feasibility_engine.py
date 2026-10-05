"""
Fusion Feasibility Engine
=========================
Engineering and Physical Feasibility Evaluation of Commercial Fusion Power by 2040.
Epistemic Class: Engineering Feasibility
Standard of Evidence: Nuclear reaction kinetics, conservation of energy,
thermodynamic power cycles, magnetohydrodynamic limits, materials damage limits.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Optional

# Physical and Nuclear Constants
C_LIGHT = 2.99792458e8          # m/s
E_CHARGE = 1.602176634e-19       # C
J_PER_KEV = 1.602176634e-16     # J / keV
J_PER_MEV = 1.602176634e-13     # J / MeV
AMU_KG = 1.66053906660e-27      # kg / amu
C_BREM = 5.35e-37               # Bremsstrahlung constant W*m^3 / keV^0.5

# Fusion reaction energies in MeV
E_DT_TOTAL_MEV = 17.589
E_DT_ALPHA_MEV = 3.52
E_DT_NEUTRON_MEV = 14.07
M_TRITIUM_KG = 3.01604928 * AMU_KG  # ~5.0083e-27 kg
TRITIUM_HALF_LIFE_YR = 12.32
LAMBDA_TRITIUM_YR = math.log(2.0) / TRITIUM_HALF_LIFE_YR  # ~0.05626 yr^-1
SECONDS_PER_YEAR = 365.25 * 86400.0


def dt_reactivity_bosch_hale(t_kev: float) -> float:
    """
    Computes D-T fusion reactivity <sigma*v> in m^3/s using the standard
    Bosch-Hale (1992) parameterization.
    Valid for 0.5 <= T <= 100 keV.
    """
    if t_kev <= 0.0:
        return 0.0

    # Bosch-Hale coefficients for D-T
    b_g = 34.3827       # sqrt(keV)
    m_rc2 = 1124656.0   # keV

    c1 = 1.17302e-9
    c2 = 1.51361e-2
    c3 = 7.51886e-2
    c4 = 4.60643e-3
    c5 = 1.35000e-2
    c6 = -1.06750e-4
    c7 = 1.36600e-5

    denom = 1.0 + t_kev * (c3 + t_kev * (c5 + t_kev * c7))
    num = t_kev * (c2 + t_kev * (c4 + t_kev * c6))
    theta = t_kev / (1.0 - (num / denom)) if denom != 0.0 else t_kev

    xi = (b_g**2 / (4.0 * theta))**(1.0 / 3.0)
    # sigma_v in cm^3/s:
    # <sigma v> = c1 * theta * sqrt(xi / (m_rc2 * t_kev^3)) * exp(-3 * xi)
    sv_cm3_s = c1 * theta * math.sqrt(xi / (m_rc2 * (t_kev**3))) * math.exp(-3.0 * xi)
    # Convert cm^3/s to m^3/s (1 cm^3 = 1e-6 m^3)
    sv_m3_s = sv_cm3_s * 1e-6
    return sv_m3_s


def dd_reactivity_approx(t_kev: float) -> float:
    """D-D fusion total reactivity approximation in m^3/s."""
    if t_kev <= 1.0:
        return 0.0
    # D-D is roughly 50 to 100x lower than D-T at relevant temperatures
    sv_dt = dt_reactivity_bosch_hale(t_kev)
    return sv_dt * 0.012 * (t_kev / 30.0)**0.3


def dhe3_reactivity_approx(t_kev: float) -> float:
    """D-3He fusion reactivity approximation in m^3/s."""
    if t_kev <= 2.0:
        return 0.0
    # D-3He peaks around 60-80 keV at ~2.0e-22 m^3/s
    # Parameterized fit
    return 2.2e-22 * math.exp(-0.5 * ((math.log(t_kev) - math.log(65.0)) / 0.8)**2)


def pb11_reactivity_approx(t_kev: float) -> float:
    """p-11B fusion reactivity approximation in m^3/s."""
    if t_kev <= 10.0:
        return 0.0
    # p-11B peaks near 300-400 keV at ~3.5e-22 m^3/s
    return 3.5e-22 * math.exp(-0.5 * ((math.log(t_kev) - math.log(350.0)) / 0.7)**2)


def pb11_bremsstrahlung_ratio(t_kev: float) -> float:
    """
    Ratio of Bremsstrahlung radiation power to p-11B fusion power in thermal equilibrium (Te = Ti).
    Reaction: p + 11B -> 3 alpha + 8.68 MeV.
    For stoichiometric ratio np / nB = 5:
    ne = np + 5*nB = 10*nB
    Z_eff = (np*1^2 + nB*5^2)/ne = (5 + 25)/10 = 3.0.
    P_brem = C_B * ne^2 * Z_eff * sqrt(Te) * (1 + 2*Te/511)
    P_fus = np * nB * <sigma v> * E_fus = 5 * nB^2 * <sigma v> * E_fus
    ne^2 * Z_eff / (5 * nB^2) = 100 * 3.0 / 5 = 60.
    """
    sv = pb11_reactivity_approx(t_kev)
    if sv <= 0.0:
        return float('inf')

    e_fus_j = 8.68 * J_PER_MEV
    # Relativistic correction to Bremsstrahlung
    rel_factor = 1.0 + (2.0 * t_kev / 511.0)
    p_brem_factor = 60.0 * C_BREM * math.sqrt(t_kev) * rel_factor
    p_fus_factor = sv * e_fus_j
    return p_brem_factor / p_fus_factor


def lawson_triple_product_dt(t_kev: float) -> float:
    """
    Computes required D-T Lawson triple product n * T * tau_E (keV * s / m^3) for ignition (Q -> inf).
    Alpha power balance:
    P_alpha >= P_brem + P_transport
    (1/4) * n^2 * <sigma v> * E_alpha = C_B * n^2 * Z_eff * sqrt(T) + 3 * n * T / tau_E
    (with Z_eff = 1.0 for pure D-T, E_alpha = 3.52 MeV).
    n * T * tau_E = 3 * T^2 / [ 0.25 * <sigma v> * E_alpha - C_B * sqrt(T) ]
    If Bremsstrahlung exceeds alpha heating, returns float('inf').
    """
    if t_kev <= 4.4:
        return float('inf')

    sv = dt_reactivity_bosch_hale(t_kev)
    e_alpha_j = E_DT_ALPHA_MEV * J_PER_MEV
    p_alpha_norm = 0.25 * sv * e_alpha_j
    p_brem_norm = C_BREM * math.sqrt(t_kev)

    net_heating = p_alpha_norm - p_brem_norm
    if net_heating <= 0.0:
        return float('inf')

    # 3 * T in Joules: 3 * (t_kev * J_PER_KEV)
    # n * tau_E = 3 * (t_kev * J_PER_KEV) / net_heating (in s / m^3)
    # Triple product n * T * tau_E in keV * s / m^3:
    n_t_tau = 3.0 * (t_kev * J_PER_KEV) * t_kev / net_heating
    return n_t_tau


def lawson_triple_product_finite_q(t_kev: float, q_target: float) -> float:
    """
    Computes D-T triple product n * T * tau_E (keV * s / m^3) for a finite energy gain Q.
    P_aux = P_fus / Q = (E_tot / (E_alpha * Q)) * P_alpha.
    """
    if t_kev <= 1.0 or q_target <= 0.0:
        return float('inf')

    sv = dt_reactivity_bosch_hale(t_kev)
    e_tot_j = E_DT_TOTAL_MEV * J_PER_MEV
    e_alpha_j = E_DT_ALPHA_MEV * J_PER_MEV

    p_alpha_norm = 0.25 * sv * e_alpha_j
    p_aux_norm = 0.25 * sv * e_tot_j / q_target
    p_brem_norm = C_BREM * math.sqrt(t_kev)

    net_heating = p_alpha_norm + p_aux_norm - p_brem_norm
    if net_heating <= 0.0:
        return float('inf')

    return 3.0 * (t_kev * J_PER_KEV) * t_kev / net_heating


@dataclass
class PlantEfficiencyParameters:
    thermal_efficiency: float       # e.g. 0.33 to 0.45
    direct_conversion_eff: float    # e.g. 0.0 to 0.85
    driver_wall_plug_eff: float     # e.g. 0.40 for NBI/RF, 0.12 for lasers
    blanket_multiplier: float       # e.g. 1.0 to 1.2
    bop_fraction: float             # Balance-of-plant recirc fraction
    magnet_cooling_fraction: float  # Cryogenic magnet refrigeration recirc fraction


def calculate_engineering_q(p_fusion_mw: float, p_aux_mw: float,
                            params: PlantEfficiencyParameters,
                            f_neutron: float = 0.8) -> Dict[str, float]:
    """
    Calculates plant gross electrical power, recirculating electrical power,
    net electrical power, and engineering gain Q_eng = P_gross / P_recirc.
    """
    # Thermal power produced in blanket and core
    f_charged = 1.0 - f_neutron
    p_th_mw = ((f_neutron * params.blanket_multiplier + f_charged) * p_fusion_mw) + p_aux_mw

    # Gross electricity generated
    p_elec_thermal = params.thermal_efficiency * p_th_mw
    p_elec_direct = params.direct_conversion_eff * (f_charged * p_fusion_mw)
    p_gross_mw = p_elec_thermal + p_elec_direct

    # Recirculating power
    p_driver_mw = p_aux_mw / params.driver_wall_plug_eff if params.driver_wall_plug_eff > 0 else 0.0
    p_bop_mw = params.bop_fraction * p_gross_mw
    p_cryo_mw = params.magnet_cooling_fraction * p_gross_mw
    p_recirc_mw = p_driver_mw + p_bop_mw + p_cryo_mw

    p_net_mw = p_gross_mw - p_recirc_mw
    q_eng = p_gross_mw / p_recirc_mw if p_recirc_mw > 0 else 0.0
    recirc_fraction = p_recirc_mw / p_gross_mw if p_gross_mw > 0 else 1.0

    return {
        "p_th_mw": p_th_mw,
        "p_gross_mw": p_gross_mw,
        "p_recirc_mw": p_recirc_mw,
        "p_net_mw": p_net_mw,
        "q_eng": q_eng,
        "recirc_fraction": recirc_fraction
    }


class TritiumBurnAndBreedingModel:
    """
    Tracks tritium consumption, breeding, and mass inventory dynamics.
    1000 MW fusion thermal power burns ~56.07 kg of tritium per full-power year (FPY).
    """
    def __init__(self, fusion_power_mw: float, capacity_factor: float,
                 burnup_fraction: float, tbr_achieved: float,
                 fuel_cycle_time_days: float, unrecoverable_loss_fraction: float,
                 startup_inventory_kg: float):
        self.fusion_power_mw = fusion_power_mw
        self.capacity_factor = capacity_factor
        self.burnup_fraction = burnup_fraction
        self.tbr_achieved = tbr_achieved
        self.fuel_cycle_time_days = fuel_cycle_time_days
        self.unrecoverable_loss_fraction = unrecoverable_loss_fraction
        self.startup_inventory_kg = startup_inventory_kg

    def annual_burn_rate_kg(self) -> float:
        """Computes annual tritium burn rate in kg/year at given capacity factor."""
        e_fus_j = E_DT_TOTAL_MEV * J_PER_MEV
        reactions_per_sec = (self.fusion_power_mw * 1e6) / e_fus_j
        kg_per_sec = reactions_per_sec * M_TRITIUM_KG
        annual_burn_fpy = kg_per_sec * SECONDS_PER_YEAR
        return annual_burn_fpy * self.capacity_factor

    def required_tbr_for_sustainability(self, doubling_time_years: float = 5.0) -> float:
        """
        Calculates required Tritium Breeding Ratio (TBR) to account for:
        1. Burnup replacement (1.0)
        2. Fuel processing unrecoverable losses: epsilon / f_b
        3. Radioactive decay of startup reserve: lambda * I_start / m_dot_burn
        4. Doubling time expansion: (ln 2 / t_d) * I_start / m_dot_burn
        5. Holdup inventory radioactive decay: lambda * I_holdup / m_dot_burn
        """
        annual_burn = self.annual_burn_rate_kg()
        if annual_burn <= 0:
            return 1.0

        # Processing losses per pass
        loss_margin = self.unrecoverable_loss_fraction / self.burnup_fraction

        # Startup reserve decay
        startup_decay_margin = (LAMBDA_TRITIUM_YR * self.startup_inventory_kg) / annual_burn

        # Doubling reserve margin
        doubling_margin = (math.log(2.0) * self.startup_inventory_kg) / (doubling_time_years * annual_burn)

        # Holdup inventory decay
        m_dot_circ_kg_yr = annual_burn / self.burnup_fraction
        i_holdup_kg = m_dot_circ_kg_yr * (self.fuel_cycle_time_days / 365.25)
        holdup_decay_margin = (LAMBDA_TRITIUM_YR * i_holdup_kg) / annual_burn

        tbr_required = 1.0 + loss_margin + startup_decay_margin + doubling_margin + holdup_decay_margin
        return tbr_required


def simulate_global_civilian_tritium(years: List[int],
                                     num_reactors_online: Dict[int, float] = None,
                                     reactor_power_mw: float = 500.0,
                                     tbr: float = 1.05) -> Dict[int, float]:
    """
    Simulates global civilian CANDU tritium reserve (kg) from 2024 to 2045.
    Initial reserve in 2024: ~28.0 kg.
    Production declines as CANDUs retire:
      2024-2027: 2.2 kg/yr
      2028-2032: 1.4 kg/yr
      2033-2038: 0.6 kg/yr
      2039+: 0.2 kg/yr
    Startup charge: 8.0 kg drawn upon initial commissioning.
    """
    if num_reactors_online is None:
        num_reactors_online = {}

    inventory = 28.0
    active_reactors_seen = set()
    result = {}

    annual_burn_per_reactor = 56.07 * (reactor_power_mw / 1000.0) * 0.8  # ~22.43 kg/yr

    for yr in years:
        if yr < 2024:
            result[yr] = inventory
            continue

        # CANDU production schedule
        if yr <= 2027:
            candu_prod = 2.2
        elif yr <= 2032:
            candu_prod = 1.4
        elif yr <= 2038:
            candu_prod = 0.6
        else:
            candu_prod = 0.2

        n_reactors = num_reactors_online.get(yr, 0.0)

        # Check for newly commissioned reactors requiring startup charge (8 kg)
        if n_reactors > 0 and yr not in active_reactors_seen:
            # First year this reactor count is seen
            new_reactors = n_reactors - len(active_reactors_seen)
            if new_reactors > 0:
                inventory -= new_reactors * 8.0
                active_reactors_seen.add(yr)

        # Reactor burn and breeding
        if n_reactors > 0:
            net_breeding_rate = (tbr - 1.0) * annual_burn_per_reactor * n_reactors
            inventory += net_breeding_rate

        # Decay of existing inventory
        inventory = inventory * math.exp(-LAMBDA_TRITIUM_YR) + candu_prod
        result[yr] = max(0.0, inventory)

    return result


class NeutronMaterialsDamageModel:
    """
    Computes first-wall displacements per atom (DPA) and mechanical component lifetime.
    Rule of thumb: 1 MW/m^2 14.1 MeV wall load produces ~10.5 DPA/FPY in ferritic steels (Eurofer97).
    """
    def __init__(self, neutron_wall_load_mw_m2: float, material_type: str,
                 dpa_lifetime_limit: float = 70.0, helium_appm_per_dpa: float = 12.0):
        self.neutron_wall_load_mw_m2 = neutron_wall_load_mw_m2
        self.material_type = material_type
        self.dpa_lifetime_limit = dpa_lifetime_limit
        self.helium_appm_per_dpa = helium_appm_per_dpa

    def annual_dpa(self, capacity_factor: float = 0.8) -> float:
        """Returns annual DPA rate at given capacity factor."""
        dpa_per_fpy = 10.5 * self.neutron_wall_load_mw_m2
        return dpa_per_fpy * capacity_factor

    def component_lifetime_years(self, capacity_factor: float = 0.8) -> float:
        """Returns component replacement lifetime in years."""
        annual = self.annual_dpa(capacity_factor)
        if annual <= 0:
            return float('inf')
        return self.dpa_lifetime_limit / annual


def eich_sol_width_mm(b_poloidal_tesla: float, p_sol_mw: float, major_radius_m: float) -> float:
    """
    Computes Scrape-Off Layer (SOL) heat flux decay width lambda_q mapped to outer midplane (in mm).
    Eich et al. (2013) multi-machine empirical scaling law:
    lambda_q = 0.63 * B_pol^-1.19 * P_SOL^-0.13 * R^0.02
    """
    if b_poloidal_tesla <= 0 or p_sol_mw <= 0 or major_radius_m <= 0:
        return 0.0
    return 0.63 * (b_poloidal_tesla**(-1.19)) * (p_sol_mw**(-0.13)) * (major_radius_m**0.02)


def divertor_peak_heat_flux_mw_m2(p_sol_mw: float, major_radius_m: float,
                                  b_poloidal_tesla: float, flux_expansion: float,
                                  strike_angle_deg: float, f_radiation: float) -> Tuple[float, float, bool]:
    """
    Computes unmitigated and mitigated peak divertor heat flux (MW/m^2).
    Peak parallel heat flux mapped along field line:
    q_parallel = P_SOL / (2 * pi * R * (lambda_q * 1e-3))
    Target unmitigated perpendicular heat flux:
    q_perp_unmit = q_parallel * (sin(strike_angle) / flux_expansion)
    With divertor radiative cooling fraction f_radiation:
    q_perp_mit = (1 - f_radiation) * q_perp_unmit
    Engineering limit for water-cooled tungsten monoblocks: <= 10.0 MW/m^2 (steady-state).
    Returns (q_perp_unmit, q_perp_mit, ok).
    """
    lambda_q_mm = eich_sol_width_mm(b_poloidal_tesla, p_sol_mw, major_radius_m)
    lambda_q_m = lambda_q_mm * 1e-3

    # Parallel heat flux
    q_parallel = p_sol_mw / (2.0 * math.pi * major_radius_m * lambda_q_m)

    # Geometry reduction: sin(theta) / flux_expansion
    theta_rad = math.radians(strike_angle_deg)
    geom_factor = math.sin(theta_rad) / flux_expansion
    q_unmit = q_parallel * geom_factor

    q_mit = (1.0 - f_radiation) * q_unmit
    ok = (q_mit <= 10.0)
    return (q_unmit, q_mit, ok)


def get_all_concept_specifications() -> List[Dict[str, Any]]:
    """Returns detailed technical specifications for the 6 primary fusion archetypes."""
    return [
        {
            "concept": "High-Field Compact Tokamak (CFS SPARC/ARC)",
            "fuel": "D-T",
            "q_plasma": 11.1,
            "p_fusion_mw": 525.0,
            "p_aux_mw": 47.3,
            "f_neutron": 0.80,
            "efficiency_params": PlantEfficiencyParameters(
                thermal_efficiency=0.40,
                direct_conversion_eff=0.0,
                driver_wall_plug_eff=0.45,
                blanket_multiplier=1.15,
                bop_fraction=0.04,
                magnet_cooling_fraction=0.05
            ),
            "wall_load_mw_m2": 2.5,
            "b_poloidal_t": 3.1,
            "p_sol_mw": 45.0,
            "major_radius_m": 3.3,
            "p_commercial_grid_by_2040": 0.18,
            "earliest_grid_year": 2039,
            "primary_physical_limit": "Eich SOL width scaling lambda_q = 0.16 mm concentrating 50+ MW/m^2 onto divertor plates",
            "binding_engineering_constraint": "REBCO HTS tape industrial capacity (100k km/plant vs 5k km/yr global output) and CANDU tritium stock exhaustion"
        },
        {
            "concept": "Advanced Stellarator (W7-X / Proxima / Type One)",
            "fuel": "D-T",
            "q_plasma": 15.0,
            "p_fusion_mw": 600.0,
            "p_aux_mw": 40.0,
            "f_neutron": 0.80,
            "efficiency_params": PlantEfficiencyParameters(
                thermal_efficiency=0.42,
                direct_conversion_eff=0.0,
                driver_wall_plug_eff=0.40,
                blanket_multiplier=1.12,
                bop_fraction=0.04,
                magnet_cooling_fraction=0.05
            ),
            "wall_load_mw_m2": 1.5,
            "b_poloidal_t": 1.5,
            "p_sol_mw": 50.0,
            "major_radius_m": 5.5,
            "p_commercial_grid_by_2040": 0.08,
            "earliest_grid_year": 2042,
            "primary_physical_limit": "Neoclassical 3D transport ripple losses and unconfined fast alpha prompt loss",
            "binding_engineering_constraint": "Extreme sub-millimeter precision fabrication of non-planar 3D superconducting coils at 10-meter scale"
        },
        {
            "concept": "Magneto-Inertial FRC (Helion Polaris/Orion)",
            "fuel": "D-3He",
            "q_plasma": 5.0,
            "p_fusion_mw": 250.0,
            "p_aux_mw": 50.0,
            "f_neutron": 0.05,  # Parasitic D-D branch
            "efficiency_params": PlantEfficiencyParameters(
                thermal_efficiency=0.35,
                direct_conversion_eff=0.70,
                driver_wall_plug_eff=0.60,
                blanket_multiplier=1.0,
                bop_fraction=0.03,
                magnet_cooling_fraction=0.03
            ),
            "wall_load_mw_m2": 0.2,
            "b_poloidal_t": 2.0,
            "p_sol_mw": 15.0,
            "major_radius_m": 1.5,
            "p_commercial_grid_by_2040": 0.03,
            "earliest_grid_year": 2044,
            "primary_physical_limit": "D-D side branch neutron/tritium generation and microturbulent transport during supersonic plasmoid merging",
            "binding_engineering_constraint": "Terrestrial 3He non-existence (<30 kg reserves) and cyclic rep-rate high-voltage switching fatigue"
        },
        {
            "concept": "Conventional Low-Field Tokamak (ITER / DEMO / STEP)",
            "fuel": "D-T",
            "q_plasma": 10.0,
            "p_fusion_mw": 500.0,
            "p_aux_mw": 50.0,
            "f_neutron": 0.80,
            "efficiency_params": PlantEfficiencyParameters(
                thermal_efficiency=0.35,
                direct_conversion_eff=0.0,
                driver_wall_plug_eff=0.40,
                blanket_multiplier=1.10,
                bop_fraction=0.06,
                magnet_cooling_fraction=0.08
            ),
            "wall_load_mw_m2": 1.0,
            "b_poloidal_t": 1.2,
            "p_sol_mw": 60.0,
            "major_radius_m": 6.2,
            "p_commercial_grid_by_2040": 0.02,
            "earliest_grid_year": 2048,
            "primary_physical_limit": "Greenwald density limit and low toroidal field (B_T <= 5.3 T) requiring massive 800+ m^3 plasma volume",
            "binding_engineering_constraint": "15-20 year civil construction lifecycle and multi-billion-dollar capital expenditure"
        },
        {
            "concept": "Laser Inertial Confinement (NIF / Longview / Focused)",
            "fuel": "D-T",
            "q_plasma": 80.0,
            "p_fusion_mw": 800.0,
            "p_aux_mw": 10.0,
            "f_neutron": 0.80,
            "efficiency_params": PlantEfficiencyParameters(
                thermal_efficiency=0.42,
                direct_conversion_eff=0.0,
                driver_wall_plug_eff=0.12,  # DPSSL laser
                blanket_multiplier=1.15,
                bop_fraction=0.04,
                magnet_cooling_fraction=0.01
            ),
            "wall_load_mw_m2": 3.0,
            "b_poloidal_t": 0.1,
            "p_sol_mw": 100.0,
            "major_radius_m": 5.0,
            "p_commercial_grid_by_2040": 0.01,
            "earliest_grid_year": 2050,
            "primary_physical_limit": "Rayleigh-Taylor hydrodynamic instability and low laser wall-plug efficiency (<15%)",
            "binding_engineering_constraint": "High rep-rate target fabrication at <$0.20/shot (10 Hz = 864,000 shots/day) and final optics neutron degradation"
        },
        {
            "concept": "Beam-Driven FRC (TAE p-B11 Copernicus / Da Vinci)",
            "fuel": "p-11B",
            "q_plasma": 2.0,
            "p_fusion_mw": 200.0,
            "p_aux_mw": 100.0,
            "f_neutron": 0.001,
            "efficiency_params": PlantEfficiencyParameters(
                thermal_efficiency=0.40,
                direct_conversion_eff=0.50,
                driver_wall_plug_eff=0.50,
                blanket_multiplier=1.0,
                bop_fraction=0.04,
                magnet_cooling_fraction=0.02
            ),
            "wall_load_mw_m2": 0.01,
            "b_poloidal_t": 1.0,
            "p_sol_mw": 20.0,
            "major_radius_m": 2.0,
            "p_commercial_grid_by_2040": 0.00001,
            "earliest_grid_year": 2060,
            "primary_physical_limit": "Bremsstrahlung radiation catastrophe P_brem/P_fus > 1.0 for all temperatures under thermal equilibrium; electron drag",
            "binding_engineering_constraint": "Gigawatt-scale neutral beam power recirculation requirement yielding negative net electrical output"
        }
    ]


def evaluate_concept(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates power balance, materials lifetime, and timeline feasibility for a concept."""
    pb = calculate_engineering_q(
        p_fusion_mw=spec["p_fusion_mw"],
        p_aux_mw=spec["p_aux_mw"],
        params=spec["efficiency_params"],
        f_neutron=spec["f_neutron"]
    )

    mat_model = NeutronMaterialsDamageModel(
        neutron_wall_load_mw_m2=spec["wall_load_mw_m2"],
        material_type="Eurofer97",
        dpa_lifetime_limit=70.0
    )
    annual_dpa = mat_model.annual_dpa(0.8)
    lifetime_yr = mat_model.component_lifetime_years(0.8)

    return {
        "concept": spec["concept"],
        "fuel": spec["fuel"],
        "q_plasma": spec["q_plasma"],
        "p_gross_mw": pb["p_gross_mw"],
        "p_recirc_mw": pb["p_recirc_mw"],
        "p_net_mw": pb["p_net_mw"],
        "q_eng": pb["q_eng"],
        "annual_dpa": annual_dpa,
        "first_wall_lifetime_yr": lifetime_yr,
        "timeline": {
            "p_commercial_grid_by_2040": spec["p_commercial_grid_by_2040"],
            "earliest_grid_year": spec["earliest_grid_year"]
        },
        "primary_physical_limit": spec["primary_physical_limit"],
        "binding_engineering_constraint": spec["binding_engineering_constraint"]
    }


def run_full_comparative_assessment() -> Dict[str, Any]:
    """Runs evaluation for all archetypes and ranks them by feasibility."""
    specs = get_all_concept_specifications()
    evaluated = [evaluate_concept(s) for s in specs]
    # Sort descending by p_commercial_grid_by_2040
    ranked = sorted(evaluated, key=lambda x: x["timeline"]["p_commercial_grid_by_2040"], reverse=True)
    return {"ranked_concepts": ranked}


if __name__ == "__main__":
    results = run_full_comparative_assessment()
    print("Ranked Fusion Concepts by 2040 Commercial Feasibility:")
    for rank, item in enumerate(results["ranked_concepts"], 1):
        print(f"{rank}. {item['concept']} | P(2040)={item['timeline']['p_commercial_grid_by_2040']*100:.2f}% | Earliest={item['timeline']['earliest_grid_year']}")
