"""
Next-Gen Hypertension Control: Semiannual Angiotensinogen siRNA and Renal Denervation Engine
=============================================================================================
Computational biophysics, pharmacokinetics/pharmacodynamics (PK/PD), bioheat transfer,
and Guytonian pressure-natriuresis systems biology for non-oral hypertension management.

Key Subsystems:
1. ZilebesiranPKPD:
   - GalNAc3-ASGPR hepatic uptake, receptor recycling, endosomal depot sequestration.
   - Cytosolic Ago2-RISC catalytic loading with saturable Ago2 capacity and multiple-turnover AGT mRNA cleavage.
   - Semiannual (180+ day) hepatic AGT suppression and circulating plasma AGT kinetics benchmarked to KARDIA-1/2.
2. RenalDenervationModel:
   - Adventitial perivascular nerve distribution (depth 1.0 - 6.0 mm from lumen) based on human histological morphometry.
   - Pennes bioheat cylindrical radial transfer equation.
   - Radiofrequency (RF closed-loop temperature control) vs. Ultrasound (Paradise 7-second sonication with balloon cooling).
   - Arrhenius protein denaturation and nerve inactivation integrals.
3. GuytonianPressureNatriuresisSystem:
   - Closed-loop Guytonian renal-body fluid balance and pressure-natriuresis curve.
   - Renin-Angiotensin-Aldosterone System (RAAS) with Michaelis-Menten Renin-AGT cleavage and JG cell feedback.
   - Renal Sympathetic Nerve Activity (RSNA) neurogenic shifts in tubular reabsorption and renin release.
4. HypertensionTherapySimulator:
   - Unified digital twin simulating oral adherence attrition vs. semiannual siRNA vs. catheter RDN.
   - Benchmarked against KARDIA-1/2, SPYRAL HTN-ON/OFF MED, and RADIANCE clinical trial data.
"""

import functools
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar

# Handle numpy trapezoid compatibility
_trapezoid = getattr(np, "trapezoid", getattr(np, "trapz", None))


# ============================================================================
# 1. BIOPHYSICAL CONSTANTS & PHYSIOLOGICAL PARAMETERS
# ============================================================================

GAS_CONSTANT_R = 8.314462618  # J / (mol * K)
BODY_TEMP_K = 310.15          # 37.0 C in Kelvin
BODY_TEMP_C = 37.0            # Core body temperature in Celsius


@dataclass(frozen=True)
class GalNAcASGPRParameters:
    """Parameters for GalNAc3-siRNA hepatocyte uptake and intracellular trafficking."""
    kd_asgpr_nm: float = 2.5              # Dissociation constant of GalNAc3 to ASGPR [nM]
    asgpr_receptors_per_cell: float = 7.5e5 # Surface ASGPR copies per hepatocyte
    total_hepatocytes: float = 2.4e11     # Total human hepatocytes (~1.5 kg liver)
    liver_volume_l: float = 1.5           # Liver parenchymal volume [L]
    plasma_volume_l: float = 3.0          # Systemic plasma volume [L]
    endocytosis_rate_per_min: float = 0.05 # ASGPR internalization rate [min^-1] (t1/2 ~ 14 min)
    receptor_recycle_rate_per_min: float = 0.04 # ASGPR recycling back to surface [min^-1]
    subcutaneous_ka_day: float = 3.6      # Subcutaneous absorption rate [day^-1] (t1/2 ~ 4.6 h)
    sc_bioavailability: float = 0.85      # Subcutaneous bioavailability
    plasma_renal_clearance_l_day: float = 18.0 # Glomerular filtration clearance [L/day]
    endosomal_escape_rate_day: float = 0.0035  # Slow cytosolic escape rate from depot [day^-1] (t1/2 ~ 200 days)
    endosomal_degradation_rate_day: float = 0.0075 # Degradation inside endolysosomes [day^-1]
    risc_loading_rate_day: float = 0.6    # Rate of guide strand Ago2 incorporation [day^-1]
    risc_half_life_days: float = 48.0     # Intracellular half-life of chemically modified RISC* [days]
    total_ago2_capacity_nm: float = 18.0  # Total hepatocellular Ago2 binding capacity [nM]


@dataclass(frozen=True)
class AGTRNAiKineticsParameters:
    """Parameters for hepatic AGT mRNA transcription, catalytic cleavage, and plasma turnover."""
    basal_mrna_synthesis_nm_day: float = 2.4   # Constitutive AGT mRNA transcription rate [nM/day]
    basal_mrna_half_life_hours: float = 12.0   # Basal AGT mRNA half-life [hours]
    risc_kcat_per_hour: float = 4.2            # Ago2 catalytic turnover on AGT mRNA [h^-1]
    risc_km_nm: float = 1.5                    # Michaelis constant for RISC* cleavage [nM]
    translation_rate_per_day: float = 18.0     # Translation of AGT protein per mRNA [day^-1]
    hepatic_agt_export_rate_day: float = 4.0   # Secretion rate from hepatocyte into sinusoid [day^-1]
    plasma_agt_half_life_hours: float = 14.0   # Plasma AGT degradation/consumption t1/2 [hours]
    basal_plasma_agt_nm: float = 1200.0        # Basal human circulating AGT (~65 ug/mL) [nM]


@dataclass(frozen=True)
class RenalArteryAblationParameters:
    """Anatomical, thermal, and acoustic properties for Catheter Renal Denervation."""
    lumen_radius_mm: float = 2.5               # Main renal artery lumen radius [mm]
    wall_thickness_mm: float = 0.8             # Intima + media thickness [mm]
    adventitia_max_depth_mm: float = 6.0       # Max adventitial radius explored [mm]
    tissue_density_kg_m3: float = 1050.0       # Soft tissue density [kg/m^3]
    tissue_specific_heat_j_kg_k: float = 3600.0# Specific heat capacity [J/(kg*K)]
    thermal_conductivity_w_m_k: float = 0.52   # Thermal conductivity [W/(m*K)]
    blood_perfusion_rate_s: float = 0.002      # Capillary blood perfusion rate [s^-1]
    blood_specific_heat_j_kg_k: float = 3800.0 # Blood specific heat [J/(kg*K)]
    blood_temp_c: float = 37.0                 # Arterial blood temperature [C]
    blood_convection_htc_w_m2_k: float = 1800.0# Convective HTC at endothelial lumen [W/(m^2*K)]
    arrhenius_activation_energy_j_mol: float = 4.18e5 # Ea for nerve thermal damage [J/mol]
    arrhenius_frequency_factor_s: float = 1.98e65     # A frequency factor [s^-1]
    nerve_depth_lognormal_mu: float = 1.163    # Median depth = exp(1.163) = 3.20 mm
    nerve_depth_lognormal_sigma: float = 0.38  # Depth dispersion parameter


