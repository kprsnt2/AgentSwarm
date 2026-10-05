"""
test_fusion_advanced_frontiers_and_grand_closure_engine.py
===========================================================
Comprehensive unit test suite for:
- MagnetizedTargetFusionEngine (RT instability, lead quench, acoustic cavitation, rep-rate)
- ProtonBoronAneutronicEngine (Bremsstrahlung clamp, Rider's theorem, secondary neutrons)
- TokamakDisruptionDynamicsEngine (Thermal quench ablation, runaway avalanches, halo forces)
- CryogenicCarnotBalanceOfPlantEngine (Carnot COP, inboard standoff shielding paradox)
- GrandConsilienceClosureEngine (Unanimous 8-architecture 2040 commercial impossibility)

Epistemic Class: Engineering Feasibility Verification
Author: Kepler (A001, Generation 0)
"""

import unittest
import math
from fusion_advanced_frontiers_and_grand_closure_engine import (
    MagnetizedTargetFusionParameters,
    MagnetizedTargetFusionEngine,
    ProtonBoronParameters,
    ProtonBoronAneutronicEngine,
    TokamakDisruptionParameters,
    TokamakDisruptionDynamicsEngine,
    CryogenicCarnotParameters,
    CryogenicCarnotBalanceOfPlantEngine,
    GrandConsilienceClosureEngine
)


class TestMagnetizedTargetFusionEngine(unittest.TestCase):
    """Verifies physical and engineering models for acoustic/piston MTF."""
    def setUp(self):
        self.engine = MagnetizedTargetFusionEngine()

    def test_speed_of_sound_pbli(self):
        # c_s = sqrt(30.5e9 / 9400) ~ 1801.3 m/s
        cs = self.engine.speed_of_sound_m_s()
        self.assertAlmostEqual(cs, 1801.3, delta=2.0)

    def test_effective_deceleration_and_rt_growth(self):
        # a_dec = 2 * (0.30 - 0.05) / (1.5e-3)^2 ~ 2.22e5 m/s^2
        a_dec = self.engine.effective_deceleration_m_s2()
        self.assertAlmostEqual(a_dec, 2.222e5, delta=1000.0)

        # Growth rate for mode 20: gamma = sqrt(k * g) > 5000 s^-1
        gamma = self.engine.rayleigh_taylor_growth_rate_s_inv(mode_m=20)
        self.assertGreater(gamma, 4000.0)

        # Amplification exp(gamma * tau) > 1000x
        amp = self.engine.rayleigh_taylor_amplification(mode_m=20)
        self.assertGreater(amp, 1000.0)

    def test_critical_lead_impurity_and_mass(self):
        # Critical impurity fraction should be small (~ 1e-4 to 2e-3)
        f_crit = self.engine.critical_lead_impurity_fraction()
        self.assertGreater(f_crit, 1.0e-5)
        self.assertLess(f_crit, 0.01)

        # Total lead mass to extinguish core should be less than 1.0 gram (in fact < 0.1 g)
        m_lead_g = self.engine.critical_lead_mass_to_quench_grams()
        self.assertLess(m_lead_g, 1.0)
        self.assertGreater(m_lead_g, 0.0)

    def test_acoustic_shock_and_cavitation_impact(self):
        # Acoustic impedance Z ~ 1.69e7 Pa*s/m
        z = self.engine.acoustic_impedance_pa_s_m()
        self.assertAlmostEqual(z, 1.693e7, delta=0.05e7)

        # Piston impact velocity for 100 MPa shock ~ 5.9 m/s
        v_p = self.engine.piston_impact_velocity_m_s()
        self.assertAlmostEqual(v_p, 5.91, delta=0.1)

        # Total kinetic energy of 500 pistons (250 t) ~ 4.36 MJ
        ke_mj = self.engine.piston_total_kinetic_energy_mj()
        self.assertAlmostEqual(ke_mj, 4.36, delta=0.2)

        # Cavitation microjet water-hammer impact pressure > 2.0 GPa
        p_impact_gpa = self.engine.cavitation_microjet_impact_pressure_gpa()
        self.assertGreater(p_impact_gpa, 2.0)

        # Impact stress exceeds Eurofer97 UTS (650 MPa) by > 3x
        stress_ratio = self.engine.vessel_cavitation_fatigue_stress_ratio()
        self.assertGreater(stress_ratio, 3.0)

    def test_repetition_rate_and_net_power(self):
        # Hydrodynamic settling limits rep rate to <= 1.0 Hz
        rep_rate = self.engine.max_hydrodynamic_repetition_rate_hz()
        self.assertLessEqual(rep_rate, 1.0)
        self.assertGreater(rep_rate, 0.3)

        # Net electric power is bounded
        p_net = self.engine.net_electrical_output_mwe()
        self.assertLess(p_net, 35.0)


