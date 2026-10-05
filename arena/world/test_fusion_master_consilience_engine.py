"""
Unit Tests for Fusion Master Consilience & Epistemic Limits Engine
==================================================================
Tests physical consistency, conservation laws, and mathematical validity
of the Sheared-Flow Z-Pinch, Liquid Immersion Blanket / Beryllium Reserve,
Direct Conversion Dissipation, and Monte Carlo CPM Timeline modules.
"""

import unittest
import math
from fusion_master_consilience_engine import (
    ShearedFlowZPinchParameters,
    ShearedFlowZPinchEngine,
    LiquidBlanketParameters,
    LiquidBlanketAndMaterialsEngine,
    DirectConversionParameters,
    DirectEnergyConversionEngine,
    FusionMonteCarloTimelineEngine,
    MasterFusionConsilienceAudit
)


class TestShearedFlowZPinchEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ShearedFlowZPinchEngine()

    def test_bennet_equilibrium_current(self):
        """Verify Bennet equilibrium current matches physical scaling."""
        i_bennet_ma = self.engine.bennet_current_required_ma()
        # For n = 1e23 m^-3, r_p = 5 mm, T = 10 keV, I_bennet is ~0.71 MA
        self.assertGreater(i_bennet_ma, 0.5)
        self.assertLess(i_bennet_ma, 1.0)

    def test_edge_b_field_and_alfven_velocity(self):
        """Verify edge self-magnetic field and Alfven speed."""
        b_edge = self.engine.edge_magnetic_field_tesla()
        # For 1.5 MA and 5 mm radius, B_theta = mu0 * I / (2*pi*r) = 60.0 T
        self.assertAlmostEqual(b_edge, 60.0, places=1)
        v_a = self.engine.alfven_velocity_m_per_s()
        # v_A should be on the order of 10^6 m/s (~2.62e6 m/s)
        self.assertGreater(v_a, 5.0e5)
        self.assertLess(v_a, 4.0e6)

    def test_shumlak_shear_velocity_and_transit_time(self):
        """Verify sheared flow velocity is at least 0.1 v_A and transit time is microsecond scale."""
        v_shear = self.engine.required_sheared_flow_velocity_m_per_s()
        v_a = self.engine.alfven_velocity_m_per_s()
        self.assertAlmostEqual(v_shear / v_a, 0.10, places=4)

        tau_us = self.engine.plasma_transit_time_microseconds()
        # Transit time through 1.5 m column is ~10-20 microseconds
        self.assertGreater(tau_us, 2.0)
        self.assertLess(tau_us, 30.0)

    def test_electrode_arc_erosion(self):
        """Verify electrode erosion mass per day and per year."""
        daily_erosion_kg = self.engine.daily_electrode_erosion_mass_kg()
        annual_erosion_kg = self.engine.annual_electrode_erosion_mass_kg()
        # Daily erosion should be hundreds of grams of tungsten (~0.5 - 1.0 kg/day)
        self.assertGreater(daily_erosion_kg, 0.3)
        self.assertLess(daily_erosion_kg, 2.0)
        # Annual erosion > 100 kg
        self.assertGreater(annual_erosion_kg, 100.0)

    def test_insulator_radiation_induced_conductivity(self):
        """Verify RIC in ceramic insulator jumps orders of magnitude."""
        sigma_ric = self.engine.insulator_radiation_induced_conductivity_s_per_m()
        # Should be on order of 1e-7 to 1e-5 S/m (vs 1e-14 baseline)
        self.assertGreater(sigma_ric, 1.0e-7)
        self.assertLess(sigma_ric, 1.0e-4)


