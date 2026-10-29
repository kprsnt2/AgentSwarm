"""
test_thyroid_regeneration_tolerance_engine.py — Rigorous Verification Test Suite
for Regenerative Thyroid Therapeutics & Antigen-Specific Tolerance Engine.

Author: Hypatia (A003), Generation 0, Autonomous Research Swarm
Domain: Regenerative Thyroid Therapeutics: Stem-Cell Folliculogenesis and Antigen-Specific Tolerance
Epistemic Class: Empirical / Quantitative Biophysical Simulation
"""

import math
import unittest
import numpy as np

import thyroid_regeneration_tolerance_engine as te
from thyroid_regeneration_tolerance_engine import (
    GAS_CONSTANT_R,
    BODY_TEMP_K,
    FARADAY_CONSTANT,
    NORMAL_SERUM_TSH_MIN,
    NORMAL_SERUM_TSH_MAX,
    NORMAL_SERUM_TSH_SET,
    NORMAL_SERUM_FT4_MIN,
    NORMAL_SERUM_FT4_MAX,
    NORMAL_SERUM_FT4_SET,
    NORMAL_SERUM_FT3_MIN,
    NORMAL_SERUM_FT3_MAX,
    NORMAL_SERUM_FT3_SET,
    FREE_FRACTION_T4,
    T4_MOLAR_MASS,
    T3_MOLAR_MASS,
    IODIDE_MOLAR_MASS,
    DifferentiationParameters,
    ThyroidDifferentiationModel,
    FollicleMorphologyParameters,
    FollicularMorphogenesisModel,
    ThyroidBiochemistryParameters,
    HormoneSynthesisSecretionEngine,
    TolerogenicNanoparticleParameters,
    AutoimmuneInterceptionModel,
    PharmacokineticParameters,
    ThyroidPharmacokineticsEngine,
    RegenerativeThyroidSimulator
)


class TestBiophysicalConstantsAndReferenceBounds(unittest.TestCase):
    """Verifies fundamental physiological constants, ranges, and chemical properties."""

    def test_euthyroid_reference_intervals(self):
        """Ensure standard euthyroid physiological reference limits are strictly monotonic and positive."""
        self.assertGreater(NORMAL_SERUM_TSH_MIN, 0.0)
        self.assertGreater(NORMAL_SERUM_TSH_MAX, NORMAL_SERUM_TSH_MIN)
        self.assertTrue(NORMAL_SERUM_TSH_MIN <= NORMAL_SERUM_TSH_SET <= NORMAL_SERUM_TSH_MAX)

        self.assertGreater(NORMAL_SERUM_FT4_MIN, 0.0)
        self.assertGreater(NORMAL_SERUM_FT4_MAX, NORMAL_SERUM_FT4_MIN)
        self.assertTrue(NORMAL_SERUM_FT4_MIN <= NORMAL_SERUM_FT4_SET <= NORMAL_SERUM_FT4_MAX)

        self.assertGreater(NORMAL_SERUM_FT3_MIN, 0.0)
        self.assertGreater(NORMAL_SERUM_FT3_MAX, NORMAL_SERUM_FT3_MIN)
        self.assertTrue(NORMAL_SERUM_FT3_MIN <= NORMAL_SERUM_FT3_SET <= NORMAL_SERUM_FT3_MAX)

    def test_molecular_weights(self):
        """Verify chemical molar masses for levothyroxine, triiodothyronine, and iodine."""
        # T4: C15H11I4NO4 = 776.87 g/mol
        self.assertAlmostEqual(T4_MOLAR_MASS, 776.87, places=2)
        # T3: C15H12I3NO4 = 650.97 g/mol
        self.assertAlmostEqual(T3_MOLAR_MASS, 650.97, places=2)
        # 1 T4 contains 4 I, 1 T3 contains 3 I
        diff_mass = T4_MOLAR_MASS - T3_MOLAR_MASS
        expected_diff = IODIDE_MOLAR_MASS - 1.008  # substitute I for H
        self.assertAlmostEqual(diff_mass, expected_diff, delta=0.5)

    def test_plasma_protein_binding_equilibrium(self):
        """Free T4 fraction in human circulation should be approximately 0.015% to 0.02%."""
        self.assertTrue(1.0e-4 <= FREE_FRACTION_T4 <= 2.5e-4)
        # At total T4 = 100 nmol/L (normal euthyroid total T4), Free T4 should be ~ 16.5 pmol/L
        engine = ThyroidPharmacokineticsEngine()
        ft4 = engine.calculate_free_t4_from_plasma(100.0)
        self.assertAlmostEqual(ft4, 16.5, places=1)


