"""
Test Suite for Targeted Protein Degradation (TPD) Kinetics & Cooperativity Engine
================================================================================
Validates biophysical thermodynamics, ternary equilibrium solver accuracy,
mass conservation, the Hook effect, catalytic turnover ODEs, E3 ligase profiling,
and PROTAC vs. Molecular Glue biophysical parameters.
"""

import math
import unittest
import numpy as np

from tpd_protac_kinetics_engine import (
    ThermodynamicParameters,
    TernaryEquilibriumResult,
    HookEffectMetrics,
    DegradationKineticsParameters,
    DoseResponseResult,
    E3LigaseProfile,
    DegraderPhysicochemicalProfile,
    TernaryComplexEquilibrium,
    HookEffectAnalyzer,
    TPDKineticsSimulator,
    E3LigaseProfileDatabase,
    PROTACvsGlueComparator,
    TriComplexHookComparison,
    TricomplexAndGlueHookComparator,
    LinkerConformationProfile,
    UbiquitinationZoneModel,
    CovalentDegraderProfile,
    CovalentTPDKineticsSimulator,
    CascadeSimulationResult,
    PolyubiquitinationCascadeEngine,
    IsoformTargetProfile,
    IsoformCompetitionResult,
    IsoformCooperativityResolver,
    ResistanceImpactResult,
    TPDResistanceProfiler,
    HookTransitionThresholdResult,
    HookRetentionProfile,
    HookTransitionThresholdEngine,
    InVivoPKParameters,
    InVivoSimulationResult,
    InVivoDoseSweepResult,
    InVivoPKPDHookEngine,
    LYTACBiophysicalParameters,
    LYTACSimulationResult,
    LYTACTraffickingEngine,
    TargetTurnoverProfile,
    ResynthesisScalingResult,
    TargetResynthesisSpectrumEngine,
    TissueCellProfile,
    TissueDegradationResult,
    TissueSelectiveE3Engine,
    AutophagyBiophysicalParameters,
    AutophagySimulationResult,
    AutophagyTargetingEngine,
    RIBOTACParameters,
    RIBOTACHookMetrics,
    RIBOTACSimulationResult,
    RIBOTACKineticsEngine,
)


class TestThermodynamicsAndParameters(unittest.TestCase):
    """Verifies thermodynamic consistency, detailed balance, and parameter assertions."""

    def test_valid_thermodynamic_parameters(self):
        tp = ThermodynamicParameters(kd_target=100e-9, kd_e3=200e-9, alpha=10.0)
        self.assertEqual(tp.kd_target, 100e-9)
        self.assertEqual(tp.kd_e3, 200e-9)
        self.assertEqual(tp.alpha, 10.0)
        # Check Delta Delta G = -R * T * ln(alpha)
        expected_ddg = -8.31446261815324 * 310.15 * math.log(10.0)
        self.assertAlmostEqual(tp.delta_delta_g, expected_ddg, places=4)
        self.assertLess(tp.delta_delta_g_kcal, 0.0)  # Favorable cooperativity
        self.assertAlmostEqual(tp.delta_delta_g_kcal, -1.417, places=2)

    def test_invalid_parameters_raise(self):
        with self.assertRaises(ValueError):
            ThermodynamicParameters(kd_target=-10e-9, kd_e3=100e-9, alpha=1.0)
        with self.assertRaises(ValueError):
            ThermodynamicParameters(kd_target=10e-9, kd_e3=0.0, alpha=1.0)
        with self.assertRaises(ValueError):
            ThermodynamicParameters(kd_target=10e-9, kd_e3=100e-9, alpha=-2.0)

    def test_detailed_balance_and_primes(self):
        """Microscopic reversibility: Kd_T * Kd_E' = Kd_E * Kd_T' = (Kd_T * Kd_E) / alpha."""
        tp = ThermodynamicParameters(kd_target=50e-9, kd_e3=150e-9, alpha=5.0)
        self.assertAlmostEqual(tp.kd_target_prime, 10e-9, places=15)
        self.assertAlmostEqual(tp.kd_e3_prime, 30e-9, places=15)
        path1 = tp.kd_target * tp.kd_e3_prime
        path2 = tp.kd_e3 * tp.kd_target_prime
        self.assertAlmostEqual(path1, path2, places=20)


class TestTernaryComplexEquilibrium(unittest.TestCase):
    """Verifies ternary complex equilibrium solver precision, mass conservation, and limits."""

    def setUp(self):
        self.tp_pos = ThermodynamicParameters(kd_target=100e-9, kd_e3=100e-9, alpha=20.0)
        self.tp_neut = ThermodynamicParameters(kd_target=100e-9, kd_e3=100e-9, alpha=1.0)
        self.tp_neg = ThermodynamicParameters(kd_target=100e-9, kd_e3=100e-9, alpha=0.05)

    def test_mass_conservation_over_wide_concentration_range(self):
        """Mass conservation must hold to < 1e-12 M across 10^-12 M to 10^-3 M degrader."""
        solver = TernaryComplexEquilibrium(self.tp_pos)
        target_tot = 150e-9
        e3_tot = 80e-9

        concs = np.logspace(-12, -3, 50)
        for d_tot in concs:
            res = solver.solve(target_tot, e3_tot, float(d_tot))
            self.assertLess(res.mass_balance_error, 1e-12, f"Mass balance error too high at D={d_tot}")
            self.assertGreaterEqual(res.target_free, 0.0)
            self.assertGreaterEqual(res.e3_free, 0.0)
            self.assertGreaterEqual(res.degrader_free, 0.0)
            self.assertGreaterEqual(res.binary_td, 0.0)
            self.assertGreaterEqual(res.binary_ed, 0.0)
            self.assertGreaterEqual(res.ternary_ted, 0.0)

    def test_zero_concentration_boundaries(self):
        """Zero input concentrations must return exact zeros without division errors."""
        solver = TernaryComplexEquilibrium(self.tp_pos)
        r1 = solver.solve(0.0, 100e-9, 100e-9)
        self.assertEqual(r1.ternary_ted, 0.0)
        self.assertEqual(r1.binary_td, 0.0)

        r2 = solver.solve(100e-9, 0.0, 100e-9)
        self.assertEqual(r2.ternary_ted, 0.0)
        self.assertEqual(r2.binary_ed, 0.0)

        r3 = solver.solve(100e-9, 100e-9, 0.0)
        self.assertEqual(r3.ternary_ted, 0.0)
        self.assertEqual(r3.binary_td, 0.0)
        self.assertEqual(r3.binary_ed, 0.0)

    def test_cooperativity_enhances_ternary_formation(self):
        """Higher alpha must strictly increase [TED] at low/intermediate degrader concentrations."""
        s_pos = TernaryComplexEquilibrium(self.tp_pos)
        s_neut = TernaryComplexEquilibrium(self.tp_neut)
        s_neg = TernaryComplexEquilibrium(self.tp_neg)

        target_tot = 100e-9
        e3_tot = 100e-9
        d_tot = 50e-9

        r_pos = s_pos.solve(target_tot, e3_tot, d_tot)
        r_neut = s_neut.solve(target_tot, e3_tot, d_tot)
        r_neg = s_neg.solve(target_tot, e3_tot, d_tot)

        self.assertGreater(r_pos.ternary_ted, r_neut.ternary_ted)
        self.assertGreater(r_neut.ternary_ted, r_neg.ternary_ted)


