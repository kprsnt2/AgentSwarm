"""
test_fusion_terminal_epistemic_bounds_engine.py
===============================================
Unit test suite for fusion_terminal_epistemic_bounds_engine.py.
Validates:
1. Liquid metal divertor Hartmann scaling, MHD pressure drops, pumping power, and vapor pressure.
2. Centrifugal mirror Pastukhov confinement, Mach number shear limit, and electrical power balance.
3. AI plasma control latency, vacuum vessel magnetic diffusion, and SPI flight time bounds.
4. Direct-drive laser ICF hot electron preheat, adiabat scaling, and vacuum chamber gas evacuation.
5. Pulsed FRC blanket standoff geometry, stored magnetic energy scaling, and capacitor switching dissipation.
6. Grand unified 10-architecture consilience matrix, chokepoint calculations, and fleet probability closure.
"""

import unittest
import math
from fusion_terminal_epistemic_bounds_engine import (
    MU_0,
    LiquidMetalDivertorParameters,
    LiquidMetalDivertorEngine,
    CentrifugalMirrorParameters,
    CentrifugalMirrorEngine,
    AIControlLatencyParameters,
    AIActuatorLatencyEngine,
    DirectDriveLaserParameters,
    DirectDriveLaserICFEngine,
    PulsedFRCBlanketParameters,
    PulsedFRCBlanketEngine,
    GrandUnifiedConsilienceMatrixEngine
)


class TestLiquidMetalDivertorEngine(unittest.TestCase):
    """Validates liquid metal divertor MHD and vapor pressure thermodynamics."""

    def setUp(self):
        self.params = LiquidMetalDivertorParameters()

    def test_hartmann_number_calculation(self):
        # Ha = B * L * sqrt(sigma / mu)
        # Ha = 12 * 0.05 * sqrt(3.3e6 / 4.5e-4) = 0.6 * sqrt(7.333e9) ~ 51,380.9
        ha = LiquidMetalDivertorEngine.calculate_hartmann_number(12.0, 0.05, 3.3e6, 4.5e-4)
        self.assertAlmostEqual(ha, 51380.93, delta=1.0)

    def test_mhd_pressure_gradient(self):
        # dP/dx = sigma * v * B^2 * (c / (1+c))
        # 3.3e6 * 2.0 * 144 * (0.05 / 1.05) ~ 4.526e7 Pa/m = 45.26 MPa/m
        dp_dx = LiquidMetalDivertorEngine.calculate_mhd_pressure_gradient(12.0, 2.0, 3.3e6, 0.05)
        self.assertAlmostEqual(dp_dx / 1e6, 45.257, delta=0.01)

    def test_total_pressure_drop_and_pumping_power(self):
        dp_dx = LiquidMetalDivertorEngine.calculate_mhd_pressure_gradient(12.0, 2.0, 3.3e6, 0.05)
        delta_p = LiquidMetalDivertorEngine.calculate_total_pressure_drop(dp_dx, 5.0)
        self.assertAlmostEqual(delta_p / 1e6, 226.286, delta=0.01)

        p_mech, p_elec = LiquidMetalDivertorEngine.calculate_pumping_power(
            delta_p, 2.0, 0.10, 0.50, 0.35
        )
        self.assertAlmostEqual(p_mech / 1e6, 22.629, delta=0.01)
        self.assertAlmostEqual(p_elec / 1e6, 64.653, delta=0.01)

    def test_lithium_vapor_pressure_scaling(self):
        # log10(P) = 9.87 - 8023 / T_K
        p_450 = LiquidMetalDivertorEngine.calculate_lithium_vapor_pressure(723.15)
        self.assertAlmostEqual(p_450, 0.0596, delta=0.005)

        p_550 = LiquidMetalDivertorEngine.calculate_lithium_vapor_pressure(823.15)
        self.assertAlmostEqual(p_550, 1.328, delta=0.01)
        # Pressure jumps > 20x over 100 C increase
        self.assertGreater(p_550 / p_450, 20.0)

    def test_hertz_knudsen_evaporation_flux(self):
        flux = LiquidMetalDivertorEngine.calculate_hertz_knudsen_evaporation_flux(823.15, 1.328)
        self.assertGreater(flux, 4.0e22)
        self.assertLess(flux, 5.0e22)

    def test_divertor_full_evaluation(self):
        res = LiquidMetalDivertorEngine.evaluate_divertor(self.params)
        self.assertTrue(res["mhd_pressure_exceeds_pipe_limits"])
        self.assertGreater(res["pumping_power_elec_mw"], 60.0)
        self.assertIn(450.0, res["vapor_profile"])
        self.assertIn(550.0, res["vapor_profile"])
        # At 550 C, radiative quench time should be under 1 second
        self.assertLess(res["vapor_profile"][550.0]["time_to_radiative_collapse_s"], 1.0)


