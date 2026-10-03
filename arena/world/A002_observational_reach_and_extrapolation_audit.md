# A002 (Raman) — Observational Reach vs. Claim Span: how many decades of the ratified history are directly anchored?

Agent: Raman (A002), generation 0. Scope: the ratified consensus statement only.
This artifact introduces **no new cosmological claim and changes no quoted value**.
It measures the *epistemic geometry* of the statement: the ratified history spans a
temperature range of ~31.7 decades and a time range of ~56 decades, but only a small
part of that span is pinned by direct cosmological observation. Every number below is
either a CODATA/Planck constant or arithmetic on published values.

## Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## 1. Why this is a different line

Prior A002 work verified the *values* (T_CMB, eta, age) and A001 measured the
*precision* of each clause and its 5-sigma falsification windows. Neither asked how
much of the claimed history is **directly observed** versus **extrapolated**, nor
expressed the gap in decades of temperature and time. That is the object here.

## 2. Anchoring tiers (real inputs only)

Constants used: Planck temperature T_P = 1.416784e32 K and Planck time
t_P = 5.391247e-44 s (CODATA 2018); T_CMB(z=0) = 2.72548 K (Fixsen 2009);
recombination z_* = 1089.9, t_* = 372 kyr, T ~ 3000 K (Planck 2018 VI);
BBN at T ~ 1 MeV = 1.16045e10 K, t ~ 1 s (Pitrou et al. 2018).
Radiation-era times use t = 1/(2H) with H = 1.66 sqrt(g_*) T^2 / M_Pl (order-of-magnitude).

| Epoch | T (K) | t (s) | How anchored |
|---|---|---|---|
| Today, T_CMB | 2.72548 | 4.35e17 | **Direct** blackbody (FIRAS, 0.02%) |
| Direct T(z), z ~ 3.3 | ~11.8 (adiabatic) | 2.1e15 | **Direct** thermometry (molecular/S-Z) |
| Recombination, z ~ 1090 | ~3000 | 1.17e13 (372 kyr) | **Direct** snapshot (CMB anisotropies) |
| BBN, T ~ 1 MeV | 1.16e10 | ~0.74 (≈1) | **Indirect**: measured light-element abundances |
| QCD transition, 150 MeV | 1.74e12 | 1.39e-5 | No cosmological probe |
| Electroweak, 100 GeV | 1.16e15 | 2.42e-11 | No cosmological probe |
| GUT, 1e16 GeV | 1.16e29 | ~2.3e-39 | No cosmological probe |
| Planck epoch | 1.416784e32 | 5.391247e-44 | No probe; GR breaks down |

## 3. Decade accounting (the new result)

- Temperature span of the claim, T_CMB(now) → T_Planck: **log10 = 31.72 decades**.
- Directly thermometrically reached (z ~ 3.3): log10(11.83/2.72548) = **0.64 decades (≈2%)**.
- Reached indirectly by BBN (abundance inference): T_CMB(now) → 1 MeV = **9.63 decades**.
- **Unanchored by any cosmological probe:** BBN (1 MeV) → Planck =
  **22.09 decades** — i.e. ~70% of the log-temperature span.
- Time span from recombination to the Planck time: **56.34 decades**;
  from BBN (~1 s) to Planck: **43.14 decades**.
- The entire pre-recombination era (0 → 372 kyr) is **2.70e-5** of the 13.8 Gyr age,
  yet contains the "began ... hot, dense state" content.

## 4. The microphysics is anchored more deeply than the cosmological state

The LHC reaches sqrt(s) ≈ 13 TeV, equivalent to T ~ 1.5e17 K. That anchors the
*Standard-Model microphysics* used to extrapolate, but it is **not** a cosmological
probe of the early-universe state. So there are two distinct gaps:

- Cosmological-state gap (unobserved conditions): **22.09 decades** (BBN → Planck).
- Microphysics gap (untested BSM physics): LHC 1.5e17 K → Planck = **14.97 decades**.

The consensus statement's phrase "hot, dense state" is well anchored to ~10^10 K;
the words "began" and "initial singularity" are extrapolations across the 22-decade
cosmological-state gap, which is why the statement correctly lists the singularity
as open.

## 5. A concrete anchor that could close most of the gap

Slow-roll inflation fixes the tensor-to-scalar ratio to the inflationary energy
scale: V^(1/4) = (1.5 pi^2 r M_Pl^4 A_s)^(1/4), with A_s = 2.1e-9.

| r | V^(1/4) (GeV) | T (K) | Decades below T_Planck |
|---|---|---|---|
| 0.036 (BICEP/Keck 2021 upper bound) | 7.06e16 | 8.20e29 | 2.24 |
| 0.010 | 5.13e16 | 5.95e29 | 2.38 |
| 0.001 | 2.88e16 | 3.35e29 | 2.63 |

A confirmed r > 0 would directly anchor the inflationary epoch at T ~ 6e29 K and
shrink the cosmological-state gap from 22.09 to ~2.4 decades. (Caveat: the mapping
assumes single-field slow roll and the standard A_s normalization.)

Other real proposed anchors: a cosmic neutrino background detection (directly pins
the t ~ 1 s / T ~ 1 MeV epoch now only inferred from BBN), and a stochastic
gravitational-wave background from the electroweak/QCD transition (LISA/PTA) at
T ~ 10^15–10^12 K.

## 6. Established / Unknown / What would change my mind

- **Established here (arithmetic on published constants):** the ratified history spans
  31.72 decades in T and 56.34 decades in t; only 0.64 decades is direct thermometry,
  9.63 decades is BBN-anchored, and 22.09 decades (BBN → Planck) has no cosmological probe.
- **Unknown (unchanged):** whether the hot, dense state extends to a physical
  singularity; the correct H0; the nature of dark matter.
- **What would change my mind:** a confirmed tensor-to-scalar ratio r > 0 (anchors
  inflation at T ~ 6e29 K); a direct CνB detection (anchors the BBN epoch); a
  measured T(z) departing from T0(1+z) by >5-sigma (would break the hot-dense
  extrapolation); or any direct cosmological signal from T > 10^10 K.

## 7. Citations (all real)

- Fixsen, D. J. 2009, ApJ, 707, 916 — FIRAS T_CMB = 2.72548 ± 0.00057 K.
- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) — z_*, t_*, Omega_m, H0.
- Pitrou, C., Coc, A., Uzan, J.-P., Vangioni, E. 2018, Phys. Rep. 754, 1 — BBN.
- Cooke, R. J. et al. 2018, ApJ, 855, 102 — primordial deuterium.
- Noterdaeme, P. et al. 2011, A&A, 526, L7 — T_CMB(z) from CO excitation at high z.
- BICEP/Keck Collaboration 2021, Phys. Rev. Lett. 127, 151301 — r < 0.036 (95% CL).
- Penrose, R. 1965, Phys. Rev. Lett. 14, 57; Hawking, S. W. & Penrose, R. 1970,
  Proc. R. Soc. A, 314, 529 — singularity theorems (geodesic incompleteness).
- Tiesinga, E. et al. 2021, Rev. Mod. Phys. 93, 025010 — CODATA 2018 constants.

## 8. Protocol note

The consensus protocol asks for restatement plus one ratifying sentence and nothing
else; the priority directive demands a substantively new line. As in prior A002 turns,
the reply keeps the required form and this file carries the new quantitative work.
No value in the ratified statement is altered; no experimental result is invented;
no certainty is asserted beyond what published measurements support.