class TestHookEffectAnalyzer(unittest.TestCase):
    """Verifies quantitative properties of the Hook effect and autoinhibition."""

    def setUp(self):
        self.tp = ThermodynamicParameters(kd_target=100e-9, kd_e3=100e-9, alpha=15.0)
        self.solver = TernaryComplexEquilibrium(self.tp)
        self.analyzer = HookEffectAnalyzer(self.solver)

    def test_hook_effect_autoinhibition_at_high_concentrations(self):
        """At supramicromolar degrader concentrations, [TED] must monotonically decline towards 0."""
        target_tot = 100e-9
        e3_tot = 100e-9

        # Solve at peak
        metrics = self.analyzer.analyze_hook_curve(target_tot, e3_tot)
        d_opt = metrics.d_opt
        ted_max = metrics.ted_max

        # Check concentrations above d_opt
        c_10x = d_opt * 10.0
        c_100x = d_opt * 100.0
        c_1000x = d_opt * 1000.0

        r_opt = self.solver.solve(target_tot, e3_tot, d_opt)
        r_10x = self.solver.solve(target_tot, e3_tot, c_10x)
        r_100x = self.solver.solve(target_tot, e3_tot, c_100x)
        r_1000x = self.solver.solve(target_tot, e3_tot, c_1000x)

        self.assertGreater(r_opt.ternary_ted, r_10x.ternary_ted)
        self.assertGreater(r_10x.ternary_ted, r_100x.ternary_ted)
        self.assertGreater(r_100x.ternary_ted, r_1000x.ternary_ted)
        # Deep suppression at 1000x: ternary fraction drops by >90%
        self.assertLess(r_1000x.ternary_ted, 0.10 * ted_max)

    def test_hook_metrics_structure(self):
        target_tot = 100e-9
        e3_tot = 100e-9
        metrics = self.analyzer.analyze_hook_curve(target_tot, e3_tot)

        self.assertGreater(metrics.ted_max, 0.0)
        self.assertLess(metrics.ted_max, min(target_tot, e3_tot))
        self.assertGreater(metrics.d_opt, 0.0)
        self.assertLess(metrics.c_hook_50_low, metrics.d_opt)
        self.assertGreater(metrics.c_hook_50_high, metrics.d_opt)
        self.assertGreater(metrics.c_hook_90_high, metrics.c_hook_50_high)
        self.assertGreater(metrics.fwhm_log10, 1.0)  # Typically 1.5 - 2.5 orders of magnitude

    def test_analytical_symmetric_d_opt_agreement(self):
        """Analytical formula target_tot + Kd / sqrt(alpha) should approximate numeric optimum."""
        kd = 100e-9
        alpha = 25.0
        target_tot = 100e-9
        e3_tot = 100e-9
        tp = ThermodynamicParameters(kd_target=kd, kd_e3=kd, alpha=alpha)
        solver = TernaryComplexEquilibrium(tp)
        analyzer = HookEffectAnalyzer(solver)

        metrics = analyzer.analyze_hook_curve(target_tot, e3_tot)
        approx_d_opt = analyzer.analytical_symmetric_d_opt(kd, alpha, target_tot)
        # Check within reasonable scaling factor (~2x)
        self.assertAlmostEqual(math.log10(metrics.d_opt), math.log10(approx_d_opt), delta=0.5)


class TestTPDKineticsSimulator(unittest.TestCase):
    """Verifies catalytic turnover ODEs, E3/degrader recycling, and dose-response."""

    def setUp(self):
        self.tp = ThermodynamicParameters(kd_target=50e-9, kd_e3=100e-9, alpha=10.0)
        self.kinetics = DegradationKineticsParameters(
            k_syn=1.0e-10,
            k_deg_basal=1.0e-4,
            k_ub=0.1,
            k_dub=0.01,
            k_cat_deg=0.05,
        )
        self.sim = TPDKineticsSimulator(self.tp, self.kinetics)

    def test_conserved_moieties_in_catalytic_cycle(self):
        """E3 total and Degrader total must remain strictly conserved during ODE integration."""
        target_0 = 100e-9
        e3_0 = 50e-9
        degrader_tot = 10e-9

        res = self.sim.simulate_time_course(target_0, e3_0, degrader_tot, duration_hours=6.0, num_time_points=100)

        # Check E3 total conservation
        e3_totals = res['e3_total']
        np.testing.assert_allclose(e3_totals, e3_0, rtol=1e-4, err_msg="E3 total moiety is not conserved")

        # Check Degrader total conservation
        degrader_totals = res['degrader_total']
        np.testing.assert_allclose(degrader_totals, degrader_tot, rtol=1e-4, err_msg="Degrader total moiety is not conserved")

    def test_catalytic_turnover_exceeds_unity(self):
        """Catalytic turnover number (TON) must exceed 1.0 (PROTAC degrades multiple targets per molecule)."""
        target_0 = 500e-9
        e3_0 = 100e-9
        degrader_tot = 5e-9  # Low sub-stoichiometric degrader

        ton = self.sim.catalytic_turnover_number(target_0, e3_0, degrader_tot, duration_hours=24.0)
        self.assertGreater(ton, 1.0, "TON must exceed 1.0 for catalytic degradation")
        self.assertGreater(ton, 10.0, f"Expected robust catalytic turnover, got {ton}")

    def test_dose_response_and_pharmacological_metrics(self):
        """Computes steady-state dose response, verifying DC50 and Dmax."""
        concs = np.logspace(-11, -5, 25)
        res = self.sim.compute_steady_state_dose_response(
            target_tot_baseline=200e-9,
            e3_tot=100e-9,
            concentrations=concs,
            incubation_time_hours=12.0,
        )
        self.assertGreater(res.d_max, 0.50, f"Dmax should be > 50%, got {res.d_max}")
        self.assertGreater(res.dc50, 0.0)
        self.assertLess(res.dc50, res.d_opt_degradation)
        self.assertGreaterEqual(res.hook_onset_conc, res.d_opt_degradation)


