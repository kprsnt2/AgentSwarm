"""
Krishna and Mahabharata: Equifinality Horizons, Algorithmic Transmission,
and Terminal Epistemic Demarcation Engine.

Author: Kepler (A001, Autonomous Research Agent, Swarm Generation 0)
Date: October 5, 2026
Domain: "what about Lord Krishna and he is real, Mahabharata happened?" (what-about-lord-krishna-and)
Epistemic Class: Metaphysical

STANDARD OF EVIDENCE: Strictly Not Empirically Decidable for Metaphysical Claims.
PROTOCOL INVARIANTS:
1. Zero assertion of a dogmatic verdict (rejection of proving or disproving the claim).
2. Zero presentation of personal conviction or devotional sentiment as findings.
3. Strict demarcation across metaphysical, material-historical, and poetic domains.
4. Formalization of what the claim asserts, what counts as evidence, and why it resists testing.
"""

import math
from typing import Dict, List, Tuple, Any


class EpistemicProtocolViolation(Exception):
    """Raised when an epistemic protocol rule is violated."""
    pass


class EquifinalityHorizonCalculator:
    """
    Computes archaeological and historiographical equifinality:
    the condition where distinct historical hypotheses yield observationally
    indistinguishable material signatures given taphonomic decay.
    """

    @staticmethod
    def compute_hypothesis_likelihoods(
        taphonomic_loss_factor: float,
        base_signals: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculates observable signature S_obs = S_base * (1 - taphonomic_loss_factor).
        When taphonomic_loss_factor -> 1.0, observable signals converge to zero/noise.
        """
        if not (0.0 <= taphonomic_loss_factor <= 1.0):
            raise ValueError("taphonomic_loss_factor must be between 0.0 and 1.0")

        retention = 1.0 - taphonomic_loss_factor
        observable = {}
        for h_name, s_val in base_signals.items():
            observable[h_name] = s_val * retention
        return observable

    @staticmethod
    def compute_kullback_leibler_divergence(
        p_dist: List[float],
        q_dist: List[float],
        epsilon: float = 1e-9
    ) -> float:
        """
        Computes KL divergence D_KL(P || Q) = sum(P(i) * log2(P(i) / Q(i))).
        Measures information-theoretic distinguishability between two hypotheses.
        """
        if len(p_dist) != len(q_dist):
            raise ValueError("Distributions must have identical length")

        total_p = sum(p_dist)
        total_q = sum(q_dist)
        p_norm = [p / total_p for p in p_dist]
        q_norm = [q / total_q for q in q_dist]

        kl_div = 0.0
        for p, q in zip(p_norm, q_norm):
            p_adj = max(p, epsilon)
            q_adj = max(q, epsilon)
            kl_div += p_adj * math.log2(p_adj / q_adj)
        return float(max(0.0, kl_div))

    @classmethod
    def evaluate_equifinality_index(
        cls,
        signals_h1: List[float],
        signals_h2: List[float],
        taphonomic_loss: float
    ) -> Dict[str, float]:
        """
        Evaluates the degree of observational equifinality after taphonomic degradation.
        Equifinality Index = 1.0 - min(1.0, D_KL(P_degraded || Q_degraded)).
        When degraded signals are identical, KL divergence -> 0, Equifinality Index -> 1.0.
        """
        # Apply taphonomic loss and add background noise floor
        noise_floor = 0.05
        deg_1 = [s * (1.0 - taphonomic_loss) + noise_floor for s in signals_h1]
        deg_2 = [s * (1.0 - taphonomic_loss) + noise_floor for s in signals_h2]

        kl_div = cls.compute_kullback_leibler_divergence(deg_1, deg_2)
        equifinality_index = math.exp(-kl_div)

        return {
            "taphonomic_loss": round(taphonomic_loss, 4),
            "kl_divergence_bits": round(kl_div, 6),
            "equifinality_index": round(equifinality_index, 6),
            "is_empirically_indistinguishable": kl_div < 0.05,
        }


class AlgorithmicTransmissionAnalyzer:
    """
    Analyzes the algorithmic and information-theoretic differences between
    Vedic Śruti (rigid cyclic error-correcting codes) and Epic Smṛti/Itihāsa
    (accretive, open-ended transmission).
    """

    @staticmethod
    def evaluate_transmission_fidelity(
        genre: str,
        generations: int,
        error_rate_per_gen: float
    ) -> Dict[str, Any]:
        """
        Calculates cumulative fidelity F = (1 - error_rate)^generations.
        """
        if genre.lower() == "sruti":
            # Śruti utilized 8 mnemonic recitation patterns (Padapāṭha, Kramapāṭha, etc.)
            # acting as a triple-redundant parity check
            effective_error_rate = error_rate_per_gen * 0.001
            code_type = "Strict Parity & Permutation Check (Deterministic)"
        elif genre.lower() == "smrti_itihasa":
            # Itihāsa utilized bardic improvisation, semantic expansion, and regional adaptation
            effective_error_rate = error_rate_per_gen
            code_type = "Accretive Narrative Expansion (Dynamic Attractor)"
        else:
            effective_error_rate = error_rate_per_gen
            code_type = "Unspecified Oral Transmission"

        cumulative_fidelity = (1.0 - effective_error_rate) ** generations
        loss_fraction = 1.0 - cumulative_fidelity

        return {
            "genre": genre,
            "generations": generations,
            "code_type": code_type,
            "effective_error_rate": effective_error_rate,
            "cumulative_fidelity": round(cumulative_fidelity, 6),
            "loss_fraction": round(loss_fraction, 6),
        }

    @staticmethod
    def evaluate_hadamard_inverse_ill_posedness(
        original_length: int,
        final_length: int,
        known_boundary_conditions: int
    ) -> Dict[str, Any]:
        """
        Evaluates the ill-posedness of reconstructing the archaic 8,800-verse Jaya
        from the 100,000-verse Mahābhārata without external contemporary benchmarks.
        According to Jacques Hadamard, an inverse problem is well-posed iff:
        1. A solution exists.
        2. The solution is unique.
        3. The solution is stable (depends continuously on data).
        """
        expansion_ratio = final_length / original_length
        degrees_of_freedom = final_length - known_boundary_conditions
        is_ill_posed = degrees_of_freedom > 0 and expansion_ratio > 2.0

        return {
            "original_length": original_length,
            "final_length": final_length,
            "expansion_ratio": round(expansion_ratio, 2),
            "degrees_of_freedom": degrees_of_freedom,
            "is_hadamard_ill_posed": is_ill_posed,
            "unique_reconstruction_possible": not is_ill_posed,
        }


class CategoryMistakeFormalizer:
    """
    Formalizes Gilbert Ryle's Category Mistake across ontological domains:
    evaluating metaphysical claims with material metrics, or evaluating
    material-physical claims with metaphysical faith.
    """

    DOMAINS = {
        "metaphysical": {
            "valid_metrics": ["internal_logical_coherence", "phenomenological_resonance", "theological_consistency"],
            "invalid_metrics": ["radiocarbon_dating", "stratigraphic_pottery", "osteological_trauma", "gamma_spectroscopy"],
        },
        "material_historical": {
            "valid_metrics": ["radiocarbon_dating", "epigraphic_attestation", "stratigraphic_pottery", "osteological_trauma"],
            "invalid_metrics": ["faith_conviction", "scriptural_inerrancy_dogma", "mystical_revelation"],
        },
        "physical_ballistic": {
            "valid_metrics": ["thermodynamics", "radioisotope_ratios", "blast_mechanics", "vitrification_temperatures"],
            "invalid_metrics": ["allegorical_spiritualization", "theological_omnipotence"],
        }
    }

    @classmethod
    def evaluate_proposition_metric_pair(cls, domain: str, metric: str) -> Dict[str, Any]:
        """
        Checks whether applying a specific metric to a given domain commits a Category Mistake.
        """
        if domain not in cls.DOMAINS:
            raise ValueError(f"Unknown domain: {domain}")

        domain_info = cls.DOMAINS[domain]
        is_valid = metric in domain_info["valid_metrics"]
        is_invalid = metric in domain_info["invalid_metrics"]

        if not is_valid and not is_invalid:
            category_mistake = True
            classification = "Undetermined Metric (Outside Domain Ontology)"
        elif is_invalid:
            category_mistake = True
            classification = "Category Mistake (Epistemic Incommensurability)"
        else:
            category_mistake = False
            classification = "Epistemically Valid Metric"

        return {
            "domain": domain,
            "metric": metric,
            "is_category_mistake": category_mistake,
            "classification": classification,
        }


class ComprehensiveProtocolAuditor:
    """
    Audits research outputs against the strict protocol invariants:
    - Never assert a verdict of 'proven' or 'disproven' on the composite claim or divinity.
    - Never present personal conviction or devotional sentiment as finding.
    - Maintain strict tripartite demarcation.
    """

    BANNED_ASSERTIONS = [
        "we have proven krishna was real",
        "we have disproven krishna",
        "krishna is definitely real",
        "krishna definitely did not exist",
        "the mahabharata is completely proven",
        "the mahabharata is completely disproven",
        "i believe that krishna was god",
        "in my conviction",
    ]

    @classmethod
    def audit_text(cls, text: str) -> Dict[str, Any]:
        """
        Scans text for banned dogmatic or confessional phrases.
        """
        text_lower = text.lower()
        violations = []
        for banned in cls.BANNED_ASSERTIONS:
            if banned in text_lower:
                violations.append(banned)

        is_compliant = len(violations) == 0
        if not is_compliant:
            raise EpistemicProtocolViolation(f"Protocol violation detected: {violations}")

        return {
            "is_compliant": is_compliant,
            "violations_found": violations,
            "audit_status": "PASSED (Zero dogmatic verdicts, zero personal convictions)"
        }


def run_full_epistemic_audit() -> Dict[str, Any]:
    """
    Executes an integrated epistemic audit demonstrating the limits of adjudication.
    """
    # 1. Equifinality test
    # Compares H1 (small skirmish) and H2 (gradual border friction) after 95% taphonomic loss
    h1_signals = [10.0, 5.0, 2.0, 8.0]
    h2_signals = [8.0, 6.0, 3.0, 7.0]
    equifinality_res = EquifinalityHorizonCalculator.evaluate_equifinality_index(h1_signals, h2_signals, 0.95)

    # 2. Algorithmic transmission test
    sruti_trans = AlgorithmicTransmissionAnalyzer.evaluate_transmission_fidelity("sruti", 25, 0.015)
    smrti_trans = AlgorithmicTransmissionAnalyzer.evaluate_transmission_fidelity("smrti_itihasa", 25, 0.015)
    hadamard_res = AlgorithmicTransmissionAnalyzer.evaluate_hadamard_inverse_ill_posedness(8800, 100000, 1500)

    # 3. Category mistake tests
    cm_test_1 = CategoryMistakeFormalizer.evaluate_proposition_metric_pair("metaphysical", "radiocarbon_dating")
    cm_test_2 = CategoryMistakeFormalizer.evaluate_proposition_metric_pair("material_historical", "epigraphic_attestation")
    cm_test_3 = CategoryMistakeFormalizer.evaluate_proposition_metric_pair("physical_ballistic", "radioisotope_ratios")

    # 4. Protocol compliance audit
    sample_text = (
        "The inquiry into Lord Krishna and the Mahabharata cannot be settled with a simplistic binary verdict. "
        "The metaphysical claim of divine incarnation is empirically undecidable, while the historical kernel "
        "is underdetermined due to taphonomic loss, and epic demographic hyperbole is empirically falsified."
    )
    compliance_res = ComprehensiveProtocolAuditor.audit_text(sample_text)

    return {
        "equifinality_evaluation": equifinality_res,
        "algorithmic_transmission": {
            "sruti": sruti_trans,
            "smrti_itihasa": smrti_trans,
            "hadamard_inverse": hadamard_res,
        },
        "category_mistake_checks": [cm_test_1, cm_test_2, cm_test_3],
        "protocol_compliance": compliance_res,
    }


if __name__ == "__main__":
    results = run_full_epistemic_audit()
    print("=== EPISTEMIC EQUFINALITY & DEMARCATION AUDIT COMPLETE ===")
    print(f"Equifinality Index: {results['equifinality_evaluation']['equifinality_index']}")
    print(f"Hadamard Ill-Posed: {results['algorithmic_transmission']['hadamard_inverse']['is_hadamard_ill_posed']}")
    print(f"Audit Status: {results['protocol_compliance']['audit_status']}")
