#!/usr/bin/env python3
"""A002 (Raman) -- independent reproduction of the flat-FLRW w0waCDM age integral,
and an attack on the label "0.835 Gyr 1sigma spread".

t0 = (1/H0) * Integral_0^1 da / [a E(a)]
E^2 = Om a^-3 + Or a^-4 + Ode * a^{-3(1+w0+wa)} exp(-3 wa (1-a))

Log substitution x=ln a:  t0 = (1/H0) * Integral_{-inf}^{0} dx / E(e^x)

No third-party dependencies.  Simpson with N=2,000,000.
"""
import math
import random

H0_TO_GYR = 977.7922216  # (km/s/Mpc)^-1 -> Gyr

# ---- inputs (swarm-record values, same as A001's age artifact) ----
PLANCK = dict(H0=67.36, Om=0.3153, w0=-1.0, wa=0.0)
DESI_LCDM = dict(H0=68.60, Om=0.300, w0=-1.0, wa=0.0)
DESI_W0WA = dict(H0=68.60, Om=0.300, w0=-0.727, wa=-1.05)
OR = 9.0e-5


def age(H0, Om, w0=-1.0, wa=0.0, Or=OR, N=500_000):
    """Return t0 [Gyr]."""
    Ode = 1.0 - Om - Or
    x0, x1 = -32.0, 0.0
    h = (x1 - x0) / N

    def E(x):
        a = math.exp(x)
        de = Ode * a ** (-3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * (1.0 - a))
        return math.sqrt(Om / a ** 3 + Or / a ** 4 + de)

    s = 1.0 / E(x0) + 1.0 / E(x1)
    for i in range(1, N):
        s += (4.0 if i % 2 else 2.0) / E(x0 + i * h)
    I = s * h / 3.0
    return H0_TO_GYR / H0 * I


def t0_of(p):
    return age(p["H0"], p["Om"], p["w0"], p["wa"])


print("=" * 72)
print("PART 1 -- independent reproduction of the reported ages")
print("=" * 72)
for name, p in [("Planck LCDM (67.36,0.3153)", PLANCK),
                ("DESI bg LCDM (68.60,0.300)", DESI_LCDM),
                ("DESI w0waCDM (68.60,0.300,-0.727,-1.05)", DESI_W0WA)]:
    print(f"{name:44s}  t0 = {t0_of(p):.4f} Gyr")

t_planck = t0_of(PLANCK)
t_bg = t0_of(DESI_LCDM)
t_w0wa = t0_of(DESI_W0WA)
print(f"\nPlanck anchor (published 13.797 +/- 0.023) : {t_planck:.4f}  "
      f"residual {t_planck - 13.797:+.4f}")
print(f"DESI w0waCDM best fit - Planck             : {t_w0wa - t_planck:+.4f} Gyr")
print(f"DESI w0waCDM best fit - DESI bg LCDM       : {t_w0wa - t_bg:+.4f} Gyr")

# ---- numerical derivatives at the DESI w0waCDM point ----
eps = 1e-4
dw0 = (age(68.60, 0.300, -0.727 + eps, -1.05) - age(68.60, 0.300, -0.727 - eps, -1.05)) / (2 * eps)
dwa = (age(68.60, 0.300, -0.727, -1.05 + eps) - age(68.60, 0.300, -0.727, -1.05 - eps)) / (2 * eps)
dH0 = (age(68.60 + 0.01, 0.300, -0.727, -1.05) - age(68.60 - 0.01, 0.300, -0.727, -1.05)) / 0.02
dOm = (age(68.60, 0.300 + eps, -0.727, -1.05) - age(68.60, 0.300 - eps, -0.727, -1.05)) / (2 * eps)
print("\nLocal derivatives at the DESI w0waCDM point [Gyr per unit]:")
print(f"  dt0/dw0 = {dw0:+.3f}   dt0/dwa = {dwa:+.3f}")
print(f"  dt0/dH0 = {dH0:+.4f}   dt0/dOm = {dOm:+.3f}")

print("\n" + "=" * 72)
print("PART 2 -- the '0.835 Gyr 1sigma spread': box range vs propagated 1sigma")
print("=" * 72)
# Kepler's 1sigma inputs
w0_bf, s_w0 = -0.727, 0.067
wa_bf = -1.05
s_wa = 0.27           # -0.27/+0.31, symmetric choice
H0_bf, s_H0 = 68.60, 0.85   # 67.75 .. 69.45

# (a) corner-to-corner range over the 1sigma hyper-rectangle (what "0.835" is)
lo = age(H0_bf + s_H0, 0.300, w0_bf + s_w0, wa_bf + s_wa)  # H0 up lowers t0
hi = age(H0_bf - s_H0, 0.300, w0_bf - s_w0, wa_bf - s_wa)
print(f"(a) 1sigma-box corner range:  min {lo:.4f}  max {hi:.4f}  span {hi-lo:.4f} Gyr")
print(f"    reported by A001        :  min 13.220  max 14.055  span 0.835 Gyr")

# (b) correct linear (independent-Gaussian) propagation
sig_lin = math.sqrt((dw0 * s_w0) ** 2 + (dwa * s_wa) ** 2 + (dH0 * s_H0) ** 2)
print(f"(b) propagated 1sigma (independent, linear): {sig_lin:.4f} Gyr")

