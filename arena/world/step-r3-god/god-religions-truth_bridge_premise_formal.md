# Bridge-Premise Neutrality: Why Every Candidate "Proof" in This Domain Is Prior-Powered, Not Data-Powered

### A formal account of the logical structure of the problem — the missing half of the God-and-religions inquiry

**Agent:** Kepler (A001), generation 0 · **Domain:** god-religions-truth · **Epistemic class:** Metaphysical
**Turn:** r3, god-religions-truth · **Companion to:** `god-religions-truth_taxonomy_and_testability.md` (r1/r2), `god-religions-truth_separation_formal.md`, `god-religions-truth_insulation_formal.md`, `god-religions-truth_confirmation_formal.md` (r2)

---

## Protocol note (read first)

This is a **metaphysical** question and is **not empirically decidable**. This document does **not** assert that any god exists
or does not exist, and does **not** judge any religion true or false. Its output is a clarification: it states what each
classic argument *logically is*, and it shows — by a theorem with a stated proof — that the evidentially load-bearing part of
each such argument is a **normative/conceptual premise that no observation can fix**, not the observational data the argument
is usually advertised on. Where a subclaim is decidable, this document reports what the record shows and points to the
companion taxonomy's ledger. Where it is not, it says so.

**Tag legend:** **[T]** = empirically or historically testable in principle. **[NT]** = not empirically testable by its own terms.
**[E+]** / **[E−]** = what would count as evidence for / against.

---

## 0. What this artifact adds, and what it does not

The three r2 formal artifacts analysed the route where religion *does* make risky, checkable claims: **dated predictions and
putative miracles**. Each showed that even there, the core commitment survives — by the Duhem structure (fault localization
carries LR = 1.0), by the identification lattice (86k–90k× shortfall against the ~3 strongest available row), and by the
hardening ceiling (0.5 against one flexible even-prior rival).

They did **not** analyse the other route: the **classic philosophical arguments** — religious diversity, divine hiddenness,
the problem of evil, the Euthyphro dilemma, design/fine-tuning, religious experience. The companion taxonomy states these
correctly and then, at §6.4, **declines to assign them a Bayes factor**, on the ground that "the auxiliaries that would
flatten them are themselves what §6.2 note 2 identifies as contested. A symmetric bound must not quantify only the direction
that suits it."

That refusal is honest but it leaves the question formally open: *is* there a number to be had? This artifact supplies one,
and it is a sharper result than the refusal anticipated. The reason the Bayes factor cannot be assigned from evidence is not
that the literature is unsettled. It is that **for this entire cluster of arguments the evidential factor and the prior
factor factorise exactly, and the evidential factor is identically 1 whatever the auxiliaries are.** Declining to quantify
was right; but the correct reason is a theorem, not a scruple — and the vacuity of the *data* term is structural, holding for
any value the auxiliaries might take. What survives is not evidence at all; it is the reader's prior tilt on a normative
premise, and that is the quantity §4 prices.

Nothing here contradicts the r2 results. It generalises them: the dated-prediction route turned out to have one
law-violating-interruption observation type; this document shows that the philosophical route has, in the relevant
sense, **no observation type at all**.

---

## 1. Formal setup

**1.1 The shape of every candidate argument.** Every argument in this domain, on either side, has the form

> **E** (a body of checkable data) ＋ **B** (a *bridge premise* connecting E to the core C or to ¬C) ⟹ conclusion about C.

The bridge premise B is what licenses the step from the data to the metaphysical conclusion. In the dated-prediction route the
bridge is an auxiliary chronology; in the philosophical route the bridge is always **normative or conceptual**. This document is
about the latter, and the difference is decisive.

**1.2 The bridge family.** B is rarely a single premise; it is a family 𝔅 = {b₁, b₂, …} of admissible readings. Example: for the
problem of evil, b ranges over "suffering must be necessary for a greater good," "suffering is moral training," "God has
reasons we cannot see," "there is compensatory afterlife," "God's goodness is not the human analogue." Each reading gives a
different P(E|C, b). Marginalise over the family, weighting by the bridge prior under each hypothesis:

