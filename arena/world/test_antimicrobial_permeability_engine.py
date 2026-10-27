"""
test_antimicrobial_permeability_engine.py
=========================================
Comprehensive empirical verification test suite for:
- LPS outer leaflet fluidity reduction & divalent cation dependence
- Porin size exclusion, Renkin hydrodynamic hindrance, & elliptical slit eyelet geometry
- Richter et al. (2017 Nature) 'eNTRy' rules evaluation and quantitative accumulation prediction
- RND tripartite efflux pump kinetics (AcrAB-TolC, MexAB-OprM) & PMF thermodynamics
- Analytical steady-state vs dynamic ODE trajectory agreement
- Critical influx-over-efflux saturation thresholds & synergistic MIC fold shifts
- Species permeability differential (E. coli vs P. aeruginosa)

Author: Raman (A002, Swarm Generation 0)
"""

import math
import unittest
import numpy as np

from antimicrobial_permeability_engine import (
    BOLTZMANN_K,
    TEMP_PHYSIOL_K,
    E_COLI_MORPHOLOGY,
    P_AERUGINOSA_MORPHOLOGY,
    CompoundProfile,
    LPSBilayerModel,
    PorinType,
    PorinSpecification,
    OMPF_SPEC,
    OMPC_SPEC,
    OPRF_SPEC,
    OPRD_SPEC,
    PorinPermeationModel,
    ENTRyRulesEngine,
    ENTRyEvaluationResult,
    ACRAB_TOLC_WT,
    ACRAB_TOLC_OVEREXPRESSOR,
    MEXAB_OPRM_WT,
    RNDEffluxModel,
    IntracellularAccumulationEngine,
    BENCHMARK_ANTIBIOTICS,
    run_antimicrobial_permeability_analysis
)


class TestLPSOuterMembraneBilayer(unittest.TestCase):
    """Verifies biophysical properties of asymmetric Lipopolysaccharide membrane."""

    def setUp(self):
        self.lps_default = LPSBilayerModel()

    def test_lps_bilayer_fluidity_reduction(self):
        """Outer leaflet must have ~100-fold lower lateral fluidity than fluid bilayer."""
        d_fluid = self.lps_default.d_lateral_pl # 1.0e-8 cm^2/s
        d_lps = self.lps_default.lps_lateral_diffusion_cm2_s
        ratio = d_fluid / d_lps
        self.assertAlmostEqual(ratio, 100.0, delta=1.0)
        self.assertLessEqual(d_lps, 1.5e-10)
        self.assertGreaterEqual(d_lps, 0.5e-10)

    def test_divalent_cation_chelation_increases_permeability(self):
        """Depleting divalent cations (e.g. EDTA) reduces headgroup bridging and increases mobility."""
        lps_chelated = LPSBilayerModel(divalent_cation_concentration_mM=0.1)
        self.assertGreater(
            lps_chelated.lps_lateral_diffusion_cm2_s,
            self.lps_default.lps_lateral_diffusion_cm2_s
        )
        
        cipro = BENCHMARK_ANTIBIOTICS["Ciprofloxacin"]
        p_norm = self.lps_default.calculate_passive_lipid_permeability(cipro)
        p_chelated = lps_chelated.calculate_passive_lipid_permeability(cipro)
        self.assertGreater(p_chelated, p_norm)

    def test_lipid_permeability_molecular_weight_sieving(self):
        """Bulky molecules must suffer exponential size attenuation across gel-phase Lipid A."""
        small_hydrophobic = CompoundProfile(
            name="SmallLipophile", mw_da=250.0, clogp=2.0, logd_74=2.0,
            tpsa_angstrom2=30.0, rotatable_bonds=2, globularity=0.2, has_primary_amine=False
        )
        bulky_hydrophobic = CompoundProfile(
            name="BulkyLipophile", mw_da=750.0, clogp=2.0, logd_74=2.0,
            tpsa_angstrom2=30.0, rotatable_bonds=2, globularity=0.2, has_primary_amine=False
        )
        p_small = self.lps_default.calculate_passive_lipid_permeability(small_hydrophobic)
        p_bulky = self.lps_default.calculate_passive_lipid_permeability(bulky_hydrophobic)
        self.assertGreater(p_small, 5.0 * p_bulky)


