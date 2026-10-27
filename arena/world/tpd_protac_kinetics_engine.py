"""
Targeted Protein Degradation (TPD) Kinetics & Cooperativity Engine
==================================================================
A comprehensive, biophysically grounded computational engine for modeling:
1. Three-body ternary complex equilibria [Target (T) - Degrader (D) - E3 Ligase (E)]
2. Binding cooperativity (alpha = Kd1 / Kd2), thermodynamic cycles, and free energy
3. The Hook Effect (two-site autoinhibition at supramicromolar degrader concentrations)
4. Catalytic degradation kinetics (polyubiquitination, 26S proteasome clearance, catalytic turnover TON)
5. E3 ligase selectivity profiling (CRBN, VHL, cIAP, MDM2)
6. Physicochemical and biophysical demarcation of PROTACs vs. Molecular Glues
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from scipy.optimize import brentq, minimize_scalar, least_squares
from scipy.integrate import solve_ivp


# ============================================================================
# 1. DATA STRUCTURES & CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class ThermodynamicParameters:
    """Thermodynamic and equilibrium parameters for ternary complex formation."""
    kd_target: float       # Binary dissociation constant T-D [M]
    kd_e3: float           # Binary dissociation constant E-D [M]
    alpha: float           # Cooperativity factor (dimensionless)
    temperature_k: float = 310.15  # Physiological temperature 37°C (310.15 K)
    gas_constant_r: float = 8.31446261815324  # J / (mol * K)

    def __post_init__(self):
        if self.kd_target <= 0:
            raise ValueError(f"kd_target must be positive, got {self.kd_target}")
        if self.kd_e3 <= 0:
            raise ValueError(f"kd_e3 must be positive, got {self.kd_e3}")
        if self.alpha <= 0:
            raise ValueError(f"Cooperativity alpha must be positive, got {self.alpha}")

    @property
    def delta_delta_g(self) -> float:
        """Cooperativity free energy change: Delta Delta G = -R * T * ln(alpha) [J/mol].
        Negative for positive cooperativity (alpha > 1), positive for negative cooperativity (alpha < 1).
        """
        return -self.gas_constant_r * self.temperature_k * math.log(self.alpha)

    @property
    def delta_delta_g_kcal(self) -> float:
        """Delta Delta G in kcal/mol (1 cal = 4.184 J)."""
        return self.delta_delta_g / 4184.0

    @property
    def kd_target_prime(self) -> float:
        """Ternary dissociation constant of Target to E-D complex: Kd_T' = Kd_T / alpha [M]."""
        return self.kd_target / self.alpha

    @property
    def kd_e3_prime(self) -> float:
        """Ternary dissociation constant of E3 to T-D complex: Kd_E' = Kd_E / alpha [M]."""
        return self.kd_e3 / self.alpha


@dataclass
class TernaryEquilibriumResult:
    """Equilibrium concentrations and mass balance validation for ternary system."""
    target_tot: float      # Total Target concentration [M]
    e3_tot: float          # Total E3 Ligase concentration [M]
    degrader_tot: float    # Total Degrader concentration [M]
    target_free: float     # Free Target [M]
    e3_free: float         # Free E3 Ligase [M]
    degrader_free: float   # Free Degrader [M]
    binary_td: float       # Binary complex Target-Degrader [M]
    binary_ed: float       # Binary complex E3-Degrader [M]
    ternary_ted: float     # Productive Ternary complex Target-E3-Degrader [M]
    mass_balance_error: float  # Maximum absolute error in mass conservation [M]

    @property
    def ternary_fraction_target(self) -> float:
        """Fraction of total target bound in ternary complex: [TED] / [T]_tot."""
        return self.ternary_ted / self.target_tot if self.target_tot > 0 else 0.0

    @property
    def ternary_fraction_e3(self) -> float:
        """Fraction of total E3 bound in ternary complex: [TED] / [E]_tot."""
        return self.ternary_ted / self.e3_tot if self.e3_tot > 0 else 0.0

    @property
    def binary_fraction_td(self) -> float:
        """Fraction of total target in binary TD complex: [TD] / [T]_tot."""
        return self.binary_td / self.target_tot if self.target_tot > 0 else 0.0

    @property
    def binary_fraction_ed(self) -> float:
        """Fraction of total E3 in binary ED complex: [ED] / [E]_tot."""
        return self.binary_ed / self.e3_tot if self.e3_tot > 0 else 0.0


@dataclass
class HookEffectMetrics:
    """Quantitative metrics describing the bell-shaped hook effect curve."""
    d_opt: float               # Degrader concentration producing maximal ternary complex [M]
    ted_max: float             # Maximal ternary complex concentration [M]
    fraction_target_max: float # Maximal fraction of target recruited into ternary complex
    c_hook_50_low: float       # Lower concentration where [TED] reaches 50% of [TED]_max [M]
    c_hook_50_high: float      # Upper concentration (hook regime) where [TED] drops to 50% of [TED]_max [M]
    fwhm_log10: float          # Full-width at half-maximum in log10 concentration units (span)
    c_hook_90_high: float      # Concentration where [TED] drops to 10% of [TED]_max (deep hook suppression) [M]
    asymmetry_ratio: float     # Ratio of high-dose span to low-dose span relative to d_opt


@dataclass
class DegradationKineticsParameters:
    """Rate constants for target synthesis, ubiquitination, and proteasomal degradation."""
    k_syn: float = 1.0e-10        # Target synthesis rate [M / s] (e.g. 0.36 uM/h = 1e-10 M/s)
    k_deg_basal: float = 1.9e-5   # Basal target degradation rate [1 / s] (~10.1 h half-life)
    k_ub: float = 0.05            # Ubiquitination rate constant from ternary complex [1 / s]
    k_dub: float = 0.005          # Deubiquitination rate constant by cellular DUBs [1 / s]
    k_cat_deg: float = 0.02       # 26S Proteasome degradation rate constant of polyUb-target [1 / s]
    k_on_t: float = 1.0e6         # Association rate for T + D [1 / (M * s)]
    k_on_e: float = 1.0e6         # Association rate for E + D [1 / (M * s)]


@dataclass
class DoseResponseResult:
    """Dose-response curve evaluation containing DC50, Dmax, and Hook onset."""
    concentrations: np.ndarray    # Tested total degrader concentrations [M]
    target_fractions: np.ndarray  # Remaining total target protein fraction relative to vehicle (0-1)
    ted_concentrations: np.ndarray # Equilibrium or kinetic ternary complex concentrations [M]
    dc50: float                   # Concentration producing 50% of maximum target degradation [M]
    d_max: float                  # Maximum target degradation fraction (0 to 1, where 1.0 = 100% degraded)
    d_opt_degradation: float      # Degrader concentration achieving maximal target clearance [M]
    hook_onset_conc: float        # Degrader concentration where degradation efficiency drops by 10% from peak [M]


@dataclass
class E3LigaseProfile:
    """Biophysical and clinical pharmacology profile for an E3 ubiquitin ligase."""
    name: str                     # e.g., 'CRBN', 'VHL', 'cIAP1', 'MDM2'
    complex_architecture: str     # Cullin-RING ligase subtype (e.g. CRL4-CRBN, CRL2-VHL)
    cellular_abundance_nm: float  # Typical endogenous cellular concentration [nM]
    canonical_ligand: str         # Reference binder (e.g. Pomalidomide, VH032)
    typical_kd_nm: float          # Typical binder affinity [nM]
    typical_cooperativity_alpha: float # Reference cooperativity with common targets
    typical_k_ub_s: float         # Catalytic ubiquitination rate [1 / s]
    autoubiquitination_rate_s: float # Rate of self-sacrifice / E3 auto-degradation [1 / s]
    primary_tissue_expression: str# High-expression tissue niches
    clinical_stage_prevalence: float # Percentage in clinical/preclinical degradation programs


@dataclass
class DegraderPhysicochemicalProfile:
    """Physicochemical descriptors and permeability metrics: PROTAC vs. Molecular Glue."""
    name: str
    modality: str                 # 'PROTAC' or 'Molecular Glue'
    e3_ligase: str                # 'CRBN', 'VHL', etc.
    target_protein: str           # e.g., 'BRD4', 'IKZF1', 'AR', 'GSPT1'
    molecular_weight: float       # Da (Lipinski threshold <= 500 Da)
    clogp: float                  # Calculated logP (Lipinski threshold <= 5)
    tpsa: float                   # Topological polar surface area [Angstrom^2]
    rotatable_bonds: int          # Rotatable bonds count (Lipinski/Veber threshold <= 10)
    hbd: int                      # Hydrogen bond donors (Lipinski threshold <= 5)
    hba: int                      # Hydrogen bond acceptors (Lipinski threshold <= 10)
    caco2_papp_1e6_cm_s: float    # Apparent permeability (x 10^-6 cm/s)
    cooperativity_alpha: float    # Ternary complex cooperativity
    chameleonic_potential: float  # Ratio of apolar/polar exposed surface area in closed vs open state (1.0 = rigid)

    @property
    def ro5_violations(self) -> int:
        """Count of Lipinski Rule of 5 violations."""
        v = 0
        if self.molecular_weight > 500:
            v += 1
        if self.clogp > 5.0:
            v += 1
        if self.hbd > 5:
            v += 1
        if self.hba > 10:
            v += 1
        return v

    @property
    def veber_violations(self) -> int:
        """Count of Veber rule violations (Rotatable bonds <= 10, tPSA <= 140 A^2)."""
        v = 0
        if self.rotatable_bonds > 10:
            v += 1
        if self.tpsa > 140.0:
            v += 1
        return v


# ============================================================================
# 2. THREE-BODY TERNARY COMPLEX EQUILIBRIUM SOLVER
# ============================================================================

class TernaryComplexEquilibrium:
    """
    Exact, mathematically rigorous equilibrium solver for the three-body system:
    Target (T) + Degrader (D) + E3 Ligase (E) <==> Ternary Complex (TED)
    
    Equations:
      [TD]  = [T][D] / Kd_T
      [ED]  = [E][D] / Kd_E
      [TED] = alpha * [T][E][D] / (Kd_T * Kd_E)
      
      [T]_tot = [T] + [TD] + [TED]
      [E]_tot = [E] + [ED] + [TED]
      [D]_tot = [D] + [TD] + [ED] + [TED]
    """

    def __init__(self, params: ThermodynamicParameters):
        self.params = params

    def solve(self, target_tot: float, e3_tot: float, degrader_tot: float) -> TernaryEquilibriumResult:
        """
        Solves the ternary equilibrium for given total concentrations of T, E, and D.
        Uses exact quadratic reduction for [E] and [T] given free [D], then 1D root-finding
        over free [D] in [0, degrader_tot]. Guaranteed unconditional convergence.
        """
        if target_tot <= 0.0 or e3_tot <= 0.0 or degrader_tot <= 0.0:
            # Handle zero boundary conditions exactly
            return TernaryEquilibriumResult(
                target_tot=max(0.0, target_tot),
                e3_tot=max(0.0, e3_tot),
                degrader_tot=max(0.0, degrader_tot),
                target_free=max(0.0, target_tot),
                e3_free=max(0.0, e3_tot),
                degrader_free=max(0.0, degrader_tot),
                binary_td=0.0,
                binary_ed=0.0,
                ternary_ted=0.0,
                mass_balance_error=0.0,
            )

        kd_t = self.params.kd_target
        kd_e = self.params.kd_e3
        alpha = self.params.alpha

        def compute_species_from_d_free(d_free: float) -> Tuple[float, float, float, float, float]:
            """Given free degrader d_free, analytically solve for [T]_free, [E]_free, [TD], [ED], [TED]."""
            a = 1.0 + d_free / kd_t
            b = 1.0 + d_free / kd_e
            c = (alpha * d_free) / (kd_t * kd_e)

            if c < 1e-30:
                # Cooperativity or free degrader is virtually zero
                t_free = target_tot / a
                e_free = e3_tot / b
                ted = 0.0
            else:
                # Solve quadratic: c * b * y^2 + (a * b + c * target_tot - c * e3_tot) * y - a * e3_tot = 0
                qa = c * b
                qb = a * b + c * (target_tot - e3_tot)
                qc = -a * e3_tot

                discriminant = qb * qb - 4.0 * qa * qc
                # Positive root:
                e_free = (-qb + math.sqrt(max(0.0, discriminant))) / (2.0 * qa)
                t_free = target_tot / (a + c * e_free)
                ted = c * t_free * e_free

            td = (t_free * d_free) / kd_t
            ed = (e_free * d_free) / kd_e
            return t_free, e_free, td, ed, ted

        def degrader_residual(d_free: float) -> float:
            """Residual: D_tot_calculated(d_free) - degrader_tot = 0."""
            t_free, e_free, td, ed, ted = compute_species_from_d_free(d_free)
            d_calc = d_free + td + ed + ted
            return d_calc - degrader_tot

        # Free degrader is strictly between 0 and degrader_tot
        res_low = degrader_residual(0.0)
        res_high = degrader_residual(degrader_tot)

        if abs(res_low) < 1e-25:
            d_free_sol = 0.0
        elif abs(res_high) < 1e-25:
            d_free_sol = degrader_tot
        else:
            d_free_sol = brentq(degrader_residual, 0.0, degrader_tot, xtol=1e-16, rtol=1e-14)

        t_free, e_free, td, ed, ted = compute_species_from_d_free(d_free_sol)

        # Validate mass balances
        t_calc = t_free + td + ted
        e_calc = e_free + ed + ted
        d_calc = d_free_sol + td + ed + ted

        err_t = abs(t_calc - target_tot)
        err_e = abs(e_calc - e3_tot)
        err_d = abs(d_calc - degrader_tot)
        max_err = max(err_t, err_e, err_d)

        return TernaryEquilibriumResult(
            target_tot=target_tot,
            e3_tot=e3_tot,
            degrader_tot=degrader_tot,
            target_free=t_free,
            e3_free=e_free,
            degrader_free=d_free_sol,
            binary_td=td,
            binary_ed=ed,
            ternary_ted=ted,
            mass_balance_error=max_err,
        )

    def titration_curve(
        self,
        target_tot: float,
        e3_tot: float,
        degrader_concentrations: np.ndarray,
    ) -> List[TernaryEquilibriumResult]:
        """Compute equilibrium profiles over an array of total degrader concentrations."""
        return [self.solve(target_tot, e3_tot, float(d_tot)) for d_tot in degrader_concentrations]


# ============================================================================
# 3. HOOK EFFECT & COOPERATIVITY ANALYZER
# ============================================================================

class HookEffectAnalyzer:
    """
    Mathematical and biophysical analysis of the two-site autoinhibitory Hook Effect.
    Characterizes:
      - Optimal degrader concentration [D]_opt producing peak ternary complex [TED]_max
      - Bell curve breadth (FWHM)
      - Upper and lower IC50/EC50 equivalents (dynamic degradation window)
      - Cooperativity impact on hook suppression threshold
    """

    def __init__(self, solver: TernaryComplexEquilibrium):
        self.solver = solver

    def analyze_hook_curve(
        self,
        target_tot: float,
        e3_tot: float,
        conc_min: float = 1.0e-12,
        conc_max: float = 1.0e-3,
        num_points: int = 400,
    ) -> HookEffectMetrics:
        """
        Calculates all key metrics of the bell-shaped hook effect curve.
        """
        log_concs = np.logspace(np.log10(conc_min), np.log10(conc_max), num_points)
        results = self.solver.titration_curve(target_tot, e3_tot, log_concs)
        ted_vals = np.array([r.ternary_ted for r in results])

        # Find maximum numerically
        max_idx = int(np.argmax(ted_vals))
        ted_max = float(ted_vals[max_idx])
        d_opt = float(log_concs[max_idx])

        # Refine maximum using bounded scalar minimization on -[TED]
        bracket_low = log_concs[max(0, max_idx - 2)]
        bracket_high = log_concs[min(num_points - 1, max_idx + 2)]
        
        opt_res = minimize_scalar(
            lambda log_c: -self.solver.solve(target_tot, e3_tot, 10.0**log_c).ternary_ted,
            bounds=(np.log10(bracket_low), np.log10(bracket_high)),
            method='bounded',
        )
        refined_d_opt = 10.0**float(opt_res.x)
        refined_res = self.solver.solve(target_tot, e3_tot, refined_d_opt)
        refined_ted_max = refined_res.ternary_ted
        frac_target_max = refined_res.ternary_fraction_target

        half_max = 0.5 * refined_ted_max
        tenth_max = 0.1 * refined_ted_max

        # Find lower 50% crossing (c_hook_50_low)
        def residual_50(log_c: float) -> float:
            c = 10.0**log_c
            return self.solver.solve(target_tot, e3_tot, c).ternary_ted - half_max

        def residual_10(log_c: float) -> float:
            c = 10.0**log_c
            return self.solver.solve(target_tot, e3_tot, c).ternary_ted - tenth_max

        # Brentq on lower half
        if residual_50(np.log10(conc_min)) * residual_50(np.log10(refined_d_opt)) < 0:
            log_c_50_low = brentq(residual_50, np.log10(conc_min), np.log10(refined_d_opt))
            c_hook_50_low = 10.0**log_c_50_low
        else:
            c_hook_50_low = conc_min

        # Brentq on upper half (hook suppression)
        if residual_50(np.log10(refined_d_opt)) * residual_50(np.log10(conc_max)) < 0:
            log_c_50_high = brentq(residual_50, np.log10(refined_d_opt), np.log10(conc_max))
            c_hook_50_high = 10.0**log_c_50_high
        else:
            c_hook_50_high = conc_max

        # Brentq for deep hook (10% of max on high-dose side)
        if residual_10(np.log10(refined_d_opt)) * residual_10(np.log10(conc_max)) < 0:
            log_c_90_high = brentq(residual_10, np.log10(refined_d_opt), np.log10(conc_max))
            c_hook_90_high = 10.0**log_c_90_high
        else:
            c_hook_90_high = conc_max

        fwhm_log10 = math.log10(c_hook_50_high) - math.log10(c_hook_50_low)
        
        # Asymmetry ratio: (log10(c_high) - log10(d_opt)) / (log10(d_opt) - log10(c_low))
        low_span = math.log10(refined_d_opt) - math.log10(c_hook_50_low)
        high_span = math.log10(c_hook_50_high) - math.log10(refined_d_opt)
        asymmetry = high_span / low_span if low_span > 0 else 1.0

        return HookEffectMetrics(
            d_opt=refined_d_opt,
            ted_max=refined_ted_max,
            fraction_target_max=frac_target_max,
            c_hook_50_low=c_hook_50_low,
            c_hook_50_high=c_hook_50_high,
            fwhm_log10=fwhm_log10,
            c_hook_90_high=c_hook_90_high,
            asymmetry_ratio=asymmetry,
        )

    @staticmethod
    def analytical_symmetric_d_opt(kd: float, alpha: float, target_tot: float) -> float:
        """
        Analytical approximation for symmetric systems where Kd_T = Kd_E = Kd and [T]_tot = [E]_tot = C0.
        When Kd >> C0, [D]_opt ~ Kd / sqrt(alpha).
        When C0 >> Kd, [D]_opt ~ C0 + Kd / sqrt(alpha).
        """
        return target_tot + kd / math.sqrt(alpha)


# ============================================================================
# 4. TPD KINETIC SIMULATOR: UBIQUITINATION & CATALYTIC TURNOVER
# ============================================================================

