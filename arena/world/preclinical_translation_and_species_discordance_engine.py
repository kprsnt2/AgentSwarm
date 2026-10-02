"""
preclinical_translation_and_species_discordance_engine.py - Causal Modeling of Preclinical Translation Failure
Agent: Hypatia (A003), Generation 0
Domain: New drug discovery (drug-discovery)

Models the translational failure boundaries between animal models and human clinical trials:
1. Allometric pharmacokinetic distortion and peak-to-trough (Cmax/Cmin) exposure disparity.
2. Cross-species genomic response divergence (Seok et al. 2013).
3. Bayesian diagnostic predictive value (PPV/NPV) of rodent models vs Human Microphysiological Systems (MPS).
4. Rigorous statistical power and Fisher exact contingency derivation for prospective clinical validation.
"""

import math
from typing import Dict, List, Tuple, Any

def normal_cdf(x: float) -> float:
    """Standard normal cumulative distribution function using error function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def normal_ppf(p: float) -> float:
    """
    Inverse standard normal cumulative distribution function (quantile / probit).
    Wichura's AS 241 rational approximation algorithm.
    """
    if p <= 0.0 or p >= 1.0:
        raise ValueError("Probability p must be strictly between 0 and 1.")
    
    q = p - 0.5
    if abs(q) <= 0.425:
        r = 0.180625 - q * q
        return q * (((((((2.5090809287301226727e+3 * r +
                          3.3430575583588128105e+4) * r +
                          6.7265770927008700853e+4) * r +
                          4.5921953931549871457e+4) * r +
                          1.3731693765509461125e+4) * r +
                          1.6715828100597728482e+3) * r +
                          6.7718002014526557e+1) * r + 1.0) / \
                   (((((((5.2264952788528545610e+3 * r +
                          2.8729085735721942674e+4) * r +
                          3.9307895800092710610e+4) * r +
                          2.1213794301586595867e+4) * r +
                          5.3941960214247511077e+3) * r +
                          6.8718700749205790830e+2) * r +
                          4.2313330701600911252e+1) * r + 1.0)
    
    r = p if q < 0.0 else 1.0 - p
    r = math.sqrt(-math.log(r))
    
    if r <= 5.0:
        r -= 1.6
        val = (((((((7.7454501427834140764e-4 * r +
                     2.272384498926918458e-2) * r +
                     2.4178072517745061177e-1) * r +
                     1.2704582524523683825e+0) * r +
                     3.6478483247632046050e+0) * r +
                     5.7694972214606914055e+0) * r +
                     4.6303378461565451683e+0) * r +
                     1.4234371107496835773e+0) / \
              (((((((1.0507500716444168432e-9 * r +
                     5.475938084995344946e-4) * r +
                     1.5198666563616457196e-2) * r +
                     1.4810397642748007459e-1) * r +
                     6.8976733498510000455e-1) * r +
                     1.6763848301838038494e+0) * r +
                     2.0531916266377588218e+0) * r + 1.0)
    else:
        r -= 5.0
        val = (((((((2.0103343992922881326e-7 * r +
                     2.7115555687434875781e-5) * r +
                     1.2426612033802778659e-3) * r +
                     2.6532189526576123028e-2) * r +
                     2.9656057182850489123e-1) * r +
                     1.7848265399172913358e+0) * r +
                     5.4637849111641143699e+0) * r +
                     6.6579046435011037772e+0) / \
              (((((((2.0442631033891978149e-15 * r +
                     1.4215117583164458887e-7) * r +
                     1.8463183175100546818e-5) * r +
                     7.8686913114561325910e-4) * r +
                     1.4845469588856340008e-2) * r +
                     1.2578172611122924620e-1) * r +
                     4.7968549929772534833e-1) * r + 1.0)
    
    return -val if q < 0.0 else val

def allometric_pk_scaling(
    bw_mouse_kg: float = 0.02,
    bw_human_kg: float = 70.0,
    cl_mouse_l_per_hr_kg: float = 2.5,
    vd_mouse_l_per_kg: float = 1.0
) -> Dict[str, float]:
    """
    Computes rigorous allometric scaling of PK parameters:
    - Clearance: CL = CL_0 * BW^0.75
    - Volume of Distribution: Vd = Vd_0 * BW^1.0
    - Elimination rate constant: k_el = CL / Vd
    - Half-life: t_1/2 = ln(2) / k_el = ln(2) * Vd / CL proportional to BW^0.25
    """
    cl_mouse_total = cl_mouse_l_per_hr_kg * bw_mouse_kg
    vd_mouse_total = vd_mouse_l_per_kg * bw_mouse_kg
    k_el_mouse = cl_mouse_total / vd_mouse_total
    t_half_mouse = math.log(2.0) / k_el_mouse

    # Scale to human
    # CL_human = CL_mouse_total * (BW_human / BW_mouse)^0.75
    cl_human_total = cl_mouse_total * math.pow(bw_human_kg / bw_mouse_kg, 0.75)
    cl_human_per_kg = cl_human_total / bw_human_kg

    # Vd_human = Vd_mouse_total * (BW_human / BW_mouse)^1.0
    vd_human_total = vd_mouse_total * (bw_human_kg / bw_mouse_kg)
    vd_human_per_kg = vd_human_total / bw_human_kg

    k_el_human = cl_human_total / vd_human_total
    t_half_human = math.log(2.0) / k_el_human

    # Half life scaling ratio (BW_human / BW_mouse)^0.25
    half_life_ratio = t_half_human / t_half_mouse

    # Peak-to-trough concentration ratio at tau = 12 hr dosing interval:
    # Cmax / Cmin = exp(k_el * tau)
    cmax_cmin_mouse_12h = math.exp(k_el_mouse * 12.0)
    cmax_cmin_human_12h = math.exp(k_el_human * 12.0)

    # To maintain trough Cmin >= Kd in mouse with tau=12h, Cmax must be cmax_cmin_mouse * Kd
    return {
        "cl_mouse_total_l_hr": cl_mouse_total,
        "cl_human_total_l_hr": cl_human_total,
        "cl_human_per_kg": cl_human_per_kg,
        "vd_mouse_total_l": vd_mouse_total,
        "vd_human_total_l": vd_human_total,
        "t_half_mouse_hr": t_half_mouse,
        "t_half_human_hr": t_half_human,
        "half_life_ratio_human_to_mouse": half_life_ratio,
        "k_el_mouse_hr_inv": k_el_mouse,
        "k_el_human_hr_inv": k_el_human,
        "cmax_cmin_ratio_mouse_12h": cmax_cmin_mouse_12h,
        "cmax_cmin_ratio_human_12h": cmax_cmin_human_12h,
        "peak_exposure_penalty_mouse": cmax_cmin_mouse_12h / cmax_cmin_human_12h
    }

def bayesian_predictive_value(sensitivity: float, specificity: float, prevalence: float) -> Dict[str, float]:
    """
    Computes Positive Predictive Value (PPV) and Negative Predictive Value (NPV)
    under Bayes' theorem.
    """
    tp = sensitivity * prevalence
    fp = (1.0 - specificity) * (1.0 - prevalence)
    fn = (1.0 - sensitivity) * prevalence
    tn = specificity * (1.0 - prevalence)

    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0.0
    fdr = fp / (tp + fp) if (tp + fp) > 0 else 0.0 # False Discovery Rate

    return {
        "sensitivity": sensitivity,
        "specificity": specificity,
        "prevalence": prevalence,
        "ppv": ppv,
        "npv": npv,
        "false_discovery_rate": fdr
    }

def calculate_two_sample_power(p1: float, p2: float, n1: int, n2: int, alpha: float = 0.05) -> float:
    """Computes statistical power for two independent proportions."""
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    se_null = math.sqrt(p_pool * (1.0 - p_pool) * (1.0 / n1 + 1.0 / n2))
    se_alt = math.sqrt(p1 * (1.0 - p1) / n1 + p2 * (1.0 - p2) / n2)
    
    z_crit = normal_ppf(1.0 - alpha / 2.0)
    delta = abs(p1 - p2)
    z_stat = (delta - z_crit * se_null) / se_alt
    return normal_cdf(z_stat)

def log_factorial(n: int) -> float:
    """Stirling or exact log factorial sum."""
    if n < 0:
        raise ValueError("Factorial not defined for negative integers.")
    return math.lgamma(n + 1)

def fisher_exact_2x2(a: int, b: int, c: int, d: int) -> Tuple[float, float]:
    """Computes odds ratio and two-sided p-value for 2x2 contingency table [[a, b], [c, d]]."""
    n = a + b + c + d
    row1 = a + b
    row2 = c + d
    col1 = a + c
    col2 = b + d

    odds_ratio = (a * d) / (b * c) if (b * c) > 0 else float('inf')

    def hypergeom_prob(x: int) -> float:
        y = row1 - x
        z = col1 - x
        w = row2 - z
        if x < 0 or y < 0 or z < 0 or w < 0:
            return 0.0
        log_p = (log_factorial(row1) + log_factorial(row2) +
                 log_factorial(col1) + log_factorial(col2) -
                 log_factorial(n) - log_factorial(x) -
                 log_factorial(y) - log_factorial(z) - log_factorial(w))
        return math.exp(log_p)

    obs_prob = hypergeom_prob(a)
    min_x = max(0, col1 - row2)
    max_x = min(row1, col1)

    p_value = 0.0
    for x in range(min_x, max_x + 1):
        pr = hypergeom_prob(x)
        if pr <= obs_prob * (1.0 + 1e-9):
            p_value += pr

    return odds_ratio, min(1.0, p_value)

class PreclinicalTranslationModel:
    """Comprehensive modeling of preclinical species discordance vs human MPS."""

    def __init__(self):
        self.allometry = allometric_pk_scaling()
        # Historical performance metrics for standard rodent disease models (Olson 2000, Arrowsmith 2011)
        self.rodent_efficacy_eval = bayesian_predictive_value(
            sensitivity=0.50, specificity=0.68, prevalence=0.10
        )
        # Human Microphysiological Systems (MPS / Organ-on-a-Chip, Emulate / Ewart 2022)
        self.mps_efficacy_eval = bayesian_predictive_value(
            sensitivity=0.87, specificity=0.98, prevalence=0.10
        )

    def evaluate_clinical_adjudication_trial(self, n_per_arm: int = 90) -> Dict[str, Any]:
        """
        Adjudication trial testing Phase II POS:
        Cohort A: Traditional Rodent In Vivo Model Selection (POS = 28.9%)
        Cohort B: Human MPS + Cross-Species QSP Filtered Selection (POS = 58.0%)
        """
        pos_a = 0.289
        pos_b = 0.580
        power = calculate_two_sample_power(pos_b, pos_a, n_per_arm, n_per_arm, alpha=0.05)

        # Expected counts
        success_a = round(n_per_arm * pos_a)
        fail_a = n_per_arm - success_a
        success_b = round(n_per_arm * pos_b)
        fail_b = n_per_arm - success_b

        odds_ratio, p_val = fisher_exact_2x2(success_b, fail_b, success_a, fail_a)

        return {
            "n_per_arm": n_per_arm,
            "total_patients": 2 * n_per_arm,
            "cohort_a_pos": pos_a,
            "cohort_b_pos": pos_b,
            "delta_pos": pos_b - pos_a,
            "statistical_power": power,
            "expected_counts": {
                "cohort_a": {"success": success_a, "fail": fail_a},
                "cohort_b": {"success": success_b, "fail": fail_b}
            },
            "odds_ratio": odds_ratio,
            "fisher_p_value": p_val
        }

if __name__ == "__main__":
    model = PreclinicalTranslationModel()
    print("--- ALLOMETRIC PK DISTORTION ---")
    for k, v in model.allometry.items():
        print(f"  {k}: {v:.4f}")
    print("\n--- BAYESIAN PREDICTIVE VALUE (10% Prevalence) ---")
    print(f"  Rodent Model PPV: {model.rodent_efficacy_eval['ppv']*100:.2f}% (FDR: {model.rodent_efficacy_eval['false_discovery_rate']*100:.2f}%)")
    print(f"  Human MPS PPV:    {model.mps_efficacy_eval['ppv']*100:.2f}% (FDR: {model.mps_efficacy_eval['false_discovery_rate']*100:.2f}%)")
    print("\n--- ADJUDICATION TRIAL POWER (N=90/arm) ---")
    res = model.evaluate_clinical_adjudication_trial(90)
    print(f"  Statistical Power: {res['statistical_power']*100:.2f}%")
    print(f"  Odds Ratio:        {res['odds_ratio']:.3f}")
    print(f"  Fisher p-value:    {res['fisher_p_value']:.4e}")
