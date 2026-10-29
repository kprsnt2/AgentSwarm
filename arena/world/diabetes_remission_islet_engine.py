"""
diabetes_remission_islet_engine.py

Comprehensive Computational Engine for:
1. Type 2 Diabetes Remission Biophysics (Twin Cycle Hypothesis, Taylor et al., DiRECT trial)
2. Stem-Cell Derived Islet Encapsulation & Transport Biophysics (T1D curative frontiers, Krogh/Reaction-Diffusion)
3. Autoimmune Interception Dynamics (Anti-CD3 Monoclonal Antibody Teplizumab, TrialNet TN-10)
4. Cross-Modality Curative & Remission Comparative Frontier Synthesis

Author: Kepler (A001) - Autonomous Research Agent
Epistemic Class: Empirical
Standard of Evidence: Quantitative, peer-reviewed clinical benchmarks, exact conservation laws.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar


# ==============================================================================
# SECTION 1: TYPE 2 DIABETES BIOPHYSICS & THE TWIN CYCLE ENGINE
# ==============================================================================

@dataclass
class TwinCycleParameters:
    """
    Biophysical parameters for the Twin Cycle Hypothesis of Type 2 Diabetes remission.
    Calibrated against Taylor et al., DiRECT trial (Lancet 2018, 2019), Counterbalance (2016),
    and ReTUNE (2021).
    """
    # Baseline physiological states
    baseline_weight_kg: float = 100.0          # Initial patient weight (kg)
    baseline_ihtg_pct: float = 16.0            # Intrahepatic triacylglycerol (%) [Normal: < 5.56%]
    baseline_iptg_pct: float = 8.5             # Intrapancreatic triacylglycerol (%) [Normal: < 5.5-6.0%]
    baseline_fpg_mmol: float = 9.2             # Fasting plasma glucose (mmol/L) [Diabetic: >= 7.0]
    baseline_airg_nmol: float = 0.04           # Acute first-phase insulin response (nmol/L) [Normal: > 0.4]
    
    # Kinetic rate constants
    k_clear_ihtg_day: float = 0.22             # Rapid liver TAG clearance rate on ~800 kcal/day (t1/2 ~ 3.15 days)
    ihtg_residual_pct: float = 2.5             # Asymptotic liver fat floor on negative energy balance (%)
    ihtg_ceiling_pct: float = 35.0             # Biological saturation ceiling for liver fat (%)
    
    k_clear_iptg_day: float = 0.028            # Slower pancreatic TAG clearance rate (t1/2 ~ 25 days / ~3.5 weeks)
    iptg_residual_pct: float = 5.2             # Asymptotic pancreatic fat floor (%)
    iptg_ceiling_pct: float = 12.0             # Biological saturation ceiling for intrapancreatic fat (%)
    
    # Thresholds
    ihtg_norm_thresh: float = 5.56             # Upper limit of normal intrahepatic fat (%)
    iptg_lipotox_thresh: float = 5.8           # Lipotoxicity threshold for beta-cell dedifferentiation (%)
    
    # Hepatic glucose production (HGP) coupling
    hgp_basal_normal: float = 10.0             # Normal basal HGP (umol/kg/min)
    hgp_overproduction_slope: float = 0.45      # HGP elevation per % IHTG above normal
    
    # Beta-cell recovery dynamics
    beta_recovery_rate_day: float = 0.035      # Rate of beta-cell redifferentiation once IPTG < threshold
    disease_duration_years: float = 3.0        # Duration of diagnosed T2D
    tau_irreversible_years: float = 7.5        # Characteristic timescale of irreversible beta-cell apoptosis


@dataclass
class TwinCycleTrajectory:
    """Simulation trajectory results from Twin Cycle Model."""
    time_days: np.ndarray
    weight_kg: np.ndarray
    ihtg_pct: np.ndarray
    iptg_pct: np.ndarray
    fpg_mmol: np.ndarray
    airg_nmol: np.ndarray
    remission_achieved: bool
    hba1c_est_pct: np.ndarray
    vldl_triglycerides_mmol: np.ndarray


class TwinCycleModel:
    """
    Coupled ODE engine simulating the Twin Cycle Hypothesis:
    - Liver cycle: Rapid negative energy balance -> rapid intrahepatic fat clearance ->
      normalization of hepatic insulin sensitivity & hepatic glucose production -> rapid drop in FPG (7-14 days).
    - Pancreas cycle: Fall in VLDL-TAG delivery -> progressive intrapancreatic fat clearance ->
      relief of beta-cell lipotoxicity -> restoration of acute first-phase insulin secretion (AIRg) by 8-16 weeks.
    """

    def __init__(self, params: Optional[TwinCycleParameters] = None):
        self.params = params or TwinCycleParameters()

    def simulate_dietary_remission(
        self,
        duration_days: int = 140,
        daily_deficit_kcal: float = 1200.0,
        diet_energy_kcal: float = 850.0
    ) -> TwinCycleTrajectory:
        """
        Simulate an intensive dietary intervention (e.g. DiRECT 825-853 kcal/day low-energy diet for 20 weeks).
        Weight loss modeled via energy balance (Hall et al. 7700 kcal/kg adipose-lean tissue mix with metabolic adaptation).
        """
        t_span = (0.0, float(duration_days))
        t_eval = np.linspace(0.0, float(duration_days), duration_days + 1)
        
        # Initial conditions: [Weight, IHTG, IPTG, AIRg]
        y0 = [
            self.params.baseline_weight_kg,
            self.params.baseline_ihtg_pct,
            self.params.baseline_iptg_pct,
            self.params.baseline_airg_nmol
        ]
        
        # Energy equivalent of body weight loss
        kg_per_kcal = 1.0 / 7700.0

        # Irreversible beta cell loss fraction based on diabetes duration
        f_irreversible = 1.0 - np.exp(-self.params.disease_duration_years / self.params.tau_irreversible_years)
        max_recoverable_airg = 0.65 * (1.0 - f_irreversible)  # Normal healthy AIRg is ~0.6-0.8 nmol/L

        def derivatives(t, y):
            w, ihtg, iptg, airg = y
            
            # Weight dynamics (diminishing loss rate due to metabolic adaptation)
            adapt_factor = np.exp(-t / 180.0)
            dw_dt = - (daily_deficit_kcal * kg_per_kcal) * (0.6 + 0.4 * adapt_factor)
            
            # Liver cycle: Rapid first-order clearance towards floor
            dihtg_dt = - self.params.k_clear_ihtg_day * (ihtg - self.params.ihtg_residual_pct)
            
            # Pancreas cycle: clearance begins as liver fat normalizes and VLDL export drops
            vldl_inflow = 0.01 * (ihtg / self.params.ihtg_norm_thresh)
            diptg_dt = - self.params.k_clear_iptg_day * (iptg - self.params.iptg_residual_pct) + vldl_inflow * 0.1
            
            # Beta cell recovery: triggers once IPTG falls below lipotoxic threshold
            if iptg < self.params.iptg_lipotox_thresh:
                dairg_dt = self.params.beta_recovery_rate_day * (max_recoverable_airg - airg)
            else:
                dairg_dt = - 0.002 * airg  # Continued slow lipotoxic decline
                
            return [dw_dt, dihtg_dt, diptg_dt, dairg_dt]

        sol = solve_ivp(derivatives, t_span, y0, t_eval=t_eval, method='RK45')
        
        w_arr = sol.y[0]
        ihtg_arr = sol.y[1]
        iptg_arr = sol.y[2]
        airg_arr = sol.y[3]
        
        # Fasting Plasma Glucose (FPG) directly mirrors Hepatic Glucose Production (HGP)
        # In DiRECT & Counterbalance, FPG drops from ~9.2 mmol/L to normal within 7-14 days as IHTG normalizes
        hgp_excess_0 = max(1e-6, (self.params.baseline_ihtg_pct - self.params.ihtg_norm_thresh) * self.params.hgp_overproduction_slope)
        hgp_excess = np.maximum(0.0, (ihtg_arr - self.params.ihtg_norm_thresh) * self.params.hgp_overproduction_slope)
        fpg_arr = 5.2 + (self.params.baseline_fpg_mmol - 5.2) * (0.85 * (hgp_excess / hgp_excess_0) + 0.15 * np.exp(-sol.t / 7.0))
        
        # Estimated HbA1c based on Nathan et al. formula: eAG (mmol/L) = 1.59 * HbA1c - 2.59
        # Smoothed over ~60-90 days erythrocyte lifespan
        hba1c_arr = np.zeros_like(fpg_arr)
        hba1c_arr[0] = (self.params.baseline_fpg_mmol + 2.59) / 1.59
        for i in range(1, len(fpg_arr)):
            dt = sol.t[i] - sol.t[i-1]
            target_a1c = (fpg_arr[i] + 2.59) / 1.59
            hba1c_arr[i] = hba1c_arr[i-1] + (target_a1c - hba1c_arr[i-1]) * (dt / 45.0)
            
        # VLDL triglycerides (mmol/L)
        vldl_arr = 0.8 + 0.08 * ihtg_arr
        
        # Remission criteria (DiRECT): HbA1c < 6.5% (< 48 mmol/mol), FPG < 7.0 mmol/L, and restored AIRg > 0.20 nmol/L
        final_remission = bool(hba1c_arr[-1] < 6.5 and fpg_arr[-1] < 7.0 and airg_arr[-1] > 0.20)
        
        return TwinCycleTrajectory(
            time_days=sol.t,
            weight_kg=w_arr,
            ihtg_pct=ihtg_arr,
            iptg_pct=iptg_arr,
            fpg_mmol=fpg_arr,
            airg_nmol=airg_arr,
            remission_achieved=final_remission,
            hba1c_est_pct=hba1c_arr,
            vldl_triglycerides_mmol=vldl_arr
        )

    def simulate_weight_regain_relapse(
        self,
        remission_traj: TwinCycleTrajectory,
        regain_duration_days: int = 365,
        daily_surplus_kcal: float = 350.0
    ) -> Dict[str, Any]:
        """
        Simulates the 'reverse route' (Al-Mrabeh et al. 2020):
        Weight regain re-saturates subcutaneous storage, triggering renewed ectopic overflow
        into liver (IHTG rises -> VLDL-TAG export rises), leading to intrapancreatic re-steatosis,
        loss of first-phase insulin response, and diabetes relapse.
        Both liver and pancreatic fat are bounded by biological ceilings.
        """
        t_eval = np.linspace(0.0, float(regain_duration_days), regain_duration_days + 1)
        w0 = remission_traj.weight_kg[-1]
        ihtg0 = remission_traj.ihtg_pct[-1]
        iptg0 = remission_traj.iptg_pct[-1]
        airg0 = remission_traj.airg_nmol[-1]
        
        kg_per_kcal = 1.0 / 7700.0
        
        def relapse_derivs(t, y):
            w, ihtg, iptg, airg = y
            # Weight increases with caloric surplus
            dw_dt = (daily_surplus_kcal * kg_per_kcal)
            
            # Liver re-accumulation of fat (saturates near biological ceiling)
            weight_gain = w - w0
            spillover_drive = max(0.0, weight_gain * 0.8)
            dihtg_dt = 0.08 * spillover_drive * max(0.0, 1.0 - ihtg / self.params.ihtg_ceiling_pct) - 0.015 * (ihtg - self.params.ihtg_residual_pct)
            
            # Pancreatic fat accumulation driven by elevated liver fat (VLDL-TAG delivery)
            vldl_export = max(0.0, ihtg - self.params.ihtg_norm_thresh) * 0.05
            diptg_dt = vldl_export * max(0.0, 1.0 - iptg / self.params.iptg_ceiling_pct) - 0.008 * (iptg - self.params.iptg_residual_pct)
            
            # AIRg declines if IPTG rises above lipotoxic threshold
            if iptg > self.params.iptg_lipotox_thresh:
                dairg_dt = - 0.015 * (iptg - self.params.iptg_lipotox_thresh) * airg
            else:
                dairg_dt = 0.0
                
            return [dw_dt, dihtg_dt, diptg_dt, dairg_dt]
            
        sol = solve_ivp(relapse_derivs, (0.0, float(regain_duration_days)), [w0, ihtg0, iptg0, airg0], t_eval=t_eval, method='RK45')
        
        w_arr = sol.y[0]
        ihtg_arr = sol.y[1]
        iptg_arr = sol.y[2]
        airg_arr = sol.y[3]
        
        hgp_excess = np.maximum(0.0, (ihtg_arr - self.params.ihtg_norm_thresh) * self.params.hgp_overproduction_slope)
        fpg_arr = 5.2 + 0.35 * hgp_excess + np.maximum(0.0, (0.3 - airg_arr) * 4.0)
        
        return {
            "time_days": sol.t,
            "weight_kg": w_arr,
            "ihtg_pct": ihtg_arr,
            "iptg_pct": iptg_arr,
            "airg_nmol": airg_arr,
            "fpg_mmol": fpg_arr,
            "relapsed": bool(fpg_arr[-1] >= 7.0 or airg_arr[-1] < 0.15)
        }


class PersonalFatThreshold:
    """
    Personal Fat Threshold (PFT) model (Taylor & Holman 2015, ReTUNE 2021).
    Explains why individuals with normal BMI (< 25 kg/m^2) can develop T2D:
    Ectopic fat overflow occurs when individual subcutaneous adipose tissue (SAT) storage capacity is exceeded.
    """

    @staticmethod
    def calculate_ectopic_overflow(
        bmi: float,
        personal_sat_capacity_bmi: float,
        body_fat_pct: float
    ) -> Dict[str, float]:
        """
        Quantify ectopic fat spillover when current adiposity exceeds personal threshold.
        """
        delta_bmi = bmi - personal_sat_capacity_bmi
        is_overflowing = delta_bmi > 0.0
        
        if is_overflowing:
            liver_spillover_pct = 5.5 + 2.8 * delta_bmi
            pancreas_spillover_pct = 5.5 + 0.85 * delta_bmi
            visceral_fat_mass_kg = 1.5 + 0.45 * delta_bmi
        else:
            liver_spillover_pct = max(1.5, 5.0 + 1.2 * delta_bmi)
            pancreas_spillover_pct = max(3.5, 5.2 + 0.4 * delta_bmi)
            visceral_fat_mass_kg = max(0.8, 1.2 + 0.2 * delta_bmi)
            
        return {
            "bmi": bmi,
            "sat_capacity_bmi": personal_sat_capacity_bmi,
            "overflow_delta_bmi": delta_bmi,
            "in_ectopic_overflow": is_overflowing,
            "estimated_ihtg_pct": liver_spillover_pct,
            "estimated_iptg_pct": pancreas_spillover_pct,
            "estimated_vat_kg": visceral_fat_mass_kg
        }

    @staticmethod
    def direct_remission_probability(weight_loss_kg: float, diabetes_duration_years: float) -> float:
        """
        Calculates empirical remission probability based on DiRECT trial data:
        - Weight loss < 5 kg: ~7-9%
        - 5 - 10 kg: ~34%
        - 10 - 15 kg: ~57%
        - >= 15 kg: ~86%
        Adjusted downward for prolonged diabetes duration (> 6 years).
        """
        beta_0 = -2.60
        beta_weight = 0.27
        beta_duration = -0.18
        
        logit = beta_0 + beta_weight * weight_loss_kg + beta_duration * diabetes_duration_years
        prob = 1.0 / (1.0 + np.exp(-logit))
        return float(np.clip(prob, 0.01, 0.95))


# ==============================================================================
# SECTION 2: STEM CELL ISLET ENCAPSULATION & TRANSPORT BIOPHYSICS (T1D)
# ==============================================================================

@dataclass
class IsletTransportParameters:
    """
    Biophysical constants for oxygen, glucose, and insulin transport in islets & encapsulation media.
    Literature benchmarks: Papas et al. (2007, 2016), Colton (2014), Avgoustiniatos et al. (2008), Vegas et al. (2016).
    """
    # Islet Equivalent (IEQ) standard: sphere of diameter 150 um (radius 75 um, ~1560 cells)
    islet_radius_cm: float = 75.0e-4           # 75 um = 0.0075 cm
    
    # Oxygen Consumption Rate (OCR) per IEQ
    # Papas et al. benchmarks: ~3.0 - 4.5 pmol/min/IEQ (corresponding to ~2.5 - 3.8 fmol/min/cell)
    # Basal: ~2.5 pmol/min/IEQ; Stimulated (high glucose): ~4.5 pmol/min/IEQ = 7.50e-14 mol/s
    ocr_stimulated_mol_per_s_ieq: float = 7.50e-14  # 4.5 pmol/min = 7.50e-14 mol/s
    ocr_basal_mol_per_s_ieq: float = 4.167e-14       # 2.5 pmol/min = 4.167e-14 mol/s
    
    # Henry's law solubility of O2 at 37 deg C in saline/tissue (mol / (cm^3 * mmHg))
    solubility_o2: float = 1.35e-9             # 1.35 umol / (L * mmHg) = 1.35e-9 mol/(cm^3 * mmHg)
    
    # Oxygen diffusion coefficients (cm^2 / s)
    d_o2_islet: float = 1.50e-5                # Dense cellular islet tissue
    d_o2_alginate: float = 2.00e-5             # Hydrogel matrix
    d_o2_membrane: float = 0.80e-5             # Semi-permeable synthetic membrane (pores 0.1-0.4 um)
    d_o2_fibrotic_scar: float = 0.70e-5        # Dense avascular pericapsular collagenous tissue
    
    # Michaelis-Menten & Hill kinetics
    km_o2_mmhg: float = 0.20                   # Km for cytochrome c oxidase (~0.2 mmHg)
    p50_gsis_mmhg: float = 10.0                # pO2 for 50% maximal GSIS (Papas et al. 2007)
    hill_coeff_gsis: float = 3.0               # Hill cooperativity coefficient for GSIS oxygen dependence
    
    # Viability & functional thresholds
    po2_anoxia_threshold_mmhg: float = 0.5     # Necrosis occurs below ~0.1-0.5 mmHg
    po2_hypoxia_impairment_mmhg: float = 10.0  # Hypoxia stress & ATP depletion below 10 mmHg
    po2_gsis_competent_mmhg: float = 20.0      # Glucose-stimulated insulin secretion fully functional
    
    # Physiological host tissue pO2 (mmHg)
    po2_subcutaneous_mmhg: float = 35.0        # Subcutaneous space (poorly vascularized)
    po2_intraperitoneal_mmhg: float = 45.0     # Omentum / peritoneal fluid
    po2_intraportal_liver_mmhg: float = 50.0   # Native hepatic sinusoid environment


class IsletMicroencapsulationModel:
    """
    Exact analytical and numerical solver for spherical microencapsulation (single islet inside alginate bead).
    Solves steady-state reaction-diffusion equation with exact Krogh free-boundary anoxic core:
      D_islet * (1/r^2) * d/dr(r^2 * dp/dr) = q_p             [r_0 <= r <= R_islet]
      dp/dr = 0, p(r) = 0                                     [0 <= r <= r_0]
      D_alg * (1/r^2) * d/dr(r^2 * dp/dr) = 0                 [R_islet < r <= R_bead]
      D_fib * (1/r^2) * d/dr(r^2 * dp/dr) = 0                 [R_bead < r <= R_bead + delta_fib]
    """

    def __init__(self, params: Optional[IsletTransportParameters] = None):
        self.params = params or IsletTransportParameters()
        
        # Calculate volumetric V_max for an IEQ
        islet_volume_cm3 = (4.0 / 3.0) * np.pi * (self.params.islet_radius_cm ** 3)
        self.vmax_o2_mol_cm3_s = self.params.ocr_stimulated_mol_per_s_ieq / islet_volume_cm3

    def solve_oxygen_profile_analytical(
        self,
        capsule_radius_um: float = 250.0,
        fibrotic_thickness_um: float = 0.0,
        host_tissue_po2_mmhg: float = 35.0
    ) -> Dict[str, float]:
        """
        Exact free-boundary analytical solution for spherical microcapsule.
        Correctly models the vanishing of consumption inside an anoxic core (r <= r_0),
        yielding exact physical non-negative pO2 profiles, viable volume fractions, and GSIS capacity.
        """
        r_i = self.params.islet_radius_cm
        r_c = capsule_radius_um * 1.0e-4
        r_f = (capsule_radius_um + fibrotic_thickness_um) * 1.0e-4
        
        # Volumetric consumption rate in terms of pO2 driving force: q_p = V_max / alpha_O2 [mmHg / s]
        q_p = self.vmax_o2_mol_cm3_s / self.params.solubility_o2
        
        # Transport resistances outside islet (mmHg * s / cm^3):
        # Drop across alginate: Delta_p_alg = q_p * (r_i^3 - r_0^3) / (3 * D_alg) * (1/r_i - 1/r_c)
        # Drop across scar:     Delta_p_fib = q_p * (r_i^3 - r_0^3) / (3 * D_fib) * (1/r_c - 1/r_f)
        k_ext = (1.0 / self.params.d_o2_alginate) * (1.0 / r_i - 1.0 / r_c)
        if fibrotic_thickness_um > 0.0:
            k_ext += (1.0 / self.params.d_o2_fibrotic_scar) * (1.0 / r_c - 1.0 / r_f)
            
        def host_po2_for_anoxic_radius(r0: float) -> float:
            """Calculates host tissue pO2 required to maintain an anoxic core of radius r0."""
            # Inside islet shell [r0, r_i]: p(r_i) = (q_p / (6 * D_islet)) * (r_i^2 - 3*r0^2 + 2*r0^3/r_i)
            p_surf = (q_p / (6.0 * self.params.d_o2_islet)) * (r_i ** 2 - 3.0 * (r0 ** 2) + 2.0 * (r0 ** 3) / r_i)
            # External drop:
            p_ext = (q_p * (r_i ** 3 - r0 ** 3) / 3.0) * k_ext
            return p_surf + p_ext

        # Threshold host pO2 to prevent any anoxia (r0 = 0):
        p_host_thresh = host_po2_for_anoxic_radius(0.0)
        
        # Theoretical zero-order unconstrained core pO2
        delta_p_fib_unconstrained = (q_p * (r_i ** 3) / (3.0 * self.params.d_o2_fibrotic_scar)) * (1.0 / r_c - 1.0 / r_f) if fibrotic_thickness_um > 0 else 0.0
        delta_p_alg_unconstrained = (q_p * (r_i ** 3) / (3.0 * self.params.d_o2_alginate)) * (1.0 / r_i - 1.0 / r_c)
        delta_p_internal_unconstrained = q_p * (r_i ** 2) / (6.0 * self.params.d_o2_islet)
        theoretical_zero_order_core_po2 = host_tissue_po2_mmhg - delta_p_fib_unconstrained - delta_p_alg_unconstrained - delta_p_internal_unconstrained

        if host_tissue_po2_mmhg >= p_host_thresh:
            # Completely viable islet! (r0 = 0)
            r_anox = 0.0
            delta_p_fib = delta_p_fib_unconstrained
            delta_p_alg = delta_p_alg_unconstrained
            p_capsule_surface = host_tissue_po2_mmhg - delta_p_fib
            p_islet_surface = p_capsule_surface - delta_p_alg
            core_po2 = p_islet_surface - delta_p_internal_unconstrained
            anoxic_vol_fraction = 0.0
            viable_vol_fraction = 1.0
        else:
            # Anoxic core exists (r0 > 0)
            core_po2 = 0.0
            # Solve for r_anox in (0, r_i)
            try:
                res = root_scalar(lambda r: host_po2_for_anoxic_radius(r) - host_tissue_po2_mmhg, bracket=[0.0, r_i], method='brentq')
                r_anox = float(res.root)
            except Exception:
                r_anox = r_i
                
            anoxic_vol_fraction = (r_anox / r_i) ** 3
            viable_vol_fraction = max(0.0, 1.0 - anoxic_vol_fraction)
            
            # Recalculate actual drops with reduced consumption
            q_active = q_p * (r_i ** 3 - r_anox ** 3)
            delta_p_fib = (q_active / (3.0 * self.params.d_o2_fibrotic_scar)) * (1.0 / r_c - 1.0 / r_f) if fibrotic_thickness_um > 0 else 0.0
            delta_p_alg = (q_active / (3.0 * self.params.d_o2_alginate)) * (1.0 / r_i - 1.0 / r_c)
            p_capsule_surface = host_tissue_po2_mmhg - delta_p_fib
            p_islet_surface = p_capsule_surface - delta_p_alg

        # Thiele modulus Phi_0 for zero-order spherical kinetics
        if p_islet_surface > 0:
            thiele_modulus = r_i * np.sqrt(q_p / (6.0 * self.params.d_o2_islet * p_islet_surface))
        else:
            thiele_modulus = 999.0

        # Functional GSIS capacity integration:
        # GSIS(p) = p^n / (p50^n + p^n) integrated across viable shell
        n_pts = 60
        r_grid = np.linspace(r_anox, r_i, n_pts)
        trapz_fn = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
        if viable_vol_fraction > 0 and p_islet_surface > 0:
            if r_anox > 0.0:
                # Anoxic core present: p(r) = (q_p / (6 * D)) * (r^2 - 3*r0^2 + 2*r0^3/r)
                p_r = (q_p / (6.0 * self.params.d_o2_islet)) * (r_grid ** 2 - 3.0 * (r_anox ** 2) + (2.0 * (r_anox ** 3) / np.maximum(r_grid, 1e-12)))
            else:
                # Fully viable islet: center pO2 is core_po2 > 0
                p_r = core_po2 + (q_p / (6.0 * self.params.d_o2_islet)) * (r_grid ** 2)
            p_r = np.maximum(0.0, p_r)
            gsis_r = (p_r ** self.params.hill_coeff_gsis) / (self.params.p50_gsis_mmhg ** self.params.hill_coeff_gsis + p_r ** self.params.hill_coeff_gsis)
            # Volume-weighted integral: (3 / r_i^3) * \int r^2 gsis(r) dr
            integral = trapz_fn(r_grid ** 2 * gsis_r, r_grid)
            gsis_competent_fraction = (3.0 / (r_i ** 3)) * integral
        else:
            gsis_competent_fraction = 0.0

        return {
            "capsule_radius_um": capsule_radius_um,
            "fibrotic_thickness_um": fibrotic_thickness_um,
            "host_tissue_po2_mmhg": host_tissue_po2_mmhg,
            "delta_p_fibrosis_mmhg": float(delta_p_fib),
            "delta_p_alginate_mmhg": float(delta_p_alg),
            "islet_surface_po2_mmhg": float(p_islet_surface),
            "core_po2_mmhg": float(core_po2),
            "theoretical_zero_order_core_po2_mmhg": float(theoretical_zero_order_core_po2),
            "anoxic_core_radius_um": float(r_anox * 1.0e4),
            "thiele_modulus": float(thiele_modulus),
            "effectiveness_factor": float(viable_vol_fraction),
            "viable_fraction": float(np.clip(viable_vol_fraction, 0.0, 1.0)),
            "gsis_competent_fraction": float(np.clip(gsis_competent_fraction, 0.0, 1.0))
        }


class MacroencapsulationDeviceModel:
    """
    Planar macroencapsulation chamber biophysical model (e.g. Vertex VX-264, Viacyte PEC-Encap, Theracyte).
    Evaluates 1D planar reaction-diffusion through device membrane, islet chamber, and pericapsular fibrotic halo.
    Solves for maximum allowable packing density, exact viable thickness, and human therapeutic footprint.
    """

    def __init__(self, params: Optional[IsletTransportParameters] = None):
        self.params = params or IsletTransportParameters()
        islet_volume_cm3 = (4.0 / 3.0) * np.pi * (self.params.islet_radius_cm ** 3)
        self.vmax_o2_islet_mol_cm3_s = self.params.ocr_stimulated_mol_per_s_ieq / islet_volume_cm3

    def compute_planar_oxygenation(
        self,
        chamber_half_thickness_um: float = 125.0,     # Device chamber thickness 2L = 250 um
        membrane_thickness_um: float = 25.0,          # Immunoprotective semipermeable membrane
        fibrotic_capsule_um: float = 40.0,            # Pericapsular fibrotic sheath
        islet_volume_fraction: float = 0.05,          # Packing density (5% volume occupied by islets)
        host_tissue_po2_mmhg: float = 35.0            # Subcutaneous bed
    ) -> Dict[str, float]:
        """
        Calculates midplane pO2, viable chamber fraction, and concentration gradient across planar macrodevice.
        Uses exact free-boundary solver: when midplane is anoxic, consumption is zero in anoxic zone.
        """
        l_chamber = chamber_half_thickness_um * 1.0e-4
        l_mem = membrane_thickness_um * 1.0e-4
        l_fib = fibrotic_capsule_um * 1.0e-4
        phi = islet_volume_fraction
        
        # Effective volumetric OCR in the chamber (mol / cm^3 / s)
        vmax_eff = phi * self.vmax_o2_islet_mol_cm3_s
        q_p_eff = vmax_eff / self.params.solubility_o2  # in mmHg / s
        
        # Effective diffusivity in hydrogel suspension: D_eff ~ D_alg * (1 - phi) + D_islet * phi
        d_eff = (1.0 - phi) * self.params.d_o2_alginate + phi * self.params.d_o2_islet

        # External resistance term (membrane + fibrotic scar):
        k_ext = (l_mem / self.params.d_o2_membrane) + (l_fib / self.params.d_o2_fibrotic_scar if l_fib > 0 else 0.0)
        
        # Minimum host pO2 required for 100% viable chamber (midplane pO2 = 0):
        # p_req_full = (q_p_eff / (2 * D_eff)) * L^2 + q_p_eff * L * k_ext
        p_req_full = (q_p_eff / (2.0 * d_eff)) * (l_chamber ** 2) + q_p_eff * l_chamber * k_ext
        
        theoretical_zero_order_midplane = host_tissue_po2_mmhg - p_req_full

        if host_tissue_po2_mmhg >= p_req_full:
            # Completely viable chamber!
            midplane_po2 = host_tissue_po2_mmhg - p_req_full
            viable_thickness_cm = l_chamber
            viable_fraction = 1.0
            is_anoxic = False
            flux = q_p_eff * l_chamber
        else:
            # Anoxic midplane core! Free boundary: solve A * lambda^2 + B * lambda - p_host = 0
            is_anoxic = True
            midplane_po2 = 0.0
            a_coeff = q_p_eff / (2.0 * d_eff)
            b_coeff = q_p_eff * k_ext
            discriminant = b_coeff ** 2 + 4.0 * a_coeff * host_tissue_po2_mmhg
            viable_thickness_cm = (-b_coeff + np.sqrt(discriminant)) / (2.0 * a_coeff)
            viable_fraction = viable_thickness_cm / l_chamber
            flux = q_p_eff * viable_thickness_cm

        # Drops across external layers:
        delta_p_fib = (flux * l_fib / self.params.d_o2_fibrotic_scar) if l_fib > 0 else 0.0
        delta_p_mem = flux * l_mem / self.params.d_o2_membrane
        p_chamber_edge = host_tissue_po2_mmhg - delta_p_fib - delta_p_mem
        delta_p_chamber = p_chamber_edge - midplane_po2

        # GSIS functional fraction across chamber
        n_pts = 60
        trapz_fn = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
        if viable_fraction > 0 and p_chamber_edge > 0:
            if not is_anoxic:
                # Fully viable chamber: midplane pO2 > 0
                x_grid = np.linspace(0.0, l_chamber, n_pts)
                p_x = midplane_po2 + (q_p_eff / (2.0 * d_eff)) * (x_grid ** 2)
                gsis_x = (p_x ** self.params.hill_coeff_gsis) / (self.params.p50_gsis_mmhg ** self.params.hill_coeff_gsis + p_x ** self.params.hill_coeff_gsis)
                gsis_fraction = (1.0 / l_chamber) * trapz_fn(gsis_x, x_grid)
            else:
                # Partially anoxic midplane: anoxic zone [0, l_chamber - viable_thickness_cm] has 0 GSIS
                u_grid = np.linspace(0.0, viable_thickness_cm, n_pts)
                p_u = (q_p_eff / (2.0 * d_eff)) * (u_grid ** 2)
                gsis_u = (p_u ** self.params.hill_coeff_gsis) / (self.params.p50_gsis_mmhg ** self.params.hill_coeff_gsis + p_u ** self.params.hill_coeff_gsis)
                gsis_fraction = (1.0 / l_chamber) * trapz_fn(gsis_u, u_grid)
        else:
            gsis_fraction = 0.0

        # Therapeutic human dose: 500,000 IEQ (~5,000 IEQ / kg for 100 kg human)
        vol_one_ieq_cm3 = (4.0 / 3.0) * np.pi * (self.params.islet_radius_cm ** 3)
        total_islet_volume_cm3 = 500000.0 * vol_one_ieq_cm3  # ~0.88 cm^3
        chamber_vol_cm3 = total_islet_volume_cm3 / phi
        device_footprint_cm2 = chamber_vol_cm3 / (2.0 * l_chamber)

        return {
            "packing_density_phi": phi,
            "chamber_half_thickness_um": chamber_half_thickness_um,
            "fibrotic_thickness_um": fibrotic_capsule_um,
            "midplane_po2_mmhg": float(midplane_po2),
            "theoretical_zero_order_midplane_mmhg": float(theoretical_zero_order_midplane),
            "chamber_edge_po2_mmhg": float(p_chamber_edge),
            "delta_p_fibrosis_mmhg": float(delta_p_fib),
            "delta_p_membrane_mmhg": float(delta_p_mem),
            "delta_p_chamber_mmhg": float(delta_p_chamber),
            "is_midplane_anoxic": bool(is_anoxic),
            "viable_fraction": float(np.clip(viable_fraction, 0.0, 1.0)),
            "gsis_functional_fraction": float(np.clip(gsis_fraction, 0.0, 1.0)),
            "human_dose_area_cm2": float(device_footprint_cm2)
        }

    def solve_max_packing_density(
        self,
        chamber_half_thickness_um: float = 125.0,
        membrane_thickness_um: float = 25.0,
        fibrotic_capsule_um: float = 30.0,
        target_min_po2_mmhg: float = 15.0,
        host_tissue_po2_mmhg: float = 35.0
    ) -> float:
        """
        Finds the maximum allowable islet packing density phi such that midplane pO2 >= target_min_po2.
        """
        def objective(phi):
            res = self.compute_planar_oxygenation(
                chamber_half_thickness_um=chamber_half_thickness_um,
                membrane_thickness_um=membrane_thickness_um,
                fibrotic_capsule_um=fibrotic_capsule_um,
                islet_volume_fraction=phi,
                host_tissue_po2_mmhg=host_tissue_po2_mmhg
            )
            return res["midplane_po2_mmhg"] - target_min_po2_mmhg

        if objective(0.001) < 0:
            return 0.0
        if objective(0.50) >= 0:
            return 0.50

        try:
            sol = root_scalar(objective, bracket=[0.001, 0.50], method='brentq')
            return float(sol.root)
        except Exception:
            return 0.0


class NutrientDiffusionLagModel:
    """
    Kinetics of nutrient and hormone transport across encapsulation barriers.
    Solves for time delay (lag) in glucose sensing and insulin secretion.
    """

    @staticmethod
    def calculate_lag_times(
        capsule_diffusion_dist_um: float = 250.0,
        d_glucose_cm2_s: float = 2.5e-6,
        d_insulin_cm2_s: float = 0.8e-6
    ) -> Dict[str, float]:
        """
        Characteristic diffusion time: tau = L^2 / (2 * D)
        """
        l_cm = capsule_diffusion_dist_um * 1.0e-4
        tau_glucose_sec = (l_cm ** 2) / (2.0 * d_glucose_cm2_s)
        tau_insulin_sec = (l_cm ** 2) / (2.0 * d_insulin_cm2_s)
        total_response_delay_sec = tau_glucose_sec + tau_insulin_sec

        return {
            "diffusion_distance_um": capsule_diffusion_dist_um,
            "glucose_diffusion_lag_sec": float(tau_glucose_sec),
            "glucose_lag_min": float(tau_glucose_sec / 60.0),
            "insulin_diffusion_lag_sec": float(tau_insulin_sec),
            "insulin_lag_min": float(tau_insulin_sec / 60.0),
            "total_biphasic_delay_min": float(total_response_delay_sec / 60.0)
        }


class ForeignBodyResponseModel:
    """
    Biophysical model of Foreign Body Response (FBR) and Pericapsular Fibrotic Overgrowth (PFO).
    Captures:
    1. Size-dependent macrophage evasion (Vegas et al., Nat Biotechnol 2016: 1.5 mm beads avoid fibrosis).
    2. Chemical modification (triazole-modified alginate TMTD / Z1-Y15, zwitterionic hydrogels).
    3. Chronological scar thickness and its progressive strangulation of oxygen supply.
    """

    @staticmethod
    def fibrotic_thickness_trajectory(
        capsule_radius_um: float,
        is_triazole_modified: bool = False,
        days_post_implant: int = 180
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predicts fibrotic capsule thickness over time based on microcapsule geometry and chemistry.
        """
        t = np.linspace(0, days_post_implant, days_post_implant + 1)
        
        # Vegas et al. (2016): spheres with diameter >= 1.5 mm (R >= 750 um) dramatically suppress FBR
        if capsule_radius_um >= 750.0:
            size_attenuation = 0.08  # ~92% reduction
        elif capsule_radius_um >= 500.0:
            size_attenuation = 0.35
        else:
            size_attenuation = 1.00  # Standard heavy foreign body response
            
        # Chemical modification effect (TMTD / Z1-Y15 or zwitterionic)
        chem_attenuation = 0.05 if is_triazole_modified else 1.00
        
        # Max asymptotic thickness for conventional small unmodified bead: ~180-200 um
        max_thickness = 200.0 * size_attenuation * chem_attenuation
        
        k_fib = 0.08  # day^-1
        thickness = max_thickness / (1.0 + np.exp(-k_fib * (t - 14.0)))
        
        return t, thickness


