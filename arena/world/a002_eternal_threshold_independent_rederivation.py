#!/usr/bin/env python3
"""
A002 (Raman) -- Independent re-derivation of the eternal-inflation threshold
A_s(local) > 1, plus a stress test of its single weakest assumption.

No external data invented. Inputs:
  A_s = 2.1e-9      (Planck 2018 VI, pivot normalization)
  phi_pivot = 15    (M_Pl reduced, N ~ 60 for V = 1/2 m^2 phi^2)
  M_Pl = 1.220890e19 GeV (reduced Planck mass)
Conventions: M_Pl = 1 in the algebra; V = 1/2 m^2 phi^2; slow roll.
"""
import math

M_PL_GEV = 1.220890e19          # reduced Planck mass, GeV
A_S_OBS = 2.1e-9                # Planck 2018 VI
PHI_PIVOT = 15.0                # M_Pl, reduced (N ~ 60)

print("=" * 72)
print("PART 1 -- Symbolic identity, checked numerically")
print("=" * 72)
# Single-field slow roll, M_Pl = 1:
#   epsilon = (1/2)(phidot/H)^2
#   A_s     = H^2/(8 pi^2 epsilon) = H^4/(4 pi^2 phidot^2)
# Quantum scatter per Hubble time:  delta_phi_Q = H/(2 pi)
# Classical roll  per Hubble time:  delta_phi_C = |phidot|/H
# Self-reproduction (eternal) iff delta_phi_Q > delta_phi_C:
#   H/(2 pi) > |phidot|/H  <=>  H^2 > 2 pi |phidot|
# Substitute |phidot| = H^2/(2 pi sqrt(A_s)):
#   H^2 > 2 pi * H^2/(2 pi sqrt(A_s))  <=>  1 > 1/sqrt(A_s)  <=>  A_s > 1.
import random
random.seed(12345)
mismatch = 0
for _ in range(2_000_000):
    H2 = 10 ** random.uniform(-12, 3)
    phidot2 = 10 ** random.uniform(-12, 3)
    A_s = H2 * H2 / (4 * math.pi ** 2 * phidot2)
    eternal_Q = H2 > 2 * math.pi * math.sqrt(phidot2)
    eternal_A = A_s > 1.0
    if eternal_Q != eternal_A:
        mismatch += 1
print(f"random slow-roll points tested : 2,000,000")
print(f"disagreements A_s>1 vs H^2>2*pi|phidot| : {mismatch}")
assert mismatch == 0

# Equivalent potential-space form: V > 24 pi^2 epsilon M_Pl^4
mismatch2 = 0
for _ in range(1_000_000):
    V = 10 ** random.uniform(-12, 3)
    eps = 10 ** random.uniform(-12, 3)
    H2 = V / 3.0
    phidot2 = 2 * eps * H2          # epsilon = (1/2) phidot^2/H^2
    A_s = H2 / (8 * math.pi ** 2 * eps)
    if (V > 24 * math.pi ** 2 * eps) != (A_s > 1.0):
        mismatch2 += 1
print(f"disagreements V>24pi^2 eps vs A_s>1        : {mismatch2}")
assert mismatch2 == 0
print("IDENTITY CONFIRMED: A_s(local) > 1  <=>  V > 24 pi^2 eps M_Pl^4")

print()
print("=" * 72)
print("PART 2 -- Quadratic model: locate the threshold and check the quoted m")
print("=" * 72)
# V = 1/2 m^2 phi^2  =>  eps = 2/phi^2
# A_s = V/(24 pi^2 eps) = m^2 phi^4 / (96 pi^2)
m2_MPl = A_S_OBS * 96 * math.pi ** 2 / PHI_PIVOT ** 4
m_MPl = math.sqrt(m2_MPl)
m_GeV = m_MPl * M_PL_GEV
print(f"A_s(phi_pivot)                      = {A_S_OBS:.3e}")
print(f"required m (reduced M_Pl)           = {m_MPl:.6e} M_Pl")
print(f"required m                          = {m_GeV:.4e} GeV")
print(f"required m / sqrt(8 pi)             = {m_GeV/math.sqrt(8*math.pi):.4e} GeV "
      f"(= value if phi were in NON-reduced Planck units)")

