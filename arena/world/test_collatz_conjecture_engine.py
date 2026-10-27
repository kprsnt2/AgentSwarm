"""
Unit test suite for collatz_conjecture_engine.py
Verifies deterministic Collatz maps, Tao logarithmic drift, 2-adic dynamics,
Baker linear forms bounds, Steiner 1-cycles, and residue-class sieving.
"""

import math
import fractions
import unittest
import numpy as np

from collatz_conjecture_engine import (
    CollatzMap,
    TaoDriftEngine,
    PAdicDynamicsEngine,
    BakerBoundsEngine,
    ResidueSieveEngine,
    CollatzResearchMaster,
)


class TestCollatzMap(unittest.TestCase):
    """Verifies core Collatz, compressed, and Syracuse arithmetic mappings."""

    def test_step_standard(self):
        self.assertEqual(CollatzMap.step_standard(6), 3)
        self.assertEqual(CollatzMap.step_standard(7), 22)
        self.assertEqual(CollatzMap.step_standard(1), 4)

    def test_step_compressed(self):
        self.assertEqual(CollatzMap.step_compressed(6), 3)
        self.assertEqual(CollatzMap.step_compressed(7), 11)
        self.assertEqual(CollatzMap.step_compressed(1), 2)
        self.assertEqual(CollatzMap.step_compressed(2), 1)

    def test_step_syracuse(self):
        next_odd, v2 = CollatzMap.step_syracuse(7)
        # 3*7 + 1 = 22 = 2 * 11 -> next_odd = 11, v2 = 1
        self.assertEqual(next_odd, 11)
        self.assertEqual(v2, 1)

        next_odd, v2 = CollatzMap.step_syracuse(5)
        # 3*5 + 1 = 16 = 2^4 * 1 -> next_odd = 1, v2 = 4
        self.assertEqual(next_odd, 1)
        self.assertEqual(v2, 4)

        with self.assertRaises(ValueError):
            CollatzMap.step_syracuse(4)  # even input invalid

    def test_trajectory_and_stopping_times(self):
        # Orbit of 27 in standard map reaches peak 9232
        traj = CollatzMap.trajectory(27, max_steps=200, map_type="standard")
        self.assertEqual(traj[0], 27)
        self.assertEqual(traj[-1], 1)
        self.assertEqual(max(traj), 9232)

        # Stopping time for 3: T(3)=5, T(5)=8, T(8)=4, T(4)=2 < 3 (4 steps in compressed)
        sigma = CollatzMap.stopping_time(3)
        self.assertIsNotNone(sigma)
        self.assertEqual(sigma, 4)

        # Total stopping time for 1 is 0
        self.assertEqual(CollatzMap.total_stopping_time(1), 0)

        # Orbit profile
        profile = CollatzMap.orbit_profile(7)
        self.assertTrue(profile["reached_one"])
        self.assertEqual(profile["initial"], 7)
        self.assertGreater(profile["peak"], 7)


class TestTaoDriftEngine(unittest.TestCase):
    """Verifies theoretical and empirical drift models and Tao's bounded values."""

    def test_syracuse_drift_theoretical(self):
        drifts = TaoDriftEngine.syracuse_drift_theoretical()
        # Syracuse natural log drift: ln(3) - 2 ln(2) = ln(3/4) approx -0.287682
        self.assertAlmostEqual(drifts["syracuse_natural_log_drift"], math.log(0.75), places=5)
        # Syracuse base-2 drift: log2(3) - 2 approx -0.415037
        self.assertAlmostEqual(drifts["syracuse_base2_log_drift"], math.log2(3.0) - 2.0, places=5)
        # Prompt Ground Truth: (1/2)*ln(3) - (3/2)*ln(2) approx -0.490415
        self.assertAlmostEqual(drifts["prompt_ground_truth_formula"], 0.5 * math.log(3.0) - 1.5 * math.log(2.0), places=5)
        # Half-step normalized prompt drift approx -0.2452 to -0.247
        self.assertAlmostEqual(drifts["prompt_half_normalized_drift"], -0.245207, places=4)
        # Compressed map natural drift: (1/2)*ln(3) - ln(2) approx -0.143841
        self.assertAlmostEqual(drifts["compressed_natural_log_drift"], 0.5 * math.log(3.0) - math.log(2.0), places=5)

    def test_empirical_syracuse_drift(self):
        res = TaoDriftEngine.empirical_syracuse_drift(sample_size=3000, bit_length=48, rng_seed=42)
        # Mean v2 should be close to 2.0 within statistical tolerance
        self.assertAlmostEqual(res["mean_v2_empirical"], 2.0, delta=0.15)
        # Variance of v2 should be close to 2.0 within statistical tolerance
        self.assertAlmostEqual(res["var_v2_empirical"], 2.0, delta=0.25)
        # Mean log drift should be negative
        self.assertLess(res["mean_log_drift_empirical"], 0.0)

    def test_tao_almost_bounded_verification(self):
        # Test Tao's theorem for small bins
        res = TaoDriftEngine.tao_almost_bounded_verification(
            samples_per_bin=200, bin_exponents=[10, 14], rng_seed=42
        )
        self.assertIn("bin_results", res)
        self.assertTrue(res["conforms_to_tao_bound"])
        self.assertGreaterEqual(res["overall_empirical_logarithmic_density"], 0.99)

    def test_renewal_skew_walk_simulation(self):
        res = TaoDriftEngine.renewal_skew_walk_simulation(n_steps=50, n_walkers=500, rng_seed=42)
        # Drift slope is log2(3) - 2 approx -0.415037
        self.assertAlmostEqual(res["drift_slope"], math.log2(3.0) - 2.0, places=5)
        # Final mean should match theoretical expected drift within tolerance
        self.assertAlmostEqual(res["empirical_mean_final"], res["expected_final_drift"], delta=3.0)


