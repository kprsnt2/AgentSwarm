"""
Test Suite for KRAS Allostery & Covalent Inactivation Kinetics Engine
====================================================================
Comprehensive unittest suite verifying:
1. Biophysical constants, thermodynamic conversions, and enumerations.
2. Nucleotide cycling steady-state and transient relaxation ODEs across WT and mutants.
3. Covalent electrophile trapping kinetics (k_inact / K_I, k_obs, t_1/2, t_90).
4. Non-covalent allosteric pocket targeting, residence time, and state selectivity.
5. Tri-complex RAS(ON) molecular glue equilibria with Cyclophilin A.
6. Secondary resistance mutation thermodynamics (Delta Delta G) and differential profiling.
7. Mechanistic combination synergy with SOS1/SHP2 inhibitors (Bliss excess, Loewe CI, DRI).
8. Downstream MAPK pathway flux and RAF-RBD complex formation.
9. In vivo pharmacokinetics and multi-dose dynamic target coverage.
10. Master simulator reporting and boundary / edge case robustness.
"""

import math
import unittest
import numpy as np

from kras_allostery_kinetics_engine import (
    GAS_CONSTANT_KCAL,
    GAS_CONSTANT_R,
    PHYSIOLOGICAL_TEMP_K,
    NucleotideState,
    KRASVariant,
    InhibitorModality,
    ResistanceMutation,
    VariantKinetics,
    InhibitorParameters,
    ResistancePerturbation,
    STANDARD_VARIANT_KINETICS,
    STANDARD_INHIBITORS,
    RESISTANCE_DATABASE,
    get_variant_specific_inhibitor,
    KRASConformationalCycleEngine,
    AllostericConformationalCouplingEngine,
    CovalentInhibitionEngine,
    CovalentAspartateEngine,
    NonCovalentAllosteryEngine,
    SecondaryResistanceEngine,
    CombinationSynergyEngine,
    TriComplexRASONEngine,
    TriComplexHookAnalysisEngine,
    EffectorBindingParameters,
    MAPKPathwaySignalingEngine,
    DrugPKParameters,
    STANDARD_PK_PROFILES,
    PharmacokineticsDynamicsEngine,
    KRASClonalEvolutionEngine,
    KRASMasterSimulator,
    RASIsoform,
    STANDARD_ISOFORM_PROFILES,
    PanKRASvsPanRASTherapeuticWindowEngine,
    HydrationSite,
    STANDARD_SIIP_HYDRATION_SITES,
    CrypticPocketSolvationEngine,
    ExtendedOncogenicChemotypeEngine,
    MembraneNanoclusteringEngine,
)


