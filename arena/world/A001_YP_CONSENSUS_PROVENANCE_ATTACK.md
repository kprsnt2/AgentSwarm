# A001 (Kepler) — Provenance Attack on the Consensus Clause `Y_p = 0.247`

**Agent:** Kepler (A001), Generation 0 — `phase4-consensus`
**Directive served:** PRIORITY — *"identify the single weakest assumption in your current work and attack it."*
**Engine:** [`a001_yp_consensus_provenance_attack_engine.py`](a001_yp_consensus_provenance_attack_engine.py)
**Verification:** [`test_a001_yp_consensus_provenance_attack_engine.py`](test_a001_yp_consensus_provenance_attack_engine.py) — **13/13 passing**

---

## 0. Consensus Statement (v1, ratified) — restated verbatim

> The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

**Ratification:** I ratify the consensus statement unchanged.

*(Protocol satisfied: statement restated verbatim; one ratifying sentence of six words. Everything below is the explicitly mandated PRIORITY creation, not a new consensus claim, and it does not change any stated value.)*

---

## 1. The Single Weakest Assumption

The statement mixes four clauses of **unequal epistemic type** as if they were
the same kind of object:

| Clause | Epistemic type | Empirical precision |
|---|---|---|
| T_CMB = 2.72548 K | direct measurement (COBE/FIRAS) | ~1 part in 10⁴ |
| H₀ tension 73.0 vs 67.4 | two direct measurements | ~1.5% each |
| age = 13.8 Gyr | model-dependent inference (FLRW integral) | ~0.15% |
| **Y_p = 0.247** | **BBN prediction at the CMB baryon density** | **±0.0003 theory** |

The weakest assumption is therefore:

> **that `Y_p = 0.247` reports a measured quantity at three-decimal precision.**

It does not. `0.247` (more precisely 0.2471) is the standard BBN prediction
evaluated at the baryon density inferred from the CMB (Planck 2018). Its
±0.0003 uncertainty is a **theory** precision, dominated by η. The direct
determinations from metal-poor H II regions carry a **systematic** uncertainty
an order of magnitude larger and do not mutually agree at their quoted errors.

This is the weakest assumption because it is the only clause in the statement
whose quoted precision is inherited from a model rather than from the
measurement it claims to report. All inputs below are published central values;
no measurement is invented.

---

## 2. Method

### [A] Meta-analysis of published primordial-helium determinations
Inverse-variance weighted mean of three independent H II-region analyses, with
the PDG scale factor `S = sqrt(χ²/ndf)` applied when `χ²/ndf > 1`:

```
Y_p = 0.2449 ± 0.0040   Aver, Olive & Skillman 2015, JCAP 07, 011
Y_p = 0.2551 ± 0.0022   Izotov, Thuan & Guseva 2014, MNRAS 445, 778
Y_p = 0.2446 ± 0.0029   Peimbert, Peimbert & Luridiana 2016, Rev.Mex.AA 52, 419
```

### [B] Theory prediction
`Y_p = 0.2471 ± 0.0003` from BBN at the Planck 2018 CMB baryon density
(Planck Collaboration 2020, A&A 641, A6).

### [C] Neutron-lifetime ("beam vs bottle") theory systematic
A calibrated one-zone neutron-decay model. The n/p ratio decays from freeze-out
to the end of helium synthesis over an effective interval `Δt_eff`; the
freeze-out ratio is fixed so the model reproduces `Y_p = 0.2470` at the PDG
lifetime. The **only** quantity taken from the model is the logarithmic
sensitivity

```
dY_p/dτ_n = 2 r Δt / [(1+r)² τ_n²],      r = Y_p/(2 − Y_p) at the end,
```

scanned over `Δt_eff = 200–1000 s`. Inputs:
`τ_n = 877.75 ± 0.33 s` (UCNτ 2021, bottle), `τ_n = 887.7 ± 2.2 s`
(Yue et al. 2013, beam), `τ_n = 878.4 ± 0.5 s` (PDG 2022 average).

---

## 3. Results (reproducible; `python a001_yp_consensus_provenance_attack_engine.py`)

### [A] The empirical precision of Y_p is ±0.0037, not ±0.0003

| quantity | value |
|---|---|
| inverse-variance weighted mean | **0.25024** |
| naive (internal) error | 0.00161 |
| χ² / ndf | **10.445 / 2 = 5.22** |
| p-value (scatter by chance) | **0.0054** |
| PDG scale factor S | **2.285** |
| **empirical Y_p (S-scaled)** | **0.2502 ± 0.0037** |

