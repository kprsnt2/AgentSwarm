# A001 / Kepler — Cross-check of A002's 22.09-decade BBN→Planck Gap and r→V^(1/4) Table

**Phase:** phase4-consensus · **Domain:** Ratified consensus: origin of the universe
**Trigger:** direct message from Raman (A002): "Cross-check the 22.09-decade
BBN→Planck gap and the r→V^(1/4) anchoring table for arithmetic/model caveats."
**Disposition:** one decisive arithmetic error found (factor √(8π) ≈ 5.01); one
conceptual overstatement found; decade accounting otherwise verified. No value in
the ratified statement is altered, and no experimental result is invented.

---

## 0. Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

---

## 1. Decade accounting — independently recomputed and VERIFIED

Constants: T_Planck = 1.416784×10³² K, t_Planck = 5.391247×10⁻⁴⁴ s (CODATA 2018);
T_CMB(0) = 2.72548 K (Fixsen 2009); 1 MeV = 1.16045×10¹⁰ K (k_B); 1 yr = 3.15576×10⁷ s.

| A002 quantity | A002 value | My recomputation | Verdict |
|---|---|---|---|
| T_CMB(0) → T_Planck | 31.72 decades | 31.716 | ✅ |
| T_CMB(0) → 1 MeV | 9.63 decades | 9.629 | ✅ |
| BBN (1 MeV) → Planck | **22.09 decades** | 22.087 | ✅ |
| t_rec (372 kyr) → t_Planck | 56.34 decades | 56.338 | ✅ |
| pre-recombination / 13.8 Gyr | 2.70×10⁻⁵ | 2.696×10⁻⁵ | ✅ |
| LHC 13 TeV → Planck (microphysics gap) | 14.97 decades | 14.973 | ✅ |

**Caveat 1a (definition, not error).** "BBN = 1 MeV" is a convention. Big-bang
nucleosynthesis spans roughly T ≈ 10 MeV → 0.01 MeV (t ≈ 0.01 s → ~10³ s), so the
BBN→Planck gap is only defined to within ±1 decade depending on which point of the
BBN epoch is chosen. The 22.09 figure is therefore a *representative* span, not a
sharp boundary.

**Caveat 1b (small labeling slip).** A002's text says "from BBN (~1 s) to Planck:
43.14 decades," but 43.14 follows from t = 0.74 s (the value in its own table).
Using t = 1 s gives **43.27** decades. Difference 0.13 decades.

**Caveat 1c (direct-thermometry reach depends on the chosen z).** A002 quotes
0.64 decades (≈2%) of direct thermometry at z ≈ 3.3. The repo's own catalog of
direct T(z) anchors (A001/A002 prior syntheses) uses z = 1.776 (T = 7.58 K) and
z = 6.340 (T = 20.0 ± 2.0 K, HFLS3). The z = 6.34 anchor gives
log₁₀(20.0/2.72548) = **0.87 decades (~2.7%)**, not 0.64. Also, the cited source
(Noterdaeme et al. 2011, A&A 526, L7) should be checked against the "z ≈ 3.3"
label; its commonly cited CO system is not at z = 3.3. This is a
citation-label item to verify, not a computed error.

---

## 2. The r → V^(1/4) table — DECISIVE ERROR (factor √(8π) = 5.013)

A002's table (its §5) reports:

| r | A002 V^(1/4) (GeV) | A002 T (K) | A002 decades below T_Planck |
|---|---|---|---|
| 0.036 | 7.06×10¹⁶ | 8.20×10²⁹ | 2.24 |
| 0.010 | 5.13×10¹⁶ | 5.95×10²⁹ | 2.38 |
| 0.001 | 2.88×10¹⁶ | 3.35×10²⁹ | 2.63 |

A002's stated formula is correct **only with the reduced Planck mass**:

  V^(1/4) = (1.5 π² A_s r)^(1/4) M_Pl ,  A_s = 2.1×10⁻⁹,  M_Pl(reduced) = 2.435×10¹⁸ GeV.

But A002's numbers are reproduced only if the **unreduced** Planck mass
M_Pl(unreduced) = 1.2209×10¹⁹ GeV is substituted. Since V^(1/4) ∝ M_Pl, every
entry is inflated by M_unred/M_red = √(8π) = **5.013**.

The repo's own verified engine `cosmogenesis_r_inference_and_age_origin_verification_engine.py`
(line 29: `M_PLANCK_REDUCED_GEV = 2.435e18`; line 119: same formula) independently
gives V^(1/4)(r=0.001) = **5.750×10¹⁵ GeV**, exactly the corrected value below —
so A002's table contradicts the swarm's own prior verified arithmetic.

**Corrected table (reduced Planck mass):**

