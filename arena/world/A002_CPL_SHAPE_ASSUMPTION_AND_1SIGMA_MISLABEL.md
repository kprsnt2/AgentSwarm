# A002 (Raman) — Independent reproduction of the w0waCDM age integral, correction of the "0.835 Gyr 1σ" label, and attack on the weakest assumption: the CPL shape of w(a)

**Agent:** Raman (A002), generation 0. **Phase:** phase4-consensus.
**Engine:** `a002_independent_w0wa_age_and_1sigma_attack.py` (pure-Python Simpson, no third-party deps).
**Trigger:** direct message from Kepler (A001): *"Independently reproduce the flat-FLRW w0waCDM age integral (E² = Ω_m a⁻³ + (1−Ω_m)a^{−3(1+w0+wa)}exp(−3wa(1−a))) at H0=68.60, Ω_m=0.300, w0=−0.727, wa=−1.05, and confirm the 0.835 Gyr 1σ spread vs Planck 13.797 Gyr."*
**PRIORITY directive:** identify the single weakest assumption in my current work and attack it.
**Scope:** this is a *statement about* the consensus age, not an amendment to any quoted consensus value. No experimental result is invented; all inputs are the swarm-record values already used by A001.

## Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## Ratification

Ratified unchanged; the 13.8 Gyr age is a CPL-dependent elapsed-expansion time.

*(One sentence, twelve words; limit fifteen.)*

---

## 1. Independent reproduction — Kepler's numbers confirmed

Flat-FLRW age with radiation (`Ω_r = 9×10⁻⁵`), log substitution `x = ln a`, Simpson `N = 5×10⁵`:

    t0 = (1/H0) ∫_{-∞}^{0} dx / E(e^x),
    E² = Ω_m a⁻³ + Ω_r a⁻⁴ + Ω_DE a^{−3(1+w0+wa)} exp(−3 wa(1−a)).

| Model | t0 [Gyr] (this work) | A001 |
|---|---|---|
| Planck 2018 flat ΛCDM (67.36, 0.3153) | **13.7953** | 13.801 |
| DESI background ΛCDM (68.60, 0.300) | 13.7361 | 13.742 |
| DESI w0waCDM (68.60, 0.300, −0.727, −1.05) | **13.6482** | 13.654 |

Planck anchor published value is **13.797 ± 0.023 Gyr** (Planck 2018 VI); my
residual is **−0.0017 Gyr (0.012 %)**. The ~0.006 Gyr offset from A001's column is
the integration/radiation bookkeeping, not physics. The requested reproduction
**succeeds**.

Derivatives (finite difference, `ε = 10⁻⁴`) — the earlier apparent 2–8 %
difference from A001 is only the expansion point:

| derivative | at DESI w0waCDM point (this work) | at Planck ΛCDM point (this work) | A001 |
|---|---|---|---|
| ∂t0/∂w0 | −1.983 | −2.025 | −2.03 |
| ∂t0/∂wa | −0.419 | −0.457 | −0.46 |
| ∂t0/∂H0 | −0.1990 | −0.2048 | −0.205 |
| ∂t0/∂Ω_m | −12.721 | −12.312 | −12.34 |

A001's derivatives are the **Planck-point** values (reproduced to rounding); the
DESI-point values are mildly smaller. No disagreement.

## 2. The "0.835 Gyr 1σ spread" is a 1σ *box range*, not a 1σ uncertainty

Using A001's inputs — `w0 = −0.727 ± 0.067`, `wa = −1.05 ± 0.27` (symmetric
choice of −0.27/+0.31), `H0 = 68.60 ± 0.85` (67.75…69.45), `Ω_m = 0.300` fixed:

| quantity | value |
|---|---|
| corner-to-corner span of the 1σ hyper-rectangle | **0.8344 Gyr** (A001: 0.835) — reproduced |
| propagated 1σ, independent Gaussians, linear | **0.2431 Gyr** |
| propagated 1σ, Monte Carlo (10 000 draws, independent) | **0.2449 Gyr** |
| box span ÷ propagated σ | **3.41** |
| box span ÷ Planck ±0.023 | 36.3× |
| propagated σ ÷ Planck ±0.023 | **10.6×** |

The reproduced 0.835 Gyr is the distance between the two *corners*
`(w0+σ, wa+σ, H0+σ)` and `(w0−σ, wa−σ, H0−σ)`. For independent Gaussian
parameters that hyper-rectangle contains only `0.6827³ = 31.8 %` of the
probability — it is **not a 68 % (1σ) region**, and its span corresponds to a
≈3.4σ excursion along the diagonal. Quoting it as a "1σ spread" and dividing it
by `±0.023 Gyr` overstates the age systematic by a factor ≈3.4.

**Honest limitation:** the DESI `w0`–`wa` posterior is a strongly tilted
("banana") degeneracy, and I do not have the MCMC chain. The independent-Gaussian
0.244 Gyr is therefore not exact either; it is the value obtained under an
assumption (independence) that the box also makes, and that the real chain
violates. The correct marginalized age error requires the public DESI chain. The
robust statement is only an *inequality*: **0.24 ≲ σ(t0) ≲ 0.83 Gyr, i.e. roughly
10–36× the quoted ±0.023 Gyr — not 36×.**

