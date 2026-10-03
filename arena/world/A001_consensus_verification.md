# A001 / Kepler — Consensus Verification Artifact
## Phase: phase4-consensus | Domain: Ratified consensus: origin of the universe

### 1. Consensus Statement (v1, ratified) — verbatim
> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

### 2. Scope of this artifact
This artifact does **not** open a new line of inquiry. It (a) audits each quantitative
claim in the Consensus Statement against established measurements, and (b) reports
*independent arithmetic* from standard constants that a third party can reproduce.
No value below is invented; measured values carry citations, derived values carry formulas.

### 3. Claim-by-claim audit

| # | Claim in statement | Established value | Source | Verdict |
|---|---|---|---|---|
| 1 | Age = 13.8 Gyr | 13.797 ± 0.023 Gyr (ΛCDM) | Planck Collaboration 2020, A&A 641, A6 (Planck 2018 VI) | Consistent (rounded) |
| 2 | Began in hot, dense state | Hot Big Bang expansion history; T increases as (1+z) | Standard cosmology | Consistent, with caveat (see §5) |
| 3 | ΛCDM + early inflation | Ω_m = 0.315, Ω_Λ = 0.685; r_{0.05} < 0.036 (95% CL) | Planck 2018 VI; BICEP/Keck 2021, PRL 127, 151301 | Consistent; inflation not directly detected |
| 4 | T_CMB = 2.72548 K | 2.72548 ± 0.00057 K | Fixsen 2009, ApJ 707, 916 (FIRAS) | Consistent |
| 5 | Y_p = 0.247 | 0.2471 ± 0.0003 (Planck+BBN); 0.2453 ± 0.0034 (metal-poor H II) | Planck 2018 VI; Cooke et al. 2018, ApJ 855, 102 | Consistent |
| 6 | Hubble tension 73.0 vs 67.4 | 73.04 ± 1.04 (SH0ES); 67.4 ± 0.5 (Planck) | Riess et al. 2022, ApJL 934, L7; Planck 2018 VI | Consistent with statement |
| 7 | Dark matter nature unknown | No confirmed non-gravitational signal | — | Correct open problem |
| 8 | Initial singularity | Not described by classical GR; quantum-gravity regime | — | Correct open problem |

### 4. Independent derived consistency checks (this work)

**Constants used** (SI): a_rad = 4σ/c = 7.5657e-16 J m^-3 K^-4; k_B = 1.380649e-23 J/K;
ħ = 1.054572e-34 J s; c = 2.99792458e8 m/s; m_p = 1.67262192e-27 kg;
ρ_c = 1.87847e-26 h^2 kg m^-3; h = 0.674; Ω_b h^2 = 0.02237.

**(a) CMB photon number density.** n_γ = [2ζ(3)/π²] (k_B T / ħc)³.
With T = 2.72548 K: k_B T = 3.76279e-23 J; ħc = 3.16153e-26 J m; ratio = 1190.18 m^-1.
n_γ = 0.243588 × (1190.18)³ = 4.106e8 m^-3 = **410.6 photons cm^-3** (standard ~411).

**(b) CMB energy density.** u_γ = a_rad T⁴ = 7.5657e-16 × (2.72548)⁴ = **4.17e-14 J m^-3**.

**(c) Baryon number density and photon-to-baryon ratio.**
ρ_c = 1.87847e-26 × 0.674² = 8.533e-27 kg m^-3; Ω_b = 0.02237/0.674² = 0.04924.
ρ_b = 4.202e-28 kg m^-3 → n_b = ρ_b/m_p = **0.2512 m^-3**.
η ≡ n_b/n_γ = 0.2512 / 4.106e8 = **6.12e-10** → n_γ/n_b = **1.63e9**.
This independently reproduces the standard Planck baryon-to-photon ratio η ≈ 6.1e-10.

**(d) Recombination temperature.** T(z) = T_0 (1+z). At z = 1090: T = 2.72548 × 1091
= **2.97e3 K** (~3000 K), the standard hydrogen recombination temperature.

**(e) Hubble tension significance (from the two quoted values).**
ΔH_0 = 73.04 − 67.4 = 5.64; σ_comb = √(1.04² + 0.5²) = 1.154 → **4.9σ**. This quantifies
the "tension" the statement names, using only the two cited measurements.

### 5. Caveat that is *not* a correction
"The universe began ... in a hot, dense state" is the consensus description of the
*observable* expansion history. Extrapolating to a literal t = 0 singularity is exactly
the open problem the statement itself flags; classical general relativity breaks down
near the Planck epoch (~1e-43 s). The statement is internally consistent because it lists
the initial singularity as unresolved.

### 6. What would change this ratification
- A confirmed nonzero tensor-to-scalar ratio r (direct evidence for inflation).
- A resolution of the H0 discrepancy by new physics or by identified systematics.
- A confirmed non-gravitational dark-matter detection.
- Any measured deviation of T(z) from T_0(1+z) at high z (tests the hot-Big-Bang scaling).
- A quantum-gravity framework replacing the initial singularity with a bounce/emergent phase.

### 7. Epistemic status
All eight claims above are either measured values with citations or arithmetic from
standard constants. Nothing here is fabricated. The Consensus Statement is **ratified
unchanged**: it is quantitatively consistent with established measurements, and its
listed open problems are correctly identified as open.

---
*A001 / Kepler, generation 0. Artifact written this turn. Reproducible with the constants in §4.*
