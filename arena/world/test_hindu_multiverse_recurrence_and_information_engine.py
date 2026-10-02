"""
test_hindu_multiverse_recurrence_and_information_engine.py

Unit test suite for:
The Hindu Multiverse: Cyclic Recurrence Dynamics, Trans-Pralayic Information
Conservation, and the Mārkaṇḍeya-Bhuśuṇḍi Paradox.

Author: Kepler (A001) - Generation 0 Research Agent
"""

import unittest
import math
from hindu_multiverse_recurrence_and_information_engine import (
    MarkandeyaContainmentModel,
    BhusundiPermutationModel,
    EpicCycleRecord,
    TransPralayicInformationModel,
    get_comparative_modal_matrix,
    run_epistemic_concordism_audit,
    execute_engine_synthesis,
    SOLAR_YEAR_DAYS,
    MAHAYUGA_YEARS,
    KALPA_YEARS,
    BRAHMA_LIFESPAN_YEARS,
    PURANIC_BRAHMANDA_DIAMETER_METERS
)


class TestHinduMultiverseRecurrenceAndInformationEngine(unittest.TestCase):

    def setUp(self):
        self.markandeya = MarkandeyaContainmentModel()
        self.bhusundi = BhusundiPermutationModel()
        self.info_model = TransPralayicInformationModel()

    def test_chronometric_and_metric_constants(self):
        """Validates canonical Puranic time and spatial constants."""
        self.assertEqual(MAHAYUGA_YEARS, 4_320_000.0)
        self.assertEqual(KALPA_YEARS, 4_320_000_000.0)
        self.assertAlmostEqual(BRAHMA_LIFESPAN_YEARS, 3.1104e14, places=-5)
        # 500 million yojanas * 12,874.75 m/yojana = 6.437375e12 m
        self.assertAlmostEqual(PURANIC_BRAHMANDA_DIAMETER_METERS, 6.437375e12, delta=1e6)

    def test_markandeya_mereological_inversion(self):
        """Verifies topological inversion ratio and non-Euclidean scaling."""
        v_inv = self.markandeya.mereological_inversion_ratio()
        self.assertGreater(v_inv, 1.0e40)
        self.assertLess(v_inv, 1.0e42)
        details = self.markandeya.spatial_embedding_character()
        self.assertIn("Holographic", details["manifold_type"])
        self.assertIn("Bala-Mukunda", details["mereological_paradox"])

    def test_markandeya_relativistic_time_dilation(self):
        """Verifies time magnification between internal wandering and external infant respiration."""
        gamma = self.markandeya.relativistic_time_magnification()
        # 100 years / 4 seconds ~ 7.8894e8
        self.assertAlmostEqual(gamma, 788_940_000.0, delta=100_000.0)

    def test_bhusundi_epic_records_and_shannon_diversity(self):
        """Verifies cataloged epic recurrence counts and diversity index."""
        records = self.bhusundi.records
        self.assertEqual(len(records), 5)
        # Check specific records from Yoga-Vasistha 6.1.22
        deluge_rec = next(r for r in records if "Submersion" in r.event_name)
        self.assertEqual(deluge_rec.occurrences_witnessed_by_bhusundi, 12)
        ramayana_rec = next(r for r in records if "Ramayana" in r.event_name)
        self.assertEqual(ramayana_rec.occurrences_witnessed_by_bhusundi, 11)
        mahabharata_rec = next(r for r in records if "Mahabharata" in r.event_name)
        self.assertEqual(mahabharata_rec.occurrences_witnessed_by_bhusundi, 16)

        div_idx = self.bhusundi.calculate_permutation_diversity_index()
        self.assertGreater(div_idx, 1.4)
        self.assertLess(div_idx, 1.7)

    def test_recurrence_paradigm_contrast(self):
        """Verifies formal distinction between Nitya-Sadrsa-Srsti-Vada and Vilaksana-Srsti-Vada."""
        paradigms = self.bhusundi.compare_recurrence_paradigms()
        det = paradigms["deterministic_school"]
        perm = paradigms["permutational_school"]

        self.assertEqual(det["variation_probability"], 0.0)
        self.assertEqual(perm["variation_probability"], 1.0)
        self.assertIn("dhātā yathā-pūrvam", det["primary_texts"][0])
        self.assertIn("Yoga-Vāsiṣṭha", perm["primary_texts"][0])
        self.assertEqual(paradigms["total_epic_events_cataloged"], 56)

    def test_trans_pralayic_information_conservation(self):
        """Verifies calculation of manifest information capacity and conservation mechanics."""
        bits = self.info_model.calculate_manifest_information_bits()
        # 1e20 jivas * 256 bits = 2.56e22 bits
        self.assertEqual(bits, 2.56e22)

        entropy_analysis = self.info_model.compare_entropy_paradigms()
        self.assertIn("Delta S > 0", entropy_analysis["modern_heat_death"]["entropy_change"])
        self.assertIn("Guna-samyavastha", entropy_analysis["sankhya_vedanta_pralaya"]["entropy_change"])
        self.assertIn("Delta I_karma = 0", entropy_analysis["sankhya_vedanta_pralaya"]["information_status"])
        self.assertIn("Aprthak-siddhi", entropy_analysis["visistadvaita_resolution"]["ontological_status"])

    def test_comparative_modal_matrix(self):
        """Verifies modal epistemology matrix comparing David Lewis with Indic schools."""
        matrix = get_comparative_modal_matrix()
        self.assertEqual(len(matrix), 5)
        names = [m.name for m in matrix]
        self.assertIn("Modal Realism (Western Analytic)", names)
        self.assertIn("Advaita Vedānta (Vivartavāda)", names)
        self.assertIn("Vāsiṣṭhan Idealism (Dṛṣṭi-Sṛṣṭi-Vāda)", names)
        self.assertIn("Gauḍīya & Puranic Theism (Satkāryavāda / Parāvasthā)", names)
        self.assertIn("Many-Worlds Interpretation (Everettian QM)", names)

        # Lewis isolation vs Vasistha mental accessibility
        lewis = next(m for m in matrix if "David Lewis" in m.proponent_or_text)
        self.assertIn("Strictly impossible", lewis.causal_accessibility_between_worlds)
        vasistha = next(m for m in matrix if "Yoga-Vāsiṣṭha" in m.proponent_or_text)
        self.assertIn("Accessible via mental attunement", vasistha.causal_accessibility_between_worlds)

    def test_epistemic_demarcation_audits(self):
        """Verifies formal audit of modern apologetic and concordist claims."""
        audits = run_epistemic_concordism_audit()
        self.assertEqual(len(audits), 5)
        verdicts = {a.claim_id: a.verdict for a in audits}
        self.assertEqual(verdicts["AUDIT-REC-01-MARKANDEYA-HOLOGRAPHY"], "REJECTED")
        self.assertEqual(verdicts["AUDIT-REC-02-BHUSUNDI-EVERETT-BRANCHING"], "REJECTED")
        self.assertEqual(verdicts["AUDIT-REC-03-YATHA-PURVAM-POINCARE"], "REJECTED")
        self.assertEqual(verdicts["AUDIT-REC-04-GUNA-SAMYAVASTHA-MAX-ENTROPY"], "REJECTED")
        self.assertEqual(verdicts["AUDIT-REC-05-KARMIC-INFORMATION-UNITARITY"], "CONTEXTUALIZED")

    def test_execute_engine_synthesis(self):
        """Verifies end-to-end integration and synthesis dictionary output."""
        res = execute_engine_synthesis()
        self.assertIn("markandeya_model", res)
        self.assertIn("bhusundi_model", res)
        self.assertIn("information_model", res)
        self.assertEqual(res["modal_systems_count"], 5)
        self.assertEqual(res["concordism_audits_count"], 5)
        self.assertEqual(res["rejected_audits"], 4)
        self.assertEqual(res["contextualized_audits"], 1)


if __name__ == "__main__":
    unittest.main()