# ==============================================================================
# SECTION 3: AUTOIMMUNE INTERCEPTION VIA TEPLIZUMAB (ANTI-CD3)
# ==============================================================================

@dataclass
class TeplizumabInterceptionParameters:
    """
    Pharmacodynamic and immunological parameters for anti-CD3 monoclonal antibody Teplizumab.
    Calibrated against TrialNet TN-10 (Herold et al., NEJM 2019, Sci Transl Med 2021).
    """
    # Natural history of Stage 2 T1D
    baseline_c_peptide_auc_nmol_l: float = 1.65   # Mean 2-hour MMTT C-peptide AUC at Stage 2
    clinical_stage3_threshold_auc: float = 0.60   # Residual C-peptide AUC triggering Stage 3 clinical diagnosis
    untreated_annual_c_peptide_loss: float = 0.495 # Annual decay rate yielding median ~24.4 months onset
    
    # Teplizumab efficacy parameters
    teplizumab_exhaustion_induction: float = 0.76  # Suppression factor during active protection
    intervention_duration_years: float = 3.0      # Duration of robust immunomodulatory protection
    waning_halflife_years: float = 1.5            # Half-life of protection waning after 3 years


class TeplizumabInterceptionModel:
    """
    Quantitative model simulating beta-cell preservation and Stage 3 T1D delay
    following a single 14-day course of Teplizumab (anti-CD3).
    """

    def __init__(self, params: Optional[TeplizumabInterceptionParameters] = None):
        self.params = params or TeplizumabInterceptionParameters()

    def simulate_interception(
        self,
        simulation_years: float = 8.0,
        teplizumab_treated: bool = True
    ) -> Dict[str, Any]:
        """
        Simulate C-peptide AUC trajectory and time to Stage 3 clinical diabetes onset.
        """
        dt = 0.02  # years
        times = np.arange(0.0, simulation_years + dt, dt)
        c_peptide = np.zeros_like(times)
        c_peptide[0] = self.params.baseline_c_peptide_auc_nmol_l
        
        stage3_time = None
        
        for i in range(1, len(times)):
            t = times[i]
            
            if not teplizumab_treated:
                # Untreated progressive autoimmune destruction
                decay_rate = self.params.untreated_annual_c_peptide_loss
            else:
                # Treated: profound deceleration during protective window
                if t <= self.params.intervention_duration_years:
                    decay_rate = self.params.untreated_annual_c_peptide_loss * (1.0 - self.params.teplizumab_exhaustion_induction)
                else:
                    # Gradual waning of immunologic tolerance back towards baseline
                    waning = np.exp(-(t - self.params.intervention_duration_years) / self.params.waning_halflife_years)
                    effective_suppression = self.params.teplizumab_exhaustion_induction * waning
                    decay_rate = self.params.untreated_annual_c_peptide_loss * (1.0 - effective_suppression)
                    
            c_peptide[i] = c_peptide[i-1] * np.exp(-decay_rate * dt)
            
            # Check Stage 3 diagnosis threshold
            if stage3_time is None and c_peptide[i] <= self.params.clinical_stage3_threshold_auc:
                stage3_time = t
                
        if stage3_time is None:
            stage3_time = simulation_years

        return {
            "treated": teplizumab_treated,
            "times_years": times,
            "c_peptide_auc": c_peptide,
            "stage3_onset_months": stage3_time * 12.0,
            "final_c_peptide_auc": float(c_peptide[-1])
        }

    def calculate_trialnet_median_delay(self) -> Dict[str, float]:
        """
        Calculates median delay to Stage 3 onset between treated and untreated cohorts.
        Matches TrialNet TN-10 benchmark (~24.4 months placebo vs ~50-60 months Teplizumab).
        """
        untreated = self.simulate_interception(teplizumab_treated=False)
        treated = self.simulate_interception(teplizumab_treated=True)
        
        delay_months = treated["stage3_onset_months"] - untreated["stage3_onset_months"]
        
        return {
            "placebo_onset_months": untreated["stage3_onset_months"],
            "teplizumab_onset_months": treated["stage3_onset_months"],
            "delay_months": delay_months,
            "delay_years": delay_months / 12.0
        }