class TestKRASAllosteryKinetics(unittest.TestCase):
    """Test suite for the biophysical KRAS allostery and kinetics engine."""

    # ========================================================================
    # 1. BIOPHYSICAL CONSTANTS & ENUMS
    # ========================================================================

    def test_constants_and_enums(self):
        """Verify standard physical constants and enum memberships."""
        self.assertAlmostEqual(GAS_CONSTANT_R, 8.31446, delta=1e-3)
        self.assertAlmostEqual(GAS_CONSTANT_KCAL, 1.9872e-3, delta=1e-4)
        self.assertAlmostEqual(PHYSIOLOGICAL_TEMP_K, 310.15, delta=0.01)

        self.assertEqual(NucleotideState.GDP.value, "GDP")
        self.assertEqual(NucleotideState.GTP.value, "GTP")

        self.assertEqual(KRASVariant.WT.value, "WT")
        self.assertEqual(KRASVariant.G12C.value, "G12C")
        self.assertEqual(KRASVariant.G12D.value, "G12D")
        self.assertEqual(KRASVariant.G12V.value, "G12V")
        self.assertEqual(KRASVariant.Q61H.value, "Q61H")

        self.assertEqual(InhibitorModality.COVALENT_SIIP.value, "COVALENT_SIIP")
        self.assertEqual(ResistanceMutation.Y96D.value, "Y96D")
        self.assertEqual(ResistanceMutation.H95D.value, "H95D")

    # ========================================================================
    # 2. VARIANT NUCLEOTIDE CYCLING & STEADY STATES
    # ========================================================================

    def test_wild_type_nucleotide_equilibrium(self):
        """Verify that WT KRAS is predominantly GDP-bound under physiological GAP activity."""
        wt_kinetics = STANDARD_VARIANT_KINETICS[KRASVariant.WT]
        f_gtp = wt_kinetics.steady_state_gtp_fraction(gap_activity=1.0, sos1_activity=1.0)
        f_gdp = wt_kinetics.steady_state_gdp_fraction(gap_activity=1.0, sos1_activity=1.0)

        # In normal physiology, GAP accelerates hydrolysis ~10^5 fold, keeping active GTP < 2%
        self.assertLess(f_gtp, 0.02)
        self.assertGreater(f_gdp, 0.98)
        self.assertAlmostEqual(f_gtp + f_gdp, 1.0, delta=1e-7)

    def test_oncogenic_mutant_steady_states(self):
        """Verify that oncogenic mutations impair hydrolysis and shift KRAS toward active GTP."""
        g12c = STANDARD_VARIANT_KINETICS[KRASVariant.G12C]
        g12d = STANDARD_VARIANT_KINETICS[KRASVariant.G12D]
        g12v = STANDARD_VARIANT_KINETICS[KRASVariant.G12V]
        q61h = STANDARD_VARIANT_KINETICS[KRASVariant.Q61H]

        f_gtp_g12c = g12c.steady_state_gtp_fraction()
        f_gtp_g12d = g12d.steady_state_gtp_fraction()
        f_gtp_g12v = g12v.steady_state_gtp_fraction()
        f_gtp_q61h = q61h.steady_state_gtp_fraction()

        # Hierarchy of GTP accumulation based on catalytic impairment
        # G12C retains moderate intrinsic/GAP hydrolysis -> ~60-75% GTP
        self.assertTrue(0.50 < f_gtp_g12c < 0.85)
        # G12D is more severely impaired -> > 95% GTP
        self.assertGreater(f_gtp_g12d, 0.95)
        # G12V beta-branched steric clash -> > 98% GTP
        self.assertGreater(f_gtp_g12v, 0.98)
        # Q61H catalytic water positioning abolished -> > 99% GTP
        self.assertGreater(f_gtp_q61h, 0.99)

    def test_conformational_cycle_engine_steady_state(self):
        """Verify cycle engine calculations and cycling turnover time."""
        engine = KRASConformationalCycleEngine(KRASVariant.G12C)
        ss = engine.compute_steady_state(gap_activity=1.0, sos1_activity=1.0)

        self.assertIn("f_gdp", ss)
        self.assertIn("f_gtp", ss)
        self.assertIn("cycle_turnover_time_seconds", ss)
        self.assertGreater(ss["cycle_turnover_time_seconds"], 0.0)
        self.assertAlmostEqual(ss["f_gdp"] + ss["f_gtp"], 1.0, delta=1e-6)
        self.assertAlmostEqual(ss["ratio_gtp_gdp"], ss["f_gtp"] / ss["f_gdp"], delta=1e-5)

    def test_transient_cycle_ode_convergence(self):
        """Verify that transient ODE relaxation converges to analytical steady state."""
        engine = KRASConformationalCycleEngine(KRASVariant.G12C)
        ss_analytical = engine.compute_steady_state()

        sim = engine.simulate_transient_cycle(
            initial_gtp_fraction=0.10,  # Far from steady state
            time_span_s=120.0,
            num_points=300,
        )

        final_gtp_fraction = sim["fraction_gtp"][-1]
        self.assertAlmostEqual(final_gtp_fraction, ss_analytical["f_gtp"], delta=1e-3)

    # ========================================================================
    # 3. COVALENT ELECTROPHILE TRAPPING KINETICS
    # ========================================================================

    def test_covalent_inhibitor_parameters(self):
        """Verify kinact/KI ratios for Sotorasib and Adagrasib against literature."""
        soto = STANDARD_INHIBITORS["Sotorasib"]
        adag = STANDARD_INHIBITORS["Adagrasib"]

        self.assertTrue(soto.is_covalent)
        self.assertTrue(adag.is_covalent)

        # Sotorasib: Canon et al. Nature 2019: kinact ~ 0.045 s^-1, KI ~ 1.7 uM -> ~26,470 M^-1 s^-1
        self.assertAlmostEqual(soto.k_inact_over_ki, 0.045 / 1.7e-6, delta=100.0)
        self.assertTrue(2.0e4 < soto.k_inact_over_ki < 3.5e4)

        # Adagrasib: Hallin et al. Cancer Discov 2020: kinact ~ 0.026 s^-1, KI ~ 0.35 uM -> ~74,285 M^-1 s^-1
        self.assertAlmostEqual(adag.k_inact_over_ki, 0.026 / 3.5e-7, delta=100.0)
        self.assertTrue(5.0e4 < adag.k_inact_over_ki < 1.0e5)

    def test_covalent_apparent_kobs_and_half_life(self):
        """Verify apparent k_obs, half-life, and time-to-90% inactivation calculations."""
        soto = STANDARD_INHIBITORS["Sotorasib"]
        engine = CovalentInhibitionEngine(soto, STANDARD_VARIANT_KINETICS[KRASVariant.G12C])

        # Zero dose should yield zero k_obs and infinite half life
        self.assertEqual(engine.calculate_apparent_kobs(0.0), 0.0)
        self.assertEqual(engine.calculate_half_life_of_inactivation_s(0.0), float("inf"))

        # At 1.0 uM
        k_obs_1um = engine.calculate_apparent_kobs(1.0e-6)
        self.assertGreater(k_obs_1um, 0.0)

        t_half_1um = engine.calculate_half_life_of_inactivation_s(1.0e-6)
        expected_thalf = math.log(2.0) / k_obs_1um
        self.assertAlmostEqual(t_half_1um, expected_thalf, delta=1e-5)

        t_90 = engine.calculate_time_to_target_inactivation_s(0.90, 1.0e-6)
        expected_t90 = math.log(10.0) / k_obs_1um
        self.assertAlmostEqual(t_90, expected_t90, delta=1e-5)

    def test_covalent_trapping_ode_simulation(self):
        """Verify full numerical ODE simulation of irreversible covalent trapping."""
        soto = STANDARD_INHIBITORS["Sotorasib"]
        engine = CovalentInhibitionEngine(soto, STANDARD_VARIANT_KINETICS[KRASVariant.G12C])

        sim = engine.simulate_covalent_inactivation(
            inhibitor_conc_m=1.0e-6,
            total_kras_m=1.0e-6,
            time_span_s=3600.0,
            num_points=500,
        )

        # Inactivated fraction should monotonically increase from 0 to near 1
        inactivated = sim["fraction_inactivated"]
        self.assertEqual(inactivated[0], 0.0)
        self.assertGreater(inactivated[-1], 0.99)
        self.assertTrue(np.all(np.diff(inactivated) >= -1e-12))

        # Active GTP fraction should drop near zero
        self.assertLess(sim["fraction_active_gtp"][-1], 0.01)

    # ========================================================================
    # 4. NON-COVALENT ALLOSTERY & SELECTIVITY (MRTX1133 / BI-2865)
    # ========================================================================

    def test_mrtx1133_picomolar_affinity_and_residence_time(self):
        """Verify MRTX1133 picomolar GDP-state affinity and target residence time."""
        mrtx = STANDARD_INHIBITORS["MRTX1133"]
        self.assertFalse(mrtx.is_covalent)
        self.assertAlmostEqual(mrtx.kd_gdp, 0.20e-9, delta=1e-12)
        self.assertAlmostEqual(mrtx.kd_gtp, 43.0e-9, delta=1e-11)

        # Residence time on KRAS G12D-GDP: t_R = 1 / k_off
        expected_tr_sec = 1.0 / (mrtx.kd_gdp * mrtx.k_on)
        self.assertAlmostEqual(mrtx.residence_time_gdp_seconds, expected_tr_sec, delta=1e-5)
        self.assertGreater(mrtx.residence_time_gdp_minutes, 10.0)  # Long residence time

    def test_mrtx1133_equilibrium_occupancy(self):
        """Verify equilibrium occupancy across cycling G12D system."""
        mrtx = STANDARD_INHIBITORS["MRTX1133"]
        engine = NonCovalentAllosteryEngine(mrtx, STANDARD_VARIANT_KINETICS[KRASVariant.G12D])

        kd_app = engine.apparent_equilibrium_kd()
        self.assertGreater(kd_app, mrtx.kd_gdp)  # Shifted by conformational partitioning

        # At 1.0 uM, occupancy should be high (>98%)
        occ_1um = engine.equilibrium_fractional_occupancy(1.0e-6)
        self.assertGreater(occ_1um, 0.98)

    def test_variant_specific_inhibitor_adaptation(self):
        """Verify that covalent and non-covalent drugs correctly adapt to mutant biochemistry."""
        soto_base = STANDARD_INHIBITORS["Sotorasib"]
        mrtx_base = STANDARD_INHIBITORS["MRTX1133"]

        # Sotorasib on G12C has kinact > 0; on G12D or WT, kinact is 0
        soto_g12c = get_variant_specific_inhibitor(soto_base, KRASVariant.G12C)
        soto_g12d = get_variant_specific_inhibitor(soto_base, KRASVariant.G12D)
        soto_wt = get_variant_specific_inhibitor(soto_base, KRASVariant.WT)

        self.assertTrue(soto_g12c.is_covalent)
        self.assertFalse(soto_g12d.is_covalent)
        self.assertFalse(soto_wt.is_covalent)
        self.assertEqual(soto_g12d.k_inact, 0.0)
        self.assertGreaterEqual(soto_g12d.kd_gdp, 5.0e-5)

        # MRTX1133 on G12D has 0.2 nM Kd; on WT or G12C, Kd is 750-fold weaker (150 nM)
        mrtx_g12d = get_variant_specific_inhibitor(mrtx_base, KRASVariant.G12D)
        mrtx_wt = get_variant_specific_inhibitor(mrtx_base, KRASVariant.WT)
        mrtx_g12c = get_variant_specific_inhibitor(mrtx_base, KRASVariant.G12C)

        self.assertAlmostEqual(mrtx_g12d.kd_gdp, 0.2e-9, delta=1e-12)
        self.assertAlmostEqual(mrtx_wt.kd_gdp, 1.5e-7, delta=1e-10)
        self.assertAlmostEqual(mrtx_g12c.kd_gdp, 1.5e-7, delta=1e-10)
        self.assertAlmostEqual(mrtx_wt.kd_gdp / mrtx_g12d.kd_gdp, 750.0, places=4)

    # ========================================================================
    # 5. TRI-COMPLEX RAS(ON) ENGINE (RMC-6236)
    # ========================================================================

    def test_tricomplex_rason_equilibria(self):
        """Verify Cyclophilin A ternary complex equilibria for active KRAS:GTP."""
        rason = STANDARD_INHIBITORS["RMC-6236"]
        self.assertEqual(rason.modality, InhibitorModality.TRICOMPLEX_RASON)

        engine = TriComplexRASONEngine(rason, STANDARD_VARIANT_KINETICS[KRASVariant.G12D])
        eq = engine.solve_ternary_complex_equilibrium(drug_conc_m=1.0e-6, kras_gtp_conc_m=1.0e-6)

        self.assertGreater(eq["ternary_complex_m"], 0.0)
        self.assertGreater(eq["fraction_effector_occluded"], 0.90)
        self.assertLess(eq["cypa_free_m"], engine.cypa_total)
        self.assertLess(eq["kras_gtp_free_m"], 1.0e-6)

    # ========================================================================
    # 6. SECONDARY RESISTANCE MUTATIONS & THERMODYNAMICS
    # ========================================================================

    def test_secondary_resistance_thermodynamic_penalty(self):
        """Verify Delta Delta G calculation from fold shift."""
        ddg_10x = SecondaryResistanceEngine.calculate_free_energy_penalty(10.0)
        expected_ddg = GAS_CONSTANT_KCAL * PHYSIOLOGICAL_TEMP_K * math.log(10.0)
        self.assertAlmostEqual(ddg_10x, expected_ddg, delta=1e-5)
        self.assertTrue(1.35 < ddg_10x < 1.45)  # ~1.4 kcal/mol per decade shift at 37 C

    def test_differential_resistance_h95d(self):
        """Verify that H95D confers selective resistance to Adagrasib while sparing Sotorasib."""
        soto = STANDARD_INHIBITORS["Sotorasib"]
        adag = STANDARD_INHIBITORS["Adagrasib"]

        soto_h95d = SecondaryResistanceEngine.get_mutated_inhibitor(soto, ResistanceMutation.H95D)
        adag_h95d = SecondaryResistanceEngine.get_mutated_inhibitor(adag, ResistanceMutation.H95D)

        soto_fold = soto_h95d.kd_gdp / soto.kd_gdp
        adag_fold = adag_h95d.kd_gdp / adag.kd_gdp

        self.assertLessEqual(soto_fold, 2.5)    # Minor impact; Sotorasib remains active
        self.assertGreaterEqual(adag_fold, 100.0) # Severe clinical resistance to Adagrasib

    def test_cross_resistance_y96d(self):
        """Verify that Y96D confers severe cross-resistance to Sotorasib, Adagrasib, and MRTX1133."""
        soto = STANDARD_INHIBITORS["Sotorasib"]
        adag = STANDARD_INHIBITORS["Adagrasib"]
        mrtx = STANDARD_INHIBITORS["MRTX1133"]

        soto_y96d = SecondaryResistanceEngine.get_mutated_inhibitor(soto, ResistanceMutation.Y96D)
        adag_y96d = SecondaryResistanceEngine.get_mutated_inhibitor(adag, ResistanceMutation.Y96D)
        mrtx_y96d = SecondaryResistanceEngine.get_mutated_inhibitor(mrtx, ResistanceMutation.Y96D)

        self.assertGreater(soto_y96d.kd_gdp / soto.kd_gdp, 400.0)
        self.assertGreater(adag_y96d.kd_gdp / adag.kd_gdp, 300.0)
        self.assertGreater(mrtx_y96d.kd_gdp / mrtx.kd_gdp, 200.0)

    def test_nucleophile_loss_c12f(self):
        """Verify that C12F completely abolishes the covalent inactivation mechanism."""
        soto = STANDARD_INHIBITORS["Sotorasib"]
        soto_c12f = SecondaryResistanceEngine.get_mutated_inhibitor(soto, ResistanceMutation.C12F)

        self.assertEqual(soto_c12f.k_inact, 0.0)
        self.assertFalse(soto_c12f.is_covalent)
        self.assertEqual(soto_c12f.k_inact_over_ki, 0.0)

    # ========================================================================
    # 7. COMBINATION SYNERGY ENGINE (SOS1 / BI-3406)
    # ========================================================================

    def test_combination_synergy_with_sos1(self):
        """Verify that SOS1 inhibition synergizes with Sotorasib (Bliss excess > 0, CI < 1.0)."""
        soto = STANDARD_INHIBITORS["Sotorasib"]
        c_eng = CovalentInhibitionEngine(soto, STANDARD_VARIANT_KINETICS[KRASVariant.G12C])
        combo_eng = CombinationSynergyEngine(c_eng)

        metrics = combo_eng.evaluate_sos1_combination(
            kras_dose_m=1.0e-7,
            sos1_dose_m=5.0e-8,
            exposure_time_s=1800.0,
        )

        # Combination inhibition must exceed single-agent alone
        self.assertGreater(metrics.combination_inhibition, metrics.single_agent_kras_inhibition)
        self.assertGreater(metrics.combination_inhibition, metrics.single_agent_partner_inhibition)

        # Synergy verification
        self.assertGreater(metrics.bliss_excess, 0.0)
        self.assertLess(metrics.combination_index_loewe, 1.0)
        self.assertGreater(metrics.dose_reduction_index_kras, 1.0)

    # ========================================================================
    # 8. EFFECTOR BINDING & MAPK PATHWAY FLUX
    # ========================================================================

    def test_mapk_effector_and_perk(self):
        """Verify RAF-RBD complex binding and phospho-ERK calculation."""
        mapk_eng = MAPKPathwaySignalingEngine()

        # Binding calculation at high free KRAS-GTP (1 uM)
        comp, frac = mapk_eng.compute_raf_complex(1.0e-6)
        self.assertGreater(comp, 0.0)
        self.assertTrue(0.0 < frac <= 1.0)

        # At zero free KRAS-GTP, complex and pERK should be 0
        comp_zero, frac_zero = mapk_eng.compute_raf_complex(0.0)
        self.assertEqual(comp_zero, 0.0)
        self.assertEqual(frac_zero, 0.0)
        self.assertEqual(mapk_eng.compute_perk_signal(0.0), 0.0)

        # Monotonicity check
        perk_low = mapk_eng.compute_perk_signal(1.0e-8)
        perk_med = mapk_eng.compute_perk_signal(1.0e-7)
        perk_high = mapk_eng.compute_perk_signal(1.0e-6)
        self.assertTrue(perk_low < perk_med < perk_high)

    # ========================================================================
    # 9. PHARMACOKINETICS & DYNAMIC TARGET COVERAGE
    # ========================================================================

    def test_pk_elimination_and_half_life(self):
        """Verify elimination rates and half-lives for clinical profiles."""
        soto_pk = STANDARD_PK_PROFILES["Sotorasib"]
        adag_pk = STANDARD_PK_PROFILES["Adagrasib"]

        self.assertAlmostEqual(soto_pk.half_life_hours, 5.5, delta=0.2)
        self.assertAlmostEqual(adag_pk.half_life_hours, 24.0, delta=0.5)

    def test_pk_dynamic_24h_simulation(self):
        """Verify 24-hour simulation of PK clearance coupled to irreversible target trapping."""
        soto_pk = STANDARD_PK_PROFILES["Sotorasib"]
        pk_eng = PharmacokineticsDynamicsEngine(soto_pk)
        soto_inh = STANDARD_INHIBITORS["Sotorasib"]

        res = pk_eng.simulate_24h_dynamic_profile(
            inhibitor_params=soto_inh,
            time_span_hours=24.0,
            num_points=100,
        )

        self.assertIn("time_hours", res)
        self.assertIn("drug_concentration_m", res)
        self.assertIn("fraction_inactivated", res)
        self.assertGreater(res["fraction_inactivated"][-1], 0.90)

    # ========================================================================
    # 10. MASTER SIMULATOR & COMPREHENSIVE REPORTING
    # ========================================================================

    def test_master_simulator_all_variants(self):
        """Verify that KRASMasterSimulator generates reports for all 5 variants without error."""
        for variant in [KRASVariant.WT, KRASVariant.G12C, KRASVariant.G12D, KRASVariant.G12V, KRASVariant.Q61H]:
            sim = KRASMasterSimulator(variant)
            report = sim.generate_comprehensive_report()
            self.assertIn(variant.value, report)
            self.assertIn("INHIBITOR BENCHMARK PERFORMANCE", report)

            profiles = sim.profile_inhibitor_panel(dose_m=1.0e-6, time_s=1800.0)
            self.assertEqual(len(profiles), len(STANDARD_INHIBITORS))
            for p in profiles:
                self.assertIn("inhibitor", p)
                self.assertIn("target_engagement_percent", p)
                self.assertTrue(0.0 <= p["target_engagement_percent"] <= 100.0)

    def test_edge_cases_and_error_handling(self):
        """Verify handling of invalid parameters and boundary values."""
        # Negative rates should raise ValueError
        with self.assertRaises(ValueError):
            VariantKinetics(KRASVariant.WT, k_hyd_int=-1.0, k_hyd_gap=1.0, k_exch_int=1.0, k_exch_sos1=1.0)

        # Negative Kd should raise ValueError
        with self.assertRaises(ValueError):
            InhibitorParameters("Invalid", InhibitorModality.COVALENT_SIIP, kd_gdp=-1.0, kd_gtp=1.0)

        # Target fraction out of bounds
        soto = STANDARD_INHIBITORS["Sotorasib"]
        cov_eng = CovalentInhibitionEngine(soto, STANDARD_VARIANT_KINETICS[KRASVariant.G12C])
        with self.assertRaises(ValueError):
            cov_eng.calculate_time_to_target_inactivation_s(1.5, 1.0e-6)

    # ========================================================================
    # 11. ALLOSTERIC CONFORMATIONAL COUPLING & POCKET GATING
    # ========================================================================

    def test_allosteric_conformational_coupling(self):
        """Verify thermodynamic pocket opening constants, probabilities, and GTP clamp penalty."""
        engine = AllostericConformationalCouplingEngine(
            delta_g_open_gdp_kcal=0.88,
            delta_delta_g_gtp_clamp_kcal=5.57,
        )

        k_open_gdp = engine.pocket_opening_equilibrium_constant(NucleotideState.GDP)
        k_open_gtp = engine.pocket_opening_equilibrium_constant(NucleotideState.GTP)

        # In GDP state, K_open ~ 0.24 (p ~ 19%)
        self.assertAlmostEqual(k_open_gdp, 0.24, delta=0.03)
        p_open_gdp = engine.pocket_open_probability(NucleotideState.GDP)
        self.assertAlmostEqual(p_open_gdp, 0.193, delta=0.03)

        # In GTP state, K_open is heavily penalized by ~5.57 kcal/mol clamp (~2.8e-5)
        self.assertLess(k_open_gtp, 1.0e-4)
        p_open_gtp = engine.pocket_open_probability(NucleotideState.GTP)
        self.assertLess(p_open_gtp, 1.0e-4)

        # Allosteric selectivity ratio > 8,000-fold
        ratio = engine.calculate_allosteric_selectivity_ratio()
        self.assertGreater(ratio, 8000.0)

        # Apparent Kd with conformational penalty
        kd_intr = 3.0e-7  # 300 nM
        kd_app_gdp = engine.apparent_kd_with_conformational_penalty(kd_intr, NucleotideState.GDP)
        kd_app_gtp = engine.apparent_kd_with_conformational_penalty(kd_intr, NucleotideState.GTP)
        self.assertAlmostEqual(kd_app_gdp * 1e6, 1.55, delta=0.2)  # ~1.55 uM
        self.assertGreater(kd_app_gtp, 1.0e-3)                     # > 1 mM

    # ========================================================================
    # 12. COVALENT ASPARTATE-DIRECTED KINETICS & STRAIN RELEASE
    # ========================================================================

    def test_covalent_aspartate_kinetics_and_strain_release(self):
        """Verify transition-state activation free energies and G12D covalent trapping."""
        malo_inh = STANDARD_INHIBITORS["Malolactone-G12D"]
        g12d_kin = STANDARD_VARIANT_KINETICS[KRASVariant.G12D]
        asp_eng = CovalentAspartateEngine(malo_inh, g12d_kin)

        # Barrier comparisons: Cys (~19.8 kcal/mol) vs unstrained Asp (~28.5) vs strain-relieved (~20.2)
        dg_cys = asp_eng.calculate_activation_free_energy_barrier("Cys")
        dg_asp_unstrained = asp_eng.calculate_activation_free_energy_barrier("Asp", has_ring_strain=False)
        dg_asp_strained = asp_eng.calculate_activation_free_energy_barrier("Asp", has_ring_strain=True)

        self.assertAlmostEqual(dg_cys, 19.8, delta=0.1)
        self.assertAlmostEqual(dg_asp_unstrained, 28.5, delta=0.1)
        self.assertAlmostEqual(dg_asp_strained, 20.2, delta=0.1)

        # Eyring Polanyi theoretical kinact: strained Asp gives kinact ~ 0.01 - 0.05 s^-1
        theo_kinact = asp_eng.calculate_theoretical_kinact(dg_asp_strained)
        self.assertGreater(theo_kinact, 0.005)
        self.assertLess(theo_kinact, 0.10)

        # Apparent k_obs and t_half in cycling system
        k_obs = asp_eng.calculate_apparent_kobs(1.0e-5)  # 10 uM
        self.assertGreater(k_obs, 0.0)
        t_half = asp_eng.calculate_half_life_of_inactivation_s(1.0e-5)
        self.assertLess(t_half, 10000.0)

        # Simulation of RMC-9805 (covalent G12D:GTP tri-complex)
        rmc9805_inh = STANDARD_INHIBITORS["RMC-9805"]
        rmc_asp_eng = CovalentAspartateEngine(rmc9805_inh, g12d_kin)
        sim_rmc = rmc_asp_eng.simulate_covalent_inactivation(1.0e-6, time_span_s=1800.0)
        self.assertIn("fraction_inactivated", sim_rmc)
        self.assertGreater(sim_rmc["fraction_inactivated"][-1], 0.90)

    # ========================================================================
    # 13. THERMODYNAMIC CYCLE DECOMPOSITION (NAGARJUNA A004 CONSILIENCE)
    # ========================================================================

    def test_nagarjuna_thermodynamic_cycle_decomposition(self):
        """Verify thermodynamic cycle FEP energy decomposition matching Nagarjuna (A004)."""
        decomp_soto_y96d = SecondaryResistanceEngine.decompose_free_energy_components(
            "Sotorasib", ResistanceMutation.Y96D
        )
        self.assertAlmostEqual(decomp_soto_y96d["total_ddg_kcal"], 3.98, delta=0.01)
        self.assertAlmostEqual(decomp_soto_y96d["vdw_ddg_kcal"], 1.85, delta=0.01)
        self.assertAlmostEqual(decomp_soto_y96d["coulombic_ddg_kcal"], -2.79, delta=0.01)
        self.assertAlmostEqual(decomp_soto_y96d["desolvation_ddg_kcal"], 4.92, delta=0.01)

        # H95D: Adagrasib loses H-bond (+3.04 kcal/mol) while Sotorasib is spared (+0.46 kcal/mol)
        decomp_adag_h95d = SecondaryResistanceEngine.decompose_free_energy_components(
            "Adagrasib", ResistanceMutation.H95D
        )
        decomp_soto_h95d = SecondaryResistanceEngine.decompose_free_energy_components(
            "Sotorasib", ResistanceMutation.H95D
        )
        self.assertAlmostEqual(decomp_adag_h95d["total_ddg_kcal"], 3.04, delta=0.01)
        self.assertAlmostEqual(decomp_soto_h95d["total_ddg_kcal"], 0.46, delta=0.01)
        self.assertGreater(decomp_adag_h95d["reorganization_ddg_kcal"], 2.0)

    # ========================================================================
    # 14. HOOK EFFECT RESISTANCE (KEPLER A001 CONSILIENCE)
    # ========================================================================

    def test_kepler_hook_effect_resistance_comparison(self):
        """Verify that Tri-Complex glues resist Hook suppression >1000-fold vs PROTACs."""
        hook_eng = TriComplexHookAnalysisEngine(
            cypa_conc_m=5.0e-6,
            vhl_conc_m=1.4e-7,
            kras_target_conc_m=1.0e-6,
        )

        # At high therapeutic concentration (10 uM):
        # Classical PROTAC ternary complex severely suppressed
        frac_protac_high = hook_eng.compute_protac_ternary_fraction(1.0e-5)
        # Tri-complex molecular glue remains high
        frac_glue_high = hook_eng.compute_tricomplex_ternary_fraction(1.0e-5)

        self.assertLess(frac_protac_high, 0.15)
        self.assertGreater(frac_glue_high, 0.85)

        # Fold resistance to hook suppression > 5x to > 1000x depending on PROTAC squelching
        ratio = hook_eng.evaluate_hook_suppression_ratio(1.0e-5)
        self.assertGreater(ratio, 5.0)

    # ========================================================================
    # 15. DARWINIAN CLONAL EVOLUTION & RESISTANCE PROGRESSION
    # ========================================================================

    def test_kras_clonal_evolution_and_progression(self):
        """Verify longitudinal tumor clonal dynamics under monotherapy vs combination therapy."""
        evo_eng = KRASClonalEvolutionEngine(
            initial_tumor_cells=1.0e9,
            growth_rate_per_day=0.03,
            carrying_capacity=5.0e10,
        )

        # Sotorasib monotherapy: relapses at ~180 days with Y96D / RTK bypass dominance
        sim_mono = evo_eng.simulate_treatment_regimen("Sotorasib_monotherapy", duration_days=365.0)
        self.assertIn("time_to_progression_days", sim_mono)
        self.assertLess(sim_mono["time_to_progression_days"], 250.0)
        self.assertIn(sim_mono["dominant_clone_at_end"], ["Y96D", "RTK_Bypass"])

        # Triplet combination (Sotorasib + SOS1 + Cetuximab): delays progression >340 days
        sim_triplet = evo_eng.simulate_treatment_regimen("Triplet_Soto_SOS1_Cetux", duration_days=365.0)
        self.assertGreater(sim_triplet["time_to_progression_days"], 340.0)

    # ========================================================================
    # 16. VARIANT SPECIFICITY FOR NOVEL INHIBITORS
    # ========================================================================

    def test_variant_specificity_for_new_inhibitors(self):
        """Verify that Malolactone-G12D and RMC-9805 are allele-specific for G12D."""
        malo = STANDARD_INHIBITORS["Malolactone-G12D"]
        rmc9805 = STANDARD_INHIBITORS["RMC-9805"]

        # Against G12D: fully active covalent warhead
        malo_g12d = get_variant_specific_inhibitor(malo, KRASVariant.G12D)
        rmc_g12d = get_variant_specific_inhibitor(rmc9805, KRASVariant.G12D)
        self.assertGreater(malo_g12d.k_inact, 0.0)
        self.assertGreater(rmc_g12d.k_inact, 0.0)

        # Against G12C: lack of Asp12 abolishes covalent reaction
        malo_g12c = get_variant_specific_inhibitor(malo, KRASVariant.G12C)
        rmc_g12c = get_variant_specific_inhibitor(rmc9805, KRASVariant.G12C)
        self.assertEqual(malo_g12c.k_inact, 0.0)
        self.assertEqual(rmc_g12c.k_inact, 0.0)

    # ========================================================================
    # 17. PAN-KRAS VS PAN-RAS ISOFORM SELECTIVITY & THERAPEUTIC WINDOW
    # ========================================================================

    def test_pan_kras_vs_pan_ras_therapeutic_window(self):
        """Verify that BI-2865 achieves wide therapeutic index (>50x) while Pan-RAS has narrow window (~4x)."""
        engine = PanKRASvsPanRASTherapeuticWindowEngine()

        # Check isoform profiles
        self.assertEqual(STANDARD_ISOFORM_PROFILES[RASIsoform.KRAS].residue_95, "His95")
        self.assertEqual(STANDARD_ISOFORM_PROFILES[RASIsoform.NRAS].residue_95, "Gln95")
        self.assertAlmostEqual(
            STANDARD_ISOFORM_PROFILES[RASIsoform.NRAS].delta_delta_g_bi2865_kcal, 2.74, delta=0.05
        )
        self.assertAlmostEqual(
            STANDARD_ISOFORM_PROFILES[RASIsoform.HRAS].delta_delta_g_bi2865_kcal, 2.86, delta=0.05
        )

        # Occupancy at 10 nM: BI-2865 engages 50% KRAS, but <2% NRAS and HRAS
        occ_bi = engine.calculate_isoform_occupancy("BI-2865", 10.0e-9)
        self.assertAlmostEqual(occ_bi[RASIsoform.KRAS], 0.50, delta=0.01)
        self.assertLess(occ_bi[RASIsoform.NRAS], 0.02)
        self.assertLess(occ_bi[RASIsoform.HRAS], 0.02)

        # RMC-6236 engages all three equipotently
        occ_rmc = engine.calculate_isoform_occupancy("RMC-6236", 5.0e-9)
        self.assertAlmostEqual(occ_rmc[RASIsoform.KRAS], 0.50, delta=0.01)
        self.assertAlmostEqual(occ_rmc[RASIsoform.NRAS], 0.50, delta=0.01)
        self.assertAlmostEqual(occ_rmc[RASIsoform.HRAS], 0.50, delta=0.01)

        # Therapeutic window comparison
        win_bi = engine.compute_therapeutic_window("BI-2865")
        win_rmc = engine.compute_therapeutic_window("RMC-6236")

        self.assertGreater(win_bi["therapeutic_index"], 50.0)
        self.assertLess(win_rmc["therapeutic_index"], 10.0)
        self.assertAlmostEqual(win_rmc["therapeutic_index"], 4.0, delta=0.5)

    # ========================================================================
    # 18. CRYPTIC POCKET SOLVATION & INHOMOGENEOUS WATER THERMODYNAMICS
    # ========================================================================

    def test_cryptic_pocket_solvation_thermodynamics(self):
        """Verify water displacement thermodynamics in Switch II pocket opening."""
        solv_eng = CrypticPocketSolvationEngine()

        # 5 discrete trapped hydration sites total +7.15 kcal/mol excess free energy
        total_excess = solv_eng.total_excess_solvation_free_energy()
        self.assertAlmostEqual(total_excess, 7.15, delta=0.01)

        # Displacing all 5 waters releases -7.15 kcal/mol
        disp_mrtx = solv_eng.calculate_displacement_free_energy("MRTX1133")
        self.assertEqual(disp_mrtx["waters_displaced_count"], 5)
        self.assertAlmostEqual(disp_mrtx["delta_g_displacement_kcal"], -7.15, delta=0.01)

        # Sotorasib displaces 4 waters
        disp_soto = solv_eng.calculate_displacement_free_energy("Sotorasib")
        self.assertEqual(disp_soto["waters_displaced_count"], 4)
        self.assertAlmostEqual(disp_soto["delta_g_displacement_kcal"], -6.15, delta=0.01)

        # Net pocket adaptation free energy:
        # GDP state: +0.88 - 7.15 = -6.27 kcal/mol (spontaneous pocket stabilization)
        net_gdp = solv_eng.net_pocket_adaptation_free_energy(NucleotideState.GDP, "MRTX1133")
        self.assertTrue(net_gdp["pocket_formation_spontaneous"])
        self.assertAlmostEqual(net_gdp["delta_g_pocket_net_kcal"], -6.27, delta=0.01)

        # GTP state: +6.45 - 7.15 = -0.70 kcal/mol (clamp penalty delta_delta_G = 5.57 kcal/mol)
        net_gtp = solv_eng.net_pocket_adaptation_free_energy(NucleotideState.GTP, "MRTX1133")
        delta_delta_g = net_gtp["delta_g_pocket_net_kcal"] - net_gdp["delta_g_pocket_net_kcal"]
        self.assertAlmostEqual(delta_delta_g, 5.57, delta=0.01)

    # ========================================================================
    # 19. EXTENDED ONCOGENIC CHEMOTYPES (G12S SuFEx, G12V, Q61H)
    # ========================================================================

    def test_extended_oncogenic_chemotypes(self):
        """Verify SuFEx targeting of G12S, non-covalent G12V, and Q61H lock."""
        chem_eng = ExtendedOncogenicChemotypeEngine()

        # G12S SuFEx simulation: 10 uM in 2 hours achieves >90% inactivation
        sufex_res = chem_eng.simulate_sufex_g12s_inactivation(dose_m=10.0e-6, time_span_s=7200.0)
        self.assertAlmostEqual(sufex_res["covalent_efficiency_m_s"], 241.38, delta=1.0)
        self.assertGreater(sufex_res["final_inactivation_percent"], 90.0)
        self.assertLess(sufex_res["t_half_minutes"], 25.0)

        # G12V comparison: RMC-6236 RAS(ON) achieves higher occupancy than BI-2865
        g12v_res = chem_eng.compare_g12v_targeting_modalities(dose_m=1.0e-6)
        self.assertGreater(g12v_res["rmc6236_occupancy_percent"], 98.0)
        self.assertEqual(g12v_res["optimal_modality"], "RMC-6236 (Tri-complex RAS(ON))")

        # Q61H lock failure: S-IIP inhibitors suffer 38-fold affinity penalty
        q61h_res = chem_eng.evaluate_q61h_lock_failure(dose_m=1.0e-6)
        self.assertLess(q61h_res["siip_inhibitor_occupancy_percent"], 80.0)
        self.assertGreater(q61h_res["rason_glue_occupancy_percent"], 99.0)

    # ========================================================================
    # 20. MEMBRANE NANOCLUSTERING & ALLOSTERIC DIMERIZATION BLOCKADE
    # ========================================================================

    def test_membrane_nanoclustering_and_dimerization(self):
        """Verify that S-IIP pocket occupancy allosterically disrupts alpha4-alpha5 dimerization."""
        mem_eng = MembraneNanoclusteringEngine()

        # Occupancy of 80% shifts dimerization Kd by >5-fold
        shift_res = mem_eng.compute_dimerization_affinity_shift(0.80)
        self.assertGreater(shift_res["dimerization_fold_shift"], 5.0)
        self.assertGreater(shift_res["dimerization_suppression_percent"], 80.0)

        # Full occupancy (0.80) suppresses RAF dimer activation beyond monomer reduction
        raf_res = mem_eng.compute_effective_raf_activation(inhibitor_occupancy=0.80, gtp_fraction=1.0)
        self.assertLess(raf_res["relative_raf_dimer_activation"], 0.05)
        self.assertGreater(raf_res["allosteric_dimer_bonus_inhibition"], 0.15)

    # ========================================================================
    # 21. TARGET RESYNTHESIS & DE NOVO TURNOVER DYNAMICS
    # ========================================================================

    def test_kras_resynthesis_and_target_turnover(self):
        """Verify KRAS de novo synthesis, protein turnover, and pulsatile trough recovery."""
        from kras_allostery_kinetics_engine import (
            KRASResynthesisTargetTurnoverEngine,
            STANDARD_INHIBITORS,
            STANDARD_VARIANT_KINETICS,
            STANDARD_PK_PROFILES,
            KRASVariant,
        )

        turnover_eng = KRASResynthesisTargetTurnoverEngine(kras_half_life_hours=24.0, baseline_kras_conc_um=1.0)
        self.assertAlmostEqual(turnover_eng.k_deg_per_hour, 0.02888, delta=0.001)
        self.assertAlmostEqual(turnover_eng.compute_steady_state_uninhibited(), 1.0, delta=1e-5)

        # Washout recovery follows exact analytical exponential kinetics
        washout_sim = turnover_eng.simulate_washout_recovery(washout_hours=48.0)
        self.assertAlmostEqual(washout_sim["recovery_fraction_at_24h"], 0.50, delta=0.001)
        self.assertAlmostEqual(washout_sim["recovery_fraction"][-1], 0.75, delta=0.001)

        kin_g12c = STANDARD_VARIANT_KINETICS[KRASVariant.G12C]

        # Sotorasib: 960 mg QD (24 h interval, short t1/2 = 5.5 h)
        soto_sim = turnover_eng.simulate_pulsatile_regimen(
            inhibitor=STANDARD_INHIBITORS["Sotorasib"],
            kinetics=kin_g12c,
            pk_params=STANDARD_PK_PROFILES["Sotorasib"],
            dose_mg=960.0,
            interval_hours=24.0,
            num_doses=7,
        )
        # Peak target engagement exceeds 90%
        self.assertGreater(soto_sim["steady_state_peak_occupancy_percent"], 90.0)
        # Sotorasib trough drug conc drops below 0.3 uM
        self.assertLess(soto_sim["drug_plasma_conc_um"][-1], 0.30)

        # Adagrasib: 600 mg BID (12 h interval, long t1/2 = 23.0 h)
        ada_sim = turnover_eng.simulate_pulsatile_regimen(
            inhibitor=STANDARD_INHIBITORS["Adagrasib"],
            kinetics=kin_g12c,
            pk_params=STANDARD_PK_PROFILES["Adagrasib"],
            dose_mg=600.0,
            interval_hours=12.0,
            num_doses=14,
        )
        # Adagrasib maintains high sustained trough drug concentration (>4.0 uM, ~19x higher than Sotorasib)
        self.assertGreater(ada_sim["drug_plasma_conc_um"][-1], 4.0)
        # Adagrasib suppresses free apo KRAS lower than Sotorasib
        self.assertLess(
            ada_sim["steady_state_trough_free_kras_um"],
            soto_sim["steady_state_trough_free_kras_um"],
        )

    # ========================================================================
    # 22. TRI-COMPLEX SIGNALOSOME STERIC CLASH
    # ========================================================================

    def test_tricomplex_signalosome_steric_clash(self):
        """Verify macromolecular clash between Cyclophilin A and 14-3-3:RAF signalosome."""
        from kras_allostery_kinetics_engine import TriComplexSignalosomeStericClashEngine

        clash_eng = TriComplexSignalosomeStericClashEngine()
        self.assertAlmostEqual(clash_eng.steric_distance_deficit_angstrom, 12.4, delta=1e-5)
        self.assertEqual(clash_eng.steric_clash_volume_angstrom3, 2450.0)

        # Clash imposes > 10^10 fold penalty on signalosome assembly
        res = clash_eng.compute_signalosome_inhibition(rason_occupancy=0.95)
        self.assertGreater(res["fold_shift_signalosome_kd"], 1.0e10)
        self.assertEqual(res["quaternary_signalosome_suppression_percent"], 95.0)

    # ========================================================================
    # 23. ADULT TISSUE GENETIC SAFETY & ISOFORM REDUNDANCY (Drosten 2010)
    # ========================================================================

    def test_adult_tissue_genetic_safety_margins(self):
        """Verify differential host tolerance for Pan-KRAS vs Pan-RAS inhibition."""
        from kras_allostery_kinetics_engine import AdultTissueGeneticSafetyEngine

        # BI-2865 (Pan-KRAS) at 95% KRAS inhibition: host tolerated in all tissues (>50% flux)
        bi_res = AdultTissueGeneticSafetyEngine.evaluate_drug_safety_margins("BI-2865", kras_target_inhibition=0.95)
        self.assertTrue(bi_res["overall_host_tolerated"])
        for tissue, data in bi_res["tissue_profiles"].items():
            self.assertGreater(data["residual_flux_percent"], 50.0)
            self.assertTrue(data["is_viable"])
            self.assertGreater(data["safety_margin_fold"], 2.5)

        # RMC-6236 (Pan-RAS) at 95% KRAS inhibition: fails safety threshold (only 5% residual flux)
        rmc_res = AdultTissueGeneticSafetyEngine.evaluate_drug_safety_margins("RMC-6236", kras_target_inhibition=0.95)
        self.assertFalse(rmc_res["overall_host_tolerated"])
        for tissue, data in rmc_res["tissue_profiles"].items():
            self.assertAlmostEqual(data["residual_flux_percent"], 5.0, delta=0.1)
            self.assertFalse(data["is_viable"])
            self.assertLess(data["safety_margin_fold"], 1.0)

    # ========================================================================
    # 24. CRYPTIC POCKET COMPARISON (S-IIP vs S-IIG vs S-IP)
    # ========================================================================

    def test_cryptic_pocket_comparison(self):
        """Verify structural and thermodynamic divergence across S-IIP, S-IIG, and S-IP."""
        from kras_allostery_kinetics_engine import CrypticPocketComparisonEngine

        pockets = CrypticPocketComparisonEngine.compare_all_pockets()
        self.assertEqual(len(pockets), 3)

        siip = CrypticPocketComparisonEngine.get_pocket_profile("S-IIP")
        siig = CrypticPocketComparisonEngine.get_pocket_profile("S-IIG")
        sip = CrypticPocketComparisonEngine.get_pocket_profile("S-IP")

        # S-IIP has largest volume and highest state selectivity
        self.assertEqual(siip["volume_angstrom3"], 580.0)
        self.assertAlmostEqual(siip["state_selectivity_fold"], 8411.4, delta=0.5)
        self.assertEqual(siip["druggability_score"], 0.92)

        # S-IIG is essentially state-agnostic (1.22x preference)
        self.assertAlmostEqual(siig["state_selectivity_fold"], 1.22, delta=0.05)
        self.assertEqual(siig["druggability_score"], 0.58)

        # S-IP has highest opening penalty and lowest druggability
        self.assertGreater(sip["delta_g_open_gdp_kcal"], 3.0)
        self.assertEqual(sip["druggability_score"], 0.32)


if __name__ == "__main__":
    unittest.main()

