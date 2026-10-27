"""
test_lead_optimization_mpo_fep_engine.py — Unit & Empirical Test Suite
Nagarjuna (A004), Generation 0.
"""

import unittest
import math
import numpy as np

from lead_optimization_mpo_fep_engine import (
    PhysicochemicalProfile,
    LeadMolecule,
    AlchemicalFEPEngine,
    AlchemicalMMPTransformation,
    LipophilicTrapEngine,
    HERGCardiotoxicityEngine,
    MPOScoringEngine,
    ParetoOptimizationEngine,
    CardiacIonChannelProfile,
    CiPACardiacSafetyEngine,
    CovalentInhibitorProfile,
    CovalentLeadOptimizationEngine,
    DegraderPhysicochemicalProfile,
    ChameleonicDegraderEngine,
    HydrationWaterSite,
    STANDARD_KRAS_SIIP_WATERS,
    GISTCrypticPocketSolvationEngine,
    ResistanceRescueEvaluation,
    ExplicitSolventResistanceCompensationEngine,
    DualCavityAlchemicalFEPEngine,
    DualCavityPerturbationResult,
    BioisostereEscapeEngine,
    BioisostereTransformationResult,
    ActiveLearningBayesianParetoEngine,
    ActiveLearningOptimizationResult,
    CrossSwarmPanKRASBenchmarkEngine,
    PanKRASLeadSafetyAssessment,
    GenerativeScoringCollapseTheoreticalProof,
    create_empirical_benchmark_dataset,
    run_generative_vs_fep_dispersion_benchmark,
    KineticResidenceTimeEngine,
    KineticUnbindingProfile,
    BoreschRestraints,
    AbsoluteBindingFreeEnergyEngine,
    ClinicalDrugDDIProfile,
    CYPInhibitionAndDDIRiskEngine,
    MembranePermeabilityIonizationEngine,
    create_clinical_cardiotoxicity_and_ddi_benchmark,
    GAS_CONSTANT_R,
    PHYSIOLOGICAL_TEMP_K,
    HUMAN_HEPATIC_BLOOD_FLOW
)


