#!/usr/bin/env python3
"""
A001 (Kepler) -- Planck-mass convention audit (answering Raman/A002) and an
attack on the weakest assumption in A001's finite-vs-eternal artifact.

Published-only inputs:
  A_s = 2.1e-9            Planck 2018 VI pivot normalization
  phi_pivot = 15 M_Pl     reduced units, N ~ 56-60 for V = 1/2 m^2 phi^2
  reduced M_Pl   = 2.435e18 GeV
  non-reduced M  = 1.220890e19 GeV  (often just called "the Planck mass")
"""
import math

A_S = 2.1e-9
PHI_PIVOT = 15.0                  # reduced Planck units
M_PL_RED = 2.435e18               # reduced Planck mass, GeV
M_PL_NONRED = 1.220890e19         # non-reduced Planck mass, GeV
GEV_INV_S = 1.519267447e24        # 1 GeV = 1.519267e24 s^-1
S_PER_GEV_INV = 1.0 / GEV_INV_S   # 6.582e-25 s per GeV^-1
GYR_S = 3.15576e16

print("=" * 74)
print("PART 1 -- Planck-mass convention audit (answers Raman's direct message)")
print("=" * 74)

# V = 1/2 m^2 phi^2, eps = 2 M_Pl^2/phi^2
# A_s = V/(24 pi^2 eps M_Pl^4) = m^2 phi^4 / (96 pi^2 M_Pl^6)
# => in reduced units (M_Pl=1): A_s = m^2 phi^4/(96 pi^2)
m_ru = math.sqrt(A_S * 96.0 * math.pi ** 2 / PHI_PIVOT ** 4)   # reduced units
print(f"m in reduced units (M_Pl=1)      = {m_ru:.6e}")
print(f"m with reduced    M_Pl={M_PL_RED:.4e} GeV = {m_ru*M_PL_RED:.4e} GeV")
print(f"m with non-reduced M={M_PL_NONRED:.4e} GeV = {m_ru*M_PL_NONRED:.4e} GeV")
print(f"ratio non-reduced/reduced        = {M_PL_NONRED/M_PL_RED:.5f}")
print(f"sqrt(8*pi)                       = {math.sqrt(8*math.pi):.5f}")
print("  -> Raman's script sets M_PL_GEV = 1.220890e19 and labels it 'reduced',")
print("     but that is the NON-reduced Planck mass. His algebra uses M_Pl=1,")
print("     which is the reduced convention. Hence m is too large by sqrt(8 pi).")

# Threshold phi_et is independent of the numerical M_Pl used, because it is
# fixed purely by A_s and phi_pivot in reduced units:
phi_et = PHI_PIVOT / A_S ** 0.25
print(f"\nphi_et = 15 / A_s^(1/4)          = {phi_et:.1f} M_Pl (reduced units)")
print(f"physical phi_et (reduced M_Pl)   = {phi_et*M_PL_RED:.4e} GeV")
# verify A_s(phi_et)=1 with the reduced-unit m
print(f"A_s(phi_et) recomputed           = "
      f"{m_ru**2*phi_et**4/(96*math.pi**2):.6f}  (must be 1)")

# The field value phi_et is NOT implied by a GeV mass: it is 15/A_s^(1/4) in
# whatever unit system one adopts. Show the inconsistency in Raman's claim:
m_ram = m_ru * M_PL_NONRED
# If m=7.65e13 GeV and reduced M_Pl, phi_et would be:
phi_et_from_ram = (96*math.pi**2*M_PL_RED**6 / m_ram**2) ** 0.25 / M_PL_RED
print(f"\nIf m = {m_ram:.3e} GeV with reduced M_Pl, then phi_et = "
      f"{phi_et_from_ram:.1f} M_Pl")
print(f"Raman states phi_et = 2216 M_Pl together with m = 7.65e13 GeV:")
print("  -> those two are mutually inconsistent (they differ by 15/A_s^(1/4) vs")
print("     the m-implied value); his phi_et is the one from m = 1.53e13 GeV.")

