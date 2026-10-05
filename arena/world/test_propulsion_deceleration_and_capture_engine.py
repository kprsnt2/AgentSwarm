"""
test_propulsion_deceleration_and_capture_engine.py

Comprehensive Verification Suite for:
1. Relativistic Rocket Rendezvous Staging Penalties.
2. Magnetic Sail Plasma Drag Kinematics and Deceleration Profiles.
3. Virial Theorem Structural Mass Limits on Superconducting Loops.
4. Gravitational Slingshot Capture Impossibility.
5. Hypervelocity Atmospheric Aerocapture Vaporization.
6. Definitive 9-Family Propulsion Feasibility Matrix.

Author: Kepler (Agent A001, Generation 0)
Domain: Practical space propulsion (propulsion)
"""

import unittest
import math
from propulsion_deceleration_and_capture_engine import (
    C,
    G0,
    AU,
    LY,
    RHO_ISM,
    B_ISM,
    relativistic_gamma,
    evaluate_rocket_rendezvous_penalty,
    evaluate_magsail_kinematics,
    evaluate_magsail_virial_mass,
    evaluate_gravitational_slingshot_capture_impossibility,
    evaluate_aerocapture_vaporization,
    get_definitive_propulsion_ranked_matrix,
)


class TestPropulsionDecelerationAndCaptureEngine(unittest.TestCase):

    def test_relativistic_gamma_and_kinetic_energy(self):
        gamma_01 = relativistic_gamma(0.10)
        self.assertAlmostEqual(gamma_01, 1.0050378, places=6)
        
        gamma_02 = relativistic_gamma(0.20)
        self.assertAlmostEqual(gamma_02, 1.0206207, places=6)
        
        with self.assertRaises(ValueError):
            relativistic_gamma(1.0)

    def test_fusion_rendezvous_staging_penalty(self):
        ve_fusion = 0.045 * C  # Daedalus class: 13,490 km/s
        res = evaluate_rocket_rendezvous_penalty(beta=0.10, ve_m_s=ve_fusion, epsilon_struct=0.05)
        
        # Flyby mass ratio ideal R_1 ~ 9.30
        self.assertAlmostEqual(res["r1_ideal"], 9.30, delta=0.05)
        # Rendezvous mass ratio ideal R_2 = R_1^2 ~ 86.49
        self.assertAlmostEqual(res["r2_ideal"], 86.49, delta=0.5)
        
        # Single stage limit is 1 / 0.05 = 20
        self.assertTrue(res["flyby_single_stage_possible"])
        self.assertFalse(res["rendezvous_single_stage_possible"])
        
        # Two-stage mass multiplier for rendezvous ~ 272.4 kg per kg payload
        self.assertAlmostEqual(res["m0_mL_rendezvous"], 272.4, delta=1.0)
        self.assertEqual(res["optimal_stages_rendezvous"], 2)

    def test_antimatter_rendezvous_staging(self):
        ve_am = 0.331 * C  # Beamed-core charged pions: 99,230 km/s
        res = evaluate_rocket_rendezvous_penalty(beta=0.10, ve_m_s=ve_am, epsilon_struct=0.05)
        
        # Ideal mass ratios
        self.assertAlmostEqual(res["r1_ideal"], 1.354, delta=0.01)
        self.assertAlmostEqual(res["r2_ideal"], 1.833, delta=0.02)
        
        # Single stage feasible for both flyby and rendezvous
        self.assertTrue(res["flyby_single_stage_possible"])
        self.assertTrue(res["rendezvous_single_stage_possible"])
        self.assertAlmostEqual(res["m0_mL_rendezvous"], 1.918, delta=0.05)
        self.assertEqual(res["optimal_stages_rendezvous"], 1)

    def test_chemical_interstellar_preclusion(self):
        ve_chem = 4432.0  # 452 s
        res = evaluate_rocket_rendezvous_penalty(beta=0.10, ve_m_s=ve_chem, epsilon_struct=0.05)
        
        # log10(R) > 2900
        self.assertGreater(res["log10_r1"], 2940.0)
        self.assertFalse(res["flyby_single_stage_possible"])
        self.assertFalse(res["rendezvous_single_stage_possible"])

    def test_magsail_kinematics_and_alfven_barrier(self):
        # 1000 kg probe with 100 m radius loop carrying 100 kA
        res = evaluate_magsail_kinematics(
            m_probe_kg=1000.0,
            r_loop_m=100.0,
            current_amp=1.0e5,
            beta_start=0.05,
            beta_final=0.00015
        )
        
        # Dipole moment M = 1e5 * pi * 100^2 = 3.14159e9 A*m^2
        self.assertAlmostEqual(res["dipole_moment_A_m2"], 3.14159e9, delta=1.0e6)
        
        # Magnetopause radius initial is ~1.42 km
        self.assertGreater(res["r_mp_initial_km"], 1.0)
        self.assertLess(res["r_mp_initial_km"], 10.0)
        
        # Magnetopause expands as probe decelerates: R_mp(v) ~ v^(-1/3)
        self.assertGreater(res["r_mp_final_km"], res["r_mp_initial_km"])
        self.assertAlmostEqual(res["r_mp_final_km"], 9.87, delta=1.0)
        
        # Alfvén speed in the ISM should be ~34.5 km/s
        self.assertAlmostEqual(res["v_alfven_m_s"], 34484.0, delta=500.0)
        self.assertAlmostEqual(res["beta_alfven"], 1.15e-4, delta=1.0e-5)
        
        # Stopping distance in light years
        self.assertGreater(res["x_decel_ly"], 0.1)

    def test_magsail_virial_mass_bounds(self):
        # 100 m radius coil carrying 100 kA
        res = evaluate_magsail_virial_mass(
            r_loop_m=100.0,
            current_amp=1.0e5,
            wire_radius_m=1.0e-4
        )
        
        # Stored magnetic energy is in the Megajoule regime (~7.5 MJ)
        self.assertGreater(res["stored_energy_mj"], 5.0)
        self.assertLess(res["stored_energy_mj"], 12.0)
        
        # Minimum virial structural mass using CNTs (sigma/rho = 4.28e7 J/kg)
        self.assertGreater(res["m_struct_min_kg"], 0.1)
        self.assertLess(res["m_struct_min_kg"], 1.0)
        
        # Superconductor mass: YBCO at Jc = 1e9 A/m^2 over 628 m loop weighs ~396 kg
        self.assertAlmostEqual(res["m_sc_kg"], 395.8, delta=2.0)
        
        # Total coil mass is ~396 kg, proving magsail is viable for 1-tonne probe but not 1-g wafercraft
        self.assertGreater(res["total_coil_mass_kg"], 300.0)
        self.assertLess(res["total_coil_mass_kg"], 500.0)

    def test_gravitational_slingshot_impossibility(self):
        # Hyperbolic entry at 0.05c and 0.20c
        res_05 = evaluate_gravitational_slingshot_capture_impossibility(v_inf_m_s=0.05 * C)
        self.assertFalse(res_05["capture_possible_gravitational_alone"])
        # Delta-v from slingshot is at most 11.4 km/s
        self.assertAlmostEqual(res_05["delta_v_slingshot_max_m_s"], 11400.0, delta=1.0)
        # Fraction of velocity changed is less than 0.1%
        self.assertLess(res_05["fraction_slingshot"], 0.001)
        # Grazing deflection angle at Proxima is negligible (< 300 arcseconds = 5 arcminutes)
        self.assertLess(res_05["deflection_arcsec"], 300.0)
        
        res_20 = evaluate_gravitational_slingshot_capture_impossibility(v_inf_m_s=0.20 * C)
        self.assertLess(res_20["fraction_slingshot"], 0.0002)
        self.assertLess(res_20["deflection_arcsec"], 20.0)

    def test_aerocapture_vaporization_physics(self):
        # Entry at 0.20c
        res_20 = evaluate_aerocapture_vaporization(beta=0.20)
        self.assertFalse(res_20["aerocapture_survivable"])
        # Kinetic energy per kg is ~1.8e15 J/kg
        self.assertGreater(res_20["specific_ke_j_kg"], 1.7e15)
        # Ratio to sublimation heat exceeds 10^7
        self.assertGreater(res_20["energy_vaporization_ratio"], 1.0e7)
        # Energy density exceeds 400 kt TNT per kg
        self.assertGreater(res_20["tnt_kt_per_kg"], 400.0)
        
        # Entry at 0.01c
        res_01 = evaluate_aerocapture_vaporization(beta=0.01)
        self.assertFalse(res_01["aerocapture_survivable"])
        self.assertGreater(res_01["energy_vaporization_ratio"], 1.0e4)

    def test_definitive_propulsion_ranked_matrix(self):
        matrix = get_definitive_propulsion_ranked_matrix()
        self.assertEqual(len(matrix), 9)
        
        # Check ranks 1 through 9
        for i, row in enumerate(matrix):
            self.assertEqual(row["rank"], i + 1)
            self.assertIn("name", row)
            self.assertIn("isp_s", row)
            self.assertIn("ve_km_s", row)
            self.assertIn("thrust_representative", row)
            self.assertIn("thrust_to_weight", row)
            self.assertIn("thrust_per_mw", row)
            self.assertIn("mission_domain", row)
            self.assertIn("interstellar_capable", row)
            self.assertIn("primary_blocker", row)
            
        # Verify interstellar capable drives
        capable_drives = [r["name"] for r in matrix if r["interstellar_capable"]]
        self.assertEqual(len(capable_drives), 3)
        self.assertIn("Nuclear Fusion (D-3He / Magnetic Nozzle)", capable_drives)
        self.assertIn("Antimatter Beamed-Core (p-pbar)", capable_drives)
        self.assertIn("Laser-Pushed Beamed Sail (Starshot)", capable_drives)


if __name__ == "__main__":
    unittest.main()
