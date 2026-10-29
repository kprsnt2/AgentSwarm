"""
Unit Test Suite for Bioelectronic Closed-Loop Engine
===================================================
Tests all modules:
1. Continuous Glucose Monitoring (CGM) Sensor & Interstitial Lag Dynamics
2. Model Predictive Control (MPC) & Closed-Loop Artificial Pancreas
3. Vagus Nerve Stimulation (VNS) & Splenic Inflammatory Reflex
4. Sub-10 nm Zero-Order Nanofluidic Implants & Biofouling Capsule Immunity
5. Multi-Modal Comparative Scaling & Energy Budgets
"""

import unittest
import numpy as np
from bioelectronic_closed_loop_engine import (
    CGMParams,
    CGMSensor,
    MinimalModelParams,
    MPCConfig,
    ModelPredictiveController,
    ArtificialPancreasSimulator,
    VNSFiberParams,
    VNSStimConfig,
    VagusNerveStimulator,
    NanochannelSpecs,
    ImplantReservoirSpecs,
    NanofluidicImplantEvaluator,
    BioelectronicComparativeSynthesis,
    run_full_diagnostic_suite,
)


class TestCGMSensorDynamics(unittest.TestCase):
    """Verifies CGM sensor dynamics, physiological lag, and biofouling drift."""
    
    def setUp(self):
        self.params = CGMParams(tau_lag_min=10.0, noise_sigma_mgdl=3.0)
        self.sensor = CGMSensor(self.params, seed=123)

    def test_interstitial_diffusion_lag_range(self):
        """Physiological ground truth: Interstitial glucose lags blood by 5-15 minutes."""
        self.assertGreaterEqual(self.params.tau_lag_min, 5.0)
        self.assertLessEqual(self.params.tau_lag_min, 15.0)

    def test_step_response_delay(self):
        """Verify 1st order lag response to an instantaneous blood glucose step."""
        self.sensor.g_interstitial = 100.0
        # Instantaneous step to 200 mg/dL
        blood_g = 200.0
        # After 10 min (1 tau), (G_int - G0)/(G_step - G0) should be approx (1 - 1/e) ~ 0.632
        dt = 0.5
        for _ in range(20): # 10 minutes total
            self.sensor.step(blood_g, dt_min=dt, days_implanted=0.0)
            
        fractional_rise = (self.sensor.g_interstitial - 100.0) / (200.0 - 100.0)
        self.assertAlmostEqual(fractional_rise, 1.0 - np.exp(-1.0), delta=0.05)

    def test_biofouling_attenuation_and_lag_increase(self):
        """Biofouling over 90 days reduces sensitivity and dilates lag."""
        retention_0, lag_0 = self.sensor.compute_biofouling_factor(0.0)
        retention_90, lag_90 = self.sensor.compute_biofouling_factor(90.0)
        retention_180, lag_180 = self.sensor.compute_biofouling_factor(180.0)
        
        self.assertEqual(retention_0, 1.0)
        self.assertEqual(lag_0, self.params.tau_lag_min)
        # At 90 days (half-life), sensitivity drops by half of max_biofouling_attenuation (12.5%)
        self.assertAlmostEqual(retention_90, 1.0 - 0.25 * 0.5, places=3)
        self.assertGreater(lag_90, lag_0)
        self.assertGreater(retention_0, retention_180)
        self.assertGreater(lag_180, lag_90)


class TestModelPredictiveController(unittest.TestCase):
    """Verifies MPC safety bounds, asymmetric penalty, and IOB brake."""
    
    def setUp(self):
        self.cfg = MPCConfig(target_glucose=110.0, max_basal_rate_u_hr=6.0, basal_rate_u_hr=1.0)
        self.mp = MinimalModelParams()
        self.mpc = ModelPredictiveController(self.cfg, self.mp)

    def test_iob_calculation(self):
        """IOB in Units must equal (s1_mU + s2_mU) / 1000."""
        s1 = 1500.0 # mU
        s2 = 1000.0 # mU
        iob = self.mpc.calculate_iob(s1, s2)
        self.assertEqual(iob, 2.5)

    def test_asymmetric_hypoglycemia_penalty(self):
        """Predicted glucose < 70 mg/dL must incur dramatically higher cost than hyperglycemia."""
        u_cand = 1.0
        u_prev = 1.0
        # Trajectory 1: 40 mg/dL below target (70 mg/dL, borderline hypo)
        traj_hypo = [60.0] * self.cfg.prediction_horizon
        # Trajectory 2: 40 mg/dL above target (150 mg/dL, moderate hyper)
        traj_hyper = [150.0] * self.cfg.prediction_horizon
        
        cost_hypo = self.mpc.compute_cost(traj_hypo, u_cand, u_prev)
        cost_hyper = self.mpc.compute_cost(traj_hyper, u_cand, u_prev)
        
        self.assertGreater(cost_hypo, cost_hyper * 2.0)

    def test_predictive_low_glucose_suspend(self):
        """When glucose is below 80 mg/dL, dose must be shut off to 0.0 U/hr."""
        dose = self.mpc.optimize_dose(g_cgm=65.0, x_est=0.01, s1_est=500.0, s2_est=500.0,
                                      i_est=15.0, u_prev=1.0)
        self.assertEqual(dose, 0.0)

    def test_dose_bounds(self):
        """Dose must strictly lie within [0.0, max_basal_rate_u_hr]."""
        for g in [50.0, 90.0, 140.0, 220.0, 300.0]:
            dose = self.mpc.optimize_dose(g_cgm=g, x_est=0.005, s1_est=300.0, s2_est=300.0,
                                          i_est=12.0, u_prev=1.0)
            self.assertGreaterEqual(dose, 0.0)
            self.assertLessEqual(dose, self.cfg.max_basal_rate_u_hr)