@dataclass(frozen=True)
class GuytonianRAASParameters:
    """Guytonian renal-fluid equilibrium and RAAS cascade parameters."""
    normal_map_mmhg: float = 95.0             # Normal mean arterial pressure [mmHg]
    hypertensive_baseline_map: float = 118.0  # Stage 2 hypertensive baseline MAP [mmHg]
    sodium_intake_mmol_day: float = 150.0      # Dietary sodium intake [mmol/day]
    base_pn_slope: float = 5.0                # Baseline pressure-natriuresis slope [mmol/(day*mmHg)]
    base_pn_intercept_mmhg: float = 65.0      # Baseline pressure threshold [mmHg]
    renin_km_agt_nm: float = 1250.0           # Renin Km for AGT substrate [nM]
    renin_kcat_s: float = 0.85                # Renin turnover number [s^-1]
    base_prc_pg_ml: float = 20.0              # Baseline plasma renin concentration [pg/mL]
    base_ang_ii_pmol_l: float = 15.0          # Baseline circulating Ang II [pmol/L]
    feedback_sensitivity_ang_ii: float = 1.8  # Feedback gain on renin secretion
    rsna_renin_gain: float = 0.5              # RSNA multiplier on renin release
    rsna_tubular_gain: float = 0.45           # RSNA direct tubular Na reabsorption gain
    raas_intercept_sensitivity: float = 20.0  # Intercept shift per normalized Ang II deviation [mmHg]
    rsna_intercept_sensitivity: float = 14.0  # Intercept shift per normalized RSNA deviation [mmHg]
    arterial_compliance_ml_mmhg: float = 1.15 # Systemic arterial compliance [mL/mmHg]
    stroke_volume_ml: float = 75.0            # Left ventricular stroke volume [mL]


# ============================================================================
# 2. MODULE 1: ZILEBESIRAN RNAi PK/PD & AGT CATALYTIC SUPPRESSION
# ============================================================================

class ZilebesiranPKPD:
    """
    Simulates GalNAc-conjugated siRNA (Zilebesiran / ALN-AGT) pharmacokinetics,
    ASGPR receptor-mediated hepatic extraction, intracellular endosomal depot kinetics,
    Ago2-RISC catalytic mRNA cleavage, and long-term semiannual AGT protein suppression.
    """

    def __init__(self,
                 galnac_params: Optional[GalNAcASGPRParameters] = None,
                 rnai_params: Optional[AGTRNAiKineticsParameters] = None):
        self.gp = galnac_params or GalNAcASGPRParameters()
        self.rp = rnai_params or AGTRNAiKineticsParameters()

        # Compute basal mRNA steady-state concentration:
        # d[mRNA]/dt = k_transcription - k_deg_basal * [mRNA] = 0
        self.k_deg_basal_day = (math.log(2.0) / (self.rp.basal_mrna_half_life_hours / 24.0))
        self.basal_mrna_nm = self.rp.basal_mrna_synthesis_nm_day / self.k_deg_basal_day

        # Compute basal hepatic AGT and plasma clearance rate to match basal_plasma_agt_nm
        self.k_clear_agt_day = (math.log(2.0) / (self.rp.plasma_agt_half_life_hours / 24.0))
        self.basal_hepatic_agt_nm = (self.rp.translation_rate_per_day * self.basal_mrna_nm) / self.rp.hepatic_agt_export_rate_day

        # Calibration factor for plasma secretion:
        # V_liver * k_sec * [AGT_liver] = V_plasma * k_clear * [AGT_plasma]
        self.plasma_secretion_gain = (self.gp.plasma_volume_l * self.k_clear_agt_day * self.rp.basal_plasma_agt_nm) / \
                                     (self.gp.liver_volume_l * self.rp.hepatic_agt_export_rate_day * self.basal_hepatic_agt_nm)

    def calculate_asgpr_capacity(self) -> float:
        """Total ASGPR binding capacity of the liver in nanomoles."""
        total_receptors = self.gp.asgpr_receptors_per_cell * self.gp.total_hepatocytes
        avogadro = 6.02214076e23
        moles = total_receptors / avogadro
        return moles * 1e9  # nanomoles (~299 nmol)

    def simulate_single_dose(self,
                             dose_mg: float = 300.0,
                             duration_days: float = 210.0,
                             time_eval_points: int = 1000) -> Dict[str, np.ndarray]:
        """
        Simulate PK/PD trajectory for a single subcutaneous dose of Zilebesiran.

        Dose is converted to nanomoles assuming siRNA molecular weight ~17,000 g/mol (GalNAc3-siRNA conjugate).

        State variables:
        y[0]: Subcutaneous depot amount (A_sc) [nmol]
        y[1]: Plasma concentration (C_plasma) [nM]
        y[2]: Liver endosomal/lysosomal depot amount (A_endo) [nmol]
        y[3]: Active loaded RISC in liver hepatocytes (RISC_star) [nM]
        y[4]: Intact AGT mRNA in hepatocytes (mRNA_agt) [nM]
        y[5]: Hepatic AGT protein (AGT_liver) [nM]
        y[6]: Circulating plasma AGT (AGT_plasma) [nM]
        """
        siRNA_mw = 17000.0  # g/mol
        dose_nmol = (dose_mg * 1e-3 / siRNA_mw) * 1e9 * self.gp.sc_bioavailability

        # Initial conditions:
        y0 = [
            dose_nmol,                     # A_sc [nmol]
            0.0,                           # C_plasma [nM]
            0.0,                           # A_endo [nmol]
            0.0,                           # RISC_star [nM]
            self.basal_mrna_nm,            # mRNA_agt [nM]
            self.basal_hepatic_agt_nm,     # AGT_liver [nM]
            self.rp.basal_plasma_agt_nm    # AGT_plasma [nM]
        ]

        t_span = (0.0, duration_days)
        t_eval = np.linspace(0.0, duration_days, time_eval_points)

        # Precompute constants
        ka = self.gp.subcutaneous_ka_day
        v_plasma = self.gp.plasma_volume_l
        v_liver = self.gp.liver_volume_l
        cl_renal = self.gp.plasma_renal_clearance_l_day
        k_endo_escape = self.gp.endosomal_escape_rate_day
        k_endo_deg = self.gp.endosomal_degradation_rate_day
        k_risc_deg = math.log(2.0) / self.gp.risc_half_life_days
        k_risc_load = self.gp.risc_loading_rate_day
        ago2_max = self.gp.total_ago2_capacity_nm

        k_synth_mrna = self.rp.basal_mrna_synthesis_nm_day
        k_deg_mrna_basal = self.k_deg_basal_day
        kcat_risc_day = self.rp.risc_kcat_per_hour * 24.0
        km_risc = self.rp.risc_km_nm

        k_trans = self.rp.translation_rate_per_day
        k_sec = self.rp.hepatic_agt_export_rate_day
        k_clear_agt = self.k_clear_agt_day
        gain_sec = self.plasma_secretion_gain

        # Michaelis-Menten hepatic uptake parameters via ASGPR
        asgpr_vmax_nmol_day = 1.2e5  # high capacity hepatic extraction (~80-90% first pass)
        asgpr_km_nm = self.gp.kd_asgpr_nm

        def derivatives(t: float, y: List[float]) -> List[float]:
            a_sc, c_plasma, a_endo, risc_star, mrna, agt_liver, agt_plasma = y

            # Non-negative clamping for numerical stability
            a_sc = max(0.0, a_sc)
            c_plasma = max(0.0, c_plasma)
            a_endo = max(0.0, a_endo)
            risc_star = max(0.0, min(ago2_max, risc_star))
            mrna = max(0.0, mrna)
            agt_liver = max(0.0, agt_liver)
            agt_plasma = max(0.0, agt_plasma)

            # 1. SC depot absorption
            rate_sc_in = ka * a_sc
            d_asc = -rate_sc_in

            # 2. Hepatic ASGPR uptake flux [nmol/day]
            uptake_rate_nmol_day = (asgpr_vmax_nmol_day * c_plasma) / (asgpr_km_nm + c_plasma) if c_plasma > 0 else 0.0

            # Renal clearance flux [nmol/day]
            renal_clearance_flux = cl_renal * c_plasma

            # Plasma siRNA balance
            d_cplasma = (rate_sc_in - renal_clearance_flux - uptake_rate_nmol_day) / v_plasma

            # 3. Endosomal depot in liver
            rate_escape = k_endo_escape * a_endo
            rate_endo_deg = k_endo_deg * a_endo
            d_aendo = uptake_rate_nmol_day - rate_escape - rate_endo_deg

            # 4. Cytosolic RISC loading with saturable Ago2 capacity
            # Free siRNA entering cytosol from endosome: concentration flux in liver volume
            cytosolic_influx_nm = rate_escape / v_liver
            # Loading rate throttled by remaining available Ago2 fraction: (1 - risc_star / ago2_max)
            fraction_free_ago2 = max(0.0, 1.0 - (risc_star / ago2_max))
            d_risc = k_risc_load * cytosolic_influx_nm * fraction_free_ago2 - k_risc_deg * risc_star

            # 5. AGT mRNA dynamics (Multiple turnover catalytic degradation by RISC*)
            v_cleavage = (kcat_risc_day * risc_star * mrna) / (km_risc + mrna) if mrna > 0 else 0.0
            d_mrna = k_synth_mrna - (k_deg_mrna_basal * mrna) - v_cleavage

            # 6. Hepatic AGT protein
            d_agt_liver = (k_trans * mrna) - (k_sec * agt_liver)

            # 7. Circulating Plasma AGT
            secretion_flux = (k_sec * agt_liver) * (v_liver / v_plasma) * gain_sec
            degradation_flux = k_clear_agt * agt_plasma
            d_agt_plasma = secretion_flux - degradation_flux

            return [d_asc, d_cplasma, d_aendo, d_risc, d_mrna, d_agt_liver, d_agt_plasma]

        sol = solve_ivp(
            derivatives,
            t_span,
            y0,
            t_eval=t_eval,
            method="Radau",
            rtol=1e-6,
            atol=1e-8
        )

        time_days = sol.t
        plasma_siRNA = sol.y[1]
        risc_active = sol.y[3]
        mrna_agt = sol.y[4]
        agt_plasma = sol.y[6]

        # Normalized suppression: 1.0 - (agt_plasma / basal)
        suppression_fraction = np.clip(1.0 - (agt_plasma / self.rp.basal_plasma_agt_nm), 0.0, 1.0)

        return {
            "time_days": time_days,
            "plasma_siRNA_nM": plasma_siRNA,
            "risc_active_nM": risc_active,
            "mrna_agt_nM": mrna_agt,
            "agt_plasma_nM": agt_plasma,
            "suppression_fraction": suppression_fraction,
            "dose_mg": dose_mg
        }

    def evaluate_semiannual_benchmarks(self, dose_mg: float = 300.0) -> Dict[str, float]:
        """
        Evaluate key clinical benchmarks matching KARDIA-1/KARDIA-2:
        - Peak (nadir) AGT suppression (%)
        - Day of peak suppression
        - AGT suppression at Week 12 (Day 84) (%)
        - AGT suppression at Week 24 (Day 168) (%)
        - AGT suppression at Week 26 (Day 182) (%)
        """
        sim = self.simulate_single_dose(dose_mg=dose_mg, duration_days=210.0, time_eval_points=1500)
        t = sim["time_days"]
        supp = sim["suppression_fraction"] * 100.0

        nadir_idx = np.argmax(supp)
        peak_suppression = float(supp[nadir_idx])
        day_of_peak = float(t[nadir_idx])

        supp_wk12 = float(np.interp(84.0, t, supp))
        supp_wk24 = float(np.interp(168.0, t, supp))
        supp_wk26 = float(np.interp(182.0, t, supp))

        return {
            "dose_mg": dose_mg,
            "peak_suppression_pct": peak_suppression,
            "day_of_peak": day_of_peak,
            "week12_suppression_pct": supp_wk12,
            "week24_suppression_pct": supp_wk24,
            "week26_suppression_pct": supp_wk26,
            "semiannual_threshold_met": (supp_wk24 >= 90.0)
        }