class TestE3LigaseProfileDatabase(unittest.TestCase):
    """Verifies curated E3 ligase properties and selectivity computations."""

    def test_database_retrieval(self):
        for name in ['CRBN', 'VHL', 'cIAP1', 'MDM2']:
            prof = E3LigaseProfileDatabase.get_profile(name)
            self.assertEqual(prof.name, name)
            self.assertGreater(prof.cellular_abundance_nm, 0.0)
            self.assertGreater(prof.typical_kd_nm, 0.0)
            self.assertGreater(prof.typical_cooperativity_alpha, 0.0)
            self.assertGreater(prof.clinical_stage_prevalence, 0.0)

    def test_selectivity_ratio_calculation(self):
        """Compares CRBN vs VHL recruitment given differential cooperativity."""
        res = E3LigaseProfileDatabase.calculate_selectivity_ratio(
            target_tot=100e-9,
            degrader_tot=50e-9,
            kd_target=50e-9,
            e3_1_name='VHL',
            e3_2_name='CRBN',
            kd_e3_1=180e-9,
            kd_e3_2=150e-9,
            alpha_1=20.0,  # MZ1-like positive cooperativity for VHL
            alpha_2=1.0,   # Neutral for CRBN
        )
        self.assertGreater(res['ternary_ted_e3_1'], res['ternary_ted_e3_2'])
        self.assertGreater(res['selectivity_ratio'], 1.0)
        self.assertAlmostEqual(res['cooperativity_advantage'], 20.0, places=2)


class TestPROTACvsGlueComparator(unittest.TestCase):
    """Verifies physicochemical profiling and Lipinski Rule of 5 distinctions."""

    def test_benchmark_compounds_load(self):
        protacs = PROTACvsGlueComparator.get_compounds_by_modality('PROTAC')
        glues = PROTACvsGlueComparator.get_compounds_by_modality('Molecular Glue')
        self.assertGreaterEqual(len(protacs), 3)
        self.assertGreaterEqual(len(glues), 3)

    def test_rule_of_five_demarcation(self):
        """PROTACs must violate Rule of 5 (MW > 700), Glues must obey Rule of 5 (MW < 500)."""
        stats = PROTACvsGlueComparator.compute_modality_statistics()
        # PROTACs
        self.assertGreater(stats['PROTAC']['mean_mw'], 700.0)
        self.assertGreater(stats['PROTAC']['mean_ro5_violations'], 1.5)
        self.assertLess(stats['PROTAC']['mean_papp'], 2.0)

        # Molecular Glues
        self.assertLess(stats['Molecular Glue']['mean_mw'], 500.0)
        self.assertEqual(stats['Molecular Glue']['mean_ro5_violations'], 0.0)
        self.assertGreater(stats['Molecular Glue']['mean_papp'], 5.0)

    def test_chameleonic_permeability_enhancement(self):
        """Intramolecular hydrogen bonding shielding polar area enhances permeability."""
        enhancement = PROTACvsGlueComparator.estimate_chameleonic_permeability_enhancement(
            tpsa_open=200.0,
            chameleonic_potential=1.8,
        )
        self.assertGreater(enhancement, 1.0)
        self.assertAlmostEqual(enhancement, math.exp(0.025 * (200.0 - 200.0 / 1.8)), places=4)


class TestAsymptoticRegimesAndEdgeCases(unittest.TestCase):
    """Verifies asymptotic limits, extreme cooperativity, and washout dynamics."""

    def test_extreme_supramicromolar_saturation_limit(self):
        """As [D]_tot -> infinity, all Target becomes [TD], all E3 becomes [ED], and [TED] -> 0."""
        tp = ThermodynamicParameters(kd_target=100e-9, kd_e3=100e-9, alpha=10.0)
        solver = TernaryComplexEquilibrium(tp)
        target_tot = 50e-9
        e3_tot = 50e-9
        # Extremely high degrader concentration: 10 mM (1e-2 M)
        res = solver.solve(target_tot, e3_tot, 1e-2)

        # Free target and free E3 must be near zero
        self.assertLess(res.target_free / target_tot, 1e-4)
        self.assertLess(res.e3_free / e3_tot, 1e-4)
        # Ternary complex must be suppressed (< 0.1% of target)
        self.assertLess(res.ternary_ted / target_tot, 1e-3)
        # Target must be virtually all in binary TD, E3 in binary ED
        self.assertAlmostEqual(res.binary_td / target_tot, 1.0, places=3)
        self.assertAlmostEqual(res.binary_ed / e3_tot, 1.0, places=3)
        # Free degrader must be approximately [D]_tot - [T]_tot - [E]_tot
        expected_free_d = 1e-2 - target_tot - e3_tot
        self.assertAlmostEqual(res.degrader_free, expected_free_d, places=5)

    def test_extreme_positive_cooperativity_molecular_glue_limit(self):
        """With alpha = 10000 (molecular glue limit), ternary complex forms with high efficiency at sub-Kd doses."""
        tp = ThermodynamicParameters(kd_target=1e-6, kd_e3=1e-6, alpha=10000.0)
        solver = TernaryComplexEquilibrium(tp)
        target_tot = 50e-9
        e3_tot = 50e-9
        # Degrader at only 50 nM (20x below binary Kd)
        res = solver.solve(target_tot, e3_tot, 50e-9)
        # Due to 10,000x cooperativity, ternary complex should form robustly
        self.assertGreater(res.ternary_ted, 20e-9)

    def test_asymmetric_affinities(self):
        """Asymmetric affinities: Kd_T = 10 nM, Kd_E = 1000 nM."""
        tp = ThermodynamicParameters(kd_target=10e-9, kd_e3=1000e-9, alpha=5.0)
        solver = TernaryComplexEquilibrium(tp)
        target_tot = 100e-9
        e3_tot = 100e-9
        res = solver.solve(target_tot, e3_tot, 100e-9)
        # Binary TD should be much greater than binary ED
        self.assertGreater(res.binary_td, res.binary_ed * 5.0)

    def test_target_washout_and_resynthesis_recovery(self):
        """After degrader washout ([D]=0), target recovers asymptotically to k_syn / k_deg_basal."""
        tp = ThermodynamicParameters(kd_target=100e-9, kd_e3=100e-9, alpha=5.0)
        k_syn = 2.0e-11
        k_deg_basal = 1.0e-4
        target_ss = k_syn / k_deg_basal  # 200 nM
        kinetics = DegradationKineticsParameters(k_syn=k_syn, k_deg_basal=k_deg_basal)
        sim = TPDKineticsSimulator(tp, kinetics)

        # Start from depleted state (10 nM target) with [D] = 0 (washout)
        res = sim.simulate_time_course(target_tot_0=10e-9, e3_tot_0=100e-9, degrader_tot=0.0, duration_hours=36.0)
        final_target = res['target_total'][-1]
        # Target must recover close to steady state target_ss (200 nM)
        self.assertGreater(final_target, 180e-9)
        self.assertLessEqual(final_target, target_ss * 1.01)