class TestPAdicDynamicsEngine(unittest.TestCase):
    """Verifies 2-adic metric, Bernstein-Lagarias conjugacy, and cycle obstructions."""

    def test_valuation_and_distance(self):
        self.assertEqual(PAdicDynamicsEngine.valuation_2(12), 2)  # 12 = 4 * 3
        self.assertEqual(PAdicDynamicsEngine.valuation_2( fractions.Fraction(3, 8) ), -3)
        self.assertEqual(PAdicDynamicsEngine.valuation_2( fractions.Fraction(10, 3) ), 1)

        # Ultrametric inequality: d(x, z) <= max(d(x, y), d(y, z))
        x, y, z = 4, 12, 28
        d_xz = PAdicDynamicsEngine.padic_distance(x, z)
        d_xy = PAdicDynamicsEngine.padic_distance(x, y)
        d_yz = PAdicDynamicsEngine.padic_distance(y, z)
        self.assertLessEqual(d_xz, max(d_xy, d_yz) + 1e-12)

    def test_padic_expansion(self):
        # 1/5 in Z_2: 5 * x = 1.
        # Since 5 = 1 + 4, 1/5 = 1 - 4 + 16 - 64 + ...
        # Binary expansion: 1, 0, 1, 1, 0, 0, 1, 1...
        digits = PAdicDynamicsEngine.padic_expansion(fractions.Fraction(1, 5), num_digits=8)
        self.assertEqual(len(digits), 8)
        self.assertEqual(digits[0], 1)

    def test_periodic_points_and_conjugacy(self):
        # Trivial positive cycle 1 -> 2 -> 1 has parity vector [1, 0]
        x_star, K, k = PAdicDynamicsEngine.periodic_point_from_parity_vector([1, 0])
        self.assertEqual(x_star, fractions.Fraction(1, 1))
        self.assertEqual((K, k), (2, 1))

        # Negative cycle -1: v = [1]
        x_neg1, K, k = PAdicDynamicsEngine.periodic_point_from_parity_vector([1])
        self.assertEqual(x_neg1, fractions.Fraction(-1, 1))

        # Negative cycle -5: v = [1, 1, 0]
        x_neg5, K, k = PAdicDynamicsEngine.periodic_point_from_parity_vector([1, 1, 0])
        self.assertEqual(x_neg5, fractions.Fraction(-5, 1))

        # Non-integral rational periodic orbit in Z_2: v = [1, 0, 1, 1, 0] -> 29/5
        x_rat, K, k = PAdicDynamicsEngine.periodic_point_from_parity_vector([1, 0, 1, 1, 0])
        self.assertEqual(x_rat, fractions.Fraction(29, 5))

        # Verify orbit dynamics of 29/5
        orbit_verif = PAdicDynamicsEngine.verify_padic_orbit(x_rat, [1, 0, 1, 1, 0])
        self.assertTrue(orbit_verif["is_periodic"])
        self.assertTrue(orbit_verif["parity_match"])
        self.assertFalse(orbit_verif["is_integer"])  # rational, not integer!

    def test_classify_negative_cycles(self):
        classified = PAdicDynamicsEngine.classify_negative_cycles()
        self.assertEqual(len(classified), 3)
        seeds = [c["cycle_seed"] for c in classified]
        self.assertEqual(seeds, [-1, -5, -17])
        for c in classified:
            self.assertTrue(c["exact_match"])
            # All negative cycles have denominator 2^K - 3^k < 0
            self.assertLess(c["denominator_2K_minus_3k"], 0)

    def test_structural_obstructions(self):
        obs = PAdicDynamicsEngine.structural_obstruction_analysis()
        self.assertIn("obstruction_1_positivity", obs)
        self.assertIn("obstruction_2_integrality", obs)
        self.assertIn("obstruction_3_realizability", obs)
        self.assertIn("obstruction_4_baker_barina_squeeze", obs)