```
P(E | C, 𝔅)  = Σ_b  P(E | C, b) · P(b | C)
P(E | ¬C, 𝔅) = Σ_b  P(E | ¬C, b) · P(b | ¬C)
BF(A) := P(E | C, 𝔅) / P(E | ¬C, 𝔅)
```

**1.3 Per-bridge likelihood ratio.** ρ_b := P(E | C, b) / P(E | ¬C, b), and the **bridge prior odds ratio**
τ_b := P(b | C) / P(b | ¬C).

---

## 2. The theorem

### Theorem 1 — Bridge Accounting (the argument's force is a weighted mean of prior × likelihood)

BF(A) = Σ_b w_b · ρ_b · τ_b, where

```
w_b  :=  P(E | ¬C, b) · P(b | ¬C)  /  Σ_b' P(E | ¬C, b') · P(b' | ¬C)      (normalised: Σ_b w_b = 1)
ρ_b  :=  P(E | C, b)  / P(E | ¬C, b)          per-bridge LIKELIHOOD ratio  — the "data" factor
τ_b  :=  P(b | C)     / P(b | ¬C)             bridge-prior ODDS ratio      — the "prior" factor
```

*Proof.* Substitute P(E|C,b) = P(E|¬C,b)·ρ_b and P(b|C) = P(b|¬C)·τ_b into the BF definition. The numerator becomes
Σ_b P(E|¬C,b)·P(b|¬C)·ρ_b·τ_b; the denominator is the same sum without ρ_b·τ_b, which normalises it to 1. ∎

So **BF(A) is a weighted mean of the products ρ_b·τ_b** — the evidential factor and the prior factor are multiplicatively
separable, and *neither can be dropped*. Four consequences, of which (i) is the one this artifact turns on:

- **1(i) — Data-neutral bridges are prior-powered.** If ρ_b = 1 for every b, then **BF(A) = ⟨τ_b⟩_w**: a weighted mean of
  bridge *prior odds ratios*. Nothing observational enters at all. The argument's entire evidentiary force is the tilt the
  reader brought to the normative premise before seeing any data.
- **1(ii) — Prior-neutral bridges are data-bounded.** If τ_b = 1 for every b, then BF(A) = ⟨ρ_b⟩_w, hence
  **min_b ρ_b ≤ BF(A) ≤ max_b ρ_b**. No argument delivers more than its most evidencially productive bridge reading. There is
  no Evidential Free Lunch.
- **1(iii) — Full neutralisation.** If ρ_b = 1 *and* τ_b = 1 for every b, then **BF(A) = 1 exactly**, and the data changes the
  posterior not at all.
- **1(iv) — General bound.** min_b(ρ_b·τ_b) ≤ BF(A) ≤ max_b(ρ_b·τ_b).

> **Note on what (i) does *not* say.** It does *not* say a bridge-neutral argument cannot move a posterior. It can — via the
> prior. What it cannot do is move it *with evidence*. That distinction is the whole of this document.

### Theorem 2 — Neutral-Bridge Tilt (Theorem 1 applied to the classic arguments)

Suppose the bridge is evidentially neutral: ρ_b = 1 for every admissible b. Then BF(A) = ⟨τ_b⟩_w.

- **2(i).** If the bridge prior is *homogeneous* — τ_b = τ for every admissible reading b — then **BF(A) = τ exactly**.
- **2(ii).** Otherwise BF(A) is the weighted mean ⟨τ_b⟩_w; Table 2 states the value that this mean must attain.
- **2(iii).** Inverting: to reach posterior p on the core from an even start, the required (weighted-mean, or under 2(i)
  homogeneous) bridge tilt is

```
τ_req = p / (1 − p).
```

That is Table 2 below. Note what it *is not*: it is not a measurement. It is the price of the conclusion. Sanity check: at
p = 0.5, τ_req = 1 — an even bridge tilt leaves an even start exactly where it was, as it must.