class TPDKineticsSimulator:
    """
    Non-equilibrium ordinary differential equation (ODE) simulation of TPD:
      Target synthesis, ternary complex formation, polyubiquitination,
      26S proteasome degradation, and catalytic recycling of PROTAC & E3 ligase.
    """

    def __init__(
        self,
        thermo_params: ThermodynamicParameters,
        kinetic_params: Optional[DegradationKineticsParameters] = None,
    ):
        self.thermo = thermo_params
        self.kinetics = kinetic_params or DegradationKineticsParameters()

    def simulate_time_course(
        self,
        target_tot_0: float,
        e3_tot_0: float,
        degrader_tot: float,
        duration_hours: float = 24.0,
        num_time_points: int = 500,
    ) -> Dict[str, np.ndarray]:
        """
        Integrates the 5-state dynamic biochemical ODE system:
          y[0] = [T]     (Free Target)
          y[1] = [E]     (Free E3 Ligase)
          y[2] = [D]     (Free Degrader)
          y[3] = [TD]    (Binary Target-Degrader)
          y[4] = [ED]    (Binary E3-Degrader)
          y[5] = [TED]   (Productive Ternary Complex)
          y[6] = [TED_ub](Ubiquitinated Ternary Complex)
          y[7] = [P_deg] (Cumulative degraded target peptides)
        """
        t_span = (0.0, duration_hours * 3600.0)
        t_eval = np.linspace(0.0, duration_hours * 3600.0, num_time_points)

        # Microscopic rate constants:
        k_on_t = self.kinetics.k_on_t
        k_off_t = k_on_t * self.thermo.kd_target
        k_on_e = self.kinetics.k_on_e
        k_off_e = k_on_e * self.thermo.kd_e3

        # For ternary complex assembly:
        # TD + E <-> TED: k_on_ted_e, k_off_ted_e = k_on_ted_e * (kd_e / alpha)
        # ED + T <-> TED: k_on_ted_t, k_off_ted_t = k_on_ted_t * (kd_t / alpha)
        k_on_ted_e = k_on_e
        k_off_ted_e = k_on_ted_e * (self.thermo.kd_e3 / self.thermo.alpha)
        k_on_ted_t = k_on_t
        k_off_ted_t = k_on_ted_t * (self.thermo.kd_target / self.thermo.alpha)

        k_syn = self.kinetics.k_syn
        k_deg_basal = self.kinetics.k_deg_basal
        k_ub = self.kinetics.k_ub
        k_dub = self.kinetics.k_dub
        k_cat_deg = self.kinetics.k_cat_deg

        # Initial state: steady-state target without degrader
        # At t=0, degrader is introduced instantaneously
        y0 = np.array([
            target_tot_0,  # [T]
            e3_tot_0,      # [E]
            degrader_tot,  # [D]
            0.0,           # [TD]
            0.0,           # [ED]
            0.0,           # [TED]
            0.0,           # [TED_ub]
            0.0,           # [P_deg]
        ], dtype=np.float64)

        def odes(t: float, y: np.ndarray) -> np.ndarray:
            t_free = max(0.0, y[0])
            e_free = max(0.0, y[1])
            d_free = max(0.0, y[2])
            td = max(0.0, y[3])
            ed = max(0.0, y[4])
            ted = max(0.0, y[5])
            ted_ub = max(0.0, y[6])

            # Fluxes:
            v_td_form = k_on_t * t_free * d_free - k_off_t * td
            v_ed_form = k_on_e * e_free * d_free - k_off_e * ed

            v_ted_from_td = k_on_ted_e * td * e_free - k_off_ted_e * ted
            v_ted_from_ed = k_on_ted_t * ed * t_free - k_off_ted_t * ted

            # Catalytic ubiquitination and deubiquitination:
            v_ub = k_ub * ted - k_dub * ted_ub

            # Proteasomal degradation: frees E and D, turns target into peptides P
            v_deg = k_cat_deg * ted_ub

            # Basal synthesis and basal degradation (of all target-containing species):
            v_syn = k_syn
            v_basal_t = k_deg_basal * t_free
            v_basal_td = k_deg_basal * td
            v_basal_ted = k_deg_basal * ted

            # Derivatives:
            dt_free = v_syn - v_basal_t - v_td_form - v_ted_from_ed
            de_free = -v_ed_form - v_ted_from_td + v_deg + v_basal_ted
            dd_free = -v_td_form - v_ed_form + v_deg + v_basal_td + v_basal_ted
            dtd = v_td_form - v_ted_from_td - v_basal_td
            ded = v_ed_form - v_ted_from_ed
            dted = v_ted_from_td + v_ted_from_ed - v_ub - v_basal_ted
            dted_ub = v_ub - v_deg
            dp_deg = v_deg

            return np.array([dt_free, de_free, dd_free, dtd, ded, dted, dted_ub, dp_deg])

        sol = solve_ivp(
            odes,
            t_span,
            y0,
            t_eval=t_eval,
            method='Radau',  # Stiff ODE solver
            rtol=1e-7,
            atol=1e-11,
        )

        time_hours = sol.t / 3600.0
        t_total = sol.y[0] + sol.y[3] + sol.y[5] + sol.y[6]  # [T] + [TD] + [TED] + [TED_ub]
        e_total = sol.y[1] + sol.y[4] + sol.y[5] + sol.y[6]
        d_total = sol.y[2] + sol.y[3] + sol.y[4] + sol.y[5] + sol.y[6]

        return {
            'time_hours': time_hours,
            'target_total': t_total,
            'target_fraction': t_total / target_tot_0,
            'free_target': sol.y[0],
            'free_e3': sol.y[1],
            'free_degrader': sol.y[2],
            'binary_td': sol.y[3],
            'binary_ed': sol.y[4],
            'ternary_ted': sol.y[5],
            'ternary_ted_ub': sol.y[6],
            'degraded_peptides': sol.y[7],
            'e3_total': e_total,
            'degrader_total': d_total,
        }

    def compute_steady_state_dose_response(
        self,
        target_tot_baseline: float,
        e3_tot: float,
        concentrations: np.ndarray,
        incubation_time_hours: float = 16.0,
    ) -> DoseResponseResult:
        """
        Generates the pharmacological dose-response curve ([Target] vs [Degrader]),
        calculating DC50, Dmax, optimal degradation concentration, and hook onset.
        """
        # Steady state target fraction:
        # Quasi-steady state target balance: k_syn = k_deg_basal * [T]_tot + k_cat_eff * [TED]
        # At baseline: target_tot_baseline = k_syn / k_deg_basal
        k_syn = self.kinetics.k_deg_basal * target_tot_baseline
        eff_kinetics = DegradationKineticsParameters(
            k_syn=k_syn,
            k_deg_basal=self.kinetics.k_deg_basal,
            k_ub=self.kinetics.k_ub,
            k_dub=self.kinetics.k_dub,
            k_cat_deg=self.kinetics.k_cat_deg,
        )
        sim = TPDKineticsSimulator(self.thermo, eff_kinetics)

        eq_solver = TernaryComplexEquilibrium(self.thermo)
        target_fractions = []
        ted_concs = []

        for c in concentrations:
            # Run dynamic ODE to specified incubation time
            res = sim.simulate_time_course(
                target_tot_0=target_tot_baseline,
                e3_tot_0=e3_tot,
                degrader_tot=float(c),
                duration_hours=incubation_time_hours,
                num_time_points=100,
            )
            final_frac = float(res['target_fraction'][-1])
            final_ted = float(res['ternary_ted'][-1] + res['ternary_ted_ub'][-1])
            target_fractions.append(final_frac)
            ted_concs.append(final_ted)

        frac_arr = np.array(target_fractions)
        ted_arr = np.array(ted_concs)

        # Minimum fraction of target remaining = 1.0 - Dmax
        min_idx = int(np.argmin(frac_arr))
        min_target_frac = frac_arr[min_idx]
        d_max = 1.0 - min_target_frac
        d_opt_deg = float(concentrations[min_idx])

        # DC50: concentration that achieves 50% of maximum target degradation
        # target_level = 1.0 - 0.5 * d_max
        target_half_deg = 1.0 - 0.5 * d_max
        dc50 = concentrations[0]
        for i in range(min_idx):
            if frac_arr[i] <= target_half_deg:
                # Interpolate
                c_prev = concentrations[i - 1]
                c_curr = concentrations[i]
                f_prev = frac_arr[i - 1]
                f_curr = frac_arr[i]
                if abs(f_curr - f_prev) > 1e-12:
                    log_dc50 = math.log10(c_prev) + (target_half_deg - f_prev) / (f_curr - f_prev) * (math.log10(c_curr) - math.log10(c_prev))
                    dc50 = 10.0**log_dc50
                else:
                    dc50 = c_curr
                break

        # Hook onset: concentration after d_opt_deg where target fraction increases by 10% of d_max
        hook_threshold = min_target_frac + 0.10 * d_max
        hook_onset_conc = concentrations[-1]
        for i in range(min_idx, len(concentrations)):
            if frac_arr[i] >= hook_threshold:
                hook_onset_conc = float(concentrations[i])
                break

        return DoseResponseResult(
            concentrations=concentrations,
            target_fractions=frac_arr,
            ted_concentrations=ted_arr,
            dc50=dc50,
            d_max=d_max,
            d_opt_degradation=d_opt_deg,
            hook_onset_conc=hook_onset_conc,
        )

    def catalytic_turnover_number(
        self,
        target_tot_0: float,
        e3_tot_0: float,
        degrader_tot: float,
        duration_hours: float = 24.0,
    ) -> float:
        """
        Quantifies catalytic turnover (TON):
        Total target molecules degraded per degrader molecule present:
        TON = [P_deg](t) / [D]_tot
        """
        res = self.simulate_time_course(target_tot_0, e3_tot_0, degrader_tot, duration_hours=duration_hours)
        peptides_formed = float(res['degraded_peptides'][-1])
        return peptides_formed / degrader_tot if degrader_tot > 0 else 0.0


# ============================================================================
# 5. E3 LIGASE SELECTIVITY PROFILING ENGINE
# ============================================================================

class E3LigaseProfileDatabase:
    """
    Curated database and comparative analysis of clinical and chemical E3 ubiquitin ligases:
    CRBN, VHL, cIAP1, and MDM2.
    """

    PROFILES: Dict[str, E3LigaseProfile] = {
        'CRBN': E3LigaseProfile(
            name='CRBN',
            complex_architecture='CRL4^CRBN (Cul4A/B-Rbx1-DDB1-CRBN)',
            cellular_abundance_nm=65.0,  # ~65 nM in typical myeloma/epithelial lines
            canonical_ligand='Pomalidomide / Lenalidomide / CC-220',
            typical_kd_nm=150.0,
            typical_cooperativity_alpha=8.5,  # Variable: 0.1 to >100 for glues
            typical_k_ub_s=0.08,
            autoubiquitination_rate_s=0.0002,  # Low basal auto-ubiquitination
            primary_tissue_expression='Ubiquitous (Hematopoietic, lymphoid, CNS)',
            clinical_stage_prevalence=52.0,  # ~52% of all TPD clinical candidates
        ),
        'VHL': E3LigaseProfile(
            name='VHL',
            complex_architecture='CRL2^VHL (Cul2-Rbx1-Elongin B/C-VHL)',
            cellular_abundance_nm=140.0,  # ~140 nM in cancer cells
            canonical_ligand='VH032 / VH101 (Hydroxyproline peptidomimetics)',
            typical_kd_nm=180.0,
            typical_cooperativity_alpha=18.0,  # High positive cooperativity with BRD4 (MZ1)
            typical_k_ub_s=0.12,
            autoubiquitination_rate_s=0.0001,  # Minimal auto-ubiquitination
            primary_tissue_expression='Ubiquitous (High in kidney, prostate, liver)',
            clinical_stage_prevalence=36.0,  # ~36% of TPD clinical candidates
        ),
        'cIAP1': E3LigaseProfile(
            name='cIAP1',
            complex_architecture='RING monomer/homodimer (BIRC2/BIRC3)',
            cellular_abundance_nm=45.0,
            canonical_ligand='SMAC Mimetics (LCL161, Bestatin/SNIPERs)',
            typical_kd_nm=35.0,
            typical_cooperativity_alpha=1.2,  # Often neutral or slightly negative
            typical_k_ub_s=0.25,  # Rapid ubiquitination
            autoubiquitination_rate_s=0.045,  # Very high auto-ubiquitination (suicidal degradation)
            primary_tissue_expression='Epithelial, lung, colon, ovarian',
            clinical_stage_prevalence=7.0,  # ~7% preclinical/clinical
        ),
        'MDM2': E3LigaseProfile(
            name='MDM2',
            complex_architecture='RING E3 ligase (MDM2-MDMX heterodimer)',
            cellular_abundance_nm=25.0,  # Basal level low, tightly p53-regulated
            canonical_ligand='Nutlin-3a / Idasanutlin / RG7112',
            typical_kd_nm=90.0,
            typical_cooperativity_alpha=0.65,  # Often negative cooperativity due to steric clashes
            typical_k_ub_s=0.05,
            autoubiquitination_rate_s=0.015,  # Moderate self-degradation
            primary_tissue_expression='Sarcomas, glioblastoma, p53-amplified carcinomas',
            clinical_stage_prevalence=5.0,  # ~5%
        ),
    }

    @classmethod
    def get_profile(cls, name: str) -> E3LigaseProfile:
        # Match case-insensitively
        norm_map = {k.lower(): v for k, v in cls.PROFILES.items()}
        target_key = name.lower()
        if target_key in norm_map:
            return norm_map[target_key]
        raise KeyError(f"E3 ligase '{name}' not found. Available: {list(cls.PROFILES.keys())}")

    @classmethod
    def calculate_selectivity_ratio(
        cls,
        target_tot: float,
        degrader_tot: float,
        kd_target: float,
        e3_1_name: str,
        e3_2_name: str,
        kd_e3_1: float,
        kd_e3_2: float,
        alpha_1: float,
        alpha_2: float,
    ) -> Dict[str, float]:
        """
        Quantifies competitive E3 selectivity ratio:
          S = [TED_1] / [TED_2]
        under identical or tissue-specific E3 concentrations.
        """
        p1 = cls.get_profile(e3_1_name)
        p2 = cls.get_profile(e3_2_name)

        e3_1_tot = p1.cellular_abundance_nm * 1e-9
        e3_2_tot = p2.cellular_abundance_nm * 1e-9

        solver1 = TernaryComplexEquilibrium(ThermodynamicParameters(kd_target, kd_e3_1, alpha_1))
        solver2 = TernaryComplexEquilibrium(ThermodynamicParameters(kd_target, kd_e3_2, alpha_2))

        res1 = solver1.solve(target_tot, e3_1_tot, degrader_tot)
        res2 = solver2.solve(target_tot, e3_2_tot, degrader_tot)

        ratio = res1.ternary_ted / res2.ternary_ted if res2.ternary_ted > 0 else float('inf')

        return {
            'ternary_ted_e3_1': res1.ternary_ted,
            'ternary_ted_e3_2': res2.ternary_ted,
            'selectivity_ratio': ratio,
            'cooperativity_advantage': alpha_1 / alpha_2,
            'affinity_advantage': kd_e3_2 / kd_e3_1,
        }


# ============================================================================
# 6. BIFUNCTIONAL PROTACS VS. MOLECULAR GLUES: COMPARATIVE ANALYSIS
# ============================================================================

class PROTACvsGlueComparator:
    """
    Biophysical, structural, and pharmacokinetic comparison between:
    - Bifunctional PROTACs (heterobifunctional degraders with linkers)
    - Molecular Glues (monovalent/neomorphic interface remodelers)
    """

    BENCHMARK_COMPOUNDS: List[DegraderPhysicochemicalProfile] = [
        # --- PROTACs ---
        DegraderPhysicochemicalProfile(
            name='MZ1',
            modality='PROTAC',
            e3_ligase='VHL',
            target_protein='BRD4 (BD2 selective)',
            molecular_weight=1002.6,
            clogp=4.8,
            tpsa=205.8,
            rotatable_bonds=18,
            hbd=4,
            hba=14,
            caco2_papp_1e6_cm_s=0.45,  # Low permeability (typical bRo5)
            cooperativity_alpha=20.0,   # Strong positive cooperativity
            chameleonic_potential=1.85, # Substantial conformational shielding
        ),
        DegraderPhysicochemicalProfile(
            name='ARV-110 (Bavdegalutamide)',
            modality='PROTAC',
            e3_ligase='CRBN',
            target_protein='Androgen Receptor (AR / AR-T878A)',
            molecular_weight=812.3,
            clogp=5.6,
            tpsa=172.4,
            rotatable_bonds=14,
            hbd=3,
            hba=11,
            caco2_papp_1e6_cm_s=0.82,
            cooperativity_alpha=3.2,
            chameleonic_potential=1.65,
        ),
        DegraderPhysicochemicalProfile(
            name='ARV-471 (Vepdegestrant)',
            modality='PROTAC',
            e3_ligase='VHL',
            target_protein='Estrogen Receptor (ERalpha / Y537S)',
            molecular_weight=723.9,
            clogp=4.2,
            tpsa=158.2,
            rotatable_bonds=11,
            hbd=3,
            hba=9,
            caco2_papp_1e6_cm_s=1.20,
            cooperativity_alpha=4.8,
            chameleonic_potential=1.55,
        ),
        DegraderPhysicochemicalProfile(
            name='dBET6',
            modality='PROTAC',
            e3_ligase='CRBN',
            target_protein='BRD4 / Pan-BET',
            molecular_weight=794.3,
            clogp=4.1,
            tpsa=176.5,
            rotatable_bonds=13,
            hbd=3,
            hba=11,
            caco2_papp_1e6_cm_s=0.62,
            cooperativity_alpha=1.0,   # Non-cooperative
            chameleonic_potential=1.40,
        ),
        # --- Molecular Glues ---
        DegraderPhysicochemicalProfile(
            name='Thalidomide',
            modality='Molecular Glue',
            e3_ligase='CRBN',
            target_protein='IKZF1 / IKZF3 / SALL4',
            molecular_weight=258.23,
            clogp=0.15,
            tpsa=75.6,
            rotatable_bonds=1,
            hbd=1,
            hba=4,
            caco2_papp_1e6_cm_s=18.5,  # High permeability (Ro5 compliant)
            cooperativity_alpha=250.0,  # Massive apparent cooperativity
            chameleonic_potential=1.02, # Rigid, no conformational change required
        ),
        DegraderPhysicochemicalProfile(
            name='Lenalidomide',
            modality='Molecular Glue',
            e3_ligase='CRBN',
            target_protein='IKZF1 / IKZF3 / CK1alpha',
            molecular_weight=259.26,
            clogp=-0.40,
            tpsa=84.4,
            rotatable_bonds=1,
            hbd=2,
            hba=4,
            caco2_papp_1e6_cm_s=12.4,
            cooperativity_alpha=650.0,
            chameleonic_potential=1.04,
        ),
        DegraderPhysicochemicalProfile(
            name='CC-90009',
            modality='Molecular Glue',
            e3_ligase='CRBN',
            target_protein='GSPT1 (Translation termination factor)',
            molecular_weight=465.5,
            clogp=2.45,
            tpsa=112.8,
            rotatable_bonds=4,
            hbd=2,
            hba=6,
            caco2_papp_1e6_cm_s=8.70,
            cooperativity_alpha=1200.0, # Exceptional neomorphic selectivity
            chameleonic_potential=1.15,
        ),
        DegraderPhysicochemicalProfile(
            name='Indisulam',
            modality='Molecular Glue',
            e3_ligase='DCAF15',
            target_protein='RBM39 (Splicing factor)',
            molecular_weight=385.8,
            clogp=1.80,
            tpsa=98.7,
            rotatable_bonds=4,
            hbd=2,
            hba=5,
            caco2_papp_1e6_cm_s=14.2,
            cooperativity_alpha=800.0,
            chameleonic_potential=1.08,
        ),
    ]

    @classmethod
    def get_compounds_by_modality(cls, modality: str) -> List[DegraderPhysicochemicalProfile]:
        return [c for c in cls.BENCHMARK_COMPOUNDS if c.modality.lower() == modality.lower()]

    @classmethod
    def compute_modality_statistics(cls) -> Dict[str, Dict[str, float]]:
        """Computes mean and std of physicochemical properties for PROTACs vs Glues."""
        protacs = cls.get_compounds_by_modality('PROTAC')
        glues = cls.get_compounds_by_modality('Molecular Glue')

        def stats_for_group(group: List[DegraderPhysicochemicalProfile]) -> Dict[str, float]:
            return {
                'mean_mw': float(np.mean([c.molecular_weight for c in group])),
                'std_mw': float(np.std([c.molecular_weight for c in group])),
                'mean_clogp': float(np.mean([c.clogp for c in group])),
                'std_clogp': float(np.std([c.clogp for c in group])),
                'mean_tpsa': float(np.mean([c.tpsa for c in group])),
                'std_tpsa': float(np.std([c.tpsa for c in group])),
                'mean_rotb': float(np.mean([c.rotatable_bonds for c in group])),
                'std_rotb': float(np.std([c.rotatable_bonds for c in group])),
                'mean_papp': float(np.mean([c.caco2_papp_1e6_cm_s for c in group])),
                'std_papp': float(np.std([c.caco2_papp_1e6_cm_s for c in group])),
                'mean_ro5_violations': float(np.mean([c.ro5_violations for c in group])),
                'mean_alpha': float(np.mean([c.cooperativity_alpha for c in group])),
            }

        return {
            'PROTAC': stats_for_group(protacs),
            'Molecular Glue': stats_for_group(glues),
        }

    @staticmethod
    def estimate_chameleonic_permeability_enhancement(
        tpsa_open: float,
        chameleonic_potential: float,
    ) -> float:
        """
        Empirical model of permeability enhancement due to chameleonic intramolecular
        hydrogen bonding (IMHB) in apolar membrane interiors:
          tPSA_effective = tPSA_open / chameleonic_potential
          Fold enhancement = exp(0.025 * (tPSA_open - tPSA_effective))
        """
        tpsa_eff = tpsa_open / chameleonic_potential
        delta_tpsa = tpsa_open - tpsa_eff
        return math.exp(0.025 * delta_tpsa)


