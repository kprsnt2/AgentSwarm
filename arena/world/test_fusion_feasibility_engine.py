"""
Unit Tests for Fusion Power 2040 Engineering Feasibility Engine
==============================================================
Autonomous Research Agent Kepler (A001, Gen 0)
"""

import unittest
import math
from fusion_feasibility_engine import (
    dt_reactivity_bosch_hale,
    dd_reactivity_approx,
    dhe3_reactivity_approx,
    pb11_reactivity_approx,
    pb11_bremsstrahlung_ratio,
    lawson_triple_product_dt,
    lawson_triple_product_finite_q,
    calculate_engineering_q,
    PlantEfficiencyParameters,
    TritiumBurnAndBreedingModel,
    simulate_global_civilian_tritium,
    NeutronMaterialsDamageModel,
    eich_sol_width_mm,
    divertor_peak_heat_flux_mw_m2,
    get_all_concept_specifications,
    evaluate_concept,
    run_full_comparative_assessment
)


class TestFusionPhysicsAndLawson(unittest.TestCase):
    """Verifies core fusion cross-sections, reactivities, and Lawson criterion."""

    def test_dt_reactivity_peak_and_magnitude(self):
        sv_10 = dt_reactivity_bosch_hale(10.0)
        sv_15 = dt_reactivity_bosch_hale(15.0)
        sv_65 = dt_reactivity_bosch_hale(65.0)
        sv_100 = dt_reactivity_bosch_hale(100.0)

        self.assertGreater(sv_15, sv_10)
        self.assertGreater(sv_65, sv_15)
        self.assertGreater(sv_65, sv_100)  # Peaks around ~65 keV
        self.assertAlmostEqual(sv_15, 2.64e-22, delta=0.5e-22)
        self.assertAlmostEqual(sv_65, 8.1e-22, delta=1.0e-22)

    def test_lawson_triple_product_ground_truth(self):
        # Ground truth: Lawson criterion n*T*tau_E must exceed ~3e21 keV*s/m^3 for D-T
        triple_products = [lawson_triple_product_dt(t) for t in range(5, 40)]
        min_tp = min(triple_products)
        self.assertGreater(min_tp, 2.0e21)
        self.assertLess(min_tp, 4.0e21)

        # Below 4.4 keV, Bremsstrahlung exceeds alpha heating
        tp_low = lawson_triple_product_dt(3.0)
        self.assertEqual(tp_low, float('inf'))

    def test_pb11_bremsstrahlung_catastrophe(self):
        # In thermal equilibrium (Te = Ti), Bremsstrahlung exceeds fusion power at ALL temperatures
        for t in [20.0, 50.0, 100.0, 200.0, 300.0, 500.0, 800.0]:
            ratio = pb11_bremsstrahlung_ratio(t)
            self.assertGreater(ratio, 1.0, f"Bremsstrahlung failed to exceed fusion power at T={t} keV")


class TestPowerBalanceAndEngineeringQ(unittest.TestCase):
    """Verifies plant energy balance, wall-plug efficiency, and Q_eng."""

    def test_iter_power_balance_not_net_electricity(self):
        # Ground truth: ITER targets Q=10, not net electricity
        params = PlantEfficiencyParameters(
            thermal_efficiency=0.33,
            direct_conversion_eff=0.0,
            driver_wall_plug_eff=0.40,
            blanket_multiplier=1.0,
            bop_fraction=0.08,
            magnet_cooling_fraction=0.10
        )
        pb = calculate_engineering_q(p_fusion_mw=500.0, p_aux_mw=50.0, params=params, f_neutron=0.8)
        self.assertLess(pb["q_eng"], 1.5)
        self.assertGreater(pb["recirc_fraction"], 0.65)

    def test_commercial_q_eng_threshold(self):
        params = PlantEfficiencyParameters(
            thermal_efficiency=0.40,
            direct_conversion_eff=0.0,
            driver_wall_plug_eff=0.45,
            blanket_multiplier=1.15,
            bop_fraction=0.04,
            magnet_cooling_fraction=0.04
        )
        pb_high = calculate_engineering_q(p_fusion_mw=1500.0, p_aux_mw=50.0, params=params, f_neutron=0.8)
        self.assertGreater(pb_high["q_eng"], 3.0)
        self.assertLess(pb_high["recirc_fraction"], 0.33)


