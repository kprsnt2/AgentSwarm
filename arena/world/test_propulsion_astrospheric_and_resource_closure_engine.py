"""
test_propulsion_astrospheric_and_resource_closure_engine.py
===========================================================
Comprehensive unit and consilience tests for the astrospheric plasma dynamics,
superconducting magsail stability, and global resource/energy cycle closure engine.

Author: Kepler (Agent A001, Generation 0)
"""

import unittest
import math
from propulsion_astrospheric_and_resource_closure_engine import (
    C, G0, AU, LY, YEAR,
    magsail_dipole_moment,
    magsail_transverse_torque,
    magsail_angular_acceleration,
    magsail_bursting_stress,
    magsail_rupture_time,
    anti_helmholtz_quadrupole_analysis,
    superconductor_radiation_fluence,
    lunar_helium3_resource_cost,
    antimatter_industrial_cost,
    laser_sail_energy_and_economic_cost,
    ranked_propulsion_closure_matrix
)


class TestPropulsionAstrosphericAndResourceClosureEngine(unittest.TestCase):

    def test_magsail_dipole_and_torque(self):
        # 100 kA current, 100 m radius
        current = 1.0e5
        radius = 100.0
        m = magsail_dipole_moment(current, radius)
        expected_m = current * math.pi * (radius**2)
        self.assertAlmostEqual(m, expected_m, places=2)
        self.assertAlmostEqual(m, 3.1415926535e9, delta=1.0e5)

        # In a stellar wind field of 10 microTesla (1.0e-5 T)
        b_field = 1.0e-5
        tau = magsail_transverse_torque(m, b_field)
        expected_tau = m * b_field
        self.assertAlmostEqual(tau, expected_tau, places=2)
        self.assertAlmostEqual(tau, 31415.9265, delta=1.0)

    def test_magsail_angular_acceleration_radius_invariance(self):
        # Verify that alpha = 2*pi*I*B / M is mathematically invariant to loop radius
        current = 1.0e5
        b_field = 1.0e-5
        mass = 396.0

        alpha = magsail_angular_acceleration(current, b_field, mass)
        expected_alpha = (2.0 * math.pi * current * b_field) / mass
        self.assertAlmostEqual(alpha, expected_alpha, places=6)
        self.assertAlmostEqual(alpha, 0.0158666, places=5)

    def test_magsail_bursting_stress_and_rupture_time(self):
        current = 1.0e5
        b_field = 1.0e-5
        mass = 396.0
        radius = 100.0
        density = 6500.0  # kg/m^3 (Hastelloy substrate + YBCO)
        sigma_uts = 3.0e9  # 3 GPa

        res = magsail_rupture_time(current, b_field, mass, radius, density, sigma_uts)
        alpha = res["angular_acceleration_rad_s2"]
        t_rupture_s = res["rupture_time_seconds"]
        
        # Verify that at t_rupture, hoop stress equals sigma_uts
        omega_rupture = alpha * t_rupture_s
        stress = magsail_bursting_stress(density, omega_rupture, radius)
        self.assertAlmostEqual(stress, sigma_uts, delta=1.0e3)
        
        # Rupture time should be on the order of ~7 minutes (428 seconds)
        self.assertGreater(t_rupture_s, 400.0)
        self.assertLess(t_rupture_s, 500.0)
        self.assertAlmostEqual(res["rupture_time_minutes"], 7.14, delta=0.2)

    def test_anti_helmholtz_quadrupole_stability(self):
        current = 1.0e5
        radius = 100.0
        mass = 396.0

        quad = anti_helmholtz_quadrupole_analysis(current, radius, mass)
        self.assertEqual(quad["net_quadrupole_dipole_moment"], 0.0)
        self.assertEqual(quad["net_uniform_torque_n_m"], 0.0)
        self.assertTrue(quad["tumbling_instability_suppressed"])
        self.assertEqual(quad["mass_penalty_multiplier"], 2.0)
        self.assertEqual(quad["total_quadrupole_mass_kg"], 792.0)

    def test_superconductor_radiation_fluence(self):
        transit_years = 42.5
        gcr_flux = 4.0  # protons/cm^2/s
        flare_fluence_annual = 5.0e12  # protons/cm^2/year
        orbital_years = 10.0

        res = superconductor_radiation_fluence(
            transit_years, gcr_flux, flare_fluence_annual, orbital_years
        )
        self.assertGreater(res["cruise_gcr_fluence_cm2"], 5.0e9)
        self.assertLess(res["cruise_gcr_fluence_cm2"], 6.0e9)
        self.assertAlmostEqual(res["orbital_flare_fluence_cm2"], 5.0e13, delta=1.0e11)
        self.assertFalse(res["superconductor_quenched_by_radiation"])
        self.assertLess(res["damage_fraction"], 0.02)  # Less than 2% of critical damage

    def test_lunar_helium3_resource_cost(self):
        payload_mass = 1000.0  # 1 tonne
        res = lunar_helium3_resource_cost(payload_mass, beta=0.10, ve=1.349e7, structural_eps=0.05)
        
        # Check wet mass multiplier is ~272.4
        self.assertAlmostEqual(res["total_wet_mass_kg"] / payload_mass, 272.4, delta=1.5)
        
        # 3He required should be ~155 tonnes
        self.assertGreater(res["he3_fuel_mass_kg"], 140000.0)
        self.assertLess(res["he3_fuel_mass_kg"], 170000.0)
        
        # Regolith mined should be ~10.35 billion tonnes
        self.assertGreater(res["regolith_mined_billion_tonnes"], 9.0)
        self.assertLess(res["regolith_mined_billion_tonnes"], 12.0)
        
        # Thermal degassing energy in TWh should be ~2156 TWh (~7.7% of global annual electricity)
        self.assertGreater(res["thermal_degas_energy_twh"], 1800.0)
        self.assertLess(res["thermal_degas_energy_twh"], 2500.0)
        self.assertGreater(res["fraction_global_annual_electricity"], 0.05)
        self.assertLess(res["fraction_global_annual_electricity"], 0.10)

    def test_antimatter_industrial_cost(self):
        payload_mass = 1000.0  # 1 tonne
        res = antimatter_industrial_cost(payload_mass, beta=0.10, ve=9.923e7, structural_eps=0.05)
        
        # Wet mass is ~1.92 tonnes
        self.assertAlmostEqual(res["wet_mass_kg"], 1918.0, delta=10.0)
        
        # Propellant is ~872 kg (436 kg pbar)
        self.assertAlmostEqual(res["pbar_mass_kg"], 436.0, delta=10.0)
        
        # Grid energy is astronomical (> 10^10 TWh at eta = 10^-9)
        self.assertGreater(res["grid_energy_twh"], 2.0e10)
        self.assertGreater(res["years_current_global_power"], 700000.0)
        
        # Annihilation hazard is ~18,700 Megatons TNT (approx 375 Tsar Bombas)
        self.assertGreater(res["annihilation_energy_megatons_tnt"], 17000.0)
        self.assertLess(res["annihilation_energy_megatons_tnt"], 22000.0)
        self.assertGreater(res["tsar_bomba_multiples"], 340.0)

    def test_laser_sail_energy_and_economic_cost(self):
        # 1 gram wafercraft to 0.20c
        res = laser_sail_energy_and_economic_cost(payload_mass_kg=0.001, beta=0.20, laser_power_w=1.0e11)
        
        # Thrust for 100 GW beam is ~667 N
        self.assertAlmostEqual(res["thrust_newtons"], 667.12, delta=1.0)
        
        # Acceleration is ~6.67e5 m/s^2 (~68,000 g)
        self.assertGreater(res["acceleration_g"], 60000.0)
        self.assertLess(res["acceleration_g"], 75000.0)
        
        # Burn time is ~90 s
        self.assertAlmostEqual(res["burn_time_seconds"], 89.88, delta=1.0)
        
        # Energy consumed is ~8.988e12 J (~2,500 MWh = ~2.5 GWh)
        self.assertGreater(res["energy_consumed_mwh"], 2400.0)
        self.assertLess(res["energy_consumed_mwh"], 2600.0)
        self.assertAlmostEqual(res["energy_consumed_gwh"], 2.50, delta=0.1)
        
        # Launch electricity cost at $0.05/kWh is ~ $124,800
        self.assertGreater(res["electricity_cost_per_launch_usd"], 100000.0)
        self.assertLess(res["electricity_cost_per_launch_usd"], 150000.0)

    def test_ranked_closure_matrix_completeness(self):
        matrix = ranked_propulsion_closure_matrix()
        self.assertEqual(len(matrix), 10)
        
        # Check all required fields exist
        required_keys = [
            "rank", "name", "isp_s", "ve_km_s", "thrust_n_min", "thrust_n_max",
            "t_w", "f_p_ratio", "primary_domain", "interstellar_capable",
            "flyby_log10_r", "rendezvous_m0_mL", "primary_energy_cost",
            "single_biggest_blocker"
        ]
        for entry in matrix:
            for k in required_keys:
                self.assertIn(k, entry)
        
        # Check ranks 1 to 10 are consecutive
        ranks = [e["rank"] for e in matrix]
        self.assertEqual(ranks, list(range(1, 11)))
        
        # Interstellar capable engines: Fusion (7), Antimatter (8), Laser Sail (9)
        capable_ranks = [e["rank"] for e in matrix if e["interstellar_capable"]]
        self.assertEqual(capable_ranks, [7, 8, 9])


if __name__ == '__main__':
    unittest.main()
