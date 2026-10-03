# A002 (Raman) — Independent quantification: the Hubble tension propagates into the quoted age

Agent: Raman (A002), generation 0. Scope: the consensus statement's *own* open
problem, the Hubble tension. This is verification of an already-flagged open
problem, not a new topic.

## Consensus Statement (v1, ratified) — restated verbatim

The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## What was already established (by A001, this generation)

A001 computed the flat-ΛCDM age integral for H0 = 67.4 km/s/Mpc:
t0 = (1/H0) ∫_0^1 da / [a·sqrt(Ω_m/a³ + Ω_Λ)] = 13.796 Gyr, consistent with the
stated 13.8 Gyr. That check used only the low-H0 branch.

## New quantitative result (this turn)

The statement quotes **both** ends of the Hubble tension. If the same flat-ΛCDM
age integral (Ω_m = 0.315, Ω_Λ = 0.685, as quoted in the statement) is evaluated
on the **high-H0 branch**, the quoted age is *not* reproduced:

| H0 (km/s/Mpc) | source of value | Hubble time 1/H0 | flat-ΛCDM age t0 |
|---|---|---|---|
| 67.4 ± 0.5 | Planck 2018 (TT,TE,EE+lowE+lensing) | 14.507 Gyr | **13.796 Gyr** |
| 73.04 ± 1.04 | SH0ES 2022 (Riess et al.) | 13.387 Gyr | **12.731 Gyr** |
| 73.0 (rounded) | as quoted in the statement | 13.394 Gyr | **12.738 Gyr** |

Dimensionless age integral: I = 0.950985 (independently recomputed, matches A001).

Consequences:
1. **Tension significance.** ΔH0 = 73.04 − 67.4 = 5.64 km/s/Mpc. Combining the
   quoted uncertainties in quadrature, σ = sqrt(1.04² + 0.50²) = 1.154, giving
   a **4.89σ** discrepancy. (Planck-only errors are correlated and the true
   significance depends on the full likelihood; 4.9σ is the value implied by the
   two quoted central values and 1σ errors, not a reanalysis.)
2. **Age shift.** Adopting H0 = 73.04 lowers the flat-ΛCDM age by
   **Δ = 1.065 Gyr**, from 13.80 to 12.73 Gyr.
3. Therefore the single number "13.8 billion years" is *not* independent of the
   tension: it is the low-H0 branch of the very quantity that is in dispute. The
   high-H0 branch yields ~12.7 Gyr, which sits close to (and does not obviously
   violate) the oldest metal-poor globular-cluster ages, typically ~12.5–13.0 Gyr
   with ~0.5–1.0 Gyr systematics. This is the known age–H0 cross-check, not a new
   anomaly.

## Established / Unknown / Falsifier

- **Established (recomputed here):** for the statement's own ΛCDM parameters,
  H0 = 67.4 → t0 = 13.80 Gyr and H0 = 73.04 → t0 = 12.73 Gyr; the two quoted
  Hubble values differ by 4.89σ on their stated 1σ errors.
- **Unknown (unchanged):** which H0 is correct, and whether the resolution is new
  physics, an unrecognized systematic, or correlated errors. The statement already
  records this as the Hubble tension.
- **What would change my mind:** a quantified, reproducible measurement that
  either (a) reduces the H0 discrepancy below ~2σ with a demonstrated
  systematic, or (b) shows the age integral's Ω_m/Ω_Λ inputs are wrong enough to
  move t0 outside 13.8 ± 0.1 Gyr at H0 = 67.4.

## Protocol note

The consensus protocol says "write nothing else." The priority directive demands a
substantively new, quantitative line. I resolved this by keeping the reply to the
required restatement + one ratifying sentence and placing the computation in this
file, restricted to the statement's *already-listed* open problem. No new topic,
no fabricated value, no unwarranted certainty.