class TestProtonBoronAneutronicEngine(unittest.TestCase):
    """Verifies Bremsstrahlung, Rider theorem, and neutron models for p-11B."""
    def setUp(self):
        self.engine = ProtonBoronAneutronicEngine()

    def test_stoichiometry_and_effective_charge(self):
        # For xi = 0.15: n_e / n_p = 1 + 5*0.15 = 1.75
        ne_np = self.engine.electron_to_proton_density_ratio()
        self.assertAlmostEqual(ne_np, 1.75, places=4)

        # Z_eff = (1 + 25*0.15) / 1.75 = 4.75 / 1.75 ~ 2.714
        z_eff = self.engine.effective_charge_z_eff()
        self.assertAlmostEqual(z_eff, 4.75 / 1.75, places=3)

    def test_bremsstrahlung_impossibility_in_thermal_equilibrium(self):
        # Thermal power ratio P_fus / P_brem must be strictly < 1.0 everywhere
        is_possible = self.engine.is_thermal_ignition_possible()
        self.assertFalse(is_possible)

        # Peak ratio should be well below 1.0 (~ 0.35 - 0.50)
        best_t, best_r = self.engine.peak_thermal_power_ratio()
        self.assertGreaterEqual(best_t, 150.0)
        self.assertLessEqual(best_t, 250.0)
        self.assertLess(best_r, 0.60)
        self.assertGreater(best_r, 0.20)

    def test_rider_non_equilibrium_theorem(self):
        # At T_i = 300 keV, T_e = 30 keV, Spitzer transfer power P_ie must exceed P_fus
        p_fus = self.engine.fusion_power_density_coeff(300.0)
        p_ie = self.engine.rider_spitzer_transfer_power_coeff(300.0, 30.0)
        ratio_ie_fus = p_ie / p_fus
        self.assertGreater(ratio_ie_fus, 10.0)

        # Recirculating power fraction must exceed 100% (in fact > 1000%)
        f_recirc = self.engine.rider_recirculating_power_ratio(300.0, 30.0)
        self.assertGreater(f_recirc, 5.0)

    def test_secondary_neutron_production_rate(self):
        # 1000 MWth p-11B produces > 1e17 secondary neutrons/sec
        n_rate = self.engine.secondary_neutron_production_rate()
        self.assertGreater(n_rate, 1.0e17)


class TestTokamakDisruptionDynamicsEngine(unittest.TestCase):
    """Verifies thermal quench, current quench, and halo force models."""
    def setUp(self):
        self.engine = TokamakDisruptionDynamicsEngine()

    def test_thermal_quench_energy_density_and_ablation(self):
        # Psi_TQ = 100 / (2.5 * sqrt(0.0015)) ~ 1032.8 MJ/(m^2*s^0.5)
        psi = self.engine.thermal_quench_energy_density_factor()
        self.assertAlmostEqual(psi, 1032.8, delta=10.0)

        # Exceeds tungsten limit (45 MJ/(m^2*s^0.5)) by > 20x
        self.assertGreater(psi / self.engine.p.tungsten_ablation_threshold_mj_m2_s05, 20.0)

        # Melt depth > 3 mm per disruption
        melt_depth = self.engine.thermal_quench_melt_depth_mm()
        self.assertGreater(melt_depth, 3.0)
        self.assertLess(melt_depth, 5.0)

    def test_current_quench_induced_field_and_avalanche(self):
        # E_ind = (10e-6 * 9e6 / 0.015) / (2*pi*3.3) ~ 289.4 V/m
        e_ind = self.engine.induced_electric_field_v_m()
        self.assertAlmostEqual(e_ind, 289.4, delta=2.0)

        # E_c ~ 0.081 V/m
        e_c = self.engine.critical_dreicer_electric_field_v_m()
        self.assertLess(e_c, 0.15)
        self.assertGreater(e_c, 0.05)

        # E / E_c > 2000
        self.assertGreater(e_ind / e_c, 2000.0)

        # Avalanche multiplication factor > 500x
        m_av = self.engine.runaway_avalanche_multiplication()
        self.assertGreater(m_av, 500.0)

    def test_halo_lorentz_force(self):
        # F_halo = 12 T * (0.30 * 9 MA) * 2.0 m = 64.8 MN
        f_halo = self.engine.asymmetric_halo_lorentz_force_mn()
        self.assertAlmostEqual(f_halo, 64.8, delta=0.5)


