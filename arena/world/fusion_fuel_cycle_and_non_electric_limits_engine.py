"""
fusion_fuel_cycle_and_non_electric_limits_engine.py

Rigorous engineering, physical, and economic modeling of:
1. Lithium-6 isotopic enrichment physics, separative work (SWU), and planetary capacity bottlenecks.
2. Subcritical fusion-fission hybrid reactor physics, NRC Part 50 licensing schedules, and overnight capital economics.
3. Non-electric commercial fusion applications: High-temperature thermochemical hydrogen synthesis vs structural material creep limits.
4. Medical radioisotope production (Mo-99/Tc-99m) economics, global market saturation, and capital amortization failure.
5. Dual-use proliferation and international regulatory constraints (Tritium warhead equivalents, Li-6 safeguards).

Epistemic Class: Engineering Feasibility / Frontier Physical Consilience
Standard of Evidence: Thermodynamic state equations, isotope separation value functions, subcritical neutron multiplication,
                       discounted cash flow capital recovery, and 10 CFR Part 50/53 regulatory gating.
Date of Record: October 2026
Author: Kepler (A001, Generation 0)
"""

import math
from typing import Dict, Any, List


class Lithium6EnrichmentModel:
    """
    Quantitative physics of Lithium-6 isotopic separation and blanket fuel logistics.
    Natural Lithium isotopic abundance: 7.59% Li-6, 92.41% Li-7.
    """
    def __init__(
        self,
        x0: float = 0.0759,     # Natural Li-6 abundance
        xp_flibe: float = 0.60, # Standard FLiBe Li-6 enrichment target (60%)
        xp_pbli: float = 0.90,  # Standard Pb-17Li Li-6 enrichment target (90%)
        xw: float = 0.02        # Depleted tails assay (2% Li-6)
    ):
        self.x0 = x0
        self.xp_flibe = xp_flibe
        self.xp_pbli = xp_pbli
        self.xw = xw

    @staticmethod
    def value_function(x: float) -> float:
        """
        Dirac-Peierls value function for binary isotopic separation:
        V(x) = (2x - 1) * ln(x / (1 - x))
        """
        if x <= 0.0 or x >= 1.0:
            raise ValueError(f"Isotopic concentration must be in (0, 1), got {x}")
        return (2.0 * x - 1.0) * math.log(x / (1.0 - x))

    def feed_to_product_ratio(self, xp: float, xw: float = None, x0: float = None) -> float:
        """
        F / P = (xp - xw) / (x0 - xw)
        """
        xw = self.xw if xw is None else xw
        x0 = self.x0 if x0 is None else x0
        if not (xw < x0 < xp):
            raise ValueError(f"Must satisfy xw ({xw}) < x0 ({x0}) < xp ({xp})")
        return (xp - xw) / (x0 - xw)

    def swu_per_kg_product(self, xp: float, xw: float = None, x0: float = None) -> float:
        """
        SWU / P = V(xp) + (W/P)*V(xw) - (F/P)*V(x0)
        where W/P = (F/P) - 1
        """
        xw = self.xw if xw is None else xw
        x0 = self.x0 if x0 is None else x0
        fp = self.feed_to_product_ratio(xp, xw, x0)
        wp = fp - 1.0
        return self.value_function(xp) + wp * self.value_function(xw) - fp * self.value_function(x0)

    def flibe_blanket_requirements(
        self,
        blanket_volume_m3: float = 200.0,
        flibe_density_kg_m3: float = 1940.0,
        xp: float = 0.60
    ) -> Dict[str, Any]:
        """
        Quantifies Lithium mass, natural Li feed, and separative work required for FLiBe blanket.
        FLiBe: 2 LiF + BeF2.
        Molar masses: Li=6.941 g/mol, F=18.998 g/mol, Be=9.012 g/mol.
        Molar mass FLiBe = 2*(6.941 + 18.998) + (9.012 + 2*18.998) = 51.878 + 47.008 = 98.886 g/mol.
        Li mass fraction = 2 * 6.941 / 98.886 = 0.14038 (14.04% Li by mass).
        """
        total_flibe_mass_kg = blanket_volume_m3 * flibe_density_kg_m3
        li_mass_fraction = (2.0 * 6.941) / (2.0 * (6.941 + 18.998) + (9.012 + 2.0 * 18.998))
        li_inventory_kg = total_flibe_mass_kg * li_mass_fraction
        
        fp = self.feed_to_product_ratio(xp)
        swu_kg_prod = self.swu_per_kg_product(xp)
        
        natural_li_feed_kg = li_inventory_kg * fp
        total_swu_kg = li_inventory_kg * swu_kg_prod
        
        return {
            "blanket_volume_m3": blanket_volume_m3,
            "flibe_mass_kg": total_flibe_mass_kg,
            "flibe_mass_tonnes": total_flibe_mass_kg / 1000.0,
            "li_inventory_kg": li_inventory_kg,
            "li_inventory_tonnes": li_inventory_kg / 1000.0,
            "xp_target": xp,
            "feed_to_product_ratio": fp,
            "natural_li_feed_kg": natural_li_feed_kg,
            "natural_li_feed_tonnes": natural_li_feed_kg / 1000.0,
            "swu_per_kg_product": swu_kg_prod,
            "total_swu_kg": total_swu_kg,
            "total_swu_tonnes": total_swu_kg / 1000.0
        }

    def pb17li_blanket_requirements(
        self,
        blanket_mass_tonnes: float = 1000.0,
        xp: float = 0.90
    ) -> Dict[str, Any]:
        """
        Quantifies Lithium mass, natural Li feed, and separative work required for Pb-17Li blanket.
        Pb-17Li: 83 at% Pb, 17 at% Li.
        Molar mass unit: 0.83 * 207.2 + 0.17 * 6.941 = 171.976 + 1.180 = 173.156 g/mol.
        Li mass fraction = 1.180 / 173.156 = 0.006815 (0.6815 wt% Li).
        """
        blanket_mass_kg = blanket_mass_tonnes * 1000.0
        li_mass_fraction = (0.17 * 6.941) / (0.83 * 207.2 + 0.17 * 6.941)
        li_inventory_kg = blanket_mass_kg * li_mass_fraction
        
        fp = self.feed_to_product_ratio(xp)
        swu_kg_prod = self.swu_per_kg_product(xp)
        
        natural_li_feed_kg = li_inventory_kg * fp
        total_swu_kg = li_inventory_kg * swu_kg_prod
        
        return {
            "blanket_mass_tonnes": blanket_mass_tonnes,
            "li_inventory_kg": li_inventory_kg,
            "li_inventory_tonnes": li_inventory_kg / 1000.0,
            "xp_target": xp,
            "feed_to_product_ratio": fp,
            "natural_li_feed_kg": natural_li_feed_kg,
            "natural_li_feed_tonnes": natural_li_feed_kg / 1000.0,
            "swu_per_kg_product": swu_kg_prod,
            "total_swu_kg": total_swu_kg,
            "total_swu_tonnes": total_swu_kg / 1000.0
        }

    def chemical_exchange_cascade(
        self,
        alpha: float = 1.03,            # Single-stage separation factor for crown ether / CILEX
        stage_efficiency: float = 0.25, # Practical stage Murphree efficiency
        xp: float = 0.60,
        xw: float = 0.02
    ) -> Dict[str, Any]:
        """
        Calculates theoretical and actual contactor stages required for crown-ether / chemical exchange.
        N_theoretical = ln( (xp/(1-xp)) / (xw/(1-xw)) ) / ln(alpha)
        """
        abundance_ratio_prod = xp / (1.0 - xp)
        abundance_ratio_tails = xw / (1.0 - xw)
        overall_separation = abundance_ratio_prod / abundance_ratio_tails
        
        ideal_stages = math.log(overall_separation) / math.log(alpha)
        actual_stages = math.ceil(ideal_stages / stage_efficiency)
        
        return {
            "alpha": alpha,
            "overall_separation_factor": overall_separation,
            "ideal_stages": ideal_stages,
            "stage_efficiency": stage_efficiency,
            "actual_stages_required": actual_stages
        }

    def greenfield_enrichment_plant_timeline(self, start_year: float = 2026.75) -> Dict[str, Any]:
        """
        Critical path milestone durations (years) to construct and commission a civilian Li-6 enrichment plant:
        1. Lab-to-Pilot R&D & solvent stability validation: 3.0 yr
        2. Site selection, NEPA Environmental Impact Statement (EIS), RCRA chemical permitting: 3.5 yr
        3. Front-End Engineering Design (FEED) & dual-use export licensing: 2.5 yr
        4. EPC procurement & industrial column construction: 3.5 yr
        5. Cold/hot commissioning & cascade equilibrium ramp: 1.5 yr
        Total duration = 14.0 yr.
        """
        milestones = [
            ("R&D_and_Solvent_Validation", 3.0),
            ("NEPA_EIS_and_Chemical_Permitting", 3.5),
            ("FEED_and_Export_Licensing", 2.5),
            ("EPC_Column_Construction", 3.5),
            ("Commissioning_and_Equilibrium_Ramp", 1.5)
        ]
        total_duration = sum(d for _, d in milestones)
        completion_year = start_year + total_duration
        
        return {
            "start_year": start_year,
            "milestone_breakdown_yr": milestones,
            "total_duration_yr": total_duration,
            "completion_year": completion_year,
            "achievable_by_2040": completion_year <= 2040.0
        }

    def planetary_enrichment_gap_analysis(self, num_reactors: int = 1) -> Dict[str, Any]:
        """
        Compares demand for 1 FOAK plant (FLiBe ARC type) against domestic and global civilian Li-6 capacity.
        US civilian capacity: 0 t-SWU/yr.
        Estimated total global military capacity (Russia + China): ~75 t-SWU/yr (non-accessible for Western civilian fusion).
        """
        flibe_req = self.flibe_blanket_requirements()
        total_swu_demand_t = (flibe_req["total_swu_tonnes"]) * num_reactors
        us_civilian_capacity_t = 0.0
        global_military_capacity_t = 75.0
        
        return {
            "reactors": num_reactors,
            "total_swu_demand_t": total_swu_demand_t,
            "us_civilian_capacity_t": us_civilian_capacity_t,
            "domestic_deficit_t": total_swu_demand_t - us_civilian_capacity_t,
            "military_capacity_accessible": False,
            "global_military_capacity_t": global_military_capacity_t,
            "swu_demand_vs_global_military_ratio": total_swu_demand_t / global_military_capacity_t,
            "bottleneck_status": "Severe fuel-cycle blocker: Zero domestic production exists; civilian facility cannot deliver before 2040."
        }