class TestPorinPermeationChannels(unittest.TestCase):
    """Verifies porin exclusion channels, Renkin steric hindrance, and electrostatics."""

    def setUp(self):
        self.ompf = PorinPermeationModel(OMPF_SPEC)
        self.ompc = PorinPermeationModel(OMPC_SPEC)

    def test_renkin_hindrance_bounds(self):
        """Renkin function must yield H in [0, 1) for r < r_pore, and exactly 0 for r >= r_pore."""
        r_pore = 0.55 # nm
        self.assertEqual(PorinPermeationModel.renkin_hindrance(0.55, r_pore), 0.0)
        self.assertEqual(PorinPermeationModel.renkin_hindrance(0.70, r_pore), 0.0)
        
        h_small = PorinPermeationModel.renkin_hindrance(0.20, r_pore)
        h_med = PorinPermeationModel.renkin_hindrance(0.40, r_pore)
        self.assertGreater(h_small, h_med)
        self.assertGreater(h_med, 0.0)
        self.assertLess(h_small, 1.0)

    def test_strict_size_exclusion_for_vancomycin(self):
        """Vancomycin (MW 1449 Da, Stokes radius ~0.75 nm) must be completely excluded from OmpF/OmpC."""
        vanco = BENCHMARK_ANTIBIOTICS["Vancomycin"]
        p_ompf = self.ompf.calculate_single_channel_permeability_cm3_s(vanco)
        p_ompc = self.ompc.calculate_single_channel_permeability_cm3_s(vanco)
        self.assertEqual(p_ompf, 0.0)
        self.assertEqual(p_ompc, 0.0)

    def test_globularity_enhancement_through_slit_pore(self):
        """A planar/low-globularity molecule (G=0.15) permeates faster than a spherical isomer (G=0.85)."""
        flat_mol = CompoundProfile(
            name="FlatIsomer", mw_da=380.0, clogp=0.0, logd_74=0.0,
            tpsa_angstrom2=90.0, rotatable_bonds=3, globularity=0.15, has_primary_amine=False
        )
        spherical_mol = CompoundProfile(
            name="SphericalIsomer", mw_da=380.0, clogp=0.0, logd_74=0.0,
            tpsa_angstrom2=90.0, rotatable_bonds=3, globularity=0.85, has_primary_amine=False
        )
        h_flat = self.ompf.calculate_effective_hindrance(flat_mol)
        h_sphere = self.ompf.calculate_effective_hindrance(spherical_mol)
        self.assertGreater(h_flat, h_sphere)

    def test_primary_amine_electrostatic_acceleration(self):
        """Primary amine protonated at pH 7.4 must exhibit favorable electrostatic translocation factor."""
        unprotonated = CompoundProfile(
            name="NeutralAnalog", mw_da=350.0, clogp=0.0, logd_74=0.0,
            tpsa_angstrom2=80.0, rotatable_bonds=3, globularity=0.20, has_primary_amine=False
        )
        aminated = CompoundProfile(
            name="PrimaryAmineAnalog", mw_da=350.0, clogp=0.0, logd_74=0.0,
            tpsa_angstrom2=80.0, rotatable_bonds=3, globularity=0.20,
            has_primary_amine=True, amine_pka=9.5, net_charge_74=1.0
        )
        f_neutral = self.ompf.calculate_electrostatic_factor(unprotonated)
        f_amine = self.ompf.calculate_electrostatic_factor(aminated)
        self.assertGreater(f_amine, f_neutral)


class TestENTRyRulesEngine(unittest.TestCase):
    """Verifies formalization of Richter et al. (Nature 2017) eNTRy rules."""

    def test_richter_6dnm_pair_validation(self):
        """6-DNM-Amine must pass eNTRy rules with High accumulation, while parent 6-DNM fails."""
        dnm_parent = BENCHMARK_ANTIBIOTICS["6-Deoxynybomycin"]
        dnm_amine = BENCHMARK_ANTIBIOTICS["6-DNM-Amine"]

        res_parent = ENTRyRulesEngine.evaluate(dnm_parent)
        res_amine = ENTRyRulesEngine.evaluate(dnm_amine)

        # Parent 6-DNM lacks primary amine
        self.assertFalse(res_parent.has_primary_amine)
        self.assertFalse(res_parent.all_entry_rules_passed)
        self.assertLess(res_parent.entry_score, 75.0)
        self.assertLess(res_parent.predicted_accumulation_nmol_per_10e12_cells, 50.0)

        # 6-DNM-Amine has primary amine, low globularity, MW < 600
        self.assertTrue(res_amine.has_primary_amine)
        self.assertTrue(res_amine.all_entry_rules_passed)
        self.assertGreaterEqual(res_amine.entry_score, 90.0)
        self.assertEqual(res_amine.predicted_accumulation_category, "High")
        self.assertGreaterEqual(res_amine.predicted_accumulation_nmol_per_10e12_cells, 100.0)

    def test_macrolide_fails_entry_rules(self):
        """Erythromycin must fail due to high MW (>600 Da), high globularity (>0.25), and rotatable bonds."""
        ery = BENCHMARK_ANTIBIOTICS["Erythromycin"]
        res = ENTRyRulesEngine.evaluate(ery)
        self.assertFalse(res.all_entry_rules_passed)
        self.assertFalse(res.mw_passed)
        self.assertFalse(res.globularity_passed)
        self.assertFalse(res.rotatable_bonds_passed)
        self.assertEqual(res.predicted_accumulation_category, "Low")


