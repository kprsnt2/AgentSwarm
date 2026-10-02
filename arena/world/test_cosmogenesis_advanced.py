"""
Unit Tests for Advanced Cosmogenesis Engine
Agent: Kepler (A001, Gen 0)
Domain: cosmogenesis (Origin of the universe)
Epistemic Class: Empirical
"""

import unittest
import math
from cosmogenesis_advanced_engine import (
    gzk_threshold_and_mean_free_path,
    penrose_entropy_and_phase_space,
    inflation_and_tcc_bounds,
    leptogenesis_davidson_ibarra_bound,
    sound_horizon_and_s8_tradeoff,
    cosmic_entropy_budget_inventory
)

class TestAdvancedCosmogenesisEngine(unittest.TestCase):

    def test_gzk_photo_pion_kinematics(self):
        """Verify GZK threshold energy and mean free path."""
        res = gzk_threshold_and_mean_free_path()
        # Mean CMB photon energy ~ 0.63 meV
        self.assertAlmostEqual(res['mean_cmb_photon_energy_eV'], 6.34e-4, delta=0.5e-4)
        # GZK threshold at mean energy ~ 1e20 eV (100 EeV)
        self.assertAlmostEqual(res['gzk_threshold_at_mean_energy_eV'], 1.07e20, delta=0.2e20)
        # GZK threshold at Wien tail ~ 4.5e19 - 5e19 eV (~50 EeV)
        self.assertAlmostEqual(res['gzk_threshold_at_wien_tail_eV'], 4.5e19, delta=1.0e19)
        # Mean free path in intergalactic space is ~3.9 Mpc (order of 1 - 20 Mpc)
        self.assertAlmostEqual(res['mean_free_path_Mpc'], 3.95, delta=0.5)
        self.assertGreater(res['mean_free_path_Mpc'], 1.0)
        self.assertLess(res['mean_free_path_Mpc'], 20.0)

    def test_penrose_entropy_and_phase_space(self):
        """Verify Penrose initial entropy and phase space volume."""
        penrose = penrose_entropy_and_phase_space()
        # Initial entropy of CMB + neutrinos ~ 10^89 to 10^90 k_B
        self.assertAlmostEqual(penrose['log10_initial_entropy'], 89.9, delta=0.5)
        # Current SMBH entropy ~ 10^104 k_B
        self.assertAlmostEqual(math.log10(penrose['current_SMBH_entropy_kB']), 104.0, delta=0.1)
        # Maximum possible Bekenstein-Hawking entropy: ~10^123 (Hubble sphere) to 10^124.4 (particle horizon)
        self.assertGreater(penrose['log10_max_entropy'], 123.0)
        self.assertLess(penrose['log10_max_entropy'], 125.0)
        # Exponent for phase space probability is ~ 10^123 - 10^124
        self.assertGreater(penrose['penrose_phase_space_exponent'], 1e123)

    def test_inflation_starobinsky_and_tcc(self):
        """Verify Starobinsky R^2 predictions and TCC swampland tension."""
        inf = inflation_and_tcc_bounds(60.0)
        # For N = 60, r ~ 12 / 3600 = 0.00333
        self.assertAlmostEqual(inf['starobinsky_r'], 0.003333, places=5)
        # n_s = 1 - 2/60 = 0.9667
        self.assertAlmostEqual(inf['starobinsky_n_s'], 0.9667, places=4)
        # Energy scale ~ 7.8e15 GeV (GUT scale)
        self.assertAlmostEqual(inf['inflationary_energy_scale_GeV'], 7.89e15, delta=0.5e15)
        # TCC maximum allowable Hubble parameter is exp(-60) * M_P ~ 1e-7 GeV
        self.assertLess(inf['tcc_max_hubble_GeV'], 1e-6)
        # Ratio of predicted H_inf to TCC max is enormous (> 10^20)
        self.assertGreater(inf['ratio_predicted_to_tcc_max'], 1e20)

    def test_leptogenesis_davidson_ibarra_bound(self):
        """Verify Davidson-Ibarra bound on right-handed neutrino mass."""
        lep = leptogenesis_davidson_ibarra_bound()
        # Minimum right-handed Majorana neutrino mass M_1 >= 10^9 GeV
        self.assertGreater(lep['davidson_ibarra_min_M1_GeV'], 1.0e9)
        self.assertLess(lep['davidson_ibarra_min_M1_GeV'], 1.0e11)
        # Minimum reheating temperature T_reh >= 10^9 GeV
        self.assertGreater(lep['min_reheating_temperature_GeV'], 1.0e9)

    def test_sound_horizon_and_s8_tradeoff(self):
        """Verify sound horizon reduction and S8 tension exacerbation."""
        res = sound_horizon_and_s8_tradeoff()
        # Required rs reduction ~ 7.8% (about 11.4 Mpc)
        self.assertAlmostEqual(res['required_rs_reduction_percent'], 7.78, delta=0.2)
        self.assertAlmostEqual(res['required_rs_reduction_Mpc'], 11.45, delta=0.5)
        # EDE exacerbates the tension with cosmic shear (from ~3.9 sigma to > 5 sigma)
        self.assertGreater(res['ede_lensing_tension_sigma'], res['lcdm_lensing_tension_sigma'])
        self.assertGreater(res['ede_lensing_tension_sigma'], 4.5)

    def test_cosmic_entropy_budget_hierarchy(self):
        """Verify the monotonic hierarchical ordering of cosmic entropy components."""
        budget = cosmic_entropy_budget_inventory()
        self.assertEqual(len(budget), 8)
        
        # Verify that SMBH entropy exceeds stellar BH entropy, which exceeds CMB entropy
        entropies = {item['component']: item['entropy_kB'] for item in budget}
        self.assertGreater(entropies['Supermassive Black Holes (SMBHs)'], entropies['Stellar Mass Black Holes'])
        self.assertGreater(entropies['Stellar Mass Black Holes'], entropies['CMB Photons'])
        self.assertGreater(entropies['CMB Photons'], entropies['Dark Matter'])
        self.assertGreater(entropies['Dark Matter'], entropies['Baryons (Gas & Stars)'])
        self.assertGreater(entropies['Cosmic Event Horizon (de Sitter)'], entropies['Supermassive Black Holes (SMBHs)'])

if __name__ == '__main__':
    unittest.main()
