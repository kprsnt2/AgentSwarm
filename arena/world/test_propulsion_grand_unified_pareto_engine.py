"""
test_propulsion_grand_unified_pareto_engine.py
==============================================
Comprehensive Verification Suite for:
1. Exact Relativistic Propulsion Mechanics and Rapidity Calculations.
2. Fishback-Powell Ramjet Drag Wall and Bremsstrahlung Radiative Collapse.
3. Multi-Stage Relativistic Rocket Scaling and 1/epsilon Structural Boundaries.
4. Laser Sail vs Magsail Hybrid Deceleration Thresholds.
5. Multi-dimensional Interstellar Mission Pareto Tradeoffs.
6. Master Ranked Feasibility Database Completeness.

Author: Kepler (Agent A001, Generation 0)
Domain: Practical space propulsion (propulsion)
"""

import unittest
import math
from propulsion_grand_unified_pareto_engine import (
    C,
    G0,
    LY,
    relativistic_gamma,
    relativistic_kinetic_energy,
    relativistic_rapidity,
    ideal_rocket_mass_ratio,
    payload_mass_multiplier,
    evaluate_bussard_ramjet_limits,
    get_propulsion_archetype_database,
    optimize_interstellar_mission,
    generate_master_ranked_table,
)


class TestGrandUnifiedParetoEngine(unittest.TestCase):

    def test_relativistic_kinematics(self):
        # Test gamma at beta = 0.10
        gamma_01 = relativistic_gamma(0.10)
        self.assertAlmostEqual(gamma_01, 1.005037815, places=7)

        # Test kinetic energy at beta = 0.10 for 1 kg
        ke_01 = relativistic_kinetic_energy(1.0, 0.10)
        self.assertAlmostEqual(ke_01, 4.52776e14, delta=1.0e10)

        # Test rapidity at beta = 0.10
        y_01 = relativistic_rapidity(0.10)
        self.assertAlmostEqual(y_01, 0.100335347, places=7)

    def test_rocket_rendezvous_squaring(self):
        # Fusion exhaust velocity ve = 0.045c
        ve = 0.045 * C
        beta = 0.10
        r_flyby = ideal_rocket_mass_ratio(beta, ve, mode="flyby")
        r_rendezvous = ideal_rocket_mass_ratio(beta, ve, mode="rendezvous")
        
        # Verify R_rendezvous == R_flyby^2
        self.assertAlmostEqual(r_rendezvous, r_flyby**2, delta=1.0e-3)
        self.assertAlmostEqual(r_flyby, 9.30, delta=0.05)
        self.assertAlmostEqual(r_rendezvous, 86.49, delta=0.5)

    def test_structural_mass_limit_one_stage_vs_two_stage(self):
        epsilon = 0.05
        # Single stage limit is R < 1 / epsilon = 20
        # For fusion flyby (R = 9.30 < 20):
        mult_flyby = payload_mass_multiplier(9.30, epsilon=epsilon, stages=1)
        self.assertAlmostEqual(mult_flyby, 16.51, delta=0.05)

        # For fusion rendezvous (R = 86.49 > 20):
        mult_rendezvous_1stage = payload_mass_multiplier(86.49, epsilon=epsilon, stages=1)
        self.assertEqual(mult_rendezvous_1stage, float('inf'))

        # For optimal 2-stage fusion rendezvous:
        mult_rendezvous_2stage = payload_mass_multiplier(86.49, epsilon=epsilon, stages=2)
        self.assertAlmostEqual(mult_rendezvous_2stage, 272.4, delta=1.0)

    def test_fishback_powell_ramjet_limits(self):
        # Test ramjet at beta = 0.05 (below cutoff) vs beta = 0.20 (above cutoff)
        res_005 = evaluate_bussard_ramjet_limits(0.05)
        res_020 = evaluate_bussard_ramjet_limits(0.20)

        # Theoretical fusion exhaust cutoff is ~0.119c
        self.assertAlmostEqual(res_005["ve_max_fraction_c"], 0.119, delta=0.005)
        
        # At beta = 0.05, drag-to-thrust ratio < 1.0 (positive thrust)
        self.assertLess(res_005["drag_to_thrust_ratio"], 1.0)
        self.assertTrue(res_005["is_thrust_positive"])

        # At beta = 0.20, drag-to-thrust ratio > 1.0 (net drag, thrust negative!)
        self.assertGreater(res_020["drag_to_thrust_ratio"], 1.0)
        self.assertFalse(res_020["is_thrust_positive"])
        self.assertLess(res_020["f_net_newtons"], 0.0)

        # Bremsstrahlung radiation loss vastly exceeds p-p fusion power density
        self.assertGreater(res_005["brem_to_fusion_ratio"], 1.0e6)

    def test_antimatter_rendezvous_capability(self):
        ve_am = 0.331 * C
        beta = 0.10
        r_am_flyby = ideal_rocket_mass_ratio(beta, ve_am, mode="flyby")
        r_am_rend = ideal_rocket_mass_ratio(beta, ve_am, mode="rendezvous")
        
        self.assertAlmostEqual(r_am_flyby, 1.354, delta=0.01)
        self.assertAlmostEqual(r_am_rend, 1.833, delta=0.01)

        mult_am_rend = payload_mass_multiplier(r_am_rend, epsilon=0.05, stages=1)
        self.assertAlmostEqual(mult_am_rend, 1.918, delta=0.01)

    def test_interstellar_mission_optimizer_proxima_flyby(self):
        # Mission: Proxima Centauri (4.246 ly) in 21.23 years (beta = 0.20), 1 gram wafercraft
        res = optimize_interstellar_mission(
            target_distance_ly=4.246,
            transit_time_years=21.23,
            payload_mass_kg=0.001,
            mode="flyby"
        )
        self.assertAlmostEqual(res["average_beta"], 0.20, delta=0.005)
        evals = {e["archetype_key"]: e for e in res["evaluations"]}

        # Laser sail must be feasible
        self.assertTrue(evals["laser_sail"]["feasible"])
        self.assertEqual(evals["laser_sail"]["mass_ratio"], 1.0)

        # Chemical and NTR must be unfeasible
        self.assertFalse(evals["chemical"]["feasible"])
        self.assertFalse(evals["ntr"]["feasible"])

        # Bussard ramjet must be unfeasible
        self.assertFalse(evals["bussard_ramjet"]["feasible"])

    def test_interstellar_mission_optimizer_proxima_rendezvous_heavy(self):
        # Mission: Proxima Centauri (4.246 ly) in 42.46 years (beta = 0.10), 1000 kg scientific craft
        res = optimize_interstellar_mission(
            target_distance_ly=4.246,
            transit_time_years=42.46,
            payload_mass_kg=1000.0,
            mode="rendezvous"
        )
        evals = {e["archetype_key"]: e for e in res["evaluations"]}

        # Fusion 2-stage is feasible
        self.assertTrue(evals["fusion"]["feasible"])
        self.assertAlmostEqual(evals["fusion"]["initial_wet_mass_kg"], 272400.0, delta=2000.0)

        # Antimatter is feasible
        self.assertTrue(evals["antimatter"]["feasible"])
        self.assertAlmostEqual(evals["antimatter"]["initial_wet_mass_kg"], 1918.0, delta=20.0)

        # Laser sail with hybrid magsail (1000 kg craft) is feasible
        self.assertTrue(evals["laser_sail"]["feasible"])

    def test_master_database_and_ranked_table(self):
        table = generate_master_ranked_table()
        self.assertEqual(len(table), 10)
        
        # Verify ranking order
        keys = [row["key"] for row in table]
        expected_keys = [
            "chemical", "sep", "solar_sail", "ntr", "nep", "orion",
            "fusion", "antimatter", "laser_sail", "bussard_ramjet"
        ]
        self.assertEqual(keys, expected_keys)

        # Ensure all rows have blockers and mission domains
        for row in table:
            self.assertTrue(len(row["blocker"]) > 10)
            self.assertTrue(len(row["domain"]) > 5)


if __name__ == "__main__":
    unittest.main()