# Threshold field value
phi_et2 = math.sqrt(96 * math.pi ** 2 / m2_MPl)     # phi_et^2
phi_et = math.sqrt(phi_et2)
print(f"phi_et (A_s(local)=1)               = {phi_et:.1f} M_Pl")
# internal check: recompute A_s at phi_et
A_et = m2_MPl * phi_et ** 4 / (96 * math.pi ** 2)
print(f"A_s(phi_et) recomputed              = {A_et:.6f}  (should be 1)")

# What m is implied by the artifact's stated phi_et = 2216?
phi_claimed = 2216.0
m_from_claimed = math.sqrt(96 * math.pi ** 2 / phi_claimed ** 4)
print(f"m implied by claimed phi_et=2216    = {m_from_claimed*M_PL_GEV:.4e} GeV")
print(f"stated m in A001 artifact            = 1.53e13 GeV")
print(f"ratio stated/self-consistent        = {1.53e13/m_GeV:.4f}  "
      f"(sqrt(8 pi) = {math.sqrt(8*math.pi):.4f})")

print()
print("=" * 72)
print("PART 3 -- Total e-folds and duration of the self-reproducing range")
print("=" * 72)
phi_end2 = 2.0                       # V=1/2 m^2 phi^2, slow-roll end eps=1 -> phi^2=2
N_total = (phi_et2 - phi_end2) / 4.0
print(f"N_total (phi_et -> end of slow roll) = {N_total:.3e} e-folds")
V_piv = 0.5 * m2_MPl * PHI_PIVOT ** 2
H_piv = math.sqrt(V_piv / 3.0)
H_GeV = H_piv * M_PL_GEV
print(f"H_inf at pivot                       = {H_piv:.4e} M_Pl = {H_GeV:.4e} GeV")
# H is NOT constant across the huge field range, so N_total/H_pivot is invalid.
# Exact: dN/dphi = -phi/2, H = m*phi/sqrt(6)  =>  dt = dN/H = (sqrt(6)/(2m)) dphi.
# Duration is uniform per unit phi, NOT dominated by late times.
dt_MPl = (math.sqrt(6) / (2 * m_MPl)) * (phi_et - math.sqrt(phi_end2))
SEC_PER_INV_MPl = 6.582119569e-25 / M_PL_GEV   # hbar/(M_Pl c^2)
dt_s = dt_MPl * SEC_PER_INV_MPl
# numeric quadrature cross-check (pure python, no numpy)
NSTEP = 4_000_000
lo = math.sqrt(phi_end2)
hi = phi_et
step = (hi - lo) / NSTEP
dt_quad = 0.0
for i in range(NSTEP):
    phi = lo + (i + 0.5) * step
    H = m_MPl * phi / math.sqrt(6.0)
    dN = 0.5 * phi * step          # |dN/dphi| = phi/2
    dt_quad += dN / H
print(f"duration (exact closed form)         = {dt_s:.3e} s")
print(f"duration (independent quadrature)    = {dt_quad*SEC_PER_INV_MPl:.3e} s")
# show why the naive N/H_pivot estimate is wrong (H varies by ~1560x over the range)
H_et = m_MPl * phi_et / math.sqrt(6.0)
print(f"H at threshold / H at end            = {H_et/(m_MPl*math.sqrt(phi_end2)/math.sqrt(6.0)):.1f}")
print(f"naive N_total/H_pivot (INVALID)      = {(N_total/H_GeV)*6.582119569e-25:.3e} s")

print()
print("=" * 72)
print("PART 4 -- WEAKEST ASSUMPTION: EFT validity at the threshold")
print("=" * 72)
print(f"phi_et / M_Pl (reduced)              = {phi_et:.1f}")
print(f"=> threshold sits log10(phi_et/M_Pl) = {math.log10(phi_et):.2f} "
      f"orders of magnitude above the EFT cutoff M_Pl")
print("The A_s>1 identity is exact and dimensionless, but locating phi_et")
print("requires extrapolating V=1/2 m^2 phi^2 ~2200x beyond its domain.")
print("Only the NEGATIVE statement (our pivot: A_s=2.1e-9, 8.68 dex below 1)")
print("is EFT-controlled and robust.")
print(f"log10(1/A_s_obs) = {math.log10(1/A_S_OBS):.2f} dex below threshold")