# ============================================================================
# 7. TRI-COMPLEX RAS(ON) & MOLECULAR GLUE HOOK IMMUNITY COMPARATOR
# ============================================================================

@dataclass
class TriComplexHookComparison:
    """Quantitative comparison of Hook effect parameters across PROTACs and Glues."""
    modality_name: str
    target_name: str
    presenter_name: str
    target_tot_m: float
    presenter_tot_m: float
    kd_target_binary_m: float
    kd_presenter_binary_m: float
    cooperativity_alpha: float
    kd_target_ternary_m: float
    d_opt_m: float
    ted_max_m: float
    c_hook_50_high_m: float
    fwhm_log10: float
    hook_shift_fold_vs_protac: float
    is_hook_immune: bool
    morrison_plateau_m: float


class TricomplexAndGlueHookComparator:
    """
    Mathematical and pharmacological comparison of ternary complex dynamics between:
    1. Heterobifunctional PROTACs (e.g. MZ1, ARV-110)
    2. Neomorphic E3 Molecular Glues (e.g. CC-90009, Indisulam, Lenalidomide)
    3. Tri-Complex RAS(ON) Molecular Glues (e.g. RMC-6236 recruiting Cyclophilin A)

    Establishes and verifies:
    - The Hook Immunity Theorem: lim_{Kd_T -> inf} [TED]([D] -> inf) = [TED]_Morrison > 0
    - Chaperone abundance buffering: [CypA] = 5-10 uM vs [E3] = 50-150 nM
    - Hook shift fold factor: H_shift = C_hook_50(Glue) / C_hook_50(PROTAC) > 50x to 15,000x
    """

    @staticmethod
    def calculate_morrison_plateau(target_tot: float, presenter_tot: float, kd_ternary: float) -> float:
        """
        Calculates the exact asymptotic ternary complex concentration as [D] -> inf
        in an ideal molecular glue where Kd_target_binary -> infinity:
          [TED]_plateau = 0.5 * (T + E + Kd' - sqrt((T + E + Kd')^2 - 4 * T * E))
        """
        sum_terms = target_tot + presenter_tot + kd_ternary
        discriminant = sum_terms * sum_terms - 4.0 * target_tot * presenter_tot
        return 0.5 * (sum_terms - math.sqrt(max(0.0, discriminant)))

    @classmethod
    def compare_paradigms(
        cls,
        target_tot: float = 100e-9,
        protac_e3_tot: float = 140e-9,      # VHL baseline ~140 nM
        glue_crbn_tot: float = 65e-9,       # CRBN baseline ~65 nM
        cypa_tot: float = 5.0e-6,           # Cytosolic CypA ~5.0 uM
    ) -> Dict[str, TriComplexHookComparison]:
        """
        Performs comparative hook analysis across standard archetypes:
        1. PROTAC MZ1 (BRD4 + VHL)
        2. PROTAC ARV-110 (AR + CRBN)
        3. Molecular Glue CC-90009 (GSPT1 + CRBN)
        4. Tri-Complex Glue RMC-6236 (KRAS:GTP + CypA, alpha=10000 glue model)
        5. Tri-Complex Glue RMC-6236 (KRAS:GTP + CypA, alpha=18.0 Hypatia model)
        """
        # Baseline reference: MZ1 PROTAC
        tp_mz1 = ThermodynamicParameters(kd_target=50e-9, kd_e3=180e-9, alpha=20.0)
        s_mz1 = TernaryComplexEquilibrium(tp_mz1)
        h_mz1 = HookEffectAnalyzer(s_mz1)
        m_mz1 = h_mz1.analyze_hook_curve(target_tot, protac_e3_tot, conc_min=1e-12, conc_max=1e-2)

        ref_hook_50 = m_mz1.c_hook_50_high

        # 1. MZ1
        res_mz1 = TriComplexHookComparison(
            modality_name="Heterobifunctional PROTAC",
            target_name="BRD4 (BD2)",
            presenter_name="VHL",
            target_tot_m=target_tot,
            presenter_tot_m=protac_e3_tot,
            kd_target_binary_m=50e-9,
            kd_presenter_binary_m=180e-9,
            cooperativity_alpha=20.0,
            kd_target_ternary_m=2.5e-9,
            d_opt_m=m_mz1.d_opt,
            ted_max_m=m_mz1.ted_max,
            c_hook_50_high_m=m_mz1.c_hook_50_high,
            fwhm_log10=m_mz1.fwhm_log10,
            hook_shift_fold_vs_protac=1.0,
            is_hook_immune=False,
            morrison_plateau_m=0.0,
        )

        # 2. ARV-110
        tp_arv = ThermodynamicParameters(kd_target=35e-9, kd_e3=150e-9, alpha=3.2)
        s_arv = TernaryComplexEquilibrium(tp_arv)
        h_arv = HookEffectAnalyzer(s_arv)
        m_arv = h_arv.analyze_hook_curve(target_tot, glue_crbn_tot, conc_min=1e-12, conc_max=1e-2)

        res_arv = TriComplexHookComparison(
            modality_name="Heterobifunctional PROTAC",
            target_name="Androgen Receptor",
            presenter_name="CRBN",
            target_tot_m=target_tot,
            presenter_tot_m=glue_crbn_tot,
            kd_target_binary_m=35e-9,
            kd_presenter_binary_m=150e-9,
            cooperativity_alpha=3.2,
            kd_target_ternary_m=35e-9 / 3.2,
            d_opt_m=m_arv.d_opt,
            ted_max_m=m_arv.ted_max,
            c_hook_50_high_m=m_arv.c_hook_50_high,
            fwhm_log10=m_arv.fwhm_log10,
            hook_shift_fold_vs_protac=m_arv.c_hook_50_high / ref_hook_50,
            is_hook_immune=False,
            morrison_plateau_m=0.0,
        )

        # 3. CC-90009 (Molecular Glue)
        # Kd_target_binary ~ 100 uM (very weak), alpha ~ 1200 -> Kd_ter ~ 83.3 nM
        kd_t_cc = 100e-6
        alpha_cc = 1200.0
        kd_ter_cc = kd_t_cc / alpha_cc
        tp_cc = ThermodynamicParameters(kd_target=kd_t_cc, kd_e3=150e-9, alpha=alpha_cc)
        s_cc = TernaryComplexEquilibrium(tp_cc)
        h_cc = HookEffectAnalyzer(s_cc)
        m_cc = h_cc.analyze_hook_curve(target_tot, glue_crbn_tot, conc_min=1e-12, conc_max=1e-1)
        morrison_cc = cls.calculate_morrison_plateau(target_tot, glue_crbn_tot, kd_ter_cc)

        res_cc = TriComplexHookComparison(
            modality_name="Neomorphic E3 Molecular Glue",
            target_name="GSPT1",
            presenter_name="CRBN",
            target_tot_m=target_tot,
            presenter_tot_m=glue_crbn_tot,
            kd_target_binary_m=kd_t_cc,
            kd_presenter_binary_m=150e-9,
            cooperativity_alpha=alpha_cc,
            kd_target_ternary_m=kd_ter_cc,
            d_opt_m=m_cc.d_opt,
            ted_max_m=m_cc.ted_max,
            c_hook_50_high_m=m_cc.c_hook_50_high,
            fwhm_log10=m_cc.fwhm_log10,
            hook_shift_fold_vs_protac=m_cc.c_hook_50_high / ref_hook_50,
            is_hook_immune=False,  # Has slight hook only at supramicromolar (>250 uM)
            morrison_plateau_m=morrison_cc,
        )

        # 4. RMC-6236 Glue Model (Kd_target_binary ~ 50 uM, Kd_CypA = 100 nM, alpha = 10000 -> Kd_ter = 5 nM)
        kd_t_rmc_glue = 50e-6
        alpha_rmc_glue = 10000.0
        kd_ter_rmc_glue = 5.0e-9
        tp_rmc_g = ThermodynamicParameters(kd_target=kd_t_rmc_glue, kd_e3=100e-9, alpha=alpha_rmc_glue)
        s_rmc_g = TernaryComplexEquilibrium(tp_rmc_g)
        h_rmc_g = HookEffectAnalyzer(s_rmc_g)
        m_rmc_g = h_rmc_g.analyze_hook_curve(target_tot, cypa_tot, conc_min=1e-12, conc_max=1.0)
        morrison_rmc_g = cls.calculate_morrison_plateau(target_tot, cypa_tot, kd_ter_rmc_glue)

        res_rmc_g = TriComplexHookComparison(
            modality_name="Tri-Complex RAS(ON) Glue (High-Alpha Model)",
            target_name="KRAS:GTP (Pan-RAS)",
            presenter_name="Cyclophilin A (CypA)",
            target_tot_m=target_tot,
            presenter_tot_m=cypa_tot,
            kd_target_binary_m=kd_t_rmc_glue,
            kd_presenter_binary_m=100e-9,
            cooperativity_alpha=alpha_rmc_glue,
            kd_target_ternary_m=kd_ter_rmc_glue,
            d_opt_m=m_rmc_g.d_opt,
            ted_max_m=m_rmc_g.ted_max,
            c_hook_50_high_m=m_rmc_g.c_hook_50_high,
            fwhm_log10=m_rmc_g.fwhm_log10,
            hook_shift_fold_vs_protac=m_rmc_g.c_hook_50_high / ref_hook_50,
            is_hook_immune=False,
            morrison_plateau_m=morrison_rmc_g,
        )

        # 5. RMC-6236 Hypatia Model (alpha = 18.0, Kd_CypA = 100 nM, Kd_ter = 5 nM -> Kd_ras_binary = 90 nM)
        kd_t_rmc_hyp = 90e-9
        alpha_rmc_hyp = 18.0
        kd_ter_rmc_hyp = 5.0e-9
        tp_rmc_h = ThermodynamicParameters(kd_target=kd_t_rmc_hyp, kd_e3=100e-9, alpha=alpha_rmc_hyp)
        s_rmc_h = TernaryComplexEquilibrium(tp_rmc_h)
        h_rmc_h = HookEffectAnalyzer(s_rmc_h)
        m_rmc_h = h_rmc_h.analyze_hook_curve(target_tot, cypa_tot, conc_min=1e-12, conc_max=1e-2)
        morrison_rmc_h = cls.calculate_morrison_plateau(target_tot, cypa_tot, kd_ter_rmc_hyp)

        res_rmc_h = TriComplexHookComparison(
            modality_name="Tri-Complex RAS(ON) (Hypatia Alpha=18 Model)",
            target_name="KRAS:GTP (G12D/Pan-RAS)",
            presenter_name="Cyclophilin A (CypA)",
            target_tot_m=target_tot,
            presenter_tot_m=cypa_tot,
            kd_target_binary_m=kd_t_rmc_hyp,
            kd_presenter_binary_m=100e-9,
            cooperativity_alpha=alpha_rmc_hyp,
            kd_target_ternary_m=kd_ter_rmc_hyp,
            d_opt_m=m_rmc_h.d_opt,
            ted_max_m=m_rmc_h.ted_max,
            c_hook_50_high_m=m_rmc_h.c_hook_50_high,
            fwhm_log10=m_rmc_h.fwhm_log10,
            hook_shift_fold_vs_protac=m_rmc_h.c_hook_50_high / ref_hook_50,
            is_hook_immune=False,
            morrison_plateau_m=morrison_rmc_h,
        )

        return {
            "MZ1": res_mz1,
            "ARV-110": res_arv,
            "CC-90009": res_cc,
            "RMC-6236_glue_model": res_rmc_g,
            "RMC-6236_hypatia_model": res_rmc_h,
        }

    @classmethod
    def test_hook_immunity_limit(
        cls,
        target_tot: float = 100e-9,
        presenter_tot: float = 100e-9,
        kd_presenter: float = 100e-9,
        kd_target_ternary: float = 20e-9,
        kd_target_binary_list: Optional[List[float]] = None,
    ) -> List[Dict[str, float]]:
        """
        Demonstrates the Hook Immunity Theorem by varying binary Kd_target from 100 nM to 10 M,
        showing that as Kd_target -> infinity, [TED] at supramicromolar concentrations approaches
        the Morrison plateau and the Hook effect disappears.
        """
        if kd_target_binary_list is None:
            kd_target_binary_list = [100e-9, 1e-6, 10e-6, 100e-6, 1e-3, 1.0]

        morrison_expected = cls.calculate_morrison_plateau(target_tot, presenter_tot, kd_target_ternary)
        out = []

        for kd_t in kd_target_binary_list:
            alpha = kd_t / kd_target_ternary
            tp = ThermodynamicParameters(kd_target=kd_t, kd_e3=kd_presenter, alpha=alpha)
            solver = TernaryComplexEquilibrium(tp)
            
            # Evaluate at peak and at extreme high dose [D] = 1.0 mM
            res_opt = solver.solve(target_tot, presenter_tot, 200e-9)
            res_1mm = solver.solve(target_tot, presenter_tot, 1e-3)
            
            out.append({
                "kd_target_binary": kd_t,
                "cooperativity_alpha": alpha,
                "ted_at_200nm": res_opt.ternary_ted,
                "ted_at_1mm": res_1mm.ternary_ted,
                "morrison_plateau": morrison_expected,
                "fraction_of_morrison_at_1mm": res_1mm.ternary_ted / morrison_expected,
            })

        return out


# ============================================================================
# 8B. EXACT COOPERATIVITY-AFFINITY THRESHOLD & HOOK IMMUNITY THEOREMS
# ============================================================================

@dataclass
class HookTransitionThresholdResult:
    """Exact closed-form threshold parameters governing the transition to monotonic saturation."""
    c_cutoff_m: float                  # Upper evaluation cutoff concentration [M]
    kd_presenter_m: float              # Presenter binary dissociation constant [M]
    ternary_kd_m: float                # Effective ternary dissociation constant Kd_ter [M]
    target_tot_m: float                # Total target concentration [M]
    presenter_tot_m: float             # Total presenter concentration [M]
    is_naturally_buffered: bool        # True if presenter_tot >= c_cutoff (inherently monotonic)
    kd_target_critical_m: float        # Critical binary Kd_target required for monotonicity [M]
    gamma_critical: float              # Critical affinity asymmetry ratio (Kd_target / Kd_presenter)
    alpha_critical: float              # Critical cooperativity factor (Kd_target / Kd_ter)
    d_opt_at_threshold_m: float        # Verified D_opt_tot at critical threshold [M]


@dataclass
class HookRetentionProfile:
    """Quantitative evaluation of Hook suppression / retention at a specified dose."""
    modality_name: str
    target_name: str
    presenter_name: str
    eval_concentration_m: float
    free_degrader_m: float
    ted_max_m: float
    d_opt_tot_m: float
    ted_at_eval_m: float
    retention_fraction: float         # TED(eval) / TED_max
    suppression_pct: float            # (1 - retention_fraction) * 100
    is_monotonic_at_eval: bool        # True if d_opt_tot >= eval_concentration
    cooperativity_alpha: float
    asymmetry_gamma: float


