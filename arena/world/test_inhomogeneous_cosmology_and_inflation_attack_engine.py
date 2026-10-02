"""
test_inhomogeneous_cosmology_and_inflation_attack_engine.py
===========================================================
Comprehensive unit test suite for inhomogeneous_cosmology_and_inflation_attack_engine.py.
Verifies all mathematical models, relativistic equations, and statistical tests attacking
the Cosmological Principle (FLRW metric) and the Inflationary Paradigm.
"""

import unittest
import math
from inhomogeneous_cosmology_and_inflation_attack_engine import (
    PhysicalConstants,
    BuchertInhomogeneousAveragingEngine,
    BuchertDomainResult,
    CosmicDipoleAnisotropyEngine,
    CosmicDipoleResult,
    KBCLocalVoidHubbleEngine,
    LocalVoidHubbleResult,
    PenroseEntropyAndInitialConditionsEngine,
    PenroseEntropyResult,
    SwamplandAndTransPlanckianEngine,
    SwamplandAttackResult,
    EkpyroticQuantumBounceEngine,
    EkpyroticBounceResult,
    MasterAssumptionAttackCompendium,
    AssumptionAttackEntry
)


class TestPhysicalConstants(unittest.TestCase):
    """Verifies fundamental physical and astronomical constants."""

    def test_constants_consistency(self):
        c = PhysicalConstants()
        self.assertEqual(c.c, 299792458.0)
        self.assertAlmostEqual(c.k_B, 1.380649e-23, places=28)
        self.assertAlmostEqual(c.G, 6.67430e-11, places=15)
        # Check derived Planck units
        derived_ell_Pl = math.sqrt(c.hbar * c.G / (c.c ** 3))
        self.assertAlmostEqual(derived_ell_Pl / c.ell_Pl, 1.0, places=3)
        derived_t_Pl = math.sqrt(c.hbar * c.G / (c.c ** 5))
        self.assertAlmostEqual(derived_t_Pl / c.t_Pl, 1.0, places=3)


class TestBuchertInhomogeneousAveragingEngine(unittest.TestCase):
    """Verifies Buchert spatial averaging and kinematical backreaction Q_D."""

    def setUp(self):
        self.engine = BuchertInhomogeneousAveragingEngine()

    def test_two_phase_backreaction_baseline(self):
        res = self.engine.compute_two_phase_backreaction(
            f_v=0.82,
            H_v_kms_Mpc=82.0,
            H_w_kms_Mpc=15.0,
            shear_ratio=0.05
        )
        self.assertIsInstance(res, BuchertDomainResult)
        self.assertAlmostEqual(res.volume_fraction_voids + res.volume_fraction_walls, 1.0, places=6)
        
        # Kinematical backreaction Q_D must be strictly positive
        self.assertGreater(res.kinematical_backreaction_Q_D, 0.0)
        
        # Effective expansion rate H_D should be a weighted average
        expected_H_D = 0.82 * 82.0 + 0.18 * 15.0
        self.assertAlmostEqual(res.H_average_kms_Mpc, expected_H_D, places=3)
        
        # Check that backreaction produces acceleration (q_D < 0)
        self.assertLess(res.effective_deceleration_q_D, 0.0)
        self.assertTrue(res.is_accelerating)

    def test_zero_variance_gives_zero_backreaction(self):
        # When void and wall expansion rates are identical, Var(theta) = 0 -> Q_D = 0
        res = self.engine.compute_two_phase_backreaction(
            f_v=0.80,
            H_v_kms_Mpc=67.4,
            H_w_kms_Mpc=67.4,
            shear_ratio=0.0
        )
        self.assertAlmostEqual(res.kinematical_backreaction_Q_D, 0.0, places=20)
        # Without backreaction or Lambda, matter causes deceleration (q_D > 0)
        self.assertGreater(res.effective_deceleration_q_D, 0.0)
        self.assertFalse(res.is_accelerating)

    def test_scan_void_fraction(self):
        scan = self.engine.scan_void_fraction_for_acceleration(
            f_v_range=(0.6, 0.9),
            steps=10,
            delta_H_kms_Mpc=67.0
        )
        self.assertEqual(len(scan), 11)
        # Verify that for high void fractions, acceleration occurs
        high_fv_result = scan[-2]  # f_v ~ 0.84
        self.assertTrue(high_fv_result[2])  # is_accelerating should be True