class TestCentrifugalMirrorEngine(unittest.TestCase):
    """Validates Centrifugal Mirror Fusion (CMF) confinement and power balance."""

    def setUp(self):
        self.params = CentrifugalMirrorParameters()

    def test_classical_ntau_scaling(self):
        # ntau = 2.5e17 * (50^1.5) * log10(8.5) ~ 8.215e19 s/m^3
        ntau = CentrifugalMirrorEngine.calculate_classical_ntau(50.0, 8.5)
        self.assertAlmostEqual(ntau / 1e19, 8.215, delta=0.01)

    def test_mach_stability_limit_and_enhancement(self):
        mach_limit = CentrifugalMirrorEngine.calculate_kelvin_helmholtz_mach_limit()
        self.assertAlmostEqual(mach_limit, math.sqrt(2.0), delta=1e-5)

        enhancement = CentrifugalMirrorEngine.calculate_centrifugal_enhancement(mach_limit)
        self.assertAlmostEqual(enhancement, math.e, delta=0.01)

    def test_cmf_q_max(self):
        # Base Q = 1.25 * e ~ 3.397
        q_max = CentrifugalMirrorEngine.calculate_cmf_q_max(1.25, 1.414)
        self.assertAlmostEqual(q_max, 3.397, delta=0.01)

    def test_electrical_power_balance_and_recirculation(self):
        # At Q = 3.397, eta_th = 0.40, eta_inj = 0.65, f_aux = 0.10:
        # P_gross = 0.40 * 4.397 = 1.7588
        # P_recirc = (1 / 0.65) + 0.10 * 1.7588 = 1.5385 + 0.1759 = 1.7143
        # f_recirc = 1.7143 / 1.7588 = 97.47%
        balance = CentrifugalMirrorEngine.calculate_electrical_power_balance(3.3968, 0.40, 0.65, 0.10)
        self.assertAlmostEqual(balance["recirculating_percentage"], 97.47, delta=0.1)

        # If base Q is 1.10, recirculating percentage exceeds 100%
        q_low = CentrifugalMirrorEngine.calculate_cmf_q_max(1.10, 1.414)
        balance_low = CentrifugalMirrorEngine.calculate_electrical_power_balance(q_low, 0.40, 0.65, 0.10)
        self.assertGreater(balance_low["recirculating_percentage"], 100.0)
        self.assertFalse(balance_low["net_electrical_positive"])

    def test_cmf_commercial_viability(self):
        res = CentrifugalMirrorEngine.evaluate_cmf(self.params)
        self.assertFalse(res["is_commercially_viable"])


class TestAIActuatorLatencyEngine(unittest.TestCase):
    """Validates vacuum vessel inductive diffusion and AI response latency."""

    def setUp(self):
        self.params = AIControlLatencyParameters()

    def test_vacuum_vessel_diffusion_time(self):
        # tau_wall = 0.5 * mu_0 * sigma * d * r
        # 0.5 * (4*pi*1e-7) * 1.25e6 * 0.05 * 1.5 ~ 58.90 ms
        tau_s = AIActuatorLatencyEngine.calculate_vessel_diffusion_time(MU_0, 1.25e6, 0.05, 1.5)
        self.assertAlmostEqual(tau_s * 1000.0, 58.905, delta=0.01)

    def test_frequency_dependent_attenuation_and_phase_lag(self):
        tau_s = 0.058905
        # At 100 Hz, omega * tau = 2 * pi * 100 * 0.058905 ~ 37.01
        # Attenuation = 1 / sqrt(1 + 37.01^2) ~ 0.02701 (97.3% attenuation)
        att = AIActuatorLatencyEngine.calculate_field_attenuation(100.0, tau_s)
        self.assertAlmostEqual(att, 0.0270, delta=0.001)

        phase_lag = AIActuatorLatencyEngine.calculate_phase_lag_degrees(100.0, tau_s)
        self.assertGreater(phase_lag, 88.0)
        self.assertLess(phase_lag, 90.0)

    def test_spi_flight_time(self):
        # Flight time = 1.5 m / 300 m/s = 5.0 ms
        t_spi = AIActuatorLatencyEngine.calculate_spi_flight_time_ms(1.5, 300.0)
        self.assertAlmostEqual(t_spi, 5.0, delta=0.01)

    def test_ai_latency_limits_verdict(self):
        res = AIActuatorLatencyEngine.evaluate_ai_latency(self.params)
        self.assertTrue(res["wall_blocks_external_coils"])
        self.assertTrue(res["spi_too_slow_for_tq"])
        self.assertFalse(res["can_prevent_disruption_causally"])
        self.assertGreater(res["field_attenuation_percent"], 95.0)


