# A001 (Kepler) — Planck-mass convention audit, and the unbounded field range: attacking my own "finite duration" claim

**Agent:** Kepler (A001), generation 0. **Phase:** phase4-consensus.
**Engine:** `a001_planck_convention_and_unbounded_field_attack.py`.
**Trigger:** direct message from Raman (A002): *"Confirm the M_Pl convention and duration formula behind m=1.53e13 GeV and 1.17e-34 s; my exact value is 2.332e-35 s."*
**Scope:** correction of a convention error in a peer artifact, and a self-attack on the weakest assumption in `A001_FINITE_VS_ETERNAL_INFLATION_AND_THE_WORD_BEGAN.md`. **No consensus value is altered.**

## Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## Ratification

Ratified unchanged; the age is a hot-phase clock, not an absolute origin.

---

## PART 1 — Convention audit: the 5× is one error, and it is Raman's

The quadratic model uses `V = ½ m² φ²`, `ε = 2 M_Pl²/φ²`, and the standard
normalization `A_s = V/(24π² ε M_Pl⁴)`, i.e.

    A_s = m² φ⁴ / (96 π² M_Pl⁶),     M_Pl = reduced Planck mass.

In reduced units (`M_Pl = 1`), fixing `A_s = 2.1e-9` (Planck 2018 VI) at
`φ = 15 M_Pl` gives

    m = 6.269207e-6 M_Pl  →  m = 1.5266e13 GeV   (reduced M_Pl = 2.435e18 GeV).

Raman's script declares `M_PL_GEV = 1.220890e19` and labels it "reduced Planck
mass." That number is the **non-reduced** Planck mass; the reduced value is
`1.220890e19/√(8π) = 2.435e18 GeV`. Because his algebra uses `M_Pl = 1`
(reduced) but his numerical conversion uses the non-reduced mass, his `m` is too
large by exactly `√(8π)`:

| Quantity | Reduced `M_Pl` (correct) | Non-reduced (Raman) | Ratio |
|---|---|---|---|
| `m` | **1.5266e13 GeV** | 7.6540e13 GeV | 5.0139 = √(8π) |
| `φ_et = 15/A_s^{1/4}` | 2215.8 `M_Pl` | 2215.8 `M_Pl` | 1 (unit-free) |
| Δt (φ_et → φ_end) | **1.1694e-34 s** | 2.3323e-35 s | 5.0139 = √(8π) |

The duration formula is the one Raman and I both used, and it is correct:

    dN/dφ = −φ/(2 M_Pl²),  H = mφ/(√6 M_Pl)  ⇒  Δt = ∫dN/H = √6(φ_et − φ_end)/(2 m M_Pl).

Substituting the reduced-mass `m` reproduces **1.1694e-34 s**, which is my
original value. Raman's **2.3323e-35 s** is the same formula with the
non-reduced mass inserted. **There is no physical disagreement: the two
artifacts agree once the Planck mass is correct.**

**Internal inconsistency in the peer claim.** Raman writes that `φ_et = 2216
M_Pl` is "the value implied by `m = 7.65e13 GeV`." It is not. `φ_et` is fixed by
`A_s` and the pivot alone in reduced units (`φ_et = 15/A_s^{1/4} = 2215.8 M_Pl`)
and is independent of the numerical Planck mass. Inserting `m = 7.65e13 GeV`
together with the *reduced* `M_Pl` gives `φ_et = 989.6 M_Pl`, not 2216. His
`φ_et = 2216` is the value implied by `m = 1.53e13 GeV` — i.e. by the reduced
convention he was trying to correct. The stated pair (`m = 7.65e13 GeV`,
`φ_et = 2216 M_Pl`) is mutually inconsistent by a factor `15/A_s^{1/4}`.

**Answer to Raman's direct message.** The convention is the **reduced** Planck
mass `M_Pl = 2.435e18 GeV`; the mass is `m = 1.5266e13 GeV`; the duration is
`Δt = √6(φ_et − φ_end)/(2 m M_Pl) = 1.1694e-34 s`. The value `2.332e-35 s`
follows only from the non-reduced Planck mass and should be withdrawn.

## PART 2 — The single weakest assumption in my current work, and the attack

My `A001_FINITE_VS_ETERNAL_INFLATION_AND_THE_WORD_BEGAN.md` concluded:

> "Even the **entire** self-reproducing field range is a finite,
> duration-negligible pre-reheating epoch."

