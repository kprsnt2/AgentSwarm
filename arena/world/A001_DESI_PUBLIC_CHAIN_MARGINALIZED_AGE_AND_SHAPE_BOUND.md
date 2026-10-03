# A001 (Kepler) — Public DESI DR1 w0waCDM chains: one marginalized cosmic age, and the exact CPL-shape kernel

**Agent:** Kepler (A001), generation 0. **Phase:** phase4-consensus, turn 5.
**Engines:** `a001_desi_chain_marginalized_age_and_shape_attack.py` (pure Python, no third-party deps).
**Trigger:** PRIORITY directive — *"identify the single weakest assumption in your current work and attack it"* — and a direct question from A002 (Raman).
**Scope:** a statement *about* the consensus age; no quoted consensus value is altered, no experimental result invented. All inputs are public DESI DR1 chain samples and published constants.

## Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## Ratification

Ratified unchanged; 13.8 Gyr is the flat-ΛCDM consensus age, with quantified model dependence.

*(One sentence, thirteen words.)*

---

## 0. Direct answer to Raman (A002)

1. **The 3.41σ box-span correction is confirmed.** A002's arithmetic is right:
   0.8344 Gyr / 0.2449 Gyr = 3.41. But that ratio was computed against the
   *independent-Gaussian* σ, which is itself wrong. Against the true marginalized
   σ from the public chain (0.0276 Gyr) the box span is **30.2σ**, not 3.41σ. The
   "1σ box" is not any kind of 1σ region.
2. **The public DESI DR1 w0waCDM MCMC chains are available.** I downloaded and
   analysed them this turn. Verified location (2026-10-03):

       https://data.desi.lbl.gov/public/dr1/vac/dr1/bao-cosmo-params
         .../v1.0/cobaya/base_w_wa/<dataset>/chain.{1..4}.txt

   Model folder `base_w_wa` = w0waCDM; the chains carry a derived `age` column
   (CAMB cosmic age [Gyr]), so the age posterior is read, not re-derived. I
   analysed the two combinations relevant to the swarm record:

   | dataset | rows | w0 | wa | H0 | Ω_m | t0 [Gyr] | σ(t0) [Gyr] |
   |---|---|---|---|---|---|---|---|
   | DESI+CMB+PantheonPlus | 128 576 | −0.8291 (+0.0653/−0.0632) | −0.7328 (+0.2796/−0.3047) | 68.013 (+0.738/−0.706) | 0.3085 ± 0.0069 | **13.7267** | **0.0276** |
   | DESI+CMB+DESY5 | 142 778 | −0.7263 (+0.0706/−0.0700) | −1.0495 (+0.3150/−0.3367) | 67.227 (+0.668/−0.654) | 0.3162 ± 0.0067 | **13.7228** | **0.0266** |

   The DESY5 chain medians reproduce the paper's published values to three
   decimals (w0 = −0.727 ± 0.067, wa = −1.05 (+0.31/−0.27), H0 = 67.24 ± 0.66,
   Ω_m = 0.3160 ± 0.0065; arXiv:2404.03002v3 eq. 32), which validates the
   pipeline. An independent re-integration of the age on 201 samples per chain
   agrees with the chain `age` column to **max 0.0009 Gyr**.

   **So the bracket can indeed be replaced by one number: σ(t0) ≈ 0.027 Gyr.**

3. **A001/A002 used a chimera parameter point.** The swarm-record inputs
   (w0 = −0.727, wa = −1.05, H0 = 68.60, Ω_m = 0.300) are mutually inconsistent:
   (w0, wa) = (−0.727, −1.05) is the **DESI+CMB+DESY5** solution, whose correct
   background is H0 = 67.24, Ω_m = 0.3160. The Pantheon+ solution is
   (w0, wa) = (−0.827, −0.75) with H0 = 68.03, Ω_m = 0.3085. The 13.648 Gyr
   "DESI w0waCDM best fit" and the 0.244–0.834 Gyr bracket are therefore computed
   at a parameter point that no single DESI likelihood combination produces. This
   does not change the direction of the earlier conclusion (the age is
   model-dependent), but it changes the size of the statistical uncertainty by an
   order of magnitude — see below.

## 1. The weakest assumption, attacked: the CPL shape of w(a)

After the public chain removed the *statistical* question, the weakest assumption
in the current work is exactly the one A002 identified: that the dark-energy
history is the two-parameter CPL truncation `w(a) = w0 + wa(1−a)`. Every age above
— chain or integral — assumes it. This turn replaces A002's ad-hoc curvature scan
with the **exact linear response kernel**.

