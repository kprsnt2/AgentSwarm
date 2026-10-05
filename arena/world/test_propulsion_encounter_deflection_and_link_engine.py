"""
test_propulsion_encounter_deflection_and_link_engine.py

Unit test harness verifying:
1. Electrostatic dust deflection physical breakdown limit (Petavolts and Earth-sized radii).
2. Magnetic dust deflection gyroradius scale (~115,000 km) and negligible lateral deflection.
3. Relativistic planetary encounter slew rate (~344 deg/s) and sub-20-microsecond exposure limits.
4. Interstellar optical link budget comparison (10 m telescope vs 1 km synthetic receiver array).
5. Completeness of 9-family ranked propulsion matrix and engineering blockers.

Author: Kepler (Agent A001, Generation 0)
"""

import unittest
import math
from propulsion_encounter_deflection_and_link_engine import (
    evaluate_electrostatic_deflection,
    evaluate_magnetic_deflection,
    evaluate_planetary_encounter_kinematics,
    evaluate_interstellar_optical_link,
    get_complete_ranked_propulsion_catalog,
    relativistic_gamma,
    C,
    DIST_PROXIMA,
    AU
)


class TestPropulsionEncounterDeflectionAndLinkEngine(unittest.TestCase):

    def test_relativistic_gamma(self):
        gamma_02 = relativistic_gamma(0.20)
        self.assertAlmostEqual(gamma_02, 1.0206207, places=6)
        with self.assertRaises(ValueError):
            relativistic_gamma(1.0)

    def test_electrostatic_deflection_impossibility(self):
        res = evaluate_electrostatic_deflection(
            grain_radius_m=1.0e-6,
            grain_density=2500.0,
            beta=0.20,
            grain_potential_volts=5.0,
            breakdown_field_v_per_m=1.0e9
        )
        self.assertFalse(res["is_feasible"])
        # Kinetic energy of 1 um grain at 0.2c should be ~ 19.41 Joules
        self.assertAlmostEqual(res["grain_ke_joules"], 19.405, delta=0.1)
        # Charge of grain ~ 5.56e-16 C (~3472 elementary charges)
        self.assertAlmostEqual(res["grain_charge_coulombs"], 5.563e-16, delta=1e-18)
        self.assertAlmostEqual(res["elementary_charges"], 3472.0, delta=10.0)
        # Required voltage ~ 34.88 Petavolts
        self.assertAlmostEqual(res["v_repel_petavolts"], 34.88, delta=0.5)
        # Conductor radius at 1 GV/m breakdown limit ~ 34,880 km (~ 5.47 Earth radii / 2.74 Earth diameters)
        self.assertAlmostEqual(res["r_sphere_min_km"], 34880.0, delta=500.0)
        self.assertGreater(res["r_earth_ratio"], 2.5)
        # Stored electrostatic energy exceeds 10^30 Joules
        self.assertGreater(res["stored_energy_joules"], 1.0e30)

    def test_magnetic_deflection_impossibility(self):
        res = evaluate_magnetic_deflection(
            grain_radius_m=1.0e-6,
            grain_density=2500.0,
            beta=0.20,
            grain_potential_volts=5.0,
            b_field_tesla=10.0,
            shield_length_m=1.0
        )
        self.assertFalse(res["is_feasible"])
        # Gyroradius ~ 115,000 km
        self.assertAlmostEqual(res["r_gyroradius_km"], 115200.0, delta=2000.0)
        # Lateral deflection over 1 m shield is sub-10 nanometers (< 1e-8 m)
        self.assertLess(res["lateral_deflection_nm"], 10.0)
        self.assertGreater(res["lateral_deflection_nm"], 1.0)

    def test_planetary_encounter_kinematics(self):
        res = evaluate_planetary_encounter_kinematics(
            beta=0.20,
            impact_parameter_km=10000.0,
            detection_envelope_km=100000.0,
            desired_surface_resolution_km=1.0
        )
        self.assertAlmostEqual(res["v_km_s"], 59958.49, delta=1.0)
        # Duration within 100,000 km envelope ~ 3.32 seconds
        self.assertAlmostEqual(res["transit_duration_envelope_s"], 3.319, delta=0.01)
        # Maximum slew rate ~ 5.996 rad/s = 343.5 deg/s
        self.assertAlmostEqual(res["max_slew_rate_rad_s"], 5.9958, delta=0.01)
        self.assertAlmostEqual(res["max_slew_rate_deg_s"], 343.54, delta=0.5)
        # Angular acceleration > 1000 deg/s^2
        self.assertGreater(res["max_angular_accel_deg_s2"], 1000.0)
        # Exposure time at 1 km resolution ~ 16.68 microseconds
        self.assertAlmostEqual(res["max_exposure_time_us"], 16.68, delta=0.1)

    def test_interstellar_optical_link_10m_vs_1km(self):
        # 10m receiver (ELT class)
        res_10m = evaluate_interstellar_optical_link(
            distance_ly=4.244,
            laser_power_w=1.0,
            wavelength_m=1.064e-6,
            d_tx_m=0.35,
            d_rx_m=10.0,
            photons_per_bit=10.0,
            compressed_image_mb=2.0
        )
        # Beam footprint diameter at Earth ~ 2 AU
        self.assertAlmostEqual(res_10m["footprint_diameter_au"], 1.99, delta=0.1)
        # Received photon rate ~ 0.00302 photons/second (1 photon every 331 s)
        self.assertAlmostEqual(res_10m["photon_rate_hz"], 0.003019, delta=0.0001)
        # Data rate ~ 0.000302 bps
        self.assertAlmostEqual(res_10m["data_rate_bps"], 0.0003019, delta=0.00002)
        # Transmission time for 2 MB image ~ 1,760 years
        self.assertGreater(res_10m["tx_time_days"], 500000.0)

        # 1 km synthetic aperture receiver array (repurposed Starshot launch array)
        res_1km = evaluate_interstellar_optical_link(
            distance_ly=4.244,
            laser_power_w=1.0,
            wavelength_m=1.064e-6,
            d_tx_m=0.35,
            d_rx_m=1000.0,
            photons_per_bit=10.0,
            compressed_image_mb=2.0
        )
        # 10,000x gain in received power over 10m
        self.assertAlmostEqual(res_1km["received_power_w"] / res_10m["received_power_w"], 10000.0, delta=1.0)
        # Photon rate ~ 30.19 photons/s
        self.assertAlmostEqual(res_1km["photon_rate_hz"], 30.19, delta=0.2)
        # Data rate ~ 3.02 bps
        self.assertAlmostEqual(res_1km["data_rate_bps"], 3.019, delta=0.05)
        # Transmission time for 2 MB image ~ 64.3 days
        self.assertAlmostEqual(res_1km["tx_time_days"], 64.3, delta=1.0)

    def test_ranked_catalog_integrity(self):
        catalog = get_complete_ranked_propulsion_catalog()
        self.assertEqual(len(catalog), 9)
        # Check ranks 1 to 9
        for i, entry in enumerate(catalog, start=1):
            self.assertEqual(entry["rank"], i)
            self.assertIn("engineering_blocker", entry)
            self.assertIn("mission_domain", entry)
            self.assertIn("thrust_per_mw_n", entry)
            self.assertGreater(len(entry["engineering_blocker"]), 20)
        # Exactly 3 families can clear interstellar
        interstellar_families = [e for e in catalog if e["interstellar_capable"]]
        self.assertEqual(len(interstellar_families), 3)
        interstellar_names = [e["name"] for e in interstellar_families]
        self.assertIn("Nuclear Fusion (D-3He)", interstellar_names)
        self.assertIn("Antimatter Beamed-Core", interstellar_names)
        self.assertIn("Laser-Pushed Beamed Sail", interstellar_names)

    def test_electrostatic_energy_exceeds_terajoules(self):
        res = evaluate_electrostatic_deflection()
        # Stored energy ~ 2.36e30 Joules
        self.assertGreater(res["stored_energy_joules"], 2.0e30)
        self.assertLess(res["stored_energy_joules"], 3.0e30)

    def test_nanometer_deflection_sub_micron(self):
        res = evaluate_magnetic_deflection(grain_radius_m=0.1e-6)
        # Even for 0.1 um grain, gyroradius is > 1,000 km
        self.assertGreater(res["r_gyroradius_km"], 1000.0)

    def test_exposure_time_at_sub_km_resolution(self):
        res = evaluate_planetary_encounter_kinematics(desired_surface_resolution_km=0.1)
        # 100 m resolution requires 1.67 microseconds exposure
        self.assertAlmostEqual(res["max_exposure_time_us"], 1.668, delta=0.01)


if __name__ == "__main__":
    unittest.main()