class TestCryogenicCarnotBalanceOfPlantEngine(unittest.TestCase):
    """Verifies Carnot COP and magnet nuclear shielding penalty models."""
    def setUp(self):
        self.engine = CryogenicCarnotBalanceOfPlantEngine()

    def test_carnot_cop_values(self):
        # At 20 K: COP_ideal = 20 / 280 = 0.0714, COP_real = 0.28 * 0.0714 = 0.0200
        # W_e / W_th = 50.0
        w_hts = self.engine.electric_watts_per_thermal_watt(20.0, is_hts=True)
        self.assertAlmostEqual(w_hts, 50.0, places=1)

        # At 4.2 K: COP_ideal = 4.2 / 295.8 = 0.0142, COP_real = 0.25 * 0.0142 = 0.00355
        # W_e / W_th = 281.7
        w_lts = self.engine.electric_watts_per_thermal_watt(4.2, is_hts=False)
        self.assertAlmostEqual(w_lts, 281.7, delta=1.0)

    def test_nuclear_heating_and_standoff_paradox(self):
        # Thickness 0.70 m: Deposited heat ~ 126.8 kWth -> HTS Cryo power ~ 6.34 MWe
        p_cryo_07 = self.engine.cryogenic_electric_power_mw(0.70, is_hts=True)
        self.assertAlmostEqual(p_cryo_07, 6.34, delta=0.2)

        # Thickness 0.40 m: Deposited heat ~ 5390 kWth -> HTS Cryo power ~ 269.5 MWe
        p_cryo_04 = self.engine.cryogenic_electric_power_mw(0.40, is_hts=True)
        self.assertGreater(p_cryo_04, 250.0)

        # LTS at 0.40 m requires > 1400 MWe (exceeding total plant output)
        p_cryo_04_lts = self.engine.cryogenic_electric_power_mw(0.40, is_hts=False)
        self.assertGreater(p_cryo_04_lts, 1400.0)


class TestGrandConsilienceClosureEngine(unittest.TestCase):
    """Verifies grand consilience audit across all 8 fusion architectures."""
    def setUp(self):
        self.closure = GrandConsilienceClosureEngine()
        self.results = self.closure.evaluate_all_architectures()

    def test_all_8_architectures_present(self):
        self.assertEqual(len(self.results), 8)
        expected_keys = [
            "1_Compact_Tokamak_ARC",
            "2_Modular_Stellarator_W7X",
            "3_Laser_ICF_NIF",
            "4_Pulsed_FRC_Helion",
            "5_Sheared_Flow_ZPinch_Zap",
            "6_Magnetized_Target_Fusion_GF",
            "7_Advanced_Fuel_pB11_TAE",
            "8_Subcritical_Fusion_Fission_Hybrid"
        ]
        for k in expected_keys:
            self.assertIn(k, self.results)

    def test_unanimous_commercial_impossibility(self):
        for name, data in self.results.items():
            self.assertEqual(
                data["commercial_verdict_2040"],
                "IMPOSSIBLE",
                f"Architecture {name} should be IMPOSSIBLE"
            )
            self.assertEqual(
                data["p_fleet_commercial_by_2040"],
                0.00,
                f"Fleet probability for {name} must be 0.00"
            )
            self.assertGreaterEqual(data["earliest_foak_grid_year"], 2039.0)


if __name__ == "__main__":
    unittest.main()