class TestBakerBoundsEngine(unittest.TestCase):
    """Verifies continued fraction convergents of log_2(3), Steiner 1-cycles, and Baker bounds."""

    def test_continued_fraction_coefficients(self):
        cf = BakerBoundsEngine.compute_continued_fraction(num_terms=15)
        # Ground truth initial terms of log_2(3): [1, 1, 1, 2, 2, 3, 1, 5, 2, 23, ...]
        expected_prefix = [1, 1, 1, 2, 2, 3, 1, 5, 2, 23]
        self.assertEqual(cf[:len(expected_prefix)], expected_prefix)

    def test_convergents(self):
        convs = BakerBoundsEngine.convergents(num_terms=10)
        # First convergents K/k:
        # idx 0: 1/1
        # idx 1: 2/1
        # idx 2: 3/2
        # idx 3: 8/5
        # idx 4: 19/12
        # idx 5: 65/41
        # idx 6: 84/53
        # idx 7: 485/306
        # idx 8: 1054/665
        # idx 9: 24727/15601
        expected_pairs = [(1, 1), (2, 1), (3, 2), (8, 5), (19, 12), (65, 41), (84, 53), (485, 306), (1054, 665), (24727, 15601)]
        computed_pairs = [(c["K"], c["k"]) for c in convs[:10]]
        self.assertEqual(computed_pairs, expected_pairs)

        # Verify Legendre property: |Lambda_n| is small
        for c in convs[3:]:
            self.assertLess(c["abs_Lambda"], 0.1)

    def test_baker_lower_bound_laurent(self):
        # Laurent bound should yield valid log bounds and positive Decimals
        res_small = BakerBoundsEngine.baker_lower_bound_laurent(8, 5)
        res_large = BakerBoundsEngine.baker_lower_bound_laurent(1054, 665)
        self.assertIn("log_lower_bound", res_small)
        self.assertIn("bound_decimal", res_small)
        self.assertGreater(res_small["bound_decimal"], 0)
        self.assertGreater(res_large["bound_decimal"], 0)
        # Larger K, k gives more negative log_lower_bound
        self.assertGreater(res_small["log_lower_bound"], res_large["log_lower_bound"])

    def test_certify_steiner_1_cycles(self):
        cert = BakerBoundsEngine.certify_steiner_1_cycles(max_k=1000)
        self.assertTrue(cert["only_trivial_cycle_exists"])
        self.assertEqual(len(cert["solutions_found"]), 1)
        sol = cert["solutions_found"][0]
        self.assertEqual(sol["k"], 1)
        self.assertEqual(sol["K"], 2)
        self.assertEqual(sol["x0"], 1)

    def test_simons_de_weger_summary(self):
        summary = BakerBoundsEngine.simons_de_weger_bounds_summary()
        self.assertIn("barina_roosendaal_bound", summary)
        self.assertGreater(summary["barina_roosendaal_bound"], 1e20)
        self.assertGreater(summary["minimum_cycle_length_K"], 3e11)


class TestResidueSieveEngine(unittest.TestCase):
    """Verifies high-throughput residue sieving and cycle impossibility."""

    def test_sieve_residues(self):
        res = ResidueSieveEngine.sieve_residues(modulus_exp=10)
        self.assertEqual(res["total_residues"], 1024)
        self.assertEqual(res["total_odds"], 512)
        self.assertLess(res["surviving_odds"], 512)
        # Terras decay rate alpha should be strictly less than 1.0
        self.assertLess(res["effective_decay_base_alpha"], 1.0)
        self.assertTrue(res["terras_exponential_bound_valid"])

    def test_certify_cycle_impossibility(self):
        # Exhaustively check K <= 10
        cert = ResidueSieveEngine.certify_cycle_impossibility(max_K=10)
        self.assertTrue(cert["certified_no_nontrivial_positive_cycles"])
        # Only trivial cycle minimum 1 should be found among positive cycles
        self.assertIn(1, cert["positive_cycle_minima"])
        self.assertEqual(len(cert["positive_cycle_minima"]), 1)
        self.assertGreater(cert["negative_cycle_count"], 0)


class TestCollatzResearchMaster(unittest.TestCase):
    """Verifies full research coordination and end-to-end synthesis."""

    def test_run_full_synthesis(self):
        master = CollatzResearchMaster()
        synth = master.run_full_synthesis()
        self.assertEqual(synth["agent_id"], "A002")
        self.assertIn("tao_drift_analysis", synth)
        self.assertIn("padic_dynamics", synth)
        self.assertIn("baker_and_cycle_bounds", synth)
        self.assertIn("residue_sieving", synth)
        self.assertIn("epistemic_conclusion", synth)
        self.assertTrue(synth["baker_and_cycle_bounds"]["steiner_1_cycle_certification"]["only_trivial_cycle_exists"])


if __name__ == "__main__":
    unittest.main()
