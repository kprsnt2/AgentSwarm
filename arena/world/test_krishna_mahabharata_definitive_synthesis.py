"""
test_krishna_mahabharata_definitive_synthesis.py

Comprehensive Unit Test Suite for krishna_mahabharata_definitive_synthesis_engine.py:
- Sarasvati Paleo-Hydrology & Vinashana Marker
- Chariot Kinematics, Inertia, and Technology Comparison
- Radiocarbon Stratigraphic Bayesian Posterior Estimation
- Aryabhata Kaliyuga Zero-Point Astronomical Inversion
- Philological Stratigraphy & Metric Chronometry
- Multi-Criterion Epistemic Adjudication & Tripartite Demarcation

Author: Kepler (A001) - Generation 0
"""

import unittest
from krishna_mahabharata_definitive_synthesis_engine import (
    SarasvatiPaleoHydrologyEngine,
    ChariotKinematicsEngine,
    RadiocarbonStratigraphicBayesianEngine,
    AryabhataKaliyugaEpochEngine,
    PhilologicalStratigraphyEngine,
    KrishnaMahabharataEpistemicAdjudicator
)


class TestKrishnaMahabharataDefinitiveSynthesis(unittest.TestCase):

    def setUp(self):
        self.hydrology = SarasvatiPaleoHydrologyEngine()
        self.kinematics = ChariotKinematicsEngine()
        self.radiocarbon = RadiocarbonStratigraphicBayesianEngine()
        self.aryabhata = AryabhataKaliyugaEpochEngine()
        self.philology = PhilologicalStratigraphyEngine()
        self.adjudicator = KrishnaMahabharataEpistemicAdjudicator()

    def test_sarasvati_hydrology_congruence(self):
        """Test that 950 BCE perfectly matches Vinashana inland termination while 3102 BCE fails."""
        res_950 = self.hydrology.evaluate_epoch_congruence(950)
        self.assertEqual(res_950["vinashana_congruence"], 1.0)
        self.assertIn("Vinashana", res_950["terminal_location"])
        self.assertFalse(res_950["reaches_sea"])

        res_3102 = self.hydrology.evaluate_epoch_congruence(3102)
        self.assertEqual(res_3102["vinashana_congruence"], 0.05)
        self.assertTrue(res_3102["reaches_sea"])

    def test_chariot_rotational_inertia(self):
        """Test that solid wheel has significantly greater rotational inertia than spoked wheel."""
        i_solid = self.kinematics.calculate_wheel_inertia(self.kinematics.sinauli_cart)
        i_spoked = self.kinematics.calculate_wheel_inertia(self.kinematics.epic_spoked_ratha)

        self.assertAlmostEqual(i_solid, 10.625, places=2)
        self.assertAlmostEqual(i_spoked, 2.308, places=2)
        ratio = i_solid / i_spoked
        self.assertGreater(ratio, 4.0)

    def test_chariot_kinematics_simulation(self):
        """Test dynamic acceleration and tactical mobility of spoked chariot vs solid cart."""
        cart_res = self.kinematics.simulate_kinematics(self.kinematics.sinauli_cart)
        ratha_res = self.kinematics.simulate_kinematics(self.kinematics.epic_spoked_ratha)

        self.assertGreater(ratha_res["linear_acceleration_ms2"], cart_res["linear_acceleration_ms2"])
        self.assertGreater(ratha_res["tactical_top_speed_kmh"], cart_res["tactical_top_speed_kmh"])
        self.assertIn("Early Iron Age", ratha_res["metallurgy_and_age"])
        self.assertIn("High", ratha_res["maneuverability_rating"])

    def test_radiocarbon_stratigraphic_posterior(self):
        """Test Bayesian C-14 posterior distribution across PGW sites."""
        post = self.radiocarbon.compute_joint_posterior()

        # Peak mode should be squarely within early iron age (1100 to 800 BCE)
        self.assertGreaterEqual(post["mode_bce"], 800)
        self.assertLessEqual(post["mode_bce"], 1150)

        # 950 BCE must have high density, while 3102 BCE has zero density
        self.assertGreater(post["density_at_950_bce"], 0.0005)
        self.assertEqual(post["density_at_3102_bce"], 0.0)

    def test_aryabhata_zero_point_construction(self):
        """Test Aryabhata's mathematical epoch backward calculation."""
        # Check planetary revolutions dictionary
        self.assertEqual(self.aryabhata.revolutions["Sun"], 4320000.0)
        self.assertEqual(self.aryabhata.solar_years_per_mahayuga, 4320000.0)

        # Check JPL ephemeris dispersion on Feb 18, 3102 BCE
        jpl = self.aryabhata.get_jpl_ephemeris_feb_18_3102_bce()
        self.assertGreater(jpl["angular_dispersion_deg"], 60.0)
        self.assertFalse(jpl["was_visible_to_naked_eye"])
        self.assertFalse(jpl["is_true_single_point_conjunction"])

    def test_philological_stratigraphy_expansion(self):
        """Test textual accretion metrics from Jaya to Shatasahasri Samhita."""
        acc = self.philology.compute_accretion_metrics()
        self.assertEqual(acc["base_core_verses (Jaya)"], 8800)
        self.assertEqual(acc["final_mahabharata_verses"], 100000)
        self.assertAlmostEqual(acc["expansion_factor_core_to_epic"], 11.36, places=2)

    def test_master_epistemic_adjudication(self):
        """Verify the complete tripartite adjudication matrix."""
        res = self.adjudicator.adjudicate_all_domains()
        adj_matrix = res["adjudication_matrix"]

        # Sub-question 1
        q1 = adj_matrix["sub_question_1_mahabharata_war"]
        self.assertIn("Historically Authenticated", q1["verdict"])
        self.assertGreaterEqual(q1["epistemic_confidence"], 0.8)
        self.assertIn("PGW", " ".join(q1["primary_evidence"]))

        # Sub-question 2
        q2 = adj_matrix["sub_question_2_historicity_of_krishna"]
        self.assertIn("Historically Anchored", q2["verdict"])
        self.assertGreaterEqual(q2["epistemic_confidence"], 0.8)
        self.assertIn("Chandogya", " ".join(q2["primary_evidence"]))

        # Sub-question 3
        q3 = adj_matrix["sub_question_3_supreme_divinity"]
        self.assertIn("Ontological", q3["verdict"])
        self.assertIn("Sabda", q3["epistemic_demarcation"]["epistemic_status"])


if __name__ == "__main__":
    unittest.main()