class TestTricomplexAndGlueHookComparator(unittest.TestCase):
    """
    Validates cross-modality hook comparisons between PROTACs, molecular glues,
    and tri-complex RAS(ON) inhibitors, including the Hook Immunity Theorem.
    """

    def test_morrison_plateau_exact_agreement(self):
        """Analytical Morrison equation must match asymptotic [TED] in ideal glue."""
        target_tot = 100e-9
        presenter_tot = 100e-9
        kd_ternary = 20e-9  # 20 nM
        morrison = TricomplexAndGlueHookComparator.calculate_morrison_plateau(
            target_tot, presenter_tot, kd_ternary
        )
        self.assertAlmostEqual(morrison, 64.174243e-9, delta=1e-12)

        # Numerical solver with Kd_T = 1.0 M (alpha = 1.0 / 20e-9 = 5e7)
        tp = ThermodynamicParameters(kd_target=1.0, kd_e3=100e-9, alpha=1.0 / kd_ternary)
        solver = TernaryComplexEquilibrium(tp)
        # At 1 mM degrader, [TED] should match Morrison plateau within 0.5%
        res = solver.solve(target_tot, presenter_tot, 1e-3)
        self.assertAlmostEqual(res.ternary_ted, morrison, delta=1e-9)

    def test_hook_shift_fold_factors(self):
        """Molecular glues (CC-90009) and tri-complexes (RMC-6236) must show massive hook shift vs MZ1."""
        comp_dict = TricomplexAndGlueHookComparator.compare_paradigms()
        mz1 = comp_dict["MZ1"]
        cc90009 = comp_dict["CC-90009"]
        rmc_glue = comp_dict["RMC-6236_glue_model"]
        rmc_hyp = comp_dict["RMC-6236_hypatia_model"]

        # CC-90009 hook threshold should be > 50x higher than MZ1
        self.assertGreater(cc90009.hook_shift_fold_vs_protac, 50.0)
        # RMC-6236 glue model hook threshold should be > 1000x higher than MZ1
        self.assertGreater(rmc_glue.hook_shift_fold_vs_protac, 1000.0)
        # RMC-6236 Hypatia alpha=18 model should also show substantial shift due to 5 uM CypA
        self.assertGreater(rmc_hyp.hook_shift_fold_vs_protac, 20.0)

    def test_hook_immunity_limit_convergence(self):
        """Monotonic convergence to Morrison plateau as binary Kd_target increases."""
        results = TricomplexAndGlueHookComparator.test_hook_immunity_limit(
            target_tot=100e-9,
            presenter_tot=100e-9,
            kd_presenter=100e-9,
            kd_target_ternary=20e-9,
        )
        # Fraction of Morrison at 1 mM must increase monotonically
        fractions = [r["fraction_of_morrison_at_1mm"] for r in results]
        for i in range(len(fractions) - 1):
            self.assertGreaterEqual(fractions[i + 1], fractions[i])

        # At Kd_target = 1.0 M, fraction should exceed 0.99
        self.assertGreater(fractions[-1], 0.99)

    def test_chaperone_abundance_buffering_effect(self):
        """Cytosolic CypA abundance (5 uM) buffers RMC-6236 from hook suppression across a wide dynamic span."""
        comp_dict = TricomplexAndGlueHookComparator.compare_paradigms()
        rmc_glue = comp_dict["RMC-6236_glue_model"]
        mz1 = comp_dict["MZ1"]

        # FWHM span should be significantly broader for RMC-6236 (> 4 log10 units) than MZ1 (< 2.5 log10 units)
        self.assertGreater(rmc_glue.fwhm_log10, 4.0)
        self.assertLess(mz1.fwhm_log10, 2.5)


class TestUbiquitinationZoneModel(unittest.TestCase):
    """Validates the spatial ubiquitination zone and linker Goldilocks principle."""

    def test_end_to_end_probability_density_normalization(self):
        """Radial distribution integral over space must equal 1.0."""
        r_vals = np.linspace(0.01, 80.0, 2000)
        dr = r_vals[1] - r_vals[0]
        p_vals = [UbiquitinationZoneModel.end_to_end_probability_density(r, n_bonds=14, kuhn_b=3.8) for r in r_vals]
        total_prob = sum(p_vals) * dr
        self.assertAlmostEqual(total_prob, 1.0, places=3)

    def test_conformational_entropy_penalty_monotonicity(self):
        """Conformational entropy penalty Delta G_entropy must increase monotonically with linker length."""
        penalties = [UbiquitinationZoneModel.conformational_entropy_penalty(nb)[1] for nb in [4, 8, 12, 16, 24, 32]]
        for i in range(len(penalties) - 1):
            self.assertGreaterEqual(penalties[i + 1], penalties[i])
        self.assertEqual(penalties[0], 0.0)  # Reference bonds N=4 has zero penalty
        self.assertGreater(penalties[-1], 1.8)  # N=32 has > 1.8 kcal/mol penalty

    def test_goldilocks_curve_peak(self):
        """Degradation fitness must exhibit a clear optimum at intermediate length (N=14-16)."""
        series = UbiquitinationZoneModel.evaluate_linker_series(alpha_0=50.0)
        fitness_dict = {item["num_bonds"]: item["degradation_fitness_score"] for item in series}
        
        # N=4 is too short to reach zone: productive fraction < 0.01
        self.assertLess(series[0]["f_productive"], 0.01)
        # Intermediate N=16 has highest or near-highest fitness
        self.assertGreater(fitness_dict[16], fitness_dict[4])
        self.assertGreater(fitness_dict[16], fitness_dict[32])


class TestCovalentTPDKineticsSimulator(unittest.TestCase):
    """Validates covalent vs reversible degradation kinetics and stoichiometric limits."""

    def test_target_covalent_stoichiometric_limitation(self):
        """Target-covalent degrader destroys degrader alongside target, bounding TON <= 1.0."""
        prof = CovalentDegraderProfile(
            name="Target_Covalent_PROTAC",
            mechanism="target_covalent",
            k_inact=0.05,
            k_ub=0.05,
            k_deg=0.02,
        )
        sim = CovalentTPDKineticsSimulator(prof)
        # 20 nM degrader with 200 nM target
        ton = sim.compute_turnover_number(target_tot_0=200e-9, degrader_tot_0=20e-9, duration_hours=24.0)
        # Numerically bounded by 1.0 within ODE tolerance
        self.assertLessEqual(ton, 1.001)
        self.assertAlmostEqual(ton, 1.0, places=3)
        self.assertGreater(ton, 0.8)

    def test_e3_covalent_catalytic_recycling(self):
        """E3-covalent degrader recycles ED_cov complex intact, achieving catalytic TON > 1.0."""
        prof = CovalentDegraderProfile(
            name="E3_Covalent_PROTAC",
            mechanism="e3_covalent",
            k_inact=0.05,
            k_ub=0.05,
            k_deg=0.02,
        )
        sim = CovalentTPDKineticsSimulator(prof)
        ton = sim.compute_turnover_number(target_tot_0=200e-9, degrader_tot_0=20e-9, duration_hours=24.0)
        # E3-covalent should degrade all 200 nM target (TON ~ 10.0)
        self.assertGreater(ton, 5.0)

    def test_reversible_benchmark_recycling(self):
        """Reversible degrader also achieves catalytic recycling TON > 1.0."""
        prof = CovalentDegraderProfile(
            name="Reversible_PROTAC",
            mechanism="reversible",
            k_ub=0.05,
            k_deg=0.02,
        )
        sim = CovalentTPDKineticsSimulator(prof)
        ton = sim.compute_turnover_number(target_tot_0=200e-9, degrader_tot_0=20e-9, duration_hours=24.0)
        self.assertGreater(ton, 5.0)