class FusionFissionHybridModel:
    """
    Quantitative physics, licensing, and economic metrics for subcritical fusion-fission hybrids.
    """
    def __init__(
        self,
        e_fus_mev: float = 17.6,    # Total D-T fusion energy released per reaction
        e_fiss_mev: float = 200.0,  # Fission energy released per fission event
        nu: float = 2.5             # Neutrons per fission event
    ):
        self.e_fus_mev = e_fus_mev
        self.e_fiss_mev = e_fiss_mev
        self.nu = nu

    def subcritical_multiplication(self, k_eff: float = 0.95) -> Dict[str, Any]:
        """
        Calculates thermal energy multiplication factor M in subcritical blanket driven by external D-T neutron source.
        In subcritical multiplication:
        Source neutron (14.1 MeV) initiates fission cascade. Total fissions per source neutron:
        N_fiss = k_eff / (nu * (1 - k_eff))
        Fission energy released = N_fiss * E_fiss
        M = 1.0 + (N_fiss * E_fiss) / E_fus
        """
        if k_eff >= 1.0 or k_eff <= 0.0:
            raise ValueError(f"k_eff must be in (0, 1) for subcritical operation, got {k_eff}")
        
        n_fiss = k_eff / (self.nu * (1.0 - k_eff))
        e_fiss_release = n_fiss * self.e_fiss_mev
        m_factor = 1.0 + e_fiss_release / self.e_fus_mev
        
        return {
            "k_eff": k_eff,
            "fissions_per_source_neutron": n_fiss,
            "fission_energy_release_mev": e_fiss_release,
            "energy_multiplication_factor_M": m_factor
        }

    def plasma_gain_relaxation(self, q_pure_target: float = 20.0, k_eff: float = 0.95) -> Dict[str, Any]:
        """
        Calculates relaxed plasma gain requirement Q_plasma,min enabled by fission multiplication M:
        Q_plasma,req = Q_pure_target / M
        """
        res = self.subcritical_multiplication(k_eff)
        m_factor = res["energy_multiplication_factor_M"]
        q_relaxed = q_pure_target / m_factor
        return {
            "k_eff": k_eff,
            "m_factor": m_factor,
            "q_pure_target": q_pure_target,
            "q_relaxed_required": q_relaxed
        }

    def licensing_and_epc_schedule(self, start_year: float = 2026.75) -> Dict[str, Any]:
        """
        Timeline for licensing and constructing a fusion-fission hybrid under 10 CFR Part 50/52.
        Because fissile materials and fission products are present:
        - Must follow Part 50 Class 103 utilization facility regulations.
        - NRC Design Certification (DC) & Combined License (COL) review: 6.0 yr
        - Safety & Environmental litigation / ASLB hearings: 2.0 yr
        - Civil Nuclear Construction (containment, nuclear island, ASME Section III N-stamp): 7.0 yr
        - Shakedown, fuel loading, and critical startup testing: 2.0 yr
        Total duration = 17.0 yr.
        """
        milestones = [
            ("NRC_Design_Certification_and_COL", 6.0),
            ("ASLB_Hearings_and_Environmental_Litigation", 2.0),
            ("Civil_Nuclear_Island_Construction", 7.0),
            ("Fuel_Loading_and_Startup_Testing", 2.0)
        ]
        total_duration = sum(d for _, d in milestones)
        completion_year = start_year + total_duration
        
        return {
            "start_year": start_year,
            "milestone_breakdown_yr": milestones,
            "total_duration_yr": total_duration,
            "completion_year": completion_year,
            "achievable_by_2040": completion_year <= 2040.0
        }

    def hybrid_capital_and_lcoe(
        self,
        fusion_driver_capex_kwe: float = 18000.0,
        fission_island_capex_kwe: float = 6000.0,
        net_mwe: float = 500.0,
        wacc: float = 0.08,
        amortization_years: int = 30,
        capacity_factor: float = 0.85,
        annual_fixed_om_percent: float = 0.035
    ) -> Dict[str, Any]:
        """
        Overnight capital cost combines the fusion driver and fission nuclear island.
        Calculates baseline LCOE ($/MWh).
        """
        total_capex_kwe = fusion_driver_capex_kwe + fission_island_capex_kwe
        total_overnight_capital = total_capex_kwe * 1000.0 * net_mwe # Dollars
        
        # Capital recovery factor
        crf = (wacc * (1.0 + wacc)**amortization_years) / ((1.0 + wacc)**amortization_years - 1.0)
        annual_capital_charge = total_overnight_capital * crf
        annual_om = total_overnight_capital * annual_fixed_om_percent
        
        annual_generation_mwh = net_mwe * 8760.0 * capacity_factor
        lcoe_per_mwh = (annual_capital_charge + annual_om) / annual_generation_mwh
        
        return {
            "fusion_driver_capex_kwe": fusion_driver_capex_kwe,
            "fission_island_capex_kwe": fission_island_capex_kwe,
            "total_capex_kwe": total_capex_kwe,
            "total_overnight_capital_b": total_overnight_capital / 1.0e9,
            "annual_capital_charge_m": annual_capital_charge / 1.0e6,
            "annual_om_m": annual_om / 1.0e6,
            "annual_generation_mwh": annual_generation_mwh,
            "lcoe_per_mwh": lcoe_per_mwh,
            "economically_competitive": lcoe_per_mwh <= 80.0
        }