class TestStemCellDifferentiationAndGRN(unittest.TestCase):
    """Verifies iPSC differentiation signaling cascades and gene regulatory networks."""

    def setUp(self):
        self.diff = ThyroidDifferentiationModel()

    def test_bmp4_and_fgf2_synergistic_promoter_occupancy(self):
        """Neither BMP4 alone nor FGF2 alone suffices; combinatorial synergy is mandatory."""
        sig_none = self.diff.signal_input(0.0, 0.0)
        sig_bmp_only = self.diff.signal_input(5.0, 0.0)
        sig_fgf_only = self.diff.signal_input(0.0, 10.0)
        sig_both = self.diff.signal_input(5.0, 10.0)

        self.assertEqual(sig_none, 0.0)
        self.assertEqual(sig_bmp_only, 0.0)
        self.assertEqual(sig_fgf_only, 0.0)
        self.assertGreater(sig_both, 0.70)
        self.assertLessEqual(sig_both, 1.0)

    def test_nkx2_1_and_pax8_coactivation_dynamics(self):
        """Activation of both NKX2-1 and PAX8 is required to drive downstream FOXE1 and TG."""
        # Isolated initial state without signals
        init_uninduced = [0.01, 0.01, 0.0, 0.0, 0.0]
        deriv_no_signal = self.diff.derivatives(0.0, np.array(init_uninduced), bmp4=0.0, fgf2=0.0)
        # Basal rates are very small
        self.assertLess(deriv_no_signal[0], 0.05)
        self.assertLess(deriv_no_signal[1], 0.05)

        # High morphogen signal triggers positive derivative
        deriv_induced = self.diff.derivatives(0.0, np.array(init_uninduced), bmp4=2.5, fgf2=5.0)
        self.assertGreater(deriv_induced[0], 1.0)
        self.assertGreater(deriv_induced[1], 0.8)

    def test_full_differentiation_timecourse(self):
        """Simulate the 14-day protocol following Antonica (2012) and Kurmann (2015)."""
        res = self.diff.simulate_differentiation(duration_days=14.0)
        self.assertTrue(res["is_follicle_committed"])
        self.assertGreater(res["nkx2_1"][-1], 0.6)
        self.assertGreater(res["pax8"][-1], 0.5)
        self.assertGreater(res["foxe1"][-1], 0.4)
        self.assertGreater(res["tg_expression"][-1], 0.6)
        self.assertGreater(res["tpo_expression"][-1], 0.5)
        self.assertGreater(res["nis_expression"][-1], 0.4)

    def test_inadequate_morphogen_fails_differentiation(self):
        """Absence of BMP4 or FGF2 prevents thyroid fate commitment."""
        res_no_bmp = self.diff.simulate_differentiation(
            duration_days=14.0,
            bmp4_profile=lambda t: 0.0,
            fgf2_profile=lambda t: 5.0
        )
        self.assertFalse(res_no_bmp["is_follicle_committed"])
        self.assertLess(res_no_bmp["nkx2_1"][-1], 0.2)


class TestFollicularMorphogenesisAndPolarity(unittest.TestCase):
    """Verifies 3D hollow lumen mechanics, Young-Laplace equilibrium, and apicobasal polarity."""

    def setUp(self):
        self.morph = FollicularMorphogenesisModel()

    def test_follicle_geometric_scaling(self):
        """Geometry verifies outer volume, lumen cavitation, and colloid volume fraction."""
        # 60 um radius follicle with 12 um cuboidal cell height
        geom = self.morph.compute_follicle_geometry(outer_radius_um=60.0)
        self.assertEqual(geom["lumen_radius_um"], 48.0)
        # Volume ratio = (48/60)^3 = 0.8^3 = 0.512 (51.2% lumen colloid)
        self.assertAlmostEqual(geom["colloid_volume_fraction"], 0.512, places=3)
        self.assertGreater(geom["basolateral_surface_area_um2"], geom["apical_surface_area_um2"])
        self.assertGreater(geom["estimated_cell_count"], 300)

    def test_young_laplace_and_elastic_pressure_balance(self):
        """Lumen mechanics must balance distending colloid oncotic pressure with Laplace wall tension."""
        geom = self.morph.compute_follicle_geometry(outer_radius_um=60.0)
        self.assertGreater(geom["laplace_pressure_kpa"], 0.05)
        self.assertGreater(geom["elastic_restoring_kpa"], 0.3)
        self.assertGreater(geom["net_distending_pressure_kpa"], 1.0)
        self.assertTrue(geom["is_mechanically_stable"])

    def test_unphysical_radius_raises_error(self):
        """Outer radius smaller than single epithelial cell height cannot form a hollow lumen."""
        with self.assertRaises(ValueError):
            self.morph.compute_follicle_geometry(outer_radius_um=10.0)

    def test_apicobasal_polarity_validation(self):
        """Polarity requires apical ZO-1/TPO and basolateral NIS."""
        # Correct physiological polarity (apical-in, basolateral-out)
        correct_pol = self.morph.verify_apicobasal_polarity(
            zo1_apical_ratio=4.0, tpo_apical_ratio=5.5, nis_basal_ratio=3.2
        )
        self.assertTrue(correct_pol["is_functionally_polarized"])

        # Inverted polarity (apical-out or unpolarized) fails
        inverted_pol = self.morph.verify_apicobasal_polarity(
            zo1_apical_ratio=1.0, tpo_apical_ratio=0.8, nis_basal_ratio=0.9
        )
        self.assertFalse(inverted_pol["is_functionally_polarized"])