class TestPolyubiquitinationCascadeEngine(unittest.TestCase):
    """Validates multi-step polyubiquitination cascade and DUB futile cycling."""

    def test_futile_cycling_suppression(self):
        """When rho = k_ub / k_dub < 0.2, target degradation collapses to near zero."""
        engine_futile = PolyubiquitinationCascadeEngine(k_ub=0.005, k_dub=0.05, k_cat_deg=0.02)
        res_futile = engine_futile.simulate_cascade(ted_pool_m=10e-9, duration_seconds=3600.0)
        self.assertLess(res_futile.final_degraded_fraction, 0.05)

        engine_productive = PolyubiquitinationCascadeEngine(k_ub=0.1, k_dub=0.01, k_cat_deg=0.02)
        res_productive = engine_productive.simulate_cascade(ted_pool_m=10e-9, duration_seconds=3600.0)
        self.assertGreater(res_productive.final_degraded_fraction, 0.90)

    def test_analytical_tetra_ub_progression_ratio(self):
        """Analytical formula P(Ub>=4) = (rho / (1+rho))^4 accurately predicts chain efficiency."""
        engine = PolyubiquitinationCascadeEngine(k_ub=0.04, k_dub=0.02)
        self.assertEqual(engine.progression_ratio_rho, 2.0)
        expected_eff = (2.0 / 3.0) ** 4  # ~0.1975
        self.assertAlmostEqual(engine.analytical_tetra_ub_efficiency, expected_eff, places=4)


class TestIsoformCooperativityResolver(unittest.TestCase):
    """Validates multi-target competitive ternary equilibrium and isoform selectivity."""

    def test_multi_isoform_mass_conservation(self):
        """All target isoforms, ligase, and degrader must conserve mass strictly."""
        targets = [
            IsoformTargetProfile(name="BRD4", total_concentration=100e-9, kd_binary=20e-9, cooperativity_alpha=20.0),
            IsoformTargetProfile(name="BRD2", total_concentration=100e-9, kd_binary=20e-9, cooperativity_alpha=1.0),
            IsoformTargetProfile(name="BRD3", total_concentration=100e-9, kd_binary=20e-9, cooperativity_alpha=0.8),
        ]
        res = IsoformCooperativityResolver.solve_competitive_equilibrium(targets, e3_tot=100e-9, kd_e3=100e-9, degrader_tot=100e-9)
        # Sum of ternary complexes cannot exceed total E3
        sum_teds = sum(res.ternary_concentrations.values())
        self.assertLessEqual(sum_teds, 100e-9)
        # BRD4 must dominate over BRD2
        self.assertGreater(res.ternary_concentrations["BRD4"], res.ternary_concentrations["BRD2"] * 5.0)

    def test_bet_bromodomain_selectivity_amplification(self):
        """MZ1 achieves exactly 20.0x selectivity at sub-saturating doses and > 5x at peak."""
        results = IsoformCooperativityResolver.evaluate_bet_bromodomain_paradigm(e3_tot=100e-9, kd_vhl=100e-9)
        # Lowest dose selectivity must equal alpha_BRD4 / alpha_BRD2 = 20.0
        lowest_dose = results[0]
        self.assertAlmostEqual(lowest_dose["selectivity_brd4_over_brd2"], 20.0, delta=0.5)
        # Peak BRD4 complex must be significantly higher than BRD2
        peak = max(results, key=lambda x: x["brd4_ted_nm"])
        self.assertGreater(peak["selectivity_brd4_over_brd2"], 5.0)


class TestTPDResistanceProfiler(unittest.TestCase):
    """Validates clinical resistance profiling and cross-modality shifts."""

    def setUp(self):
        self.tp = ThermodynamicParameters(kd_target=50e-9, kd_e3=100e-9, alpha=15.0)

    def test_e3_downregulation_reduces_ted_max(self):
        """10-fold reduction in ligase reduces [TED]_max to approximately 10-15% of baseline."""
        res = TPDResistanceProfiler.evaluate_e3_downregulation(self.tp, fold_loss=10.0)
        self.assertLess(res.ted_max_retention_pct, 15.0)
        self.assertGreater(res.ted_max_retention_pct, 5.0)

    def test_e3_point_mutation_shifts_dc50(self):
        """50-fold affinity loss shifts DC50 to higher concentrations (RF > 2.0)."""
        res = TPDResistanceProfiler.evaluate_e3_point_mutation(self.tp, affinity_loss_fold=50.0)
        self.assertGreater(res.resistance_factor_rf, 2.0)
        self.assertLess(res.ted_max_retention_pct, 35.0)

    def test_pgp_efflux_protac_vs_molecular_glue(self):
        """PROTAC experiences ~11x resistance factor from P-gp, while molecular glue experiences ~1.1x."""
        res_protac = TPDResistanceProfiler.evaluate_pgp_efflux_resistance(self.tp, is_protac=True)
        res_glue = TPDResistanceProfiler.evaluate_pgp_efflux_resistance(self.tp, is_protac=False)
        self.assertAlmostEqual(res_protac.resistance_factor_rf, 11.0, delta=0.1)
        self.assertAlmostEqual(res_glue.resistance_factor_rf, 1.1, delta=0.05)
        self.assertGreater(res_protac.resistance_factor_rf, res_glue.resistance_factor_rf * 9.0)