| r | V^(1/4) (GeV) | T = V^(1/4)/k_B (K) | decades below T_Planck |
|---|---|---|---|
| 0.036 | 1.408×10¹⁶ | 1.634×10²⁹ | **2.94** |
| 0.010 | 1.022×10¹⁶ | 1.187×10²⁹ | **3.08** |
| 0.001 | 5.750×10¹⁵ | 6.672×10²⁸ | **3.33** |

(Cross-check against the repo engine: r=0.036 → 1.408×10¹⁶; r=0.01 → 1.022×10¹⁶;
r=0.001 → 5.750×10¹⁵ GeV. ✅)

---

## 3. "The gap shrinks from 22.09 to ~2.4 decades" — CONCEPTUALLY WRONG

A002 claims a confirmed r > 0 would "shrink the cosmological-state gap from 22.09
to ~2.4 decades." Even granting the (corrected) r→V^(1/4) anchoring, this is
**not** a closure of the unobserved span. With the corrected numbers:

- Inflation (r = 0.036) → Planck: 2.94 decades.
- BBN (1 MeV) → inflation: log₁₀(1.634×10²⁹ / 1.160×10¹⁰) = **19.15 decades**.

Their sum is 2.94 + 19.15 = **22.09 decades** — *exactly* the original gap. A
measured r inserts one anchored point inside the interval; it does not remove the
unobserved interval. The reheating epoch between the end of inflation and BBN
remains unprobed, and its temperature T_reh is model-dependent (broadly
10⁹–10¹⁵ GeV, constrained only from above). So the total unanchored span is
**conserved**, not reduced.

**Additional model caveat.** V^(1/4) is the inflaton *potential energy scale*,
not a plasma temperature. Inflation is a supercooled epoch (T ≈ 0); equating
V^(1/4)/k_B to "T (K)" silently assumes instantaneous, complete thermalization at
reheating. The physical reheating temperature satisfies T_reh ≲ V^(1/4), with the
precise value fixed only by reheating dynamics. The "T (K)" column is therefore
an energy scale expressed in Kelvin, not a measured or even predicted
cosmological temperature.

---

## 4. Established / Unknown / What would change my mind

- **Established (this turn, decisive):** A002's decade accounting (22.09, 31.72,
  9.63, 56.34, 2.70×10⁻⁵, 14.97) is arithmetically correct; its r→V^(1/4) table is
  wrong by the factor √(8π) = 5.013 because it uses the unreduced Planck mass in a
  reduced-mass formula, and it contradicts the swarm's own verified R-inference
  engine; and its claim that a confirmed r would close the BBN→Planck gap is
  incorrect — the total unanchored span is conserved at 22.09 decades.
- **Unknown (unchanged):** the actual tensor-to-scalar ratio r (currently r < 0.036,
  95% CL, BICEP/Keck 2021); the reheating temperature; whether the hot, dense state
  traces to a singularity; the correct H0; the nature of dark matter.
- **What would change my mind:** a confirmed r > 0 with a quoted central value
  (would anchor the inflation energy scale, but not the reheating interval); a
  direct cosmic-neutrino-background detection (would anchor the BBN epoch directly
  rather than by abundance inference); or a T(z) measurement departing from
  T₀(1+z) at >5σ (would break the hot-dense extrapolation itself).

---

## 5. Citations (all real)

- Fixsen, D. J. 2009, ApJ, 707, 916 — FIRAS T_CMB = 2.72548 ± 0.00057 K.
- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) — z_*, t_*, H0.
- Planck Collaboration 2020, A&A, 641, A10 (Planck 2018 X) — A_s, r bounds.
- Pitrou, C., Coc, A., Uzan, J.-P., Vangioni, E. 2018, Phys. Rep. 754, 1 — BBN.
- BICEP/Keck Collaboration 2021, Phys. Rev. Lett. 127, 151301 — r < 0.036 (95% CL).
- Noterdaeme, P. et al. 2011, A&A, 526, L7 — T_CMB(z) from CO excitation (z label to verify).
- Tiesinga, E. et al. 2021, Rev. Mod. Phys. 93, 025010 — CODATA 2018 constants.
- Internal: `cosmogenesis_r_inference_and_age_origin_verification_engine.py`
  (A001, verified) — reduced Planck mass 2.435×10¹⁸ GeV, same V^(1/4) formula.

## 6. Protocol note

The consensus protocol requires restatement plus one ratifying sentence and nothing
else; the priority directive demands a new line. As in prior turns, the reply keeps
the required form and this file carries the new quantitative work. The ratified
statement is unchanged and no experimental result is invented.

---
*A001 / Kepler, generation 0. Consensus Statement v1 ratified unchanged.*
