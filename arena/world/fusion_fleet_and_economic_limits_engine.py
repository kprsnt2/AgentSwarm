"""
Fusion Fleet and Economic Limits Engine
=======================================
Quantitative modeling of:
1. Coupled multi-reactor tritium fleet dynamics and doubling time paradox ("The Tritium Trap").
2. Bottom-up nuclear techno-economic LCOE scaling vs power density.
3. Virial structural mass and slow-quench thermal runaway in HTS magnets.
4. Disruption electromagnetic loads and Rosenbluth runaway electron avalanches.

Epistemic Class: Engineering Feasibility
Standard of Evidence: Nuclear kinetics, virial theorem, magneto-solid mechanics,
relativistic runaway avalanche theory, discounted cash-flow techno-economics.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

# Fundamental physical constants
MU_0 = 4.0 * math.pi * 1e-7          # H/m (permeability of free space)
E_CHARGE = 1.602176634e-19           # C
M_ELECTRON = 9.1093837e-31           # kg
C_LIGHT = 2.99792458e8               # m/s
EPSILON_0 = 8.8541878128e-12         # F/m
AMU_KG = 1.66053906660e-27           # kg
M_TRITIUM_KG = 3.01604928 * AMU_KG   # kg
TRITIUM_HALF_LIFE_YR = 12.32
LAMBDA_TRITIUM_YR = math.log(2.0) / TRITIUM_HALF_LIFE_YR  # 0.05626 yr^-1
SECONDS_PER_YEAR = 365.25 * 86400.0


@dataclass
class FleetDynamicsParameters:
    reactor_power_mw_th: float = 525.0
    capacity_factor: float = 0.80
    burnup_fraction: float = 0.02
    unrecoverable_loss_fraction: float = 0.001
    startup_inventory_kg: float = 8.0
    holdup_time_days: float = 1.0


class TritiumFleetDynamicsEngine:
    """
    Models dynamic tritium inventory evolution across global civilian reserves
    and multi-reactor fusion fleets.
    """
    def __init__(self, params: FleetDynamicsParameters = None):
        self.p = params if params is not None else FleetDynamicsParameters()

    def annual_burn_rate_kg(self) -> float:
        """Annual burn rate per reactor in kg/year."""
        e_fus_j = 17.589 * 1e6 * E_CHARGE
        reactions_per_sec = (self.p.reactor_power_mw_th * 1e6) / e_fus_j
        burn_kg_per_sec = reactions_per_sec * M_TRITIUM_KG
        return burn_kg_per_sec * SECONDS_PER_YEAR * self.p.capacity_factor

    def holdup_inventory_kg(self) -> float:
        """Tritium residing in the active on-site fuel processing loop."""
        annual_burn = self.annual_burn_rate_kg()
        circulation_rate_kg_yr = annual_burn / self.p.burnup_fraction
        return circulation_rate_kg_yr * (self.p.holdup_time_days / 365.25)

    def net_annual_surplus_kg(self, tbr: float) -> float:
        """
        Net annual surplus tritium bred by an operating reactor:
        Surplus = Bred - Burned - Fuel Cycle Losses - Inventory Decay.
        """
        annual_burn = self.annual_burn_rate_kg()
        bred = tbr * annual_burn
        burned = annual_burn
        processing_loss = (self.p.unrecoverable_loss_fraction / self.p.burnup_fraction) * annual_burn
        total_inv = self.p.startup_inventory_kg + self.holdup_inventory_kg()
        decay_loss = LAMBDA_TRITIUM_YR * total_inv

        return bred - burned - processing_loss - decay_loss

    def doubling_time_years(self, tbr: float) -> float:
        """
        Time in years required for an operating reactor to accumulate enough
        surplus tritium to seed one new identical reactor (startup inventory).
        Returns float('inf') if surplus <= 0.
        """
        surplus_rate = self.net_annual_surplus_kg(tbr)
        if surplus_rate <= 0.0:
            return float('inf')
        return self.p.startup_inventory_kg / surplus_rate

    def minimum_tbr_for_doubling_time(self, target_doubling_time_yr: float) -> float:
        """Computes minimum TBR needed to achieve a given doubling time."""
        annual_burn = self.annual_burn_rate_kg()
        if annual_burn <= 0:
            return 1.0
        total_inv = self.p.startup_inventory_kg + self.holdup_inventory_kg()
        decay_loss = LAMBDA_TRITIUM_YR * total_inv
        processing_loss_ratio = self.p.unrecoverable_loss_fraction / self.p.burnup_fraction
        required_surplus = self.p.startup_inventory_kg / target_doubling_time_yr

        tbr_min = 1.0 + processing_loss_ratio + (decay_loss + required_surplus) / annual_burn
        return tbr_min

    def simulate_fleet_growth(self, start_year: int = 2039, end_year: int = 2060,
                              initial_reserve_kg: float = 18.0,
                              tbr: float = 1.05) -> Dict[str, Any]:
        """
        Simulates the growth of commercial fusion fleet from the remaining civilian reserve.
        """
        years = list(range(start_year, end_year + 1))
        reserve = initial_reserve_kg
        reactors = 0
        surplus_pool = 0.0
        fleet_history = []
        reserve_history = []

        for yr in years:
            # Check if reserve or surplus can commission a new reactor
            if reactors == 0 and reserve >= self.p.startup_inventory_kg:
                reactors += 1
                reserve -= self.p.startup_inventory_kg
            elif surplus_pool >= self.p.startup_inventory_kg:
                new_reactors = int(surplus_pool // self.p.startup_inventory_kg)
                reactors += new_reactors
                surplus_pool -= new_reactors * self.p.startup_inventory_kg

            # Account for CANDU reserve decay
            reserve = max(0.0, reserve * math.exp(-LAMBDA_TRITIUM_YR))

            # Fleet breeding surplus or deficit
            if reactors > 0:
                surplus_rate = self.net_annual_surplus_kg(tbr)
                surplus_pool += surplus_rate * reactors
                # Surplus pool decays if positive
                if surplus_pool > 0:
                    surplus_pool = max(0.0, surplus_pool * math.exp(-LAMBDA_TRITIUM_YR))
                else:
                    # Deficit degrades active inventory
                    surplus_pool = min(0.0, surplus_pool)

            fleet_history.append(reactors)
            reserve_history.append(reserve)

        return {
            "years": years,
            "fleet_size": fleet_history,
            "reserve_kg": reserve_history,
            "final_surplus_pool_kg": surplus_pool
        }


@dataclass
class FusionCostParameters:
    net_electric_mwe: float = 108.0
    plasma_volume_m3: float = 140.0
    rebco_tape_km: float = 100000.0
    tape_cost_per_meter: float = 20.0       # $/m target (current is ~$50-100/m)
    magnet_structures_cost_m: float = 800.0 # $M
    vessel_and_in_vessel_m: float = 500.0   # $M
    cryogenics_cost_m: float = 250.0        # $M
    tritium_plant_cost_m: float = 450.0     # $M
    bop_turbine_cost_m: float = 450.0       # $M
    civil_and_licensing_m: float = 700.0    # $M
    fixed_charge_rate: float = 0.09         # 9% annual capital charge rate
    fixed_om_m_per_year: float = 60.0       # $M/year
    blanket_replace_cost_m: float = 150.0   # $M per replacement outage
    first_wall_lifetime_yr: float = 3.33    # replacement every 3.33 years
    outage_duration_months: float = 12.0    # 12 months remote replacement
    unplanned_outage_rate: float = 0.10     # 10% unplanned outage rate


class FusionTechnoEconomicEngine:
    """
    Computes bottom-up capital expenditure (CAPEX), capacity factor,
    operating costs (OPEX), and Levelized Cost of Electricity (LCOE).
    """
    def __init__(self, params: FusionCostParameters = None):
        self.p = params if params is not None else FusionCostParameters()

    def overnight_capital_cost_millions(self) -> float:
        """Computes total overnight capital cost in $ Millions."""
        tape_cost_m = (self.p.rebco_tape_km * 1000.0 * self.p.tape_cost_per_meter) / 1e6
        total_m = (tape_cost_m +
                   self.p.magnet_structures_cost_m +
                   self.p.vessel_and_in_vessel_m +
                   self.p.cryogenics_cost_m +
                   self.p.tritium_plant_cost_m +
                   self.p.bop_turbine_cost_m +
                   self.p.civil_and_licensing_m)
        return total_m

    def specific_capital_cost_per_kwe(self) -> float:
        """Capital cost in $/kWe net electric capacity."""
        total_capex = self.overnight_capital_cost_millions() * 1e6
        kwe = self.p.net_electric_mwe * 1000.0
        return total_capex / kwe

    def effective_capacity_factor(self) -> float:
        """
        Capacity factor bounded by periodic first-wall replacement outages
        and unplanned downtime.
        Cycle: operating_years = first_wall_lifetime_yr,
        outage_years = outage_duration_months / 12.
        """
        op_yr = self.p.first_wall_lifetime_yr
        outage_yr = self.p.outage_duration_months / 12.0
        cycle_yr = op_yr + outage_yr
        planned_availability = op_yr / cycle_yr
        return planned_availability * (1.0 - self.p.unplanned_outage_rate)

    def levelized_cost_of_electricity_mwh(self) -> float:
        """
        Computes LCOE in $/MWh:
        LCOE = (Annual Capital Cost + Fixed O&M + Annualized Blanket Replacement) / Annual Net Generation
        """
        capex_m = self.overnight_capital_cost_millions()
        annual_capital_m = capex_m * self.p.fixed_charge_rate

        # Annualized blanket replacement cost
        op_yr = self.p.first_wall_lifetime_yr
        outage_yr = self.p.outage_duration_months / 12.0
        cycle_yr = op_yr + outage_yr
        annual_blanket_m = self.p.blanket_replace_cost_m / cycle_yr

        annual_total_cost_m = annual_capital_m + self.p.fixed_om_m_per_year + annual_blanket_m

        cf = self.effective_capacity_factor()
        annual_generation_mwh = self.p.net_electric_mwe * 8760.0 * cf

        if annual_generation_mwh <= 0:
            return float('inf')

        lcoe = (annual_total_cost_m * 1e6) / annual_generation_mwh
        return lcoe


class MagnetVirialAndQuenchEngine:
    """
    Computes structural mass lower bounds from the Virial Stress Theorem
    and thermal runaway hotspot limits from slow normal zone propagation in HTS tapes.
    """
    def __init__(self, b_peak_tesla: float = 23.0, major_radius_m: float = 3.3,
                 coil_minor_radius_m: float = 2.3, coil_elongation: float = 2.0,
                 allowable_stress_mpa: float = 600.0,
                 steel_density_kg_m3: float = 7850.0):
        self.b_peak_tesla = b_peak_tesla
        self.r0 = major_radius_m
        self.a_coil = coil_minor_radius_m
        self.kappa_coil = coil_elongation
        self.sigma_allow = allowable_stress_mpa * 1e6
        self.rho = steel_density_kg_m3

    def stored_magnetic_energy_gj(self) -> float:
        """
        Computes stored magnetic energy in the toroidal field:
        U_M = int (B^2 / (2*mu_0)) dV across the entire TF coil bore volume.
        For a torus of major radius R0 and non-circular bore (a_coil, b_coil = kappa*a_coil):
        U_M = (pi * kappa_coil * a_coil^2 * R0) * (B_0^2 / (2 * mu_0)) * geometric_factor.
        For ARC: B_peak = 23 T, B_0 = 9.2 T, U_M ~ 40-45 GJ.
        """
        # Peak field is at the inner conductor nose: R_nose ~ 1.5 m in ARC
        r_nose = 1.5
        b_on_axis = self.b_peak_tesla * (r_nose / self.r0)  # ~10.45 T on axis

        # Integration of B_0^2 (R0/R)^2 / (2*mu_0) over elliptical cross-section:
        # Volume of coil bore: V_bore = 2 * pi * R0 * pi * a_coil^2 * kappa_coil
        v_bore = 2.0 * (math.pi**2) * self.r0 * (self.a_coil**2) * self.kappa_coil
        # Average B^2 / (2*mu_0) in bore with 1/R^2 dependence:
        # <1/R^2> ~ 1 / [ R0^2 * (1 - (a_coil/R0)^2)^(1/2) ]
        geom_factor = 1.0 / math.sqrt(max(0.1, 1.0 - (self.a_coil / self.r0)**2))
        avg_energy_density = (b_on_axis**2 / (2.0 * MU_0)) * geom_factor
        u_joules = avg_energy_density * v_bore
        return u_joules / 1e9

    def virial_minimum_structural_mass_tonnes(self) -> float:
        """
        Virial structural theorem: Mass >= (rho / sigma_allow) * U_M.
        Applies unconditionally to all self-contained magnetic geometries.
        """
        u_joules = self.stored_magnetic_energy_gj() * 1e9
        min_mass_kg = (self.rho / self.sigma_allow) * u_joules
        return min_mass_kg / 1000.0

    def hts_hotspot_burnout_time_seconds(self, current_density_a_m2: float = 1.5e8,
                                        copper_fraction: float = 0.40,
                                        t_init_k: float = 20.0,
                                        t_critical_k: float = 523.0) -> float:
        """
        Computes time to reach critical delamination temperature (523 K)
        during an unmitigated quench in REBCO tape.
        HTS normal zone propagation velocity is extremely slow (~0.01 - 0.05 m/s),
        preventing quench self-spreading and localizing Joule heating.
        """
        # Average copper resistivity in 20-500K range including magnetoresistance: ~2.5e-8 Ohm*m
        rho_cu = 2.5e-8
        # Average volumetric heat capacity: ~1.8e6 J/(m^3*K)
        c_v = 1.8e6

        j_cu = current_density_a_m2 / copper_fraction
        p_joule = (j_cu**2) * rho_cu  # W/m^3

        delta_t = t_critical_k - t_init_k
        burnout_time = (c_v * delta_t) / p_joule
        return burnout_time


class DisruptionAndAvalancheEngine:
    """
    Computes disruption electromagnetic forces on vacuum vessel structures
    and relativistic runaway electron avalanche amplification (Rosenbluth mechanism).
    """
    def __init__(self, plasma_current_ma: float = 9.0, major_radius_m: float = 3.3,
                 minor_radius_m: float = 1.13, b_toroidal_t: float = 12.2,
                 electron_density_m3: float = 3.0e20, z_eff: float = 1.5):
        self.ip_ma = plasma_current_ma
        self.r0 = major_radius_m
        self.a = minor_radius_m
        self.bt = b_toroidal_t
        self.ne = electron_density_m3
        self.z_eff = z_eff

    def induced_loop_electric_field_v_m(self, current_quench_time_ms: float = 10.0) -> float:
        """
        Induced parallel electric field E_parallel during rapid current quench.
        Inductance L_p ~ mu_0 * R0 * [ln(8*R0/a) - 1.75].
        """
        l_p = MU_0 * self.r0 * (math.log(8.0 * self.r0 / self.a) - 1.75)
        di_dt = (self.ip_ma * 1e6) / (current_quench_time_ms * 1e-3)
        loop_voltage = l_p * di_dt
        e_parallel = loop_voltage / (2.0 * math.pi * self.r0)
        return e_parallel

    def critical_dreicer_electric_field_v_m(self) -> float:
        """
        Critical electric field E_c to sustain runaway electron acceleration (Connor-Hastie):
        E_c = n_e * e^3 * ln(Lambda) / (4 * pi * epsilon_0^2 * m_e * c^2).
        """
        ln_lambda = 15.0
        num = self.ne * (E_CHARGE**3) * ln_lambda
        denom = 4.0 * math.pi * (EPSILON_0**2) * M_ELECTRON * (C_LIGHT**2)
        return num / denom

    def runaway_avalanche_gain_exponent(self) -> float:
        """
        Rosenbluth knock-on avalanche exponent:
        gamma_runaway ~ I_p / [ I_A * sqrt(2 + Z_eff) ]
        where Alfven current I_A = 4*pi*m_e*c / (mu_0*e) ~ 0.085 MA.
        """
        i_alfven_ma = (4.0 * math.pi * M_ELECTRON * C_LIGHT / (MU_0 * E_CHARGE)) / 1e6  # ~0.085 MA
        exponent = self.ip_ma / (i_alfven_ma * math.sqrt(2.0 + self.z_eff))
        return exponent

    def peak_asymmetric_halo_force_meganewtons(self, halo_fraction: float = 0.3,
                                               tpf: float = 1.5) -> float:
        """
        Peak vertical/lateral Lorentz load on vacuum vessel from halo currents:
        F = TPF * I_halo * B_T * (2 * pi * R0).
        """
        i_halo = halo_fraction * (self.ip_ma * 1e6)
        force_n = tpf * i_halo * self.bt * (2.0 * math.pi * self.r0)
        return force_n / 1e6


def run_comprehensive_economic_and_fleet_synthesis() -> Dict[str, Any]:
    """Runs integrated evaluation of all 4 advanced frontiers."""
    fleet_engine = TritiumFleetDynamicsEngine()
    cost_engine = FusionTechnoEconomicEngine()
    magnet_engine = MagnetVirialAndQuenchEngine()
    disruption_engine = DisruptionAndAvalancheEngine()

    # Doubling times at various TBRs
    doubling_times = {
        "TBR_1.05": fleet_engine.doubling_time_years(1.05),
        "TBR_1.08": fleet_engine.doubling_time_years(1.08),
        "TBR_1.12": fleet_engine.doubling_time_years(1.12),
        "TBR_1.15": fleet_engine.doubling_time_years(1.15)
    }

    tbr_for_10yr = fleet_engine.minimum_tbr_for_doubling_time(10.0)
    fleet_sim = fleet_engine.simulate_fleet_growth(2039, 2050, initial_reserve_kg=18.0, tbr=1.05)

    overnight_capex = cost_engine.overnight_capital_cost_millions()
    specific_capex = cost_engine.specific_capital_cost_per_kwe()
    cf = cost_engine.effective_capacity_factor()
    lcoe = cost_engine.levelized_cost_of_electricity_mwh()

    energy_gj = magnet_engine.stored_magnetic_energy_gj()
    virial_mass = magnet_engine.virial_minimum_structural_mass_tonnes()
    burnout_sec = magnet_engine.hts_hotspot_burnout_time_seconds()

    e_ind = disruption_engine.induced_loop_electric_field_v_m(10.0)
    e_crit = disruption_engine.critical_dreicer_electric_field_v_m()
    avalanche_exp = disruption_engine.runaway_avalanche_gain_exponent()
    halo_force_mn = disruption_engine.peak_asymmetric_halo_force_meganewtons()

    return {
        "fleet_dynamics": {
            "annual_burn_kg": fleet_engine.annual_burn_rate_kg(),
            "holdup_inv_kg": fleet_engine.holdup_inventory_kg(),
            "doubling_times_yr": doubling_times,
            "tbr_for_10yr_doubling": tbr_for_10yr,
            "fleet_size_at_2040": fleet_sim["fleet_size"][1],  # 2040 is index 1
            "fleet_size_at_2050": fleet_sim["fleet_size"][-1]
        },
        "techno_economics": {
            "overnight_capex_m": overnight_capex,
            "specific_capex_per_kwe": specific_capex,
            "capacity_factor": cf,
            "lcoe_per_mwh": lcoe
        },
        "magnetics_and_quench": {
            "stored_energy_gj": energy_gj,
            "virial_mass_tonnes": virial_mass,
            "hotspot_burnout_time_sec": burnout_sec
        },
        "disruptions_and_avalanches": {
            "induced_electric_field_v_m": e_ind,
            "critical_electric_field_v_m": e_crit,
            "avalanche_exponent": avalanche_exp,
            "halo_force_mn": halo_force_mn
        }
    }


if __name__ == "__main__":
    res = run_comprehensive_economic_and_fleet_synthesis()
    print("=== Fusion Fleet & Techno-Economic Synthesis Results ===")
    print(f"Annual Tritium Burn: {res['fleet_dynamics']['annual_burn_kg']:.2f} kg/yr")
    print(f"Doubling Time at TBR=1.05: {res['fleet_dynamics']['doubling_times_yr']['TBR_1.05']}")
    print(f"Doubling Time at TBR=1.08: {res['fleet_dynamics']['doubling_times_yr']['TBR_1.08']:.1f} yr")
    print(f"TBR required for 10-yr doubling: {res['fleet_dynamics']['tbr_for_10yr_doubling']:.4f}")
    print(f"Fleet Size at 2040: {res['fleet_dynamics']['fleet_size_at_2040']}")
    print(f"Overnight CAPEX: ${res['techno_economics']['overnight_capex_m']:.1f}M (${res['techno_economics']['specific_capex_per_kwe']:.0f}/kWe)")
    print(f"Capacity Factor: {res['techno_economics']['capacity_factor']*100:.1f}%")
    print(f"LCOE: ${res['techno_economics']['lcoe_per_mwh']:.1f}/MWh")
    print(f"Stored Magnetic Energy: {res['magnetics_and_quench']['stored_energy_gj']:.1f} GJ")
    print(f"Virial Structural Mass: {res['magnetics_and_quench']['virial_mass_tonnes']:.1f} tonnes")
    print(f"HTS Hotspot Burnout Time: {res['magnetics_and_quench']['hotspot_burnout_time_sec']*1000:.1f} ms")
    print(f"Halo Current Lorentz Load: {res['disruptions_and_avalanches']['halo_force_mn']:.1f} MN")
    print(f"Runaway Avalanche Exponent: {res['disruptions_and_avalanches']['avalanche_exponent']:.1f}")