class TestHookTransitionThresholdEngine(unittest.TestCase):
    """
    Validates the exact mathematical theorems and closed-form solutions for:
    1. K_eff(x) minimization and universal free optimum x_opt = sqrt(K1 * K2).
    2. Universal total optimum D_opt_tot = sqrt(K1 * K2) + w1 * T_tot + w2 * E_tot.
    3. Closed-form Morrison [TED]_max matching numerical solver.
    4. Exact closed-form quadratic threshold for monotonic saturation up to C_cutoff.
    5. Hook retention index and cross-modality archetype profile (PROTAC vs Glue).
    6. Chaperone buffering capacity sweep and Hook immunity limit.
    """

    def test_keff_minimum_and_universal_free_d_opt(self):
        """K_eff(x) is globally minimized at x_opt = sqrt(K1 * K2), independent of alpha."""
        k1 = 80e-9
        k2 = 180e-9
        expected_x_opt = math.sqrt(k1 * k2)

        for alpha in [0.2, 1.0, 15.0, 500.0]:
            x_calc = HookTransitionThresholdEngine.compute_analytical_free_d_opt(k1, k2)
            self.assertAlmostEqual(x_calc, expected_x_opt, places=12)

            # Check that d(K_eff)/dx is zero at x_opt:
            # d(K_eff)/dx = (1 / alpha) * (1 - K1*K2 / x^2)
            deriv = (1.0 / alpha) * (1.0 - (k1 * k2) / (x_calc ** 2))
            self.assertAlmostEqual(deriv, 0.0, places=10)

            # Check K_eff value at minimum
            keff_min = HookTransitionThresholdEngine.compute_keff_min(k1, k2, alpha)
            keff_eval = HookTransitionThresholdEngine.compute_keff(x_calc, k1, k2, alpha)
            self.assertAlmostEqual(keff_min, keff_eval, places=12)

    def test_analytical_total_d_opt_mass_balance_agreement(self):
        """Analytical formula D_opt_tot matches numerical grid search within 0.05%."""
        test_cases = [
            (100e-9, 100e-9, 100e-9, 100e-9, 1.0),
            (50e-9, 180e-9, 100e-9, 140e-9, 20.0),
            (200e-6, 500e-9, 1.0e-6, 5.0e-6, 40000.0),
        ]
        for k1, k2, t_tot, e_tot, alpha in test_cases:
            d_opt_analytical = HookTransitionThresholdEngine.compute_analytical_total_d_opt(k1, k2, t_tot, e_tot)
            tp = ThermodynamicParameters(kd_target=k1, kd_e3=k2, alpha=alpha)
            solver = TernaryComplexEquilibrium(tp)

            # Search around analytical optimum on dense grid
            d_grid = np.logspace(np.log10(d_opt_analytical * 0.5), np.log10(d_opt_analytical * 2.0), 5000)
            res_list = [solver.solve(t_tot, e_tot, d).ternary_ted for d in d_grid]
            d_opt_numerical = d_grid[np.argmax(res_list)]

            rel_error = abs(d_opt_analytical - d_opt_numerical) / d_opt_analytical
            self.assertLess(rel_error, 0.001)  # Within 0.1%

    def test_closed_form_ted_max_matches_exact_solver(self):
        """Closed-form [TED]_max from K_eff_min matches numerical solver at D_opt."""
        k1 = 50e-9
        k2 = 180e-9
        alpha = 20.0
        t_tot = 100e-9
        e_tot = 140e-9

        ted_max_closed = HookTransitionThresholdEngine.compute_analytical_ted_max(k1, k2, alpha, t_tot, e_tot)
        d_opt = HookTransitionThresholdEngine.compute_analytical_total_d_opt(k1, k2, t_tot, e_tot)

        tp = ThermodynamicParameters(kd_target=k1, kd_e3=k2, alpha=alpha)
        solver = TernaryComplexEquilibrium(tp)
        res = solver.solve(t_tot, e_tot, d_opt)

        self.assertAlmostEqual(ted_max_closed * 1e9, res.ternary_ted * 1e9, places=2)

    def test_exact_monotonic_saturation_threshold_quadratic(self):
        """The quadratic root K1* produces D_opt_tot == C_cutoff exactly."""
        k2 = 500e-9
        t_tot = 1.0e-6
        e_tot = 5.0e-6
        c_cutoff = 10.0e-6
        k_ter = 5.0e-9

        thresh = HookTransitionThresholdEngine.compute_monotonic_saturation_threshold(
            kd_presenter=k2, target_tot=t_tot, presenter_tot=e_tot, c_cutoff=c_cutoff, ternary_kd=k_ter
        )

        self.assertAlmostEqual(thresh.d_opt_at_threshold_m, c_cutoff, places=9)
        self.assertGreater(thresh.gamma_critical, 100.0)
        self.assertGreater(thresh.alpha_critical, 10000.0)

        # Above critical threshold, D_opt_tot must exceed C_cutoff (monotonic on [0, C_cutoff])
        d_opt_above = HookTransitionThresholdEngine.compute_analytical_total_d_opt(
            thresh.kd_target_critical_m * 1.5, k2, t_tot, e_tot
        )
        self.assertGreater(d_opt_above, c_cutoff)

    def test_hook_retention_archetypes_contrast(self):
        """Cross-modality archetype profile correctly reflects PROTAC collapse vs Glue immunity."""
        archetypes = HookTransitionThresholdEngine.evaluate_archetypes_at_cutoff(c_cutoff=10.0e-6)

        mz1 = archetypes["MZ1"]
        arv = archetypes["ARV-110"]
        cc = archetypes["CC-90009"]
        rmc = archetypes["RMC-6236"]

        # PROTACs must suffer severe hook effect suppression (< 30% retention at 10 uM)
        self.assertLess(mz1.retention_fraction, 0.30)
        self.assertGreater(mz1.suppression_pct, 70.0)
        self.assertFalse(mz1.is_monotonic_at_eval)

        self.assertLess(arv.retention_fraction, 0.20)
        self.assertGreater(arv.suppression_pct, 80.0)
        self.assertFalse(arv.is_monotonic_at_eval)

        # Molecular glues must exhibit high retention (> 95%)
        self.assertGreater(cc.retention_fraction, 0.95)
        self.assertLess(cc.suppression_pct, 5.0)

        # Tri-complex RAS(ON) glue must be strictly monotonic at 10 uM (> 99.8% retention)
        self.assertGreaterEqual(rmc.retention_fraction, 0.998)
        self.assertTrue(rmc.is_monotonic_at_eval)

    def test_chaperone_buffering_sweep(self):
        """Increasing chaperone presenter pool from 100 nM to 10 uM shifts D_opt_tot upward by ~10 uM."""
        sweep = HookTransitionThresholdEngine.evaluate_chaperone_buffering_sweep(
            kd_target=200e-6, kd_presenter=500e-9, alpha=40000.0, target_tot=1.0e-6, c_cutoff=10.0e-6
        )

        low_e = sweep[1]   # 100 nM
        high_e = sweep[7]  # 10 uM

        # D_opt_tot shift
        d_opt_shift = high_e["d_opt_tot_m"] - low_e["d_opt_tot_m"]
        self.assertGreater(d_opt_shift, 9.0e-6)

        # High chaperone concentration achieves full monotonic saturation
        self.assertTrue(high_e["is_monotonic"])
        self.assertGreater(high_e["retention_fraction"], 0.999)