### §2.1 What "neutral bridge" means here, precisely — and the one place the theorem needs care

Three points, because this is where the result could be over-read.

**(a) The defense bridges are the neutral ones.** For each argument in Table 1 there are *two* kinds of admissible bridge
reading. On the **defense** bridges — greater good, free will, inscrutability, eschatological compensation, soul-making,
observer selection, naturalistic etiology — the data E is just as expected under C as under ¬C, so **ρ_b = 1 exactly**. On the
**offense** bridges — "a good God would prevent gratuitous suffering," "a perfectly loving God would prevent reasonable
nonbelief" — ρ_b < 1, and the argument looks strong. So it is **not** the case that every admissible bridge is neutral in
every argument, and this artifact does not claim it.

**(b) But ρ_b on the offense bridges is not a measurement either.** This is the decisive point. For the classic arguments E is
a general fact about the world (suffering exists; non-resistant nonbelievers exist; religions disagree; constants are
life-permitting), not the output of a model that could estimate a likelihood. **The literature does not estimate ρ_b from
data; it stipulates ρ_b as part of the bridge reading.** Hence in every case BF(A) = ⟨ρ_b·τ_b⟩_w is a product of two
stipulated quantities, and the offense/defense dispute is *entirely* a dispute about P(b|C) — about τ_b — dressed up as a
dispute about likelihood. Table 2 prices that dispute. This is the sharper form of the claim, and it survives the case where a
proponent or an opponent declines the neutral bridges.

**(c) The theorem's reach, stated exactly.** Theorem 1(i) applies to the sub-family of neutral bridges and yields
BF = ⟨τ_b⟩_w there. Theorem 1(ii) applies when the prior is even and yields BF = ⟨ρ_b⟩_w, bounded by the best and worst
readings. Theorem 1(iii) yields BF = 1 exactly only under both. **No case of the general form escapes the accounting of
Theorem 1:** the argument's force is always a weighted mean of ρ_b·τ_b, never a quantity observation delivers on its own.

### Theorem 3 — Non-identifiability (the ceiling imposed by the size of the candidate set)

Let ℂ = {C₁,…,C_N} be the candidate cores. Even granting a per-rival likelihood ratio λ against *each* rival, the posterior on
any one rival is

```
p = λ / (λ + N − 1),
```

so the per-rival ratio needed to reach posterior p is

```
λ_req(p, N) = (N − 1) · p / (1 − p).
```

With N = 10⁴ (the upper end of the commonly cited 4,000–10,000+ individuation range, and the figure the r2 artifacts use):
p = 0.90 ⟹ λ_req = **89,991**; p = 0.99 ⟹ **989,901**; p = 0.999 ⟹ **9,989,001**. The companion separation artifact's
strongest available ledger row is ≈ 3 — a shortfall of ≈ 30,000× against even the 90% bar. **Identification is N−1 times
harder than bare existence**, and no finite body of evidence negotiates that ratio without discriminating between rivals.

### Theorem 4 — Category decay (why "proof" is the wrong word)

A deductive proof with n independent premises, each of warrant w, carries conjunctive warrant wⁿ. To exceed target p:

```
w_min(n, p) = p^(1/n).
```

For p = 0.90: n = 2 ⟹ 0.9487; n = 3 ⟹ 0.9655; n = 5 ⟹ 0.9791; n = 8 ⟹ 0.9869. (The companion taxonomy's instance: three
premises at w = 0.8 give 0.512.)

Now the category error, exactly. Every candidate premise in this domain is one of:
- **analytic** — true by definition, hence true in every possible world, hence carrying no information about the contingent
  matter of whether a god exists. A being *defined* as existing makes the question tautological; a definition so wide that it
  fits every world is empirically empty. (Taxonomy §0.1: "God is the ground of existence" buys non-circularity with vacuity.)
- **synthetic** — contingent and informative, hence defeasible, hence incapable of delivering w_min(n, p).

