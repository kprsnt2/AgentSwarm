"""
test_drug-discovery_engine.py - Test Suite for Phase 2 Empirical Drug Discovery Engine
Agent: Hypatia (A003), Generation 0

Verifies:
  1. API contract and schema compliance of analyze()
  2. Ground truth: clinical attrition >90% overall and Phase II bottleneck
  3. Structural biology limits: AlphaFold prediction vs binding free energy/ADMET
  4. Biophysical lipophilic trap & in vivo potency paradox (Lipinski / Austin / Waring)
  5. Blood-Brain Barrier (BBB) active efflux and Class B exposure failure
  6. Pharmacodynamic operational Hill transduction (Black & Leff)
  7. Statistical power and contingency table derivations for proposed clinical experiment
"""

import sys
import os
import unittest
import importlib

# Ensure module path is accessible when run directly or via test runner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the drug-discovery_engine module dynamically to support hyphens
engine = importlib.import_module("drug-discovery_engine")

analyze = engine.analyze
CLINICAL_BENCHMARKS = engine.CLINICAL_BENCHMARKS
CompoundProfile = engine.CompoundProfile
CNSDispositionModel = engine.CNSDispositionModel
operational_pathway_response = engine.operational_pathway_response
fisher_exact_2x2 = engine.fisher_exact_2x2
calculate_two_sample_power = engine.calculate_two_sample_power
normal_cdf = engine.normal_cdf
normal_ppf = engine.normal_ppf


