"""
patient_heterogeneity_and_endotype_stratification_engine.py
Agent: Hypatia (A003), Generation 0
Domain: New drug discovery (drug-discovery)

Quantitative Mathematical Engine for Modeling:
  1. The "All-Comers Trap": Cohort dilution in syndromic, polygenic disease indications.
  2. The Quadratic Sample Size Penalty: N_required proportional to (1 / f_responder)^2.
  3. Phase II Statistical Power Collapse under unstratified trial designs.
  4. Computational Multi-Omic Endotype Classifier Enrichment and Rescue.
  5. Fisher exact and two-sample Z-power derivations for prospective clinical adjudication.
"""

import math
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple


def normal_cdf(x: float) -> float:
    """Computes standard normal cumulative distribution function Phi(x)."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normal_ppf(p: float) -> float:
    """
    Computes inverse normal CDF (probit) using Acklam's rational approximation.
    Accurate to within 1.15e-9 across (0, 1).
    """
    if p <= 0.0 or p >= 1.0:
        raise ValueError(f"p must be strictly in (0, 1), got {p}")

    a = [-3.969683028665376e+01, 2.209460984245205e+02,
         -2.759285104469687e+02, 1.383577518672690e+02,
         -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02,
         -1.556989798598866e+02, 6.680131188771972e+01,
         -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01,
         -2.400758277161838e+00, -2.549732539343734e+00,
         4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01,
         2.445134137142996e+00, 3.754408661907416e+00]

    q = min(p, 1.0 - p)
    if q > 0.02425:
        r = p - 0.5
        r2 = r * r
        num = ((((a[0] * r2 + a[1]) * r2 + a[2]) * r2 + a[3]) * r2 + a[4]) * r2 + a[5]
        den = ((((b[0] * r2 + b[1]) * r2 + b[2]) * r2 + b[3]) * r2 + b[4]) * r2 + 1.0
        return r * num / den
    else:
        r = math.sqrt(-2.0 * math.log(q))
        num = ((((c[0] * r + c[1]) * r + c[2]) * r + c[3]) * r + c[4]) * r + c[5]
        den = (((d[0] * r + d[1]) * r + d[2]) * r + d[3]) * r + 1.0
        val = num / den
        return -val if p < 0.5 else val


@dataclass(frozen=True)
class SyndromicTrialModel:
    """
    Models clinical efficacy and statistical power in syndromic polygenic trials
    as a function of mechanistic responder subphenotype prevalence (f_responder).
    """
    disease_indication: str
    true_biological_effect_d: float  # True Cohen's d in biological responders (e.g. 0.60)
    unselected_responder_prevalence: float  # Fraction of syndromic cohort with active target pathway
    phase2_sample_size_per_arm: int = 100
    alpha: float = 0.05

    def calculate_diluted_effect(self, f_resp: float) -> float:
        """
        Observed trial effect size when only f_resp fraction responds:
        d_obs = f_resp * d_true + (1 - f_resp) * 0 = f_resp * d_true.
        """
        return f_resp * self.true_biological_effect_d

    def calculate_statistical_power(self, f_resp: float, n_per_arm: int) -> float:
        """
        Computes power for two-sample independent t-test (large-sample Z approximation):
        Power = Phi( (d_obs * sqrt(N / 2)) - z_(1 - alpha/2) ).
        """
        d_obs = self.calculate_diluted_effect(f_resp)
        z_crit = normal_ppf(1.0 - self.alpha / 2.0)
        ncp = d_obs * math.sqrt(n_per_arm / 2.0)
        z_beta = ncp - z_crit
        return normal_cdf(z_beta)

    def calculate_required_sample_size(self, f_resp: float, target_power: float = 0.80) -> int:
        """
        Computes required sample size per arm to achieve target power:
        N_per_arm = 2 * ((z_crit + z_beta) / d_obs)^2.
        Exhibits quadratic scaling: N proportional to 1 / (f_resp)^2.
        """
        d_obs = self.calculate_diluted_effect(f_resp)
        if d_obs <= 1e-6:
            return 10000000
        z_crit = normal_ppf(1.0 - self.alpha / 2.0)
        z_beta = normal_ppf(target_power)
        n_exact = 2.0 * ((z_crit + z_beta) / d_obs) ** 2
        return int(math.ceil(n_exact))

    def evaluate_enrichment_impact(
        self,
        classifier_sensitivity: float = 0.85,
        classifier_specificity: float = 0.90
    ) -> Dict[str, Any]:
        """
        Calculates positive predictive value (enriched prevalence) of a multi-omic classifier:
        PPV = (Sens * Prev) / (Sens * Prev + (1 - Spec) * (1 - Prev))
        """
        prev = self.unselected_responder_prevalence
        tp = classifier_sensitivity * prev
        fp = (1.0 - classifier_specificity) * (1.0 - prev)
        enriched_prev = tp / (tp + fp)

        # Baseline (Unselected All-Comers)
        base_d = self.calculate_diluted_effect(prev)
        base_power = self.calculate_statistical_power(prev, self.phase2_sample_size_per_arm)
        base_n_req = self.calculate_required_sample_size(prev, target_power=0.80)

        # Enriched (Computational Multi-Omic Selection)
        enriched_d = self.calculate_diluted_effect(enriched_prev)
        enriched_power = self.calculate_statistical_power(enriched_prev, self.phase2_sample_size_per_arm)
        enriched_n_req = self.calculate_required_sample_size(enriched_prev, target_power=0.80)

        sample_size_reduction_factor = base_n_req / enriched_n_req
        power_gain_abs = enriched_power - base_power

        return {
            "disease_indication": self.disease_indication,
            "true_d_in_responders": self.true_biological_effect_d,
            "baseline": {
                "unselected_prevalence": prev,
                "observed_d": round(base_d, 4),
                "phase2_power_at_n100": round(base_power, 4),
                "required_n_per_arm_for_80pct_power": base_n_req,
                "total_trial_n_for_80pct_power": 2 * base_n_req
            },
            "classifier_specs": {
                "sensitivity": classifier_sensitivity,
                "specificity": classifier_specificity,
                "enriched_prevalence_ppv": round(enriched_prev, 4)
            },
            "enriched": {
                "observed_d": round(enriched_d, 4),
                "phase2_power_at_n100": round(enriched_power, 4),
                "required_n_per_arm_for_80pct_power": enriched_n_req,
                "total_trial_n_for_80pct_power": 2 * enriched_n_req
            },
            "comparative_advantage": {
                "sample_size_reduction_factor": round(sample_size_reduction_factor, 2),
                "phase2_power_gain_percentage_points": round(power_gain_abs * 100.0, 1),
                "type2_error_drop": round((1.0 - base_power) - (1.0 - enriched_power), 4)
            }
        }


# ============================================================================
# HISTORICAL CASE BENCHMARKS
# ============================================================================

CASE_STUDIES: Dict[str, SyndromicTrialModel] = {
    "Alzheimer_Syndromic_Dementia": SyndromicTrialModel(
        disease_indication="Alzheimer's Disease (All-Comers vs Amyloid/Tau Centiloid Biomarker)",
        true_biological_effect_d=0.55,
        unselected_responder_prevalence=0.20,  # Only ~20% of unselected clinical dementia is early-stage plaque-driven
        phase2_sample_size_per_arm=120
    ),
    "Atherosclerosis_Inflammation_CANTOS": SyndromicTrialModel(
        disease_indication="Atherosclerosis Anti-IL1B (CANTOS: All-Comers vs hsCRP >= 2 mg/L)",
        true_biological_effect_d=0.45,
        unselected_responder_prevalence=0.35,  # ~35% of CAD patients have residual inflammatory risk
        phase2_sample_size_per_arm=150
    ),
    "Severe_Asthma_Eosinophilic": SyndromicTrialModel(
        disease_indication="Severe Asthma Anti-IL5 (All-Comers vs Eosinophils >= 300/uL)",
        true_biological_effect_d=0.65,
        unselected_responder_prevalence=0.25,  # ~25% have severe T2-high eosinophilic asthma
        phase2_sample_size_per_arm=80
    ),
    "Heart_Failure_Preserved_EF": SyndromicTrialModel(
        disease_indication="Heart Failure with Preserved Ejection Fraction (HFpEF)",
        true_biological_effect_d=0.50,
        unselected_responder_prevalence=0.22,  # Multiple divergent etiologies (metabolic, amyloid, hypertensive)
        phase2_sample_size_per_arm=140
    )
}


def run_comprehensive_stratification_analysis() -> Dict[str, Any]:
    """Runs stratification evaluations across all major complex polygenic disease benchmarks."""
    results = {}
    for key, model in CASE_STUDIES.items():
        results[key] = model.evaluate_enrichment_impact(
            classifier_sensitivity=0.85,
            classifier_specificity=0.90
        )
    return results


if __name__ == "__main__":
    res = run_comprehensive_stratification_analysis()
    print("=== PATIENT HETEROGENEITY & MULTI-OMIC ENDOTYPING ANALYSIS ===")
    for k, v in res.items():
        print(f"\n--- {v['disease_indication']} ---")
        print(f"  Baseline: Prev={v['baseline']['unselected_prevalence']}, d_obs={v['baseline']['observed_d']}, Ph2 Power={v['baseline']['phase2_power_at_n100']*100:.1f}%, Req Total N={v['baseline']['total_trial_n_for_80pct_power']}")
        print(f"  Enriched: Prev={v['classifier_specs']['enriched_prevalence_ppv']}, d_obs={v['enriched']['observed_d']}, Ph2 Power={v['enriched']['phase2_power_at_n100']*100:.1f}%, Req Total N={v['enriched']['total_trial_n_for_80pct_power']}")
        print(f"  Gain: Sample Size Reduction={v['comparative_advantage']['sample_size_reduction_factor']}x, Power Gain=+{v['comparative_advantage']['phase2_power_gain_percentage_points']} pts")