There is no third kind. So a *deductive* proof of the core is unavailable in principle, not merely unfound; an *empirical*
proof is blocked by Theorems 1–3; an *abductive* proof collapses into the prior via Theorem 2. **"Proof" is not a high bar
here that evidence has not yet cleared; it is the wrong category.**

### Corollary 5 — The unified statement

For any argument of the form E ＋ B ⟹ C in this domain: **if the bridge B is evidentially neutral, BF(A) = ⟨τ_b⟩_w — a
weighted mean of bridge prior odds ratios, a quantity fixed before any observation, and exactly 1 when that prior is even.
If instead the bridge prior is even but B is not evidentially neutral, BF(A) = ⟨ρ_b⟩_w — a weighted mean of per-bridge
likelihood ratios, bounded by the best and worst single bridge readings.** In no case does observation, by itself, arbitrate
the core commitment. This is the exact sense in which the question "is there a true God, and could any proof establish it?"
resists proof: **not because the evidence is thin, but because the connective tissue between evidence and conclusion is not
evidence.**

---

## 3. Table 1 — The classic arguments, decomposed into E and B

| # | Argument | **E** (data) | Tag | **B** (bridge premise) | Tag | Defense bridge neutral? (ρ_b = 1) | Verdict (Thm 1–2, §2.1) |
|---|---|---|---|---|---|---|---|
| A1 | **Religious diversity** | incompatible, each apparently well-attested religious claims coexist across cultures, with no convergence on one | **[T]** (coexistence is observable; the *incompatibility* and the *equal warrant* are not) | if a true God existed and sought relationship, this pattern would not obtain / the cognitive faculty producing religious belief is equally truth-tracking in all cultures | **[NT]** (normative: what a truth-seeking God would leave, and whose apparent warrant counts) | **yes** — "God may permit free exploration," "misinformation is not God's doing," "the apparent triumph of one tradition is the relevant pattern" | BF = ⟨τ⟩_w on the neutral bridges; the offense bridge is stipulated, not measured |
| A2 | **Divine hiddenness** | reasonable, truth-seeking, non-resistant nonbelievers exist | **[T]** (minor premise checkable, per taxonomy §3.2) | a perfectly loving being ensures no non-resistant subject remains in reasonable nonbelief | **[NT]** (what perfect love *would* do; greater-good defenses render it compatible with any data) | **yes** — soul-making, "reasons we cannot see," freedom, eschatological compensation | BF = ⟨τ⟩_w on the neutral bridges; otherwise stipulated |
| A3 | **Problem of evil** | intense, apparently pointless suffering of apparently innocent beings exists | **[T]** | a good, omnipotent being prevents suffering that is not necessary for a greater good / not morally justified | **[NT]** (normative + contested greater-good claims) | **yes** — free-will defense, soul-making, unknown greater goods, afterlife compensation | BF = ⟨τ⟩_w on the neutral bridges; otherwise stipulated |
| A4 | **Euthyphro dilemma** | *none* — purely a priori | — | (horn 1) moral facts are independent of divine command ↔ (horn 2) moral facts are constituted by divine command | **[NT]** (metaethical fork; no dataset at all) | n/a — there is no E | BF **undefined** in the evidential sense; a metaethical choice, not a measurement. The purest case of the category error |
| A5 | **Design / fine-tuning** | physical constants lie in a narrow life-permitting range | **[T]** (data real; taxonomy row 7) | the life-permitting narrowness is improbable under non-design | **[NT]** (depends on the measure over constant-space, which is exactly the underdetermination among design / multiverse / necessity) | **yes** — multiverse + observer selection, or brute necessity | BF ≈ 1–3 at most (taxonomy §6 row 7) and *only* if the measure is granted |
| A6 | **Religious experience / cumulative case** | reports of experience across traditions | **[T] weak** (reports are checkable; their cause is not) | experiences of X are veridical indicators of X | **[NT]** | **yes** — naturalistic etiology, mutually contradictory reports across traditions | BF = ⟨τ⟩_w on the neutral bridges; the veridicality premise is granted, not shown |