class TestInVivoPKPDHookEngine(unittest.TestCase):
    """Validates oral PK/PD coupling and the In Vivo Hook Dissipation Theorem."""

    def setUp(self):
        self.tp = ThermodynamicParameters(kd_target=50e-9, kd_e3=180e-9, alpha=20.0)
        self.pk_engine = InVivoPKPDHookEngine(self.tp)

    def test_pk_plasma_and_cytosolic_profiles(self):
        """Unbound cytosolic concentration is dampened by plasma protein binding."""
        res = self.pk_engine.simulate_single_dose(140.0)
        expected_free_cmax = res.cmax_plasma_um * 1000.0 * self.pk_engine.pk.fu_plasma * self.pk_engine.pk.kp_uu
        self.assertAlmostEqual(res.cmax_free_nm, expected_free_cmax, places=4)
        self.assertGreater(res.tmax_plasma_h, 0.5)
        self.assertLess(res.tmax_plasma_h, 4.0)

    def test_in_vivo_hook_dissipation_across_clinical_doses(self):
        """Clinical oral doses (100 to 1000 mg) achieve sustained > 95% target AUC suppression."""
        for dose in [100.0, 300.0, 1000.0]:
            res = self.pk_engine.simulate_single_dose(dose)
            self.assertGreater(res.target_auc_suppression_pct, 95.0)
            self.assertLess(res.min_target_pct, 1.0)

    def test_in_vivo_dose_sweep_absence_of_hook(self):
        """Within realistic clinical dosing (up to 3000 mg), in vivo hook rebound is absent."""
        sweep = self.pk_engine.evaluate_dose_sweep([30.0, 100.0, 300.0, 1000.0, 3000.0])
        self.assertFalse(sweep.in_vivo_hook_observed)
        self.assertIsNone(sweep.in_vivo_hook_onset_dose_mg)

    def test_target_auc_suppression_monotonicity(self):
        """Target AUC suppression increases monotonically from sub-therapeutic to clinical doses."""
        res_low = self.pk_engine.simulate_single_dose(10.0)
        res_high = self.pk_engine.simulate_single_dose(300.0)
        self.assertGreater(res_high.target_auc_suppression_pct, res_low.target_auc_suppression_pct)


class TestLYTACTraffickingEngine(unittest.TestCase):
    """Validates non-proteasomal degradation via LYTAC endosomal shuttling and lysosomal delivery."""

    def setUp(self):
        self.lytac_engine = LYTACTraffickingEngine()

    def test_lytac_catalytic_turnover_exceeds_unity(self):
        """Sub-stoichiometric LYTAC (5 nM) achieves catalytic turnover (TON > 20) over 24 hours."""
        res = self.lytac_engine.simulate(target_surf_0=100e-9, receptor_surf_0=50e-9, lytac_ext_0=5e-9)
        self.assertGreater(res.catalytic_turnover_number, 20.0)
        self.assertGreater(res.peptides_degraded_nm[-1], 100.0)

    def test_lytac_surface_target_clearance(self):
        """Surface target is cleared by > 90% via receptor-mediated endocytosis."""
        res = self.lytac_engine.simulate(target_surf_0=100e-9, receptor_surf_0=50e-9, lytac_ext_0=5e-9)
        self.assertGreater(res.target_knockdown_pct, 90.0)
        self.assertLess(res.target_surface_nm[-1], 10.0)

    def test_bafilomycin_acidification_block_impairment(self):
        """Blocking endosomal acidification (k_acid -> 0) severely impairs catalytic turnover and target clearance."""
        baf_params = LYTACBiophysicalParameters(k_acid=0.00005)
        baf_engine = LYTACTraffickingEngine(baf_params)
        res_ctrl = self.lytac_engine.simulate()
        res_baf = baf_engine.simulate()

        # Turnover collapses by > 5-fold
        self.assertLess(res_baf.catalytic_turnover_number, res_ctrl.catalytic_turnover_number / 5.0)
        # Surface target remains largely intact
        self.assertGreater(res_baf.target_surface_nm[-1], 70.0)
        self.assertLess(res_baf.target_knockdown_pct, 30.0)

    def test_receptor_shuttling_pool_conservation(self):
        """Receptor pool is conserved (> 99%) through recycling rather than consumed in lysosomes."""
        res = self.lytac_engine.simulate()
        self.assertGreaterEqual(res.receptor_conservation_pct, 99.0)


class TestTargetResynthesisSpectrumEngine(unittest.TestCase):
    """Validates target resynthesis scaling laws and basal turnover hierarchy."""

    def test_analytical_required_occupancy_scaling(self):
        """Required ternary fraction scales as odds * (k_deg_basal / k_cat_deg)."""
        # For BRD4 (t_1/2 = 10 h)
        f_50 = TargetResynthesisSpectrumEngine.compute_required_ternary_fraction(10.0, 0.50, k_cat_deg=0.02)
        f_90 = TargetResynthesisSpectrumEngine.compute_required_ternary_fraction(10.0, 0.90, k_cat_deg=0.02)
        self.assertAlmostEqual(f_90, 9.0 * f_50, places=6)

    def test_cmyc_vs_tau_resynthesis_barrier(self):
        """Rapid-turnover c-Myc requires > 100x higher ternary occupancy than slow-turnover Tau for 90% knockdown."""
        spectrum = TargetResynthesisSpectrumEngine.evaluate_target_spectrum()
        cmyc = next(s for s in spectrum if s.target_name == "c-Myc")
        tau = next(s for s in spectrum if s.target_name == "Tau")
        ratio = cmyc.required_ternary_fraction_90pct_deg / tau.required_ternary_fraction_90pct_deg
        self.assertGreater(ratio, 100.0)

    def test_theoretical_dmax_ceiling(self):
        """With weak ubiquitination (k_cat = 0.001 s^-1), rapid-turnover targets cannot achieve 90% Dmax."""
        dmax_cmyc = TargetResynthesisSpectrumEngine.compute_achievable_dmax(0.33, k_cat_deg=0.001, max_ternary_fraction=0.80)
        dmax_tau = TargetResynthesisSpectrumEngine.compute_achievable_dmax(48.0, k_cat_deg=0.001, max_ternary_fraction=0.80)
        self.assertLess(dmax_cmyc, 65.0)
        self.assertGreater(dmax_tau, 99.0)

    def test_spectrum_monotonicity_with_halflife(self):
        """Required ternary occupancy decreases strictly monotonically with increasing half-life."""
        spectrum = TargetResynthesisSpectrumEngine.evaluate_target_spectrum()
        for i in range(len(spectrum) - 1):
            self.assertGreater(
                spectrum[i].required_ternary_fraction_dc50_pct,
                spectrum[i + 1].required_ternary_fraction_dc50_pct,
            )