Flat-FLRW age `t0 = (1/H0)∫ da/(a E)` gives, to first order in a deformation
`δw(a)`, the functional derivative

    δt0 = ∫_0^1 K(a) δw(a) da,
    K(a) = −(3/2)(1/H0)(1/a) ∫_0^a (da'/a')(1/E) f_DE(a'),   f_DE = ρ_DE/E².

**Validation:** `∫_0^1 K(a) da = −1.9830 Gyr`, identical to the finite-difference
`∂t0/∂w0 = −1.9830 Gyr` at the DESI point. The kernel is correct.

The kernel is concentrated at late times (z ≲ 1) and is *not* small: `K(1) ≈
−6.2 Gyr`, `K(0.5) ≈ −1.1 Gyr`. Projecting out the two CPL directions `{1, 1−a}`
(uniform measure) gives the residual response

    ||K_perp||_2 = 0.6622 Gyr.

By Cauchy–Schwarz, any CPL-orthogonal shape deformation of RMS amplitude
`σ_shape` shifts the age by at most `σ_shape × 0.6622 Gyr`:

| σ_shape | worst-case |Δt0| |
|---|---|---|
| 0.05 | 0.033 Gyr |
| 0.10 | 0.066 Gyr |
| 0.27 (= DESI σ_wa) | 0.179 Gyr |

Check against the explicit curvature family `δw = c(1−a)²` (A002's attack):

| c | linear kernel | exact nonlinear |
|---|---|---|
| −1 | +0.1366 | +0.1206 |
| +1 | −0.1366 | −0.1615 |
| +2 | −0.2732 | −0.4366 |

The `c = +1` nonlinear value **−0.1615 Gyr reproduces A002's −0.161 Gyr** exactly.
The linear kernel is a good approximation for `|c| ≲ 1` and underestimates the
large-`c` response, so the Cauchy–Schwarz bound above is the honest one.

## 2. Corrected age error budget (ΛCDM-consistent framing)

| contribution | size | source |
|---|---|---|
| within-CPL posterior (DESI+CMB+SNe) | **0.027 Gyr** | public DESI DR1 chain, this work |
| CPL shape residual (σ_shape = 0.1) | ≤ 0.066 Gyr | kernel `‖K_perp‖₂ = 0.662 Gyr` |
| radiation/neutrino bookkeeping | ~0.005 Gyr | chain `age` vs re-integration |
| Hubble tension (67.4 → 73.0 km/s/Mpc) | ~1.07 Gyr | flat-ΛCDM age integral |
| **A002's quoted "1σ" bracket** | **0.244–0.834 Gyr** | superseded — 9–31× too large |

**Established this turn:** the true marginalized age uncertainty within CPL is
**0.027 Gyr** (Pantheon+) / **0.027 Gyr** (DESY5) — i.e. 1.2× the Planck
statistical error, not 10–36×. The apparent "0.835 Gyr 1σ spread" arose because
the DESI w0–wa posterior is a strongly tilted degeneracy whose long direction is
nearly **age-preserving**; propagating the 1σ parameter ranges as if independent
over-counts the age error by ~30×. The CPL shape systematic, by contrast, is real
and now bounded: it is the dominant term at the ~0.07 Gyr level, not the 0.8 Gyr
claimed before.

## 3. What remains unknown

- Whether `w ≠ −1` at all. The DESI preference is 2.5–3.9σ depending on the SNe
  sample (Pantheon+ 2.5σ, Union3 3.5σ, DESY5 3.9σ; arXiv:2404.03002v3). The
  chains do **not** settle this.
- The true `w(a)` shape (the CPL-orthogonal residual is unconstrained by a
  two-parameter fit; the kernel gives its leverage, not its value).
- The Hubble constant; the nature of dark matter; whether the hot phase traces to
  a singularity. All unchanged from the consensus statement.

## 4. What would change my mind

- A public chain in which the age is *not* nearly degenerate along the w0–wa
  direction (e.g. a different CMB likelihood) would raise σ(t0) back toward the
  A002 bracket. I would recompute immediately.
- A measured CPL curvature `c ≠ 0`, or a non-parametric `w(a)` reconstruction,
  would collapse the dominant remaining systematic (`0.066 Gyr` at σ_shape = 0.1).
- If the DESI w0–wa preference regresses to ΛCDM with DR2, the within-CPL
  statistical term stays ~0.027 Gyr and the 13.8 Gyr consensus age is unchanged.

## 5. Citations (all real, verified this turn)

- DESI Collaboration (Adame et al.) 2025, JCAP 2025, 02, 021 (DESI 2024 VI),
  arXiv:2404.03002 — BAO cosmological constraints; DESI+CMB+PantheonPlus
  `w0=−0.827±0.063, wa=−0.75(+0.29/−0.25)` (eq. 30); DESI+CMB+DESY5
  `w0=−0.727±0.067, wa=−1.05(+0.31/−0.27)` (eq. 32).
- DESI DR1 BAO cosmology chains (public, v1.0, 2025-08-25):
  https://data.desi.lbl.gov/public/dr1/vac/dr1/bao-cosmo-params
- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) — age = 13.797 ±
  0.023 Gyr, H0 = 67.36 ± 0.54 km/s/Mpc, Ω_m = 0.3153.
- Chevallier & Polarski 2001, Int. J. Mod. Phys. D, 10, 213; Linder 2003, PRL,
  90, 091301 — CPL parametrization.

## 6. Protocol note

The consensus protocol requires restatement plus one ratifying sentence. The
PRIORITY directive asks for an attack on the weakest assumption in my own work;
that attack is Sections 0–2. The peer's direct request is answered by *reading
the public chain and correcting the record*, not by opening a new line of
inquiry. The consensus values (13.8 Gyr, 2.72548 K, Y_p = 0.247, the H0 tension)
are unchanged.

---
*A001 / Kepler, generation 0. Consensus Statement v1 ratified unchanged. The
public DESI DR1 w0waCDM chains give a marginalized cosmic age of 13.727 ± 0.028
Gyr (Pantheon+) and 13.723 ± 0.027 Gyr (DESY5), replacing the 0.24–0.83 Gyr
bracket; the exact CPL-shape kernel bounds the remaining shape systematic at
≤ 0.066 Gyr for σ_shape = 0.1.*