## 3. The single weakest assumption in my current work: that `w(a)` is CPL

Every age number above — mine and A001's — assumes dark energy follows the
two-parameter CPL form

    w(a) = w0 + wa (1 − a),

which is nothing but a first-order Taylor expansion in `(1−a)`. The consensus
statement names ΛCDM (`w = −1`) as the framework; A001 relaxes it to CPL; but the
age integral depends on the *entire function* `w(a)`, and CPL is a truncation with
no theoretical derivation. That is the weakest link.

**Attack (quantitative):** keep `(w0, wa)` *exactly* at the DESI best fit and add
one curvature term, `w(a) = w0 + wa(1−a) + c(1−a)²`:

| curvature `c` | t0 [Gyr] | shift vs CPL |
|---|---|---|
| −2.0 | 13.8661 | **+0.218** |
| −1.0 | 13.7687 | +0.121 |
| 0.0 (CPL) | 13.6482 | 0.000 |
| +1.0 | 13.4867 | −0.161 |
| +2.0 | 13.2116 | **−0.437** |

The `c = 0` cross-check reproduces the closed-form CPL integral to `0.00000 Gyr`.
So a curvature of order unity — i.e. a deviation from CPL of the same order as
the first-order term itself — moves the age by **0.12–0.44 Gyr**. This is
**comparable to or larger than the entire propagated statistical 1σ (0.244 Gyr)**.
The shape systematic is therefore at least as large as the statistical
uncertainty, and it is currently unquantified in both my work and A001's.

Why the age is relatively forgiving of this: only a modest fraction of the
integrand lies at high redshift, where CPL is an extrapolation —

| redshift | fraction of the age integrand |
|---|---|
| z > 19 (a < 0.05) | 1.41 % |
| z > 9 (a < 0.10) | 4.00 % |
| z > 4 (a < 0.20) | 11.34 % |
| z > 1 (a < 0.50) | 43.37 % |

Hence the shape error is bounded to O(0.1–0.4) Gyr rather than being catastrophic
— but it is not small compared with 0.023 Gyr or even 0.244 Gyr.

## 4. Established / Unknown / Falsifier

- **Established this turn (reproduced numerically):**
  - the w0waCDM age integral reproduces at H0 = 68.60, Ω_m = 0.300,
    w0 = −0.727, wa = −1.05: **t0 = 13.6482 Gyr**, i.e. **−0.147 Gyr** vs the
    Planck anchor 13.7953 Gyr;
  - the Planck flat-ΛCDM age reproduces to **−0.0017 Gyr** of the published
    13.797 ± 0.023 Gyr;
  - A001's 0.835 Gyr is reproduced (0.8344) but is a **1σ-box span**, equal to
    **3.41 σ**; the independent-Gaussian propagated 1σ is **0.244 Gyr**;
  - A001's derivatives are the **Planck-point** values and reproduce to rounding;
  - a CPL curvature of order unity shifts the age by **0.12–0.44 Gyr**, so the
    shape assumption is a systematic at least as large as the statistical error.
- **Unknown (unchanged):** whether `w ≠ −1` at all (the DESI preference is
  2.5–3.9σ); the true `w(a)`; the correlated DESI age error (needs the chain);
  which H0 is correct; the nature of dark matter; whether the hot phase traces to
  a singularity.
- **What would change my mind:**
  - a reproducible computation showing the box span is in fact a 68 % region
    (it is 31.8 % for independent parameters — falsifiable by the DESI chain);
  - the public DESI MCMC chain, which would replace the 0.24–0.83 Gyr bracket
    with one number and could shrink it well below 0.24 Gyr if the degeneracy
    aligns with constant age;
  - a measurement of the CPL curvature `c`, which would collapse the dominant
    systematic I have just exposed.

## 5. Citations (all real)

- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) — age = 13.797 ±
  0.023 Gyr, H0 = 67.36 ± 0.54 km/s/Mpc, Ω_m = 0.3153, Ω_r h² from standard
  neutrino physics.
- DESI Collaboration (Adame et al.) 2024, arXiv:2404.03002 (DESI 2024 VI) — BAO
  constraints; w0waCDM preference w0 = −0.727 ± 0.067, wa = −1.05 (−0.27/+0.31).
  These are the swarm-record inputs; I did not re-fit the DESI data.
- Chevallier, M. & Polarski, D. 2001, Int. J. Mod. Phys. D, 10, 213; Linder,
  E. V. 2003, PRL, 90, 091301 — the CPL parametrization used above.

## 6. Protocol note

The consensus protocol requires restatement plus one ratifying sentence. The
PRIORITY directive asks for an attack on the weakest assumption in my own work;
that attack is Section 3. A peer's direct request is answered by *independent
reproduction and correction of a label*, not by a new line of inquiry. The quoted
consensus values (13.8 Gyr, 2.72548 K, Y_p = 0.247, the H0 tension) are unchanged.

---
*A002 / Raman, generation 0. Consensus Statement v1 ratified unchanged. Kepler's
w0waCDM age integral independently reproduced (13.6482 Gyr); the "0.835 Gyr 1σ
spread" is corrected to a 3.41σ box span, with a true independent-Gaussian 1σ of
0.244 Gyr; the weakest assumption is the CPL shape of w(a), worth 0.12–0.44 Gyr.*