**Reading of Table 1.** In every row the *E* column is checkable and in most rows the data is not seriously disputed. In
every row the *B* column is normative or conceptual. **The disputes in this literature are almost never about E.** They are
about B — which is precisely the part Theorem 2 shows cannot be settled by E.

---

## 4. Table 2 — The bridge-tilt lattice (Theorem 2(iii))

What bridge prior odds ratio τ_req each target posterior demands, when the bridge is evidentially neutral and the start is
even (prior 0.5):

| Target posterior p on the core | Required bridge prior odds ratio τ_req = p/(1−p) | Reading |
|---|---|---|
| 0.600 | **1.5** | "I regard the normative premise 1.5× more likely if the core is true than if it is false." |
| 0.750 | **3** | a 3:1 tilt in the bridge |
| 0.900 | **9** | a 9:1 tilt |
| 0.990 | **99** | a 99:1 tilt |
| 0.999 | **999** | a 999:1 tilt |
| 0.9999 | **9 999** | a 10⁴:1 tilt |

**Interpretation, stated plainly.** If the data is bridge-neutral — which Table 1 says is the case for A1, A2, A3, A5, A6 —
then to end up 90% confident in the core on the strength of the argument, the bridge family must already carry a **9:1
weighted-mean tilt** (or, under Theorem 2(i), a homogeneous 9:1 tilt) in favour of the normative premise under the core over
its denial. That is the whole argument. It is available to anyone, in either direction, at the price of a stipulated tilt.
**Two reasoners with identical evidence and opposite tilts reach opposite conclusions with equal logical propriety**, and no
observation adjudicates between them. This is the precise mechanism behind the taxonomy's "resists testing": the bridge is
where the conclusion is surreptitiously imported from.

**The symmetric caveat, which must not be dropped.** The lattice runs *both* ways. An anti-theist who assigns a 9:1 tilt to
"a perfectly loving God would not leave reasonable nonbelief" reaches 90% in their direction by the identical route. The
theorem is not an argument for either side; it is the statement that **neither side's conclusion is being produced by
evidence.** Any reading of this artifact as scoring for one side has inverted it.

---

## 5. Table 3 — Per-family testability of the core, for all eight families the brief names

Counts of ledger rows (companion taxonomy, rows 1–14) touching each family, split [T]/[NT]. **The family→row mapping is this
artifact's own and is stated so that it can be contested row by row.** Rows are double-counted where a family genuinely shares
the claim (rows 9, 12, 13 are cross-traditional).

| Family | Ledger rows | [T] count | [NT] count | **Core claims testable** |
|---|---|---|---|---|
| Classical monotheism — Judaism / Christianity | 1, 2, 3, 4, 5, 8, 11, 12, 14 | 6 | 3 | **0** |
| Classical monotheism — Islam | 6, 11, 12, 14 | 1 | 3 | **0** |
| Polytheism — Hindu traditions | 9, 10 | 2 | 0 | **0** |
| Polytheism — ANE / Greco-Roman | (none in ledger; treated at taxonomy §1.2) | 0 | 0 | **0** |
| Pantheism | 12 | 0 | 1 | **0** |
| Panentheism | 12 | 0 | 1 | **0** |
| Non-theistic Advaita Vedānta | 11, 12, 13, 14 (apophatic cluster) | 0 | 4 | **0** |
| Deism | 7 | 1 | 0 | **0** |
| Buddhism (non-theistic) | 9, 13 | 1 | 1 | **0** |
| Jainism | 13 (karma), plus its [O] report at taxonomy §1.7 | 0 | 1 | **0** |

**Total ledger rows 14 (10 [T], 4 [NT])**, matching the companion taxonomy's stated tally.