# ==============================================================================
# SECTION 4: UNIFIED CURATIVE & REMISSION COMPARATIVE FRONTIER
# ==============================================================================

class CurativeDiabetesFrontier:
    """
    Multi-criteria comparative synthesis across all four tablet-free curative/remission paradigms:
    1. T2D Intensive Dietary Remission (Twin Cycle / DiRECT protocol)
    2. T1D Autoimmune Interception (Teplizumab / anti-CD3)
    3. T1D Stem Cell Allogeneic Islets + Immunosuppression (Vertex VX-880)
    4. T1D Stem Cell Macroencapsulation (Vertex VX-264 / Bioartificial Pancreas)
    """

    @staticmethod
    def compare_modalities() -> List[Dict[str, Any]]:
        return [
            {
                "modality": "T2D Intensive Dietary Remission (DiRECT Protocol)",
                "target_population": "T2D within 6 years of diagnosis",
                "biological_mechanism": "Caloric restriction -> rapid hepatic TAG clearance (7d) -> slower intrapancreatic TAG clearance (8-12w) -> beta-cell redifferentiation",
                "durability_years": "2-5+ years (contingent on weight maintenance)",
                "insulin_independence_rate_pct": 86.0,  # for >=15 kg loss cohort
                "severe_hypoglycemia_risk": "Zero (physiologic endogenous regulation restored)",
                "immunosuppression_required": False,
                "primary_biophysical_bottleneck": "Behavioral weight regain triggering hepatic/pancreatic resteatosis; permanent beta-cell apoptosis in long-standing disease (>10y)"
            },
            {
                "modality": "T1D Autoimmune Interception (Teplizumab / Tzield)",
                "target_population": "Stage 2 T1D (autoantibodies present + dysglycemia)",
                "biological_mechanism": "Anti-CD3 induction of CD8+ T cell exhaustion (KLRG1+ TIGIT+) and FoxP3+ Treg expansion, slowing residual beta-cell attrition",
                "durability_years": "Median 2.0-3.0 year delay of Stage 3 onset",
                "insulin_independence_rate_pct": 0.0,  # Delays onset of Stage 3 rather than reversing established Stage 3
                "severe_hypoglycemia_risk": "Zero during pre-Stage 3 honeymoon period",
                "immunosuppression_required": False,  # 14-day single immunomodulatory course
                "primary_biophysical_bottleneck": "Eventual resurgence of auto-reactive memory clones; does not regenerate destroyed beta-cell mass"
            },
            {
                "modality": "T1D Stem Cell Allogeneic Islets (Vertex VX-880)",
                "target_population": "Stage 3 T1D with severe hypoglycemia unawareness",
                "biological_mechanism": "Portal vein infusion of fully differentiated hESC/iPSC-derived islets; rapid engraftment with high sinusoidal pO2 (50 mmHg)",
                "durability_years": "2-5+ years (ADA 2024 Phase 1/2 clinical data)",
                "insulin_independence_rate_pct": 91.0,  # evaluable patients reaching HbA1c < 7% & insulin independence
                "severe_hypoglycemia_risk": "100% elimination of severe hypoglycemic events",
                "immunosuppression_required": True,   # Life-long systemic immunosuppression (tacrolimus, MMF)
                "primary_biophysical_bottleneck": "Off-target immunosuppression toxicity (nephrotoxicity, infection, malignancy risk), restricting eligibility to severe recurrent SHEs"
            },
            {
                "modality": "T1D Stem Cell Macroencapsulation (Vertex VX-264 / Bioartificial Pancreas)",
                "target_population": "Broad Stage 3 T1D without immunosuppression",
                "biological_mechanism": "SC-islets sealed in immunoprotective retrievable chamber; molecular cut-off blocks host antibodies and T cells",
                "durability_years": "Preclinical / Early clinical (Months to 1-2 years)",
                "insulin_independence_rate_pct": 25.0,  # Constrained by hypoxia in subcutaneous space
                "severe_hypoglycemia_risk": "Substantial reduction if islet graft survives",
                "immunosuppression_required": False,
                "primary_biophysical_bottleneck": "Reaction-diffusion oxygen strangulation (subcutaneous pO2 35 mmHg - drops across scar, membrane, and islet bed drive core anoxia)"
            }
        ]