class HookTransitionThresholdEngine:
    """
    Formalizes the exact mathematical cooperativity-affinity threshold (alpha vs Kd1/Kd2)
    where a ternary degrader/glue transitions from Hook squelching to monotonic saturation.

    Core Theorems Established:
    1. Morrison-Equivalent Closed-Form:
       K_eff(x) = (K1 + x)(K2 + x) / (alpha * x) = (1 / alpha) * (K1 * K2 / x + K1 + K2 + x)
       [TED](x) = 0.5 * (T_tot + E_tot + K_eff(x) - sqrt((T_tot + E_tot + K_eff(x))^2 - 4 * T_tot * E_tot))
    2. Universal Free Optimum:
       x_opt = sqrt(K1 * K2), independent of cooperativity alpha.
    3. Universal Total Optimum:
       D_opt_tot = sqrt(K1 * K2) + (sqrt(K2) * T_tot + sqrt(K1) * E_tot) / (sqrt(K1) + sqrt(K2))
       (independent of [TED]_max and alpha).
    4. Hook Immunity Theorem:
       lim_{K1 -> inf} K_eff(x) = K_ter * (1 + K2 / x) is strictly monotonically decreasing,
       meaning [TED](x) is strictly monotonically increasing on [0, inf) to [TED]_Morrison.
    5. Operational Monotonic Saturation Threshold:
       D_opt_tot >= C_cutoff translates to an exact quadratic in u = sqrt(K1):
       sqrt(K2) * u^2 + (K2 + E_tot - C_cutoff) * u + sqrt(K2) * (T_tot - C_cutoff) = 0
       yielding exact critical thresholds K1*, gamma*, and alpha*.
    6. Chaperone Buffering Theorem:
       High presenter abundance (e.g. CypA = 5-10 uM) directly buffers D_opt_tot upward by 5-10 uM
       and clamps free drug, suppressing binary non-productive competition by 10-20x.
    """

    @staticmethod
    def compute_keff(x: float, kd_target: float, kd_presenter: float, alpha: float) -> float:
        """Calculates effective ternary dissociation constant K_eff(x) = (K1 + x)(K2 + x) / (alpha * x)."""
        if x <= 0.0 or alpha <= 0.0:
            return float("inf")
        return ((kd_target + x) * (kd_presenter + x)) / (alpha * x)

    @staticmethod
    def compute_analytical_free_d_opt(kd_target: float, kd_presenter: float) -> float:
        """Returns x_opt = sqrt(K_D,target * K_D,presenter)."""
        return math.sqrt(kd_target * kd_presenter)

    @classmethod
    def compute_analytical_total_d_opt(
        cls, kd_target: float, kd_presenter: float, target_tot: float, presenter_tot: float
    ) -> float:
        """
        Calculates exact total degrader concentration D_opt_tot maximizing ternary complex:
        D_opt_tot = sqrt(K1 * K2) + (sqrt(K2) * T_tot + sqrt(K1) * E_tot) / (sqrt(K1) + sqrt(K2)).
        """
        sqrt_k1 = math.sqrt(kd_target)
        sqrt_k2 = math.sqrt(kd_presenter)
        denom = sqrt_k1 + sqrt_k2
        w1 = sqrt_k2 / denom
        w2 = sqrt_k1 / denom
        return math.sqrt(kd_target * kd_presenter) + w1 * target_tot + w2 * presenter_tot

    @staticmethod
    def compute_keff_min(kd_target: float, kd_presenter: float, alpha: float) -> float:
        """Returns global minimum effective dissociation constant: K_eff_min = (sqrt(K1) + sqrt(K2))^2 / alpha."""
        if alpha <= 0.0:
            return float("inf")
        return ((math.sqrt(kd_target) + math.sqrt(kd_presenter)) ** 2) / alpha

    @classmethod
    def compute_analytical_ted_max(
        cls, kd_target: float, kd_presenter: float, alpha: float, target_tot: float, presenter_tot: float
    ) -> float:
        """Calculates absolute theoretical maximum ternary complex concentration [TED]_max."""
        keff_min = cls.compute_keff_min(kd_target, kd_presenter, alpha)
        s = target_tot + presenter_tot + keff_min
        disc = max(0.0, s * s - 4.0 * target_tot * presenter_tot)
        return 0.5 * (s - math.sqrt(disc))

    @classmethod
    def compute_ted_from_free_d(
        cls, x: float, kd_target: float, kd_presenter: float, alpha: float, target_tot: float, presenter_tot: float
    ) -> float:
        """Computes [TED] for a given free degrader concentration x via Morrison quadratic."""
        if x <= 0.0:
            return 0.0
        keff = cls.compute_keff(x, kd_target, kd_presenter, alpha)
        s = target_tot + presenter_tot + keff
        disc = max(0.0, s * s - 4.0 * target_tot * presenter_tot)
        return 0.5 * (s - math.sqrt(disc))

    @classmethod
    def compute_total_d_from_free_d(
        cls, x: float, kd_target: float, kd_presenter: float, alpha: float, target_tot: float, presenter_tot: float
    ) -> float:
        """Calculates total degrader D_tot corresponding to a given free degrader concentration x."""
        if x <= 0.0:
            return 0.0
        ted = cls.compute_ted_from_free_d(x, kd_target, kd_presenter, alpha, target_tot, presenter_tot)
        td = (x / (kd_target + x)) * (target_tot - ted)
        ed = (x / (kd_presenter + x)) * (presenter_tot - ted)
        return x + td + ed + ted

    @classmethod
    def solve_exact_ternary(
        cls, d_tot: float, kd_target: float, kd_presenter: float, alpha: float, target_tot: float, presenter_tot: float
    ) -> Tuple[float, float]:
        """
        Solves the exact ternary equilibrium for a given total degrader concentration D_tot.
        Returns (x_free, ted_conc).
        """
        if d_tot <= 0.0 or target_tot <= 0.0 or presenter_tot <= 0.0:
            return 0.0, 0.0

        def residual(x: float) -> float:
            return cls.compute_total_d_from_free_d(x, kd_target, kd_presenter, alpha, target_tot, presenter_tot) - d_tot

        try:
            x_sol = brentq(residual, 1e-18, d_tot, xtol=1e-15, rtol=1e-12)
        except Exception:
            x_sol = d_tot
        ted_sol = cls.compute_ted_from_free_d(x_sol, kd_target, kd_presenter, alpha, target_tot, presenter_tot)
        return float(x_sol), float(ted_sol)

    @classmethod
    def compute_monotonic_saturation_threshold(
        cls,
        kd_presenter: float,
        target_tot: float,
        presenter_tot: float,
        c_cutoff: float = 10.0e-6,
        ternary_kd: float = 5.0e-9,
    ) -> HookTransitionThresholdResult:
        """
        Computes the exact closed-form critical threshold for monotonic saturation up to C_cutoff.
        Solves:
          sqrt(K2) * u^2 + (K2 + E_tot - C_cutoff) * u + sqrt(K2) * (T_tot - C_cutoff) = 0
        where u = sqrt(K1).
        """
        k2 = kd_presenter
        e_tot = presenter_tot
        t_tot = target_tot

        is_buffered = (presenter_tot >= c_cutoff)

        A = math.sqrt(k2)
        B = k2 + e_tot - c_cutoff
        C = math.sqrt(k2) * (t_tot - c_cutoff)

        disc = B * B - 4.0 * A * C
        if disc < 0:
            u_star = max(0.0, -B / (2.0 * A))
        else:
            u_star = (-B + math.sqrt(disc)) / (2.0 * A)
            if u_star < 0:
                u_star = 0.0

        k1_star = u_star ** 2
        gamma_star = k1_star / k2 if k2 > 0 else float("inf")
        alpha_star = k1_star / ternary_kd if ternary_kd > 0 else float("inf")

        d_opt_calc = cls.compute_analytical_total_d_opt(k1_star, k2, t_tot, e_tot) if k1_star > 0 else e_tot

        return HookTransitionThresholdResult(
            c_cutoff_m=c_cutoff,
            kd_presenter_m=k2,
            ternary_kd_m=ternary_kd,
            target_tot_m=t_tot,
            presenter_tot_m=e_tot,
            is_naturally_buffered=is_buffered,
            kd_target_critical_m=k1_star,
            gamma_critical=gamma_star,
            alpha_critical=alpha_star,
            d_opt_at_threshold_m=d_opt_calc,
        )

    @classmethod
    def evaluate_hook_retention_profile(
        cls,
        modality_name: str,
        target_name: str,
        presenter_name: str,
        kd_target: float,
        kd_presenter: float,
        alpha: float,
        target_tot: float,
        presenter_tot: float,
        eval_conc: float = 10.0e-6,
    ) -> HookRetentionProfile:
        """Evaluates detailed Hook retention and suppression at an evaluation concentration."""
        x_free, ted_eval = cls.solve_exact_ternary(eval_conc, kd_target, kd_presenter, alpha, target_tot, presenter_tot)
        ted_max = cls.compute_analytical_ted_max(kd_target, kd_presenter, alpha, target_tot, presenter_tot)
        d_opt_tot = cls.compute_analytical_total_d_opt(kd_target, kd_presenter, target_tot, presenter_tot)

        retention = (ted_eval / ted_max) if ted_max > 0 else 0.0
        retention = min(1.0, max(0.0, retention))
        suppression = (1.0 - retention) * 100.0

        return HookRetentionProfile(
            modality_name=modality_name,
            target_name=target_name,
            presenter_name=presenter_name,
            eval_concentration_m=eval_conc,
            free_degrader_m=x_free,
            ted_max_m=ted_max,
            d_opt_tot_m=d_opt_tot,
            ted_at_eval_m=ted_eval,
            retention_fraction=retention,
            suppression_pct=suppression,
            is_monotonic_at_eval=(d_opt_tot >= eval_conc),
            cooperativity_alpha=alpha,
            asymmetry_gamma=(kd_target / kd_presenter),
        )

    @classmethod
    def evaluate_archetypes_at_cutoff(cls, c_cutoff: float = 10.0e-6) -> Dict[str, HookRetentionProfile]:
        """
        Compares the 4 archetypes at clinical/assay cutoff (default 10 uM):
        1. MZ1 PROTAC (BRD4 + VHL)
        2. ARV-110 PROTAC (AR + CRBN)
        3. CC-90009 Glue (GSPT1 + CRBN)
        4. RMC-6236 Tri-Complex Glue (KRAS:GTP + CypA)
        """
        mz1 = cls.evaluate_hook_retention_profile(
            modality_name="Heterobifunctional PROTAC",
            target_name="BRD4",
            presenter_name="VHL",
            kd_target=50e-9,
            kd_presenter=180e-9,
            alpha=20.0,
            target_tot=100e-9,
            presenter_tot=140e-9,
            eval_conc=c_cutoff,
        )

        arv = cls.evaluate_hook_retention_profile(
            modality_name="Heterobifunctional PROTAC",
            target_name="Androgen Receptor",
            presenter_name="CRBN",
            kd_target=35e-9,
            kd_presenter=150e-9,
            alpha=3.2,
            target_tot=100e-9,
            presenter_tot=65e-9,
            eval_conc=c_cutoff,
        )

        cc = cls.evaluate_hook_retention_profile(
            modality_name="Neomorphic E3 Molecular Glue",
            target_name="GSPT1",
            presenter_name="CRBN",
            kd_target=100e-6,
            kd_presenter=150e-9,
            alpha=1200.0,
            target_tot=100e-9,
            presenter_tot=65e-9,
            eval_conc=c_cutoff,
        )

        rmc = cls.evaluate_hook_retention_profile(
            modality_name="Tri-Complex RAS(ON) Molecular Glue",
            target_name="KRAS:GTP",
            presenter_name="Cyclophilin A",
            kd_target=200e-6,
            kd_presenter=500e-9,
            alpha=40000.0,
            target_tot=1.0e-6,
            presenter_tot=5.0e-6,
            eval_conc=c_cutoff,
        )

        return {
            "MZ1": mz1,
            "ARV-110": arv,
            "CC-90009": cc,
            "RMC-6236": rmc,
        }

    @classmethod
    def evaluate_chaperone_buffering_sweep(
        cls,
        kd_target: float = 200e-6,
        kd_presenter: float = 500e-9,
        alpha: float = 40000.0,
        target_tot: float = 1.0e-6,
        c_cutoff: float = 10.0e-6,
        presenter_concs: Optional[List[float]] = None,
    ) -> List[Dict[str, float]]:
        """
        Sweeps presenter/chaperone concentration (from 50 nM up to 20 uM) and quantifies
        how high chaperone abundance expands D_opt_tot and preserves ternary complex.
        """
        if presenter_concs is None:
            presenter_concs = [50e-9, 100e-9, 200e-9, 500e-9, 1.0e-6, 2.0e-6, 5.0e-6, 10.0e-6, 20.0e-6]

        out = []
        for e_tot in presenter_concs:
            prof = cls.evaluate_hook_retention_profile(
                modality_name="Titrated Chaperone Presenter",
                target_name="Target",
                presenter_name=f"Presenter_{e_tot*1e6:.2f}uM",
                kd_target=kd_target,
                kd_presenter=kd_presenter,
                alpha=alpha,
                target_tot=target_tot,
                presenter_tot=e_tot,
                eval_conc=c_cutoff,
            )
            out.append({
                "presenter_tot_m": e_tot,
                "d_opt_tot_m": prof.d_opt_tot_m,
                "ted_max_m": prof.ted_max_m,
                "ted_at_cutoff_m": prof.ted_at_eval_m,
                "retention_fraction": prof.retention_fraction,
                "suppression_pct": prof.suppression_pct,
                "is_monotonic": prof.is_monotonic_at_eval,
            })
        return out


# ============================================================================
# 9. SPATIAL "UBIQUITINATION ZONE" & LINKER CONFORMATIONAL ENTROPY
# ============================================================================

@dataclass
class LinkerConformationProfile:
    """Biophysical characteristics of the PROTAC linker and ubiquitination zone."""
    name: str = "PEG3"
    num_flexible_bonds: int = 14            # Number of rotatable bonds in linker backbone
    kuhn_length_angstrom: float = 3.8       # Kuhn segment length in solution [Angstrom]
    r_min_zone: float = 15.0                # Minimum steric non-clash distance to E2~Ub active site [Angstrom]
    r_max_zone: float = 35.0                # Maximum catalytic radius of E2~Ub catalytic thioester [Angstrom]
    r_opt: float = 25.0                     # Optimal distance for productive lysine attack [Angstrom]
    sigma_zone: float = 6.0                 # Zone dispersion width [Angstrom]
    reference_bonds: int = 4                # Baseline rigid linker length for entropy reference


class UbiquitinationZoneModel:
    """
    Models the spatial geometry of target lysine engagement by the E2~Ub conjugate
    docked to the E3 ligase, combining polymer end-to-end statistics (Gaussian / Worm-Like Chain)
    with conformational entropy penalties on ternary complex assembly.
    """

    @classmethod
    def end_to_end_probability_density(cls, r: float, n_bonds: int, kuhn_b: float = 3.8) -> float:
        """
        Radial probability density P(r) for Gaussian polymer chain of N bonds and Kuhn length b:
        P(r) = 4 * pi * r^2 * (3 / (2 * pi * N * b^2))^(3/2) * exp(-3 * r^2 / (2 * N * b^2))
        """
        if r <= 0.0 or n_bonds <= 0:
            return 0.0
        nb2 = n_bonds * (kuhn_b ** 2)
        norm = 4.0 * math.pi * (3.0 / (2.0 * math.pi * nb2)) ** 1.5
        return norm * (r ** 2) * math.exp(-3.0 * (r ** 2) / (2.0 * nb2))

    @classmethod
    def conformational_entropy_penalty(
        cls, n_bonds: int, n_ref: int = 4, temperature_k: float = 310.15
    ) -> Tuple[float, float]:
        """
        Calculates conformational entropy loss Delta S_conf and resulting free energy penalty
        Delta G_entropy = -T * Delta S_conf when a flexible linker becomes restricted in the ternary complex.
        Delta S_conf = -1.5 * R * ln(N / N_ref)
        Returns (delta_s_j_mol_k, delta_g_kcal_mol).
        """
        r_gas = 8.31446261815324  # J / (mol * K)
        if n_bonds <= n_ref:
            return 0.0, 0.0
        delta_s = -1.5 * r_gas * math.log(n_bonds / n_ref)
        delta_g_joules = -temperature_k * delta_s
        delta_g_kcal = delta_g_joules / 4184.0
        return delta_s, delta_g_kcal

    @classmethod
    def calculate_productive_fraction(
        cls, profile: LinkerConformationProfile, n_points: int = 1000
    ) -> float:
        """
        Computes the spatial overlap integral:
        f_productive = integral_{r_min}^{r_max} P(r) * exp(-(r - r_opt)^2 / (2 * sigma^2)) dr
        representing the probability that the target lysine enters the productive catalytic zone.
        """
        r_vals = np.linspace(0.01, 80.0, n_points)
        dr = r_vals[1] - r_vals[0]
        nb2 = profile.num_flexible_bonds * (profile.kuhn_length_angstrom ** 2)
        norm = 4.0 * math.pi * (3.0 / (2.0 * math.pi * nb2)) ** 1.5
        p_r = norm * (r_vals ** 2) * np.exp(-3.0 * (r_vals ** 2) / (2.0 * nb2))

        # Catalytic zone kernel
        kernel = np.exp(-((r_vals - profile.r_opt) ** 2) / (2.0 * (profile.sigma_zone ** 2)))
        mask = (r_vals >= profile.r_min_zone) & (r_vals <= profile.r_max_zone)

        f_prod = float(np.sum(p_r[mask] * kernel[mask]) * dr)
        return min(1.0, max(0.0, f_prod))

    @classmethod
    def evaluate_linker_series(
        cls,
        alpha_0: float = 50.0,
        bond_counts: Optional[List[int]] = None,
        kuhn_b: float = 3.8,
    ) -> List[Dict[str, float]]:
        """
        Demonstrates the PROTAC Linker Goldilocks Principle by evaluating productive fraction,
        conformational entropy loss, effective cooperativity, and overall degradation fitness
        across a series of linker lengths.
        """
        if bond_counts is None:
            bond_counts = [4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32]

        results = []
        for nb in bond_counts:
            prof = LinkerConformationProfile(
                name=f"Linker_N{nb}",
                num_flexible_bonds=nb,
                kuhn_length_angstrom=kuhn_b,
            )
            f_prod = cls.calculate_productive_fraction(prof)
            delta_s, delta_g_kcal = cls.conformational_entropy_penalty(nb, prof.reference_bonds)

            alpha_eff = alpha_0 * ((prof.reference_bonds / nb) ** 1.5) if nb >= prof.reference_bonds else alpha_0
            degradation_fitness = f_prod * alpha_eff

            results.append({
                "num_bonds": nb,
                "f_productive": f_prod,
                "delta_s_j_mol_k": delta_s,
                "delta_g_entropy_kcal_mol": delta_g_kcal,
                "alpha_effective": alpha_eff,
                "degradation_fitness_score": degradation_fitness,
            })
        return results


# ============================================================================
# 10. COVALENT / IRREVERSIBLE PROTAC KINETICS ENGINE
# ============================================================================

@dataclass
class CovalentDegraderProfile:
    """Kinetic parameters for covalent / irreversible PROTAC engagement."""
    name: str
    mechanism: str                 # 'target_covalent', 'e3_covalent', or 'reversible'
    k_inact: float = 0.02          # Inactivation rate constant [1 / s]
    k_on_target: float = 1.0e6     # Target association rate [1 / (M * s)]
    kd_target: float = 50.0e-9     # Target reversible affinity [M]
    k_on_e3: float = 1.0e6         # E3 association rate [1 / (M * s)]
    kd_e3: float = 100.0e-9        # E3 reversible affinity [M]
    alpha: float = 10.0            # Cooperativity factor
    k_ub: float = 0.05             # Ubiquitination rate [1 / s]
    k_deg: float = 0.02            # 26S proteasome degradation rate [1 / s]