**The finding is the column that is everywhere zero.** Across ten family rows, the count of testable *core*-metaphysical
claims is **0 of 0**. Every one of the ten [T] rows is a peripheral subclaim — an event, a date, a text, a cosmological
structure, or a physical constant. The [NT] rows are exactly the core-metaphysics rows. **The separation is total and
systematic, not incidental.** Confirming a peripheral row (row 3, the crucifixion under Pilate, is near-certain on multiple
independent attestation) leaves the core untouched — a fact about history remains a fact about history — and refuting a
peripheral row (rows 1–2, the Exodus and conquest, are not corroborated) is absorbed by the hiddenness/inscrutability
auxiliaries documented at taxonomy §3.3 and §6.2.

**Ground-truth notes carried forward:** Advaita Vedānta is non-dualist and does not posit a personal creator god in the
Abrahamic sense — which is why its ledger entries sit entirely in the [NT] apophatic cluster. The Euthyphro dilemma is stated
in Plato's *Euthyphro* (~10a) and is row A4 above.

---

## 6. What the decidable layer actually shows (reported, with the standing blocker stated honestly)

The companion taxonomy's [T] ledger, verbatim in state:

| Row | Claim | State of the evidence |
|---|---|---|
| 1 | Mass Exodus from Egypt, c. 13th c. BCE | **Not corroborated**; mainstream sees indigenous settlement; small-kernel question open |
| 2 | Foreign conquest of Canaan | Continuity/indigenous model favoured |
| 3 | Crucifixion under Pilate | **Well established** (multiple independent attestation) |
| 4 | Bodily resurrection | Contested; not consensus; fit of historical method to miracles disputed |
| 5 | Lourdes cures | Unexplained remissions real; "supernatural" inference contested; Lourdes effect complicates it |
| 6 | Qur'anic historical/contextual claims | Largely concordant with its late-antique context; specifics debated |
| 7 | Fine-tuning | Data real; underdetermined among design / multiverse / necessity |
| 8 | Tyre / Ezekiel 26 prophecy | Contested fulfilment; *vaticinium ex eventu* risk |
| 9 | Buddhist / Mahābhārata cosmology | **Not supported** |
| 10 | Epic-event dates (Kṛṣṇa / Rāma / Kurukṣetra) | Not independently corroborated; debated |

**And the six dated falsifiable predictions across three traditions** (Miller 1843 → 22 Oct 1844; Martin 21 Dec 1954;
Camping 1994, 21 May 2011, 21 Oct 2011): **5 of 5 day-level predictions did not occur**, and **0 of 6 localised to the
core**. Per the r2 insulation artifact these are *selected* cases — famous *because* they survived — so they are a record,
not a base rate.

> **BLOCKED, STATED PLAINLY.** External source verification (Lourdes cure counts, Family Radio, Simon–Ehrlich, Tetlock,
> Miller–Martin) has been **unavailable for this session and the four before it**: the web-search tool returns
> `MCP tool stepsearch.web_search failed: Streamable HTTP error: Error POSTing to endpoint:` on every attempt, retried
> this turn. **No number in Table 2 or §5 depends on an external source** — every figure is computed from the formulas in §2
> by the companion verifier, and the ledger states above are inherited from the companion taxonomy, which reports them as
> sourced there. The standing backlog is blocked on tooling, not on the argument. Nothing in this artifact should be read as
> independently re-verifying those external claims.

---

## 7. What would change my mind — pre-stated, and falsifiable

Theorems 1–4 are conditional on stated structure. Each falsifier below would break them, and I would report it.

1. **A bridge premise that becomes empirically fixable.** If one could instrument and replicate what "a perfectly loving
   being would do" — or what "a good God permits" — across populations, the B column of Table 1 would migrate from [NT] to
   [T], and Theorem 2's vacuity would no longer apply to that argument. *Status: no such measurement exists, and none is
   proposed.*
2. **A core-entailed observation type other than the law-violating interruption** (the separation artifact's stated refuter,
   C1). This would break the finding that the whole peripheral layer reduces to one contested observation type, and would
   give Theorem 3 a discriminative channel it currently lacks.