class TestRNDEffluxPumps(unittest.TestCase):
    """Verifies tripartite RND pump kinetics, proton motive force, and dual pocket recognition."""

    def setUp(self):
        self.pump = RNDEffluxModel(ACRAB_TOLC_WT)

    def test_proton_motive_force_free_energy(self):
        """PMF coupling must yield ~30-40 kJ/mol thermodynamic driving potential."""
        delta_g = self.pump.spec.free_energy_per_mole_j
        self.assertGreaterEqual(delta_g, 30_000.0)
        self.assertLessEqual(delta_g, 45_000.0)

    def test_dual_pocket_substrate_recognition(self):
        """Macrolides bind proximal pocket with high affinity; hydrophilic zwitterions evade."""
        ery = BENCHMARK_ANTIBIOTICS["Erythromycin"]
        amp = BENCHMARK_ANTIBIOTICS["Ampicillin"]
        
        km_ery = self.pump.predict_km_uM(ery)
        km_amp = self.pump.predict_km_uM(amp)

        self.assertLess(km_ery, 25.0) # High affinity for macrolide in proximal pocket
        self.assertGreater(km_amp, 20.0) # Lower affinity for ampicillin

    def test_overexpressor_increases_vmax(self):
        """MDR overexpressing mutant must have higher V_max than wild-type."""
        overexpressor = RNDEffluxModel(ACRAB_TOLC_OVEREXPRESSOR)
        vmax_wt = self.pump.calculate_vmax_moles_per_cell_s()
        vmax_mdr = overexpressor.calculate_vmax_moles_per_cell_s()
        self.assertGreater(vmax_mdr, 5.0 * vmax_wt)


class TestCoupledAccumulationAndThresholds(unittest.TestCase):
    """Verifies coupled ODE integration, steady-state algebra, and saturation thresholds."""

    def setUp(self):
        self.engine = IntracellularAccumulationEngine(morphology=E_COLI_MORPHOLOGY)

    def test_analytical_steady_state_matches_numerical_ode(self):
        """The exact quadratic analytical root must match the asymptotic ODE simulation."""
        cipro = BENCHMARK_ANTIBIOTICS["Ciprofloxacin"]
        c_out = 15.0 # uM
        
        # Analytical steady-state
        c_peri_analytical = self.engine.solve_steady_state_periplasmic_uM(cipro, c_out)
        
        # Numerical ODE trajectory for 60 seconds
        traj = self.engine.simulate_dynamic_trajectory(cipro, c_out, time_span_s=60.0)
        c_peri_numerical = traj["c_peri_uM"][-1]

        self.assertAlmostEqual(c_peri_analytical, c_peri_numerical, delta=0.05)

    def test_critical_saturation_threshold_transition(self):
        """External concentration exceeding C_threshold must transition into Influx-Saturated regime."""
        dnm_amine = BENCHMARK_ANTIBIOTICS["6-DNM-Amine"]
        c_thresh = self.engine.calculate_critical_accumulation_threshold_uM(dnm_amine)
        self.assertGreater(c_thresh, 0.0)
        self.assertLess(c_thresh, 15.0)

        # Below threshold: efflux actively depletes
        rep_low = self.engine.evaluate_antibiotic_kinetic_profile(dnm_amine, c_out_uM=0.2 * c_thresh)
        self.assertEqual(rep_low.regime, "Efflux-Dominated (Strict Depletion)")

        # Above threshold: influx overwhelms pump
        rep_high = self.engine.evaluate_antibiotic_kinetic_profile(dnm_amine, c_out_uM=2.0 * c_thresh)
        self.assertEqual(rep_high.regime, "Influx-Saturated (Efflux Overwhelmed)")

    def test_efflux_synergy_and_mic_fold_shift_differential(self):
        """Poorly permeant substrates (Novobiocin, Erythromycin) must show high MIC fold-shift (>50x),
        while highly permeant eNTRy substrates show low fold-shift (<5x)."""
        novo = BENCHMARK_ANTIBIOTICS["Novobiocin"]
        ery = BENCHMARK_ANTIBIOTICS["Erythromycin"]
        dnm_amine = BENCHMARK_ANTIBIOTICS["6-DNM-Amine"]

        rep_novo = self.engine.evaluate_antibiotic_kinetic_profile(novo, c_out_uM=10.0)
        rep_ery = self.engine.evaluate_antibiotic_kinetic_profile(ery, c_out_uM=10.0)
        rep_amine = self.engine.evaluate_antibiotic_kinetic_profile(dnm_amine, c_out_uM=10.0)

        self.assertGreater(rep_novo.predicted_mic_fold_shift_vs_null_efflux, 50.0)
        self.assertGreater(rep_ery.predicted_mic_fold_shift_vs_null_efflux, 50.0)
        self.assertLess(rep_amine.predicted_mic_fold_shift_vs_null_efflux, 5.0)

    def test_pseudomonas_aeruginosa_outer_membrane_impermeability(self):
        """P. aeruginosa outer membrane permeability must be orders of magnitude lower than E. coli."""
        engine_ecoli = IntracellularAccumulationEngine(morphology=E_COLI_MORPHOLOGY)
        engine_pa = IntracellularAccumulationEngine(morphology=P_AERUGINOSA_MORPHOLOGY)

        cipro = BENCHMARK_ANTIBIOTICS["Ciprofloxacin"]
        p_ecoli, _, _ = engine_ecoli.calculate_total_om_permeability_cm_s(cipro)
        p_pa, _, _ = engine_pa.calculate_total_om_permeability_cm_s(cipro)

        self.assertGreater(p_ecoli, 10.0 * p_pa)


if __name__ == "__main__":
    unittest.main()