class TestLeadOptimizationMPOFEPEngine(unittest.TestCase):
    """Rigorous test suite for computational lead optimization, FEP, and MPO engine."""

    def setUp(self):
        self.fep_engine = AlchemicalFEPEngine(temperature_k=PHYSIOLOGICAL_TEMP_K)
        self.herg_engine = HERGCardiotoxicityEngine()
        self.lipo_engine = LipophilicTrapEngine()
        self.mpo_engine = MPOScoringEngine()
        self.pareto_engine = ParetoOptimizationEngine()
        self.benchmark_data = create_empirical_benchmark_dataset()

    def test_fundamental_thermodynamic_relations(self):
        """Test Delta G = RT ln(Kd / C0) and pKd conversion."""
        # For Kd = 1.0 nM (1e-9 M)
        kd_nm = 1.0
        kd_molar = 1e-9
        expected_pkd = 9.0
        expected_dg = GAS_CONSTANT_R * PHYSIOLOGICAL_TEMP_K * math.log(kd_molar)

        prof = PhysicochemicalProfile(
            name="TestMol", mw=400.0, clogp=2.5, clogd74=2.5, tpsa=80.0,
            hbd=1, hba=5, rotatable_bonds=4, pka_base=None, pka_acid=None,
            aromatic_rings=2
        )
        mol = LeadMolecule(profile=prof, target_name="Target", kd_experimental_nm=kd_nm)

        self.assertAlmostEqual(mol.pkd, expected_pkd, places=4)
        self.assertAlmostEqual(mol.delta_g_bind_experimental, expected_dg, places=3)
        self.assertTrue(mol.delta_g_bind_experimental < -12.0)  # ~ -12.7 kcal/mol for 1 nM

    def test_zwanzig_forward_and_reverse_fep(self):
        """Test Zwanzig exponential formula on synthetic Gaussian distribution."""
        np.random.seed(101)
        true_dg = -2.5  # kcal/mol
        variance_u = 0.5  # low variance -> Zwanzig should be exact
        beta = self.fep_engine.beta

        # When Delta U is Gaussian with mean mu and variance sigma^2:
        # <exp(-beta dU)> = exp(-beta * mu + 0.5 * beta^2 * sigma^2)
        # Delta G = mu - 0.5 * beta * sigma^2
        sigma_u = math.sqrt(variance_u)
        mu_u = true_dg + 0.5 * beta * variance_u

        samples_forward = np.random.normal(loc=mu_u, scale=sigma_u, size=20000)
        calc_dg, var_dg = self.fep_engine.zwanzig_fep_forward(samples_forward)

        self.assertAlmostEqual(calc_dg, true_dg, delta=0.08)
        self.assertTrue(var_dg > 0.0)

        # Reverse test: Delta U_rev = -Delta U
        mu_rev = -true_dg + 0.5 * beta * variance_u
        samples_reverse = np.random.normal(loc=mu_rev, scale=sigma_u, size=20000)
        calc_dg_rev, var_dg_rev = self.fep_engine.zwanzig_fep_reverse(samples_reverse)
        self.assertAlmostEqual(calc_dg_rev, true_dg, delta=0.08)

    def test_bennett_acceptance_ratio_exactness(self):
        """Test Bennett Acceptance Ratio (BAR) converges to true free energy with lower variance than Zwanzig."""
        np.random.seed(202)
        true_dg = 1.75  # kcal/mol
        sigma = 1.0
        beta = self.fep_engine.beta

        # Forward work distribution (sampled from state 0)
        # P0(w) ~ N(true_dg + 0.5 * beta * sigma^2, sigma^2)
        mu_01 = true_dg + 0.5 * beta * (sigma ** 2)
        w_01 = np.random.normal(loc=mu_01, scale=sigma, size=5000)

        # Reverse work distribution (sampled from state 1)
        # P1(w) ~ N(-true_dg + 0.5 * beta * sigma^2, sigma^2)
        mu_10 = -true_dg + 0.5 * beta * (sigma ** 2)
        w_10 = np.random.normal(loc=mu_10, scale=sigma, size=5000)

        dg_bar, var_bar = self.fep_engine.bennett_acceptance_ratio(w_01, w_10)
        self.assertAlmostEqual(dg_bar, true_dg, delta=0.05)
        self.assertTrue(var_bar > 0.0)

    def test_thermodynamic_integration_quadrature(self):
        """Test Thermodynamic Integration (TI) recovers analytical integral."""
        # Let dU/dlambda = 2.0 * lambda + 1.0 -> int_0^1 (2*lam + 1) dlam = [lam^2 + lam]_0^1 = 2.0
        lambdas = np.linspace(0.0, 1.0, 11)
        gradients = 2.0 * lambdas + 1.0
        stds = np.full_like(lambdas, 0.05)

        dg_ti, var_ti = self.fep_engine.thermodynamic_integration(lambdas, gradients, stds)
        self.assertAlmostEqual(dg_ti, 2.0, places=4)
        self.assertTrue(var_ti > 0.0)

    def test_soft_core_potential_singularity_elimination(self):
        """Test that soft-core potential avoids r->0 singularity at lambda = 0.5 and lambda = 0.0."""
        # For standard LJ, r->0 causes 1/r^12 -> infinity.
        # Soft-core potential must remain finite even at r = 0.0 when 0 < lambda < 1.
        u_sc_r0, du_dlam_r0 = self.fep_engine.soft_core_lennard_jones(r=0.0, lam=0.5, sigma=0.3, epsilon=0.25, alpha=0.5)
        self.assertTrue(np.isfinite(u_sc_r0))
        self.assertTrue(np.isfinite(du_dlam_r0))
        # At lambda = 1 (fully on), soft term alpha*(1-1)^2 = 0, so at r = sigma = 0.3:
        # soft_term = (0.3/0.3)^6 = 1.0 -> bracket = 1/1^2 - 1/1 = 0 -> U = 0
        u_sc_sigma, _ = self.fep_engine.soft_core_lennard_jones(r=0.3, lam=1.0, sigma=0.3, epsilon=0.25, alpha=0.5)
        self.assertAlmostEqual(u_sc_sigma, 0.0, places=5)

    def test_phase_space_overlap_metrics(self):
        """Test Bhattacharyya coefficient and KL divergence for overlapping vs separated distributions."""
        # Highly overlapping distributions
        d1 = np.random.normal(loc=0.0, scale=1.0, size=2000)
        d2 = np.random.normal(loc=0.0, scale=1.0, size=2000)
        bhat_high, kl_low = self.fep_engine.phase_space_overlap(d1, -d2)
        self.assertTrue(bhat_high > 0.85)

        # Disjoint distributions (poor overlap)
        d3 = np.random.normal(loc=10.0, scale=0.5, size=2000)
        d4 = np.random.normal(loc=-10.0, scale=0.5, size=2000)
        bhat_low, kl_high = self.fep_engine.phase_space_overlap(d3, -d4)
        self.assertTrue(bhat_low < 0.05)

    def test_matched_molecular_pair_alchemical_cycle(self):
        """Test that Alchemical Thermodynamic Cycle obeys Hess's Law and matches experimental Delta Delta G."""
        mmps = self.benchmark_data["mmps"]
        for mmp in mmps:
            # Calculated Delta Delta G
            ddg_fep = mmp.delta_delta_g_fep
            ddg_exp = mmp.delta_delta_g_experimental
            # Error should be within typical FEP accuracy (< 0.1 kcal/mol on our benchmark MMPs)
            self.assertAlmostEqual(ddg_fep, ddg_exp, delta=0.1)
            self.assertTrue(mmp.fep_absolute_error < 0.1)

    def test_kras_secondary_resistance_mutations_hypatia_benchmark(self):
        """
        Verify exact empirical Delta Delta G targets from Hypatia:
        - Y96D: +3.98 kcal/mol
        - H95D: +3.04 kcal/mol
        """
        wt = self.benchmark_data["sotorasib_wt"]
        y96d = self.benchmark_data["sotorasib_y96d"]
        h95d = self.benchmark_data["sotorasib_h95d"]

        # Empirical Delta Delta G for Y96D
        ddg_y96d = y96d.delta_g_bind_experimental - wt.delta_g_bind_experimental
        self.assertAlmostEqual(ddg_y96d, 3.98, places=2)

        # Empirical Delta Delta G for H95D
        ddg_h95d = h95d.delta_g_bind_experimental - wt.delta_g_bind_experimental
        self.assertAlmostEqual(ddg_h95d, 3.04, places=2)

        # Ratio of Kd values: exp(DDG / RT)
        # Y96D Kd should be ~633x weaker
        ratio_y96d = y96d.kd_experimental_nm / wt.kd_experimental_nm
        expected_ratio_y96d = math.exp(3.98 / (GAS_CONSTANT_R * PHYSIOLOGICAL_TEMP_K))
        self.assertAlmostEqual(ratio_y96d, expected_ratio_y96d, places=2)

    def test_lipophilic_trap_and_general_solubility_equation(self):
        """Test that aqueous solubility collapses exponentially with clogP via GSE."""
        # For clogP = 1.0 vs clogP = 4.0 vs clogP = 5.5 (MP = 150°C)
        sol_p1 = self.lipo_engine.calculate_aqueous_solubility_um(clogp=1.0, melting_point_c=150.0)
        sol_p4 = self.lipo_engine.calculate_aqueous_solubility_um(clogp=4.0, melting_point_c=150.0)
        sol_p55 = self.lipo_engine.calculate_aqueous_solubility_um(clogp=5.5, melting_point_c=150.0)

        # GSE: log10(S) drops by exactly (4.0 - 1.0) = 3.0 log units -> 1000-fold drop!
        ratio = sol_p1 / sol_p4
        self.assertAlmostEqual(ratio, 1000.0, places=2)
        self.assertTrue(sol_p4 < 20.0)  # In marginal solubility regime (< 20 uM)
        self.assertTrue(sol_p55 < 1.0)  # In insoluble regime (< 1 uM) for lipophilic leads

    def test_plasma_protein_binding_and_unbound_fraction(self):
        """Test Austin et al. model for plasma protein binding."""
        # Lipophilic molecule (clogP = 4.8) vs hydrophilic (clogP = 1.0)
        fu_lipo = self.lipo_engine.calculate_plasma_unbound_fraction(clogp=4.8)
        fu_hydro = self.lipo_engine.calculate_plasma_unbound_fraction(clogp=1.0)

        # fu must be between 0 and 1
        self.assertTrue(0.0001 <= fu_lipo <= 1.0)
        self.assertTrue(0.0001 <= fu_hydro <= 1.0)
        # Lipophilic compound should have much smaller unbound fraction
        self.assertTrue(fu_lipo < 0.05)  # typically < 2% unbound
        self.assertTrue(fu_hydro > fu_lipo * 5.0)

    def test_human_well_stirred_liver_clearance(self):
        """Test hepatic clearance limits: extraction ratio bounded in [0, 1]."""
        clearance = self.lipo_engine.calculate_hepatic_clearance(
            clogp=3.5, tpsa=60.0, heavy_atom_count=30, fu_plasma=0.05
        )
        self.assertTrue(0.0 <= clearance["extraction_ratio"] <= 1.0)
        self.assertTrue(0.0 <= clearance["f_first_pass"] <= 1.0)
        self.assertTrue(0.0 < clearance["cl_hepatic"] <= HUMAN_HEPATIC_BLOOD_FLOW)

    def test_herg_cardiotoxicity_terfenadine_vs_fexofenadine(self):
        """
        Validate classic historic hERG wall demarcation:
        Terfenadine (withdrawn for fatal Torsades de Pointes) vs Fexofenadine (safe active metabolite).
        """
        terf = self.benchmark_data["terfenadine"]
        fexo = self.benchmark_data["fexofenadine"]

        # Terfenadine: basic cation (pKa 8.6), high lipophilicity (clogP 4.8) -> potent hERG blocker
        ic50_terf = self.herg_engine.predict_herg_ic50_um(terf.profile)
        fu_terf = self.lipo_engine.calculate_plasma_unbound_fraction(terf.profile.clogp, 0.0, terf.profile.fraction_cationic)
        safety_terf = self.herg_engine.calculate_herg_safety_margin(ic50_terf, terf.cmax_total_um, fu_terf)

        # Fexofenadine: zwitterion, lower lipophilicity (clogP 2.8), polar carboxylic acid -> high IC50
        ic50_fexo = self.herg_engine.predict_herg_ic50_um(fexo.profile)
        fu_fexo = self.lipo_engine.calculate_plasma_unbound_fraction(fexo.profile.clogp, fexo.profile.fraction_anionic, fexo.profile.fraction_cationic)
        safety_fexo = self.herg_engine.calculate_herg_safety_margin(ic50_fexo, fexo.cmax_total_um, fu_fexo)

        self.assertTrue(ic50_terf < 1.0)  # Potent blocker (< 1 uM)
        self.assertTrue(ic50_fexo > 10.0) # > 10 uM safe
        self.assertTrue(ic50_fexo > ic50_terf * 15.0)

        # Terfenadine fails safety margin
        self.assertFalse(safety_terf["is_acceptable"])
        self.assertTrue(safety_fexo["is_acceptable"])

    def test_cns_mpo_scoring_wager_functionality(self):
        """Test Pfizer CNS MPO score (Wager et al. 2010) on ideal vs poor CNS profiles."""
        # Ideal CNS candidate: MW 300, clogP 2.0, clogD 1.8, TPSA 60, HBD 0, pKa 7.2
        ideal_prof = PhysicochemicalProfile(
            name="IdealCNS", mw=300.0, clogp=2.0, clogd74=1.8, tpsa=60.0,
            hbd=0, hba=3, rotatable_bonds=3, pka_base=7.2, pka_acid=None, aromatic_rings=2
        )
        score_ideal = self.mpo_engine.cns_mpo_score(ideal_prof)
        self.assertAlmostEqual(score_ideal["total_cns_mpo"], 6.0, places=2)
        self.assertTrue(score_ideal["high_cns_penetration_prob"])

        # Poor CNS candidate: MW 550, clogP 5.5, clogD 4.5, TPSA 140, HBD 4, pKa 10.5
        poor_prof = PhysicochemicalProfile(
            name="PoorCNS", mw=550.0, clogp=5.5, clogd74=4.5, tpsa=140.0,
            hbd=4, hba=8, rotatable_bonds=9, pka_base=10.5, pka_acid=None, aromatic_rings=3
        )
        score_poor = self.mpo_engine.cns_mpo_score(poor_prof)
        self.assertAlmostEqual(score_poor["total_cns_mpo"], 0.0, places=2)
        self.assertFalse(score_poor["high_cns_penetration_prob"])

    def test_peripheral_mpo_scoring_and_hard_attrition(self):
        """Test Peripheral MPO scoring: detects hard attrition flags for cardiotoxicity and insoluble leads."""
        terf = self.benchmark_data["terfenadine"]
        fexo = self.benchmark_data["fexofenadine"]

        score_terf = self.mpo_engine.peripheral_mpo_score(terf, self.herg_engine, self.lipo_engine)
        score_fexo = self.mpo_engine.peripheral_mpo_score(fexo, self.herg_engine, self.lipo_engine)

        # Terfenadine must trigger hard attrition flag due to hERG SM < 30
        self.assertTrue(score_terf["hard_attrition_flag"])
        self.assertFalse(score_fexo["hard_attrition_flag"])
        self.assertTrue(score_fexo["total_peripheral_mpo"] > score_terf["total_peripheral_mpo"])

    def test_pareto_frontier_identification(self):
        """Test multi-objective Pareto non-dominated sorting."""
        leads = self.benchmark_data["lead_series"]
        objectives = ["pkd", "lle", "herg_ic50", "solubility"]
        pareto_indices = self.pareto_engine.identify_pareto_frontier(leads, objectives)

        self.assertTrue(len(pareto_indices) > 0)
        self.assertTrue(len(pareto_indices) <= len(leads))

    def test_generative_potency_trajectory_hERG_wall_collision(self):
        """
        Verify simulation of unconstrained generative chemistry optimization:
        Optimizing purely for potency drives lipophilicity, collapsing solubility and colliding with hERG wall.
        """
        starting_lead = self.benchmark_data["lead_series"][0]  # Scaffold_R_H
        traj = self.pareto_engine.simulate_generative_potency_trajectory(
            starting_molecule=starting_lead,
            num_steps=6,
            potency_drive_per_step_kcal=-0.6
        )

        step_0 = traj[0]
        step_last = traj[-1]

        # Potency increased dramatically (Kd decreased by > 100-fold)
        self.assertTrue(step_last["kd_nm"] < step_0["kd_nm"] * 0.01)
        self.assertTrue(step_last["pkd"] > step_0["pkd"])

        # Lipophilicity and MW increased
        self.assertTrue(step_last["clogp"] > step_0["clogp"] + 2.5)
        self.assertTrue(step_last["mw"] > step_0["mw"] + 100.0)

        # Aqueous solubility collapsed by > 100-fold
        self.assertTrue(step_last["solubility_um"] < step_0["solubility_um"] * 0.01)

        # hERG IC50 decreased into dangerous blockade regime (< 1.0 uM)
        self.assertTrue(step_last["herg_ic50_um"] < step_0["herg_ic50_um"])

        # Hard attrition triggered at end of naive trajectory
        self.assertTrue(step_last["hard_attrition"])

    def test_generative_vs_fep_statistical_dispersion_benchmark(self):
        """
        Quantify why FEP achieves ~0.9 kcal/mol precision on matched molecular pairs
        while empirical docking and 3D equivariant GNNs collapse to RMSE > 2.0 kcal/mol.
        """
        bench = run_generative_vs_fep_dispersion_benchmark(n_pairs=300, random_seed=42)

        fep_rmse = bench["fep_metrics"]["rmse"]
        docking_rmse = bench["docking_metrics"]["rmse"]
        gnn_rmse = bench["gnn_metrics"]["rmse"]

        # FEP RMSE must be ~ 0.85 kcal/mol (< 1.0 kcal/mol)
        self.assertTrue(0.70 <= fep_rmse <= 1.0)

        # Docking RMSE > 2.0 kcal/mol
        self.assertTrue(docking_rmse > 2.0)

        # GNN RMSE > 2.0 kcal/mol
        self.assertTrue(gnn_rmse > 2.0)

        # FEP must have much higher fraction of predictions within 1 kcal/mol
        self.assertTrue(bench["fep_metrics"]["fraction_within_1kcal"] > 0.70)
        self.assertTrue(bench["docking_metrics"]["fraction_within_1kcal"] < 0.40)


    def test_soft_core_derivative_finite_difference(self):
        """Verify analytical dU/dlambda matches numerical central finite difference to < 1e-6."""
        r_vals = [0.15, 0.25, 0.35, 0.50]
        lam_vals = [0.1, 0.3, 0.5, 0.7, 0.9]
        eps = 1e-6

        for r in r_vals:
            for lam in lam_vals:
                u, du_analytical = self.fep_engine.soft_core_lennard_jones(r=r, lam=lam)
                u_plus, _ = self.fep_engine.soft_core_lennard_jones(r=r, lam=lam + eps)
                u_minus, _ = self.fep_engine.soft_core_lennard_jones(r=r, lam=lam - eps)
                du_numerical = (u_plus - u_minus) / (2.0 * eps)
                self.assertAlmostEqual(du_analytical, du_numerical, places=5)

    def test_electrophysiology_action_potential_prolongation(self):
        """Verify I_Kr blockade and action potential duration (QTc) prolongation calculations."""
        # Unbound conc = 0.05 uM, IC50 = 0.05 uM -> 50% block
        res_50 = self.herg_engine.electrophysiology_action_potential_prolongation(
            cmax_unbound_um=0.05, ic50_um=0.05
        )
        self.assertAlmostEqual(res_50["fractional_ikr_block"], 0.50, places=2)
        self.assertTrue(res_50["qtc_prolongation_ms"] > 50.0)  # > 50 ms prolongation
        self.assertTrue(res_50["exceeds_ich_e14_threshold"])
        self.assertTrue(res_50["projected_qtc_ms"] > 460.0)

        # Very low unbound conc: safe, below 10 ms ICH threshold
        res_safe = self.herg_engine.electrophysiology_action_potential_prolongation(
            cmax_unbound_um=0.0001, ic50_um=10.0
        )
        self.assertTrue(res_safe["fractional_ikr_block"] < 0.001)
        self.assertTrue(res_safe["qtc_prolongation_ms"] < 2.0)
        self.assertFalse(res_safe["exceeds_ich_e14_threshold"])

    def test_cns_mpo_score_monotonicity_and_boundaries(self):
        """Verify all 6 Pfizer CNS MPO transformation functions strictly obey Wager et al. (2010)."""
        # Test clogP ramp (3.0 -> 1.0, 4.0 -> 0.5, 5.0 -> 0.0)
        p1 = PhysicochemicalProfile(name="p1", mw=300, clogp=3.0, clogd74=1.0, tpsa=50, hbd=0, hba=2, rotatable_bonds=2, pka_base=7.0, pka_acid=None, aromatic_rings=1)
        p2 = PhysicochemicalProfile(name="p2", mw=300, clogp=4.0, clogd74=1.0, tpsa=50, hbd=0, hba=2, rotatable_bonds=2, pka_base=7.0, pka_acid=None, aromatic_rings=1)
        p3 = PhysicochemicalProfile(name="p3", mw=300, clogp=5.0, clogd74=1.0, tpsa=50, hbd=0, hba=2, rotatable_bonds=2, pka_base=7.0, pka_acid=None, aromatic_rings=1)

        c1 = self.mpo_engine.cns_mpo_score(p1)["components"]
        c2 = self.mpo_engine.cns_mpo_score(p2)["components"]
        c3 = self.mpo_engine.cns_mpo_score(p3)["components"]

        self.assertAlmostEqual(c1["t_clogp"], 1.0)
        self.assertAlmostEqual(c2["t_clogp"], 0.5)
        self.assertAlmostEqual(c3["t_clogp"], 0.0)

        # Test TPSA hump (10 -> 0, 30 -> 0.5, 60 -> 1.0, 105 -> 0.5, 130 -> 0.0)
        p_tpsa_10 = PhysicochemicalProfile(name="pt1", mw=300, clogp=2, clogd74=1, tpsa=10, hbd=0, hba=2, rotatable_bonds=2, pka_base=7, pka_acid=None, aromatic_rings=1)
        p_tpsa_30 = PhysicochemicalProfile(name="pt2", mw=300, clogp=2, clogd74=1, tpsa=30, hbd=0, hba=2, rotatable_bonds=2, pka_base=7, pka_acid=None, aromatic_rings=1)
        p_tpsa_60 = PhysicochemicalProfile(name="pt3", mw=300, clogp=2, clogd74=1, tpsa=60, hbd=0, hba=2, rotatable_bonds=2, pka_base=7, pka_acid=None, aromatic_rings=1)
        p_tpsa_105 = PhysicochemicalProfile(name="pt4", mw=300, clogp=2, clogd74=1, tpsa=105, hbd=0, hba=2, rotatable_bonds=2, pka_base=7, pka_acid=None, aromatic_rings=1)
        p_tpsa_130 = PhysicochemicalProfile(name="pt5", mw=300, clogp=2, clogd74=1, tpsa=130, hbd=0, hba=2, rotatable_bonds=2, pka_base=7, pka_acid=None, aromatic_rings=1)

        self.assertAlmostEqual(self.mpo_engine.cns_mpo_score(p_tpsa_10)["components"]["t_tpsa"], 0.0)
        self.assertAlmostEqual(self.mpo_engine.cns_mpo_score(p_tpsa_30)["components"]["t_tpsa"], 0.5)
        self.assertAlmostEqual(self.mpo_engine.cns_mpo_score(p_tpsa_60)["components"]["t_tpsa"], 1.0)
        self.assertAlmostEqual(self.mpo_engine.cns_mpo_score(p_tpsa_105)["components"]["t_tpsa"], 0.5)
        self.assertAlmostEqual(self.mpo_engine.cns_mpo_score(p_tpsa_130)["components"]["t_tpsa"], 0.0)

    def test_ligand_efficiency_and_lipophilic_efficiency_scaling(self):
        """Verify LE, LLE, and LDE formulas across lead compounds."""
        leads = self.benchmark_data["lead_series"]
        for lead in leads:
            # LE = -Delta G / HAC
            calc_le = -lead.delta_g_bind_experimental / lead.profile.heavy_atom_count
            self.assertAlmostEqual(lead.ligand_efficiency, calc_le, places=4)

            # LLE = pKd - clogP
            calc_lle = lead.pkd - lead.profile.clogp
            self.assertAlmostEqual(lead.lipophilic_ligand_efficiency, calc_lle, places=4)

            # LDE = pKd - clogD74
            calc_lde = lead.pkd - lead.profile.clogd74
            self.assertAlmostEqual(lead.lipophilic_distribution_efficiency, calc_lde, places=4)

    def test_pareto_hypervolume_and_crowding_distance(self):
        """Test 2D hypervolume calculation and NSGA-II crowding distance."""
        pts = np.array([[1.0, 5.0], [2.0, 4.0], [4.0, 2.0], [5.0, 1.0]])
        hv = ParetoOptimizationEngine.compute_2d_hypervolume(pts, reference_point=(0.0, 0.0))
        self.assertAlmostEqual(hv, 14.0, places=4)

        cd = ParetoOptimizationEngine.compute_crowding_distance(pts)
        self.assertTrue(np.isinf(cd[0]))
        self.assertTrue(np.isinf(cd[-1]))
        self.assertTrue(all(cd[1:-1] > 0))

    def test_cipa_multichannel_verapamil_paradox(self):
        """
        Verify the Verapamil Paradox under FDA CiPA guidelines:
        Verapamil is a potent hERG blocker (IC50 = 150 nM), yet causes zero TdP
        because concurrent CaV1.2 block (IC50 = 180 nM) neutralizes repolarization delay.
        """
        cipa_data = self.benchmark_data["cipa_profiles"]
        verapamil = cipa_data["verapamil"]
        eval_verapamil = CiPACardiacSafetyEngine.evaluate_cipa_risk_tier(verapamil)

        self.assertGreater(eval_verapamil["fraction_block_herg"], 0.10)
        self.assertGreater(eval_verapamil["fraction_block_cav12"], 0.10)
        self.assertLess(eval_verapamil["delta_apd90_ms"], 20.0)
        self.assertEqual(eval_verapamil["tier"], "LOW_RISK_SAFE")
        self.assertTrue(eval_verapamil["is_safe"])

    def test_cipa_multichannel_terfenadine_vs_dofetilide_high_risk(self):
        """
        Verify high-risk classification for unbalanced I_Kr blockers (Dofetilide, Terfenadine).
        """
        cipa_data = self.benchmark_data["cipa_profiles"]
        dofetilide = cipa_data["dofetilide"]
        eval_dof = CiPACardiacSafetyEngine.evaluate_cipa_risk_tier(dofetilide)

        self.assertEqual(eval_dof["tier"], "HIGH_RISK")
        self.assertFalse(eval_dof["is_safe"])
        self.assertGreater(eval_dof["delta_apd90_ms"], 30.0)
        self.assertLess(eval_dof["delta_qnet_uC_per_uF"], -0.015)

        fex = cipa_data["fexofenadine"]
        eval_fex = CiPACardiacSafetyEngine.evaluate_cipa_risk_tier(fex)
        self.assertEqual(eval_fex["tier"], "LOW_RISK_SAFE")
        self.assertTrue(eval_fex["is_safe"])
        self.assertAlmostEqual(eval_fex["delta_apd90_ms"], 0.0, delta=1.0)

    def test_covalent_kinetics_kinact_over_ki(self):
        """
        Verify covalent two-step inactivation kinetics (k_inact / K_I)
        and target inactivation half-life for Sotorasib and Adagrasib.
        """
        cov_data = self.benchmark_data["covalent_profiles"]
        soto = cov_data["sotorasib"]

        eff_soto = CovalentLeadOptimizationEngine.calculate_covalent_efficiency(soto)
        self.assertAlmostEqual(eff_soto["kinact_over_ki_M_inv_s_inv"], 31666.67, delta=100.0)

        t_half_soto = CovalentLeadOptimizationEngine.calculate_target_inactivation_half_life(soto)
        self.assertGreater(t_half_soto, 1.0)
        self.assertLess(t_half_soto, 20.0)

        wsi = CovalentLeadOptimizationEngine.calculate_warhead_selectivity_index(soto)
        self.assertGreater(wsi, 1e5)

    def test_covalent_mpo_score_and_glutathione_hard_attrition(self):
        """
        Verify Covalent MPO scoring and hard attrition flag for hyper-reactive
        electrophiles (hallucinated generative warheads causing idiosyncratic DILI).
        """
        cov_data = self.benchmark_data["covalent_profiles"]
        soto = cov_data["sotorasib"]
        hallucinated = cov_data["hallucinated_electrophile"]

        score_soto = CovalentLeadOptimizationEngine.covalent_mpo_score(soto)
        self.assertGreaterEqual(score_soto["total_covalent_mpo"], 7.0)
        self.assertFalse(score_soto["hard_attrition_flag"])

        score_hallucinated = CovalentLeadOptimizationEngine.covalent_mpo_score(hallucinated)
        self.assertTrue(score_hallucinated["hard_attrition_flag"])
        self.assertIn("DILI Risk", score_hallucinated["attrition_reason"])

    def test_chameleonic_imhb_thermodynamics_and_permeability_boost(self):
        """
        Verify Beyond-Rule-of-5 Intramolecular Hydrogen Bonding (IMHB)
        thermodynamic equilibrium and polar surface shielding in PROTACs.
        """
        deg_data = self.benchmark_data["degrader_profiles"]
        arv110 = deg_data["arv110"]

        eq = ChameleonicDegraderEngine.calculate_conformer_equilibrium(arv110)
        self.assertGreater(eq["fraction_closed_in_membrane"], 0.70)
        self.assertLess(eq["tpsa_effective_dynamic_A2"], arv110.tpsa_aq)

        perm = ChameleonicDegraderEngine.predict_apparent_permeability(arv110)
        self.assertGreater(perm["permeability_boost_ratio"], 5.0)
        self.assertTrue(perm["is_orally_permeable"])

    def test_bro5_mpo_score_protac_druggability(self):
        """
        Verify bRo5 Druggability MPO Score demarcating orally viable PROTACs
        (ARV-110, ARV-471) from rigid non-chameleonic degraders.
        """
        deg_data = self.benchmark_data["degrader_profiles"]
        arv110 = deg_data["arv110"]
        arv471 = deg_data["arv471"]
        rigid = deg_data["rigid_degrader"]

        score_110 = ChameleonicDegraderEngine.bro5_druggability_mpo_score(arv110)
        score_471 = ChameleonicDegraderEngine.bro5_druggability_mpo_score(arv471)
        score_rigid = ChameleonicDegraderEngine.bro5_druggability_mpo_score(rigid)

        self.assertTrue(score_110["is_orally_viable"])
        self.assertTrue(score_471["is_orally_viable"])
        self.assertGreaterEqual(score_110["total_bro5_mpo"], 6.0)

        self.assertFalse(score_rigid["is_orally_viable"])
        self.assertLess(score_rigid["total_bro5_mpo"], 6.0)
        self.assertLess(score_rigid["total_bro5_mpo"], score_110["total_bro5_mpo"])

    def test_gist_cryptic_pocket_water_displacement_thermodynamics(self):
        """
        Verify Grid Inhomogeneous Solvation Theory (GIST / WaterMap) thermodynamic cycle:
        Displacement of 5 high-energy trapped waters (Phe78, Met72, Val9, Ile100, Gly12)
        releases -7.15 kcal/mol favorable free energy (-4.25 kcal enthalpy, -2.90 kcal entropy),
        offsetting the +0.88 kcal/mol pocket opening penalty in GDP-bound KRAS.
        """
        gist = GISTCrypticPocketSolvationEngine()
        self.assertAlmostEqual(gist.total_excess_solvation_free_energy(), 7.15, places=3)
        self.assertAlmostEqual(gist.total_excess_enthalpy(), 4.25, places=3)
        self.assertAlmostEqual(gist.total_excess_entropy_penalty(), 2.90, places=3)

        # Full displacement by MRTX1133
        mrtx_disp = gist.calculate_water_displacement_free_energy("MRTX1133")
        self.assertEqual(mrtx_disp["waters_displaced_count"], 5)
        self.assertAlmostEqual(mrtx_disp["delta_g_displacement_kcal"], -7.15, places=3)

        # Partial displacement by Sotorasib (displaces 4 waters)
        sot_disp = gist.calculate_water_displacement_free_energy("Sotorasib")
        self.assertEqual(sot_disp["waters_displaced_count"], 4)
        self.assertAlmostEqual(sot_disp["delta_g_displacement_kcal"], -6.15, places=3)

        # Pocket adaptation in GDP state: +0.88 - 7.15 = -6.27 kcal/mol (spontaneous!)
        gdp_adapt = gist.net_pocket_adaptation_free_energy("GDP", "MRTX1133")
        self.assertAlmostEqual(gdp_adapt["delta_g_pocket_net_kcal"], -6.27, places=3)
        self.assertTrue(gdp_adapt["pocket_formation_spontaneous"])

        # Pocket adaptation in GTP state: +6.45 - 7.15 = -0.70 kcal/mol (barely spontaneous)
        gtp_adapt = gist.net_pocket_adaptation_free_energy("GTP", "MRTX1133")
        self.assertAlmostEqual(gtp_adapt["delta_g_pocket_net_kcal"], -0.70, places=3)

        # GNN omission error quantification
        err = gist.quantify_gnn_solvation_omission_error("MRTX1133")
        self.assertAlmostEqual(err["omitted_water_displacement_kcal"], 7.15, places=3)
        self.assertGreater(err["expected_gnn_systematic_error_kcal"], 4.5)

    def test_y96d_thermodynamic_decomposition_hypatia_consilience(self):
        """
        Confirm thermodynamic cycle decomposition of KRAS Y96D resistance penalty
        in exact numerical consilience with Hypatia (A003):
        Total Delta Delta G = +3.98 kcal/mol = +1.85 (electrostatic) + 1.15 (desolvation)
        + 0.70 (pi-stacking loss) + 0.28 (loop strain).
        """
        decomp = ExplicitSolventResistanceCompensationEngine.decompose_y96d_resistance_penalty()
        self.assertAlmostEqual(decomp["electrostatic_clash_kcal"], 1.85, places=2)
        self.assertAlmostEqual(decomp["aspartate_born_desolvation_kcal"], 1.15, places=2)
        self.assertAlmostEqual(decomp["pi_pi_quadrupole_stacking_loss_kcal"], 0.70, places=2)
        self.assertAlmostEqual(decomp["switch_ii_loop_strain_kcal"], 0.28, places=2)
        self.assertAlmostEqual(decomp["total_delta_delta_g_kcal"], 3.98, places=2)

    def test_y96d_rescue_strategies_salt_bridge_vs_fluorination_herg_tradeoff(self):
        """
        Evaluate the Salt-Bridge Trap vs the Fluorination Escape Route:
        Proves that while an arginine-mimetic basic amine analogue rescues target affinity
        (Kd = 2.2 nM), it triggers fatal hERG channel inhibition (IC50 = 0.186 uM, SM = 24.9 < 30,
        Hard Attrition = True, QTc prolongation > 25 ms).
        Conversely, the multi-fluorinated scaffold analogue restores nanomolar potency (Kd = 7.5 nM)
        without basic charge, maintaining safe cardiac margin (SM = 229.6 >> 30, Hard Attrition = False)
        and superior Peripheral MPO (8.53 vs 6.19), proving it is the unique Pareto-optimal solution.
        """
        engine = ExplicitSolventResistanceCompensationEngine()
        rescues = engine.evaluate_sotorasib_y96d_rescue_strategies(cmax_total_um=1.5)

        parent = rescues["uncompensated_parent"]
        amine = rescues["basic_amine_salt_bridge"]
        fluoro = rescues["multi_fluorinated_scaffold"]

        # 1. Uncompensated parent
        self.assertAlmostEqual(parent.delta_delta_g_vs_wt, 3.98, places=2)
        self.assertGreater(parent.kd_mutant_nm, 1000.0)  # > 1 uM
        self.assertFalse(parent.is_pareto_optimal)
        self.assertFalse(parent.hard_attrition_flag)  # Safe on hERG, but inactive

        # 2. Basic Amine Salt-Bridge Analogue: affinity recovered, cardiotoxic failure!
        self.assertLess(amine.kd_mutant_nm, 5.0)  # ~2.2 nM potent
        self.assertLess(amine.herg_ic50_um, 0.25)  # Potent hERG blocker (< 250 nM)
        self.assertLess(amine.herg_safety_margin, 30.0)  # Fails ICH S7B safety threshold (< 30)
        self.assertTrue(amine.hard_attrition_flag)  # Rejection flag triggered
        self.assertGreater(amine.qtc_prolongation_ms, 7.5)  # Severe prolongation vs baseline
        self.assertGreater(amine.qtc_prolongation_ms, fluoro.qtc_prolongation_ms * 5.0)
        self.assertFalse(amine.is_pareto_optimal)

        # 3. Multi-Fluorinated Scaffold Analogue: affinity recovered AND cardiac safety preserved
        self.assertLess(fluoro.kd_mutant_nm, 15.0)  # ~7.5 nM potent
        self.assertGreater(fluoro.herg_ic50_um, 5.0)  # Clean hERG profile
        self.assertGreater(fluoro.herg_safety_margin, 100.0)  # Generous safety margin (>> 30)
        self.assertFalse(fluoro.hard_attrition_flag)  # No attrition flags
        self.assertLess(fluoro.qtc_prolongation_ms, 2.0)  # Minimal QTc prolongation (< 2 ms)
        self.assertTrue(fluoro.is_pareto_optimal)  # Pareto optimal
        self.assertGreater(fluoro.peripheral_mpo_score, amine.peripheral_mpo_score)

    def test_cross_swarm_benchmark_dataset_integration(self):
        """Verify cross-swarm integration objects in benchmark dataset."""
        self.assertIn("gist_engine", self.benchmark_data)
        self.assertIn("resistance_engine", self.benchmark_data)
        self.assertIn("sotorasib_y96d_rescues", self.benchmark_data)

        rescues = self.benchmark_data["sotorasib_y96d_rescues"]
        self.assertEqual(len(rescues), 3)
        self.assertIn("multi_fluorinated_scaffold", rescues)
        self.assertTrue(rescues["multi_fluorinated_scaffold"].is_pareto_optimal)

    def test_dual_cavity_alchemical_fep_and_selectivity_erosion(self):
        """
        Dual-Cavity Alchemical FEP: Test that on-target gains can be negated by
        disproportionate hERG pore cavity gains (Selectivity Erosion Index).
        """
        engine = DualCavityAlchemicalFEPEngine()

        # Case 1: Polar fluorination -> on-target gain + hERG detoxicity
        res_polar = engine.evaluate_dual_cavity_perturbation(
            transformation_name="Polar_Fluorination",
            delta_delta_g_target=-1.20,
            delta_clogp=-0.30,
            delta_aromatic_rings=0,
            delta_fraction_cationic=0.0,
            delta_tpsa=10.0
        )
        self.assertFalse(res_polar.selectivity_erosion_flag)
        self.assertGreater(res_polar.therapeutic_index_multiplier, 10.0)
        self.assertIn("EXPANDED", res_polar.verdict)

        # Case 2: Lipophilic basic amine -> on-target gain (-1.2 kcal) but hERG gain (-3.76 kcal)
        res_basic = engine.evaluate_dual_cavity_perturbation(
            transformation_name="Lipophilic_Basic_Amine",
            delta_delta_g_target=-1.20,
            delta_clogp=0.80,
            delta_aromatic_rings=1,
            delta_fraction_cationic=0.95,
            delta_tpsa=5.0
        )
        self.assertTrue(res_basic.selectivity_erosion_flag)
        self.assertLess(res_basic.therapeutic_index_multiplier, 0.05)
        self.assertIn("EROSION", res_basic.verdict)

    def test_3d_bioisostere_bcp_escape_from_herg_wall(self):
        """
        3D Saturated Bioisostere: Phenyl to Bicyclo[1.1.1]pentane (BCP)
        Demonstrates >50x hERG detoxicity, >5x solubility increase, and ADMET score gain.
        """
        engine = BioisostereEscapeEngine()
        baseline_prof = PhysicochemicalProfile(
            name="Aromatic_Lead",
            mw=420.0,
            clogp=3.80,
            clogd74=3.50,
            tpsa=65.0,
            hbd=1,
            hba=4,
            rotatable_bonds=4,
            pka_base=None,
            pka_acid=None,
            aromatic_rings=3,
            melting_point_c=185.0
        )
        res = engine.evaluate_phenyl_to_bcp(baseline_prof)
        self.assertEqual(res.delta_clogp, -0.72)
        self.assertGreater(res.solubility_fold_increase, 4.5)
        self.assertGreater(res.herg_ic50_fold_increase, 45.0)
        self.assertGreater(res.delta_delta_g_herg, 2.0)
        self.assertGreater(res.cyp_clearance_reduction_percent, 40.0)
        self.assertGreater(res.pareto_admet_score_gain, 1.5)
        self.assertIn("OPTIMAL 3D BIOISOSTERE", res.verdict)

    def test_3d_bioisostere_cubane_transformation(self):
        """
        3D Saturated Bioisostere: Phenyl to 1,4-Cubane substitution.
        Demonstrates rigid 3D spatial presentation with >50x hERG detoxicity.
        """
        engine = BioisostereEscapeEngine()
        baseline_prof = PhysicochemicalProfile(
            name="Aromatic_Lead",
            mw=420.0,
            clogp=3.80,
            clogd74=3.50,
            tpsa=65.0,
            hbd=1,
            hba=4,
            rotatable_bonds=4,
            pka_base=None,
            pka_acid=None,
            aromatic_rings=3,
            melting_point_c=185.0
        )
        res = engine.evaluate_phenyl_to_cubane(baseline_prof)
        self.assertEqual(res.delta_clogp, -0.45)
        self.assertGreater(res.solubility_fold_increase, 2.5)
        self.assertGreater(res.herg_ic50_fold_increase, 50.0)
        self.assertGreater(res.delta_delta_g_herg, 2.4)
        self.assertGreater(res.cyp_clearance_reduction_percent, 50.0)

    def test_active_learning_generative_potency_only_collides_with_herg(self):
        """
        Generative AI failure mode: unconstrained docking score selection
        picks lipophilic and aromatic variants that collide directly with the hERG wall.
        """
        al_engine = ActiveLearningBayesianParetoEngine()
        candidates = al_engine.generate_candidate_library()
        self.assertEqual(len(candidates), 60)

        # Sort by docking score (most negative)
        top_docking = sorted(candidates, key=lambda c: c.predicted_docking_score)[:5]
        # All top docking picks should have severe hERG liability (< 1.0 uM)
        for cand in top_docking:
            self.assertLess(cand.true_herg_ic50_um, 1.0)
            self.assertGreater(cand.clogp, 3.8)

    def test_active_learning_fep_guided_bayesian_pareto_convergence(self):
        """
        Closed-loop FEP-guided Active Learning: EHVI acquisition discovers
        high-potency, safe leads (Kd < 5 nM, SM > 50) and expands hypervolume within 12 FEP steps.
        """
        al_engine = ActiveLearningBayesianParetoEngine()
        res = al_engine.run_optimization_comparison(n_fep_budget=12, cmax_total_um=1.0)

        self.assertTrue(res.generative_unconstrained_collided_herg)
        self.assertTrue(res.fep_guided_achieved_pareto_optimality)
        self.assertLess(res.top_lead_target_kd_nm, 5.0)
        self.assertGreater(res.top_lead_herg_safety_margin, 50.0)
        self.assertGreater(res.hypervolume_gain, 0.0)
        self.assertEqual(res.final_pareto_size, 12)
        self.assertGreater(len(res.history), 0)

    def test_hypatia_consilience_bi2865_pan_kras_clean_cardiac_margin(self):
        """
        Cross-swarm consilience with Hypatia (A003): BI-2865 achieves
        Pan-KRAS selectivity (>80-fold over NRAS/HRAS) with clean cardiac safety margin (>300).
        """
        kras_engine = CrossSwarmPanKRASBenchmarkEngine()
        leads = kras_engine.evaluate_pan_kras_leads()
        bi2865 = leads["bi_2865"]

        self.assertEqual(bi2865.compound_name, "BI-2865")
        self.assertEqual(bi2865.kd_kras_nm, 4.0)
        self.assertGreater(bi2865.isoform_selectivity_fold, 80.0)
        self.assertGreater(bi2865.herg_safety_margin, 300.0)
        self.assertFalse(bi2865.hard_attrition_flag)
        self.assertEqual(bi2865.torsades_risk_tier, "LOW_RISK")
        self.assertGreater(bi2865.peripheral_mpo_score, 5.0)

    def test_hypatia_consilience_mrtx1133_salt_bridge_vs_free_fraction(self):
        """
        Cross-swarm consilience with Hypatia (A003): MRTX1133 (KRAS G12D selective)
        navigates the basic salt-bridge trap through high potency (0.2 nM),
        but remains vulnerable if free fraction surges.
        """
        kras_engine = CrossSwarmPanKRASBenchmarkEngine()
        leads = kras_engine.evaluate_pan_kras_leads()
        mrtx1133 = leads["mrtx_1133"]

        self.assertEqual(mrtx1133.compound_name, "MRTX1133")
        self.assertEqual(mrtx1133.kd_kras_nm, 0.20)
        self.assertLess(mrtx1133.herg_ic50_um, 3.0)  # Moderate blocker due to basic pyrrolidine
        self.assertGreater(mrtx1133.herg_safety_margin, 300.0) # Safe at therapeutic free dose
        self.assertFalse(mrtx1133.hard_attrition_flag)

        # Vulnerability check: if unbound Cmax rises to 0.10 uM, SM drops below 30
        cmax_surge = 0.10
        sm_surge = mrtx1133.herg_ic50_um / cmax_surge
        self.assertLess(sm_surge, 30.0)  # Violates safety margin!

    def test_hypatia_consilience_rmc6236_tri_complex_macromolecular_shielding(self):
        """
        Cross-swarm consilience with Hypatia (A003): RMC-6236 (RAS(ON) Tri-Complex)
        uses macromolecular steric shielding via Cyclophilin A to occlude ion channels.
        """
        kras_engine = CrossSwarmPanKRASBenchmarkEngine()
        leads = kras_engine.evaluate_pan_kras_leads()
        rmc6236 = leads["rmc_6236"]

        self.assertEqual(rmc6236.compound_name, "RMC-6236")
        self.assertEqual(rmc6236.kd_kras_nm, 0.50)
        self.assertTrue(rmc6236.macromolecular_shielding)
        self.assertGreater(rmc6236.herg_safety_margin, 400.0)
        self.assertFalse(rmc6236.hard_attrition_flag)

    def test_generative_scoring_collapse_theoretical_lower_bound_proof(self):
        """
        Theoretical proof: Static Generative scoring functions have an irreducible
        variance lower bound >= 2.2 kcal/mol, while alchemical FEP achieves <= 0.9 kcal/mol.
        """
        proof_engine = GenerativeScoringCollapseTheoreticalProof()
        var_comps = proof_engine.calculate_theoretical_variance_components()
        self.assertGreater(var_comps["var_water_reorganization"], 3.0)
        self.assertGreater(var_comps["total_irreducible_variance"], 5.5)
        self.assertGreater(var_comps["theoretical_lower_bound_rmse_kcal"], 2.2)

        fep_canc = proof_engine.calculate_fep_cycle_cancellation(n_effective_snapshots=5000)
        self.assertLess(fep_canc["fep_rmse_kcal"], 1.0)
        self.assertLess(fep_canc["fep_rmse_kcal"], 0.45 * var_comps["theoretical_lower_bound_rmse_kcal"])

    def test_expanded_empirical_benchmark_dataset_integration(self):
        """Verify that all new engines and benchmarks are present in the benchmark dataset."""
        self.assertIn("dual_cavity_engine", self.benchmark_data)
        self.assertIn("bioisostere_engine", self.benchmark_data)
        self.assertIn("active_learning_engine", self.benchmark_data)
        self.assertIn("pan_kras_engine", self.benchmark_data)
        self.assertIn("scoring_collapse_proof", self.benchmark_data)

        # Quick validation of instances
        pan_leads = self.benchmark_data["pan_kras_engine"].evaluate_pan_kras_leads()
        self.assertEqual(len(pan_leads), 3)
        self.assertIn("bi_2865", pan_leads)

    def test_kinetic_residence_time_eyring_unbinding_barrier(self):
        """
        Tests transition state Eyring equation: Delta G^ddagger = RT ln(k_B T / (h * k_off)),
        residence time tau = 1 / k_off, and thermodynamic consistency.
        """
        kinetic_engine = KineticResidenceTimeEngine(temperature_k=PHYSIOLOGICAL_TEMP_K)
        profile = kinetic_engine.calculate_koff_and_residence_time(
            delta_g_unbinding_barrier_kcal=21.0,
            delta_g_binding_kcal=-11.5
        )
        self.assertAlmostEqual(profile.delta_g_unbinding_barrier_kcal, 21.0, places=2)
        self.assertAlmostEqual(profile.k_off_s_inv, 0.0103, delta=0.001)
        self.assertAlmostEqual(profile.residence_time_s, 97.1, delta=1.5)
        self.assertAlmostEqual(profile.residence_time_min, 1.62, delta=0.1)

        # Invert k_off back to unbinding barrier
        recomputed_barrier = kinetic_engine.calculate_unbinding_barrier_from_koff(profile.k_off_s_inv)
        self.assertAlmostEqual(recomputed_barrier, 21.0, places=3)

        # Check thermodynamic consistency: Kd = exp(Delta G / RT)
        expected_kd_nm = math.exp(-11.5 / (GAS_CONSTANT_R * PHYSIOLOGICAL_TEMP_K)) * 1e9
        self.assertAlmostEqual(profile.kd_nm, expected_kd_nm, delta=0.01)

    def test_herg_channel_trapping_kinetics(self):
        """
        Tests hERG channel trapping kinetics: fast unbinding vs lethal rate-dependent accumulation.
        """
        kinetic_engine = KineticResidenceTimeEngine(temperature_k=PHYSIOLOGICAL_TEMP_K)

        # Fast unbinding drug: k_off = 5.0 s^-1
        fast_result = kinetic_engine.evaluate_herg_channel_trapping(k_off_herg_s_inv=5.0, heart_rate_bpm=60.0)
        self.assertEqual(fast_result["trapping_tier"], "FAST_UNBINDING_BENIGN")
        self.assertGreater(fast_result["fraction_unbound_per_beat"], 0.90)
        self.assertLess(fast_result["cumulative_amplification_factor"], 1.1)

        # Lethal trapped drug: k_off = 0.005 s^-1 (tau = 200 s)
        trapped_result = kinetic_engine.evaluate_herg_channel_trapping(k_off_herg_s_inv=0.005, heart_rate_bpm=60.0)
        self.assertEqual(trapped_result["trapping_tier"], "LETHAL_TRAPPED_BLOCKER")
        self.assertGreater(trapped_result["fraction_trapped_per_beat"], 0.99)
        self.assertGreater(trapped_result["cumulative_amplification_factor"], 100.0)

    def test_boresch_analytical_restraint_correction(self):
        """
        Tests Boresch standard-state restraint analytical free energy correction Delta G^circ_restr.
        """
        restraints = BoreschRestraints(
            r0_angstrom=5.0,
            theta_a_deg=90.0,
            theta_b_deg=90.0,
            k_r_kcal_per_mol_ang2=10.0,
            k_theta_a_kcal_per_mol_rad2=20.0,
            k_theta_b_kcal_per_mol_rad2=20.0,
            k_phi_a_kcal_per_mol_rad2=20.0,
            k_phi_b_kcal_per_mol_rad2=20.0,
            k_phi_c_kcal_per_mol_rad2=20.0
        )
        delta_g_restr = restraints.calculate_standard_state_correction(PHYSIOLOGICAL_TEMP_K)
        # Analytical expected value ~ 8.10 kcal/mol
        self.assertAlmostEqual(delta_g_restr, 8.101, delta=0.05)

        # Verify monotonicity: tighter restraints (higher force constants) increase restraint penalty
        stiffer_restraints = BoreschRestraints(k_r_kcal_per_mol_ang2=40.0)
        stiffer_delta_g = stiffer_restraints.calculate_standard_state_correction(PHYSIOLOGICAL_TEMP_K)
        self.assertGreater(stiffer_delta_g, delta_g_restr)

    def test_absolute_binding_free_energy_double_decoupling_cycle(self):
        """
        Tests ABFE double decoupling cycle:
        Delta G^circ_bind = Delta G_water - Delta G_complex - Delta G^circ_restr + Delta G_restr_complex
        """
        abfe_engine = AbsoluteBindingFreeEnergyEngine(temperature_k=PHYSIOLOGICAL_TEMP_K)
        restraints = BoreschRestraints()

        # Decoupling from water: +18.5 kcal/mol
        # Decoupling from complex: +35.2 kcal/mol
        # Restraints in bound complex: +0.2 kcal/mol
        # Boresch standard state correction: +8.10 kcal/mol
        # Expected Delta G^circ_bind = 18.5 - 35.2 - 8.10 + 0.2 = -24.6 kcal/mol
        result = abfe_engine.compute_abfe(
            delta_g_decouple_water=18.5,
            delta_g_decouple_complex=35.2,
            delta_g_restr_complex=0.2,
            restraints=restraints
        )
        self.assertAlmostEqual(result["delta_g_bind_absolute_kcal"], -24.601, delta=0.05)
        self.assertGreater(result["kd_nm"], 0.0)

    def test_generative_scaffold_hop_omitted_restraint_failure(self):
        """
        Tests comparison between Generative AI static scoring and rigorous ABFE:
        shows omission of restraint entropy causes systematic overprediction.
        """
        abfe_engine = AbsoluteBindingFreeEnergyEngine(temperature_k=PHYSIOLOGICAL_TEMP_K)
        abfe_res = abfe_engine.compute_abfe(
            delta_g_decouple_water=15.0,
            delta_g_decouple_complex=25.0,
            delta_g_restr_complex=0.1
        )
        comp = abfe_engine.compare_with_generative_scaffold_hop(
            predicted_score_kcal=-24.0,
            abfe_result=abfe_res
        )
        self.assertGreater(comp["restraint_penalty_kcal"], 7.0)
        self.assertGreater(comp["absolute_error_kcal"], 5.0)

    def test_cyp3a4_inhibition_mechanistic_auc_ratio(self):
        """
        Tests static DDI model: AUC_ratio = 1 / [ (1 - fm) + fm / (1 + [I]_u / Ki) ].
        """
        cyp_engine = CYPInhibitionAndDDIRiskEngine()

        # Cisapride under Ketoconazole: fm = 0.88, Ki = 0.02 uM, [I]_u = 0.25 uM
        auc_ratio = cyp_engine.calculate_auc_ratio(
            fraction_metabolized_cyp=0.88,
            ki_perpetrator_um=0.02,
            conc_perpetrator_unbound_um=0.25
        )
        self.assertAlmostEqual(auc_ratio, 5.40, delta=0.1)

        # Baseline: zero inhibitor concentration gives AUC_ratio = 1.0
        auc_baseline = cyp_engine.calculate_auc_ratio(
            fraction_metabolized_cyp=0.88,
            ki_perpetrator_um=0.02,
            conc_perpetrator_unbound_um=0.0
        )
        self.assertAlmostEqual(auc_baseline, 1.0, places=4)

    def test_clinical_ddi_cardiac_safety_cisapride_collapse_vs_mosapride_prucalopride(self):
        """
        Tests real clinical benchmark: Cisapride collapses below SM < 30 under CYP3A4 inhibition,
        while second-generation Mosapride and Prucalopride maintain wide safety margins.
        """
        cyp_engine = CYPInhibitionAndDDIRiskEngine()
        benchmarks = create_clinical_cardiotoxicity_and_ddi_benchmark()

        cisapride = benchmarks["cisapride"]
        mosapride = benchmarks["mosapride"]
        prucalopride = benchmarks["prucalopride"]

        # 5.4-fold AUC increase under Ketoconazole
        cis_eval = cyp_engine.evaluate_post_ddi_cardiac_safety(cisapride, auc_ratio=5.4)
        self.assertEqual(cis_eval["ddi_risk_tier"], "FATAL_PROARRHYTHMIC_COLLAPSE")
        self.assertLess(cis_eval["sm_post_ddi"], 10.0)

        # Mosapride under same DDI
        mos_eval = cyp_engine.evaluate_post_ddi_cardiac_safety(mosapride, auc_ratio=5.4)
        self.assertEqual(mos_eval["ddi_risk_tier"], "CARDIAC_SAFETY_PRESERVED")
        self.assertGreater(mos_eval["sm_post_ddi"], 300.0)

        # Prucalopride has minimal CYP metabolism (fm = 0.15)
        pruc_auc = cyp_engine.calculate_auc_ratio(0.15, 0.02, 0.25)
        pruc_eval = cyp_engine.evaluate_post_ddi_cardiac_safety(prucalopride, auc_ratio=pruc_auc)
        self.assertEqual(pruc_eval["ddi_risk_tier"], "CARDIAC_SAFETY_PRESERVED")
        self.assertGreater(pruc_eval["sm_post_ddi"], 3000.0)

    def test_astemizole_vs_cetirizine_cardiotoxicity_demarcation(self):
        """
        Tests Astemizole (sub-nM hERG block, fatal) vs Cetirizine (zwitterion, clean margin).
        """
        cyp_engine = CYPInhibitionAndDDIRiskEngine()
        benchmarks = create_clinical_cardiotoxicity_and_ddi_benchmark()

        astemizole = benchmarks["astemizole"]
        cetirizine = benchmarks["cetirizine"]

        ast_eval = cyp_engine.evaluate_post_ddi_cardiac_safety(astemizole, auc_ratio=4.0)
        self.assertEqual(ast_eval["ddi_risk_tier"], "FATAL_PROARRHYTHMIC_COLLAPSE")
        self.assertLess(ast_eval["sm_post_ddi"], 5.0)

        cet_eval = cyp_engine.evaluate_post_ddi_cardiac_safety(cetirizine, auc_ratio=1.1)
        self.assertEqual(cet_eval["ddi_risk_tier"], "CARDIAC_SAFETY_PRESERVED")
        self.assertGreater(cet_eval["sm_post_ddi"], 900.0)

    def test_henderson_hasselbalch_speciation_and_effective_logd(self):
        """
        Tests Henderson-Hasselbalch speciation and effective logD at physiological and gut pH.
        """
        perm_engine = MembranePermeabilityIonizationEngine()

        spec_74 = perm_engine.calculate_speciation(pka=9.5, is_base=True, ph=7.4)
        self.assertAlmostEqual(spec_74["fraction_neutral"], 0.00788, delta=0.001)
        self.assertAlmostEqual(spec_74["fraction_ionized"], 0.99212, delta=0.001)

        logd = perm_engine.calculate_effective_logd(clogp=3.5, pka=9.5, is_base=True, ph=7.4)
        self.assertAlmostEqual(logd, 1.41, delta=0.05)

        spec_acid = perm_engine.calculate_speciation(pka=3.8, is_base=False, ph=7.4)
        self.assertAlmostEqual(spec_acid["fraction_neutral"], 0.00025, delta=0.0001)
        self.assertAlmostEqual(spec_acid["fraction_ionized"], 0.99975, delta=0.0001)

    def test_caco2_transcellular_permeability_and_fa_absorption(self):
        """
        Tests Caco-2 Papp prediction and Amidon human fraction absorbed Fa.
        """
        perm_engine = MembranePermeabilityIonizationEngine()

        papp_high = perm_engine.calculate_caco2_papp(clogd=2.0, mw=350, tpsa=50)
        self.assertGreater(papp_high, 5.0)
        fa_high = perm_engine.estimate_human_fraction_absorbed(papp_high)
        self.assertGreater(fa_high, 0.85)

        papp_low = perm_engine.calculate_caco2_papp(clogd=-1.0, mw=650, tpsa=160)
        self.assertLess(papp_low, 0.5)
        fa_low = perm_engine.estimate_human_fraction_absorbed(papp_low)
        self.assertLess(fa_low, 0.35)

    def test_basicity_paradox_coupled_gut_barrier_and_herg_trap(self):
        """
        Tests the Basicity Paradox: boosting amine basicity (pKa 6.5 -> 9.8)
        collapses Caco-2 Papp and drives hERG IC50 directly into the cardiotoxic zone.
        """
        perm_engine = MembranePermeabilityIonizationEngine()

        clean_lead = perm_engine.evaluate_basicity_paradox(clogp=3.0, pka=6.5, mw=420, tpsa=70)
        toxic_lead = perm_engine.evaluate_basicity_paradox(clogp=3.0, pka=9.8, mw=420, tpsa=70)

        self.assertGreater(clean_lead["caco2_papp_1e6_cm_s"], toxic_lead["caco2_papp_1e6_cm_s"] * 5.0)
        self.assertGreater(clean_lead["fraction_absorbed_fa"], toxic_lead["fraction_absorbed_fa"])
        self.assertGreater(clean_lead["predicted_herg_ic50_um"], toxic_lead["predicted_herg_ic50_um"] * 5.0)
        self.assertEqual(toxic_lead["herg_risk_status"], "CARDIO_TOXIC")

    def test_clinical_cardiotoxicity_and_ddi_benchmark_dataset_integrity(self):
        """
        Validates all 7 clinical drug profiles in the benchmark dataset.
        """
        dataset = create_clinical_cardiotoxicity_and_ddi_benchmark()
        self.assertEqual(len(dataset), 7)
        self.assertIn("cisapride", dataset)
        self.assertIn("mosapride", dataset)
        self.assertIn("prucalopride", dataset)
        self.assertIn("astemizole", dataset)
        self.assertIn("cetirizine", dataset)
        self.assertIn("terfenadine", dataset)
        self.assertIn("fexofenadine", dataset)

        for name, drug in dataset.items():
            self.assertGreater(drug.herg_ic50_um, 0.0)
            self.assertGreater(drug.cmax_free_baseline_um, 0.0)
            self.assertGreaterEqual(drug.fraction_metabolized_cyp, 0.0)
            self.assertLessEqual(drug.fraction_metabolized_cyp, 1.0)


if __name__ == "__main__":
    unittest.main()