class TestArtificialPancreasSimulator(unittest.TestCase):
    """Verifies end-to-end 24h closed-loop simulation against clinical benchmarks."""
    
    def test_clinical_benchmarks_tir_and_tbr(self):
        """
        Ground Truth Verification:
        AID keeps patients in target range (70-180 mg/dL) > 70% of the day
        and minimizes hypoglycemia (< 70 mg/dL) < 4%.
        """
        sim = ArtificialPancreasSimulator(seed=42)
        meals = [(420.0, 45.0), (750.0, 70.0), (1140.0, 60.0)]
        res = sim.simulate_24h(meals, days_implanted=7.0)
        
        self.assertGreater(res["TIR_percent"], 70.0, f"TIR was {res['TIR_percent']}%, expected > 70%")
        self.assertLess(res["TBR_percent"], 4.0, f"TBR was {res['TBR_percent']}%, expected < 4%")
        self.assertLess(res["glycemic_cv_percent"], 36.0, "Glycemic CV should be below 36%")

    def test_pump_energy_and_battery(self):
        """Verifies thermodynamic fluid work and electrical battery requirements."""
        sim = ArtificialPancreasSimulator()
        # 40 Units/day typical human dose
        energy_metrics = sim.compute_pump_energy(total_daily_units=40.0, days_operation=30.0)
        
        # Fluid mechanical work should be millijoules/day
        self.assertGreater(energy_metrics["fluid_mech_work_j_per_day"], 0.0)
        self.assertLess(energy_metrics["fluid_mech_work_j_per_day"], 0.01) # < 10 mJ/day
        # Total electrical power should be order of 2-5 Joules/day
        self.assertGreater(energy_metrics["total_j_per_day"], 1.0)
        self.assertLess(energy_metrics["total_j_per_day"], 10.0)
        # Battery capacity for 30 days should be < 50 mAh (very compact rechargeable)
        self.assertLess(energy_metrics["battery_capacity_mah_30d"], 50.0)


class TestVagusNerveStimulator(unittest.TestCase):
    """Verifies bioelectronic VNS, Lapicque-Weiss recruitment, Shannon limit, and cytokine suppression."""
    
    def setUp(self):
        self.vns = VagusNerveStimulator()

    def test_weiss_lapicque_threshold_hierarchy(self):
        """A-fibers have lowest threshold, B-fibers intermediate, C-fibers highest."""
        rec = self.vns.calculate_fiber_recruitment(current_ma=1.0, pw_us=250.0)
        self.assertLess(rec["threshold_A_ma"], rec["threshold_B_ma"])
        self.assertLess(rec["threshold_B_ma"], rec["threshold_C_ma"])

    def test_selective_b_fiber_recruitment(self):
        """At 1.0 mA, 250 us: B-fibers should be predominantly recruited (>90%) while C-fibers remain low."""
        rec = self.vns.calculate_fiber_recruitment(current_ma=1.0, pw_us=250.0)
        self.assertGreater(rec["recruitment_fraction_B"], 0.90)
        self.assertLess(rec["recruitment_fraction_C"], 0.30)

    def test_shannon_limit_compliance(self):
        """
        Validates electrochemical safety:
        k = log10(D) + log10(Q) <= 1.5 to prevent neural damage and electrode corrosion.
        """
        shannon = self.vns.validate_shannon_limit(current_ma=1.0, pw_us=250.0, area_mm2=2.0)
        self.assertTrue(shannon["is_within_safety_limit"])
        self.assertLessEqual(shannon["shannon_k"], 1.5)
        self.assertGreater(shannon["safety_margin_k"], 0.0)

    def test_shannon_limit_violation_detection(self):
        """Excessive current on tiny electrode area must trigger safety violation."""
        shannon_unsafe = self.vns.validate_shannon_limit(current_ma=10.0, pw_us=1000.0, area_mm2=0.1)
        self.assertFalse(shannon_unsafe["is_within_safety_limit"])
        self.assertGreater(shannon_unsafe["shannon_k"], 1.5)

    def test_inflammatory_reflex_suppression(self):
        """
        Ground Truth:
        Efferent vagal activation suppresses peak TNF-alpha release during endotoxin surge.
        """
        # Active VNS
        vns_active = VagusNerveStimulator(VNSStimConfig(pulse_current_ma=1.0, frequency_hz=10.0))
        res_active = vns_active.simulate_inflammatory_suppression(duration_hours=12.0, endotoxin_time_hr=2.0)
        
        # Sham VNS (0 mA)
        vns_sham = VagusNerveStimulator(VNSStimConfig(pulse_current_ma=0.0, frequency_hz=10.0))
        res_sham = vns_sham.simulate_inflammatory_suppression(duration_hours=12.0, endotoxin_time_hr=2.0)
        
        self.assertLess(res_active["peak_tnf_pg_ml"], res_sham["peak_tnf_pg_ml"] * 0.6)
        self.assertLess(res_active["auc_tnf_pg_ml_hr"], res_sham["auc_tnf_pg_ml_hr"] * 0.7)

    def test_battery_longevity(self):
        """Primary hermetic battery (e.g. 350 mAh CFx) must sustain VNS for > 5 years."""
        longevity = self.vns.compute_power_and_battery_life(battery_capacity_mah=350.0, battery_voltage_v=3.2)
        self.assertGreater(longevity["battery_lifetime_years"], 5.0)
        self.assertLess(longevity["average_power_microwatts"], 50.0)


