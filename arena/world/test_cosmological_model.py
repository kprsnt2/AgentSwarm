"""
Unit and Consistency Verification Suite for Cosmological Engine
Agent: Kepler (A001, Gen 0)
Domain: cosmogenesis (Origin of the universe)
Epistemic Class: Empirical
"""

import unittest
import math
from cosmological_model import (
    T_CMB_FIXSEN,
    H0_PLANCK,
    H0_SHOES,
    Y_P_MEASURED,
    cmb_thermodynamics,
    bbn_freezeout_and_abundances,
    hubble_tension_significance,
    lithium7_anomaly_significance,
    flrw_expansion_rate,
    cmb_horizon_problem_quantification,
    flatness_problem_finetuning
)

class TestCosmologicalFoundations(unittest.TestCase):

    def test_cmb_ground_truth(self):
        """Verify CMB temperature matches COBE/FIRAS ground truth (2.725 K)."""
        cmb = cmb_thermodynamics(T_CMB_FIXSEN)
        # Ground truth: T = 2.725 K
        self.assertAlmostEqual(cmb['temperature_K'], 2.72548, places=3)
        # Ground truth: Photon density ~ 411 photons / cm^3
        self.assertAlmostEqual(cmb['photon_density_cm3'], 410.7, delta=1.0)
        # Peak frequency in microwave band ~ 160 GHz
        self.assertAlmostEqual(cmb['peak_frequency_GHz'], 160.2, delta=1.0)
        # Peak wavelength ~ 1.06 mm
        self.assertAlmostEqual(cmb['peak_wavelength_mm'], 1.063, delta=0.01)

    def test_bbn_primordial_abundances_ground_truth(self):
        """Verify primordial nucleosynthesis produces ~75% H, ~25% He-4 by mass."""
        bbn = bbn_freezeout_and_abundances()
        
        # Ground truth: Primordial helium-4 mass fraction Y_p ~ 0.25 (25%)
        self.assertAlmostEqual(bbn['Y_p_helium4_mass_fraction'], 0.25, delta=0.01)
        # Ground truth: Primordial hydrogen mass fraction X ~ 0.75 (75%)
        self.assertAlmostEqual(bbn['X_hydrogen_mass_fraction'], 0.75, delta=0.01)
        
        # Sum of fractions must be exactly 1.0
        self.assertAlmostEqual(
            bbn['Y_p_helium4_mass_fraction'] + bbn['X_hydrogen_mass_fraction'],
            1.0,
            places=7
        )
        
        # Consistent with observational baseline Y_p = 0.245 +- 0.003
        self.assertAlmostEqual(bbn['Y_p_helium4_mass_fraction'], Y_P_MEASURED, delta=0.01)

    def test_hubble_tension_ground_truth(self):
        """Verify Hubble tension between local ~73 km/s/Mpc and CMB ~67.4 km/s/Mpc."""
        ht = hubble_tension_significance()
        
        # Ground truths
        self.assertAlmostEqual(ht['H0_early_km_s_Mpc'], 67.4, delta=0.1)
        self.assertAlmostEqual(ht['H0_late_km_s_Mpc'], 73.0, delta=0.1)
        
        # Difference ~ 5.68 km/s/Mpc
        self.assertAlmostEqual(ht['delta_H0'], 5.68, places=2)
        
        # Statistical tension must be near or above 4.8 sigma (~5 sigma)
        self.assertGreater(ht['tension_significance_sigma'], 4.5)
        self.assertLess(ht['tension_significance_sigma'], 5.5)

    def test_lithium7_anomaly(self):
        """Verify the cosmological lithium problem discrepancy factor and significance."""
        li7 = lithium7_anomaly_significance()
        # Discrepancy factor of ~3 between standard BBN prediction and observation
        self.assertAlmostEqual(li7['ratio_prediction_to_observation'], 2.96, delta=0.2)
        # Discrepancy exceeds 5 sigma (empirically > 8 sigma)
        self.assertGreater(li7['discrepancy_sigma'], 5.0)

    def test_horizon_problem_causal_disconnection(self):
        """Verify CMB horizon problem: causal patches at recombination ~ 1 degree (~10^4 patches)."""
        hp = cmb_horizon_problem_quantification()
        # Horizon angle subtended at z ~ 1090 is approximately 1.0 - 1.3 degrees
        self.assertAlmostEqual(hp['angular_scale_horizon_degrees'], 1.17, delta=0.2)
        # Number of causally disconnected regions without inflation is on the order of 10^4
        self.assertGreater(hp['number_of_causally_disconnected_patches'], 5000)
        self.assertLess(hp['number_of_causally_disconnected_patches'], 20000)

    def test_flatness_finetuning(self):
        """Verify flatness problem requires extreme fine-tuning without inflation."""
        fp = flatness_problem_finetuning()
        # Divergence growth from Planck epoch exceeds 10^50
        self.assertGreater(fp['total_divergence_growth'], 1e50)
        # Required fine-tuning |1 - Omega| < 10^-60
        self.assertLess(fp['required_finetuning_at_planck_epoch'], 1e-60)

    def test_flrw_expansion_monotonicity(self):
        """Verify H(z) increases monotonically with redshift."""
        h0 = flrw_expansion_rate(0.0)
        h1 = flrw_expansion_rate(1.0)
        h10 = flrw_expansion_rate(10.0)
        h1100 = flrw_expansion_rate(1100.0)
        
        self.assertGreater(h1, h0)
        self.assertGreater(h10, h1)
        self.assertGreater(h1100, h10)

if __name__ == '__main__':
    unittest.main()