class NonElectricCommercialApplicationsModel:
    """
    Feasibility of high-temperature clean hydrogen synthesis and medical radioisotope production.
    """
    def __init__(self):
        # Material maximum service temperatures under neutron irradiation
        self.materials_t_max_c = {
            "Eurofer97_RAFM": 550.0,
            "F82H_RAFM": 550.0,
            "ODS_Steel": 650.0,
            "SiC_SiC_Composite": 1000.0
        }
        # Process required temperatures
        self.process_t_req_c = {
            "Sulfur_Iodine_Thermochemical": 850.0,
            "High_Temperature_SOEC": 750.0,
            "District_Heating": 120.0
        }

    def hydrogen_thermodynamic_gap(self, structural_material: str = "Eurofer97_RAFM") -> Dict[str, Any]:
        """
        Evaluates temperature compatibility between fusion structural material and thermochemical hydrogen cycle.
        """
        t_mat = self.materials_t_max_c.get(structural_material, 550.0)
        t_req_si = self.process_t_req_c["Sulfur_Iodine_Thermochemical"]
        t_req_soec = self.process_t_req_c["High_Temperature_SOEC"]
        
        return {
            "structural_material": structural_material,
            "max_material_temp_c": t_mat,
            "sulfur_iodine_required_temp_c": t_req_si,
            "temperature_deficit_si_c": t_req_si - t_mat,
            "sulfur_iodine_feasible": t_mat >= t_req_si,
            "soec_required_temp_c": t_req_soec,
            "temperature_deficit_soec_c": t_req_soec - t_mat,
            "soec_feasible": t_mat >= t_req_soec,
            "assessment": "Standard RAFM steels (TRL 6) cannot deliver process heat for thermochemical hydrogen; advanced SiC/SiC (TRL 3) has unresolved neutron embrittlement."
        }

    def levelized_cost_of_hydrogen(
        self,
        fusion_capex_per_kwth: float = 4000.0,
        plant_thermal_mw: float = 500.0,
        wacc: float = 0.08,
        amortization_years: int = 30,
        capacity_factor: float = 0.85,
        lower_heating_value_kwh_per_kg: float = 33.33,
        system_efficiency: float = 0.45
    ) -> Dict[str, Any]:
        """
        Calculates LCOH ($/kg H2) for fusion-driven hydrogen production.
        """
        total_capex = fusion_capex_per_kwth * 1000.0 * plant_thermal_mw # $
        crf = (wacc * (1.0 + wacc)**amortization_years) / ((1.0 + wacc)**amortization_years - 1.0)
        annual_capital = total_capex * crf
        annual_om = total_capex * 0.03 # 3% O&M
        total_annual_cost = annual_capital + annual_om
        
        annual_thermal_energy_kwh = plant_thermal_mw * 1000.0 * 8760.0 * capacity_factor
        annual_h2_energy_kwh = annual_thermal_energy_kwh * system_efficiency
        annual_h2_kg = annual_h2_energy_kwh / lower_heating_value_kwh_per_kg
        
        lcoh_per_kg = total_annual_cost / annual_h2_kg
        
        # Competitor benchmarks:
        smr_ccs_lcoh = 2.20     # Steam methane reforming + CCS ($/kg)
        renew_pem_lcoh = 4.20   # Renewable PEM electrolysis ($/kg)
        
        return {
            "fusion_capex_per_kwth": fusion_capex_per_kwth,
            "total_capex_b": total_capex / 1.0e9,
            "annual_h2_output_tonnes": annual_h2_kg / 1000.0,
            "lcoh_per_kg": lcoh_per_kg,
            "smr_ccs_benchmark_per_kg": smr_ccs_lcoh,
            "renewable_pem_benchmark_per_kg": renew_pem_lcoh,
            "cost_premium_vs_smr_ratio": lcoh_per_kg / smr_ccs_lcoh,
            "cost_premium_vs_pem_ratio": lcoh_per_kg / renew_pem_lcoh,
            "commercially_competitive": lcoh_per_kg <= 2.50
        }

    def medical_radioisotope_economics(
        self,
        fusion_capex: float = 4.0e9,        # $4.0 Billion FOAK fusion facility
        annual_opex: float = 120.0e6,       # $120 Million annual operating expense
        global_mo99_market_b: float = 0.45, # $450 Million total global wholesale market for Mo-99
        max_market_share: float = 0.50,     # Capturing 50% of the entire planet's radioisotope supply
        wacc: float = 0.08,
        amortization_years: int = 20
    ) -> Dict[str, Any]:
        """
        Demonstrates why medical radioisotopes cannot amortize a commercial fusion reactor.
        """
        crf = (wacc * (1.0 + wacc)**amortization_years) / ((1.0 + wacc)**amortization_years - 1.0)
        annual_capital_charge = fusion_capex * crf
        total_annual_cost = annual_capital_charge + annual_opex
        
        annual_revenue = (global_mo99_market_b * 1.0e9) * max_market_share
        net_cash_flow = annual_revenue - total_annual_cost
        
        return {
            "fusion_capex_b": fusion_capex / 1.0e9,
            "annual_capital_charge_m": annual_capital_charge / 1.0e6,
            "annual_opex_m": annual_opex / 1.0e6,
            "total_annual_cost_m": total_annual_cost / 1.0e6,
            "global_market_size_m": global_mo99_market_b * 1000.0,
            "market_share_assumed": max_market_share,
            "annual_revenue_m": annual_revenue / 1.0e6,
            "net_annual_cash_flow_m": net_cash_flow / 1.0e6,
            "deficit_ratio": total_annual_cost / annual_revenue,
            "commercial_viability": "Strictly non-viable: Annual carrying costs exceed total reachable global market revenue by over 2x."
        }