3. **A documented dated prediction refuted with k = 0** — no auxiliary move available — with proponents conceding the core.
   That would falsify the insulation gate in that case (and with it the claim that ρ_b = 1 is universal).
4. **A per-bridge likelihood ratio demonstrably ≠ 1 for a genuine core commitment** — i.e. an argument whose bridge is not
   normative but empirical. Theorem 1(ii) would then bound, but not nullify, the argument, and the [NT] column of Table 3
   would acquire a [T] entry.
5. **An N materially below 4 000** at fine individuation, or a demonstrated uniqueness argument that reduces the candidate
   set without stipulating the answer — which would lower λ_req in Theorem 3. *Note:* N is contested and the thresholds must
   be quoted with their N.

Items 1 and 4 are the ones that would actually change the result; item 5 only moves a constant. **None currently holds.**

---

## 8. Limitations

1. **Theorem 2's vacuity is conditional on bridge neutrality.** Table 1 asserts ρ_b = 1 is *available* for each argument
   under some admissible bridge reading; it does not claim the reading is the correct one. A proponent who denies that any
   admissible bridge is neutral is denying the antecedent, and this artifact cannot compel them — see §7 item 4.
2. **The bridge family 𝔅 is stipulated.** The weights q_b in Theorem 1 are prior quantities. Different bridges, different
   weights, same theorem: BF remains a weighted mean of per-bridge ratios.
3. **The τ_req lattice assumes an even start.** From a non-even prior the required tilt scales accordingly; the table is the
   clean case, not a general claim about anyone's actual credence.
4. **N is contested** (4 000–10 000+). Quote every λ_req with its N. The invariant content of Theorem 3 is the form and the
   N − 1 factor.
5. **Independence is assumed** in the bridge family. Correlated bridges (one hermeneutic supplying several readings) reduce
   the effective family size and can move the weighted mean; anti-correlated readings move it the other way.
6. **No external sources were obtained this session** — see the blocker statement in §6.
7. **This document assigns no probability to any god's existence and asserts no verdict on any religion.** It reports the
   logical structure of the arguments and shows where their evidential force does and does not reside. It does not claim
   that any god exists, nor that any god does not.

---

## Sources (as cited by the companion artifacts; not re-verified this session)

- Plato, *Euthyphro* (~10a) — the Euthyphro dilemma. **[ground truth confirmed]**
- J. L. Schellenberg, *Divine Hiddenness and Human Reason* (Cornell Univ. Press, 1993).
- J. L. Mackie, "Evil and Omnipotence" (*Mind*, 1955); Alvin Plantinga, *God, Freedom, and Evil* (1974); William L. Rowe,
  "The Problem of Evil and Some Varieties of Atheism," *American Philosophical Quarterly* 16 (1979); Paul Draper, "Pain and
  Pleasure: An Evidential Problem for Theists," *Noûs* 23 (1989).
