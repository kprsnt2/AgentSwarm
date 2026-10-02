"""
test_hindu_multiverse_definitive_corpus_ontology_and_meta_synthesis_engine.py

Unit test verification suite for hindu_multiverse_definitive_corpus_ontology_and_meta_synthesis_engine.py.
Author: Kepler (A001) - Generation 0 Research Agent
"""

import unittest
import math
from hindu_multiverse_definitive_corpus_ontology_and_meta_synthesis_engine import (
    IndraAndAntsParableEngine,
    CorpusMultiverseOntology,
    HermeneuticVectorsOfMultiverse,
    ConcordismDemarcationEngine,
    FalsificationProtocolEngine,
    execute_definitive_multiverse_synthesis,
    MAHAYUGA_YEARS,
    KALPA_YEARS,
    BRAHMA_LIFESPAN_YEARS,
    INDRAS_PER_BRAHMA_LIFESPAN
)

class TestDefinitiveMultiverseEngine(unittest.TestCase):

    def test_canonical_chronometric_constants(self):
        """Verify the exact canonical Puranic time scaling formulas."""
        self.assertAlmostEqual(MAHAYUGA_YEARS, 4_320_000.0)
        self.assertAlmostEqual(KALPA_YEARS, 4_320_000_000.0)
        self.assertAlmostEqual(BRAHMA_LIFESPAN_YEARS, 3.1104e14)
        self.assertEqual(INDRAS_PER_BRAHMA_LIFESPAN, 504_000)

    def test_indra_and_ants_kinetics(self):
        """Verify calculations for the ant column karmic history."""
        ant_count = 700
        sim = IndraAndAntsParableEngine.calculate_ant_column_karmic_history(ant_count)
        self.assertEqual(sim["ant_count"], 700)
        self.assertEqual(sim["former_indras_count"], 700)
        self.assertEqual(sim["kalpas_represented"], 50.0)  # 700 / 14 = 50 Kalpas
        self.assertGreater(sim["total_solar_years_of_reign"], 1e11)
        self.assertGreater(sim["ratio_to_modern_universe_age"], 1.0)

    def test_sage_lomesa_lifespan(self):
        """Verify Sage Lomeśa's chest-hair lifespan calculation."""
        hairs = 100_000
        sim = IndraAndAntsParableEngine.calculate_sage_lomesa_lifespan(hairs)
        expected_lifespan = hairs * BRAHMA_LIFESPAN_YEARS
        self.assertAlmostEqual(sim["total_lomesa_lifespan_years"], expected_lifespan)
        self.assertEqual(sim["total_brahmas_witnessed"], 100_000)
        self.assertEqual(sim["total_indras_witnessed"], 100_000 * 504_000)
        self.assertGreater(sim["ratio_to_modern_universe_age"], 1e9)

    def test_recursive_sage_hierarchy(self):
        """Verify the exponential tower of trans-cosmic sages."""
        tiers = IndraAndAntsParableEngine.calculate_recursive_sage_hierarchy(3, 100_000)
        self.assertEqual(len(tiers), 3)
        self.assertEqual(tiers[0]["tier"], 1)
        self.assertAlmostEqual(tiers[0]["lifespan_years"], 3.1104e14)
        self.assertAlmostEqual(tiers[1]["lifespan_years"], 3.1104e19)
        self.assertAlmostEqual(tiers[2]["lifespan_years"], 3.1104e24)

    def test_soteriological_humiliation_index(self):
        """Verify the SHI monotonic increase and ego reduction."""
        shi_low = IndraAndAntsParableEngine.soteriological_humiliation_index(1.0, 1.0)
        self.assertEqual(shi_low["soteriological_humiliation_index"], 0.0)
        self.assertEqual(shi_low["ego_retention_fraction"], 1.0)

        shi_high = IndraAndAntsParableEngine.soteriological_humiliation_index(1e14, 504_000)
        self.assertGreater(shi_high["soteriological_humiliation_index"], 0.90)
        self.assertLess(shi_high["ego_retention_fraction"], 0.10)

    def test_eighteen_mahapuranas_audit(self):
        """Verify all 18 Mahāpurāṇas are classified with correct attributes."""
        audit = CorpusMultiverseOntology.get_eighteen_mahapuranas_audit()
        self.assertEqual(len(audit), 18)
        
        # Verify key canonical parallel-affirming Purāṇas
        self.assertTrue(audit["Bhāgavata Purāṇa"]["parallel_bubbles"])
        self.assertTrue(audit["Brahma-vaivarta Purāṇa"]["parallel_bubbles"])
        self.assertTrue(audit["Padma Purāṇa"]["parallel_bubbles"])
        self.assertTrue(audit["Śiva Purāṇa"]["parallel_bubbles"])
        
        # Verify key serial/monocosm Purāṇas
        self.assertFalse(audit["Brahma Purāṇa"]["parallel_bubbles"])
        self.assertFalse(audit["Varāha Purāṇa"]["parallel_bubbles"])

    def test_tradition_comparative_matrix(self):
        """Verify cross-darśanic comparative stances."""
        matrix = CorpusMultiverseOntology.get_tradition_comparative_matrix()
        self.assertIn("Pūrva Mīmāṁsā (Kumārila Bhaṭṭa)", matrix)
        self.assertFalse(matrix["Pūrva Mīmāṁsā (Kumārila Bhaṭṭa)"]["multiverse_present"])
        self.assertIn("na kadācid anīdṛśaṁ jagat", matrix["Pūrva Mīmāṁsā (Kumārila Bhaṭṭa)"]["mechanism"])

        self.assertFalse(matrix["Astronomical Siddhāntas (Āryabhaṭa, Brahmagupta)"]["multiverse_present"])
        self.assertTrue(matrix["High Puranic (Bhāgavata, Brahma-vaivarta)"]["multiverse_present"])

    def test_four_hermeneutic_vectors(self):
        """Verify the structural definition of the four hermeneutic vectors."""
        vectors = HermeneuticVectorsOfMultiverse.get_four_vectors()
        self.assertEqual(len(vectors), 4)
        for name, v in vectors.items():
            self.assertIn("primary_function", v)
            self.assertIn("canonical_texts", v)

    def test_concordism_demarcation_metrics(self):
        """Verify mathematical divergence between Puranic and modern physical metrics."""
        metrics = ConcordismDemarcationEngine.compare_metrics()
        self.assertIn("Spatial Scale (Diameter)", metrics)
        self.assertIn("Time Scale (Universal Duration)", metrics)
        
        spatial = metrics["Spatial Scale (Diameter)"]
        self.assertGreater(spatial["ratio_modern_to_puranic"], 1e6)

    def test_concordist_fallacy_evaluations(self):
        """Verify evaluation of common apologetic concordist fallacies."""
        rv = ConcordismDemarcationEngine.evaluate_concordist_fallacy("rigveda_many_worlds")
        self.assertIn("yathāpūrvam", rv["philological_truth"])
        self.assertIn("Category Error", rv["epistemic_violation"])

        indra = ConcordismDemarcationEngine.evaluate_concordist_fallacy("indra_ants_quantum_multiverse")
        self.assertIn("mada-bhaṅga", indra["philological_truth"])

    def test_falsification_criteria(self):
        """Verify all falsification conditions and audit integrity."""
        criteria = FalsificationProtocolEngine.get_falsification_criteria()
        self.assertGreaterEqual(len(criteria), 4)
        audit = FalsificationProtocolEngine.run_falsification_audit()
        self.assertTrue(audit["all_unfalsified"])
        self.assertEqual(audit["epistemic_integrity_score"], 1.0)

    def test_master_pipeline_execution(self):
        """Verify end-to-end execution of definitive synthesis."""
        res = execute_definitive_multiverse_synthesis()
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["eighteen_puranas_breakdown"]["total_mahapuranas"], 18)
        self.assertGreater(res["eighteen_puranas_breakdown"]["affirming_parallel_bubbles"], 9)

if __name__ == "__main__":
    unittest.main()