# ==============================================================================
# SECTION 5: DEMO / CLI EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TABLET-FREE DIABETES REMISSION & STEM-CELL ISLET BIOPHYSICS ENGINE")
    print("=" * 80)
    
    # 1. Twin Cycle Simulation
    print("\n--- 1. Twin Cycle Model (DiRECT Protocol: 850 kcal/day for 20 weeks) ---")
    tc_engine = TwinCycleModel()
    traj = tc_engine.simulate_dietary_remission(duration_days=140, daily_deficit_kcal=1200.0)
    print(f"Initial Weight: {traj.weight_kg[0]:.1f} kg -> Final Weight: {traj.weight_kg[-1]:.1f} kg (Loss: {traj.weight_kg[0] - traj.weight_kg[-1]:.1f} kg)")
    print(f"Day 0  - IHTG: {traj.ihtg_pct[0]:.1f}%, IPTG: {traj.iptg_pct[0]:.1f}%, FPG: {traj.fpg_mmol[0]:.1f} mmol/L, AIRg: {traj.airg_nmol[0]:.3f} nmol/L")
    print(f"Day 7  - IHTG: {traj.ihtg_pct[7]:.1f}%, IPTG: {traj.iptg_pct[7]:.1f}%, FPG: {traj.fpg_mmol[7]:.1f} mmol/L, AIRg: {traj.airg_nmol[7]:.3f} nmol/L")
    print(f"Day 28 - IHTG: {traj.ihtg_pct[28]:.1f}%, IPTG: {traj.iptg_pct[28]:.1f}%, FPG: {traj.fpg_mmol[28]:.1f} mmol/L, AIRg: {traj.airg_nmol[28]:.3f} nmol/L")
    print(f"Day 140- IHTG: {traj.ihtg_pct[-1]:.1f}%, IPTG: {traj.iptg_pct[-1]:.1f}%, FPG: {traj.fpg_mmol[-1]:.1f} mmol/L, AIRg: {traj.airg_nmol[-1]:.3f} nmol/L")
    print(f"Remission Achieved: {traj.remission_achieved} (HbA1c: {traj.hba1c_est_pct[-1]:.1f}%)")

    # DiRECT weight-loss stratified remission probabilities
    print("\nDiRECT Stratified Remission Probabilities (Taylor et al. 2018):")
    for loss in [3.0, 7.5, 12.5, 17.5]:
        p = PersonalFatThreshold.direct_remission_probability(weight_loss_kg=loss, diabetes_duration_years=3.0)
        print(f"  Weight loss {loss:4.1f} kg -> Remission Probability: {p*100.0:4.1f}%")

    # Relapse demonstration upon weight regain
    print("\nWeight Regain Relapse Simulation (Reverse Route):")
    relapse = tc_engine.simulate_weight_regain_relapse(traj, regain_duration_days=365, daily_surplus_kcal=350.0)
    print(f"  After 365 days surplus: Weight: {relapse['weight_kg'][-1]:.1f} kg | IHTG: {relapse['ihtg_pct'][-1]:.1f}% | IPTG: {relapse['iptg_pct'][-1]:.1f}% | FPG: {relapse['fpg_mmol'][-1]:.1f} mmol/L | AIRg: {relapse['airg_nmol'][-1]:.3f} nmol/L | Relapsed: {relapse['relapsed']}")

    # 2. Islet Microencapsulation Transport
    print("\n--- 2. Islet Microencapsulation Oxygen Transport (Single 150 um Islet) ---")
    micro_engine = IsletMicroencapsulationModel()
    for fib in [0.0, 15.0, 30.0, 60.0]:
        res = micro_engine.solve_oxygen_profile_analytical(capsule_radius_um=250.0, fibrotic_thickness_um=fib, host_tissue_po2_mmhg=35.0)
        print(f"  Scar {fib:4.1f} um: Core pO2 = {res['core_po2_mmhg']:5.1f} mmHg (Zero-order: {res['theoretical_zero_order_core_po2_mmhg']:5.1f}) | Surf = {res['islet_surface_po2_mmhg']:5.1f} mmHg | Anoxic R = {res['anoxic_core_radius_um']:4.1f} um | Viable = {res['viable_fraction']*100.0:5.1f}% | GSIS Competent = {res['gsis_competent_fraction']*100.0:5.1f}%")

    # 3. Macroencapsulation Planar Chamber
    print("\n--- 3. Planar Macroencapsulation Chamber (VX-264 Prototype) ---")
    macro_engine = MacroencapsulationDeviceModel()
    for phi in [0.02, 0.05, 0.08, 0.12]:
        mres = macro_engine.compute_planar_oxygenation(
            chamber_half_thickness_um=125.0,
            membrane_thickness_um=25.0,
            fibrotic_capsule_um=30.0,
            islet_volume_fraction=phi,
            host_tissue_po2_mmhg=35.0
        )
        print(f"  Density phi={phi:.2f}: Midplane pO2 = {mres['midplane_po2_mmhg']:5.1f} mmHg | Edge = {mres['chamber_edge_po2_mmhg']:5.1f} mmHg | Viable = {mres['viable_fraction']*100.0:5.1f}% | GSIS = {mres['gsis_functional_fraction']*100.0:5.1f}% | 500k Area = {mres['human_dose_area_cm2']:6.1f} cm^2 | Anoxic = {mres['is_midplane_anoxic']}")

    max_phi = macro_engine.solve_max_packing_density(chamber_half_thickness_um=125.0, fibrotic_capsule_um=30.0, target_min_po2_mmhg=15.0)
    print(f"  Maximum Allowable Packing Density (Midplane pO2 >= 15 mmHg): phi = {max_phi*100.0:.2f}%")

    # 4. Teplizumab Interception
    print("\n--- 4. Teplizumab Autoimmune Interception (TrialNet TN-10 Benchmark) ---")
    tepli_engine = TeplizumabInterceptionModel()
    delays = tepli_engine.calculate_trialnet_median_delay()
    print(f"  Placebo Median Stage 3 Onset:    {delays['placebo_onset_months']:.1f} months")
    print(f"  Teplizumab Median Stage 3 Onset: {delays['teplizumab_onset_months']:.1f} months")
    print(f"  Delay in Clinical Diabetes:      {delays['delay_months']:.1f} months ({delays['delay_years']:.2f} years)")
    print("=" * 80)
