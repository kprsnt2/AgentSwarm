#!/usr/bin/env python3
"""
test_relativistic_flight_frontiers.py
=====================================
Automated verification test suite for relativistic flight frontiers:
- Relativistic Ackeret-Stefan-Boltzmann rocket limits
- Interstellar dust mechanics and active deflection failure
- Sacrificial ablation and sail furling
- Exact 1g hyperbolic trajectories and CMB forward radiative flash
- Causality obstruction and chronology protection

Author: Raman (Agent A002, Generation 0)
Domain: Travel at or near light speed (lightspeed)
"""

import math
import unittest
from relativistic_flight_frontiers import (
    C, G0, YEAR, LY, SIGMA_SB, K_B, H_PLANCK, HBAR, EPS_0, Q_E, M_P, T_CMB, U_CMB,
    ackeret_mass_ratio, radiator_specific_mass, antimatter_engine_limits,
    dust_charge_to_mass, dust_field_emission_charge_to_mass,
    dust_magnetic_gyroradius, dust_lateral_deflection,
    cumulative_dust_ablation_thickness, single_grain_crater_depth, sail_furling_comparison,
    hyperbolic_trajectory_1g, cmb_forward_radiation_state,
    tolman_antitelephone_boost_velocity, cauchy_horizon_divergence_scaling,
    SHIELD_MATERIALS
)