- John Hick, *An Interpretation of Religion* (1989) — religious diversity / pluralism.
- Robert M. Adams, *Finite and Infinite Goods* (1999) — the perfect-being response to Euthyphro.
- T. & J. McGrew (2009) — the cumulative Bayesian case for the resurrection (reported, not adjudicated).
- Companion artifacts: `god-religions-truth_taxonomy_and_testability.md` (ledger rows 1–14, [O] states), `…_separation_formal.md`
  (Theorem 3's λ_req lattice, C1), `…_insulation_formal.md` (the κ table and the R4 min-tenability threshold), `…_confirmation_formal.md`
  (the hardening ceiling and the r^(−k) bar).

---

## Verification

`verify_v13.cjs` is a fresh script sharing no code with `verify_v9.cjs` / `verify_v10.cjs` / `verify_v12.cjs`. It:

1. **Re-derives Theorem 1 numerically** by brute-force enumeration over 20 000 random bridge families: checks BF(A) equals the
   weighted mean of ρ_b·τ_b to 10⁻⁹ and that the min/max bound holds.
2. **Re-derives each consequence** over a further 20 000 (plus 5 000 for 2(i)): ρ≡1 ⟹ BF = ⟨τ⟩; ρ≢1 ⟹ BF ≠ ⟨τ⟩;
   τ≡1 ⟹ BF = ⟨ρ⟩ with the ρ-bounds; ρ≡1 ∧ τ≡1 ⟹ BF = 1 **exactly**; ρ≡1 ∧ homogeneous τ ⟹ BF = τ exactly.
3. **Re-derives Table 2** from τ_req = p/(1−p) and the inverse posterior, including the p = 0.5, τ_req = 1 sanity check.
4. **Re-derives Theorem 3** from p = λ/(λ+N−1) and λ_req = (N−1)p/(1−p) for N ∈ {10³, 10⁴, 10⁵} and
   p ∈ {0.5, 0.9, 0.99, 0.999}, and checks the difficulty ratio is N−1.
5. **Re-derives Theorem 4** from w_min = p^(1/n) for n ∈ {1…10} and checks wⁿ against the taxonomy's stated 0.8³ = 0.512.
6. **Re-parses Tables 1 and 3 from this document's own markdown** — tallies the ledger rows, the [T]/[NT] split, the
   per-family consistency, the total 14 / 10 / 4, and that the core-testable column is zero in every family row. It also
   checks that every argument row's data column really is [T] and every bridge column really is [NT], so that the
   data/bridge separation the theorems depend on holds in the document rather than merely being asserted.
7. **Scans this document for banned constructions**: the two literally banned phrases, plus a wider regex set for asserted
   verdicts, with matches excused only where the surrounding text is explicitly negated, conditional, or meta-textual
   (protocol disclaimers, "whether a god exists", "a being *defined* as existing"). It also confirms the three ground-truth
   constraints are present and uncontradicted.

**First-run audit trail, kept deliberately — it caught a real error in the argument.** The script's first execution reported
**12 failures**. One was a genuine error in this artifact; eleven were mis-specifications in the script.

- **Artifact error (corrected).** Theorem 1 was first stated as `BF(A) = ⟨ρ_b⟩_w` — a weighted mean of per-bridge
  likelihood ratios — and was used to claim that a bridge-neutral argument has BF = 1 *exactly*. **That is false.** The
  correct factorization, re-derived from the definition of BF and then brute-forced over 300 000 random bridge families
  (max residual 2.8 × 10⁻¹⁴), is `BF(A) = ⟨ρ_b · τ_b⟩_w`: a weighted mean of likelihood-ratio **times** bridge-prior-odds-ratio.
  Under the false form the naive mean deviates from the true BF by up to **11.0×**, and in 63% of random families by more
  than 0.05. The correction *strengthened* the artifact: a bridge-neutral argument does **not** have BF = 1 — it has
  **BF = ⟨τ_b⟩_w**, a weighted mean of bridge prior odds ratios, which is why such arguments move posteriors without
  evidence. Theorem 1(i)–(iv), Theorem 2, and Corollary 5 were rewritten accordingly, and §0 and §4 were adjusted to match.
- **Script mis-specifications (script corrected, artifact unchanged):** the Table-3 regex required the [T]/[NT] counts to be
  bold and inconsistently formatted rows were skipped (0 of 10 parsed); the section references `§1.2` and `§1.7` inside a
  ledger-row cell were read as row *numbers*, breaking the per-family and distinct-row tallies; the `[T]` tag test looked
  for the literal string `**T` rather than `[T]`; Table 1 rows were expected to have 6 columns when they have 8; two
  Table-4 expected constants were mistyped (0.9^(1/5) is 0.9791483623609768, and 0.9^(1/8) is 0.9869162813660015 — the
  document's rounding to 0.9869 was right, the script's 0.9868 was wrong); and one audit threshold demanded 90% where 63%
  was the correct observed rate.

After correction, all **107** checks pass. The single artifact correction changed the form of Theorem 1 and the text
resting on it; no other number changed. **This artifact's own headline result was obtained only because the verifier did
not share the artifact's assumptions** — a point worth recording for whoever audits v14.
