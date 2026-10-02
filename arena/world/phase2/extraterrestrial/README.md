# Extraterrestrial Engine — Phase 2 (Agent Nagarjuna, A004)

**Domain:** Are aliens real? (extraterrestrial) · **Epistemic class:** Exploratory

`extraterrestrial_engine.py` answers one standing question by strictly partitioning it
into three separate, independently decidable questions, and for each one it supplies a
**falsifiable prediction** plus the **observation that would settle it**. Plausibility is
never treated as evidence, and no discovery is asserted.

1. **Q1 — Does life exist elsewhere?** *Plausible and investigable.* With ~5,500
   confirmed exoplanets and the Kopparapu et al. (2013) habitable zone, the analysis
   quantifies an Earth-like CH4+O2 atmosphere as a strong thermodynamic disequilibrium
   (`Delta G ≈ -803 kJ/mol`, required CH4 flux ~10^15 molecules m⁻² s⁻¹) with CO as the
   abiotic false-positive gate. Prediction: ≥1 of 30 surveyed temperate rocky planets
   shows coupled CH4+O2 with f_CO/f_O2 < 0.05 at ≥5σ. Settling observation: ELT/HWO
   spectroscopy excluding photochemical mimics, or in situ plume analysis at
   Europa/Enceladus. Falsified by a census of ≥100 planets showing only abiotic
   atmospheres.
2. **Q2 — Does intelligent life exist?** *Undecidable.* Monte-Carlo over
   Sandberg-Drexler-Ord log-uniform priors gives P(N < 1) ≈ 0.4 with a 5–95th
   percentile spread spanning many orders of magnitude: the Fermi paradox is partly an
   artefact of epistemic variance. Less than 10⁻¹⁶ of the 8-D cosmic haystack has been
   searched, so the null result is weak evidence. Prediction and null-falsification are
   stated as an all-sky 1–10 GHz survey to EIRP 10¹² W within 100 pc.
3. **Q3 — Has it visited Earth?** *Unsupported; rejected under the null hypothesis.*
   Relativistic prices: at β = 0.10 the specific energy is ~4.5 × 10¹⁴ J/kg (~108 kT TNT
   per kg), with fusion mass ratio R ≈ 7 (flyby) and R² ≈ 55 (round trip). A Bayesian
   audit with a generous prior and a flattering Bayes factor still leaves
   P(visit | anecdote) ~10⁻⁶. Prediction: if ET technology has operated nearby, debris
   with >10σ non-solar isotopic fractionation exists. Settling observation: TEM /
   mass-spectrometry of recovered material, plus calibrated multi-modal sensor telemetry
   of >100 g atmospheric manoeuvres.

## Usage

```bash
python extraterrestrial_engine.py     # prints domain / confidence / counts
python test_extraterrestrial_engine.py
```

`analyze()` returns `{domain, claims, confidence, evidence}`; `evidence` entries each
carry `kind`, `value`, and `source` (literature or first-principles derivation).

## Advance over Phase 2: statistical power and the abiotic-O₂ budget

Phase 2 *stated* a prediction ("≥ 1 of 30 planets"); it never asked how much that
prediction buys. Three new first-principles models close that gap.

**Q1 — detection power.** `P(≥1) = 1 − (1 − f)ᴺ` over a binomial model of independent
planets. A 30-planet survey has **96 %** power if biospheres are common (f = 0.10), but
only **79 %** at f = 0.05, **45 %** at 0.02 and **26 %** at 0.01. Holding 90 % power for a
*rare* biosphere (f = 0.02) needs **114** surveyed atmospheres. The exact inverse model,
`f_upper = 1 − (1 − C)^{1/n}`, gives the 95 % null bound: **0.095** after 30 nulls,
**0.00997** after **299**. Target supply is not the bottleneck — ~**971** rocky
temperate HZ planets orbit FGK stars within 30 pc (η₊ = 0.37, Hsu et al. 2019), 3.2× the
required census — atmospheric sensitivity is. Note the epistemic point: even a
299-planet null bounds only 4 × 10⁸ of ~4 × 10¹⁰ galaxy-wide HZ planets, so a null
establishes **rarity, never aloneness**.

**Q1 — why O₂ alone is a weak biosignature.** From `H₂O → H₂ + ½O₂` and `p = m_col·g`,
losing one Earth ocean leaves **239 bar** of abiotic O₂ — **1138×** Earth's entire
biosynthetic O₂ inventory (0.21 bar). Earth-like abiotic O₂ therefore needs only
**8.8 × 10⁻⁴** of an ocean, i.e. **4.4 kg/s** of hydrogen escape for 10⁹ yr — just
**1.5×** Earth's *present* escape rate. So an abiotic O₂ mono-detection would settle
nothing; the CO/CH₄ companion gate is the discriminator. (Anchor: Luger & Barnes 2015,
DOI 10.1089/ast.2014.1231.)

**Q2 — the null-survey ceiling.** `f_T,upper = 1 − (1 − C)^{1/n}`. A 95 % null over
10⁶ stars bounds transmitting stars to **f_T < 3.0 × 10⁻⁶**, which still permits
**~1.1** transmitters in the 4.2 × 10⁶ pc³ searched volume (~3.6 × 10⁵ real stars). The
requested 10⁶-star survey is already **2.8×** larger than the real 100 pc census, so the
null cannot be strengthened by re-surveying that volume; reaching f_T < 10⁻⁹ needs
**~3.0 × 10⁹** targets. Q2 is undecidable *in practice*, not merely in principle.

## Usage

```bash
python extraterrestrial_engine.py              # prints domain / confidence / counts
python test_extraterrestrial_engine.py         # 15 tests, exits 0
```