class TestRelativisticFlightFrontiers(unittest.TestCase):

    def test_01_fundamental_constants(self):
        """Verify SI / CODATA physical constants and CMB rest energy density."""
        self.assertEqual(C, 299792458.0)
        self.assertEqual(G0, 9.80665)
        self.assertAlmostEqual(T_CMB, 2.7255, places=4)
        # u_CMB = 4 * sigma_SB * T^4 / c
        expected_u = (4.0 * SIGMA_SB / C) * (T_CMB**4)
        self.assertAlmostEqual(U_CMB, expected_u, places=18)
        self.assertTrue(4.17e-14 < U_CMB < 4.18e-14)

    def test_02_ackeret_mass_ratio(self):
        """Verify relativistic Ackeret rocket equation mass ratios."""
        # For photon rocket w = c: m0 / mf = sqrt((1+beta)/(1-beta))
        beta = 0.90
        mr_photon = ackeret_mass_ratio(beta, C)
        expected_mr = math.sqrt((1.0 + beta) / (1.0 - beta))
        self.assertAlmostEqual(mr_photon, expected_mr, places=6)
        self.assertAlmostEqual(mr_photon, math.sqrt(19.0), places=6) # sqrt(1.9 / 0.1) = sqrt(19) ~ 4.3588989

        # For beta = 0.99, photon rocket:
        mr_099 = ackeret_mass_ratio(0.99, C)
        self.assertAlmostEqual(mr_099, math.sqrt(199.0), places=6) # ~ 14.1067

        # For D-T fusion (w ~ 0.087c):
        w_fusion = 0.087 * C
        mr_fusion_01 = ackeret_mass_ratio(0.10, w_fusion)
        # Check that fusion mass ratio grows exponentially with beta
        self.assertTrue(mr_fusion_01 > 3.0)
        mr_fusion_02 = ackeret_mass_ratio(0.20, w_fusion)
        self.assertTrue(mr_fusion_02 > 10.0)

        # Invalid inputs
        with self.assertRaises(ValueError):
            ackeret_mass_ratio(1.0, C)
        with self.assertRaises(ValueError):
            ackeret_mass_ratio(0.5, 0.0)

    def test_03_radiator_specific_mass(self):
        """Verify Stefan-Boltzmann radiator specific mass scaling."""
        alpha_1000 = radiator_specific_mass(1000.0, eps_rad=0.90, sigma_panel=5.0)
        alpha_1200 = radiator_specific_mass(1200.0, eps_rad=0.90, sigma_panel=5.0)
        alpha_1800 = radiator_specific_mass(1800.0, eps_rad=0.90, sigma_panel=5.0)

        # Scaling alpha ~ T^-4: alpha(1000) / alpha(1800) = (1800/1000)^4 = 1.8^4 = 10.4976
        self.assertAlmostEqual(alpha_1000 / alpha_1800, 1.8**4, places=4)
        self.assertTrue(2.3e-5 < alpha_1200 < 2.4e-5)
        self.assertTrue(4.6e-6 < alpha_1800 < 4.7e-6)

    def test_04_antimatter_engine_limits_and_radiator_paradox(self):
        """Verify the Relativistic Thermal Radiator Paradox for antimatter rockets."""
        res = antimatter_engine_limits(
            f_waste=0.05,
            w_eff=0.60 * C,
            t_rad=1800.0,
            eps_rad=0.90,
            sigma_panel=5.0
        )
        # Waste heat per Newton of thrust: ~41.64 MW / N
        self.assertAlmostEqual(res["p_waste_per_newton_W_N"] / 1e6, 41.6378, places=3)
        # Radiator mass per Newton of thrust: ~194.3 kg / N
        self.assertAlmostEqual(res["m_rad_per_newton_kg_N"], 194.30, places=1)
        # Maximum acceleration: ~ 0.00515 m/s^2 (~ 0.00052 g)
        self.assertAlmostEqual(res["a_max_m_s2"], 0.005147, places=5)
        self.assertTrue(5.1e-4 < res["a_max_g0"] < 5.3e-4)
        # Acceleration time to 0.2c: ~380 years
        self.assertTrue(370.0 < res["tau_accel_years"] < 390.0)
        # Acceleration distance to 0.2c: ~38 light-years
        self.assertTrue(37.0 < res["d_accel_ly"] < 39.0)

    def test_05_dust_charge_to_mass(self):
        """Verify dust grain equilibrium and field emission charge-to-mass ratios."""
        r_1um = 1.0e-6
        qm_eq = dust_charge_to_mass(r_1um, u_potential_v=3.0, rho_grain=2500.0)
        # q/m = 3 * eps0 * 3 / (2500 * 1e-12) ~ 3.1875e-2 C/kg
        self.assertAlmostEqual(qm_eq, 0.031875, places=5)

        qm_max = dust_field_emission_charge_to_mass(r_1um, e_crit_v_m=1.0e9, rho_grain=2500.0)
        # q_max/m = 3 * eps0 * 1e9 / (2500 * 1e-6) ~ 10.625 C/kg
        self.assertAlmostEqual(qm_max, 10.625, places=3)

    def test_06_dust_magnetic_gyroradius(self):
        """Verify that dust magnetic gyroradius is astronomically large (deflection failure)."""
        r_1um = 1.0e-6
        rg_eq = dust_magnetic_gyroradius(r_1um, beta=0.20, b_field_tesla=5.0)
        # Gyroradius at 5 Tesla for 1 um grain is ~ 383,967 km (larger than Earth-Moon distance!)
        self.assertTrue(rg_eq > 3.8e8) # > 380,000 km
        
        rg_max = dust_magnetic_gyroradius(r_1um, beta=0.20, b_field_tesla=5.0, use_field_emission_limit=True)
        # Even at extreme field emission limit, gyroradius is > 1,150 km!
        self.assertTrue(rg_max > 1.15e6) # > 1,150 km

    def test_07_dust_lateral_deflection(self):
        """Verify that lateral displacement across a 10m shield field is negligible."""
        r_1um = 1.0e-6
        dy_eq = dust_lateral_deflection(r_1um, beta=0.20, l_field_m=10.0, b_field_tesla=5.0)
        # dy_eq ~ 1.30e-7 m = 0.13 um!
        self.assertAlmostEqual(dy_eq * 1e6, 0.1302, places=3)

        dy_max = dust_lateral_deflection(r_1um, beta=0.20, l_field_m=10.0, b_field_tesla=5.0, use_field_emission_limit=True)
        # dy_max ~ 4.34e-5 m = 0.043 mm!
        self.assertAlmostEqual(dy_max * 1e3, 0.0434, places=3)

    def test_08_cumulative_dust_ablation(self):
        """Verify cumulative dust ablation depth for graphite and other materials."""
        res_graphite_02 = cumulative_dust_ablation_thickness(0.20, 4.244 * LY, "Graphite")
        # Graphite ablation depth at 0.2c: ~ 2.77 mm
        self.assertAlmostEqual(res_graphite_02["ablation_depth_mm"], 2.772, places=2)
        # Mass lost: ~ 6.26 kg/m^2
        self.assertAlmostEqual(res_graphite_02["mass_lost_kg_m2"], 6.265, places=2)

        res_graphite_05 = cumulative_dust_ablation_thickness(0.50, 4.244 * LY, "Graphite")
        # At 0.5c, ablation depth is ~ 20.8 mm
        self.assertAlmostEqual(res_graphite_05["ablation_depth_mm"], 20.796, places=2)

        res_beryllium_02 = cumulative_dust_ablation_thickness(0.20, 4.244 * LY, "Beryllium")
        # Beryllium ablation depth at 0.2c: ~ 6.23 mm
        self.assertAlmostEqual(res_beryllium_02["ablation_depth_mm"], 6.229, places=2)

    def test_09_single_grain_crater_depth(self):
        """Verify explosive crater penetration depth for discrete dust grains."""
        # 10 um grain at beta = 0.2 in Graphite
        res = single_grain_crater_depth(10.0e-6, beta=0.20, material="Graphite")
        # Grain mass: (4/3) * pi * 2500 * (1e-5)^3 ~ 1.047e-11 kg
        self.assertAlmostEqual(res["m_grain_kg"], 1.0472e-11, places=14)
        # Kinetic energy: ~ 19.4 kJ (~ 4.64 g TNT)
        self.assertAlmostEqual(res["e_k_joules"], 19407.7, places=1)
        self.assertAlmostEqual(res["tnt_equivalent_grams"], 4.6387, places=2)
        # Crater depth: ~ 2.74 mm
        self.assertAlmostEqual(res["crater_depth_mm"], 2.74, places=2)

    def test_10_sail_furling_comparison(self):
        """Verify mass reduction achieved by furling laser sail edge-on during cruise."""
        res = sail_furling_comparison(
            beta=0.20,
            distance_m=4.244 * LY,
            sail_area_face_on=16.0,
            chip_area_edge_on=1.0e-4,
            material="Graphite"
        )
        # Face-on 16 m^2 requires ~ 100.2 kg of graphite shield!
        self.assertAlmostEqual(res["shield_mass_face_on_kg"], 100.238, places=2)
        # Edge-on 1 cm^2 requires only ~ 0.626 grams of graphite!
        self.assertAlmostEqual(res["shield_mass_edge_on_grams"], 0.6265, places=3)
        self.assertAlmostEqual(res["mass_reduction_factor"], 160000.0, places=1)

    def test_11_hyperbolic_trajectory_1g(self):
        """Verify exact relativistic 1g proper-time trajectories."""
        # Proxima Centauri (4.244 ly)
        proxima = hyperbolic_trajectory_1g(4.244 * LY)
        self.assertAlmostEqual(proxima["tau_total_years"], 3.54, places=2)
        self.assertAlmostEqual(proxima["t_total_years"], 5.87, places=2)
        self.assertAlmostEqual(proxima["gamma_peak"], 3.19, places=2)
        self.assertAlmostEqual(proxima["beta_peak"], 0.9496, places=3)

        # Tau Ceti (11.9 ly)
        tau_ceti = hyperbolic_trajectory_1g(11.9 * LY)
        self.assertAlmostEqual(tau_ceti["tau_total_years"], 5.14, places=2)
        self.assertAlmostEqual(tau_ceti["t_total_years"], 13.70, places=2)
        self.assertAlmostEqual(tau_ceti["gamma_peak"], 7.10, places=1)

        # Galactic Center (26,000 ly)
        gc = hyperbolic_trajectory_1g(26000.0 * LY)
        self.assertAlmostEqual(gc["tau_total_years"], 19.76, places=2)
        self.assertAlmostEqual(gc["t_total_years"], 26001.94, places=1)
        self.assertAlmostEqual(gc["gamma_peak"], 13420.8, places=0)
        self.assertAlmostEqual(gc["aberration_cone_arcsec"], 15.37, places=1)

        # Andromeda (2.54 Mly)
        m31 = hyperbolic_trajectory_1g(2.54e6 * LY)
        self.assertAlmostEqual(m31["tau_total_years"], 28.63, places=2)
        self.assertAlmostEqual(m31["t_total_years"], 2540001.94, places=0)
        self.assertAlmostEqual(m31["gamma_peak"], 1311016.0, places=-3)

    def test_12_cmb_forward_radiation_state(self):
        """Verify the Forward Radiative Flash from Doppler-shifted CMB at high gamma."""
        # At Galactic Center midpoint: gamma = 13420.8
        beta_gc = math.sqrt(1.0 - 1.0 / (13420.8**2))
        res_gc = cmb_forward_radiation_state(13420.8, beta_gc)
        # Forward flux is ~ 3.01 kW/m^2
        self.assertTrue(3000.0 < res_gc["flux_W_m2"] < 3010.0)
        # Forward temperature is ~ 73,157 K
        self.assertTrue(73000.0 < res_gc["t_forward_K"] < 73500.0)
        # Peak photon energy is ~ 31.3 eV (ionizing extreme UV)
        self.assertTrue(31.0 < res_gc["e_peak_eV"] < 32.0)

        # At Andromeda midpoint: gamma = 1311016.0
        beta_m31 = math.sqrt(1.0 - 1.0 / (1311016.0**2))
        res_m31 = cmb_forward_radiation_state(1311016.0, beta_m31)
        # Forward flux is ~ 28.7 MW/m^2!
        self.assertTrue(2.8e7 < res_m31["flux_W_m2"] < 2.9e7)
        # Forward temperature is ~ 7.15 million K!
        self.assertTrue(7.1e6 < res_m31["t_forward_K"] < 7.2e6)
        # Peak photon energy is ~ 3.06 keV (hard X-rays)
        self.assertTrue(3.0e3 < res_m31["e_peak_eV"] < 3.1e3)

    def test_13_causality_obstruction(self):
        """Verify Tolman antitelephone threshold velocity for closed timelike loops."""
        # For U = 2c: v_thresh = 2 * c^2 * (2c) / (4c^2 + c^2) = 4/5 c = 0.8c
        v_thresh_2c = tolman_antitelephone_boost_velocity(2.0 * C)
        self.assertAlmostEqual(v_thresh_2c / C, 0.80, places=6)

        # For U = 10c: v_thresh = 20/101 c ~ 0.198c
        v_thresh_10c = tolman_antitelephone_boost_velocity(10.0 * C)
        self.assertAlmostEqual(v_thresh_10c / C, 20.0 / 101.0, places=6)

        # As U -> c, v_thresh -> c
        v_thresh_1001c = tolman_antitelephone_boost_velocity(1.001 * C)
        self.assertTrue(v_thresh_1001c > 0.999 * C)

        with self.assertRaises(ValueError):
            tolman_antitelephone_boost_velocity(C)

    def test_14_cauchy_horizon_divergence(self):
        """Verify vacuum stress-energy tensor divergence scaling near Cauchy horizon."""
        t1 = 1.0e-3 # 1 ms
        t2 = 1.0e-6 # 1 us
        div1 = cauchy_horizon_divergence_scaling(t1)
        div2 = cauchy_horizon_divergence_scaling(t2)
        # Quartic scaling: (t1 / t2)^4 = 1000^4 = 1e12
        self.assertAlmostEqual(div2 / div1, 1.0e12, places=3)
        self.assertTrue(div2 > 1.0e-14)


if __name__ == "__main__":
    unittest.main()
