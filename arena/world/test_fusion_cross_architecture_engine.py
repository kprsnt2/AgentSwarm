"""
Unit Tests for Fusion Cross-Architecture and EPC Timeline Closure Engine
========================================================================
13 rigorous unit tests verifying:
1. Laser ICF repetition rate and target volume physics
2. Target fabrication economic ceiling ($0.20/target)
3. Laser driver recirculating power and engineering gain
4. Final optics neutron bombardment flux
5. Helion D-He3 terrestrial fuel exhaustion (< 5 years)
6. Helion D-D self-breeding parasitic tritium and 14.1 MeV neutron activation
7. D-He3 Bremsstrahlung power balance
8. Stellarator 3D non-planar modular coil REBCO bending strain limits
9. Stellarator fast alpha collisionless prompt loss wall heat flux
10. Stellarator 3D blanket geometric coverage TBR deficit (< 1.0)
11. Nuclear EPC Critical Path Method (CPM) baseline completion year (> 2043)
12. Nuclear EPC optimistic theoretical limit (completion ~ 2040.2+)
13. Unified consilience audit integration
"""

import unittest
from fusion_cross_architecture_engine import (
    LaserICFParameters, LaserICFEngine,
    HelionFRCParameters, HelionFRCEngine,
    StellaratorParameters, StellaratorLimitsEngine,
    NuclearEPCCriticalPathEngine,
    UnifiedFusionConsilienceEngine
)


class TestLaserICFEngine(unittest.TestCase):
    def setUp(self):
        self.engine = LaserICFEngine()

    def test_yield_and_repetition_rate(self):
        # 2.5 MJ driver * gain 80 = 200 MJ yield
        self.assertAlmostEqual(self.engine.yield_per_shot_mj(), 200.0, places=2)
        # 1000 MWth / 200 MJ = 5.0 Hz
        self.assertAlmostEqual(self.engine.required_repetition_rate_hz(), 5.0, places=2)

    def test_daily_target_consumption(self):
        # 5 Hz * 86400 s * 0.80 CF = 345,600 targets/day
        daily = self.engine.daily_target_consumption()
        self.assertAlmostEqual(daily, 345600.0, places=1)
        self.assertGreater(self.engine.annual_target_consumption(), 1.2e8)

    def test_target_cost_economic_ceiling(self):
        # 200 MJ * 0.40 = 80 MJ electric = 22.22 kWh
        kwh = self.engine.gross_electrical_per_shot_kwh()
        self.assertAlmostEqual(kwh, 80.0 / 3.6, places=2)
        # At $0.06/kWh, gross rev = $1.333/shot. 15% fuel limit = $0.20/shot
        cost_ceiling = self.engine.target_cost_economic_ceiling_usd()
        self.assertAlmostEqual(cost_ceiling, 0.20, delta=0.01)

    def test_recirculating_power_and_q_eng(self):
        # Driver 2.5 MJ / 0.12 eff = 20.83 MJ electric
        # Gross electric = 80.0 MJ electric -> 26.04% laser recirc + 8% aux = 34.04%
        f_rec = self.engine.recirculating_power_fraction()
        self.assertAlmostEqual(f_rec, 0.3404, delta=0.01)
        q_eng = self.engine.engineering_gain()
        self.assertAlmostEqual(q_eng, 1.0 / 0.3404, delta=0.1)

    def test_final_optics_fast_neutron_flux(self):
        # Fast 14.1 MeV neutron flux at 12 m radius
        flux = self.engine.final_optics_fast_neutron_flux()
        self.assertGreater(flux, 1e16)
        self.assertLess(flux, 1e18)