class CovalentTPDKineticsSimulator:
    """
    Simulates non-equilibrium kinetics of covalent degraders, contrasting:
    1. Target-Covalent PROTACs: Degrader is covalently locked to target; upon proteasomal degradation,
       the degrader is destroyed with the target (TON <= 1.0, stoichiometric, non-catalytic).
    2. E3-Covalent PROTACs: Degrader is covalently locked to E3; upon proteasomal degradation,
       ED_cov complex is recycled intact to recruit and degrade multiple targets (TON > 1.0).
    3. Reversible PROTACs: Both degrader and E3 are catalytically recycled intact.
    """

    def __init__(self, profile: CovalentDegraderProfile):
        self.profile = profile

    def simulate_timecourse(
        self,
        target_tot_0: float = 200.0e-9,
        e3_tot_0: float = 100.0e-9,
        degrader_tot_0: float = 20.0e-9,
        duration_hours: float = 24.0,
        n_points: int = 500,
    ) -> Dict[str, np.ndarray]:
        """Runs stiff ODE integration of covalent reaction networks."""
        t_span = (0.0, duration_hours * 3600.0)
        t_eval = np.linspace(t_span[0], t_span[1], n_points)

        k_on_t = self.profile.k_on_target
        k_off_t = k_on_t * self.profile.kd_target
        k_on_e = self.profile.k_on_e3
        k_off_e = k_on_e * self.profile.kd_e3
        alpha = self.profile.alpha
        k_inact = self.profile.k_inact
        k_ub = self.profile.k_ub
        k_deg = self.profile.k_deg

        if self.profile.mechanism == "target_covalent":
            y0 = np.array([target_tot_0, degrader_tot_0, e3_tot_0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

            def odes(t: float, y: np.ndarray) -> np.ndarray:
                T, D, E, TD_rev, TD_cov, ED, TED_cov, TED_ub, P_deg, D_cons = np.maximum(0.0, y)

                v_td_rev = k_on_t * T * D - k_off_t * TD_rev
                v_cov = k_inact * TD_rev
                v_ed = k_on_e * E * D - k_off_e * ED
                v_ted_e = k_on_e * TD_cov * E - (k_off_e / alpha) * TED_cov
                v_ub = k_ub * TED_cov
                v_deg = k_deg * TED_ub

                dT = -v_td_rev
                dD = -v_td_rev - v_ed
                dE = -v_ed - v_ted_e + v_deg  # E3 is recycled intact!
                dTD_rev = v_td_rev - v_cov
                dTD_cov = v_cov - v_ted_e
                dED = v_ed
                dTED_cov = v_ted_e - v_ub
                dTED_ub = v_ub - v_deg
                dP_deg = v_deg
                dD_cons = v_deg  # Degrader molecule destroyed along with target!

                return np.array([dT, dD, dE, dTD_rev, dTD_cov, dED, dTED_cov, dTED_ub, dP_deg, dD_cons])

        elif self.profile.mechanism == "e3_covalent":
            y0 = np.array([target_tot_0, degrader_tot_0, e3_tot_0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

            def odes(t: float, y: np.ndarray) -> np.ndarray:
                T, D, E, ED_rev, ED_cov, TD, TED_cov, TED_ub, P_deg, D_cons = np.maximum(0.0, y)

                v_ed_rev = k_on_e * E * D - k_off_e * ED_rev
                v_cov = k_inact * ED_rev
                v_td = k_on_t * T * D - k_off_t * TD
                v_ted_t = k_on_t * ED_cov * T - (k_off_t / alpha) * TED_cov
                v_ub = k_ub * TED_cov
                v_deg = k_deg * TED_ub

                dT = -v_td - v_ted_t
                dD = -v_ed_rev - v_td
                dE = -v_ed_rev
                dED_rev = v_ed_rev - v_cov
                dED_cov = v_cov - v_ted_t + v_deg  # ED_cov complex is recycled intact!
                dTD = v_td
                dTED_cov = v_ted_t - v_ub
                dTED_ub = v_ub - v_deg
                dP_deg = v_deg
                dD_cons = 0.0  # Degrader survives on E3

                return np.array([dT, dD, dE, dED_rev, dED_cov, dTD, dTED_cov, dTED_ub, dP_deg, dD_cons])

        else:
            y0 = np.array([target_tot_0, degrader_tot_0, e3_tot_0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

            def odes(t: float, y: np.ndarray) -> np.ndarray:
                T, D, E, TD, ED, TED, dummy, TED_ub, P_deg, D_cons = np.maximum(0.0, y)

                v_td = k_on_t * T * D - k_off_t * TD
                v_ed = k_on_e * E * D - k_off_e * ED
                v_ted_e = k_on_e * TD * E - (k_off_e / alpha) * TED
                v_ted_t = k_on_t * ED * T - (k_off_t / alpha) * TED
                v_ub = k_ub * TED
                v_deg = k_deg * TED_ub

                dT = -v_td - v_ted_t
                dD = -v_td - v_ed + v_deg  # Degrader recycled!
                dE = -v_ed - v_ted_e + v_deg  # E3 recycled!
                dTD = v_td - v_ted_e
                dED = v_ed - v_ted_t
                dTED = v_ted_e + v_ted_t - v_ub
                dTED_ub = v_ub - v_deg
                dP_deg = v_deg
                dD_cons = 0.0

                return np.array([dT, dD, dE, dTD, dED, dTED, 0.0, dTED_ub, dP_deg, dD_cons])

        sol = solve_ivp(odes, t_span, y0, t_eval=t_eval, method="Radau", rtol=1e-7, atol=1e-12)

        return {
            "time_hours": sol.t / 3600.0,
            "target_free": sol.y[0],
            "degrader_free": sol.y[1],
            "e3_free": sol.y[2],
            "peptides_degraded": sol.y[8],
            "degrader_consumed": sol.y[9],
            "target_total": target_tot_0 - sol.y[8],
        }

    def compute_turnover_number(
        self,
        target_tot_0: float = 200.0e-9,
        e3_tot_0: float = 100.0e-9,
        degrader_tot_0: float = 20.0e-9,
        duration_hours: float = 24.0,
    ) -> float:
        """Calculates catalytic turnover number: TON = [Target degraded] / [Degrader initial]."""
        res = self.simulate_timecourse(target_tot_0, e3_tot_0, degrader_tot_0, duration_hours)
        t_deg = float(res["peptides_degraded"][-1])
        return t_deg / degrader_tot_0 if degrader_tot_0 > 0 else 0.0


# ============================================================================
# 11. POLYUBIQUITINATION CASCADE & DUB FUTILE CYCLING ENGINE
# ============================================================================

@dataclass
class CascadeSimulationResult:
    """Time-course and steady-state outputs for the polyubiquitination cascade."""
    time_seconds: np.ndarray
    ub0_ted: np.ndarray
    ub1_ted: np.ndarray
    ub2_ted: np.ndarray
    ub3_ted: np.ndarray
    ub4_ted: np.ndarray
    target_degraded: np.ndarray
    final_degraded_fraction: float
    chain_progression_ratio: float
    theoretical_transfer_efficiency: float


class PolyubiquitinationCascadeEngine:
    """
    Explicitly models the sequential ubiquitin chain assembly (Ub0 -> Ub1 -> Ub2 -> Ub3 -> Ub4)
    and counteracting deubiquitination by cellular DUBs (e.g. USP7, USP15), enforcing that the
    26S proteasome recognizes and degrades only tetra-ubiquitinated species (Ub >= 4).
    """

    def __init__(
        self,
        k_ub: float = 0.05,
        k_dub: float = 0.01,
        k_cat_deg: float = 0.02,
    ):
        self.k_ub = k_ub
        self.k_dub = k_dub
        self.k_cat_deg = k_cat_deg

    @property
    def progression_ratio_rho(self) -> float:
        """Chain progression ratio: rho = k_ub / k_dub."""
        return self.k_ub / self.k_dub if self.k_dub > 0 else float("inf")

    @property
    def analytical_tetra_ub_efficiency(self) -> float:
        """
        Steady-state probability that a ubiquitin chain reaches tetra-ubiquitin (Ub4)
        against competing DUB debranching: P(Ub >= 4) = (rho / (1 + rho))^4.
        """
        rho = self.progression_ratio_rho
        return (rho / (1.0 + rho)) ** 4

    def simulate_cascade(
        self,
        ted_pool_m: float = 10.0e-9,
        duration_seconds: float = 3600.0,
        n_points: int = 500,
    ) -> CascadeSimulationResult:
        """Simulates time course of multi-step polyubiquitination and proteasomal clearance."""
        t_eval = np.linspace(0.0, duration_seconds, n_points)
        y0 = np.array([ted_pool_m, 0.0, 0.0, 0.0, 0.0, 0.0])

        k_ub = self.k_ub
        k_dub = self.k_dub
        k_deg = self.k_cat_deg

        def odes(t: float, y: np.ndarray) -> np.ndarray:
            u0, u1, u2, u3, u4, deg = np.maximum(0.0, y)

            v01 = k_ub * u0 - k_dub * u1
            v12 = k_ub * u1 - k_dub * u2
            v23 = k_ub * u2 - k_dub * u3
            v34 = k_ub * u3 - k_dub * u4
            v_deg = k_deg * u4

            du0 = -v01
            du1 = v01 - v12
            du2 = v12 - v23
            du3 = v23 - v34
            du4 = v34 - v_deg
            ddeg = v_deg

            return np.array([du0, du1, du2, du3, du4, ddeg])

        sol = solve_ivp(odes, (0.0, duration_seconds), y0, t_eval=t_eval, method="Radau", rtol=1e-7, atol=1e-12)

        t_deg_final = float(sol.y[5][-1])
        return CascadeSimulationResult(
            time_seconds=sol.t,
            ub0_ted=sol.y[0],
            ub1_ted=sol.y[1],
            ub2_ted=sol.y[2],
            ub3_ted=sol.y[3],
            ub4_ted=sol.y[4],
            target_degraded=sol.y[5],
            final_degraded_fraction=t_deg_final / ted_pool_m if ted_pool_m > 0 else 0.0,
            chain_progression_ratio=self.progression_ratio_rho,
            theoretical_transfer_efficiency=self.analytical_tetra_ub_efficiency,
        )

    def evaluate_dub_resistance_sweep(
        self,
        ratios: Optional[List[float]] = None,
        k_dub_base: float = 0.05,
        ted_pool_m: float = 10.0e-9,
        duration_seconds: float = 3600.0,
    ) -> List[Dict[str, float]]:
        """
        Sweeps across progression ratios rho = k_ub / k_dub, proving that
        target degradation collapses precipitously once rho < 0.5 (DUB futile cycle).
        """
        if ratios is None:
            ratios = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]

        results = []
        for r in ratios:
            k_ub = k_dub_base * r
            engine = PolyubiquitinationCascadeEngine(k_ub=k_ub, k_dub=k_dub_base, k_cat_deg=self.k_cat_deg)
            res = engine.simulate_cascade(ted_pool_m=ted_pool_m, duration_seconds=duration_seconds)
            results.append({
                "progression_ratio_rho": r,
                "k_ub": k_ub,
                "k_dub": k_dub_base,
                "analytical_efficiency": engine.analytical_tetra_ub_efficiency,
                "numerical_degraded_fraction": res.final_degraded_fraction,
                "target_degraded_nm": float(res.target_degraded[-1]) * 1e9,
            })
        return results


# ============================================================================
# 12. MULTI-TARGET ISOFORM SELECTIVITY VIA DIFFERENTIAL COOPERATIVITY
# ============================================================================

@dataclass
class IsoformTargetProfile:
    """Biophysical profile for a target isoform competing for degrader and ligase."""
    name: str
    total_concentration: float     # Total cellular isoform concentration [M]
    kd_binary: float               # Binary dissociation constant with warhead [M]
    cooperativity_alpha: float     # Ternary cooperativity factor with E3


@dataclass
class IsoformCompetitionResult:
    """Results of competitive multi-target ternary equilibrium."""
    degrader_tot: float
    free_degrader: float
    free_e3: float
    ternary_concentrations: Dict[str, float]
    ternary_fractions: Dict[str, float]
    selectivity_ratios: Dict[str, float]  # Selectivity ratio of each isoform vs reference (first isoform)


class IsoformCooperativityResolver:
    """
    Solves the coupled non-linear multi-target equilibrium when multiple homologous isoforms
    (e.g. BRD4, BRD2, BRD3) compete simultaneously for a limiting pool of E3 ligase and degrader.
    Uses nested 1D Brent root-finding for unconditional, high-precision convergence.
    """

    @classmethod
    def solve_competitive_equilibrium(
        cls,
        targets: List[IsoformTargetProfile],
        e3_tot: float,
        kd_e3: float,
        degrader_tot: float,
    ) -> IsoformCompetitionResult:
        """Solves the simultaneous competitive equilibrium across all target isoforms."""
        if degrader_tot <= 0.0 or e3_tot <= 0.0 or len(targets) == 0:
            return IsoformCompetitionResult(
                degrader_tot=degrader_tot,
                free_degrader=degrader_tot,
                free_e3=e3_tot,
                ternary_concentrations={t.name: 0.0 for t in targets},
                ternary_fractions={t.name: 0.0 for t in targets},
                selectivity_ratios={t.name: 1.0 for t in targets},
            )

        def e_residual(e_free: float, d_free: float) -> float:
            b = 1.0 + d_free / kd_e3
            rhs = e_free * b
            for t in targets:
                ai = 1.0 + d_free / t.kd_binary
                ci = (t.cooperativity_alpha * d_free) / (t.kd_binary * kd_e3)
                rhs += t.total_concentration * (ci * e_free) / (ai + ci * e_free)
            return rhs - e3_tot

        def d_residual(d_free: float) -> float:
            if d_free <= 0.0:
                return -degrader_tot
            e_free = brentq(e_residual, 0.0, e3_tot, args=(d_free,), xtol=1e-16)
            ed = (e_free * d_free) / kd_e3
            d_calc = d_free + ed
            for t in targets:
                ai = 1.0 + d_free / t.kd_binary
                ci = (t.cooperativity_alpha * d_free) / (t.kd_binary * kd_e3)
                ti = t.total_concentration / (ai + ci * e_free)
                tdi = (ti * d_free) / t.kd_binary
                tedi = ci * ti * e_free
                d_calc += tdi + tedi
            return d_calc - degrader_tot

        d_free_sol = brentq(d_residual, 0.0, degrader_tot, xtol=1e-16)
        e_free_sol = brentq(e_residual, 0.0, e3_tot, args=(d_free_sol,), xtol=1e-16)

        ternary_concs = {}
        ternary_fracs = {}
        for t in targets:
            ai = 1.0 + d_free_sol / t.kd_binary
            ci = (t.cooperativity_alpha * d_free_sol) / (t.kd_binary * kd_e3)
            ti = t.total_concentration / (ai + ci * e_free_sol)
            tedi = ci * ti * e_free_sol
            ternary_concs[t.name] = tedi
            ternary_fracs[t.name] = tedi / t.total_concentration if t.total_concentration > 0 else 0.0

        ref_name = targets[0].name
        ref_ted = ternary_concs[ref_name]
        selectivity_ratios = {}
        for t in targets:
            ted_val = ternary_concs[t.name]
            selectivity_ratios[t.name] = (ref_ted / ted_val) if ted_val > 0 else float("inf")

        return IsoformCompetitionResult(
            degrader_tot=degrader_tot,
            free_degrader=d_free_sol,
            free_e3=e_free_sol,
            ternary_concentrations=ternary_concs,
            ternary_fractions=ternary_fracs,
            selectivity_ratios=selectivity_ratios,
        )

    @classmethod
    def evaluate_bet_bromodomain_paradigm(
        cls,
        e3_tot: float = 100.0e-9,
        kd_vhl: float = 100.0e-9,
        degrader_doses: Optional[np.ndarray] = None,
    ) -> List[Dict[str, float]]:
        """
        Simulates the classic MZ1 / BET bromodomain benchmark:
        BRD4 (alpha=20.0), BRD2 (alpha=1.0), and BRD3 (alpha=0.8) with identical binary warhead
        affinity (Kd = 20 nM). Quantifies selectivity amplification across 6 orders of degrader dose.
        """
        if degrader_doses is None:
            degrader_doses = np.logspace(-11, -5, 25)

        targets = [
            IsoformTargetProfile(name="BRD4", total_concentration=100.0e-9, kd_binary=20.0e-9, cooperativity_alpha=20.0),
            IsoformTargetProfile(name="BRD2", total_concentration=100.0e-9, kd_binary=20.0e-9, cooperativity_alpha=1.0),
            IsoformTargetProfile(name="BRD3", total_concentration=100.0e-9, kd_binary=20.0e-9, cooperativity_alpha=0.8),
        ]

        out = []
        for d in degrader_doses:
            res = cls.solve_competitive_equilibrium(targets, e3_tot, kd_vhl, d)
            out.append({
                "degrader_conc_m": d,
                "brd4_ted_nm": res.ternary_concentrations["BRD4"] * 1e9,
                "brd2_ted_nm": res.ternary_concentrations["BRD2"] * 1e9,
                "brd3_ted_nm": res.ternary_concentrations["BRD3"] * 1e9,
                "selectivity_brd4_over_brd2": res.selectivity_ratios["BRD2"],
                "selectivity_brd4_over_brd3": res.selectivity_ratios["BRD3"],
            })
        return out


# ============================================================================
# 13. CLINICAL RESISTANCE PROFILING ENGINE
# ============================================================================

@dataclass
class ResistanceImpactResult:
    """Quantitative impact of resistance mechanisms on TPD efficacy and dosing."""
    mechanism_name: str
    sensitive_dc50_m: float
    resistant_dc50_m: float
    resistance_factor_rf: float    # DC50_resistant / DC50_sensitive (fold shift)
    sensitive_ted_max_m: float
    resistant_ted_max_m: float
    ted_max_retention_pct: float   # (TED_max_resistant / TED_max_sensitive) * 100
    intracellular_drug_retention_pct: float


class TPDResistanceProfiler:
    """
    Quantifies the four primary clinical resistance modalities in targeted protein degradation:
    1. E3 Ligase Genomic Loss / Downregulation (e.g. CRBN loss in multiple myeloma).
    2. E3 Binding Pocket Mutation (e.g. CRBN C391Y or W380A point mutations).
    3. ABCB1 / MDR1 P-glycoprotein Active Drug Efflux (depleting intracellular PROTAC pools).
    4. DUB Overexpression / Futile Cycling (elevating deubiquitination rate).
    """

    @classmethod
    def evaluate_e3_downregulation(
        cls,
        tp: ThermodynamicParameters,
        target_tot: float = 100.0e-9,
        e3_tot_sensitive: float = 65.0e-9,
        fold_loss: float = 10.0,
    ) -> ResistanceImpactResult:
        """Models E3 downregulation (e.g. 10-fold reduction in cellular CRBN)."""
        solver_sens = TernaryComplexEquilibrium(tp)
        analyzer_sens = HookEffectAnalyzer(solver_sens)
        m_sens = analyzer_sens.analyze_hook_curve(target_tot, e3_tot_sensitive)

        e3_tot_res = e3_tot_sensitive / fold_loss
        solver_res = TernaryComplexEquilibrium(tp)
        analyzer_res = HookEffectAnalyzer(solver_res)
        m_res = analyzer_res.analyze_hook_curve(target_tot, e3_tot_res)

        rf = m_res.c_hook_50_low / m_sens.c_hook_50_low if m_sens.c_hook_50_low > 0 else 1.0

        return ResistanceImpactResult(
            mechanism_name=f"E3 Ligase Downregulation ({fold_loss:.1f}x Loss)",
            sensitive_dc50_m=m_sens.c_hook_50_low,
            resistant_dc50_m=m_res.c_hook_50_low,
            resistance_factor_rf=rf,
            sensitive_ted_max_m=m_sens.ted_max,
            resistant_ted_max_m=m_res.ted_max,
            ted_max_retention_pct=(m_res.ted_max / m_sens.ted_max) * 100.0,
            intracellular_drug_retention_pct=100.0,
        )

    @classmethod
    def evaluate_e3_point_mutation(
        cls,
        tp: ThermodynamicParameters,
        target_tot: float = 100.0e-9,
        e3_tot: float = 65.0e-9,
        affinity_loss_fold: float = 50.0,
    ) -> ResistanceImpactResult:
        """Models E3 pocket mutation (e.g. CRBN C391Y causing 50-fold loss of binary E3 affinity)."""
        solver_sens = TernaryComplexEquilibrium(tp)
        analyzer_sens = HookEffectAnalyzer(solver_sens)
        m_sens = analyzer_sens.analyze_hook_curve(target_tot, e3_tot)

        tp_mut = ThermodynamicParameters(
            kd_target=tp.kd_target,
            kd_e3=tp.kd_e3 * affinity_loss_fold,
            alpha=tp.alpha,
        )
        solver_res = TernaryComplexEquilibrium(tp_mut)
        analyzer_res = HookEffectAnalyzer(solver_res)
        m_res = analyzer_res.analyze_hook_curve(target_tot, e3_tot)

        rf = m_res.c_hook_50_low / m_sens.c_hook_50_low if m_sens.c_hook_50_low > 0 else 1.0

        return ResistanceImpactResult(
            mechanism_name=f"E3 Pocket Mutation ({affinity_loss_fold:.1f}x Affinity Loss)",
            sensitive_dc50_m=m_sens.c_hook_50_low,
            resistant_dc50_m=m_res.c_hook_50_low,
            resistance_factor_rf=rf,
            sensitive_ted_max_m=m_sens.ted_max,
            resistant_ted_max_m=m_res.ted_max,
            ted_max_retention_pct=(m_res.ted_max / m_sens.ted_max) * 100.0,
            intracellular_drug_retention_pct=100.0,
        )

    @classmethod
    def evaluate_pgp_efflux_resistance(
        cls,
        tp: ThermodynamicParameters,
        target_tot: float = 100.0e-9,
        e3_tot: float = 65.0e-9,
        is_protac: bool = True,
    ) -> ResistanceImpactResult:
        """
        Models active drug efflux via P-glycoprotein (MDR1 / ABCB1).
        High-MW PROTACs (bRo5) are prime P-gp substrates suffering severe intracellular depletion,
        whereas low-MW molecular glues bypass P-gp efflux due to rapid passive diffusion and low recognition.
        """
        solver = TernaryComplexEquilibrium(tp)
        analyzer = HookEffectAnalyzer(solver)
        m_sens = analyzer.analyze_hook_curve(target_tot, e3_tot)

        if is_protac:
            intracellular_retention = 0.0909  # 1 / (1 + 10.0)
            mech_name = "P-gp / MDR1 Overexpression (PROTAC Scaffold)"
        else:
            intracellular_retention = 0.909   # 1 / (1 + 0.1)
            mech_name = "P-gp / MDR1 Overexpression (Molecular Glue Scaffold)"

        dc50_res = m_sens.c_hook_50_low / intracellular_retention
        rf = 1.0 / intracellular_retention

        return ResistanceImpactResult(
            mechanism_name=mech_name,
            sensitive_dc50_m=m_sens.c_hook_50_low,
            resistant_dc50_m=dc50_res,
            resistance_factor_rf=rf,
            sensitive_ted_max_m=m_sens.ted_max,
            resistant_ted_max_m=m_sens.ted_max,
            ted_max_retention_pct=100.0,
            intracellular_drug_retention_pct=intracellular_retention * 100.0,
        )


# ============================================================================
# 14. IN VIVO PHARMACOKINETIC-PHARMACODYNAMIC (PK/PD) HOOK DISSIPATION ENGINE
# ============================================================================

@dataclass(frozen=True)
class InVivoPKParameters:
    """Pharmacokinetic disposition parameters for oral degrader administration."""
    ka_per_h: float = 1.0            # Oral absorption rate constant [1/h]
    cl_l_per_h: float = 15.0         # Total plasma clearance [L/h]
    vc_l: float = 120.0              # Central distribution volume [L]
    vp_l: float = 250.0              # Peripheral distribution volume [L]
    q_l_per_h: float = 15.0          # Intercompartmental clearance [L/h]
    fu_plasma: float = 0.02          # Plasma unbound fraction (2% free for ARV-110/471)
    kp_uu: float = 1.0               # Unbound cytosolic partition ratio (C_u,cell / C_u,plasma)
    bioavailability_f: float = 0.50  # Oral bioavailability fraction (50%)
    mw_g_per_mol: float = 850.0      # Molecular weight [g/mol]


@dataclass
class InVivoSimulationResult:
    """Time-course simulation of in vivo pharmacokinetics and target degradation."""
    time_hours: np.ndarray
    plasma_conc_total_um: np.ndarray     # Total plasma drug concentration [uM]
    cytosolic_free_conc_nm: np.ndarray   # Unbound cytosolic drug concentration [nM]
    target_protein_nm: np.ndarray        # Total active target protein concentration [nM]
    ternary_complex_nm: np.ndarray       # Active ternary complex [TED] [nM]
    cmax_plasma_um: float
    cmax_free_nm: float
    tmax_plasma_h: float
    min_target_pct: float                # Minimum remaining target as % of baseline
    terminal_target_pct: float           # Target remaining at end of dosing interval %
    mean_target_pct: float               # Time-averaged remaining target % over interval
    target_auc_suppression_pct: float    # 100% - mean_target_pct


@dataclass
class InVivoDoseSweepResult:
    """Summary of target degradation across a clinical dose range."""
    doses_mg: List[float]
    cmax_plasma_um: List[float]
    cmax_free_nm: List[float]
    mean_target_pct: List[float]
    terminal_target_pct: List[float]
    in_vivo_hook_observed: bool
    in_vivo_hook_onset_dose_mg: Optional[float]


class InVivoPKPDHookEngine:
    """
    Couples two-compartment oral pharmacokinetics with intracellular ternary equilibrium
    and target proteolysis dynamics.
    
    Proves the 'In Vivo Hook Dissipation Theorem':
    1. Plasma protein binding dampens free cytosolic concentration (C_u,cell = fu * Cp),
       preventing clinically relevant doses from reaching the high-dose autoinhibition threshold.
    2. Pharmacokinetic clearance dynamically sweeps concentrations downward across the
       optimal ternary window, sustaining catalytic degradation and preventing target rebound.
    """

    def __init__(
        self,
        tp: ThermodynamicParameters,
        pk_params: Optional[InVivoPKParameters] = None,
        k_cat_deg: float = 0.02,
        t_half_target_h: float = 10.0,
    ):
        self.tp = tp
        self.pk = pk_params if pk_params is not None else InVivoPKParameters()
        self.k_cat_deg = k_cat_deg
        self.t_half_target_h = t_half_target_h
        self.k_deg_basal = math.log(2.0) / (t_half_target_h * 3600.0)

    def _solve_quasisteady_ted(self, z_free: float, target_tot: float, e3_tot: float) -> float:
        """Exact closed-form ternary complex concentration given free cytosolic degrader."""
        if z_free <= 1e-18 or target_tot <= 1e-18 or e3_tot <= 1e-18:
            return 0.0
        a = 1.0 + z_free / self.tp.kd_target
        b = 1.0 + z_free / self.tp.kd_e3
        c = (self.tp.alpha * z_free) / (self.tp.kd_target * self.tp.kd_e3)
        A_q = c * b
        B_q = a * b + c * (target_tot - e3_tot)
        C_q = -a * e3_tot
        disc = max(0.0, B_q**2 - 4.0 * A_q * C_q)
        y = (-B_q + math.sqrt(disc)) / (2.0 * A_q)
        x = target_tot / (a + c * y)
        return min(target_tot, max(0.0, c * x * y))

    def simulate_single_dose(
        self,
        dose_mg: float,
        target_tot_0: float = 100.0e-9,
        e3_tot: float = 140.0e-9,
        duration_hours: float = 24.0,
        dt_seconds: float = 30.0,
    ) -> InVivoSimulationResult:
        """
        Simulates 24-hour single-dose oral PK/PD profile with analytical exponential integration.
        """
        dose_mol = (dose_mg * 1e-3 * self.pk.bioavailability_f) / self.pk.mw_g_per_mol
        k_syn = self.k_deg_basal * target_tot_0

        ka = self.pk.ka_per_h / 3600.0
        cl = self.pk.cl_l_per_h / 3600.0
        q = self.pk.q_l_per_h / 3600.0
        vc = self.pk.vc_l
        vp = self.pk.vp_l
        fu = self.pk.fu_plasma
        kp_uu = self.pk.kp_uu

        n_steps = int((duration_hours * 3600.0) / dt_seconds) + 1
        time_pts = np.linspace(0.0, duration_hours, n_steps)

        a_gut = dose_mol
        a_c = 0.0
        a_p = 0.0
        target_cur = target_tot_0

        cp_list = []
        cu_list = []
        target_list = []
        ted_list = []

        for _ in range(n_steps):
            cp = a_c / vc
            cu = fu * kp_uu * cp
            ted = self._solve_quasisteady_ted(cu, target_cur, e3_tot)
            f_ted = ted / target_cur if target_cur > 1e-18 else 0.0

            cp_list.append(cp * 1e6)        # uM
            cu_list.append(cu * 1e9)        # nM
            target_list.append(target_cur * 1e9)  # nM
            ted_list.append(ted * 1e9)            # nM

            # Update target via exact exponential integration
            k_eff = self.k_deg_basal + self.k_cat_deg * f_ted
            t_ss = k_syn / k_eff
            target_cur = t_ss + (target_cur - t_ss) * math.exp(-k_eff * dt_seconds)

            # Update PK state
            d_gut = ka * a_gut
            a_gut = max(0.0, a_gut - d_gut * dt_seconds)
            d_ac = (d_gut - (cl / vc) * a_c - (q / vc) * a_c + (q / vp) * a_p) * dt_seconds
            d_ap = ((q / vc) * a_c - (q / vp) * a_p) * dt_seconds
            a_c = max(0.0, a_c + d_ac)
            a_p = max(0.0, a_p + d_ap)

        cp_arr = np.array(cp_list)
        cu_arr = np.array(cu_list)
        t_arr = np.array(target_list)
        ted_arr = np.array(ted_list)

        cmax_plasma = float(np.max(cp_arr))
        cmax_free = float(np.max(cu_arr))
        tmax_plasma_h = float(time_pts[np.argmax(cp_arr)])

        target_base_nm = target_tot_0 * 1e9
        min_target_pct = float((np.min(t_arr) / target_base_nm) * 100.0)
        terminal_target_pct = float((t_arr[-1] / target_base_nm) * 100.0)
        mean_target_pct = float((np.mean(t_arr) / target_base_nm) * 100.0)
        auc_suppression = 100.0 - mean_target_pct

        return InVivoSimulationResult(
            time_hours=time_pts,
            plasma_conc_total_um=cp_arr,
            cytosolic_free_conc_nm=cu_arr,
            target_protein_nm=t_arr,
            ternary_complex_nm=ted_arr,
            cmax_plasma_um=cmax_plasma,
            cmax_free_nm=cmax_free,
            tmax_plasma_h=tmax_plasma_h,
            min_target_pct=min_target_pct,
            terminal_target_pct=terminal_target_pct,
            mean_target_pct=mean_target_pct,
            target_auc_suppression_pct=auc_suppression,
        )

    def evaluate_dose_sweep(
        self,
        doses_mg: Optional[List[float]] = None,
        target_tot_0: float = 100.0e-9,
        e3_tot: float = 140.0e-9,
    ) -> InVivoDoseSweepResult:
        """
        Sweeps doses from sub-therapeutic to massive supratherapeutic levels (e.g. 10 to 100,000 mg).
        Identifies if an in vivo Hook rebound occurs.
        """
        if doses_mg is None:
            doses_mg = [10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0, 100000.0]

        cmax_plasma_list = []
        cmax_free_list = []
        mean_target_list = []
        terminal_target_list = []

        for d in doses_mg:
            res = self.simulate_single_dose(d, target_tot_0=target_tot_0, e3_tot=e3_tot)
            cmax_plasma_list.append(res.cmax_plasma_um)
            cmax_free_list.append(res.cmax_free_nm)
            mean_target_list.append(res.mean_target_pct)
            terminal_target_list.append(res.terminal_target_pct)

        # Detect hook rebound in mean remaining target (elevation by > 5% from minimum)
        min_mean_target = min(mean_target_list)
        min_idx = mean_target_list.index(min_mean_target)
        hook_observed = False
        hook_dose = None

        for idx in range(min_idx + 1, len(mean_target_list)):
            if mean_target_list[idx] > min_mean_target + 5.0:
                hook_observed = True
                hook_dose = doses_mg[idx]
                break

        return InVivoDoseSweepResult(
            doses_mg=doses_mg,
            cmax_plasma_um=cmax_plasma_list,
            cmax_free_nm=cmax_free_list,
            mean_target_pct=mean_target_list,
            terminal_target_pct=terminal_target_list,
            in_vivo_hook_observed=hook_observed,
            in_vivo_hook_onset_dose_mg=hook_dose,
        )


# ============================================================================
# 15. NON-PROTEASOMAL DEGRADATION: LYTACS & ENDOSOMAL TRAFFICKING ENGINE
# ============================================================================

@dataclass(frozen=True)
class LYTACBiophysicalParameters:
    """Biophysical and trafficking parameters for Lysosome-Targeting Chimeras."""
    kd_receptor_surface: float = 20.0e-9      # Surface shuttling receptor affinity (pH 7.4) [M]
    kd_receptor_acidic: float = 5.0e-6        # Endosomal shuttling receptor affinity (pH 5.2) [M]
    kd_target: float = 50.0e-9                # Target warhead affinity [M]
    alpha_surface: float = 5.0                # Surface ternary cooperativity factor
    k_on: float = 1.0e5                       # Association rate constant [1/(M*s)]
    k_int: float = 0.005                      # Clathrin endocytosis rate [1/s] (t_1/2 ~ 2.3 min)
    k_acid: float = 0.01                      # Acidification-induced cargo dissociation rate [1/s]
    k_rec: float = 0.03                       # Receptor recycling back to cell membrane [1/s]
    k_lys: float = 0.01                       # Lysosomal proteolytic degradation rate [1/s]
    k_syn_surf: float = 1.0e-12               # Surface target homeostatic baseline synthesis [M/s]
    k_deg_basal: float = 1.0e-5               # Basal receptor-mediated/shedding turnover [1/s]
    k_ex: float = 0.01                        # Free LYTAC ligand extracellular efflux/recycling [1/s]


@dataclass
class LYTACSimulationResult:
    """Time-course simulation of LYTAC receptor-mediated endocytosis and lysosomal clearance."""
    time_hours: np.ndarray
    target_surface_nm: np.ndarray
    receptor_surface_nm: np.ndarray
    peptides_degraded_nm: np.ndarray
    extracellular_lytac_nm: np.ndarray
    catalytic_turnover_number: float
    target_knockdown_pct: float
    receptor_conservation_pct: float


class LYTACTraffickingEngine:
    """
    Models the multi-compartment receptor-mediated endocytosis, endosomal acidification,
    and lysosomal degradation of extracellular/membrane target proteins by LYTACs.
    
    Captures:
    1. Neutral pH 7.4 high-affinity ternary complex assembly on plasma membrane
    2. Rapid endocytic internalization via CI-M6PR or ASGPR
    3. Acidic pH 5.2 conformational uncoupling and cargo release
    4. Receptor recycling back to plasma membrane (conserved shuttling vehicle)
    5. Proteolytic cleavage in lysosomes by cathepsins
    """

    def __init__(self, params: Optional[LYTACBiophysicalParameters] = None):
        self.params = params if params is not None else LYTACBiophysicalParameters()

    def simulate(
        self,
        target_surf_0: float = 100.0e-9,
        receptor_surf_0: float = 50.0e-9,
        lytac_ext_0: float = 5.0e-9,
        duration_hours: float = 24.0,
    ) -> LYTACSimulationResult:
        p = self.params
        k_off_r = p.k_on * p.kd_receptor_surface
        k_off_t = p.k_on * p.kd_target

        # State vector:
        # [0] T_s, [1] R_s, [2] TL_s, [3] RL_s, [4] TRL_s,
        # [5] TRL_e, [6] T_e, [7] R_e, [8] L_e, [9] P_deg, [10] L_ext
        def rhs(t, y):
            T_s, R_s, TL_s, RL_s, TRL_s, TRL_e, T_e, R_e, L_e, P_deg, L_ext = [max(0.0, v) for v in y]

            # Surface binding fluxes
            v_tl = p.k_on * T_s * L_ext - k_off_t * TL_s
            v_rl = p.k_on * R_s * L_ext - k_off_r * RL_s
            v_trl_r = (p.k_on * p.alpha_surface) * TL_s * R_s - k_off_r * TRL_s
            v_trl_t = (p.k_on * p.alpha_surface) * RL_s * T_s - k_off_t * TRL_s

            # Internalization
            v_int_trl = p.k_int * TRL_s
            v_int_rl = p.k_int * RL_s

            # Endosomal uncoupling
            v_acid = p.k_acid * TRL_e

            # Receptor recycling and lysosomal degradation
            v_rec = p.k_rec * R_e
            v_lys = p.k_lys * T_e
            v_ex = p.k_ex * L_e

            # Target synthesis & basal turnover
            v_syn = p.k_syn_surf
            v_deg_b = p.k_deg_basal * T_s

            dT_s = v_syn - v_deg_b - v_tl - v_trl_t
            dR_s = v_rec - v_rl - v_trl_r
            dTL_s = v_tl - v_trl_r
            dRL_s = v_rl - v_trl_t - v_int_rl
            dTRL_s = v_trl_r + v_trl_t - v_int_trl

            dTRL_e = v_int_trl - v_acid
            dT_e = v_acid - v_lys
            dR_e = v_acid + v_int_rl - v_rec
            dL_e = v_acid + v_int_rl - v_ex
            dP_deg = v_lys
            dL_ext = -v_tl - v_rl + v_ex

            return [dT_s, dR_s, dTL_s, dRL_s, dTRL_s, dTRL_e, dT_e, dR_e, dL_e, dP_deg, dL_ext]

        y0 = [target_surf_0, receptor_surf_0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, lytac_ext_0]
        t_eval = np.linspace(0.0, duration_hours * 3600.0, 50)

        sol = solve_ivp(rhs, [0, duration_hours * 3600.0], y0, method='Radau', atol=1e-13, rtol=1e-8, t_eval=t_eval)

        t_hours = sol.t / 3600.0
        ts_nm = np.clip(sol.y[0] * 1e9, 0.0, None)
        rs_nm = np.clip(sol.y[1] * 1e9, 0.0, None)
        pdeg_nm = np.clip(sol.y[9] * 1e9, 0.0, None)
        lext_nm = np.clip(sol.y[10] * 1e9, 0.0, None)

        total_pdeg_m = max(0.0, float(sol.y[9][-1]))
        ton = total_pdeg_m / lytac_ext_0 if lytac_ext_0 > 0 else 0.0

        target_kd_pct = float(max(0.0, 100.0 * (1.0 - sol.y[0][-1] / target_surf_0)))
        total_r_final = sol.y[1][-1] + sol.y[3][-1] + sol.y[4][-1] + sol.y[5][-1] + sol.y[7][-1]
        rec_conservation = float((total_r_final / receptor_surf_0) * 100.0)

        return LYTACSimulationResult(
            time_hours=t_hours,
            target_surface_nm=ts_nm,
            receptor_surface_nm=rs_nm,
            peptides_degraded_nm=pdeg_nm,
            extracellular_lytac_nm=lext_nm,
            catalytic_turnover_number=float(ton),
            target_knockdown_pct=target_kd_pct,
            receptor_conservation_pct=rec_conservation,
        )


# ============================================================================
# 16. TARGET RESYNTHESIS HALF-LIFE SCALING & TURNOVER SPECTRUM ENGINE
# ============================================================================

@dataclass(frozen=True)
class TargetTurnoverProfile:
    """Quantitative turnover characteristics of an intracellular target."""
    name: str
    t_half_hours: float
    description: str


@dataclass
class ResynthesisScalingResult:
    """Degradation potency and occupancy requirements as a function of target half-life."""
    target_name: str
    t_half_hours: float
    k_deg_basal_s: float
    required_ternary_fraction_dc50_pct: float
    required_ternary_fraction_90pct_deg: float
    achievable_dmax_pct: float
    is_catalytically_achievable_90pct: bool


class TargetResynthesisSpectrumEngine:
    """
    Formulates the exact steady-state analytical relationship between target half-life (t_1/2),
    synthesis rate (k_syn), basal proteasomal turnover (k_deg_basal), and degradation potency (DC50, Dmax).
    
    Proves the 'Resynthesis Barrier Law':
    Targets with rapid turnover (e.g. c-Myc, t_1/2 ~ 20 min) require orders-of-magnitude higher
    catalytic clearance velocities than stable targets (e.g. Tau, KRAS) to achieve equivalent Dmax.
    """

    REFERENCE_TARGETS = [
        TargetTurnoverProfile("c-Myc", 0.33, "Oncogenic transcription factor with ultra-rapid turnover"),
        TargetTurnoverProfile("MDM2", 0.50, "p53-regulating E3 ligase and proto-oncogene"),
        TargetTurnoverProfile("ERalpha", 4.00, "Nuclear hormone receptor (Breast Cancer)"),
        TargetTurnoverProfile("BRD4", 10.00, "Bromodomain epigenetic reader"),
        TargetTurnoverProfile("AR", 16.00, "Androgen receptor (Prostate Cancer)"),
        TargetTurnoverProfile("KRAS", 24.00, "Small GTPase with slow basal turnover"),
        TargetTurnoverProfile("Tau", 48.00, "Neurodegenerative microtubule-associated protein"),
    ]

    @staticmethod
    def compute_required_ternary_fraction(
        t_half_hours: float,
        target_degradation_fraction: float = 0.50,
        k_cat_deg: float = 0.02,
    ) -> float:
        """
        Computes the fraction of target that must be engaged in active ternary complex
        to achieve a specified degradation fraction (e.g. 0.50 for DC50, 0.90 for 90% knockdown).
        
        Formula: f_TED_req = (D_frac / (1 - D_frac)) * (k_deg_basal / k_cat_deg)
        """
        if target_degradation_fraction >= 1.0 or target_degradation_fraction <= 0.0:
            raise ValueError("target_degradation_fraction must be in (0, 1)")
        t_half_s = t_half_hours * 3600.0
        k_deg_basal = math.log(2.0) / t_half_s
        odds = target_degradation_fraction / (1.0 - target_degradation_fraction)
        return odds * (k_deg_basal / k_cat_deg)

    @staticmethod
    def compute_achievable_dmax(
        t_half_hours: float,
        k_cat_deg: float = 0.02,
        max_ternary_fraction: float = 0.80,
    ) -> float:
        """
        Computes the theoretical ceiling of target degradation depth (Dmax)
        given a maximal attainable ternary complex recruitment fraction.
        
        Formula: Dmax = (k_cat * f_max) / (k_deg_basal + k_cat * f_max)
        """
        t_half_s = t_half_hours * 3600.0
        k_deg_basal = math.log(2.0) / t_half_s
        v_cat = k_cat_deg * max_ternary_fraction
        return (v_cat / (k_deg_basal + v_cat)) * 100.0

    @classmethod
    def evaluate_target_spectrum(
        cls,
        k_cat_deg: float = 0.02,
        max_ternary_fraction: float = 0.80,
    ) -> List[ResynthesisScalingResult]:
        """
        Evaluates the clinical target spectrum under realistic catalytic ubiquitination rates.
        """
        results = []
        for target in cls.REFERENCE_TARGETS:
            t_s = target.t_half_hours * 3600.0
            k_basal = math.log(2.0) / t_s
            f_dc50 = cls.compute_required_ternary_fraction(target.t_half_hours, 0.50, k_cat_deg)
            f_90 = cls.compute_required_ternary_fraction(target.t_half_hours, 0.90, k_cat_deg)
            dmax = cls.compute_achievable_dmax(target.t_half_hours, k_cat_deg, max_ternary_fraction)

            results.append(ResynthesisScalingResult(
                target_name=target.name,
                t_half_hours=target.t_half_hours,
                k_deg_basal_s=k_basal,
                required_ternary_fraction_dc50_pct=f_dc50 * 100.0,
                required_ternary_fraction_90pct_deg=f_90 * 100.0,
                achievable_dmax_pct=dmax,
                is_catalytically_achievable_90pct=(f_90 <= max_ternary_fraction),
            ))
        return results


# ============================================================================
# 18. TISSUE-SELECTIVE E3 LIGASE HIJACKING & PLATELET-SPARING ENGINE
# ============================================================================

@dataclass
class TissueCellProfile:
    """Cellular and tissue expression profile for assessing degradation therapeutic index."""
    name: str                           # e.g., 'Tumor_Lineage', 'Human_Platelet'
    e3_type: str                        # 'VHL', 'CRBN', 'MDM2', 'cIAP', etc.
    e3_abundance_nm: float              # Cellular abundance of E3 ligase [nM]
    target_abundance_nm: float          # Baseline cellular target protein level [nM]
    target_half_life_hours: float       # Basal turnover half-life [hours]
    critical_survival_threshold_pct: float = 30.0  # Minimal target fraction required for cell survival [%]
    is_anucleate: bool = False          # True for platelets/erythrocytes (no de novo transcription)
    crl_machinery_competence: float = 1.0 # Ubiquitination machinery competence factor (0 to 1)

@dataclass
class TissueDegradationResult:
    """Quantitative outcome of tissue-selective degradation evaluation."""
    compound_name: str
    e3_recruited: str
    dose_nm: float
    tumor_target_level_pct: float
    normal_tissue_target_level_pct: float
    tumor_dc50_nm: float
    normal_tissue_dc50_nm: float
    therapeutic_safety_index: float     # Ratio DC50_normal / DC50_tumor
    is_tumor_ablated: bool              # True if tumor target <= 20%
    is_normal_tissue_spared: bool       # True if normal tissue target >= critical_threshold
    platelet_sparing_margin_fold: float # Safety fold margin relative to platelet toxicity

class TissueSelectiveE3Engine:
    """
    Biophysical engine evaluating tissue-restricted E3 ligase expression to eliminate
    dose-limiting toxicities in healthy host organs.
    Exemplified by the BCL-xL DT2216 (VHL) vs PZ15227 (CRBN) thrombocytopenia paradigm.
    """

    @classmethod
    def simulate_tissue_depletion(
        cls,
        cell_profile: TissueCellProfile,
        thermo_params: ThermodynamicParameters,
        degrader_tot_nm: float,
        duration_hours: float = 24.0,
        k_ub_base: float = 0.05,
        k_cat_deg: float = 0.01,
    ) -> float:
        """
        Simulates target protein depletion [% of baseline] in a specific tissue/cell profile.
        Incorporates anucleate status (no de novo synthesis in platelets) and CRL machinery competence.
        """
        t_half_s = cell_profile.target_half_life_hours * 3600.0
        k_deg_basal = math.log(2.0) / t_half_s
        target_tot_0 = cell_profile.target_abundance_nm * 1e-9
        e3_tot_0 = max(1e-15, cell_profile.e3_abundance_nm * 1e-9)
        degrader_tot = degrader_tot_nm * 1e-9

        # Resynthesis rate: normal nucleated cells have steady-state k_syn = k_deg_basal * T0.
        # Anucleate platelets have essentially no de novo transcription (residual translational leakage <= 2%).
        if cell_profile.is_anucleate:
            k_syn = k_deg_basal * target_tot_0 * 0.02
        else:
            k_syn = k_deg_basal * target_tot_0

        k_ub = k_ub_base * cell_profile.crl_machinery_competence

        kp = DegradationKineticsParameters(
            k_deg_basal=k_deg_basal,
            k_syn=k_syn,
            k_ub=k_ub,
            k_cat_deg=k_cat_deg,
        )

        sim = TPDKineticsSimulator(thermo_params, kp)
        res = sim.simulate_time_course(
            target_tot_0=target_tot_0,
            e3_tot_0=e3_tot_0,
            degrader_tot=degrader_tot,
            duration_hours=duration_hours,
            num_time_points=100,
        )
        return float(res['target_fraction'][-1] * 100.0)

    @classmethod
    def compute_tissue_dc50(
        cls,
        cell_profile: TissueCellProfile,
        thermo_params: ThermodynamicParameters,
        duration_hours: float = 24.0,
        k_ub_base: float = 0.05,
        k_cat_deg: float = 0.01,
    ) -> float:
        """
        Computes the DC50 [nM] for a specific tissue/cell type over the simulation duration.
        Returns a ceiling of 1e6 nM (1 mM) if 50% degradation cannot be achieved.
        """
        max_degradation = 100.0 - cls.simulate_tissue_depletion(
            cell_profile, thermo_params, degrader_tot_nm=1e4, duration_hours=duration_hours,
            k_ub_base=k_ub_base, k_cat_deg=k_cat_deg
        )
        if max_degradation < 50.0:
            return 1.0e6

        def obj(log_d: float) -> float:
            d_nm = math.exp(log_d)
            pct_rem = cls.simulate_tissue_depletion(
                cell_profile, thermo_params, degrader_tot_nm=d_nm, duration_hours=duration_hours,
                k_ub_base=k_ub_base, k_cat_deg=k_cat_deg
            )
            return pct_rem - 50.0

        try:
            log_sol = brentq(obj, math.log(0.01), math.log(1e4), xtol=1e-3)
            return float(math.exp(log_sol))
        except Exception:
            return 1.0e6

    @classmethod
    def evaluate_bcl_xl_paradigm(
        cls,
        doses_nm: Optional[List[float]] = None,
    ) -> Dict[str, Dict[str, Union[float, List[TissueDegradationResult]]]]:
        """
        Comprehensive benchmark of the clinical BCL-xL platelet-sparing paradigm:
        1. DT2216 (VHL-recruiting PROTAC): High VHL in tumors, negligible/un-neddylated VHL in platelets.
        2. PZ15227 (CRBN-recruiting PROTAC): Abundant CRBN in both tumors and platelets.
        """
        if doses_nm is None:
            doses_nm = [1.0, 10.0, 50.0, 100.0, 500.0, 1000.0]

        tumor_profile = TissueCellProfile(
            name="BCL-xL Dependent Tumor (MOLT-4 / T-ALL)",
            e3_type="VHL",
            e3_abundance_nm=250.0,
            target_abundance_nm=100.0,
            target_half_life_hours=24.0,
            critical_survival_threshold_pct=20.0,
            is_anucleate=False,
            crl_machinery_competence=1.0,
        )

        platelet_vhl_profile = TissueCellProfile(
            name="Human Platelet (VHL)",
            e3_type="VHL",
            e3_abundance_nm=0.05,       # Virtually undetectable VHL protein in platelets
            target_abundance_nm=100.0,
            target_half_life_hours=72.0,
            critical_survival_threshold_pct=30.0,
            is_anucleate=True,
            crl_machinery_competence=0.01, # Un-neddylated Cul2 in platelets
        )

        platelet_crbn_profile = TissueCellProfile(
            name="Human Platelet (CRBN)",
            e3_type="CRBN",
            e3_abundance_nm=200.0,      # Abundantly expressed in megakaryocytes & platelets
            target_abundance_nm=100.0,
            target_half_life_hours=72.0,
            critical_survival_threshold_pct=30.0,
            is_anucleate=True,
            crl_machinery_competence=1.0, # Active Cul4A-DDB1 machinery
        )

        tp_dt2216 = ThermodynamicParameters(kd_target=50e-9, kd_e3=100e-9, alpha=8.0)
        tp_pz15227 = ThermodynamicParameters(kd_target=40e-9, kd_e3=200e-9, alpha=6.0)

        # Compute DC50s
        dc50_dt2216_tumor = cls.compute_tissue_dc50(tumor_profile, tp_dt2216)
        dc50_dt2216_platelet = cls.compute_tissue_dc50(platelet_vhl_profile, tp_dt2216)
        tsi_dt2216 = dc50_dt2216_platelet / dc50_dt2216_tumor

        dc50_pz15227_tumor = cls.compute_tissue_dc50(tumor_profile, tp_pz15227)
        dc50_pz15227_platelet = cls.compute_tissue_dc50(platelet_crbn_profile, tp_pz15227)
        tsi_pz15227 = dc50_pz15227_platelet / dc50_pz15227_tumor

        dt2216_results = []
        for d in doses_nm:
            t_tum = cls.simulate_tissue_depletion(tumor_profile, tp_dt2216, d)
            t_plat = cls.simulate_tissue_depletion(platelet_vhl_profile, tp_dt2216, d)
            dt2216_results.append(TissueDegradationResult(
                compound_name="DT2216",
                e3_recruited="VHL",
                dose_nm=d,
                tumor_target_level_pct=t_tum,
                normal_tissue_target_level_pct=t_plat,
                tumor_dc50_nm=dc50_dt2216_tumor,
                normal_tissue_dc50_nm=dc50_dt2216_platelet,
                therapeutic_safety_index=tsi_dt2216,
                is_tumor_ablated=(t_tum <= 20.0),
                is_normal_tissue_spared=(t_plat >= platelet_vhl_profile.critical_survival_threshold_pct),
                platelet_sparing_margin_fold=tsi_dt2216,
            ))

        pz15227_results = []
        for d in doses_nm:
            t_tum = cls.simulate_tissue_depletion(tumor_profile, tp_pz15227, d)
            t_plat = cls.simulate_tissue_depletion(platelet_crbn_profile, tp_pz15227, d)
            pz15227_results.append(TissueDegradationResult(
                compound_name="PZ15227",
                e3_recruited="CRBN",
                dose_nm=d,
                tumor_target_level_pct=t_tum,
                normal_tissue_target_level_pct=t_plat,
                tumor_dc50_nm=dc50_pz15227_tumor,
                normal_tissue_dc50_nm=dc50_pz15227_platelet,
                therapeutic_safety_index=tsi_pz15227,
                is_tumor_ablated=(t_tum <= 20.0),
                is_normal_tissue_spared=(t_plat >= platelet_crbn_profile.critical_survival_threshold_pct),
                platelet_sparing_margin_fold=tsi_pz15227,
            ))

        return {
            "DT2216": {
                "tumor_dc50_nm": dc50_dt2216_tumor,
                "platelet_dc50_nm": dc50_dt2216_platelet,
                "therapeutic_safety_index": tsi_dt2216,
                "dose_responses": dt2216_results,
            },
            "PZ15227": {
                "tumor_dc50_nm": dc50_pz15227_tumor,
                "platelet_dc50_nm": dc50_pz15227_platelet,
                "therapeutic_safety_index": tsi_pz15227,
                "dose_responses": pz15227_results,
            }
        }


# ============================================================================
# 19. AUTOPHAGY-TARGETING CHIMERAS (ATTECs & AUTACs): 2D MEMBRANE INDUCED PROXIMITY
# ============================================================================

@dataclass
class AutophagyBiophysicalParameters:
    """Biophysical and kinetic parameters governing macroautophagic aggregate degradation."""
    kd_aggregate_nm: float = 50.0          # ATTEC affinity for target aggregate (e.g. mHTT, Tau fibril) [nM]
    kd_lc3_nm: float = 200.0               # ATTEC affinity for LC3B / autophagosome marker [nM]
    alpha_cooperativity: float = 5.0       # Ternary tethering cooperativity
    phagophore_lc3_density_per_um2: float = 1200.0 # LC3-II membrane density [molecules / um^2]
    reaction_shell_thickness_nm: float = 10.0      # Sub-membrane reaction boundary layer [nm]
    k_engulf_s: float = 0.005              # Rate constant for phagophore engulfment [s^-1]
    k_lysosomal_clearance_s: float = 0.01  # Rate constant for lysosomal hydrolase destruction [s^-1]
    k_syn_aggregate_nm_hr: float = 1.0     # Baseline aggregate production rate [nM / hr]
    aggregate_particle_diameter_nm: float = 25.0   # Diameter of misfolded aggregate (polyQ / oligomer) [nm]
    proteasome_pore_diameter_nm: float = 1.3       # 20S proteasome entrance barrel diameter [nm] (13 Å)

@dataclass
class AutophagySimulationResult:
    """Quantitative outcome of ATTEC autophagic aggregate clearance simulation."""
    baseline_aggregate_nm: float
    residual_aggregate_nm: float
    aggregate_knockdown_pct: float
    catalytic_turnover_number: float       # Aggregates cleared per ATTEC molecule (TON)
    effective_2d_lc3_concentration_um: float # Local concentration at phagophore membrane [uM]
    membrane_enhancement_factor: float     # Ratio C_2D,eff / C_3D,bulk
    proteasome_clearance_pct: float        # Clearance by proteasome alone (0% due to steric block)
    autophagic_clearance_pct: float        # Clearance by ATTEC-induced macroautophagy
    is_catalytic: bool                     # True if TON > 1.0

class AutophagyTargetingEngine:
    """
    Biophysical simulation engine for Autophagosome-Tethering Compounds (ATTECs)
    and Autophagy-Targeting Chimeras (AUTACs).
    Models 2D membrane-surface induced proximity, steric proteasome exclusion,
    and autophagosomal engulfment / lysosomal destruction kinetics.
    """

    AVOGADRO: float = 6.02214076e23

    @classmethod
    def compute_2d_effective_concentration(
        cls,
        lc3_density_per_um2: float = 1200.0,
        shell_thickness_nm: float = 10.0,
        bulk_cytosolic_lc3_nm: float = 500.0,
    ) -> Tuple[float, float]:
        """
        Computes the effective local concentration C_eff,2D [uM] of LC3-II on phagophore membranes:
          C_eff = sigma / (N_A * h)
        where sigma is surface density [m^-2] and h is shell thickness [m].
        Returns (C_eff_uM, fold_enhancement_over_bulk).
        """
        sigma_m2 = lc3_density_per_um2 * 1.0e12  # convert um^-2 to m^-2
        h_m = shell_thickness_nm * 1.0e-9        # convert nm to m
        # Molarity: mol / m^3 * 1e-3 m^3/L = mol / L
        c_molar = (sigma_m2 / (cls.AVOGADRO * h_m)) * 1.0e-3
        c_um = c_molar * 1.0e6
        bulk_um = bulk_cytosolic_lc3_nm * 1.0e-3
        enhancement_factor = c_um / bulk_um
        return float(c_um), float(enhancement_factor)

    @classmethod
    def compute_proteasome_pore_transmission(
        cls,
        particle_diameter_nm: float = 25.0,
        pore_diameter_nm: float = 1.3,
    ) -> float:
        """
        Computes steric partition coefficient K_part of a globular particle into a cylindrical pore:
          K_part = (1 - d_particle / d_pore)^2 if d_particle < d_pore else 0.0.
        For multimeric aggregates (d >= 15-50 nm) entering 13 Å pore, K_part = 0.0 (absolute exclusion).
        """
        if particle_diameter_nm >= pore_diameter_nm:
            return 0.0
        return float((1.0 - particle_diameter_nm / pore_diameter_nm) ** 2)

    @classmethod
    def simulate_attec_clearance(
        cls,
        params: Optional[AutophagyBiophysicalParameters] = None,
        attec_conc_nm: float = 50.0,
        duration_hours: float = 48.0,
        aggregate_0_nm: float = 50.0,
    ) -> AutophagySimulationResult:
        """
        Simulates dynamic macroautophagic clearance of insoluble protein aggregates by ATTECs.
        Integrates tethering, autophagosome engulfment, and lysosomal degradation.
        """
        p = params or AutophagyBiophysicalParameters()
        c_eff_lc3_um, enhancement = cls.compute_2d_effective_concentration(
            p.phagophore_lc3_density_per_um2, p.reaction_shell_thickness_nm
        )
        c_eff_lc3_nm = c_eff_lc3_um * 1000.0

        tp_membrane = ThermodynamicParameters(
            kd_target=p.kd_aggregate_nm * 1e-9,
            kd_e3=p.kd_lc3_nm * 1e-9,
            alpha=p.alpha_cooperativity,
        )
        solver = TernaryComplexEquilibrium(tp_membrane)

        k_syn_s = (p.k_syn_aggregate_nm_hr / 3600.0) * 1e-9  # M / s
        k_deg_basal_autophagy = math.log(2.0) / (72.0 * 3600.0) # slow basal autophagy, t1/2 = 72h

        t_span = (0.0, duration_hours * 3600.0)
        t_eval = np.linspace(0.0, duration_hours * 3600.0, 100)
        y0 = np.array([aggregate_0_nm * 1e-9, 0.0, 0.0], dtype=np.float64)

        d_tot = attec_conc_nm * 1e-9
        lc3_tot_mem = c_eff_lc3_nm * 1e-9

        def odes(t: float, y: np.ndarray) -> np.ndarray:
            agg = max(1e-15, y[0])
            engulfed = max(0.0, y[1])

            # Instantaneous quasi-equilibrium ternary tethering on membrane:
            eq = solver.solve(target_tot=agg, e3_tot=lc3_tot_mem, degrader_tot=d_tot)
            tethered_complex = eq.ternary_ted

            # Engulfment flux into autophagosomes:
            v_engulf = p.k_engulf_s * tethered_complex

            # Lysosomal fusion and hydrolase degradation flux:
            v_lys = p.k_lysosomal_clearance_s * engulfed

            # Basal fluxes:
            v_syn = k_syn_s
            v_basal = k_deg_basal_autophagy * agg

            d_agg = v_syn - v_basal - v_engulf
            d_engulfed = v_engulf - v_lys
            d_deg = v_lys

            return np.array([d_agg, d_engulfed, d_deg])

        sol = solve_ivp(odes, t_span, y0, t_eval=t_eval, method='Radau', rtol=1e-5, atol=1e-12)

        residual_agg = float(sol.y[0, -1] * 1e9)
        degraded_cumulative = float(sol.y[2, -1] * 1e9)
        knockdown_pct = float(((aggregate_0_nm - residual_agg) / aggregate_0_nm) * 100.0)
        ton = float(degraded_cumulative / attec_conc_nm if attec_conc_nm > 0 else 0.0)

        return AutophagySimulationResult(
            baseline_aggregate_nm=aggregate_0_nm,
            residual_aggregate_nm=residual_agg,
            aggregate_knockdown_pct=knockdown_pct,
            catalytic_turnover_number=ton,
            effective_2d_lc3_concentration_um=c_eff_lc3_um,
            membrane_enhancement_factor=enhancement,
            proteasome_clearance_pct=0.0,
            autophagic_clearance_pct=knockdown_pct,
            is_catalytic=(ton > 1.0),
        )


# ============================================================================
# 20. RIBOTACs (RIBONUCLEASE-TARGETING CHIMERAS): QUATERNARY EQUILIBRIUM & THE HOOK THEOREM
# ============================================================================

@dataclass
class RIBOTACParameters:
    """Biophysical parameters for targeted RNA cleavage via dimeric RNase L recruitment."""
    kd_rna_nm: float = 15.0            # Affinity of RNA-binding warhead for oncogenic RNA [nM]
    kd_rnase_l_monomer_nm: float = 100.0 # Affinity of recruiter for latent RNase L monomer [nM]
    kd_dimer_clamp_nm: float = 20.0     # Affinity for recruiting 2nd RNase L monomer [nM]
    alpha_1: float = 5.0                # Cooperativity of 1st RNase L recruitment
    alpha_dimer: float = 10.0           # Cooperativity of 2nd RNase L recruitment (dimer clamp)
    k_cleave_s: float = 0.05            # Endoribonucleolytic cleavage rate constant [s^-1]
    rna_half_life_hours: float = 4.0    # Basal target RNA transcript half-life [hours]
    rna_tot_0_nm: float = 20.0          # Initial oncogenic RNA abundance [nM]
    rnase_l_tot_nm: float = 100.0       # Cellular RNase L monomer pool [nM]

@dataclass
class RIBOTACHookMetrics:
    """Metrics quantifying the steepness and descending limb of the quaternary Hook effect."""
    d_opt_nm: float
    quaternary_max_nm: float
    c_hook_50_high_nm: float
    asymptotic_descending_slope: float # Theoretical: -2.0 (quadratic autoinhibition)

@dataclass
class RIBOTACSimulationResult:
    """Quantitative outcome of dynamic RIBOTAC RNA cleavage simulation."""
    degrader_conc_nm: float
    active_quaternary_complex_nm: float
    residual_rna_nm: float
    rna_knockdown_pct: float
    catalytic_turnover_number: float
    quaternary_hook_asymptotic_slope: float
    is_catalytic: bool

class RIBOTACKineticsEngine:
    """
    Biophysical engine for Ribonuclease-Targeting Chimeras (RIBOTACs).
    Models quaternary induced proximity: [Target RNA - RIBOTAC - RNase L_1 - RNase L_2].
    Proves the Quaternary Hook Steepness Theorem:
      lim_[D]->inf [RNA:D:L_2] proportional to 1 / [D]^2 (slope -2.0),
    exhibiting twice the log-log descending slope of classical PROTACs (slope -1.0).
    """

    @classmethod
    def solve_quaternary_equilibrium(
        cls,
        params: RIBOTACParameters,
        rna_tot: float,
        rnase_l_tot: float,
        degrader_tot: float,
    ) -> Dict[str, float]:
        """
        Solves the four-species coupled non-linear mass conservation equations:
          [R]_free, [L]_free, [D]_free
        Species formed:
          [RD] = [R]_f * [D]_f / Kd_rna
          [LD] = [L]_f * [D]_f / Kd_l1
          [RDL] = [RD] * [L]_f / (Kd_l1 / alpha_1)
          [RDL2] = [RDL] * [L]_f / (Kd_l2 / alpha_dimer) (Active catalytic quaternary complex)
        """
        kd_r = params.kd_rna_nm * 1e-9
        kd_l1 = params.kd_rnase_l_monomer_nm * 1e-9
        kd_l2 = params.kd_dimer_clamp_nm * 1e-9
        a1 = params.alpha_1
        a2 = params.alpha_dimer

        kd_l1_prime = kd_l1 / a1
        kd_l2_prime = kd_l2 / a2

        r_tot = rna_tot
        l_tot = rnase_l_tot
        d_tot = degrader_tot

        def residuals(log_vars: np.ndarray) -> List[float]:
            rf = math.exp(log_vars[0])
            lf = math.exp(log_vars[1])
            df = math.exp(log_vars[2])

            rd = (rf * df) / kd_r
            ld = (lf * df) / kd_l1
            rdl = (rd * lf) / kd_l1_prime
            rdl2 = (rdl * lf) / kd_l2_prime

            res_r = (rf + rd + rdl + rdl2) - r_tot
            res_l = (lf + ld + rdl + 2.0 * rdl2) - l_tot
            res_d = (df + rd + ld + rdl + rdl2) - d_tot

            return [res_r / max(1e-15, r_tot), res_l / max(1e-15, l_tot), res_d / max(1e-15, d_tot)]

        init = [
            math.log(max(1e-15, r_tot / (1.0 + d_tot / kd_r))),
            math.log(max(1e-15, l_tot / (1.0 + d_tot / kd_l1))),
            math.log(max(1e-15, d_tot)),
        ]

        res = least_squares(residuals, init, method='lm', xtol=1e-11, ftol=1e-11)
        rf = math.exp(res.x[0])
        lf = math.exp(res.x[1])
        df = math.exp(res.x[2])

        rd = (rf * df) / kd_r
        ld = (lf * df) / kd_l1
        rdl = (rd * lf) / kd_l1_prime
        rdl2 = (rdl * lf) / kd_l2_prime

        return {
            'free_rna': rf,
            'free_rnase_l': lf,
            'free_degrader': df,
            'binary_rd': rd,
            'binary_ld': ld,
            'ternary_rdl': rdl,
            'quaternary_rdl2': rdl2,
        }

    @classmethod
    def analyze_quaternary_hook_curve(
        cls,
        params: Optional[RIBOTACParameters] = None,
        num_points: int = 50,
    ) -> RIBOTACHookMetrics:
        """
        Sweeps degrader concentration from 1 pM to 1 mM.
        Computes D_opt, Quaternary_max, C_hook_50_high, and proves the asymptotic slope is -2.0.
        """
        p = params or RIBOTACParameters()
        r_tot = p.rna_tot_0_nm * 1e-9
        l_tot = p.rnase_l_tot_nm * 1e-9

        d_grid = np.logspace(-12, -3, num_points)
        rdl2_vals = []

        for d in d_grid:
            eq = cls.solve_quaternary_equilibrium(p, r_tot, l_tot, d)
            rdl2_vals.append(eq['quaternary_rdl2'])

        rdl2_arr = np.array(rdl2_vals)
        max_idx = int(np.argmax(rdl2_arr))
        d_opt = float(d_grid[max_idx])
        rdl2_max = float(rdl2_arr[max_idx])

        # Find high 50% hook threshold
        c_hook_50_high = d_opt * 100.0
        for i in range(max_idx, len(d_grid)):
            if rdl2_arr[i] <= 0.50 * rdl2_max:
                c_hook_50_high = float(d_grid[i])
                break

        # Compute asymptotic slope on extreme descending limb (last 8 points)
        high_d = d_grid[-8:]
        high_rdl2 = rdl2_arr[-8:]
        log_d = np.log(high_d)
        log_r = np.log(high_rdl2)
        slope = float(np.polyfit(log_d, log_r, 1)[0])

        return RIBOTACHookMetrics(
            d_opt_nm=d_opt * 1e9,
            quaternary_max_nm=rdl2_max * 1e9,
            c_hook_50_high_nm=c_hook_50_high * 1e9,
            asymptotic_descending_slope=slope,
        )

    @classmethod
    def simulate_ribotac_kinetics(
        cls,
        params: Optional[RIBOTACParameters] = None,
        degrader_conc_nm: float = 50.0,
        duration_hours: float = 24.0,
    ) -> RIBOTACSimulationResult:
        """
        Simulates dynamic cleavage of target RNA by RIBOTAC-recruited RNase L.
        """
        p = params or RIBOTACParameters()
        r_tot_0 = p.rna_tot_0_nm * 1e-9
        l_tot = p.rnase_l_tot_nm * 1e-9
        d_tot = degrader_conc_nm * 1e-9

        t_half_s = p.rna_half_life_hours * 3600.0
        k_deg_basal = math.log(2.0) / t_half_s
        k_syn = k_deg_basal * r_tot_0

        t_span = (0.0, duration_hours * 3600.0)
        t_eval = np.linspace(0.0, duration_hours * 3600.0, 100)

        y0 = np.array([r_tot_0, 0.0], dtype=np.float64)

        def odes(t: float, y: np.ndarray) -> np.ndarray:
            rna_curr = max(1e-15, y[0])
            eq = cls.solve_quaternary_equilibrium(p, rna_curr, l_tot, d_tot)
            rdl2 = eq['quaternary_rdl2']

            v_cleave = p.k_cleave_s * rdl2
            v_syn = k_syn
            v_basal = k_deg_basal * rna_curr

            drna = v_syn - v_basal - v_cleave
            dcleaved = v_cleave

            return np.array([drna, dcleaved])

        sol = solve_ivp(odes, t_span, y0, t_eval=t_eval, method='Radau', rtol=1e-5, atol=1e-12)

        residual_rna = float(sol.y[0, -1] * 1e9)
        cleaved_tot = float(sol.y[1, -1] * 1e9)
        knockdown_pct = float(((p.rna_tot_0_nm - residual_rna) / p.rna_tot_0_nm) * 100.0)
        ton = float(cleaved_tot / degrader_conc_nm if degrader_conc_nm > 0 else 0.0)

        hook_metrics = cls.analyze_quaternary_hook_curve(p, num_points=40)
        eq_final = cls.solve_quaternary_equilibrium(p, residual_rna * 1e-9, l_tot, d_tot)

        return RIBOTACSimulationResult(
            degrader_conc_nm=degrader_conc_nm,
            active_quaternary_complex_nm=float(eq_final['quaternary_rdl2'] * 1e9),
            residual_rna_nm=residual_rna,
            rna_knockdown_pct=knockdown_pct,
            catalytic_turnover_number=ton,
            quaternary_hook_asymptotic_slope=hook_metrics.asymptotic_descending_slope,
            is_catalytic=(ton > 1.0),
        )

    @classmethod
    def compare_protac_vs_ribotac_hook_steepness(
        cls,
        eval_conc_um: float = 100.0,
    ) -> Dict[str, float]:
        """
        Direct quantitative comparison of PROTAC (3-body) vs RIBOTAC (4-body)
        Hook effect suppression at supramicromolar concentrations.
        """
        p_ribo = RIBOTACParameters()
        hook_ribo = cls.analyze_quaternary_hook_curve(p_ribo)

        tp_protac = ThermodynamicParameters(kd_target=15e-9, kd_e3=100e-9, alpha=5.0)
        solver_protac = TernaryComplexEquilibrium(tp_protac)
        hook_analyzer = HookEffectAnalyzer(solver_protac)
        hook_protac = hook_analyzer.analyze_hook_curve(target_tot=20e-9, e3_tot=100e-9)

        c_eval = eval_conc_um * 1e-6

        res_protac = solver_protac.solve(20e-9, 100e-9, c_eval)
        protac_retention = float(res_protac.ternary_ted / hook_protac.ted_max)

        res_ribo = cls.solve_quaternary_equilibrium(p_ribo, 20e-9, 100e-9, c_eval)
        ribo_retention = float(res_ribo['quaternary_rdl2'] / (hook_ribo.quaternary_max_nm * 1e-9))

        suppression_ratio = float(protac_retention / max(1e-15, ribo_retention))

        return {
            'eval_concentration_um': eval_conc_um,
            'protac_peak_ted_nm': hook_protac.ted_max * 1e9,
            'protac_ted_at_eval_nm': res_protac.ternary_ted * 1e9,
            'protac_retention_fraction': protac_retention,
            'ribotac_peak_rdl2_nm': hook_ribo.quaternary_max_nm,
            'ribotac_rdl2_at_eval_nm': res_ribo['quaternary_rdl2'] * 1e9,
            'ribotac_retention_fraction': ribo_retention,
            'ribotac_excess_suppression_ratio': suppression_ratio,
            'protac_asymptotic_slope': -1.0,
            'ribotac_asymptotic_slope': hook_ribo.asymptotic_descending_slope,
        }


# ============================================================================
# 21. EXECUTION DEMO / SMOKE TEST
# ============================================================================

if __name__ == '__main__':
    print("=== TPD KINETICS & COOPERATIVITY ENGINE ===")
    tp = ThermodynamicParameters(kd_target=100e-9, kd_e3=150e-9, alpha=15.0)
    print(f"Cooperativity alpha: {tp.alpha}, Delta Delta G: {tp.delta_delta_g_kcal:.2f} kcal/mol")
    
    solver = TernaryComplexEquilibrium(tp)
    res = solver.solve(target_tot=100e-9, e3_tot=100e-9, degrader_tot=50e-9)
    print(f"At [D]=50 nM: [TED] = {res.ternary_ted * 1e9:.2f} nM ({res.ternary_fraction_target * 100:.1f}% target bound)")

    hook_analyzer = HookEffectAnalyzer(solver)
    metrics = hook_analyzer.analyze_hook_curve(target_tot=100e-9, e3_tot=100e-9)
    print(f"Hook Effect: [D]_opt = {metrics.d_opt * 1e9:.2f} nM, [TED]_max = {metrics.ted_max * 1e9:.2f} nM")
    print(f"FWHM: {metrics.fwhm_log10:.2f} log10 units, Upper 50% hook: {metrics.c_hook_50_high * 1e9:.2f} nM")
    
    sim = TPDKineticsSimulator(tp)
    ton = sim.catalytic_turnover_number(target_tot_0=200e-9, e3_tot_0=100e-9, degrader_tot=10e-9, duration_hours=24.0)
    print(f"Catalytic turnover TON (24h at [D]=10 nM, [T]0=200 nM): {ton:.2f} targets/degrader")

    # Linker Goldilocks demo
    goldilocks = UbiquitinationZoneModel.evaluate_linker_series(alpha_0=50.0)
    best_linker = max(goldilocks, key=lambda x: x["degradation_fitness_score"])
    print(f"Optimal Linker: N={best_linker['num_bonds']} bonds (Fitness Score: {best_linker['degradation_fitness_score']:.3f})")

    # Multi-isoform selectivity demo
    iso_results = IsoformCooperativityResolver.evaluate_bet_bromodomain_paradigm()
    peak_iso = max(iso_results, key=lambda x: x["brd4_ted_nm"])
    print(f"MZ1 Isoform Selectivity at Peak: BRD4/BRD2 = {peak_iso['selectivity_brd4_over_brd2']:.2f}x")

    # Hook Transition Threshold demo (Consilience with Hypatia A003)
    thresh = HookTransitionThresholdEngine.compute_monotonic_saturation_threshold(
        kd_presenter=500e-9, target_tot=1.0e-6, presenter_tot=5.0e-6, c_cutoff=10.0e-6, ternary_kd=5.0e-9
    )
    print(f"Tri-Complex Monotonic Saturation Threshold: alpha* = {thresh.alpha_critical:.1f}, gamma* = {thresh.gamma_critical:.1f}")
    arch = HookTransitionThresholdEngine.evaluate_archetypes_at_cutoff(c_cutoff=10.0e-6)
    print(f"Hook Retention at 10 uM: MZ1 = {arch['MZ1'].retention_fraction*100:.1f}%, RMC-6236 = {arch['RMC-6236'].retention_fraction*100:.1f}%")

    # In Vivo PK/PD Hook Dissipation demo
    pk_engine = InVivoPKPDHookEngine(tp)
    pk_res = pk_engine.simulate_single_dose(dose_mg=140.0)
    print(f"In Vivo PK/PD (140 mg QD): Cmax_plasma = {pk_res.cmax_plasma_um:.2f} uM, Cmax_free = {pk_res.cmax_free_nm:.2f} nM, AUC Suppression = {pk_res.target_auc_suppression_pct:.1f}%")

    # LYTAC demo
    lytac_engine = LYTACTraffickingEngine()
    lytac_res = lytac_engine.simulate()
    print(f"LYTAC Shuttling (24h): TON = {lytac_res.catalytic_turnover_number:.2f} targets/LYTAC, Target KD = {lytac_res.target_knockdown_pct:.1f}%, Rec Cons = {lytac_res.receptor_conservation_pct:.1f}%")

    # Resynthesis Spectrum demo
    spectrum = TargetResynthesisSpectrumEngine.evaluate_target_spectrum()
    cmyc = next(s for s in spectrum if s.target_name == 'c-Myc')
    tau = next(s for s in spectrum if s.target_name == 'Tau')
    print(f"Resynthesis Spectrum: c-Myc f_TED(90%) = {cmyc.required_ternary_fraction_90pct_deg:.2f}% vs Tau f_TED(90%) = {tau.required_ternary_fraction_90pct_deg:.2f}%")

    # Tissue-Selective BCL-xL demo
    bclxl_eval = TissueSelectiveE3Engine.evaluate_bcl_xl_paradigm(doses_nm=[100.0])
    dt = bclxl_eval["DT2216"]["dose_responses"][0]
    pz = bclxl_eval["PZ15227"]["dose_responses"][0]
    print(f"Tissue-Selective TPD (100 nM): DT2216 Platelet Target = {dt.normal_tissue_target_level_pct:.1f}% (TSI = {bclxl_eval['DT2216']['therapeutic_safety_index']:.1f}x) vs PZ15227 Platelet Target = {pz.normal_tissue_target_level_pct:.1f}%")

    # ATTEC Autophagy demo
    attec_res = AutophagyTargetingEngine.simulate_attec_clearance(attec_conc_nm=50.0)
    print(f"ATTEC Autophagy (50 nM): Aggregate Knockdown = {attec_res.aggregate_knockdown_pct:.1f}%, TON = {attec_res.catalytic_turnover_number:.2f}, 2D C_eff = {attec_res.effective_2d_lc3_concentration_um:.1f} uM ({attec_res.membrane_enhancement_factor:.1f}x boost)")

    # RIBOTAC Quaternary Hook demo
    ribo_comp = RIBOTACKineticsEngine.compare_protac_vs_ribotac_hook_steepness(eval_conc_um=100.0)
    print(f"RIBOTAC Quaternary Hook: Slope = {ribo_comp['ribotac_asymptotic_slope']:.2f} (vs PROTAC {ribo_comp['protac_asymptotic_slope']:.1f}), 100 uM Excess Suppression = {ribo_comp['ribotac_excess_suppression_ratio']:.1f}x")


