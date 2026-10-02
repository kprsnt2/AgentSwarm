"""
Unit and Consistency Tests for Relativistic Flight and Causality Models
Agent: Kepler (A001, Gen 0)
"""

import unittest
import math
from relativity_calculator import (
    c, g, m_p, ly_meters,
    lorentz_factor, kinetic_energy_per_kg,
    rocket_mass_ratio, brachistochrone_trajectory,
    beamed_laser_sail, ism_hazards,
    tachyonic_antitelephone_exact
)

class TestRelativisticPhysics(unittest.TestCase):

    def test_lorentz_factor(self):
        # Established ground truth check: v = 0.99c -> gamma ~ 7.0888
        gamma_99 = lorentz_factor(0.99)
        self.assertAlmostEqual(gamma_99, 7.088812, places=4)
        
        # Ground truth check: energy to accelerate 1 kg to 0.99c is ~5.5e17 J
        ke_1kg = kinetic_energy_per_kg(0.99)
        self.assertAlmostEqual(ke_1kg / 1e17, 5.4723, places=2)

    def test_rocket_equation_limits(self):
        # Antimatter ideal photon rocket beta_e = 1.0
        # Boost to 0.9c: sqrt((1+0.9)/(1-0.9)) = sqrt(19) = 4.3588989
        r_photon_09 = rocket_mass_ratio(0.9, 1.0, burns=1)
        self.assertAlmostEqual(r_photon_09, math.sqrt(19.0), places=5)
        
        # Brachistochrone (accel + decel): (sqrt(19))^2 = 19.0
        r_photon_09_brach = rocket_mass_ratio(0.9, 1.0, burns=2)
        self.assertAlmostEqual(r_photon_09_brach, 19.0, places=5)
        
        # Fusion rocket (beta_e = 0.05) to 0.9c
        # Mass ratio = 19^(1 / (2*0.05)) = 19^10 = 6.131e12
        r_fusion_09 = rocket_mass_ratio(0.9, 0.05, burns=1)
        self.assertAlmostEqual(r_fusion_09, 19.0**10, places=-5)
        
        # Accel + Decel fusion 0.9c = 19^20 = 3.759e25 kg
        r_fusion_09_brach = rocket_mass_ratio(0.9, 0.05, burns=2)
        self.assertAlmostEqual(r_fusion_09_brach, 19.0**20, places=-15)

    def test_brachistochrone_kinematics(self):
        # 1-g trip to Proxima Centauri (4.246 ly)
        traj = brachistochrone_trajectory(4.246)
        # Expected proper time ~3.54 years, Earth time ~5.87 years
        self.assertAlmostEqual(traj['crew_time_years'], 3.542, places=2)
        self.assertAlmostEqual(traj['earth_time_years'], 5.872, places=2)
        self.assertTrue(traj['peak_beta'] < 1.0)
        self.assertAlmostEqual(traj['peak_beta'], 0.9496, places=3)

    def test_ism_proton_energies(self):
        # Ground truth: at 0.9c, ISM is lethal particle flux
        ism_09 = ism_hazards(0.9, n_cm3=1.0)
        # Proton rest mass ~938.272 MeV; gamma ~ 2.294 -> KE = (2.294-1)*0.938 ~ 1.214 GeV
        self.assertAlmostEqual(ism_09['proton_ke_GeV'], 1.214, places=2)
        # Power flux > 50 kW/m^2
        self.assertAlmostEqual(ism_09['power_flux_kW_m2'], 52.49, places=1)

    def test_tachyonic_antitelephone_causality(self):
        # Threshold formula: v_th = 2 * U / (U^2 + 1)
        # For U = 2.0c: v_th = 4 / 5 = 0.8c
        res_sub = tachyonic_antitelephone_exact(2.0, 0.5)
        self.assertFalse(res_sub['is_causality_violated'])
        self.assertGreater(res_sub['delta_t'], 0)
        
        res_super = tachyonic_antitelephone_exact(2.0, 0.9)
        self.assertTrue(res_super['is_causality_violated'])
        self.assertLess(res_super['delta_t'], 0)
        # Arrives at t3 = 62.81 s, emission was at 100.0 s
        self.assertAlmostEqual(res_super['t3'], 62.81, places=1)

if __name__ == '__main__':
    unittest.main()
