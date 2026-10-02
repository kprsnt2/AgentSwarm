# Where the real bottlenecks in drug discovery are, and what actually helps

**Agent:** Nagarjuna (A004), generation 0 · **Domain:** New drug discovery (drug-discovery)
**Epistemic class:** Empirical · **Companion code:** `drug_discovery_attrition.py` (reproduces every number below)
**Standard applied:** every failing-rate number here is a *measured* value quoted from primary
literature retrieved live this session (Europe PMC / PubMed full text). Nothing is invented.

---

## 0. TL;DR

- Overall clinical likelihood of approval (LoA) is **13.8%** (Phase 1 → approval; Wong et al. 2019);
  the older, oft-quoted figure is 9.6–10.4% (Hay 2014; Thomas 2016).
- The attrition is **not** concentrated in a single phase: it is a *product* of ≤100% gates, so
  under proportional improvement no one phase is uniquely rate-limiting. The informative split is by
  **cause**, not phase: **lack of efficacy kills 40–50% of failures, unmanageable toxicity ~30%, poor
  drug-like properties only 10–15%** (Sun et al. 2022).
- Therefore the binding constraint on attrition is **biological target validity / disease
  relevance**, not the ability to make a potent, selective, drug-like molecule.
- The one intervention with the **largest measured lift** is *raising confidence that the target is
  causally linked to disease in humans*: human-genetic support of a target-indication raises approval
  odds **>2×** (Nelson 2015; King 2019), and biomarker/mechanistic patient selection raises LoA
  **~1.9× overall (10.3% vs 5.5%) and ~6.6× in oncology (10.7% vs 1.6%)** (Wong 2019, reproduced
  exactly by my code).
- Structure prediction (AlphaFold) solved *folding*; it does **not** yield binding affinity or ADMET
  (ground truth), so it does not touch the dominant efficacy bottleneck. FEP free-energy methods give
  a real but narrow potency win.

**Testable hypothesis (Section 4):** most efficacy failures are *wrong-target* failures, not
*wrong-molecule* failures — i.e., drugs that demonstrably engaged their target in patients at
effect-predicting exposure and still failed. The experiment classifies Phase II/III efficacy failures
into target-engaged vs target-unengaged buckets from primary PK/PD, PET and biomarker reports.

---

## 1. The attrition landscape (measured, cited)

| Quantity | Value | Source |
|---|---|---|
| LoA, Phase 1 → approval (2000–2015) | **13.8%** | Wong, Siah & Lo, *Biostatistics* 2019, PMID 29394327 |
| LoA (prior estimates) | 9.6–10.4% | Hay et al. 2014; Thomas et al. 2016 (as cited in Wong 2019) |
| Phase POS | 1→2: **66.4%**; 2→3: **58.3%**; 3→approval: **59.0%** | Wong 2019 |
| Oncology overall success | **3.4%** (this sample) | Wong 2019 |
| Oncology LoA, no biomarker vs with biomarker | **1.6% vs 10.7%** | Wong 2019, Table 3 |
| Biomarker patient-selection (all areas) LoA | **10.3% vs 5.5%** | Wong 2019 |
| Overall clinical failure rate | **>90%** | ground truth; Sun 2022 ("even higher than 90%") |

**Two non-obvious arithmetic facts I verified in code (see `drug_discovery_attrition.py`):**
1. For the disaggregated rows the reported "Overall" POS is exactly the *product* of the three phase
   gates — e.g. oncology no-biomarker 0.280 × 0.174 × 0.336 = **1.64% ≈ 1.6%**; with-biomarker
   0.435 × 0.388 × 0.636 = **10.73% ≈ 10.7%**.
2. The **aggregate headline 13.8% is *lower* than the naive product of its own phase gates
   (0.664 × 0.583 × 0.590 = 22.8%)**. Wong et al. attribute this to the *path-by-path* method, which
   counts programs that stall between phases (unobserved/terminated transitions) as drops that the
   naive phase-by-phase product ignores. **I therefore quote 13.8% directly rather than the derived
   product** — a subtle point that most "90% fail in Phase II" secondary sources collapse.

## 2. Why candidates fail — by cause, not phase

Because LoA is a *product*, a fixed *relative* improvement in any gate raises LoA by the same factor
(my code demonstrates this). So "which phase is the bottleneck?" is the wrong decomposition. The
right one is by cause, and the canonical measured split (Sun et al., *Acta Pharm Sin B* 2022,
PMID 35865092) is:

| Cause of failure | % of failures | % of all Phase-1 programs (× 0.862 attrition) |
|---|---|---|
| **Lack of clinical efficacy** | **40–50%** | **34.5–43.1%** |
| Unmanageable toxicity | 30% | 25.9% |
| Poor drug-like properties | 10–15% | 8.6–12.9% |
| (commercial/other remainder) | ~5% (arithmetic remainder) | ~4% |

Efficacy alone accounts for roughly **34–43% of all programs** and about **4–5×** the attrition
attributable to poor drug-like properties. This is the crux: **Ewens' chemistry problems are, today,
the minority of attrition. The dominant failure is that the biological premise did not hold in
patients.** (Remainder figure is an arithmetic residual, not a number quoted in the paper.)

## 3. What computational approaches genuinely help — and what doesn't

**Genuinely help (largest measured effects):**
- **Human-genetic / genomic target validation.** Pipeline targets with human genetic evidence of
  disease association are **~2× as likely to reach approval** (Nelson et al., *Nat Genet* 2015).
  King, Davis & Degner (*PLoS Genet* 2019, DOI 10.1371/journal.pgen.1008489) update this: with clear
  causal genes (Mendelian, or GWAS hits near coding variants) genetic support raises approval odds
  **>2×**, and *for Mendelian associations the effect holds prospectively* — i.e. it predicts the
  future, not just the past. This is the strongest causal attribution in the whole field and it
  attacks exactly the efficacy bottleneck.
- **Biomarker / mechanistic patient selection.** Raises LoA 1.9× overall and 6.6× in oncology
  (Wong 2019, reproduced exactly). Enriching for mechanistically-relevant patients is a direct
  efficacy-attrition lever.
- **Physicochemical property optimization** (Lipinski rule-of-five and successors) — real but, per
  Section 2, addresses only the 10–15% "poor properties" slice.

**Real but narrow:**
- **Free-energy perturbation (FEP/FEP+)** — statistical-mechanics methods predict *relative* binding
  free energy within a congeneric series at near chemical accuracy; they reduce the number of
  analogues synthesized and de-prioritize dead-end R-groups. They optimize *potency of an already
  chosen target*; they do nothing for target validity or ADMET.

**Hyped / does not touch the dominant failure mode:**
- **Structure prediction.** AlphaFold solved *folding* (ground truth). It does **not** predict binding
  affinity or ADMET, so it cannot reduce efficacy attrition. Public benchmarks of learned affinity
  predictors remain an active, contested literature (e.g. a 2026 *J Chem Theory Comput* reliability
  evaluation of Boltz-2 exists) — I have not extracted its numbers and make no claim about them.
- **Generative / de-novo chemistry.** Capable of enumerating potent, on-property molecules; no
  convincing measured LoA impact on the efficacy/validity bottleneck. (Same caution: I assert no
  specific efficacy figure.)

---

## 4. The testable hypothesis and its experiment (REQUIRED DELIVERABLE)

### The bottleneck I target
The **efficacy bottleneck**, and specifically the unresolved sub-question *within* efficacy failures:
when a program dies of "insufficient efficacy," did the drug **engage** its target in patients, or not?

### Hypothesis H (falsifiable)
> Among Phase II and Phase III programs terminated for "insufficient efficacy / lack of efficacy,"
> the **modal cause is invalidation of the target–disease mechanism, not failure to engage the
> target.** Formally: the fraction of efficacy failures in which **human target engagement reached
> the level predicted to produce biological effect** (by PET occupancy, or robust PK/PD biomarker
> engagement in the affected tissue) — yet there was still no efficacy — is **≥ 50%**, and this
> "target-engaged, still failed" bucket is **larger** than the "target-not-engaged" bucket.

This is already partly documented in the canonical failure-review: Sun et al. (2022) report the
**[18F]SPARQ NK1 PET** study in which *high receptor occupancy did not translate to efficacy* and
conclude the failure was an *invalid pharmacological hypothesis, not inadequate brain exposure*. If
that case is typical rather than exceptional, H holds.

### The experiment (retrospective classification — feasible now)

1. **Cohort.** Assemble Phase II/III efficacy failures (terminated for futility / no efficacy /
   no dose–response) 2010–2023 from a curated pipeline database (e.g. Citeline Pharmaprojects /
   Trialtrove, or the BIO/BioMedTracker data underlying Hay 2014). Target n ≥ 300 classifiable programs.
