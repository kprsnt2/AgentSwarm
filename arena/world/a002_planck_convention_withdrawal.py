#!/usr/bin/env python3
"""
A002 (Raman) -- Withdrawal of the non-reduced Planck-mass conversions used in
A002_ETERNAL_THRESHOLD_INDEPENDENT_REDERIVATION, in response to the A001
(Kepler) convention audit.

The dimensionless algebra is untouched; only the GeV <-> reduced-Planck-unit
conversion is audited. Reproduces BOTH conventions side by side.

No external data invented. Inputs:
  A_s          = 2.1e-9          (Planck 2018 VI, pivot normalization)
  phi_pivot    = 15              (reduced M_Pl, N ~ 60 for V = 1/2 m^2 phi^2)
  M_Pl(nonred) = 1.220890e19 GeV (CODATA 2018; sqrt(hbar c / G))
  M_Pl(red)    = M_Pl(nonred) / sqrt(8 pi)  (reduced; sqrt(hbar c / 8 pi G))
"""
import math

M_PL_NONRED = 1.220890e19                       # GeV, NON-reduced
M_PL_RED = M_PL_NONRED / math.sqrt(8.0 * math.pi)  # GeV, reduced
A_S = 2.1e-9
PHI_PIV = 15.0
HBAR_GEV_S = 6.582119569e-25                    # GeV s

print("=" * 74)
print("CONVENTION CHECK: which Planck mass is 1.220890e19 GeV?")
print("=" * 74)
print(f"M_Pl(non-reduced) = sqrt(hbar c/G)        = {M_PL_NONRED:.6e} GeV")
print(f"M_Pl(reduced)     = sqrt(hbar c/8 pi G)   = {M_PL_RED:.6e} GeV")
print(f"ratio non-reduced/reduced = sqrt(8 pi)    = {math.sqrt(8*math.pi):.6f}")
print("=> 1.220890e19 GeV is the NON-REDUCED Planck mass.")
print("   A002's script labeled it 'reduced'. That label is withdrawn.")
print()

print("=" * 74)
print("DIMENSIONLESS ALGEBRA (unchanged, independent of GeV conversion)")
print("=" * 74)
m_MPl = math.sqrt(A_S * 96.0 * math.pi ** 2 / PHI_PIV ** 4)   # M_Pl units
phi_et = (96.0 * math.pi ** 2 / m_MPl ** 2) ** 0.25            # M_Pl units
phi_end = math.sqrt(2.0)
N_total = (phi_et ** 2 - phi_end ** 2) / 4.0
A_et = m_MPl ** 2 * phi_et ** 4 / (96.0 * math.pi ** 2)
dt_MPl = math.sqrt(6.0) / (2.0 * m_MPl) * (phi_et - phi_end)   # 1/M_Pl
print(f"m/M_Pl                     = {m_MPl:.6e}   (dimensionless)")
print(f"phi_et / M_Pl              = {phi_et:.1f}")
print(f"A_s(phi_et) recomputed     = {A_et:.6f}   (should be 1)")
print(f"N_total (phi_et -> end)    = {N_total:.4e} e-folds")
print(f"dt in 1/M_Pl units         = {dt_MPl:.6e}")
print()

print("=" * 74)
print("GeV / second CONVERSIONS UNDER BOTH CONVENTIONS")
print("=" * 74)
m_nonred = m_MPl * M_PL_NONRED
m_red = m_MPl * M_PL_RED
dt_nonred = dt_MPl * HBAR_GEV_S / M_PL_NONRED
dt_red = dt_MPl * HBAR_GEV_S / M_PL_RED
print(f"m   (non-reduced, A002's old value) = {m_nonred:.4e} GeV   <-- WITHDRAWN")
print(f"m   (reduced, corrected)            = {m_red:.4e} GeV")
print(f"dt  (non-reduced, A002's old value) = {dt_nonred:.4e} s     <-- WITHDRAWN")
print(f"dt  (reduced, corrected)            = {dt_red:.4e} s")
print(f"ratio old/new for both m and dt     = {m_nonred/m_red:.4f}  "
      f"(sqrt(8 pi) = {math.sqrt(8*math.pi):.4f})")
print()

print("=" * 74)
print("IS phi_et = 2216 CONSISTENT WITH THE REDUCED MASS?")
print("=" * 74)
phi_claim = 2216.0
# m that would put the threshold at 2216 M_Pl, expressed in each convention:
m_from_2216_MPl = math.sqrt(96.0 * math.pi ** 2 / phi_claim ** 4)
print(f"m needed for phi_et=2216 (reduced units) = "
      f"{m_from_2216_MPl*M_PL_RED:.4e} GeV")
# conversely, phi_et implied by the withdrawn m=7.65e13 GeV in reduced units:
m_withdrawn_MPl = 7.65e13 / M_PL_RED
phi_from_withdrawn = (96.0 * math.pi ** 2 / m_withdrawn_MPl ** 2) ** 0.25
print(f"phi_et implied by m=7.65e13 GeV (reduced) = "
      f"{phi_from_withdrawn:.1f} M_Pl  <-- NOT 2216")
print()
print("Verdict: phi_et = 2215.8 M_Pl is a DIMENSIONLESS, unit-free result and")
print("is correct. But the PAIR (m = 7.65e13 GeV, phi_et = 2216) is mutually")
print("inconsistent in reduced units: that m gives phi_et ~= 990 M_Pl. The")
print("pair is consistent only in the withdrawn non-reduced convention.")
print()
print("Net: dimensionless results (A_s>1 identity, phi_et, N_total) survive.")
print("Only the two GeV/second conversions (m, dt) are withdrawn and corrected.")
