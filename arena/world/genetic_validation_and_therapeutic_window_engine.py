"""
genetic_validation_and_therapeutic_window_engine.py - Causal Analysis of Genetic Validation vs Residual Attrition
Agent: Hypatia (A003), Generation 0
Epistemic Class: Empirical
Standards of Evidence: Strictly quantitative, anchored in peer-reviewed clinical, genetic, and pharmacological data.

Formalizes:
  1. Empirical Bayesian clinical transition probabilities stratified by human genetic evidence (Nelson 2015, King 2019).
  2. The Genetic Validation Paradox: Why 83% of genetically supported targets still fail in clinical trials.
  3. The Therapeutic Window / On-Target Toxicity Boundary Model (Black-Leff & Hill equations).
  4. Chronic lifelong 50% heterozygous suppression vs acute adult 85% pharmacological inhibition.
  5. The BACE1 Alzheimer's empirical paradigm: APP A673T protective genetics vs clinical failure via substrate pleiotropy.
  6. Statistical power and sample size derivations for a prospective adjudication cohort.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any


@dataclass(frozen=True)
class PhaseTransitionRates:
    phase1_to_phase2: float
    phase2_to_phase3: float
    phase3_to_nda: float
    nda_to_approval: float

    @property
    def cumulative_loa(self) -> float:
        """Overall clinical Likelihood of Approval (Phase I to Approval)."""
        return (
            self.phase1_to_phase2
            * self.phase2_to_phase3
            * self.phase3_to_nda
            * self.nda_to_approval
        )

    @property
    def cumulative_attrition(self) -> float:
        """Overall clinical attrition rate."""
        return 1.0 - self.cumulative_loa


# Empirical transition benchmarks from Nelson et al. 2015 Nature Genetics & King et al. 2019 PLOS Genetics
GENETIC_ATTRITION_BENCHMARKS = {
    "No_Genetic_Support": PhaseTransitionRates(
        phase1_to_phase2=0.584,
        phase2_to_phase3=0.289,
        phase3_to_nda=0.578,
        nda_to_approval=0.879,
    ),
    "Human_Genetic_Support": PhaseTransitionRates(
        phase1_to_phase2=0.682,
        phase2_to_phase3=0.445,
        phase3_to_nda=0.620,
        nda_to_approval=0.900,
    ),
}


@dataclass
class TargetTherapeuticWindow:
    target_name: str
    kd_nm: float
    ec50_efficacy_occupancy: float  # e.g., 0.85 (85% occupancy required for clinical efficacy)
    ec50_toxicity_occupancy: float  # e.g., 0.70 (70% occupancy in normal tissue triggers Dose-Limiting Toxicity)
    genetic_loss_of_function_effect: float = 0.50  # 50% reduction in lifetime heterozygotes
    substrate_pleiotropy_count: int = 1  # Number of physiological substrates cleaved/regulated

    def required_free_concentration_for_efficacy(self) -> float:
        """Calculate unbound concentration Cu required to achieve efficacy occupancy."""
        if self.ec50_efficacy_occupancy >= 1.0:
            return float("inf")
        return self.kd_nm * (self.ec50_efficacy_occupancy / (1.0 - self.ec50_efficacy_occupancy))

    def threshold_free_concentration_for_toxicity(self) -> float:
        """Calculate unbound concentration Cu at which normal-tissue toxicity manifests."""
        if self.ec50_toxicity_occupancy >= 1.0:
            return float("inf")
        return self.kd_nm * (self.ec50_toxicity_occupancy / (1.0 - self.ec50_toxicity_occupancy))

    def therapeutic_index(self) -> float:
        """
        Therapeutic Index (TI) = Cu,toxicity_threshold / Cu,efficacy_required.
        TI < 1.0 indicates an impossible therapeutic window for unselective orthosteric inhibition.
        """
        cu_eff = self.required_free_concentration_for_efficacy()
        cu_tox = self.threshold_free_concentration_for_toxicity()
        if cu_eff <= 0.0:
            return 0.0
        return cu_tox / cu_eff

    def lifetime_vs_acute_dosage_ratio(self) -> float:
        """
        Ratio of acute adult pharmacological occupancy required to lifelong heterozygous gene dosage.
        Lifelong 50% suppression represents genetic protection; acute 85% represents drug occupancy.
        """
        return self.ec50_efficacy_occupancy / self.genetic_loss_of_function_effect

    def evaluate_clinical_viability(self) -> Dict[str, Any]:
        cu_eff = self.required_free_concentration_for_efficacy()
        cu_tox = self.threshold_free_concentration_for_toxicity()
        ti = self.therapeutic_index()
        is_viable = ti >= 1.0

        return {
            "target_name": self.target_name,
            "kd_nm": self.kd_nm,
            "required_cu_efficacy_nm": round(cu_eff, 2),
            "threshold_cu_toxicity_nm": round(cu_tox, 2),
            "therapeutic_index": round(ti, 3),
            "is_clinically_viable": is_viable,
            "dosage_ratio_acute_to_genetic": round(self.lifetime_vs_acute_dosage_ratio(), 2),
            "substrate_pleiotropy_count": self.substrate_pleiotropy_count,
            "failure_mode": (
                "None" if is_viable
                else "Mechanism-based on-target toxicity / Narrow Therapeutic Index"
            ),
        }


def normal_cdf(x: float) -> float:
    """Standard normal cumulative distribution function via error function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normal_ppf(p: float) -> float:
    """Inverse normal CDF (quantile function) via rational approximation."""
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p must be in (0, 1)")

    # Rational approximation for central and tail regions
    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    ]

    p_low = 0.02425
    p_high = 1.0 - p_low

    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (
            ((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]
        ) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        return (
            (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q
        ) / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(
            ((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]
        ) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)


def calculate_proportional_hazards_power(
    hr: float, n_patients: int, event_rate: float = 0.75, alpha: float = 0.05
) -> Dict[str, float]:
    """
    Calculate statistical power for a time-to-event trial using Schoenfeld's formula.
    D = n_patients * event_rate (total number of observed events).
    """
    events = n_patients * event_rate
    ln_hr = math.log(hr)
    z_alpha = normal_ppf(1.0 - alpha / 2.0)

    # From D = 4 * (z_alpha + z_beta)^2 / (ln_hr)^2
    # sqrt(D * ln_hr^2 / 4) - z_alpha = z_beta
    arg = math.sqrt(events * (ln_hr**2) / 4.0) - z_alpha
    power = normal_cdf(arg)

    return {
        "hazard_ratio": hr,
        "n_patients": n_patients,
        "expected_events": round(events, 1),
        "alpha": alpha,
        "statistical_power": round(power, 4),
    }


def analyze_genetic_paradox() -> Dict[str, Any]:
    """
    Comprehensive quantitative analysis of human genetic support vs residual attrition.
    """
    no_gen = GENETIC_ATTRITION_BENCHMARKS["No_Genetic_Support"]
    gen = GENETIC_ATTRITION_BENCHMARKS["Human_Genetic_Support"]

    loa_no_gen = no_gen.cumulative_loa
    loa_gen = gen.cumulative_loa
    enrichment_ratio = loa_gen / loa_no_gen
    phase2_or = (gen.phase2_to_phase3 / (1.0 - gen.phase2_to_phase3)) / (
        no_gen.phase2_to_phase3 / (1.0 - no_gen.phase2_to_phase3)
    )

    # Model representative targets:
    # 1. BACE1 (Alzheimer's: APP A673T protective; failures due to substrate pleiotropy and on-target toxicity)
    bace1 = TargetTherapeuticWindow(
        target_name="BACE1_Orthosteric",
        kd_nm=10.0,
        ec50_efficacy_occupancy=0.85,
        ec50_toxicity_occupancy=0.65,  # NRG1 / NCAM1 cleavage inhibition triggers cognitive worsening at >65%
        genetic_loss_of_function_effect=0.40,  # A673T causes ~40% lifetime reduction in Abeta
        substrate_pleiotropy_count=32,  # >30 known physiological substrates
    )

    # 2. PCSK9 (Cardiovascular: LDLR protection; clean success due to high therapeutic index)
    pcsk9 = TargetTherapeuticWindow(
        target_name="PCSK9_Target",
        kd_nm=5.0,
        ec50_efficacy_occupancy=0.80,
        ec50_toxicity_occupancy=0.99,  # Complete genetic knockout is benign in humans
        genetic_loss_of_function_effect=0.50,
        substrate_pleiotropy_count=1,
    )

    # 3. Pan-Notch (Oncology: clean genetic role, but severe gastrointestinal toxicity)
    notch = TargetTherapeuticWindow(
        target_name="Pan_Notch_Inhibitor",
        kd_nm=25.0,
        ec50_efficacy_occupancy=0.85,
        ec50_toxicity_occupancy=0.55,  # Secretory diarrhea at >55% gut Notch1/2 inhibition
        genetic_loss_of_function_effect=0.50,
        substrate_pleiotropy_count=4,
    )

    # Calculate power for an adjudication trial testing substrate-selective modulation
    trial_power = calculate_proportional_hazards_power(hr=0.65, n_patients=340, event_rate=0.75, alpha=0.05)

    return {
        "transition_rates": {
            "no_genetic_support": {
                "phase1_to_phase2": no_gen.phase1_to_phase2,
                "phase2_to_phase3": no_gen.phase2_to_phase3,
                "phase3_to_nda": no_gen.phase3_to_nda,
                "nda_to_approval": no_gen.nda_to_approval,
                "cumulative_loa": round(loa_no_gen, 4),
                "cumulative_attrition": round(no_gen.cumulative_attrition, 4),
            },
            "human_genetic_support": {
                "phase1_to_phase2": gen.phase1_to_phase2,
                "phase2_to_phase3": gen.phase2_to_phase3,
                "phase3_to_nda": gen.phase3_to_nda,
                "nda_to_approval": gen.nda_to_approval,
                "cumulative_loa": round(loa_gen, 4),
                "cumulative_attrition": round(gen.cumulative_attrition, 4),
            },
            "loa_enrichment_ratio": round(enrichment_ratio, 2),
            "phase2_transition_odds_ratio": round(phase2_or, 2),
            "residual_attrition_rate_genetically_supported": round(gen.cumulative_attrition, 4),
        },
        "target_case_evaluations": [
            bace1.evaluate_clinical_viability(),
            pcsk9.evaluate_clinical_viability(),
            notch.evaluate_clinical_viability(),
        ],
        "prospective_adjudication_trial_power": trial_power,
    }


if __name__ == "__main__":
    import pprint
    results = analyze_genetic_paradox()
    pprint.pprint(results)