class TestNanofluidicImplantEvaluator(unittest.TestCase):
    """Verifies sub-10 nm slit zero-order release, FBR capsule immunity, and titanium casing."""
    
    def setUp(self):
        self.evaluator = NanofluidicImplantEvaluator()

    def test_steric_confinement_factor(self):
        """Hydrodynamic diameter approaching slit height reduces diffusivity via Renkin-Deen."""
        phi, d_eff = self.evaluator.compute_hindered_diffusivity()
        self.assertGreater(phi, 0.0)
        self.assertLess(phi, 1.0)
        self.assertLess(d_eff, self.evaluator.nano.drug_bulk_diffusivity_m2_s)

    def test_zero_order_release_magnitude(self):
        """Calculates release rate for peptide payload (order of 0.05 - 1.0 mg/day)."""
        rel = self.evaluator.calculate_zero_order_release_rate()
        self.assertGreater(rel["daily_release_mg_day"], 0.01)
        self.assertLess(rel["daily_release_mg_day"], 5.0)

    def test_biofouling_capsule_immunity_proof(self):
        """
        Physical Law Verification:
        R_nano >> R_capsule ensures > 99% flux stability despite fibrous encapsulation.
        """
        bio = self.evaluator.evaluate_biofouling_impact()
        self.assertTrue(bio["is_zero_order_preserved"])
        self.assertGreater(bio["flux_retention_fraction"], 0.99)
        self.assertLess(bio["resistance_ratio_capsule_to_nano"], 0.01)

    def test_titanium_reservoir_sizing_12_months(self):
        """Titanium Grade 5 implant sizing for 12 months continuous zero-order delivery."""
        res = self.evaluator.size_reservoir(duration_months=12.0)
        self.assertTrue(res["is_clinically_feasible"])
        self.assertLess(res["total_length_mm"], 60.0) # Subcutaneous length under 6 cm
        self.assertLess(res["reservoir_volume_ml"], 2.0) # Internal volume under 2 mL
        self.assertGreater(res["burst_pressure_bar"], 500.0) # Structural factor of safety


class TestComparativeSynthesisAndDiagnostics(unittest.TestCase):
    """Verifies cross-modality comparative synthesis and end-to-end diagnostic runner."""
    
    def test_comparative_table_structure(self):
        table = BioelectronicComparativeSynthesis.generate_comparative_table()
        self.assertIn("Closed_Loop_AID_Artificial_Pancreas", table)
        self.assertIn("Bioelectronic_Vagus_Nerve_Stimulation", table)
        self.assertIn("Nanofluidic_Passive_Zero_Order_Implant", table)
        for _, modality in table.items():
            self.assertTrue(modality["zero_tablet_compliance"])

    def test_full_diagnostic_suite(self):
        diag = run_full_diagnostic_suite()
        self.assertIn("artificial_pancreas", diag)
        self.assertIn("bioelectronic_vns", diag)
        self.assertIn("nanofluidic_implant", diag)
        self.assertIn("comparative_table", diag)


if __name__ == "__main__":
    unittest.main()
