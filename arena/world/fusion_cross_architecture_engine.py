"""
Fusion Cross-Architecture and EPC Timeline Closure Engine
=========================================================
Quantitative physics and critical-path engineering models for:
1. Laser Inertial Confinement Fusion (ICF):
   - Rep-rate scaling vs thermal power and target gain
   - Allowable target manufacturing cost vs electricity price
   - Driver wall-plug efficiency and recirculating power fraction
   - Final optics neutron damage and laser-induced damage threshold (LIDT) collapse
2. Magneto-Inertial Pulsed FRC (D-He3 / Helion Archetype):
   - Terrestrial He-3 reserve depletion rate and lifetime
   - Parasitic D-D fusion branches (Tritium breeding and fast neutron production)
   - In-situ D-T burn and 14.1 MeV neutron activation penalty
   - Bremsstrahlung vs fusion power at D-He3 operating temperatures (70-100 keV)
3. Advanced Modular Stellarators (W7-X / Proxima Archetype):
   - 3D coil compound curvature strain on brittle REBCO HTS tapes
   - Fast alpha particle collisionless stochastic ripple loss fraction
   - 3D geometric blanket coverage penalty and homogeneous TBR deficit
4. Nuclear Plant EPC & Regulatory Critical-Path Timeline:
   - Critical Path Method (CPM) calculation from October 2026 to commercial operation
   - Earliest possible grid synchronization date under aggressive, baseline, and historical slip models

Epistemic Class: Engineering Feasibility
Standard of Evidence: Conservation of energy, nuclear cross-sections, Bremsstrahlung radiation limits,
solid mechanics strain limits, CPM project scheduling.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

# Fundamental physical constants
MU_0 = 4.0 * math.pi * 1e-7          # H/m
E_CHARGE = 1.602176634e-19           # C
M_ELECTRON = 9.1093837e-31           # kg
C_LIGHT = 2.99792458e8               # m/s
EPSILON_0 = 8.8541878128e-12         # F/m
AMU_KG = 1.66053906660e-27           # kg

# Nuclear Masses
M_DEUTERIUM_KG = 2.01410178 * AMU_KG
M_TRITIUM_KG = 3.01604928 * AMU_KG
M_HE3_KG = 3.0160293 * AMU_KG
M_HE4_KG = 4.002602 * AMU_KG
M_PROTON_KG = 1.00727647 * AMU_KG
M_NEUTRON_KG = 1.00866492 * AMU_KG

# Reaction Q values (Joules)
Q_DT_J = 17.589 * 1e6 * E_CHARGE      # 17.589 MeV -> 2.818e-12 J
Q_DHE3_J = 18.354 * 1e6 * E_CHARGE    # 18.354 MeV -> 2.941e-12 J
Q_DD_N_J = 3.269 * 1e6 * E_CHARGE     # D + D -> n (2.45 MeV) + He3 (0.82 MeV)
Q_DD_P_J = 4.033 * 1e6 * E_CHARGE     # D + D -> p (3.02 MeV) + T (1.01 MeV)

SECONDS_PER_YEAR = 365.25 * 86400.0


# ==============================================================================
# 1. LASER INERTIAL CONFINEMENT FUSION (ICF) ENGINE
# ==============================================================================

@dataclass
class LaserICFParameters:
    plant_thermal_power_mw: float = 1000.0   # 1000 MWth target
    driver_energy_mj: float = 2.5            # 2.5 MJ laser pulse
    target_gain: float = 80.0                # Target gain Q_target
    laser_wall_plug_efficiency: float = 0.12 # 12% for DPSSL
    thermal_efficiency: float = 0.40         # 40% steam/salt cycle
    auxiliary_power_fraction: float = 0.08   # 8% BOP and cryo
    electricity_price_per_kwh: float = 0.06  # $0.06/kWh ($60/MWh) wholesale
    fuel_cost_fraction_limit: float = 0.15   # Max 15% revenue for target fuel
    chamber_radius_m: float = 12.0           # 12 m chamber radius
    capacity_factor: float = 0.80


class LaserICFEngine:
    """
    Evaluates physical, repetition-rate, target-cost, and optical limits
    for commercial Laser Inertial Confinement Fusion.
    """
    def __init__(self, params: LaserICFParameters = None):
        self.p = params if params is not None else LaserICFParameters()

    def yield_per_shot_mj(self) -> float:
        """Fusion yield per shot in Megajoules."""
        return self.p.driver_energy_mj * self.p.target_gain

    def required_repetition_rate_hz(self) -> float:
        """Required laser repetition rate in Hz to achieve nominal thermal power."""
        yield_j = self.yield_per_shot_mj() * 1e6
        nominal_power_w = self.p.plant_thermal_power_mw * 1e6
        return nominal_power_w / yield_j

    def daily_target_consumption(self) -> float:
        """Number of targets consumed per calendar day at capacity factor."""
        rep_rate = self.required_repetition_rate_hz()
        return rep_rate * 86400.0 * self.p.capacity_factor

    def annual_target_consumption(self) -> float:
        """Total targets consumed per year."""
        return self.daily_target_consumption() * 365.25

    def gross_electrical_per_shot_kwh(self) -> float:
        """Gross electricity generated per target shot in kWh."""
        thermal_yield_mj = self.yield_per_shot_mj()
        electric_mj = thermal_yield_mj * self.p.thermal_efficiency
        return (electric_mj * 1e6) / 3.6e6  # 3.6 MJ = 1 kWh

    def target_cost_economic_ceiling_usd(self) -> float:
        """
        Maximum allowable target manufacturing cost ($) such that target cost
        does not exceed fuel_cost_fraction_limit of gross electricity revenue.
        """
        kwh = self.gross_electrical_per_shot_kwh()
        revenue_per_shot = kwh * self.p.electricity_price_per_kwh
        return revenue_per_shot * self.p.fuel_cost_fraction_limit

    def laser_wall_plug_energy_per_shot_mj(self) -> float:
        """Electrical energy consumed by laser driver per shot in MJ."""
        return self.p.driver_energy_mj / self.p.laser_wall_plug_efficiency

    def recirculating_power_fraction(self) -> float:
        """
        Total recirculating power fraction f_recirc = P_recirc / P_gross.
        """
        gross_elec_mj = self.yield_per_shot_mj() * self.p.thermal_efficiency
        laser_elec_mj = self.laser_wall_plug_energy_per_shot_mj()
        laser_recirc = laser_elec_mj / gross_elec_mj
        return laser_recirc + self.p.auxiliary_power_fraction

    def engineering_gain(self) -> float:
        """Engineering gain Q_eng = P_gross / P_recirc = 1 / f_recirc."""
        f_rec = self.recirculating_power_fraction()
        if f_rec <= 0.0:
            return float('inf')
        return 1.0 / f_rec

    def net_electrical_power_mwe(self) -> float:
        """Net electrical power output in MWe."""
        gross_mwe = self.p.plant_thermal_power_mw * self.p.thermal_efficiency
        f_rec = self.recirculating_power_fraction()
        return gross_mwe * (1.0 - f_rec)

    def final_optics_fast_neutron_flux(self) -> float:
        """
        14.1 MeV fast neutron flux at final optic surface (neutrons / m^2 / s).
        Assuming 80% of D-T fusion energy is carried by 14.1 MeV neutrons.
        """
        yield_j = self.yield_per_shot_mj() * 1e6
        neutron_energy_per_shot_j = 0.80 * yield_j
        e_14mev_j = 14.06 * 1e6 * E_CHARGE
        neutrons_per_shot = neutron_energy_per_shot_j / e_14mev_j
        hz = self.required_repetition_rate_hz()
        neutrons_per_sec = neutrons_per_shot * hz

        # Chamber surface area at final optics distance
        area = 4.0 * math.pi * (self.p.chamber_radius_m ** 2)
        return neutrons_per_sec / area


# ==============================================================================
# 2. MAGNETO-INERTIAL PULSED FRC (D-He3 / HELION ARCHETYPE) ENGINE
# ==============================================================================

@dataclass
class HelionFRCParameters:
    plant_thermal_power_mw: float = 150.0   # 150 MWth nominal
    capacity_factor: float = 0.80
    global_terrestrial_he3_kg: float = 30.0 # US DOE & global stockpile
    compression_efficiency: float = 0.85    # Capacitor bank to magnetic compression
    recovery_efficiency: float = 0.80       # Inductive direct expansion recovery
    operating_temperature_kev: float = 75.0 # Required for D-He3
    electron_temperature_kev: float = 65.0


class HelionFRCEngine:
    """
    Evaluates physical, fuel inventory, parasitic D-D neutronics,
    and Bremsstrahlung limits for pulsed D-He3 FRC schemes.
    """
    def __init__(self, params: HelionFRCParameters = None):
        self.p = params if params is not None else HelionFRCParameters()

    def annual_he3_burn_kg(self) -> float:
        """
        Annual Helium-3 mass consumed in kg/year for nominal thermal power.
        Reaction: D + He3 -> p (14.68 MeV) + alpha (3.67 MeV) = 18.354 MeV.
        """
        reactions_per_sec = (self.p.plant_thermal_power_mw * 1e6) / Q_DHE3_J
        kg_per_sec = reactions_per_sec * M_HE3_KG
        return kg_per_sec * SECONDS_PER_YEAR * self.p.capacity_factor

    def years_to_exhaust_global_stockpile(self) -> float:
        """Years until a single plant exhausts the entire global terrestrial He-3 reserve."""
        annual_burn = self.annual_he3_burn_kg()
        if annual_burn <= 0:
            return float('inf')
        return self.p.global_terrestrial_he3_kg / annual_burn

    def parasitic_dd_neutron_and_tritium_rates(self) -> Dict[str, float]:
        """
        If a plant attempts to breed its own He-3 from D-D reactions:
        Branch 1 (50%): D + D -> n (2.45 MeV) + He3 (0.82 MeV)
        Branch 2 (50%): D + D -> p (3.02 MeV) + T (1.01 MeV)
        Breeding 1 atom of He-3 inherently breeds 1 atom of Tritium and 1 2.45 MeV neutron.
        In-situ: In a D-D plasma, cross-section for D-T fusion is ~100x larger than D-D.
        Tritium burns promptly with deuterium: D + T -> alpha (3.5 MeV) + n (14.1 MeV).
        """
        annual_he3_needed_kg = self.annual_he3_burn_kg()
        he3_atoms_needed = (annual_he3_needed_kg) / M_HE3_KG

        # For every He3 atom produced, exactly one Tritium atom is produced
        tritium_bred_kg = he3_atoms_needed * M_TRITIUM_KG

        # 2.45 MeV neutron production
        dd_neutrons_per_yr = he3_atoms_needed
        dd_neutron_energy_gj = (dd_neutrons_per_yr * 2.45 * 1e6 * E_CHARGE) / 1e9

        # In-situ prompt D-T burn: 100% of bred tritium burns with deuterium
        dt_14mev_neutrons_per_yr = he3_atoms_needed
        dt_neutron_energy_gj = (dt_14mev_neutrons_per_yr * 14.06 * 1e6 * E_CHARGE) / 1e9

        total_neutron_energy_gj = dd_neutron_energy_gj + dt_neutron_energy_gj
        total_neutron_power_mw = (total_neutron_energy_gj * 1e9) / (SECONDS_PER_YEAR * self.p.capacity_factor)

        return {
            "tritium_co_produced_kg_yr": tritium_bred_kg,
            "dd_2_45_mev_neutrons_per_yr": dd_neutrons_per_yr,
            "dt_14_1_mev_neutrons_per_yr": dt_14mev_neutrons_per_yr,
            "dd_neutron_energy_gj_yr": dd_neutron_energy_gj,
            "dt_neutron_energy_gj_yr": dt_neutron_energy_gj,
            "total_neutron_power_mw": total_neutron_power_mw,
            "total_neutron_energy_fraction_of_thermal": total_neutron_power_mw / self.p.plant_thermal_power_mw
        }

    def bremsstrahlung_to_fusion_power_ratio(self) -> float:
        """
        Computes Bremsstrahlung radiation loss vs fusion power for 1:1 D-He3 mixture
        at the specified operating temperatures.
        Z_eff for 1:1 D:He3 mixture:
        n_D = n_0, n_He3 = n_0 -> n_e = n_D + 2*n_He3 = 3 n_0
        Z_eff = (n_D * 1^2 + n_He3 * 2^2) / n_e = (1 + 4) / 3 = 5/3 = 1.667.
        Bosch-Hale / Miley cross-section for D-He3 at 75 keV:
        <sigma v> ~ 1.2e-22 m^3/s.
        """
        # Cross section at 75 keV in m^3/s
        sigmav = 1.2e-22
        t_e_kev = self.p.electron_temperature_kev
        z_eff = 5.0 / 3.0

        # Bremsstrahlung power density coefficient (W m^3 / keV^0.5)
        # P_br = 5.35e-37 * n_e^2 * Z_eff * sqrt(T_e) * (1 + 2*T_e/511)
        rel_factor = 1.0 + (2.0 * t_e_kev / 511.0)
        p_brem_coeff = 5.35e-37 * (3.0**2) * z_eff * math.sqrt(t_e_kev) * rel_factor

        # Fusion power density: P_fus = n_D * n_He3 * Q_fus = n_0 * n_0 * Q_fus
        p_fus_coeff = sigmav * Q_DHE3_J

        return p_brem_coeff / p_fus_coeff


# ==============================================================================
# 3. ADVANCED MODULAR STELLARATOR ENGINE (W7-X / PROXIMA ARCHETYPE)
# ==============================================================================

@dataclass
class StellaratorParameters:
    major_radius_m: float = 5.5
    minor_radius_m: float = 1.0
    field_on_axis_t: float = 7.0
    peak_field_on_coil_t: float = 14.0
    rebco_cable_thickness_m: float = 0.025     # 25 mm thick high-current cable
    min_coil_bend_radius_m: float = 0.45       # Tightest 3D modular coil bend
    max_allowable_rebco_strain: float = 0.004  # 0.40% critical strain limit
    fast_alpha_loss_fraction: float = 0.22     # 22% collisionless prompt loss
    fusion_alpha_power_mw: float = 100.0       # 100 MW of 3.5 MeV alphas (500 MWth DT)
    localized_loss_area_m2: float = 0.60       # Concentrated alpha strike area
    blanket_geometric_coverage: float = 0.65   # 65% blanket coverage (limited by coils)
    local_1d_tbr: float = 1.35                 # Ideal 1D TBR with Be multiplier


class StellaratorLimitsEngine:
    """
    Evaluates 3D modular coil bending strain, energetic alpha prompt loss,
    and geometric blanket coverage limits in advanced stellarators.
    """
    def __init__(self, params: StellaratorParameters = None):
        self.p = params if params is not None else StellaratorParameters()

    def peak_coil_bending_strain(self) -> float:
        """
        Peak mechanical bending strain in REBCO cable on tightest 3D modular curve:
        epsilon = cable_thickness / (2 * R_bend).
        """
        return self.p.rebco_cable_thickness_m / (2.0 * self.p.min_coil_bend_radius_m)

    def strain_safety_factor(self) -> float:
        """
        Ratio of allowable strain limit to actual peak bending strain.
        Safety factor < 1.0 indicates mechanical conductor failure / delamination.
        """
        strain = self.peak_coil_bending_strain()
        return self.p.max_allowable_rebco_strain / strain

    def min_allowable_bend_radius_m(self) -> float:
        """Minimum bend radius (m) required to avoid exceeding REBCO strain limit."""
        return self.p.rebco_cable_thickness_m / (2.0 * self.p.max_allowable_rebco_strain)

    def localized_alpha_heat_flux_mw_m2(self) -> float:
        """
        Peak localized heat flux (MW/m^2) on first wall from unconfined
        prompt-loss fast 3.5 MeV alpha particles.
        """
        lost_alpha_power_mw = self.p.fast_alpha_loss_fraction * self.p.fusion_alpha_power_mw
        return lost_alpha_power_mw / self.p.localized_loss_area_m2

    def homogeneous_3d_tbr(self) -> float:
        """
        Homogeneous 3D Tritium Breeding Ratio accounting for non-planar coil
        crowding and blanket cutouts:
        TBR_3D = Coverage * TBR_local.
        """
        return self.p.blanket_geometric_coverage * self.p.local_1d_tbr


# ==============================================================================
# 4. NUCLEAR PLANT EPC & REGULATORY CRITICAL PATH TIMELINE ENGINE
# ==============================================================================

@dataclass
class EPCPhase:
    name: str
    duration_months_optimistic: int
    duration_months_baseline: int
    duration_months_historical_slip: int
    predecessors: List[str]


class NuclearEPCCriticalPathEngine:
    """
    Computes Critical Path Method (CPM) calendar timelines from October 2026
    to commercial grid operation across optimistic, baseline, and historical
    nuclear project slip scenarios.
    """
    def __init__(self, start_year: float = 2026.75): # Oct 1, 2026 = 2026.75
        self.start_year = start_year
        self.phases: Dict[str, EPCPhase] = {
            "PHASE_1_PROTOTYPE_Q": EPCPhase(
                "Scientific Gain Demonstration (Q>1)", 24, 30, 36, []
            ),
            "PHASE_2_FEED_DESIGN": EPCPhase(
                "Front-End Engineering Design (FEED)", 18, 24, 36, ["PHASE_1_PROTOTYPE_Q"]
            ),
            "PHASE_3_REGULATORY_PERMIT": EPCPhase(
                "Site Permitting & Environmental Review", 36, 48, 60, ["PHASE_2_FEED_DESIGN"]
            ),
            "PHASE_4_LONG_LEAD_PROCURE": EPCPhase(
                "Long-Lead Component Procurement (HTS, Cryostat)", 36, 48, 60, ["PHASE_2_FEED_DESIGN"]
            ),
            "PHASE_5_CIVIL_CONSTRUCTION": EPCPhase(
                "Civil & Nuclear Island Construction", 36, 48, 66, ["PHASE_3_REGULATORY_PERMIT", "PHASE_4_LONG_LEAD_PROCURE"]
            ),
            "PHASE_6_INTEGRATED_ASSEMBLY": EPCPhase(
                "Tokamak Core Assembly & BOP Hookup", 18, 24, 36, ["PHASE_5_CIVIL_CONSTRUCTION"]
            ),
            "PHASE_7_COLD_COMMISSIONING": EPCPhase(
                "Cryogenic Cooldown & Magnet Energization", 10, 12, 18, ["PHASE_6_INTEGRATED_ASSEMBLY"]
            ),
            "PHASE_8_FIRST_PLASMA_DD": EPCPhase(
                "First Plasma & Fuel Handling Shakedown", 10, 12, 18, ["PHASE_7_COLD_COMMISSIONING"]
            ),
            "PHASE_9_GRID_SYNCHRONIZATION": EPCPhase(
                "D-T Power Escalation & Commercial Grid Sync", 6, 12, 18, ["PHASE_8_FIRST_PLASMA_DD"]
            )
        }

    def compute_critical_path(self, mode: str = "baseline") -> Dict[str, Any]:
        """
        Computes the critical path duration and completion dates.
        mode: 'optimistic', 'baseline', or 'historical_slip'.
        """
        # Forward pass CPM
        earliest_start: Dict[str, int] = {}
        earliest_finish: Dict[str, int] = {}

        for phase_id, phase in self.phases.items():
            if mode == "optimistic":
                duration = phase.duration_months_optimistic
            elif mode == "historical_slip":
                duration = phase.duration_months_historical_slip
            else:
                duration = phase.duration_months_baseline

            if not phase.predecessors:
                es = 0
            else:
                es = max(earliest_finish[pred] for pred in phase.predecessors)

            ef = es + duration
            earliest_start[phase_id] = es
            earliest_finish[phase_id] = ef

        total_months = max(earliest_finish.values())
        total_years = total_months / 12.0
        completion_year = self.start_year + total_years

        # Detailed schedule breakdown
        schedule = []
        for phase_id, phase in self.phases.items():
            es = earliest_start[phase_id]
            ef = earliest_finish[phase_id]
            schedule.append({
                "phase_id": phase_id,
                "name": phase.name,
                "start_month": es,
                "finish_month": ef,
                "start_calendar_year": self.start_year + (es / 12.0),
                "finish_calendar_year": self.start_year + (ef / 12.0),
                "duration_months": ef - es
            })

        return {
            "mode": mode,
            "total_duration_months": total_months,
            "total_duration_years": total_years,
            "start_year": self.start_year,
            "completion_year": completion_year,
            "is_achievable_by_2040": completion_year <= 2040.0,
            "schedule": schedule
        }


# ==============================================================================
# 5. GRAND UNIFIED FUSION CONSILIENCE AUDIT
# ==============================================================================

class UnifiedFusionConsilienceEngine:
    """
    Integrates results across all 6 fusion paradigms and EPC timeline calculations
    to produce the definitive consilience score.
    """
    def __init__(self):
        self.icf = LaserICFEngine()
        self.frc = HelionFRCEngine()
        self.stel = StellaratorLimitsEngine()
        self.epc = NuclearEPCCriticalPathEngine()

    def audit_all_architectures(self) -> Dict[str, Any]:
        """Runs comparative evaluations across all non-tokamak and timeline metrics."""
        icf_metrics = {
            "rep_rate_hz": self.icf.required_repetition_rate_hz(),
            "daily_targets": self.icf.daily_target_consumption(),
            "max_target_cost_usd": self.icf.target_cost_economic_ceiling_usd(),
            "recirc_fraction": self.icf.recirculating_power_fraction(),
            "optics_neutron_flux": self.icf.final_optics_fast_neutron_flux()
        }

        frc_metrics = {
            "annual_he3_burn_kg": self.frc.annual_he3_burn_kg(),
            "years_to_deplete_stockpile": self.frc.years_to_exhaust_global_stockpile(),
            "parasitic_neutrons": self.frc.parasitic_dd_neutron_and_tritium_rates(),
            "brem_to_fus_ratio": self.frc.bremsstrahlung_to_fusion_power_ratio()
        }

        stel_metrics = {
            "peak_strain": self.stel.peak_coil_bending_strain(),
            "strain_safety_factor": self.stel.strain_safety_factor(),
            "min_bend_radius_m": self.stel.min_allowable_bend_radius_m(),
            "alpha_loss_heat_flux_mw_m2": self.stel.localized_alpha_heat_flux_mw_m2(),
            "tbr_3d": self.stel.homogeneous_3d_tbr()
        }

        epc_opt = self.epc.compute_critical_path("optimistic")
        epc_base = self.epc.compute_critical_path("baseline")
        epc_slip = self.epc.compute_critical_path("historical_slip")

        return {
            "icf": icf_metrics,
            "frc_he3": frc_metrics,
            "stellarator": stel_metrics,
            "timeline": {
                "optimistic_completion": epc_opt["completion_year"],
                "baseline_completion": epc_base["completion_year"],
                "historical_slip_completion": epc_slip["completion_year"],
                "optimistic_by_2040": epc_opt["is_achievable_by_2040"],
                "baseline_by_2040": epc_base["is_achievable_by_2040"]
            }
        }