class TestHelionFRCEngine(unittest.TestCase):
    def setUp(self):
        self.engine = HelionFRCEngine()

    def test_he3_burn_and_depletion(self):
        # 150 MWth D-He3 at 80% CF burns ~6.45 kg/year
        burn = self.engine.annual_he3_burn_kg()
        self.assertAlmostEqual(burn, 6.45, delta=0.2)
        # Global stockpile (30 kg) depleted in < 5 years
        years = self.engine.years_to_exhaust_global_stockpile()
        self.assertAlmostEqual(years, 30.0 / burn, delta=0.1)
        self.assertLess(years, 5.0)

    def test_parasitic_dd_neutrons_and_tritium(self):
        # Producing 6.45 kg of He3 breeds 6.45 kg of Tritium!
        res = self.engine.parasitic_dd_neutron_and_tritium_rates()
        self.assertAlmostEqual(res["tritium_co_produced_kg_yr"], 6.45, delta=0.2)
        # In-situ prompt DT burn produces tens of MW of 14.1 MeV fast neutrons
        self.assertGreater(res["total_neutron_power_mw"], 15.0)
        self.assertGreater(res["total_neutron_energy_fraction_of_thermal"], 0.10)

    def test_bremsstrahlung_ratio(self):
        # Bremsstrahlung ratio for D-He3 at 75 keV is significant
        ratio = self.engine.bremsstrahlung_to_fusion_power_ratio()
        self.assertGreater(ratio, 0.20)


class TestStellaratorLimitsEngine(unittest.TestCase):
    def setUp(self):
        self.engine = StellaratorLimitsEngine()

    def test_coil_bending_strain_limit(self):
        # 25 mm cable around 0.45 m radius -> strain = 0.025 / (2 * 0.45) = 2.78%
        strain = self.engine.peak_coil_bending_strain()
        self.assertAlmostEqual(strain, 0.02778, places=4)
        # Exceeds 0.4% limit by nearly 7x -> safety factor ~ 0.14
        sf = self.engine.strain_safety_factor()
        self.assertLess(sf, 0.20)
        # Min bend radius needed is > 3.0 meters
        self.assertGreater(self.engine.min_allowable_bend_radius_m(), 3.0)

    def test_fast_alpha_loss_heat_flux(self):
        # 22% prompt loss of 100 MW alpha power = 22 MW over 0.60 m^2 = 36.67 MW/m^2
        flux = self.engine.localized_alpha_heat_flux_mw_m2()
        self.assertAlmostEqual(flux, 36.67, delta=0.5)
        self.assertGreater(flux, 15.0) # exceeds tungsten armor limit

    def test_homogeneous_3d_tbr(self):
        # 65% blanket coverage * 1.35 local TBR = 0.8775 < 1.0 (tritium deficit)
        tbr = self.engine.homogeneous_3d_tbr()
        self.assertAlmostEqual(tbr, 0.8775, places=3)
        self.assertLess(tbr, 1.0)


class TestNuclearEPCCriticalPathEngine(unittest.TestCase):
    def setUp(self):
        self.epc = NuclearEPCCriticalPathEngine(start_year=2026.75)

    def test_critical_path_baseline(self):
        # Baseline EPC duration exceeds 200 months (>16.5 years)
        res = self.epc.compute_critical_path("baseline")
        self.assertGreater(res["total_duration_months"], 190)
        self.assertGreater(res["completion_year"], 2043.0)
        self.assertFalse(res["is_achievable_by_2040"])

    def test_critical_path_optimistic(self):
        # Under zero-slip optimistic timeline, duration is 158 months (13.17 years)
        res = self.epc.compute_critical_path("optimistic")
        self.assertGreaterEqual(res["total_duration_months"], 150)
        # October 2026 + 13.17 years = late 2039 / 2040.0
        self.assertAlmostEqual(res["completion_year"], 2039.92, delta=0.1)

    def test_critical_path_historical_slip(self):
        # Historical nuclear schedule slip (+40-50%) pushes grid past 2048
        res = self.epc.compute_critical_path("historical_slip")
        self.assertGreater(res["completion_year"], 2048.0)


class TestUnifiedConsilienceAudit(unittest.TestCase):
    def test_audit_execution(self):
        audit = UnifiedFusionConsilienceEngine().audit_all_architectures()
        self.assertIn("icf", audit)
        self.assertIn("frc_he3", audit)
        self.assertIn("stellarator", audit)
        self.assertIn("timeline", audit)
        self.assertFalse(audit["timeline"]["baseline_by_2040"])


if __name__ == "__main__":
    unittest.main()
