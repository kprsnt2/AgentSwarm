"""
test_fusion_fuel_cycle_and_non_electric_limits_engine.py

Comprehensive unit test suite for fusion_fuel_cycle_and_non_electric_limits_engine.py.
Verifies all physical, chemical, logistical, and economic models for Lithium-6 enrichment,
fusion-fission hybrids, non-electric applications (H2 / Mo-99), and dual-use safeguards.
"""

import unittest
import math
from fusion_fuel_cycle_and_non_electric_limits_engine import (
    Lithium6EnrichmentModel,
    FusionFissionHybridModel,
    NonElectricCommercialApplicationsModel,
    RegulatoryAndProliferationModel,
    MasterFuelCycleAndNonElectricConsilience
)


class TestLithium6EnrichmentModel(unittest.TestCase):
    def setUp(self):
        self.model = Lithium6EnrichmentModel()

    def test_value_function_properties(self):
        # Dirac-Peierls value function must be 0 at x=0.5
        v_half = self.model.value_function(0.5)
        self.assertAlmostEqual(v_half, 0.0, places=5)
        # V(x) must be strictly positive for x != 0.5
        self.assertGreater(self.model.value_function(0.0759), 0.0)
        self.assertGreater(self.model.value_function(0.60), 0.0)
        self.assertGreater(self.model.value_function(0.90), 0.0)

    def test_feed_to_product_ratio(self):
        # F/P = (0.60 - 0.02) / (0.0759 - 0.02) = 0.58 / 0.0559 = 10.3756
        fp = self.model.feed_to_product_ratio(xp=0.60, xw=0.02, x0=0.0759)
        self.assertAlmostEqual(fp, 10.37567, places=4)

    def test_swu_per_kg_product(self):
        swu_kg = self.model.swu_per_kg_product(xp=0.60, xw=0.02, x0=0.0759)
        # Hand-calculated value: ~13.114 kg-SWU/kg product
        self.assertAlmostEqual(swu_kg, 13.1136, places=3)

    def test_flibe_blanket_requirements(self):
        res = self.model.flibe_blanket_requirements(blanket_volume_m3=200.0, xp=0.60)
        self.assertAlmostEqual(res["flibe_mass_tonnes"], 388.0, places=1)
        # Li mass in FLiBe is approx 14% -> ~54.5 tonnes
        self.assertAlmostEqual(res["li_inventory_tonnes"], 54.467, places=1)
        # Natural Li feed: ~565 tonnes
        self.assertAlmostEqual(res["natural_li_feed_tonnes"], 565.13, places=0)
        # SWU demand: ~714 tonnes-SWU
        self.assertAlmostEqual(res["total_swu_tonnes"], 714.26, places=0)

    def test_pb17li_blanket_requirements(self):
        res = self.model.pb17li_blanket_requirements(blanket_mass_tonnes=1000.0, xp=0.90)
        self.assertAlmostEqual(res["li_inventory_tonnes"], 6.815, places=2)
        self.assertGreater(res["natural_li_feed_tonnes"], 100.0)
        self.assertGreater(res["total_swu_tonnes"], 150.0)

    def test_chemical_exchange_cascade(self):
        res = self.model.chemical_exchange_cascade(alpha=1.03, stage_efficiency=0.25, xp=0.60, xw=0.02)
        # Ideal stages approx 145
        self.assertAlmostEqual(res["ideal_stages"], 145.38, places=1)
        # Actual stages with 25% efficiency = ceil(145.38 / 0.25) = 582
        self.assertEqual(res["actual_stages_required"], 582)

    def test_greenfield_enrichment_plant_timeline(self):
        res = self.model.greenfield_enrichment_plant_timeline(start_year=2026.75)
        self.assertEqual(res["total_duration_yr"], 14.0)
        self.assertAlmostEqual(res["completion_year"], 2040.75, places=2)
        self.assertFalse(res["achievable_by_2040"])

    def test_planetary_enrichment_gap_analysis(self):
        res = self.model.planetary_enrichment_gap_analysis(num_reactors=1)
        self.assertEqual(res["us_civilian_capacity_t"], 0.0)
        self.assertGreater(res["domestic_deficit_t"], 700.0)
        self.assertFalse(res["military_capacity_accessible"])
        self.assertGreater(res["swu_demand_vs_global_military_ratio"], 9.0)


