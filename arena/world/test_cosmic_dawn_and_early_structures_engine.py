"""
Unit Test Suite for Cosmic Dawn, Early Structure Formation, and Primordial Physical Discrepancies Engine
Agent: Kepler (A001) | Generation: 0 | Domain: Origin of the Universe (Cosmogenesis)
"""

import unittest
import math
from cosmic_dawn_and_early_structures_engine import (
    calculate_cmb_thermodynamics,
    evaluate_bbn_lithium_anomaly,
    sound_horizon_and_early_dark_energy_shift,
    jwst_highz_galaxy_overdensity,
    cosmic_dawn_21cm_temperature_anomaly,
    inflationary_non_gaussianity_bounds,
    relic_neutrino_effective_dof,
    primordial_magnetic_field_void_bounds,
    compile_master_cosmic_dawn_registry,
    T_CMB_0,
    H0_CMB,
    H0_LOCAL,
    N_EFF_SM,
)


class TestCosmicDawnAndEarlyStructuresEngine(unittest.TestCase):
    def test_cmb_thermodynamics(self):
        res = calculate_cmb_thermodynamics()
        self.assertAlmostEqual(res["T0_kelvin"], 2.72548, places=4)
        # Relic photon density must be ~410.7 cm^-3
        self.assertGreater(res["n_gamma_cm3"], 405.0)
        self.assertLess(res["n_gamma_cm3"], 415.0)
        # Baryon-to-photon ratio eta must be in (6.0 - 6.2)e-10
        self.assertGreater(res["eta_baryon_photon"], 5.9e-10)
        self.assertLess(res["eta_baryon_photon"], 6.3e-10)

    def test_bbn_lithium_tension(self):
        res = evaluate_bbn_lithium_anomaly()
        # Primordial mass fractions: ~75% H, ~25% He
        self.assertAlmostEqual(res["helium_4_mass_fraction"], 0.245, places=3)
        self.assertAlmostEqual(res["hydrogen_1_mass_fraction"], 0.755, places=3)
        # Tension between BBN 7Li theory (4.68e-10) and Spite plateau (1.58e-10)
        self.assertGreater(res["z_score_tension"], 8.0)
        self.assertGreater(res["discrepancy_ratio"], 2.8)

    def test_sound_horizon_and_ede(self):
        res = sound_horizon_and_early_dark_energy_shift()
        # Hubble tension significance must exceed 4.8 sigma
        self.assertGreater(res["h0_tension_sigma"], 4.8)
        # Sound horizon must shrink by ~11.37 Mpc (~7.7%)
        self.assertLess(res["delta_rs_mpc"], -10.0)
        self.assertGreater(res["delta_rs_mpc"], -13.0)
        self.assertGreater(res["percentage_reduction"], 7.0)
        self.assertLess(res["percentage_reduction"], 8.5)
        # EDE must exacerbate KiDS S8 tension
        self.assertGreater(res["s8_kids_tension_ede_sigma"], res["s8_kids_tension_planck_sigma"])

    def test_jwst_highz_peaks(self):
        res = jwst_highz_galaxy_overdensity(redshift=10.0, m_star_msun=10**10.5)
        self.assertGreater(res["m_halo_req_msun"], 1.5e11)
        # Peak significance nu > 6 sigma
        self.assertGreater(res["nu_peak_significance"], 6.0)
        # Highly suppressed Gaussian probability
        self.assertLess(res["log10_gaussian_probability"], -9.0)

    def test_cosmic_dawn_21cm(self):
        res = cosmic_dawn_21cm_temperature_anomaly()
        self.assertAlmostEqual(res["t_cmb_k"], 49.60, delta=0.1)
        # Standard adiabatic floor cannot exceed ~ -250 mK
        self.assertGreater(res["delta_tb_standard_min_mk"], -250.0)
        self.assertLess(res["delta_tb_standard_min_mk"], -200.0)
        # EDGES observed is -500 mK
        self.assertEqual(res["delta_tb_edges_obs_mk"], -500.0)
        # Discrepancy factor > 2
        self.assertGreater(res["discrepancy_factor"], 2.0)

    def test_inflation_non_gaussianity(self):
        res = inflationary_non_gaussianity_bounds()
        # Maldacena consistency bound gives ~0.015 for single field
        self.assertAlmostEqual(res["fnl_local_single_field_maldacena"], 0.0146, places=3)
        # SPHEREx can discriminate f_NL = 1 at 2 sigma
        self.assertGreater(res["discrimination_margin_sigma"], 1.8)

    def test_relic_neutrinos(self):
        res = relic_neutrino_effective_dof()
        self.assertAlmostEqual(res["n_eff_standard_model"], 3.044, places=3)
        # CMB-S4 forecast precision 0.03
        self.assertEqual(res["cmbs4_forecast_sigma"], 0.03)
        # Minimal scalar relic gives Delta N_eff ~ 0.027
        self.assertAlmostEqual(res["minimal_scalar_thermal_relic_shift"], 0.027, places=3)

    def test_primordial_magnetic_fields(self):
        res = primordial_magnetic_field_void_bounds()
        self.assertEqual(res["pmf_min_void_gauss"], 1e-16)
        self.assertAlmostEqual(res["pmf_max_cmb_gauss"], 8e-10)
        self.assertGreater(res["orders_of_magnitude_window"], 6.0)

    def test_master_registry_compilation(self):
        reg = compile_master_cosmic_dawn_registry()
        self.assertIn("cmb_thermodynamics", reg)
        self.assertIn("bbn_lithium", reg)
        self.assertIn("sound_horizon_ede", reg)
        self.assertIn("jwst_highz", reg)
        self.assertIn("cosmic_dawn_21cm", reg)
        self.assertIn("inflation_non_gaussianity", reg)
        self.assertIn("relic_neutrinos", reg)
        self.assertIn("primordial_magnetic_fields", reg)


if __name__ == "__main__":
    unittest.main()