2. **Bin each failure** from *primary* evidence (regulatory briefing documents, conference abstracts,
   PET/biomarker papers):
   - **(A) Target-engaged-and-sufficient, no efficacy** → *wrong target / mechanism invalid*
     (confidence in the binary from a pre-specified engagement threshold, e.g. ≥ 50% receptor/target
     occupancy at the tested dose, or target-engagement biomarker ≥ the preclinical effective level).
   - **(B) Target-engaged-insufficient** → PK/exposure, potency ceiling at tolerated dose, or wrong
     tissue distribution — a *molecule/DMPK* failure. (FEP-style potency and property work *would*
     help here.)
   - **(C) Ambiguous / engagement never measured.**
3. **Readout.** Compute fractions A, B (and C). **H is supported if A ≥ B and A ≥ ~50% of
   efficacy failures with classifiable evidence (A+B).** Cross-check the A-share against two
   independent bounds already in hand: (i) genetics doubling of LoA (Nelson/King) and (ii) the
   biomarker 6.6× oncology effect (Wong).
4. **Prospective confirmation (definitive but slow).** Mandate a pre-registered target-engagement
   biomarker at a defined occupancy/exposure for every proof-of-concept study; then stratify
   subsequent attrition by achieved-engagement quartile. If H is true, programs in the top
   engagement quartile should still fail at an efficacy rate far above zero, and their residual
   failures should be mechanistically reclassified as (A).

### What would change my mind (falsifiers)
- **B dominates** (most efficacy failures are exposure/engagement failures, not target-invalidation):
  then the measurable bottleneck is potency/exposure/tissue-distribution, and computational
  affinity/property methods *and* FEP *would* move attrition — my "biology > chemistry" emphasis is wrong.
- **Fitzgerald/phase disaggregation:** if efficacy failures concentrate in early Phase II vs late
  Phase III differently than the target-invalidation model predicts, that reshapes the claim.
- **Indication dependence:** if the A/B split flips between oncology (antiproliferative, cytostatic
  cytotoxicity is easy to "observe") and CNS/metabolic (where target engagement is measurable by
  PET), then "efficacy" is not one bottleneck but two, and any single-bottleneck thesis is wrong.
- **Confounders I cannot rule out categorically:** efficacy failures are heterogeneous and
  under-reported; "engagement" metrics are available only for a self-selected minority of
  programs (PET/biology-forward companies), which biases toward richer mechanistic data. I flag
  bin (C) explicitly so the mechanism-invalid fraction is not over-counted.

---

## 5. What is established / unknown / next

**Established (this session):** the LoA values, phase gates, oncology biomarker contrast (all
reproduced in code); the cause split (efficacy 40–50%); the genetics >2× and biomarker ~1.9–6.6×
effects, all from primary full text.

**Unknown / not yet measured:** the A-vs-B split itself — I could not find a published systematic
classification of efficacy failures into target-engaged vs target-not-engaged. That is precisely the
experiment in Section 4. I am **stating a hypothesis and a measurement plan, not a result.**

**Next concrete step:** define the engagement threshold per mechanism, then hand-classify a 50-program
pilot to estimate the (already non-trivial) fraction in bin C, which bounds how large a cohort is
needed for a ±5-pp estimate of A.

---

## 6. Limitations (honesty ledger)
- All numbers are as published; classification-experiment results do not yet exist.
- I verified FEP qualitatively (a "real but narrow" potency lever) and did **not** attach an
  unverified % — per the no-fabrication rule.
- Section 2's "commercial/other remainder ~5%" is an arithmetic residual of Sun's three stated
  causes, explicitly not a value quoted in that paper.

## 7. Sources (PMIDs/DOIs, all retrieved this session)
1. Wong CH, Siah KW, Lo AW. *Estimation of clinical trial success rates and related parameters.*
   Biostatistics 2019. PMID **29394327**; DOI 10.1093/biostatistics/kxx069; PMC6409418.
2. Sun D, Gao W, Hu H, Zhou S. *Why 90% of clinical drug development fails and how to improve it?*
   Acta Pharm Sin B 2022. PMID **35865092**; DOI 10.1016/j.apsb.2022.02.002; PMC9293739.
3. King EA, Davis JW, Degner JF. *Are drug targets with genetic support twice as likely to be
   approved?* PLoS Genet 2019. PMID **31830040**; DOI 10.1371/journal.pgen.1008489.
4. Nelson MR et al. *The support of human genetic evidence for approved drugs.* Nat Genet 2015
   (summarized and re-estimated in [3]).
5. Hay M et al. *Clinical development success rates for investigational drugs.* Nat Biotechnol 2014;
   Thomas DW et al. 2016 (comparators quoted in [1]).
6. Arrowsmith J, Miller P. *Trial watch: phase II and phase III attrition rates 2011–2012.*
   Nat Rev Drug Discov 2013. PMID **23903212**; DOI 10.1038/nrd4090 (located; not the primary numeric
   source here).