class TestTritiumSupplyAndBreeding(unittest.TestCase):
    """Verifies tritium burn rates, required TBR, and CANDU stock depletion."""

    def test_annual_burn_rate_scaling(self):
        # 1000 MW fusion (1 GW_th) burns ~56 kg of tritium per FPY
        model = TritiumBurnAndBreedingModel(
            fusion_power_mw=1000.0,
            capacity_factor=1.0,
            burnup_fraction=0.02,
            tbr_achieved=1.05,
            fuel_cycle_time_days=1.0,
            unrecoverable_loss_fraction=1e-3,
            startup_inventory_kg=8.0
        )
        annual_burn = model.annual_burn_rate_kg()
        self.assertAlmostEqual(annual_burn, 56.07, delta=1.5)

    def test_required_tbr_exceeds_unity(self):
        # Ground truth: Tritium is not naturally abundant; breeding required
        model = TritiumBurnAndBreedingModel(
            fusion_power_mw=500.0,
            capacity_factor=0.8,
            burnup_fraction=0.02,
            tbr_achieved=1.08,
            fuel_cycle_time_days=1.0,
            unrecoverable_loss_fraction=1e-3,
            startup_inventory_kg=8.0
        )
        tbr_req = model.required_tbr_for_sustainability(doubling_time_years=5.0)
        self.assertGreater(tbr_req, 1.05)
        self.assertLess(tbr_req, 1.20)

    def test_global_tritium_candu_depletion(self):
        years = list(range(2024, 2045))
        traj_no_reactors = simulate_global_civilian_tritium(years, num_reactors_online={}, reactor_power_mw=500.0)
        self.assertLess(traj_no_reactors[2040], 25.0)
        self.assertGreater(traj_no_reactors[2040], 15.0)

        # 1 pilot reactor drawing 8 kg startup in 2035 causes step drop
        reactors_online = {2035: 1.0, 2036: 1.0, 2037: 1.0, 2038: 1.0, 2039: 1.0, 2040: 1.0}
        traj_with_reactor = simulate_global_civilian_tritium(years, num_reactors_online=reactors_online, reactor_power_mw=500.0, tbr=1.05)
        self.assertLess(traj_with_reactor[2035], traj_no_reactors[2035] - 6.0)

        # If breeding blanket achieves TBR = 0.85 (underbreeding), inventory collapses below 10 kg by 2040
        traj_underbreeding = simulate_global_civilian_tritium(years, num_reactors_online=reactors_online, reactor_power_mw=500.0, tbr=0.85)
        self.assertLess(traj_underbreeding[2040], 10.0)


class TestMaterialsDamageAndDivertorExhaust(unittest.TestCase):
    """Verifies DPA accumulation and Eich divertor scrape-off layer scaling."""

    def test_dpa_accumulation_and_lifetime(self):
        model = NeutronMaterialsDamageModel(
            neutron_wall_load_mw_m2=2.5,
            material_type="Eurofer97",
            dpa_lifetime_limit=70.0,
            helium_appm_per_dpa=12.0
        )
        dpa_yr = model.annual_dpa(0.8)
        self.assertAlmostEqual(dpa_yr, 21.0, delta=0.5)
        lifetime = model.component_lifetime_years(0.8)
        self.assertAlmostEqual(lifetime, 3.33, delta=0.2)

    def test_eich_scaling_law_lambda_q(self):
        lambda_sparc = eich_sol_width_mm(b_poloidal_tesla=3.1, p_sol_mw=30.0, major_radius_m=1.85)
        lambda_iter = eich_sol_width_mm(b_poloidal_tesla=1.2, p_sol_mw=100.0, major_radius_m=6.2)

        self.assertLess(lambda_sparc, 0.25)
        self.assertGreater(lambda_iter, 0.25)
        self.assertLess(lambda_sparc, lambda_iter)

    def test_divertor_unmitigated_heat_flux_exceeds_limits(self):
        q_unmit, q_mit, ok = divertor_peak_heat_flux_mw_m2(
            p_sol_mw=45.0,
            major_radius_m=3.3,
            b_poloidal_tesla=3.1,
            flux_expansion=15.0,
            strike_angle_deg=2.5,
            f_radiation=0.90
        )
        self.assertGreater(q_unmit, 50.0)
        self.assertTrue(ok)


class TestConceptRankingAndDeliverable(unittest.TestCase):
    """Verifies all concepts are evaluated and ranked according to 2040 commercial feasibility."""

    def test_ranked_assessment_completeness(self):
        results = run_full_comparative_assessment()
        ranked = results["ranked_concepts"]

        self.assertEqual(len(ranked), 6)
        self.assertIn("Compact Tokamak", ranked[0]["concept"])
        self.assertIn("TAE p-B11", ranked[-1]["concept"])

        for item in ranked:
            p_val = item["timeline"]["p_commercial_grid_by_2040"]
            self.assertLessEqual(p_val, 0.20)
            self.assertGreaterEqual(p_val, 0.0)
            self.assertTrue(len(item["primary_physical_limit"]) > 10)
            self.assertTrue(len(item["binding_engineering_constraint"]) > 10)


if __name__ == "__main__":
    unittest.main()
