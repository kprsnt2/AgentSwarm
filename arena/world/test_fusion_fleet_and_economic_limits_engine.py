"""
Unit Tests for Fusion Fleet and Economic Limits Engine
======================================================
Autonomous Research Agent Kepler (A001, Gen 0)
"""

import unittest
import math
from fusion_fleet_and_economic_limits_engine import (
    FleetDynamicsParameters,
    TritiumFleetDynamicsEngine,
    FusionCostParameters,
    FusionTechnoEconomicEngine,
    MagnetVirialAndQuenchEngine,
    DisruptionAndAvalancheEngine,
    run_comprehensive_economic_and_fleet_synthesis
)


class TestTritiumFleetDynamics(unittest.TestCase):
    """Verifies multi-reactor fleet dynamics and doubling time paradox."""

    def setUp(self):
        self.engine = TritiumFleetDynamicsEngine()

    def test_annual_burn_rate_magnitude(self):
        # 525 MW_th at 80% capacity factor burns ~23.5 kg/yr
        burn = self.engine.annual_burn_rate_kg()
        self.assertAlmostEqual(burn, 23.55, delta=1.0)

    def test_doubling_time_tbr_105_is_infinite(self):
        # At TBR = 1.05, processing losses and radioactive decay exceed net breeding
        # The surplus generation rate is negative; reactor cannot sustain itself
        t_double = self.engine.doubling_time_years(1.05)
        self.assertEqual(t_double, float('inf'))

    def test_doubling_time_tbr_108_is_century_scale(self):
        # At TBR = 1.08, net surplus is positive but tiny (~0.05-0.10 kg/yr)
        # Doubling time requires over 80 years
        t_double = self.engine.doubling_time_years(1.08)
        self.assertGreater(t_double, 80.0)

    def test_minimum_tbr_for_10_year_doubling(self):
        # To seed a new reactor every 10 years, TBR must exceed 1.10
        tbr_min = self.engine.minimum_tbr_for_doubling_time(10.0)
        self.assertGreater(tbr_min, 1.10)
        self.assertLess(tbr_min, 1.25)

    def test_fleet_size_strictly_one_by_2040(self):
        # Even with FOAK commissioning in 2039, fleet size in 2040 is exactly 1
        sim = self.engine.simulate_fleet_growth(2039, 2050, initial_reserve_kg=18.0, tbr=1.05)
        self.assertEqual(sim["fleet_size"][0], 1)  # 2039
        self.assertEqual(sim["fleet_size"][1], 1)  # 2040


class TestFusionTechnoEconomics(unittest.TestCase):
    """Verifies CAPEX, capacity factor limits, and LCOE scaling."""

    def setUp(self):
        self.engine = FusionTechnoEconomicEngine()

    def test_overnight_capex_and_specific_cost(self):
        capex_m = self.engine.overnight_capital_cost_millions()
        specific_cost = self.engine.specific_capital_cost_per_kwe()
        # FOAK ARC-class plant costs > $4.0 Billion (> $35,000 / kWe)
        self.assertGreater(capex_m, 4000.0)
        self.assertGreater(specific_cost, 35000.0)

    def test_effective_capacity_factor_bound(self):
        # First-wall replacement every 3.3 years with 12-month outage caps CF < 70%
        cf = self.engine.effective_capacity_factor()
        self.assertLess(cf, 0.70)
        self.assertGreater(cf, 0.55)

    def test_lcoe_vastly_exceeds_grid_parity(self):
        lcoe = self.engine.levelized_cost_of_electricity_mwh()
        # Commercial wholesale electricity is $30-$60/MWh
        # Fusion LCOE exceeds $300/MWh
        self.assertGreater(lcoe, 300.0)


class TestMagneticsAndQuench(unittest.TestCase):
    """Verifies Virial stress theorem and HTS slow-quench burnout time."""

    def setUp(self):
        self.engine = MagnetVirialAndQuenchEngine()

    def test_stored_magnetic_energy(self):
        u_mag = self.engine.stored_magnetic_energy_gj()
        self.assertGreater(u_mag, 30.0)
        self.assertLess(u_mag, 80.0)

    def test_virial_structural_mass(self):
        mass = self.engine.virial_minimum_structural_mass_tonnes()
        # Virial theorem lower bound on structural cold mass > 400 tonnes
        self.assertGreater(mass, 400.0)

    def test_hts_hotspot_burnout_under_half_second(self):
        t_burn = self.engine.hts_hotspot_burnout_time_seconds()
        # Slow NZP causes adiabatic burnout in under 0.5 seconds
        self.assertLess(t_burn, 0.50)
        self.assertGreater(t_burn, 0.05)


class TestDisruptionsAndAvalanches(unittest.TestCase):
    """Verifies Lorentz forces and relativistic runaway avalanche multiplication."""

    def setUp(self):
        self.engine = DisruptionAndAvalancheEngine()

    def test_induced_electric_field_vs_dreicer(self):
        e_ind = self.engine.induced_loop_electric_field_v_m(10.0)
        e_crit = self.engine.critical_dreicer_electric_field_v_m()
        self.assertGreater(e_ind, 100.0)
        self.assertLess(e_crit, 0.5)
        # Ratio E / E_crit >> 1
        self.assertGreater(e_ind / e_crit, 500.0)

    def test_runaway_avalanche_gain_exponent(self):
        gamma = self.engine.runaway_avalanche_gain_exponent()
        # Avalanche multiplication exponent > 50 (gain > 10^21)
        self.assertGreater(gamma, 50.0)

    def test_peak_halo_force_meganewtons(self):
        f_halo = self.engine.peak_asymmetric_halo_force_meganewtons()
        # Peak vertical force > 500 MN (> 50,000 tonnes-force)
        self.assertGreater(f_halo, 500.0)


class TestIntegratedSynthesis(unittest.TestCase):
    """Verifies the complete integrated synthesis pipeline."""

    def test_synthesis_runs_and_reports_correctly(self):
        res = run_comprehensive_economic_and_fleet_synthesis()
        self.assertEqual(res["fleet_dynamics"]["fleet_size_at_2040"], 1)
        self.assertGreater(res["techno_economics"]["lcoe_per_mwh"], 300.0)
        self.assertGreater(res["magnetics_and_quench"]["virial_mass_tonnes"], 400.0)
        self.assertGreater(res["disruptions_and_avalanches"]["avalanche_exponent"], 50.0)


if __name__ == "__main__":
    unittest.main()