# (c) Monte Carlo, independent Gaussians
random.seed(20240607)
vals = []
NMC = 10_000
for _ in range(NMC):
    w0 = random.gauss(w0_bf, s_w0)
    wa = random.gauss(wa_bf, s_wa)
    H0 = random.gauss(H0_bf, s_H0)
    vals.append(age(H0, 0.300, w0, wa, N=5_000))
mean = sum(vals) / NMC
var = sum((v - mean) ** 2 for v in vals) / (NMC - 1)
sd = math.sqrt(var)
vals.sort()
p16, p50, p84 = vals[int(0.16 * NMC)], vals[int(0.50 * NMC)], vals[int(0.84 * NMC)]
print(f"(c) Monte Carlo (N={NMC}, independent Gaussians):")
print(f"    mean {mean:.4f}  sd {sd:.4f} Gyr   16/50/84 pct {p16:.4f}/{p50:.4f}/{p84:.4f}")

print(f"\n    Box span / propagated sd = {(hi-lo)/sd:.2f} sigma-equivalent")
print(f"    Box span / quoted Planck stat error (0.023) = {(hi-lo)/0.023:.1f}x")
print(f"    Propagated sd / quoted Planck stat error    = {sd/0.023:.1f}x")

print("\n" + "=" * 72)
print("PART 3 -- attack on the weakest assumption: CPL is the w(a) history")
print("=" * 72)
# The age depends on w(a) over all a; CPL is a 2-parameter truncation.
# Same (w0, wa) but a different 2-parameter history w(a) changes the age.
# Test: CPL vs a history matching w0 and dw/da at a=1 but with different
# curvature, w(a) = w0 + wa(1-a) + c(1-a)^2  (c=0 is CPL).
def age_general(H0, Om, w0, wa, c=0.0, Or=OR, N=500_000):
    Ode = 1.0 - Om - Or
    x0, x1 = -32.0, 0.0
    h = (x1 - x0) / N

    # rho_DE(a)/rho_DE,0 = a^{-3} exp( -3 Integral_1^a w(a') d ln a' )
    # For w = w0 + wa(1-a) + c(1-a)^2 the exponent has a closed form.
    def exponent(a):
        # Int_1^a w(a') dln a', a'=e^y, y from 0 to ln a
        # w = w0 + wa(1-e^y) + c(1-e^y)^2
        # Int_0^{ln a} [w0 + wa - wa e^y + c(1 - 2e^y + e^{2y})] dy
        L = math.log(a)
        A = w0 + wa + c
        B = -wa - 2 * c
        C = c
        return A * L + B * (a - 1.0) + C * (a * a - 1.0) / 2.0

    def E2(x):
        a = math.exp(x)
        # d ln rho_DE / d ln a = -3(1+w)  =>  rho_DE = Ode a^-3 exp(-3 Int w dln a)
        de = Ode * a ** -3.0 * math.exp(-3.0 * exponent(a))
        return Om / a ** 3 + Or / a ** 4 + de

    s = 1.0 / math.sqrt(E2(x0)) + 1.0 / math.sqrt(E2(x1))
    for i in range(1, N):
        s += (4.0 if i % 2 else 2.0) / math.sqrt(E2(x0 + i * h))
    return H0_TO_GYR / H0 * s * h / 3.0


# sanity: c=0 must equal CPL
t_cpl = age(68.60, 0.300, -0.727, -1.05)
t_c0 = age_general(68.60, 0.300, -0.727, -1.05, c=0.0)
print(f"CPL cross-check: closed-form {t_cpl:.4f}  vs general c=0 {t_c0:.4f}  "
      f"(diff {t_c0-t_cpl:+.5f})")
print("\nSame (w0,wa) but adding curvature c(1-a)^2 (a CPL-truncation systematic):")
for c in [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0]:
    t = age_general(68.60, 0.300, -0.727, -1.05, c=c)
    print(f"  c = {c:+.1f}   t0 = {t:.4f} Gyr   shift {t - t_cpl:+.4f}")

print("\n" + "=" * 72)
print("PART 4 -- high-z weight of the age integrand (why CPL extrapolation is weak)")
print("=" * 72)
# fraction of the dimensionless age integral accumulated below a=0.2, 0.5
# clean fraction computation
def fraction_below(a_split, H0, Om, w0, wa, Or=OR, N=200_000):
    Ode = 1.0 - Om - Or
    x0, x1 = -32.0, 0.0
    h = (x1 - x0) / N
    x_split = math.log(a_split)
    full = 0.0
    below = 0.0
    for i in range(N + 1):
        x = x0 + i * h
        a = math.exp(x)
        de = Ode * a ** (-3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * (1.0 - a))
        f = 1.0 / math.sqrt(Om / a ** 3 + Or / a ** 4 + de)
        w = 1.0 if (i == 0 or i == N) else (4.0 if i % 2 else 2.0)
        full += w * f
        if x <= x_split:
            below += w * f
    return below / full


for a_split in [0.05, 0.1, 0.2, 0.5]:
    fr = fraction_below(a_split, 68.60, 0.300, -0.727, -1.05)
    print(f"  fraction of age integrand from a < {a_split:4.2f} "
          f"(z > {1/a_split - 1:5.1f}): {fr*100:5.2f}%")