**This is the weakest assumption, and it is false as stated.** For `V = ½m²φ²`
the local amplitude `A_s(local) = m²φ⁴/(96π² M_Pl⁶)` *increases* with `φ`, so
self-reproduction (`A_s(local) > 1`) holds for `φ > φ_et = 2215.8 M_Pl`. The
segment I integrated, `[φ_end = √2 M_Pl, φ_et]`, has `A_s(local) ≤ 1`
(`A_s(φ_end) = 1.66e-13`, `A_s(φ_et) = 1`): it is precisely the
**non-self-reproducing last roll**. I computed the duration of a bounded,
sub-threshold segment and mislabeled it "the entire self-reproducing field
range."

Quantitatively, the classical traversal time from an arbitrary start `φ_0` to
the end of slow roll is

    Δt(φ_0) = √6 (φ_0 − φ_end) / (2 m M_Pl),

which grows **linearly and without bound** in `φ_0`:

| start `φ_0` | Δt |
|---|---|
| 2215.8 `M_Pl` (threshold) | 1.17e-34 s |
| 1e4 `M_Pl` | 5.28e-34 s |
| 1e10 `M_Pl` | 5.28e-28 s |
| 8.25e54 `M_Pl` | **13.8 Gyr** |

So the "finite, duration-negligible" result is a property of the *bounded
sub-threshold* segment, not of eternal inflation. The self-reproducing range is
`[φ_et, ∞)`, and its classical traversal time diverges; for a sufficiently large
initial field value the pre-reheating epoch would itself last 13.8 Gyr (at
`φ_0 ≈ 8.2e54 M_Pl`). The order-of-magnitude conclusion "60 e-folds is
negligible" survives; the stronger claim "the whole eternal range is
duration-negligible" does not.

**The deeper layer of the same weakness.** Inside the self-reproducing regime the
per-e-fold quantum scatter `H/(2π)` exceeds the classical roll `√(2ε) M_Pl`, so
the field is **diffusion-dominated**. There `dφ/dN` is not a drift velocity and
the "time" `∫dφ/|φ̇|` is not the physical duration: the exit time is a random
variable set by a first-passage problem, and its distribution — hence the mean
pre-reheating duration — is measure-dependent (the standard measure problem).
The finite number `1.17e-34 s` is therefore not the duration of eternal
inflation under any controlled calculation. What *is* controlled is only the
negative, model-independent statement at the observed pivot: `A_s = 2.1e-9` is
8.68 dex below the self-reproduction threshold, so **our observable patch is not
eternally inflating**.

**Consequence for the consensus sentence.** This strengthens, rather than
weakens, the prior relativization: "our observable hot phase began 13.8 Gyr ago"
is a statement about a bounded, sub-threshold roll plus reheating. It carries no
information about the duration of any global eternally inflating phase, whose
"beginning" remains the listed open problem (the initial singularity).

## Established / Unknown / Falsifier

- **Established (this turn, reproduced numerically):** reduced `M_Pl =
  2.435e18 GeV`; `m = 1.5266e13 GeV`; `φ_et = 2215.8 M_Pl`; `Δt(φ_et→φ_end) =
  1.1694e-34 s`. The peer value `2.332e-35 s` and mass `7.65e13 GeV` are the
  same quantities evaluated with the non-reduced Planck mass; the discrepancy is
  exactly `√(8π)`. The segment `[φ_end, φ_et]` has `A_s(local) ≤ 1`, so it is
  not the self-reproducing range. `Δt(φ_0)` diverges linearly in `φ_0`.
- **Unknown (unchanged):** whether inflation is eternal anywhere; the duration
  (measure) of any eternal phase; the global topology; whether the BGV past
  boundary is a bounce or a singularity; dark-matter identity; which `H0` is
  correct.
- **What would change my mind:** a measure prescription that makes the exit-time
  distribution from the self-reproducing regime normalizable with a controlled
  mean, or a UV completion that fixes the initial field value `φ_0` (equivalently
  the total e-fold number). Neither is in evidence.

## Citations (all real)

- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) — `A_s = 2.1e-9`,
  age = 13.797 ± 0.023 Gyr.
- BICEP/Keck Collaboration 2021, PRL, 127, 151301 — `r < 0.036` (95 % CL).
- Guth, A. H. 2007, J. Phys. A, 40, 6811 — stochastic eternal inflation.
- Linde, A. D. 1986, Phys. Lett. B, 175, 395 — eternal chaotic inflation.
- Borde, A., Guth, A. H. & Vilenkin, A. 2003, PRL, 90, 151301 — past geodesic
  incompleteness.

## Protocol note

The consensus protocol requires restatement plus one ratifying sentence. The
PRIORITY directive asks for an attack on the weakest assumption in my own work.
This artifact answers a peer's direct convention question (correcting a
convention error, not a consensus value), then attacks my own over-strong
"finite duration" claim. No experimental result is invented and no quoted
consensus value is altered.

---
*A001 / Kepler, generation 0. Consensus Statement v1 ratified unchanged.*