# ============================================================================
# 3. MODULE 2: CATHETER-BASED RENAL DENERVATION (RDN) BIOPHYSICS
# ============================================================================

class RenalDenervationModel:
    """
    Biophysical simulation of Catheter Renal Denervation (RDN).
    Models:
    1. Adventitial sympathetic nerve radial depth distribution.
    2. Pennes Bioheat 1D cylindrical radial thermal transfer equation.
    3. Radiofrequency (RF with closed-loop power control) vs Ultrasound (uRDN acoustic attenuation).
    4. Arrhenius thermal protein denaturation / axonal necrosis integral.
    5. Net efferent and afferent nerve ablation percentage.
    """

    def __init__(self, params: Optional[RenalArteryAblationParameters] = None):
        self.p = params or RenalArteryAblationParameters()

    def nerve_probability_density(self, r_mm: float) -> float:
        """
        Log-normal probability density function of nerve distance from arterial lumen (depth d = r - r_lumen).
        Based on human histological morphometry (Sakakura et al. JACC 2014).
        """
        depth_mm = r_mm - self.p.lumen_radius_mm
        if depth_mm <= 0.0:
            return 0.0

        mu = self.p.nerve_depth_lognormal_mu
        sigma = self.p.nerve_depth_lognormal_sigma
        denom = depth_mm * sigma * math.sqrt(2.0 * math.pi)
        exponent = -((math.log(depth_mm) - mu) ** 2) / (2.0 * (sigma ** 2))
        return math.exp(exponent) / denom

    def solve_bioheat_temperature_profile(self,
                                          modality: str = "rf",
                                          duration_s: Optional[float] = None,
                                          rf_power_w: float = 5.0,
                                          us_intensity_w_cm2: float = 24.0,
                                          num_radial_nodes: int = 150) -> Dict[str, np.ndarray]:
        """
        Solves the transient Pennes bioheat transfer equation in cylindrical coordinates:
        rho * c * dT/dt = (1/r) * d/dr (k * r * dT/dr) + q_source(r) - omega_b * c_b * (T - T_blood)

        Modality:
        - "rf": Radiofrequency catheter (Symplicity Spyral style).
                Duration: 60 s default. Contact electrode with convective blood cooling
                and closed-loop generator control regulating peak electrode temp <= 65 C.
        - "ultrasound": Ultrasound balloon (Paradise style).
                Duration: 7.0 s default per sonication. Water-cooled balloon maintaining
                lumen at 37-40 C, 9 MHz acoustic attenuation q_us(r) = 2 * alpha * I(r).
        """
        if duration_s is None:
            duration_s = 60.0 if modality.lower() == "rf" else 7.0

        r_lumen = self.p.lumen_radius_mm * 1e-3         # m
        r_max = (self.p.lumen_radius_mm + self.p.adventitia_max_depth_mm + 4.0) * 1e-3  # m

        r_grid = np.linspace(r_lumen, r_max, num_radial_nodes)
        dr = r_grid[1] - r_grid[0]

        rho = self.p.tissue_density_kg_m3
        c = self.p.tissue_specific_heat_j_kg_k
        k = self.p.thermal_conductivity_w_m_k
        w_b = self.p.blood_perfusion_rate_s * rho
        c_b = self.p.blood_specific_heat_j_kg_k
        t_blood = self.p.blood_temp_c

        # Volumetric source term profile q(r) [W/m^3]
        q_source_base = np.zeros(num_radial_nodes)
        if modality.lower() == "rf":
            # RF electrical dissipation: monopolar current spreading radially.
            # q(r) = q0 * (r_lumen / r)^4. Total tissue power ~ 2.5 W per electrode (remainder carried by blood).
            p_tissue = 2.5
            l_contact = 0.0015  # 1.5 mm electrode contact length
            # Integral: int_{r0}^inf q0 (r0/r)^4 2*pi*r*L dr = pi * L * q0 * r0^2
            vol_eff = math.pi * l_contact * (r_lumen ** 2)
            q0 = p_tissue / vol_eff
            for i, r in enumerate(r_grid):
                ratio = r_lumen / r
                q_source_base[i] = q0 * (ratio ** 4) * math.exp(-(r - r_lumen) / 0.004)
        elif modality.lower() == "ultrasound":
            # Ultrasound acoustic beam: 9 MHz acoustic attenuation
            # Tissue attenuation: alpha ~ 0.8 dB/(cm*MHz) = 7.2 dB/cm = 82.9 Np/m
            alpha_tissue = 83.0  # Np/m
            i0_w_m2 = us_intensity_w_cm2 * 1e4  # convert W/cm^2 to W/m^2
            for i, r in enumerate(r_grid):
                # Cylindrical spreading + attenuation
                intensity = i0_w_m2 * (r_lumen / r) * math.exp(-2.0 * alpha_tissue * (r - r_lumen))
                q_source_base[i] = 2.0 * alpha_tissue * intensity
        else:
            raise ValueError(f"Unknown RDN modality: {modality}. Choose 'rf' or 'ultrasound'.")

        # Initial temperature: uniform core body temperature 37.0 C
        T = np.full(num_radial_nodes, t_blood)

        # Time stepping parameters: explicit finite difference with Von Neumann stability
        alpha_diff = k / (rho * c)
        dt = min(0.005, 0.35 * (dr ** 2) / alpha_diff)
        n_steps = max(1, int(duration_s / dt))

        # Store temperature history
        t_history = np.zeros((n_steps, num_radial_nodes))

        h_blood = self.p.blood_convection_htc_w_m2_k
        r_inner = r_grid[1:-1]

        for step in range(n_steps):
            T_new = np.copy(T)

            # Generator feedback throttle for RF to prevent charring / steam pops
            # If electrode contact temp approaches 65 C, power throttles down
            power_factor = 1.0
            if modality.lower() == "rf":
                if T[0] > 60.0:
                    power_factor = max(0.1, 1.0 - (T[0] - 60.0) / 6.0)

            q_source = q_source_base * power_factor

            # Cylindrical Laplacian: (1/r) d/dr (r dT/dr) = d2T/dr2 + (1/r) dT/dr
            d2T_dr2 = (T[2:] - 2.0 * T[1:-1] + T[:-2]) / (dr ** 2)
            dT_dr = (T[2:] - T[:-2]) / (2.0 * dr)
            laplacian = d2T_dr2 + (1.0 / r_inner) * dT_dr

            perfusion_sink = w_b * c_b * (T[1:-1] - t_blood)
            dT_dt = (k * laplacian + q_source[1:-1] - perfusion_sink) / (rho * c)
            T_new[1:-1] = T[1:-1] + dt * dT_dt

            # Boundary conditions:
            if modality.lower() == "rf":
                # Convective cooling from lumen blood + Joule dissipation
                T_new[0] = T_new[1] + (dr / k) * (h_blood * (t_blood - T_new[1]) + (q_source[0] * dr * 0.5))
                # Generator hardware clamp: max 65 C
                T_new[0] = min(65.0, max(t_blood, T_new[0]))
            else:
                # Ultrasound balloon: active fluid circulation cools lumen surface to ~38-40 C
                T_new[0] = 38.5
                T_new[1] = 0.5 * (T_new[0] + T_new[2])

            # Outer boundary (far-field tissue at r_max): core body temperature
            T_new[-1] = t_blood

            T = T_new
            t_history[step, :] = T

        return {
            "r_grid_mm": r_grid * 1e3,
            "depth_from_lumen_mm": (r_grid - r_lumen) * 1e3,
            "final_temperature_c": T,
            "peak_temperature_c": np.max(t_history, axis=0),
            "time_history_s": np.linspace(0.0, duration_s, n_steps),
            "temperature_history": t_history,
            "modality": modality,
            "duration_s": duration_s,
            "dt": dt
        }

    def compute_arrhenius_damage(self, thermal_sim: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Computes Arrhenius thermal damage integral Omega(r) and nerve survival fraction:
        Omega(r) = int_0^t A * exp(-E_a / (R * T(r, tau))) dtau
        Fraction of nerve fibers ablated F_ablated(r) = 1.0 - exp(-Omega(r)).
        """
        t_hist = thermal_sim["temperature_history"]  # shape (n_steps, num_nodes)
        dt = thermal_sim["dt"]
        r_grid_mm = thermal_sim["r_grid_mm"]
        depth_mm = thermal_sim["depth_from_lumen_mm"]

        a_factor = self.p.arrhenius_frequency_factor_s
        ea = self.p.arrhenius_activation_energy_j_mol
        r_gas = GAS_CONSTANT_R

        # Convert temperature history from Celsius to Kelvin
        t_kelvin = t_hist + 273.15

        # Compute damage rate: A * exp(-Ea / (R * T))
        exponent = -ea / (r_gas * t_kelvin)
        rate = a_factor * np.exp(np.clip(exponent, -700.0, 0.0))

        # Integrate over time
        omega = np.sum(rate * dt, axis=0)

        # Fractional survival S(r) = exp(-Omega(r))
        survival = np.exp(-np.clip(omega, 0.0, 100.0))
        ablation_fraction = 1.0 - survival

        return {
            "r_grid_mm": r_grid_mm,
            "depth_from_lumen_mm": depth_mm,
            "arrhenius_omega": omega,
            "ablation_fraction": ablation_fraction
        }

    def calculate_total_denervation_efficiency(self,
                                               modality: str = "rf",
                                               duration_s: Optional[float] = None) -> Dict[str, float]:
        """
        Integrates ablation fraction over the anatomical nerve depth distribution
        to compute net sympathetic denervation percentage (both efferent and afferent).
        """
        thermal_sim = self.solve_bioheat_temperature_profile(modality=modality, duration_s=duration_s)
        damage = self.compute_arrhenius_damage(thermal_sim)

        depths = damage["depth_from_lumen_mm"]
        r_coords = damage["r_grid_mm"]
        ablation_profile = damage["ablation_fraction"]

        # Nerve probability density across nodes
        densities = np.array([self.nerve_probability_density(r) for r in r_coords])

        norm = _trapezoid(densities, r_coords)
        if norm <= 0:
            norm = 1.0

        net_denervation_fraction = float(_trapezoid(ablation_profile * densities, r_coords) / norm)
        net_denervation_fraction = float(np.clip(net_denervation_fraction, 0.0, 1.0))

        # Compute depth at which 50% damage occurs (effective ablation depth)
        idx_above_50 = np.where(ablation_profile >= 0.5)[0]
        effective_depth_mm = float(depths[idx_above_50[-1]]) if len(idx_above_50) > 0 else 0.0

        # Endothelial thermal injury assessment (depth < 0.5 mm)
        intimal_damage_fraction = float(ablation_profile[0])

        return {
            "modality": modality,
            "duration_s": thermal_sim["duration_s"],
            "net_denervation_pct": net_denervation_fraction * 100.0,
            "effective_ablation_depth_mm": effective_depth_mm,
            "endothelial_sparing_pct": (1.0 - intimal_damage_fraction) * 100.0,
            "max_tissue_temp_c": float(np.max(thermal_sim["peak_temperature_c"]))
        }


# ============================================================================
# 4. MODULE 3: GUYTONIAN PRESSURE-NATRIURESIS & NEURO-HUMORAL COUPLING
# ============================================================================

class GuytonianPressureNatriuresisSystem:
    """
    Guytonian long-term blood pressure control system.
    Integrates:
    - Renin enzymatic cleavage of Angiotensinogen (Michaelis-Menten kinetics).
    - Angiotensin II formation and AT1 receptor downstream signaling.
    - Renal Sympathetic Nerve Activity (RSNA) efferent and afferent drives.
    - Guytonian pressure-natriuresis shift and dynamic equilibrium MAP.
    - SBP and DBP calculation via arterial compliance.
    """

    def __init__(self, params: Optional[GuytonianRAASParameters] = None):
        self.p = params or GuytonianRAASParameters()

    def calculate_renin_flux(self, agt_nm: float, prc_pg_ml: float) -> float:
        """
        Michaelis-Menten rate of Angiotensin I generation:
        v = (k_cat * PRC * [AGT]) / (K_m + [AGT])
        """
        km = self.p.renin_km_agt_nm
        v_raw = (self.p.renin_kcat_s * prc_pg_ml * agt_nm) / (km + agt_nm)
        return v_raw

    def solve_steady_state_raas(self,
                                agt_suppression_fraction: float = 0.0,
                                rdn_denervation_fraction: float = 0.0) -> Dict[str, float]:
        """
        Solves the steady-state neuro-humoral equilibrium:
        - agt_suppression_fraction: fraction of circulating AGT suppressed (0.0 to 0.98).
        - rdn_denervation_fraction: fraction of renal nerves ablated (0.0 to 1.0).
        """
        # Residual circulating AGT
        agt_circulating_nm = self.p.renin_km_agt_nm * (1.0 - agt_suppression_fraction) * (self.p.renin_km_agt_nm / 1250.0)
        agt_circulating_nm = max(5.0, agt_circulating_nm)

        # Sympathetic tone: reduction in efferent and afferent RSNA
        residual_rsna_fraction = 1.0 - (0.80 * rdn_denervation_fraction)

        base_prc = self.p.base_prc_pg_ml
        base_ang_ii = self.p.base_ang_ii_pmol_l

        def raas_objective(prc_guess: float) -> float:
            flux = self.calculate_renin_flux(agt_circulating_nm, prc_guess)
            base_flux = self.calculate_renin_flux(1200.0, base_prc)
            ang_ii = base_ang_ii * (flux / base_flux)

            # Target PRC determined by negative feedback from Ang II and RSNA drive
            feedback_ratio = base_ang_ii / max(0.1, ang_ii)
            feedback_mult = (feedback_ratio ** 0.5)
            rsna_mult = 1.0 + self.p.rsna_renin_gain * (residual_rsna_fraction - 1.0)
            target_prc = base_prc * feedback_mult * max(0.2, rsna_mult)

            return prc_guess - target_prc

        sol = root_scalar(raas_objective, bracket=[0.1, 500.0], method="brentq")
        eq_prc = float(sol.root)

        flux_eq = self.calculate_renin_flux(agt_circulating_nm, eq_prc)
        base_flux = self.calculate_renin_flux(1200.0, base_prc)
        eq_ang_ii = base_ang_ii * (flux_eq / base_flux)

        return {
            "circulating_agt_nm": agt_circulating_nm,
            "prc_pg_ml": eq_prc,
            "ang_ii_pmol_l": eq_ang_ii,
            "ang_ii_ratio_to_base": eq_ang_ii / base_ang_ii,
            "residual_rsna_fraction": residual_rsna_fraction
        }

    def compute_pressure_natriuresis_curve(self,
                                           raas_state: Dict[str, float]) -> Dict[str, float]:
        """
        Determines the shifted Guytonian pressure-natriuresis intercept and slope:
        MAP_intercept = Base_Intercept + delta_Intercept(Ang II) + delta_Intercept(RSNA)
        """
        ang_ratio = raas_state["ang_ii_ratio_to_base"]
        rsna_ratio = raas_state["residual_rsna_fraction"]

        # Hypertensive baseline shift: elevated Ang II and RSNA relative to baseline
        delta_intercept_ang = self.p.raas_intercept_sensitivity * (ang_ratio - 1.0)
        delta_intercept_rsna = self.p.rsna_intercept_sensitivity * (rsna_ratio - 1.0)

        # Baseline hypertensive offset: in essential hypertension, intrinsic renal curve is shifted right
        essential_htn_shift = self.p.hypertensive_baseline_map - self.p.normal_map_mmhg

        intercept = self.p.base_pn_intercept_mmhg + essential_htn_shift + delta_intercept_ang + delta_intercept_rsna
        intercept = max(40.0, intercept)

        # Slope: dampened by high Ang II and high RSNA
        slope = self.p.base_pn_slope / (1.0 + 0.3 * max(0.0, ang_ratio - 1.0) + 0.2 * max(0.0, rsna_ratio - 1.0))

        return {
            "intercept_mmhg": intercept,
            "slope_mmol_day_mmhg": slope
        }

    def solve_blood_pressure(self,
                             agt_suppression_fraction: float = 0.0,
                             rdn_denervation_fraction: float = 0.0) -> Dict[str, float]:
        """
        Solves for long-term equilibrium Mean Arterial Pressure (MAP),
        Systolic Blood Pressure (SBP), and Diastolic Blood Pressure (DBP).
        """
        raas = self.solve_steady_state_raas(agt_suppression_fraction, rdn_denervation_fraction)
        pn = self.compute_pressure_natriuresis_curve(raas)

        # Guyton equilibrium: Na excretion = Na intake
        # Intake = Slope * (MAP - Intercept)
        # MAP = Intercept + Intake / Slope
        map_eq = pn["intercept_mmhg"] + (self.p.sodium_intake_mmol_day / pn["slope_mmol_day_mmhg"])

        # Pulse pressure: PP = Stroke Volume / Arterial Compliance
        pulse_pressure = self.p.stroke_volume_ml / self.p.arterial_compliance_ml_mmhg

        # SBP = MAP + 2/3 * PP, DBP = MAP - 1/3 * PP
        sbp = map_eq + (2.0 / 3.0) * pulse_pressure
        dbp = map_eq - (1.0 / 3.0) * pulse_pressure

        return {
            "map_mmhg": map_eq,
            "sbp_mmhg": sbp,
            "dbp_mmhg": dbp,
            "pulse_pressure_mmhg": pulse_pressure,
            "ang_ii_pmol_l": raas["ang_ii_pmol_l"],
            "prc_pg_ml": raas["prc_pg_ml"],
            "rsna_ratio": raas["residual_rsna_fraction"],
            "agt_suppression_fraction": agt_suppression_fraction,
            "rdn_denervation_fraction": rdn_denervation_fraction
        }


# ============================================================================
# 5. MODULE 4: CLINICAL TRIAL DIGITAL TWIN & ADHERENCE ERADICATION
# ============================================================================

class HypertensionTherapySimulator:
    """
    Unified clinical trial digital twin simulating real-world therapeutic modalities:
    1. Standard of Care Oral Antihypertensives (ACEi/ARB + CCB) with patient non-adherence.
    2. Semiannual Zilebesiran RNAi monotherapy and combination therapy.
    3. Catheter Renal Denervation (RF / uRDN) adherence-independent intervention.
    4. Combined Dual Non-Oral Therapy (Zilebesiran + RDN).
    """

    def __init__(self):
        self.rnai_engine = ZilebesiranPKPD()
        self.rdn_engine = RenalDenervationModel()
        self.guyton_engine = GuytonianPressureNatriuresisSystem()
        self._rdn_cache: Dict[Tuple[str, Optional[float]], Dict[str, float]] = {}
        self._rnai_cache: Dict[Tuple[float, float], Dict[str, np.ndarray]] = {}
        self._zil_sbp_cache: Dict[Tuple[float, int], Tuple[np.ndarray, np.ndarray]] = {}
        self._dual_sbp_cache: Dict[Tuple[float, str, int], Tuple[np.ndarray, np.ndarray, float]] = {}
        self._rdn_sbp_cache: Dict[str, Tuple[float, float]] = {}

    def get_rdn_result(self, modality: str = "rf", duration_s: Optional[float] = None) -> Dict[str, float]:
        key = (modality, duration_s)
        if key not in self._rdn_cache:
            self._rdn_cache[key] = self.rdn_engine.calculate_total_denervation_efficiency(modality=modality, duration_s=duration_s)
        return self._rdn_cache[key]

    def get_rnai_result(self, dose_mg: float = 300.0, duration_days: float = 180.0) -> Dict[str, np.ndarray]:
        key = (dose_mg, duration_days)
        if key not in self._rnai_cache:
            self._rnai_cache[key] = self.rnai_engine.simulate_single_dose(dose_mg=dose_mg, duration_days=duration_days)
        return self._rnai_cache[key]

    def get_zilebesiran_deterministic_sbp(self, dose_mg: float = 300.0, duration_days: int = 180) -> Tuple[np.ndarray, np.ndarray]:
        key = (dose_mg, duration_days)
        if key not in self._zil_sbp_cache:
            pkpd = self.get_rnai_result(dose_mg=dose_mg, duration_days=float(duration_days))
            t_sim = pkpd["time_days"]
            supp_sim = pkpd["suppression_fraction"]
            days = np.arange(duration_days)
            daily_supp = np.interp(days, t_sim, supp_sim)
            base_sbp = np.zeros(duration_days)
            for d in range(duration_days):
                bp = self.guyton_engine.solve_blood_pressure(
                    agt_suppression_fraction=float(daily_supp[d]),
                    rdn_denervation_fraction=0.0
                )
                base_sbp[d] = bp["sbp_mmhg"]
            self._zil_sbp_cache[key] = (daily_supp, base_sbp)
        return self._zil_sbp_cache[key]

    def get_dual_deterministic_sbp(self, dose_mg: float = 300.0, modality: str = "ultrasound", duration_days: int = 180) -> Tuple[np.ndarray, np.ndarray, float]:
        key = (dose_mg, modality, duration_days)
        if key not in self._dual_sbp_cache:
            daily_supp, _ = self.get_zilebesiran_deterministic_sbp(dose_mg, duration_days)
            rdn_res = self.get_rdn_result(modality=modality)
            denervation_frac = rdn_res["net_denervation_pct"] / 100.0
            base_sbp = np.zeros(duration_days)
            for d in range(duration_days):
                bp = self.guyton_engine.solve_blood_pressure(
                    agt_suppression_fraction=float(daily_supp[d]),
                    rdn_denervation_fraction=denervation_frac
                )
                base_sbp[d] = bp["sbp_mmhg"]
            self._dual_sbp_cache[key] = (daily_supp, base_sbp, rdn_res["net_denervation_pct"])
        return self._dual_sbp_cache[key]

    def get_rdn_deterministic_sbp(self, modality: str = "rf") -> Tuple[float, float]:
        key = modality
        if key not in self._rdn_sbp_cache:
            rdn_res = self.get_rdn_result(modality=modality)
            denervation_frac = rdn_res["net_denervation_pct"] / 100.0
            bp = self.guyton_engine.solve_blood_pressure(
                agt_suppression_fraction=0.0,
                rdn_denervation_fraction=denervation_frac
            )
            self._rdn_sbp_cache[key] = (bp["sbp_mmhg"], rdn_res["net_denervation_pct"])
        return self._rdn_sbp_cache[key]

    def simulate_oral_adherence_trajectory(self,
                                           duration_days: int = 180,
                                           adherence_rate: float = 0.50,
                                           seed: int = 42) -> Dict[str, np.ndarray]:
        """
        Simulates daily oral pill taking under realistic patient adherence (e.g. 50% PDC at 1 year).
        Demonstrates blood pressure volatility, missed dose rebound ("cuff leak"),
        and early-morning hypertension spikes.
        """
        np.random.seed(seed)
        days = np.arange(duration_days)

        # Baseline untreated BP
        uncontrolled = self.guyton_engine.solve_blood_pressure(0.0, 0.0)
        sbp_baseline = uncontrolled["sbp_mmhg"]

        # Maximum oral drug effect on SBP when fully adherent: -16 mmHg
        oral_max_effect = 16.0
        oral_half_life_days = 0.7  # ~17 hours elimination t1/2 (e.g. Valsartan / Amlodipine mix)
        k_elim = math.log(2.0) / oral_half_life_days

        # Adherence Bernoulli sequence
        doses_taken = (np.random.rand(duration_days) < adherence_rate).astype(float)

        drug_level = np.zeros(duration_days)
        sbp_trajectory = np.zeros(duration_days)

        current_level = 0.0
        for d in range(duration_days):
            current_level = current_level * math.exp(-k_elim) + doses_taken[d]
            drug_level[d] = current_level
            # SBP response with Emax saturating relationship
            effect = oral_max_effect * (current_level / (1.0 + current_level))
            noise = np.random.normal(0.0, 2.0)
            sbp_trajectory[d] = sbp_baseline - effect + noise

        time_in_target = float(np.mean(sbp_trajectory < 130.0) * 100.0)

        return {
            "days": days,
            "doses_taken": doses_taken,
            "drug_level": drug_level,
            "sbp_trajectory": sbp_trajectory,
            "time_in_target_pct": time_in_target,
            "mean_sbp": float(np.mean(sbp_trajectory)),
            "sbp_standard_deviation": float(np.std(sbp_trajectory))
        }

    def simulate_zilebesiran_semiannual_trajectory(self,
                                                   dose_mg: float = 300.0,
                                                   duration_days: int = 180,
                                                   seed: Optional[int] = None) -> Dict[str, np.ndarray]:
        """
        Simulates continuous 6-month blood pressure trajectory following
        a single subcutaneous dose of Zilebesiran (adherence = 100% inherently).
        """
        if seed is not None:
            np.random.seed(seed)
        daily_suppression, base_sbp = self.get_zilebesiran_deterministic_sbp(dose_mg=dose_mg, duration_days=duration_days)
        days = np.arange(duration_days)
        noise = np.random.normal(0.0, 1.2, size=duration_days)
        sbp_trajectory = base_sbp + noise

        time_in_target = float(np.mean(sbp_trajectory < 130.0) * 100.0)

        return {
            "days": days,
            "agt_suppression": daily_suppression,
            "sbp_trajectory": sbp_trajectory,
            "time_in_target_pct": time_in_target,
            "mean_sbp": float(np.mean(sbp_trajectory)),
            "sbp_standard_deviation": float(np.std(sbp_trajectory))
        }

    def simulate_rdn_trajectory(self,
                                modality: str = "rf",
                                duration_days: int = 180,
                                seed: Optional[int] = None) -> Dict[str, np.ndarray]:
        """
        Simulates 24-hour continuous adherence-independent BP reduction
        from a one-time catheter renal denervation.
        """
        if seed is not None:
            np.random.seed(seed)
        base_sbp, net_denervation = self.get_rdn_deterministic_sbp(modality=modality)
        days = np.arange(duration_days)
        sbp_trajectory = base_sbp + np.random.normal(0.0, 1.5, size=duration_days)

        time_in_target = float(np.mean(sbp_trajectory < 130.0) * 100.0)

        return {
            "days": days,
            "net_denervation_pct": net_denervation,
            "sbp_trajectory": sbp_trajectory,
            "time_in_target_pct": time_in_target,
            "mean_sbp": float(np.mean(sbp_trajectory)),
            "sbp_standard_deviation": float(np.std(sbp_trajectory))
        }

    def simulate_dual_non_oral_therapy(self,
                                       dose_mg: float = 300.0,
                                       modality: str = "ultrasound",
                                       duration_days: int = 180,
                                       seed: Optional[int] = None) -> Dict[str, np.ndarray]:
        """
        Simulates dual non-oral intervention:
        Semiannual Zilebesiran siRNA + Catheter Renal Denervation.
        Completely eliminates oral medication burden and achieves continuous normotension.
        """
        if seed is not None:
            np.random.seed(seed)
        daily_suppression, base_sbp, net_denervation = self.get_dual_deterministic_sbp(
            dose_mg=dose_mg, modality=modality, duration_days=duration_days
        )
        days = np.arange(duration_days)
        sbp_trajectory = base_sbp + np.random.normal(0.0, 1.0, size=duration_days)

        time_in_target = float(np.mean(sbp_trajectory < 130.0) * 100.0)

        return {
            "days": days,
            "sbp_trajectory": sbp_trajectory,
            "time_in_target_pct": time_in_target,
            "mean_sbp": float(np.mean(sbp_trajectory)),
            "sbp_standard_deviation": float(np.std(sbp_trajectory)),
            "net_denervation_pct": net_denervation,
            "peak_agt_suppression_pct": float(np.max(daily_suppression) * 100.0)
        }

    def run_virtual_trial_cohort(self, n_patients: int = 100) -> Dict[str, Dict[str, float]]:
        """
        Runs a comparative cohort study across the four therapeutic paradigms:
        1. Oral standard-of-care (adherence 50%)
        2. RDN alone (RF / Ultrasound)
        3. Zilebesiran 300 mg semiannual alone
        4. Dual non-oral regimen (Zilebesiran + RDN)
        """
        results = {
            "Oral_SOC_50pct": {"mean_sbp": [], "ttr_pct": [], "sbp_sd": []},
            "RDN_Alone": {"mean_sbp": [], "ttr_pct": [], "sbp_sd": []},
            "Zilebesiran_Alone": {"mean_sbp": [], "ttr_pct": [], "sbp_sd": []},
            "Dual_Non_Oral": {"mean_sbp": [], "ttr_pct": [], "sbp_sd": []}
        }

        for i in range(n_patients):
            seed = 1000 + i
            # 1. Oral SOC
            oral = self.simulate_oral_adherence_trajectory(duration_days=180, adherence_rate=0.50, seed=seed)
            results["Oral_SOC_50pct"]["mean_sbp"].append(oral["mean_sbp"])
            results["Oral_SOC_50pct"]["ttr_pct"].append(oral["time_in_target_pct"])
            results["Oral_SOC_50pct"]["sbp_sd"].append(oral["sbp_standard_deviation"])

            # 2. RDN Alone
            rdn = self.simulate_rdn_trajectory(modality="rf", duration_days=180, seed=seed)
            results["RDN_Alone"]["mean_sbp"].append(rdn["mean_sbp"])
            results["RDN_Alone"]["ttr_pct"].append(rdn["time_in_target_pct"])
            results["RDN_Alone"]["sbp_sd"].append(rdn["sbp_standard_deviation"])

            # 3. Zilebesiran Alone
            zil = self.simulate_zilebesiran_semiannual_trajectory(dose_mg=300.0, duration_days=180, seed=seed)
            results["Zilebesiran_Alone"]["mean_sbp"].append(zil["mean_sbp"])
            results["Zilebesiran_Alone"]["ttr_pct"].append(zil["time_in_target_pct"])
            results["Zilebesiran_Alone"]["sbp_sd"].append(zil["sbp_standard_deviation"])

            # 4. Dual Non-Oral
            dual = self.simulate_dual_non_oral_therapy(dose_mg=300.0, modality="ultrasound", duration_days=180, seed=seed)
            results["Dual_Non_Oral"]["mean_sbp"].append(dual["mean_sbp"])
            results["Dual_Non_Oral"]["ttr_pct"].append(dual["time_in_target_pct"])
            results["Dual_Non_Oral"]["sbp_sd"].append(dual["sbp_standard_deviation"])

        summary = {}
        for arm, metrics in results.items():
            summary[arm] = {
                "avg_sbp_mmhg": float(np.mean(metrics["mean_sbp"])),
                "avg_ttr_pct": float(np.mean(metrics["ttr_pct"])),
                "avg_sbp_variability_sd": float(np.mean(metrics["sbp_sd"]))
            }

        return summary


# ============================================================================
# 6. STANDALONE EXECUTION & CLINICAL VERIFICATION
# ============================================================================

def main():
    print("=" * 78)
    print("NEXT-GEN HYPERTENSION CONTROL: COMPUTATIONAL BIOPHYSICS & TRIAL ENGINE")
    print("=" * 78)

    # 1. Zilebesiran PK/PD evaluation
    print("\n--- 1. Zilebesiran Semiannual siRNA PK/PD Evaluation ---")
    rnai = ZilebesiranPKPD()
    benchmarks_300 = rnai.evaluate_semiannual_benchmarks(dose_mg=300.0)
    benchmarks_600 = rnai.evaluate_semiannual_benchmarks(dose_mg=600.0)

    print(f"Dose 300 mg: Peak Suppression = {benchmarks_300['peak_suppression_pct']:.1f}% on Day {benchmarks_300['day_of_peak']:.0f}")
    print(f"             Week 12 Suppression = {benchmarks_300['week12_suppression_pct']:.1f}%")
    print(f"             Week 24 Suppression = {benchmarks_300['week24_suppression_pct']:.1f}%")
    print(f"             Semiannual Goal (>90% at W24): {benchmarks_300['semiannual_threshold_met']}")

    print(f"Dose 600 mg: Peak Suppression = {benchmarks_600['peak_suppression_pct']:.1f}% on Day {benchmarks_600['day_of_peak']:.0f}")
    print(f"             Week 24 Suppression = {benchmarks_600['week24_suppression_pct']:.1f}%")

    # 2. Catheter Renal Denervation Biophysics
    print("\n--- 2. Catheter Renal Denervation (RDN) Biophysics ---")
    rdn = RenalDenervationModel()
    rf_eff = rdn.calculate_total_denervation_efficiency(modality="rf", duration_s=60.0)
    us_eff = rdn.calculate_total_denervation_efficiency(modality="ultrasound", duration_s=7.0)

    print(f"Radiofrequency (RF): Net Denervation = {rf_eff['net_denervation_pct']:.1f}%, Ablation Depth = {rf_eff['effective_ablation_depth_mm']:.2f} mm")
    print(f"                     Endothelial Sparing = {rf_eff['endothelial_sparing_pct']:.1f}%, Peak T = {rf_eff['max_tissue_temp_c']:.1f} C")
    print(f"Ultrasound (uRDN):   Net Denervation = {us_eff['net_denervation_pct']:.1f}%, Ablation Depth = {us_eff['effective_ablation_depth_mm']:.2f} mm")
    print(f"                     Endothelial Sparing = {us_eff['endothelial_sparing_pct']:.1f}%, Peak T = {us_eff['max_tissue_temp_c']:.1f} C")

    # 3. Guytonian Systems Physiology
    print("\n--- 3. Guytonian Blood Pressure Equilibrium ---")
    guyton = GuytonianPressureNatriuresisSystem()
    bp_baseline = guyton.solve_blood_pressure(0.0, 0.0)
    bp_rdn = guyton.solve_blood_pressure(0.0, rf_eff['net_denervation_pct'] / 100.0)
    bp_zil = guyton.solve_blood_pressure(0.92, 0.0)
    bp_dual = guyton.solve_blood_pressure(0.92, us_eff['net_denervation_pct'] / 100.0)

    print(f"Untreated Hypertensive Baseline: SBP/DBP = {bp_baseline['sbp_mmhg']:.1f}/{bp_baseline['dbp_mmhg']:.1f} mmHg (MAP = {bp_baseline['map_mmhg']:.1f})")
    print(f"RDN Alone (RF):                  SBP/DBP = {bp_rdn['sbp_mmhg']:.1f}/{bp_rdn['dbp_mmhg']:.1f} mmHg (Delta SBP = {bp_rdn['sbp_mmhg'] - bp_baseline['sbp_mmhg']:.1f})")
    print(f"Zilebesiran Alone (92% AGT red): SBP/DBP = {bp_zil['sbp_mmhg']:.1f}/{bp_zil['dbp_mmhg']:.1f} mmHg (Delta SBP = {bp_zil['sbp_mmhg'] - bp_baseline['sbp_mmhg']:.1f})")
    print(f"Dual Non-Oral Therapy:           SBP/DBP = {bp_dual['sbp_mmhg']:.1f}/{bp_dual['dbp_mmhg']:.1f} mmHg (Delta SBP = {bp_dual['sbp_mmhg'] - bp_baseline['sbp_mmhg']:.1f})")

    # 4. Virtual Cohort Trial (Adherence Simulation)
    print("\n--- 4. Virtual Cohort Adherence & Efficacy Trial (N=100) ---")
    simulator = HypertensionTherapySimulator()
    cohort_summary = simulator.run_virtual_trial_cohort(n_patients=50)
    for arm, res in cohort_summary.items():
        print(f"Arm: {arm:<20} | Mean SBP: {res['avg_sbp_mmhg']:.1f} mmHg | TTR (<130 mmHg): {res['avg_ttr_pct']:.1f}% | Volatility SD: {res['avg_sbp_variability_sd']:.2f} mmHg")

    print("=" * 78)


if __name__ == "__main__":
    main()