class TestCosmicDipoleAnisotropyEngine(unittest.TestCase):
    """Verifies Ellis-Baldwin kinematic dipole calculations and CatWISE tension."""

    def setUp(self):
        self.engine = CosmicDipoleAnisotropyEngine()

    def test_catwise_quasar_dipole_rejection(self):
        res = self.engine.evaluate_quasar_dipole()
        self.assertIsInstance(res, CosmicDipoleResult)
        
        # Beta parameter v / c
        expected_beta = (369.82 * 1000.0) / 299792458.0
        self.assertAlmostEqual(res.beta_parameter, expected_beta, places=6)
        
        # Expected kinematic dipole ~ [2 + 1.05 * (1 + 0.75)] * beta
        enhancement = 2.0 + 1.05 * 1.75  # 2 + 1.8375 = 3.8375
        expected_D = enhancement * expected_beta
        self.assertAlmostEqual(res.expected_kinematic_dipole, expected_D, places=5)
        self.assertAlmostEqual(res.expected_kinematic_dipole, 0.00473, delta=0.003)
        
        # Discrepancy ratio: observed (0.01554) vs expected (~0.00712 or 0.00473 depending on exact count model)
        self.assertGreater(res.discrepancy_factor, 1.5)
        
        # Gaussian significance must be > 3 sigma
        self.assertGreater(res.gaussian_significance_sigma, 3.0)
        
        # Full vector significance from Secrest et al. 2022
        self.assertAlmostEqual(res.full_vector_significance_sigma, 4.91, places=2)
        
        # FLRW isotropy assumption must be flagged as rejected
        self.assertTrue(res.flrw_isotropy_rejected)


class TestKBCLocalVoidHubbleEngine(unittest.TestCase):
    """Verifies KBC void outflow dynamics and resolution of the Hubble tension."""

    def setUp(self):
        self.engine = KBCLocalVoidHubbleEngine()

    def test_void_outflow_resolves_hubble_tension(self):
        res = self.engine.evaluate_void_impact(
            void_radius_Mpc=300.0,
            delta_void=-0.25,
            nonlinear_boost_factor=1.88,
            H0_global=67.36,
            sigma_global=0.54,
            H0_local_obs=73.04,
            sigma_local_obs=1.04
        )
        self.assertIsInstance(res, LocalVoidHubbleResult)
        
        # Matter growth factor f ~ Omega_m^0.55
        expected_f = 0.3153 ** 0.55
        self.assertAlmostEqual(res.matter_growth_factor_f, expected_f, places=3)
        
        # Unadjusted tension should be ~ 4.85 sigma
        self.assertAlmostEqual(res.unadjusted_tension_sigma, 4.85, delta=0.15)
        
        # Predicted local H0 should match SH0ES (73.04) closely
        self.assertAlmostEqual(res.H0_local_predicted, 73.04, delta=0.5)
        
        # Adjusted residual tension should be negligible (< 0.5 sigma)
        self.assertLess(res.void_adjusted_residual_sigma, 0.5)
        
        # Tension is resolved by local inhomogeneity
        self.assertTrue(res.tension_resolved_by_inhomogeneity)


class TestPenroseEntropyAndInitialConditionsEngine(unittest.TestCase):
    """Verifies Penrose gravitational entropy and the initial conditions paradox."""

    def setUp(self):
        self.engine = PenroseEntropyAndInitialConditionsEngine()

    def test_entropy_inventory_and_fine_tuning(self):
        res = self.engine.calculate_entropy_inventory()
        self.assertIsInstance(res, PenroseEntropyResult)
        
        # Thermal entropy should be on order 10^88 to 10^90 k_B
        self.assertGreater(res.thermal_matter_entropy_k_B, 1e88)
        self.assertLess(res.thermal_matter_entropy_k_B, 1e92)
        
        # SMBH entropy should be on order 10^104 k_B
        self.assertAlmostEqual(math.log10(res.supermassive_black_hole_entropy_k_B), 104.0, delta=1.0)
        
        # Holographic de Sitter entropy should be on order 10^122 k_B
        self.assertAlmostEqual(math.log10(res.de_sitter_holographic_entropy_k_B), 122.0, delta=2.0)
        
        # Maximal gravitational entropy should be on order 10^123 k_B
        self.assertAlmostEqual(res.penrose_entropy_exponent, 123.0, delta=2.0)
        
        # Initial inflaton patch entropy bound is tiny (<= 10^15 k_B)
        self.assertLessEqual(res.inflaton_patch_entropy_bound_k_B, 1e16)
        
        # Verifies that inflation exacerbates the tuning paradox
        self.assertTrue(res.inflation_exacerbates_tuning)