class TestFusionFissionHybridModel(unittest.TestCase):
    def setUp(self):
        self.model = FusionFissionHybridModel()

    def test_subcritical_multiplication(self):
        # At keff = 0.95, M ~ 87.36
        res = self.model.subcritical_multiplication(k_eff=0.95)
        self.assertAlmostEqual(res["energy_multiplication_factor_M"], 87.3636, places=2)
        
        # At keff = 0.80, M ~ 19.18
        res80 = self.model.subcritical_multiplication(k_eff=0.80)
        self.assertAlmostEqual(res80["energy_multiplication_factor_M"], 19.1818, places=2)

    def test_plasma_gain_relaxation(self):
        res = self.model.plasma_gain_relaxation(q_pure_target=20.0, k_eff=0.95)
        self.assertLess(res["q_relaxed_required"], 0.3) # 20 / 87.36 = 0.229

    def test_hybrid_licensing_schedule(self):
        res = self.model.licensing_and_epc_schedule(start_year=2026.75)
        self.assertEqual(res["total_duration_yr"], 17.0)
        self.assertAlmostEqual(res["completion_year"], 2043.75, places=2)
        self.assertFalse(res["achievable_by_2040"])

    def test_hybrid_capital_and_lcoe(self):
        res = self.model.hybrid_capital_and_lcoe(
            fusion_driver_capex_kwe=18000.0,
            fission_island_capex_kwe=6000.0,
            net_mwe=500.0
        )
        self.assertEqual(res["total_capex_kwe"], 24000.0)
        self.assertAlmostEqual(res["total_overnight_capital_b"], 12.0, places=1)
        self.assertGreater(res["lcoe_per_mwh"], 300.0)
        self.assertFalse(res["economically_competitive"])


class TestNonElectricCommercialApplicationsModel(unittest.TestCase):
    def setUp(self):
        self.model = NonElectricCommercialApplicationsModel()

    def test_hydrogen_thermodynamic_gap(self):
        # Eurofer97 limit is 550 C, Sulfur-Iodine needs 850 C -> 300 C deficit
        res = self.model.hydrogen_thermodynamic_gap(structural_material="Eurofer97_RAFM")
        self.assertEqual(res["temperature_deficit_si_c"], 300.0)
        self.assertFalse(res["sulfur_iodine_feasible"])
        self.assertFalse(res["soec_feasible"])

    def test_levelized_cost_of_hydrogen(self):
        res = self.model.levelized_cost_of_hydrogen(fusion_capex_per_kwth=4000.0)
        self.assertGreater(res["lcoh_per_kg"], 4.5)
        self.assertGreater(res["cost_premium_vs_smr_ratio"], 2.0)
        self.assertFalse(res["commercially_competitive"])

    def test_medical_radioisotope_economics(self):
        res = self.model.medical_radioisotope_economics()
        self.assertAlmostEqual(res["total_annual_cost_m"], 527.4, places=1)
        self.assertAlmostEqual(res["annual_revenue_m"], 225.0, places=1)
        self.assertAlmostEqual(res["net_annual_cash_flow_m"], -302.4, places=1)
        self.assertGreater(res["deficit_ratio"], 2.0)


class TestRegulatoryAndProliferationModel(unittest.TestCase):
    def setUp(self):
        self.model = RegulatoryAndProliferationModel(warhead_tritium_g=4.5)

    def test_tritium_proliferation_metric(self):
        res = self.model.tritium_proliferation_metric(plant_inventory_kg=3.0)
        # 3000 g / 4.5 g = 666.67 warheads
        self.assertAlmostEqual(res["warhead_equivalents"], 666.67, places=1)

    def test_regulatory_pathway_comparison(self):
        res = self.model.regulatory_pathway_comparison()
        self.assertIn("Pure_Fusion_Part_30", res)
        self.assertIn("Fusion_Fission_Hybrid", res)
        self.assertEqual(res["Fusion_Fission_Hybrid"]["licensing_duration_yr"], 14.0)


class TestMasterFuelCycleAndNonElectricConsilience(unittest.TestCase):
    def test_master_audit_run(self):
        master = MasterFuelCycleAndNonElectricConsilience()
        audit = master.run_full_epistemic_audit()
        self.assertIn("NO", audit["verdict"])
        self.assertEqual(len(audit["findings"]), 5)


if __name__ == "__main__":
    unittest.main()
