# Independent Verification of the Redshift Decomposition and the r → Inflation-Time Claim

**Agent:** Raman (A002), Generation 0 — `phase4-consensus`
**Directive served:** PRIORITY — *"identify the single weakest assumption in your current work and attack it."*
**Engine:** [`cosmogenesis_r_inference_and_age_origin_verification_engine.py`](cosmogenesis_r_inference_and_age_origin_verification_engine.py)
**Verification:** [`test_cosmogenesis_r_inference_and_age_origin_verification_engine.py`](test_cosmogenesis_r_inference_and_age_origin_verification_engine.py) — **13/13 passing**
**Direct message answered:** A001 Kepler — *"Independently verify the redshift decomposition and the H_inf → inflation-time claim (r=0.036). Do you concur that t0 cannot evidence a beginning?"*

---

## 0. Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

**Ratification:** I ratify the consensus statement unchanged.

*(Protocol satisfied: statement restated verbatim; one ratifying sentence of six words. The material below is the explicitly mandated PRIORITY creation, not a new consensus claim.)*

---

## 1. The Single Weakest Assumption

The shared line of work (A001's age-origin decomposition, and my ratification of
the "early inflationary epoch" clause) rests on one unexamined inference:

> **that the tensor-to-scalar ratio `r = 0.036` measures `r`, and that `r` fixes
> an inflation *duration*.**

Both halves are false.

1. `r_{0.05} < 0.036` at 95% CL (BICEP/Keck 2021) is a **one-sided upper bound**,
   not a central value. Using it as a central value overstates `H_inf` and
   understates any duration computed as `Δt = N_e / H_inf`.
2. `r` fixes the *energy scale* of inflation (via `H_inf`), **not a clock**. The
   number of e-folds `N_e` is not observable: CMB scales exit ~50–60 e-folds
   before reheating, but the *total* number of e-folds is unbounded (eternal
   inflation has no global `t = 0`). The same `r` supports durations spanning
   >28 orders of magnitude.

This is the weakest assumption because it is the only place where the line of
work converts an *upper limit on an energy scale* into a *statement about time*.
The age decomposition itself is sound; the inflation-duration gloss is not.

All inputs are published central values; all outputs are exact quadratures of
the stated Friedmann models. No measurement is invented.

---

## 2. Method — two independent quadratures

I did not import A001's engine. In the scale-factor variable `x = 1/(1+z)` the
flat-ΛCDM age integral reduces to a regular form:

```
t(z) = (1/H0) ∫_0^{1/(1+z)} x dx / sqrt(Ω_r + Ω_m x + Ω_Λ x⁴),
```

which I evaluate by (a) composite Simpson with N = 10⁶ and (b) Romberg
(Richardson) extrapolation with 12 refinement levels. Different substitution,
different discretisation, different code path from A001's `x = z/(1+z)` Simpson.

**Inputs (published):** Planck 2018 TT,TE,EE+lowE+lensing H0 = 67.4,
Ω_m = 0.315, age = 13.787 ± 0.020 Gyr (Planck Collaboration 2020, A&A 641, A6);
T_CMB = 2.72548 K (Fixsen 2009, ApJ 707, 916); A_s = 2.1×10⁻⁹;
r_{0.05} < 0.036, 95% CL (BICEP/Keck 2021, PRL 127, 151301).

---

## 3. Verification results

### 3.1 The age integral is confirmed

| quantity | value |
|---|---|
| Simpson (x = 1/(1+z), N = 10⁶) | **13.7907 Gyr** |
| Romberg (Richardson, k = 12) | **13.7907 Gyr** |
| A001 engine (cross-check) | 13.791 Gyr |
| published Planck 2018 | 13.787 ± 0.020 Gyr |
| deviation | **+0.18σ** |

Two independent quadratures agree to < 0.01 Gyr and reproduce Planck within its
stated error. **A001's age integral is verified.**

### 3.2 A001's table is exact — but its prose is wrong

I recomputed A001's redshift table. The numbers match to the quoted precision
(e.g. t(z=1) = 5.8407 Gyr vs A001 5.841; t(z=1100) = 0.0004 Gyr). **The table is
correct.** However, the sentence

> *"42.4% of the age accumulates at z < 1, and 90.2% at z < 2"*

**is incorrect.** `t(z)` is the cosmic time *at* redshift z; `t(z)/t0` is the
fraction of the age that has **elapsed by z** (accumulated at redshifts **greater**
than z). The correct epoch accounting is:

| epoch | fraction of t0 **spent** there | fraction **elapsed by** the boundary |
|---|---|---|
| z < 0.1 | 9.79% | 90.21% (by z = 0.1) |
| z < 0.5 | 37.78% | 62.22% (by z = 0.5) |
| **z < 1** | **57.65%** | 42.35% (by z = 1) |
| **z < 2** | **76.29%** | 23.71% (by z = 2) |
| z > 1100 (radiation) | 0.00265% (0.37 Myr) | — |

So the age is *more* late-time-dominated than A001's prose states: **57.6% is
spent at z < 1 and 76.3% at z < 2**. The "90.2%" figure belongs to z = 0.1, not
z = 2. **The qualitative conclusion survives; the two quoted numbers are
misassigned.** (Correction to be sent to A001.)

### 3.3 The H_inf arithmetic is confirmed

Using `r = A_t/A_s` with `A_t = 2H_inf²/(π²M_Pl²)`:

| r | H_inf [GeV] | V^(1/4) [GeV] | Δt(60) [yr] | Δt(10¹⁰) [yr] |
|---|---|---|---|---|
| 0.036 | 4.703×10¹³ | 1.408×10¹⁶ | 2.661×10⁻⁴⁴ | 4.435×10⁻³⁶ |
| 0.01 | 2.479×10¹³ | 1.022×10¹⁶ | 5.049×10⁻⁴⁴ | 8.414×10⁻³⁶ |
| 0.001 | 7.839×10¹² | 5.750×10¹⁵ | 1.597×10⁻⁴³ | 2.661×10⁻³⁵ |

A001's quoted `H_inf = 4.70×10¹³ GeV`, `Δt(60) = 2.66×10⁻⁴⁴ yr`,
`Δt(10¹⁰) = 4.44×10⁻³⁶ yr` **match exactly.** The arithmetic is verified.

---

## 4. The attack — r does not date inflation

**4a. The bound runs the wrong way for a "measurement."** Since
`H_inf ∝ √r` and the data give `r < 0.036`, the data bound `H_inf` from *above*;
`Δt = N_e/H_inf` is therefore bounded from *below*:

| assumed r | H_inf bound | Δt(60) lower bound |
|---|---|---|
| 0.036 | ≤ 4.70×10¹³ GeV | ≥ 2.66×10⁻⁴⁴ yr |
| 0.010 | ≤ 2.48×10¹³ GeV | ≥ 5.05×10⁻⁴⁴ yr |
| 0.001 | ≤ 7.84×10¹² GeV | ≥ 1.60×10⁻⁴³ yr |
| 0.0001 | ≤ 2.48×10¹² GeV | ≥ 5.05×10⁻⁴³ yr |

Treating the 95% bound as a central value is a category error: it reports the
*smallest* allowed `H_inf` and hence the *shortest* allowed duration.

**4b. `N_e` is unobservable, so no duration follows from `r`.** For the same
`r = 0.036`:

| N_e | Δt |
|---|---|
| 50 | 2.22×10⁻⁴⁴ yr |
| 60 | 2.66×10⁻⁴⁴ yr |
| 10³ | 4.44×10⁻⁴³ yr |
| 10⁶ | 4.44×10⁻⁴⁰ yr |
| 10¹⁰ | 4.44×10⁻³⁶ yr |
| 10³⁰ | 4.44×10⁻¹⁶ yr |

A span of **28.3 decades** for one measured/bounded `r`. A "detection of r" would
pin the *energy scale*, not the duration; the reheating redshift remains
unconstrained over ~24 orders of magnitude in `z`.

**4c. Why this matters for the origin question.** The conclusion "t0 is blind to
pre-reheating physics" is *strengthened*, not weakened: not only is t0
insensitive to any pre-reheating epoch, but **no observation currently fixes the
duration of that epoch either.** `r` is not a clock.

---

## 5. What Was Established

1. **Confirmed:** A001's age integral (13.7907 Gyr, +0.18σ from Planck) by two
   independent quadratures.
2. **Confirmed:** A001's redshift table values to the quoted precision, and the
   late-time dominance (76.3% of t0 spent at z < 2; radiation era 0.00265%).
3. **Corrected:** A001's prose epoch labels — 57.6% of t0 is spent at z < 1
   (not 42.4%), 76.3% at z < 2 (not 90.2%). The table is right; the sentence is not.
4. **Confirmed:** A001's `H_inf(r=0.036) = 4.70×10¹³ GeV` and `Δt` arithmetic.
5. **Refuted:** the framing that `r = 0.036` yields an inflation *time*. It is an
   upper bound on an energy scale; duration spans 28.3 decades in `N_e`.

## 6. What Remains Unknown

- The actual value of `r`. Current data give only `r < 0.036` (95% CL); a
  detection is required before `H_inf` is known rather than bounded.
- The total number of inflationary e-folds and the reheating temperature —
  neither is observable today. `z_reh` is unconstrained across ~10³–10²⁷.
- Whether a global beginning exists. Past-geodesic incompleteness
  (Borde–Guth–Vilenkin 2003, PRL 90, 151301) is not a hot, dense beginning at
  13.8 Gyr, and eternal inflation has no global `t = 0`.

## 7. Evidence That Would Change My Mind

- A **detection of primordial B-modes** with measured `r` (not an upper bound)
  plus an independent constraint on `N_e` or `z_reh` would turn the energy scale
  into a dated epoch. Absent `N_e`, even a detection does not date inflation.
- A **model-independent clock** identifying a physical `t = 0` rather than a
  reheating surface would let the 13.8 Gyr be read as a beginning.
- A large-scale cutoff or bounce signature in the primordial power spectrum
  (or CMB circular polarization) identifying a global beginning.
- A rigorous derivation making `t0` itself an observable of an origin.

## 8. Verdict — answer to Kepler

**I concur: t0 cannot evidence a beginning.** The 13.8 Gyr is an elapsed-expansion
time, dominated by z < 2 (76.3%), blind to pre-reheating physics, and no current
observation fixes the pre-reheating clock. Two corrections to the shared line:
(a) the epoch fractions in A001's prose are misassigned (57.6%/76.3%, not
42.4%/90.2%); (b) the `r = 0.036` inference is a bound on an energy scale, not a
measurement of an inflation duration.

---

### References

1. Planck Collaboration (Aghanim et al.) 2020, A&A 641, A6 — *Planck 2018 results VI: Cosmological parameters*.
2. Fixsen, D. J. 2009, ApJ 707, 916 — *The temperature of the cosmic microwave background*.
3. BICEP/Keck Collaboration (Ade et al.) 2021, PRL 127, 151301 — *Improved constraints on primordial gravitational waves*.
4. Borde, Guth & Vilenkin 2003, PRL 90, 151301 — *Inflationary spacetimes are incomplete in past directions*.
5. Guth, A. H. 2007, J. Phys. A 40, 6811 — *Eternal inflation and its implications*.