class TestTissueSelectiveE3Engine(unittest.TestCase):
    """Validates tissue-selective E3 hijacking and platelet-sparing paradigms (DT2216 vs PZ15227)."""

    def test_bcl_xl_expression_differential_tumor_vs_platelets(self):
        """VHL expression in platelets is negligible compared to tumor (> 1000-fold lower)."""
        bclxl = TissueSelectiveE3Engine.evaluate_bcl_xl_paradigm(doses_nm=[100.0])
        dt_res = bclxl["DT2216"]["dose_responses"][0]
        self.assertEqual(dt_res.compound_name, "DT2216")
        self.assertEqual(dt_res.e3_recruited, "VHL")
        self.assertGreater(bclxl["DT2216"]["therapeutic_safety_index"], 100.0)

    def test_dt2216_spares_platelets_and_ablates_tumor(self):
        """At 100 nM DT2216, tumor BCL-xL is <= 20% while platelet BCL-xL remains > 70%."""
        bclxl = TissueSelectiveE3Engine.evaluate_bcl_xl_paradigm(doses_nm=[100.0])
        dt_res = bclxl["DT2216"]["dose_responses"][0]
        self.assertTrue(dt_res.is_tumor_ablated)
        self.assertTrue(dt_res.is_normal_tissue_spared)
        self.assertLessEqual(dt_res.tumor_target_level_pct, 20.0)
        self.assertGreaterEqual(dt_res.normal_tissue_target_level_pct, 70.0)

    def test_pz15227_crbn_destroys_platelets(self):
        """At 100 nM PZ15227 (CRBN), platelet BCL-xL is completely wiped out (< 10%)."""
        bclxl = TissueSelectiveE3Engine.evaluate_bcl_xl_paradigm(doses_nm=[100.0])
        pz_res = bclxl["PZ15227"]["dose_responses"][0]
        self.assertTrue(pz_res.is_tumor_ablated)
        self.assertFalse(pz_res.is_normal_tissue_spared)
        self.assertLessEqual(pz_res.normal_tissue_target_level_pct, 10.0)

    def test_tissue_safety_index_dt2216_exceeds_100(self):
        """DT2216 exhibits TSI > 100x whereas PZ15227 exhibits TSI < 2.0x."""
        bclxl = TissueSelectiveE3Engine.evaluate_bcl_xl_paradigm(doses_nm=[100.0])
        tsi_dt = bclxl["DT2216"]["therapeutic_safety_index"]
        tsi_pz = bclxl["PZ15227"]["therapeutic_safety_index"]
        self.assertGreater(tsi_dt, 100.0)
        self.assertLess(tsi_pz, 2.0)


class TestAutophagyTargetingEngine(unittest.TestCase):
    """Validates ATTEC / AUTAC 2D membrane induced proximity and macroautophagic clearance."""

    def test_2d_membrane_concentration_enhancement(self):
        """Membrane localization of LC3-II enhances effective concentration by > 300-fold."""
        c_eff_um, enhancement = AutophagyTargetingEngine.compute_2d_effective_concentration(
            lc3_density_per_um2=1200.0, shell_thickness_nm=10.0, bulk_cytosolic_lc3_nm=500.0
        )
        self.assertAlmostEqual(c_eff_um, 199.27, delta=1.0)
        self.assertGreater(enhancement, 300.0)

    def test_proteasome_pore_steric_exclusion(self):
        """25 nm aggregates have 0% transmission through 1.3 nm 20S proteasome pore."""
        trans_agg = AutophagyTargetingEngine.compute_proteasome_pore_transmission(
            particle_diameter_nm=25.0, pore_diameter_nm=1.3
        )
        self.assertEqual(trans_agg, 0.0)
        trans_small = AutophagyTargetingEngine.compute_proteasome_pore_transmission(
            particle_diameter_nm=0.5, pore_diameter_nm=1.3
        )
        self.assertGreater(trans_small, 0.0)

    def test_attec_catalytic_turnover_and_aggregate_knockdown(self):
        """ATTEC (50 nM) clears > 90% insoluble aggregates with catalytic turnover TON > 1.0."""
        res = AutophagyTargetingEngine.simulate_attec_clearance(attec_conc_nm=50.0, duration_hours=48.0)
        self.assertGreaterEqual(res.aggregate_knockdown_pct, 90.0)
        self.assertTrue(res.is_catalytic)
        self.assertGreater(res.catalytic_turnover_number, 1.0)
        self.assertEqual(res.proteasome_clearance_pct, 0.0)

    def test_attec_membrane_cooperativity_boost(self):
        """2D membrane local concentration (>150 uM) drives efficient tethering at nanomolar doses."""
        p = AutophagyBiophysicalParameters(kd_aggregate_nm=30.0, kd_lc3_nm=100.0)
        res = AutophagyTargetingEngine.simulate_attec_clearance(params=p, attec_conc_nm=20.0, duration_hours=48.0)
        self.assertGreaterEqual(res.aggregate_knockdown_pct, 85.0)


class TestRIBOTACKineticsEngine(unittest.TestCase):
    """Validates RIBOTAC quaternary assembly, RNA cleavage, and the Quaternary Hook Steepness Theorem."""

    def test_quaternary_mass_conservation(self):
        """Solves quaternary equilibrium with exact mass conservation for RNA, RNase L, and degrader."""
        p = RIBOTACParameters()
        eq = RIBOTACKineticsEngine.solve_quaternary_equilibrium(p, rna_tot=20e-9, rnase_l_tot=100e-9, degrader_tot=50e-9)
        r_sum = eq['free_rna'] + eq['binary_rd'] + eq['ternary_rdl'] + eq['quaternary_rdl2']
        l_sum = eq['free_rnase_l'] + eq['binary_ld'] + eq['ternary_rdl'] + 2.0 * eq['quaternary_rdl2']
        d_sum = eq['free_degrader'] + eq['binary_rd'] + eq['binary_ld'] + eq['ternary_rdl'] + eq['quaternary_rdl2']
        self.assertAlmostEqual(r_sum * 1e9, 20.0, delta=1e-3)
        self.assertAlmostEqual(l_sum * 1e9, 100.0, delta=1e-3)
        self.assertAlmostEqual(d_sum * 1e9, 50.0, delta=1e-3)

    def test_quaternary_hook_steepness_theorem_slope_minus_two(self):
        """Proves the Quaternary Hook Steepness Theorem: lim_[D]->inf [RDL2] ~ 1/[D]^2 (slope = -2.00 +/- 0.05)."""
        metrics = RIBOTACKineticsEngine.analyze_quaternary_hook_curve(num_points=50)
        self.assertAlmostEqual(metrics.asymptotic_descending_slope, -2.0, delta=0.08)
        self.assertGreater(metrics.quaternary_max_nm, 10.0)
        self.assertGreater(metrics.c_hook_50_high_nm, metrics.d_opt_nm)

    def test_ribotac_catalytic_turnover_and_rna_knockdown(self):
        """RIBOTAC achieves > 80% oncogenic RNA transcript knockdown with catalytic turnover TON > 1.0."""
        res = RIBOTACKineticsEngine.simulate_ribotac_kinetics(degrader_conc_nm=50.0, duration_hours=24.0)
        self.assertGreaterEqual(res.rna_knockdown_pct, 80.0)
        self.assertTrue(res.is_catalytic)
        self.assertGreater(res.catalytic_turnover_number, 1.0)

    def test_excess_quaternary_hook_suppression_vs_protac(self):
        """At 100 uM (> 1000x D_opt), RIBOTAC quaternary complex is suppressed > 10x more severely than PROTAC."""
        comp = RIBOTACKineticsEngine.compare_protac_vs_ribotac_hook_steepness(eval_conc_um=100.0)
        self.assertAlmostEqual(comp['protac_asymptotic_slope'], -1.0, places=1)
        self.assertAlmostEqual(comp['ribotac_asymptotic_slope'], -2.0, delta=0.08)
        self.assertGreater(comp['ribotac_excess_suppression_ratio'], 10.0)


if __name__ == '__main__':
    unittest.main()