print()
print("=" * 74)
print("PART 2 -- Duration audit: same convention error explains the 5x")
print("=" * 74)
# Exact quadratic duration, threshold -> end of slow roll (phi_end = sqrt2 M_Pl):
#   dN/dphi = -phi/2 ; H = m phi / sqrt(6)  =>  dt = (sqrt(6)/(2 m)) dphi
phi_end = math.sqrt(2.0)
dt_ru = math.sqrt(6.0) * (phi_et - phi_end) / (2.0 * m_ru)   # units 1/M_Pl

def to_seconds(dt_ru, M_pl_gev):
    return dt_ru / M_pl_gev * S_PER_GEV_INV

dt_correct = to_seconds(dt_ru, M_PL_RED)
dt_ram = to_seconds(dt_ru, M_PL_NONRED)
print(f"dt (threshold -> end), reduced M_Pl    = {dt_correct:.4e} s  [A001 artifact]")
print(f"dt (threshold -> end), non-reduced M   = {dt_ram:.4e} s  [Raman]")
print(f"ratio                                  = {dt_correct/dt_ram:.5f} "
      f"(= sqrt(8 pi) = {math.sqrt(8*math.pi):.5f})")
print("  -> the two artifacts agree once the Planck mass is correct; the 5x is")
print("     entirely the convention error, not a physical disagreement.")

print()
print("=" * 74)
print("PART 3 -- WEAKEST ASSUMPTION: 'the entire self-reproducing field range'")
print("=" * 74)
print("For V = 1/2 m^2 phi^2, A_s(local) = m^2 phi^4/(96 pi^2 M_Pl^6) INCREASES")
print("with phi. Self-reproduction (A_s(local)>1) holds for phi > phi_et.")
print(f"  A_s at phi_end = sqrt2 M_Pl : {m_ru**2*phi_end**4/(96*math.pi**2):.3e}")
print(f"  A_s at phi_et              : 1.0")
print("So the segment [phi_end, phi_et] is the NON-self-reproducing last roll.")
print("A001's 1.17e-34 s is the traversal time of THAT bounded segment, not of")
print("the self-reproducing range, which is [phi_et, infinity). Mislabel.")

# Classical traversal time from an arbitrary start phi_0 > phi_et:
#   dt(phi_0) = sqrt(6)(phi_0 - phi_end)/(2 m)  -> grows linearly, diverges.
def dt_from_phi0(phi0):
    return to_seconds(math.sqrt(6.0)*(phi0 - phi_end)/(2.0*m_ru), M_PL_RED)

t_age = 13.8 * GYR_S
# invert for phi_0 that gives a 13.8 Gyr pre-reheating epoch
phi0_age = 2.0*m_ru*(t_age/S_PER_GEV_INV*M_PL_RED)/math.sqrt(6.0) + phi_end
print(f"\nClassical traversal time from phi_0 to end:")
print(f"  dt(phi_0) = sqrt(6)(phi_0 - phi_end)/(2m)  -- linear in phi_0")
print(f"  phi_0 for dt = 13.8 Gyr : {phi0_age:.3e} M_Pl "
      f"= {phi0_age*M_PL_RED:.3e} GeV")
print(f"  dt at phi_0 = 1e4 M_Pl  : {dt_from_phi0(1e4):.3e} s")
print(f"  dt at phi_0 = 1e10 M_Pl : {dt_from_phi0(1e10):.3e} s")
print("  -> the duration is unbounded above; it is not a property of 'eternal")
print("     inflation' but of the (arbitrary) initial field value.")
print("  -> deeper: inside the self-reproducing regime the dynamics is")
print("     diffusion-dominated (quantum scatter > classical drift), so the")
print("     classical clock dt = dphi/|phidot| is not the physical duration;")
print("     the exit-time distribution and its moments are measure-dependent.")
print("=" * 74)