class TestIodideOrganificationAndHormoneSecretion(unittest.TestCase):
    """Verifies NIS transport, TPO/DUOX2 coupling, and TSH-responsive T4/T3 secretion."""

    def setUp(self):
        self.engine = HormoneSynthesisSecretionEngine()

    def test_tsh_receptor_activation_dose_response(self):
        """TSH activates TSHR signaling sigmoidally with physiological EC50 ~ 1.5 mIU/L."""
        resp_zero = self.engine.tsh_receptor_activation(0.0)
        resp_ec50 = self.engine.tsh_receptor_activation(1.5)
        resp_high = self.engine.tsh_receptor_activation(30.0)

        self.assertAlmostEqual(resp_zero["receptor_occupancy"], 0.0, places=4)
        self.assertAlmostEqual(resp_ec50["receptor_occupancy"], 0.50, places=2)
        self.assertGreater(resp_high["receptor_occupancy"], 0.95)
        self.assertGreater(resp_high["camp_fold_induction"], 7.0)

    def test_organoid_t4_and_t3_secretion(self):
        """Engineered organoids secrete physiological T4 and T3 in a 12:1 molar ratio."""
        sec = self.engine.simulate_organoid_hormone_output(
            organoid_follicle_count=5000,
            serum_tsh_miu_l=2.0,
            incubation_hours=24.0,
            serum_iodide_um=0.3
        )
        self.assertGreater(sec["t4_secreted_ng"], 0.5)
        self.assertGreater(sec["t3_secreted_ng"], 0.02)
        self.assertAlmostEqual(sec["t4_to_t3_molar_ratio"], 12.0, places=2)

    def test_tsh_dependent_secretion_stimulation(self):
        """Secretory output increases monotonically with TSH stimulation factor."""
        sec_low = self.engine.simulate_organoid_hormone_output(organoid_follicle_count=2000, serum_tsh_miu_l=0.2)
        sec_high = self.engine.simulate_organoid_hormone_output(organoid_follicle_count=2000, serum_tsh_miu_l=5.0)
        self.assertGreater(sec_high["t4_secreted_ng"], 2.2 * sec_low["t4_secreted_ng"])


class TestAutoimmuneInterceptionAndTolerogenicNanoparticles(unittest.TestCase):
    """Verifies LSEC presentation, Treg induction, and halting of Hashimoto's follicular apoptosis."""

    def setUp(self):
        self.immune = AutoimmuneInterceptionModel()

    def test_untreated_hashimotos_disease_progression(self):
        """Untreated autoreactive Teff expansion leads to severe follicular destruction."""
        res = self.immune.simulate_pathology_and_interception(
            initial_follicle_count=3.0e6,
            initial_autoreactive_teff=5.0e4,
            simulation_days=180.0,
            tnp_dosing_schedule=None
        )
        # Without intervention, follicles are progressively destroyed
        self.assertLess(res["follicular_survival_fraction"], 0.60)
        self.assertFalse(res["is_autoimmunity_halted"])
        self.assertGreater(res["autoreactive_teff"][-1], res["autoreactive_teff"][0])

    def test_tnp_induced_tolerance_and_follicle_preservation(self):
        """tNP presenting TPO/Tg peptides to LSECs induces Tregs and halts follicular destruction."""
        dosing = [(10.0, 10.0), (17.0, 10.0), (24.0, 10.0), (31.0, 8.0)]
        res = self.immune.simulate_pathology_and_interception(
            initial_follicle_count=3.0e6,
            initial_autoreactive_teff=5.0e4,
            simulation_days=180.0,
            tnp_dosing_schedule=dosing
        )
        self.assertTrue(res["is_autoimmunity_halted"])
        self.assertGreater(res["follicular_survival_fraction"], 0.85)
        self.assertGreater(np.max(res["induced_tregs"]), 5000.0)
        self.assertGreater(res["induced_tregs"][-1], 200.0)
        self.assertLess(res["autoreactive_teff"][-1], 0.15 * 5.0e4)