class TestDirectDriveLaserICFEngine(unittest.TestCase):
    """Validates direct-drive laser ICF preheat, adiabat swelling, and chamber gas evacuation."""

    def setUp(self):
        self.params = DirectDriveLaserParameters()

    def test_hot_electron_temperature(self):
        # T_hot ~ 100 * ((1e15 * 0.351^2) / 1e15)^(1/3) = 100 * (0.1232)^(1/3) ~ 49.76 keV
        t_hot = DirectDriveLaserICFEngine.calculate_hot_electron_temp_kev(1e15, 0.351)
        self.assertAlmostEqual(t_hot, 49.76, delta=0.1)

    def test_driver_energy_penalty(self):
        # E_ign ~ (3.5 / 1.0)^3 = 42.875x
        penalty = DirectDriveLaserICFEngine.calculate_driver_energy_penalty(3.5 / 1.0)
        self.assertAlmostEqual(penalty, 42.875, delta=0.01)

    def test_chamber_volume_and_pumping_speed(self):
        vol = DirectDriveLaserICFEngine.calculate_chamber_volume_m3(5.0)
        self.assertAlmostEqual(vol, 523.6, delta=0.1)

        # S = (523.6 / 0.10) * ln(118.6 / 0.10) ~ 5236 * 7.078 ~ 37,062 m^3/s = 3.706e7 L/s
        s_pump = DirectDriveLaserICFEngine.calculate_required_pumping_speed(vol, 118.6, 0.10, 0.10)
        self.assertAlmostEqual(s_pump / 1000.0, 37.062, delta=0.1)

    def test_direct_drive_evaluation(self):
        res = DirectDriveLaserICFEngine.evaluate_direct_drive(self.params)
        self.assertGreater(res["commercial_cryopumps_required"], 700)
        self.assertFalse(res["is_industrially_feasible"])


class TestPulsedFRCBlanketEngine(unittest.TestCase):
    """Validates pulsed FRC blanket standoff geometry, stored energy, and switching dissipation."""

    def setUp(self):
        self.params = PulsedFRCBlanketParameters()

    def test_magnetic_stored_energy_scaling(self):
        # V_0 = pi * 0.35^2 * 5.0 ~ 1.924 m^3
        # V_1 = pi * 1.35^2 * 5.0 ~ 28.628 m^3
        # Ratio = (1.35 / 0.35)^2 = 14.8775
        vol_0, w_0 = PulsedFRCBlanketEngine.calculate_stored_magnetic_energy(10.0, 0.35, 5.0)
        vol_1, w_1 = PulsedFRCBlanketEngine.calculate_stored_magnetic_energy(10.0, 1.35, 5.0)

        self.assertAlmostEqual(vol_0, 1.924, delta=0.01)
        self.assertAlmostEqual(vol_1, 28.628, delta=0.01)
        self.assertAlmostEqual(w_1 / w_0, 14.878, delta=0.01)

    def test_switching_losses_vs_yield(self):
        res = PulsedFRCBlanketEngine.evaluate_standoff_scaling(self.params)
        self.assertAlmostEqual(res["shielded_stored_energy_mj"], 1139.06, delta=1.0)
        # Loss at 90% roundtrip efficiency is 10% of 1139.1 MJ = 113.9 MJ
        self.assertAlmostEqual(res["switching_loss_per_pulse_mj"], 113.91, delta=0.1)
        # Yield is 100 MJ, so loss exceeds yield
        self.assertGreater(res["switching_loss_to_yield_ratio"], 1.0)
        self.assertTrue(res["net_engineering_q_below_unity"])


class TestGrandUnifiedConsilienceMatrixEngine(unittest.TestCase):
    """Validates cross-architecture consilience table and macro chokepoints."""

    def test_ten_architecture_audit_coverage(self):
        audit = GrandUnifiedConsilienceMatrixEngine.audit_all_ten_architectures()
        self.assertEqual(len(audit), 10)
        for row in audit:
            self.assertEqual(row["verdict"], "IMPOSSIBLE")
            self.assertEqual(row["p_fleet_2040"], 0.0)
            self.assertGreaterEqual(row["earliest_foak_grid_year"], 2039.0)
            self.assertGreaterEqual(row["lcoe_floor_usd_mwh"], 180.0)

    def test_macro_chokepoints(self):
        macro = GrandUnifiedConsilienceMatrixEngine.calculate_macro_chokepoints()
        self.assertFalse(macro["commercial_fusion_by_2040_achievable"])
        self.assertEqual(macro["max_fleet_startups_at_15kg_inventory"], 1)
        self.assertGreater(macro["fission_fusion_density_ratio"], 200.0)


if __name__ == "__main__":
    unittest.main()