class TestSwamplandAndTransPlanckianEngine(unittest.TestCase):
    """Verifies quantum gravity Swampland and TCC constraints on inflation."""

    def setUp(self):
        self.engine = SwamplandAndTransPlanckianEngine()

    def test_starobinsky_model_in_swampland(self):
        res = self.engine.evaluate_inflation_model(
            model_name="Starobinsky R^2",
            r=0.0033,
            N_efolds=60.0
        )
        self.assertIsInstance(res, SwamplandAttackResult)
        
        # Lyth excursion Delta phi ~ sqrt(r/8) * 60 ~ 1.2 M_Pl
        self.assertGreater(res.inflaton_excursion_Delta_phi_Mpl, 1.0)
        
        # de Sitter parameter c = sqrt(r/8) ~ 0.020 << 1 -> in Swampland
        self.assertLess(res.swampland_de_sitter_parameter_c, 0.05)
        self.assertTrue(res.is_in_swampland)
        
        # TCC maximum allowable r is <= 10^-30
        self.assertLess(res.tcc_max_tensor_ratio_r, 1e-25)
        
        # Since r = 0.0033 >> 1e-30, it violates TCC
        self.assertTrue(res.violates_tcc)
        
        # A LiteBIRD detection of r ~ 10^-3 would falsify TCC
        self.assertTrue(res.litebird_detection_would_falsify_tcc)


class TestEkpyroticQuantumBounceEngine(unittest.TestCase):
    """Verifies non-singular ekpyrotic bounce dynamics and perturbation spectra."""

    def setUp(self):
        self.engine = EkpyroticQuantumBounceEngine()

    def test_ekpyrotic_bounce_scaling_and_spectra(self):
        res = self.engine.evaluate_bounce(equation_of_state_w=3.1)
        self.assertIsInstance(res, EkpyroticBounceResult)
        
        # Shear scales as a^-6
        self.assertEqual(res.shear_density_scaling_exponent, -6.0)
        
        # Ekpyrotic energy scales as a^(-3(1+w)) = a^-12.3
        self.assertAlmostEqual(res.ekpyrotic_density_scaling_exponent, -12.3, places=2)
        
        # Relative shear scales as a^(3(w-1)) = a^+6.3
        self.assertAlmostEqual(res.relative_shear_scaling_exponent, 6.3, places=2)
        
        # BKL chaos is suppressed because relative shear decays to zero as a -> 0
        self.assertTrue(res.bkl_chaotic_oscillations_suppressed)
        
        # Critical bounce density is on order 10^96 kg/m^3
        self.assertGreater(res.critical_bounce_density_kg_m3, 1e95)
        
        # Scalar tilt is red (n_s ~ 0.96)
        self.assertGreater(res.scalar_spectral_index_n_s, 0.94)
        self.assertLess(res.scalar_spectral_index_n_s, 0.98)
        
        # Tensor tilt is strictly BLUE (n_T > 0), decisively distinguishing it from inflation
        self.assertGreater(res.tensor_spectral_index_n_T, 0.0)
        self.assertTrue(res.tensor_tilt_is_blue)
        
        # Avoids trans-Planckian and eternal multiverse problems
        self.assertTrue(res.avoids_trans_planckian_problem)
        self.assertTrue(res.avoids_eternal_multiverse_catastrophe)


class TestMasterAssumptionAttackCompendium(unittest.TestCase):
    """Verifies the synthesis compendium of attacked foundational assumptions."""

    def test_compendium_entries(self):
        compendium = MasterAssumptionAttackCompendium.get_attack_compendium()
        self.assertEqual(len(compendium), 6)
        
        ids = [entry.assumption_id for entry in compendium]
        self.assertIn("ATTACK-01", ids)
        self.assertIn("ATTACK-02", ids)
        self.assertIn("ATTACK-03", ids)
        self.assertIn("ATTACK-04", ids)
        self.assertIn("ATTACK-05", ids)
        self.assertIn("ATTACK-06", ids)
        
        for entry in compendium:
            self.assertTrue(len(entry.assumption_name) > 0)
            self.assertTrue(len(entry.fatal_vulnerability) > 0)
            self.assertTrue(len(entry.quantitative_metric) > 0)
            self.assertTrue(len(entry.decisive_resolving_test) > 0)
            self.assertTrue(len(entry.verdict) > 0)


if __name__ == "__main__":
    unittest.main()