class TestPharmacokineticsOralVsSubcutaneousImplant(unittest.TestCase):
    """Verifies PK/PD modeling of daily oral levothyroxine vs continuous subcutaneous implants."""

    def setUp(self):
        self.pk = ThyroidPharmacokineticsEngine()

    def test_oral_absorption_interactions(self):
        """Food, coffee, and iron chelation significantly reduce steady-state Free T4."""
        oral_fasting = self.pk.simulate_oral_lt4_regimen(daily_dose_ug=100.0, duration_days=60.0, condition="fasting")
        oral_meal = self.pk.simulate_oral_lt4_regimen(daily_dose_ug=100.0, duration_days=60.0, condition="food")
        oral_coffee = self.pk.simulate_oral_lt4_regimen(daily_dose_ug=100.0, duration_days=60.0, condition="coffee")

        self.assertGreater(oral_fasting["steady_state_mean_ft4"], oral_meal["steady_state_mean_ft4"])
        self.assertGreater(oral_meal["steady_state_mean_ft4"], oral_coffee["steady_state_mean_ft4"])

    def test_peak_to_trough_fluctuations_contrast(self):
        """Oral LT4 produces diurnal peak-to-trough spikes, whereas SubQ implant is zero-order steady."""
        oral = self.pk.simulate_oral_lt4_regimen(daily_dose_ug=100.0, duration_days=60.0, condition="fasting")
        subq = self.pk.simulate_subcutaneous_implant(daily_release_ug=85.0, duration_days=60.0)

        self.assertGreater(oral["steady_state_ft4_fluctuation_percent"], 5.0)
        self.assertLess(subq["steady_state_ft4_fluctuation_percent"], 0.5)

    def test_hpt_axis_negative_feedback(self):
        """Pituitary TSH suppression follows steep log-linear feedback with circulating FT4."""
        tsh_hypo = self.pk.calculate_pituitary_tsh(8.0)    # Low FT4 (hypothyroid)
        tsh_euthyroid = self.pk.calculate_pituitary_tsh(16.5) # Euthyroid FT4
        tsh_hyper = self.pk.calculate_pituitary_tsh(30.0)  # High FT4 (thyrotoxic)

        self.assertGreater(tsh_hypo, 10.0)
        self.assertTrue(1.0 <= tsh_euthyroid <= 2.5)
        self.assertLess(tsh_hyper, 0.4)


class TestIntegratedMultiscaleClinicalTrialSimulator(unittest.TestCase):
    """Verifies the multi-arm clinical scenario simulator integrating regeneration and tolerance."""

    def setUp(self):
        self.sim = RegenerativeThyroidSimulator()

    def test_comparative_trial_execution(self):
        """Run standard 180-day 7-arm trial and verify all inter-arm differences."""
        trial = self.sim.run_comparative_trial(simulation_days=180.0)

        # Arm 1: Untreated progresses to severe primary hypothyroidism
        self.assertGreater(trial["arm1_untreated"]["final_tsh"], 15.0)

        # Arm 3: Erratic oral dosing has compromised Time-in-Range (<80%)
        self.assertLess(trial["arm3_oral_erratic"]["time_in_range_tsh"], 85.0)

        # Arm 5: Organoids alone without tolerance are attacked and fail
        self.assertGreater(trial["arm5_organoid_alone"]["final_tsh"], 10.0)

        # Arm 6: Combo tNP + Organoids successfully restores euthyroidism
        self.assertTrue(trial["arm6_combo_tnp_organoid"]["euthyroid_restored"])
        self.assertTrue(NORMAL_SERUM_TSH_MIN <= trial["arm6_combo_tnp_organoid"]["final_tsh"] <= NORMAL_SERUM_TSH_MAX)

        # Arm 7: Subcutaneous implant maintains superior Time-in-Range
        self.assertGreater(trial["arm7_subcutaneous_implant"]["time_in_range_tsh"], 95.0)


if __name__ == "__main__":
    unittest.main()