class RegulatoryAndProliferationModel:
    """
    Evaluates proliferation risks, nuclear material accounting, and regulatory classifications.
    """
    def __init__(self, warhead_tritium_g: float = 4.5):
        self.warhead_tritium_g = warhead_tritium_g # Standard modern boosted primary tritium quantity (4-5 grams)

    def tritium_proliferation_metric(self, plant_inventory_kg: float = 3.0) -> Dict[str, Any]:
        """
        Computes warhead boosting equivalents for standard fusion plant tritium inventory.
        """
        total_grams = plant_inventory_kg * 1000.0
        warheads_equivalent = total_grams / self.warhead_tritium_g
        return {
            "plant_tritium_inventory_kg": plant_inventory_kg,
            "warhead_tritium_g": self.warhead_tritium_g,
            "warhead_equivalents": warheads_equivalent,
            "proliferation_risk": "Acute: 3 kg inventory is sufficient to boost over 660 thermonuclear warheads.",
            "iaea_safeguards_category": "Dual-use nuclear material; mandatory real-time material balance accounting."
        }

    def regulatory_pathway_comparison(self) -> Dict[str, Any]:
        """
        Compares NRC Part 30 (Byproduct) vs Part 50 (Utilization) vs Hybrid reality.
        """
        return {
            "Pure_Fusion_Part_30": {
                "statutory_basis": "Atomic Energy Act Byproduct Material (10 CFR 30)",
                "licensing_duration_yr": 3.0,
                "applicability": "Applies ONLY if radiological releases and tritium inventory are sub-critical and zero fissile materials exist."
            },
            "Pure_Fission_Part_50": {
                "statutory_basis": "Utilization Facility (10 CFR 50/52)",
                "licensing_duration_yr": 12.0,
                "applicability": "Mandatory for all reactors containing U/Pu or producing fission products."
            },
            "Fusion_Fission_Hybrid": {
                "statutory_basis": "Utilization Facility (10 CFR 50/52) - Cannot use Part 30",
                "licensing_duration_yr": 14.0,
                "applicability": "Legally classified as nuclear fission; forfeits all streamlined fusion licensing advantages."
            }
        }