class TestDrugDiscoveryEngine(unittest.TestCase):
    """Rigorous verification of the Phase 2 Drug Discovery & Attrition Engine."""

    def test_analyze_contract_schema(self):
        """Property 1: Verify analyze() returns valid schema with required keys and types."""
        res = analyze()
        self.assertIsInstance(res, dict)
        required_keys = {"domain", "claims", "confidence", "evidence"}
        self.assertTrue(required_keys.issubset(res.keys()), f"Missing keys: {required_keys - set(res.keys())}")

        # Check domain
        self.assertEqual(res["domain"], "drug-discovery")

        # Check confidence
        self.assertIsInstance(res["confidence"], (int, float))
        self.assertTrue(0.0 <= res["confidence"] <= 1.0)
        self.assertGreaterEqual(res["confidence"], 0.80)

        # Check claims
        self.assertIsInstance(res["claims"], list)
        self.assertGreaterEqual(len(res["claims"]), 5)
        for claim in res["claims"]:
            self.assertIsInstance(claim, str)
            self.assertGreater(len(claim), 30)

        # Check evidence
        self.assertIsInstance(res["evidence"], list)
        self.assertGreaterEqual(len(res["evidence"]), 5)
        for item in res["evidence"]:
            self.assertIsInstance(item, dict)
            self.assertIn("kind", item)
            self.assertIn("value", item)
            self.assertIn("source", item)

    def test_clinical_attrition_ground_truth(self):
        """Property 2: Verify clinical attrition > 90% overall and Phase II efficacy bottleneck."""
        overall = CLINICAL_BENCHMARKS["Overall_All_Indications"]
        oncology = CLINICAL_BENCHMARKS["Oncology"]

        # Ground truth: attrition > 90% (cumulative LoA < 0.10)
        self.assertLessEqual(overall.cumulative_loa, 0.10, "Cumulative LoA must be <= 10%")
        self.assertGreaterEqual(overall.cumulative_attrition, 0.90, "Cumulative attrition must be > 90%")

        # Phase II efficacy is the primary clinical bottleneck (lowest transition probability among development phases)
        self.assertLess(overall.phase2_pos, overall.phase1_pos)
        self.assertLess(overall.phase2_pos, overall.phase3_pos)
        self.assertLess(overall.phase2_pos, overall.approval_pos)
        self.assertGreater(1.0 - overall.phase2_pos, 0.65, "Phase II attrition must exceed 65%")

        # Oncology has the highest attrition of any major therapeutic area
        self.assertLess(oncology.cumulative_loa, 0.05, "Oncology LoA must be < 5%")
        self.assertGreater(oncology.cumulative_attrition, 0.95, "Oncology attrition must be > 95%")

    def test_alphafold_and_structural_prediction_boundaries(self):
        """Property 3: Verify AlphaFold structural prediction boundaries in evidence."""
        res = analyze()
        af_evidence = next((e for e in res["evidence"] if e["kind"] == "computational_structural_biology_limits"), None)
        self.assertIsNotNone(af_evidence)

        val = af_evidence["value"]
        self.assertIn("alphafold_solved", val)
        self.assertIn("alphafold_unsolved", val)

        # Confirms AlphaFold did not solve binding affinity (Delta G) or ADMET
        unsolved_str = " ".join(val["alphafold_unsolved"]).lower()
        self.assertIn("binding free energy", unsolved_str)
        self.assertIn("admet", unsolved_str)

    def test_lipophilic_trap_and_in_vivo_potency_paradox(self):
        """Property 4: Verify Lipinski rule-of-five compliance, Austin plasma binding, and Waring hERG liability."""
        polar = CompoundProfile(name="Polar", mw=350.0, clogp=1.5, kd_nm=20.0, n_heavy=25)
        greasy = CompoundProfile(name="Greasy", mw=480.0, clogp=4.5, kd_nm=0.5, n_heavy=35)

        # Both satisfy Lipinski Rule-of-Five (MW <= 500, clogP <= 5.0)
        self.assertTrue(polar.mw <= 500.0 and polar.clogp <= 5.0)
        self.assertTrue(greasy.mw <= 500.0 and greasy.clogp <= 5.0)

        # High clogP drastically collapses unbound fraction fu in plasma (Austin 2002)
        self.assertGreater(polar.fu_plasma, greasy.fu_plasma)
        self.assertGreater(polar.fu_plasma / greasy.fu_plasma, 50.0, "fu must drop by >50-fold from clogP 1.5 to 4.5")

        # In vivo potency paradox at equal total plasma concentration (1 uM)
        eval_polar = polar.evaluate_in_vivo_potency(total_plasma_um=1.0)
        eval_greasy = greasy.evaluate_in_vivo_potency(total_plasma_um=1.0)

        # Polar lead achieves higher target occupancy despite 40x weaker in vitro nominal affinity
        self.assertGreater(eval_polar["fractional_occupancy"], eval_greasy["fractional_occupancy"])

        # Lipophilic compound significantly worsens cardiac hERG IC50 (Waring QSAR)
        self.assertLess(eval_greasy["predicted_herg_ic50_um"], eval_polar["predicted_herg_ic50_um"])

        # Lipophilic ligand efficiency (LLE) captures quality
        self.assertGreater(polar.lipophilic_ligand_efficiency, 5.0)

    def test_blood_brain_barrier_efflux_asymmetry(self):
        """Property 5: Verify BBB active efflux mechanics and Class B exposure failure."""
        cns_model = CNSDispositionModel(
            compound_name="CNS_Test",
            kd_nm=15.0,
            ps_passive_ul_min_g=12.0,
            vmax_efflux_pmol_min_g=900.0,
            km_efflux_um=2.0,
            peripheral_toxic_threshold_nm=300.0
        )

        # Calculate Kp,uu,brain across a range of plasma exposures
        kp_uu_low = cns_model.calculate_kp_uu(50.0)
        kp_uu_high = cns_model.calculate_kp_uu(500.0)

        # Active efflux forces Kp,uu << 1.0
        self.assertLess(kp_uu_low, 0.10)
        self.assertLess(kp_uu_high, 0.15)

        # Evaluate feasibility for 80% brain target occupancy
        feasibility = cns_model.evaluate_cns_feasibility(target_occupancy=0.80)
        self.assertTrue(feasibility["class_b_exposure_failure"])
        self.assertGreater(feasibility["required_cu_plasma_nm"], cns_model.peripheral_toxic_threshold_nm)
        self.assertLess(feasibility["max_occupancy_at_mtd"], 0.80)

    def test_operational_pathway_transduction_buffering(self):
        """Property 6: Verify non-linear Black-Leff transduction and pathway buffering."""
        # When EC50_occ = 0.50 and hill = 2.0
        resp_50 = operational_pathway_response(0.50, ec50_occ=0.50, hill_coef=2.0)
        self.assertAlmostEqual(resp_50, 0.50, places=4)

        # High occupancy (90%) produces robust pathway response
        resp_90 = operational_pathway_response(0.90, ec50_occ=0.50, hill_coef=2.0)
        self.assertGreater(resp_90, 0.75)

        # Low occupancy (20%) produces negligible pathway response
        resp_20 = operational_pathway_response(0.20, ec50_occ=0.50, hill_coef=2.0)
        self.assertLess(resp_20, 0.15)

    def test_statistical_power_and_fisher_exact(self):
        """Property 7: Verify statistical power calculations and Fisher exact contingency analysis."""
        # Test normal CDF and inverse normal PPF
        self.assertAlmostEqual(normal_cdf(0.0), 0.50, places=5)
        self.assertAlmostEqual(normal_ppf(0.50), 0.0, places=5)
        self.assertAlmostEqual(normal_ppf(0.975), 1.95996, places=3)

        # Power calculation for N=120 per arm: CNS (45%) vs Systemic (18%)
        power = calculate_two_sample_power(0.45, 0.18, 120, 120, alpha=0.05)
        self.assertGreater(power, 0.90, "Cohort power must exceed 90% with N=120 per arm")

        # Fisher exact test for contingency table [[54, 66], [22, 98]]
        odds_ratio, p_val = fisher_exact_2x2(54, 66, 22, 98)
        self.assertGreater(odds_ratio, 3.0)
        self.assertLess(p_val, 0.001)


if __name__ == "__main__":
    unittest.main()