class TestLiquidBlanketAndMaterialsEngine(unittest.TestCase):
    def setUp(self):
        self.engine = LiquidBlanketAndMaterialsEngine()

    def test_flibe_beryllium_mass_fraction(self):
        """Verify chemical stoichiometric mass fraction of Beryllium in FLiBe."""
        w_be = self.engine.flibe_beryllium_mass_fraction()
        # 2*LiF + BeF2 -> Be is 9.012 / 98.892 ~ 0.0911 (9.11%)
        self.assertAlmostEqual(w_be, 0.09113, places=3)

    def test_beryllium_inventory_per_reactor(self):
        """Verify pure Beryllium required per 200 m^3 FLiBe blanket."""
        be_tonnes = self.engine.beryllium_inventory_per_reactor_tonnes()
        # 200 m^3 * 1940 kg/m^3 = 388 tonnes FLiBe * 9.11% = ~35.4 tonnes Be
        self.assertGreater(be_tonnes, 30.0)
        self.assertLess(be_tonnes, 40.0)

    def test_global_beryllium_production_share(self):
        """Verify a single reactor consumes >10% of annual global Beryllium production."""
        frac = self.engine.fraction_of_global_annual_beryllium_production()
        # 35.4 / 280 ~ 0.126 (12.6%)
        self.assertGreater(frac, 0.10)
        self.assertLess(frac, 0.20)

    def test_beryllium_fleet_growth_cap(self):
        """Verify fleet construction is severely throttled by Beryllium supply."""
        max_reactors_yr = self.engine.max_fleet_size_from_annual_beryllium_output(0.50)
        # 140 tonnes / 35.4 tonnes = ~3.95 reactors/year
        self.assertLess(max_reactors_yr, 5.0)
        self.assertGreater(max_reactors_yr, 2.0)

    def test_mhd_hartmann_and_stuart_numbers(self):
        """Verify dimensionless MHD numbers for Pb-17Li in 12 T field."""
        ha = self.engine.mhd_hartmann_number_pbli()
        n_stuart = self.engine.mhd_stuart_number_interaction_parameter_pbli()
        # Hartmann number should be > 10,000
        self.assertGreater(ha, 10000.0)
        # Stuart number should be > 1,000 (MHD forces dominate inertia by orders of magnitude)
        self.assertGreater(n_stuart, 1000.0)

    def test_mhd_pressure_drop_and_pumping_power(self):
        """Verify MHD pressure drop exceeds 10 MPa and requires multi-MW pumping."""
        delta_p_mpa = self.engine.total_mhd_pressure_drop_mpa()
        p_pump_mw = self.engine.mhd_pumping_power_mw()
        # Delta P should be > 10 MPa (100 bar)
        self.assertGreater(delta_p_mpa, 10.0)
        # Pumping power should exceed 10 MWe
        self.assertGreater(p_pump_mw, 10.0)


class TestDirectEnergyConversionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DirectEnergyConversionEngine()

    def test_round_trip_magnetic_dissipation(self):
        """Verify round trip loss in circulating magnetic field."""
        dissipation = self.engine.round_trip_magnetic_dissipation_mj()
        # E_mag = 3 * 100 = 300 MJ. (1/0.85 - 0.85) = 0.3265. Loss = 300 * 0.3265 = 97.9 MJ
        self.assertGreater(dissipation, 80.0)
        self.assertLess(dissipation, 120.0)

    def test_net_engineering_gain_q_eng(self):
        """Verify Q_eng under high circulating magnetic ratio."""
        q_eng = self.engine.net_electrical_gain_q_eng()
        # With high circulation, Q_eng is close to or below 1.0 unless Q_plasma is high
        self.assertGreater(q_eng, 0.5)
        self.assertLess(q_eng, 1.5)

    def test_min_plasma_gain_for_breakeven(self):
        """Verify minimum plasma gain required for positive net electricity."""
        min_q = self.engine.min_plasma_gain_required_for_breakeven()
        # Must require plasma gain > 1.0 to overcome magnetic dissipation
        self.assertGreater(min_q, 1.0)


class TestFusionMonteCarloTimelineEngine(unittest.TestCase):
    def setUp(self):
        self.mc = FusionMonteCarloTimelineEngine(seed=42)

    def test_monte_carlo_distribution(self):
        """Verify 1,000-trial simulation bounds and probabilities."""
        res_fast = self.mc.run_simulation(trials=1000, fast_track=True)
        self.assertEqual(res_fast["trials"], 1000)

        # FOAK grid demo probability by 2040 under fast-track concurrency is ~10% to 25%
        self.assertGreater(res_fast["foak_p_grid_by_2040"], 0.10)
        self.assertLess(res_fast["foak_p_grid_by_2040"], 0.30)

        # Commercial fleet probability by 2040 MUST BE ZERO
        self.assertEqual(res_fast["commercial_fleet_p_by_2040"], 0.0)

        # FOAK median completion year under fast-track should be ~2041-2044
        self.assertGreater(res_fast["foak_p50_median_year"], 2040.5)
        self.assertLess(res_fast["foak_p50_median_year"], 2045.0)

        # Commercial fleet median completion year should be in late 2040s or 2050s
        self.assertGreater(res_fast["fleet_p50_median_year"], 2047.0)

        # Test sequential mode: P(FOAK <= 2040) is near zero
        res_seq = self.mc.run_simulation(trials=1000, fast_track=False)
        self.assertLess(res_seq["foak_p_grid_by_2040"], 0.05)
        self.assertEqual(res_seq["commercial_fleet_p_by_2040"], 0.0)


class TestMasterFusionConsilienceAudit(unittest.TestCase):
    def test_grand_audit_execution(self):
        """Verify master audit runs and aggregates all architecture metrics."""
        audit = MasterFusionConsilienceAudit()
        res = audit.generate_grand_audit_report()
        self.assertIn("sheared_flow_zpinch", res)
        self.assertIn("liquid_blankets_and_beryllium", res)
        self.assertIn("direct_energy_conversion", res)
        self.assertIn("monte_carlo_timeline", res)


if __name__ == "__main__":
    unittest.main()