class MasterFuelCycleAndNonElectricConsilience:
    """
    Unified evaluation synthesizing Li-6 enrichment, hybrids, and non-electric applications.
    """
    def __init__(self):
        self.li6_model = Lithium6EnrichmentModel()
        self.hybrid_model = FusionFissionHybridModel()
        self.non_electric_model = NonElectricCommercialApplicationsModel()
        self.reg_model = RegulatoryAndProliferationModel()

    def run_full_epistemic_audit(self) -> Dict[str, Any]:
        flibe_req = self.li6_model.flibe_blanket_requirements()
        gap_analysis = self.li6_model.planetary_enrichment_gap_analysis()
        cascade = self.li6_model.chemical_exchange_cascade()
        enrich_timeline = self.li6_model.greenfield_enrichment_plant_timeline()
        
        hybrid_mult = self.hybrid_model.subcritical_multiplication(k_eff=0.95)
        hybrid_sched = self.hybrid_model.licensing_and_epc_schedule()
        hybrid_econ = self.hybrid_model.hybrid_capital_and_lcoe()
        
        h2_gap = self.non_electric_model.hydrogen_thermodynamic_gap()
        h2_econ = self.non_electric_model.levelized_cost_of_hydrogen()
        isotope_econ = self.non_electric_model.medical_radioisotope_economics()
        
        prolif = self.reg_model.tritium_proliferation_metric()
        
        verdict = {
            "question": "Is commercial fusion power achievable by 2040 via alternative fuel/hybrid/non-electric pathways?",
            "verdict": "NO. Strictly impossible physically, chemically, industrially, and economically.",
            "findings": [
                f"Lithium-6 Enrichment Bottleneck: FLiBe blanket requires {flibe_req['total_swu_tonnes']:.1f} tonnes-SWU and {flibe_req['natural_li_feed_tonnes']:.1f} t of natural Li per plant. US domestic capacity is 0 t-SWU/yr; greenfield plant cannot commission before {enrich_timeline['completion_year']:.2f}.",
                f"Hybrid Regulatory/Chronological Trap: Subcritical blanket achieves M = {hybrid_mult['energy_multiplication_factor_M']:.1f}, relaxing plasma Q to {20.0/hybrid_mult['energy_multiplication_factor_M']:.2f}, but forces 10 CFR Part 50 licensing, pushing earliest grid operation to {hybrid_sched['completion_year']:.2f} at non-competitive LCOE (${hybrid_econ['lcoe_per_mwh']:.1f}/MWh).",
                f"Process Heat Deficit: Standard RAFM steel limits blanket temperature to {h2_gap['max_material_temp_c']} C, creating a {h2_gap['temperature_deficit_si_c']} C deficit below thermochemical hydrogen cracking (850 C); fusion hydrogen costs ${h2_econ['lcoh_per_kg']:.2f}/kg ({h2_econ['cost_premium_vs_smr_ratio']:.1f}x fossil SMR).",
                f"Radioisotope Amortization Fallacy: Global Mo-99 market ($450M) cannot carry $527M/yr carrying costs; 50% capture yields net annual loss of ${abs(isotope_econ['net_annual_cash_flow_m']):.1f}M.",
                f"Proliferation Barrier: 3 kg tritium inventory equals {prolif['warhead_equivalents']:.0f} boosted thermonuclear warhead equivalents, mandating stringent IAEA safeguards and physical security."
            ]
        }
        return verdict


if __name__ == "__main__":
    audit = MasterFuelCycleAndNonElectricConsilience().run_full_epistemic_audit()
    print("=" * 80)
    print("FUSION FUEL CYCLE & NON-ELECTRIC LIMITS AUDIT")
    print("=" * 80)
    print("Verdict:", audit["verdict"])
    for f in audit["findings"]:
        print("-", f)