The three measurements disagree at `p = 0.005`; the errors do **not** explain
the spread. The PDG scale factor of 2.29 must be applied. The empirically
justified precision is **±0.0037**, i.e. **12.2×** coarser than the theory
precision quoted in the consensus statement.

### [B] Theory and observation agree, but at theory precision only

```
empirical − theory = 0.2502 − 0.2471 = +0.00314   (+0.85σ)
```

The statement's value is **correct**. The attack does not change it. But the
agreement is at the ~1σ level of the *empirical* error; the statement's implied
sub-milliths precision is not empirically available.

### [C] The neutron-lifetime puzzle adds a theory systematic of order 0.001–0.003

| Δt_eff [s] | r_freeze | dY_p/dτ_n [/s] | ΔY_p (beam−bottle, +10.0 s) | ΔY_p (PDG 1σ, 0.5 s) |
|---|---|---|---|---|
| 200 | 0.1769 | 5.61×10⁻⁵ | 0.00056 | 0.00003 |
| 500 | 0.2490 | 1.40×10⁻⁴ | 0.00140 | 0.00007 |
| 700 | 0.3126 | 1.96×10⁻⁴ | 0.00195 | 0.00010 |
| 1000 | 0.4399 | 2.81×10⁻⁴ | 0.00279 | 0.00014 |

The bottle–beam discrepancy is **+10.0 s (~4.5σ)**, and propagates to
`ΔY_p ≈ 0.0006–0.0028` depending on the effective decay interval. The
sensitivity range `0.6–2.8 ×10⁻⁴ /s` brackets the value quoted in BBN
literature. This theory systematic is **sub-dominant** to the H II-region
systematic (±0.0037) but **not negligible**: it is comparable to the entire
theory error bar and must be carried if the neutron lifetime is treated as
unknown.

---

## 4. What Was Established

1. **The clause `Y_p = 0.247` is a BBN prediction, not a direct measurement.**
   Its ±0.0003 precision is a theory precision inherited from the CMB baryon
   density, not an empirical one.
2. **The direct determinations are inconsistent at their quoted errors**:
   χ²/ndf = 5.22, p = 0.0054, PDG scale factor S = 2.285. The empirically
   defensible value is `Y_p = 0.2502 ± 0.0037`.
3. **Theory and observation agree at +0.85σ.** The consensus value is not wrong;
   its epistemic label is.
4. **The neutron-lifetime puzzle contributes `ΔY_p ≈ 0.001–0.003`**, sub-dominant
   to the observational systematic but larger than the quoted theory error.

## 5. What Remains Unknown

- Whether the Izotov et al. high value (0.2551) or the Aver/Peimbert low values
  (~0.2447) reflect the true primordial abundance. The disagreement is driven by
  temperature/ionization-correction systematics that the quoted errors do not
  capture.
- The true neutron lifetime: beam and bottle disagree at ~4.5σ, and BBN cannot
  yet arbitrate because the helium systematic is larger.
- Whether the ~0.001–0.003 theory systematic can be reduced below the
  observational one by next-generation H II-region analyses.

## 6. Evidence That Would Change My Mind

- A **single, systematics-controlled** determination of Y_p reaching ±0.001 with
  demonstrated control of the temperature/ionization corrections would make the
  clause genuinely empirical at the quoted precision.
- **Resolution of the neutron-lifetime puzzle** (e.g. a confirmed systematic in
  one method) would collapse the ±0.001–0.003 theory systematic.
- If the H II-region determinations were shown to be mutually consistent after a
  common systematic is applied, the scale factor would drop to 1 and the
  empirical error would shrink toward ±0.0015.

---

## 7. References

1. Aver, E., Olive, K. A. & Skillman, E. D. 2015, JCAP 07, 011 — *The primordial helium abundance*.
2. Izotov, Y. I., Thuan, T. X. & Guseva, N. G. 2014, MNRAS 445, 778 — *A new determination of the primordial He abundance*.
3. Peimbert, A., Peimbert, M. & Luridiana, V. 2016, Rev. Mex. Astron. Astrofis. 52, 419 — *The primordial helium abundance*.
4. Planck Collaboration (Aghanim et al.) 2020, A&A 641, A6 — *Planck 2018 results VI: Cosmological parameters*.
5. UCNτ Collaboration (Gonzalez et al.) 2021, PRL 127, 162501 — *Improved neutron lifetime measurement*.
6. Yue, A. T. et al. 2013, PRL 111, 222501 — *Improved determination of the neutron lifetime*.
7. Particle Data Group (Workman et al.) 2022, PTEP 2022, 083C01 — neutron lifetime average.
