# What the Swarm Actually Discovered

*Part 7 of the AgentSwarm series — the research output, audited.*

---

## Beyond "not lying": did the agents do real work?

The first six posts in this series are about trustworthiness. This one is about
the thing the trustworthiness was *for*: 68 reports and 139 Python engines,
written autonomously, across cosmology, relativistic flight, propulsion, drug
discovery, astrobiology, and comparative religion.

I had every quantitative claim independently recomputed — roughly 25 key
quantities. **22 of 25 were correct to the digits printed.** What follows are
the strongest results, in the audit's ranked order. (The full audit lives in
`arena/docs/RESEARCH_SYNTHESIS.md` and `arena/audit/annotations.json`.)

## 1. The generalized radiator law — the strongest single result

For any onboard thermal propulsion system, waste heat has to be radiated, and
Stefan–Boltzmann doesn't negotiate. The swarm derived the coupling:

```
P_waste / F = ½ · v_e · (1−η) / η
→ a_max = 4εσT⁴η / (σ_panel · v_e · (1−η))
```

The corollary is genuinely counterintuitive: **raising exhaust velocity makes an
onboard rocket *worse*, not better** — because radiator mass per Newton of
thrust scales *linearly* with v_e. Run the numbers for an ideal antimatter
rocket (v_e = 0.36c, η = 0.95, radiator at 1800 K): 41.64 MW per Newton,
requiring 194.3 kg of radiator per Newton, clamping acceleration to
**5.25×10⁻⁴ g** — meaning the burn to reach 0.2c takes **38.0 light-years**.

A second agent independently reached the same conclusion from the opposite
direction (the rocket equation), and the two derivations meet. This is usually
stated qualitatively in the literature; the corpus states it as a closed-form
scaling law with numbers.

## 2. The 10¹² error an agent caught in itself

The corpus's most epistemically interesting artifact is not a number but a
**retraction**. Revision 1 of the propulsion analysis scored fusion at
I_sp = 10⁵ s and reported a mass ratio of 10¹³ to reach 0.1c. Revision 2 —
written by the same agent, unprompted — caught that its exhaust velocity was
~3× below the Project Daedalus design point, noted that a factor-3 error in v_e
is a factor of e^9.7 ≈ 10⁴ in mass ratio, and corrected the figure to
**3.1–18.4**, cross-validated against Daedalus itself (50,000 t → 3,500 t at
0.12c, MR ≈ 14).

The original document, the revision note, and the correction all remain in the
file. The audit verified the corrected values independently. That is what an
honest research log looks like — and it's the behavior the ledger design is
meant to reward.

## 3. The FTL causality obstruction, proved twice

Two agents derived the antitelephone threshold by **different algebraic
routes** — one from a two-observer tachyonic reply construction, one from the
invariant interval — and converged exactly:

```
v > 2c²U / (U² + c²)
```

For U = 2c, the threshold is 0.80c; at v = 0.9c, a reply to a message sent at
t₁ = 100 s arrives at t₃ = **62.81 s — 37.19 seconds before the question was
asked.** The corpus then carries it through to the QFT consequence
(microcausality violation → frame-dependent time-ordering → S†S ≠ I →
negative-norm states), which is a level of completion most treatments skip.

## 4. Big Bang nucleosynthesis from first principles

Freeze-out at T_f ≈ 0.75 MeV gives (n/p)_f = e^(−1.2933/0.75) = 0.1783; 200
seconds of β-decay (τ_n = 878.4 s) reduces it to 0.1420; so
Y_p = 2(0.1420)/1.1420 = **0.2486**, against a measured **0.245 ± 0.003**.

A correct textbook chain, landing inside the error bar, with **zero free
parameters** — computed by the agent's own engine, which the audit re-ran.

## 5. The lipophilic trap, arithmetically demonstrated

The best counterintuitive result in the drug-discovery corpus. Two compounds,
same target, same total concentration:

- **Candidate 1:** cLogP 1.8, K_d 50 nM → free fraction 9.206% → occupancy
  **64.8%**
- **Candidate 2:** cLogP 4.8, K_d **0.5 nM** (100× tighter binder) → free
  fraction collapses **279-fold** to 0.033% → occupancy **39.6%**

The 100× affinity gain is overwhelmed by the free-fraction collapse. The
"better" molecule is the *worse* drug — and simultaneously loses 45× of its
hERG safety margin. The audit recomputed this end to end against the published
empirical relations (Austin 2002, Waring 2010). Exact.

## 6. The BACE1 paradox, resolved mechanistically

Why did human genetics validate BACE1 as an Alzheimer's target (the protective
A673T variant, OR ≈ 0.20) while four BACE1 inhibitors with 70–90% target
engagement all failed — on cognitive *worsening*? The swarm's answer: **A673T
sits on the substrate (APP), not the enzyme.** An orthosteric inhibitor
indiscriminately blocks BACE1's 30+ other substrates; the protective variant
subtly adjusts one cleavage. Quantified as a therapeutic index of 0.328 —
against PCSK9's 24.75, the correct control, where the target has no substrate
pleiotropy and healthy homozygous nulls exist. The audit called this the
strongest piece of scientific reasoning in the corpus.

## 7. The rest of the shelf

- **Propulsion, ranked.** Nine drive families ordered by feasibility today —
  and the ordering *inverts almost exactly* when ranked by interstellar
  capability. Chemical rockets are already at 87% of their bond-energy ceiling
  (there is no chemical breakthrough available); antimatter's wall is production
  rate, not physics: a 1-tonne probe to 0.1c needs only 4.2 g of antiprotons,
  but CERN-scale production of 2.5 kg takes 2.5×10¹² years — ~180× the age of
  the universe.
- **The Fermi paradox as variance artifact.** Monte Carlo over honest
  log-uniform priors gives median N ~ 0.6–1.2 with P(N<1) = 35–45%. The paradox
  needs no exotic resolution; we've searched <10⁻¹⁶ of the parameter space.
- **Commercial fusion by 2040?** A dedicated benchmark question run 6 times
  across two substrates: the swarm's verdict was **no** under standard
  engineering-feasibility constraints, argued from burn kinetics, the virial
  theorem, and discounted cash-flow techno-economics — with the engines' unit
  tests passing.

## Where the errors actually live

The audit found five defects. Their distribution is the finding:

> **Every error was in markdown prose. Every Python module computes correctly.**

The agents' *computational* reasoning is sound; the slips appear when results
are transcribed into narrative. A chemical mass ratio quoted as 10²⁸⁹⁷,
10²⁹³⁷, and 10²⁸⁹⁵ in three different files — arithmetic says 10²⁹⁰⁵, and all
three are wrong *and mutually inconsistent*. An Andromeda trip time reported at
about half the round trip. An interstellar-medium flux given as 22.7 W/m² in
one report and 2.25×10⁴ W/m² at the same velocity in another.

This is the **opposite** of the usual LLM failure mode, where the prose is
fluent and the arithmetic underneath is broken. Here the computation is right
and the prose drifts. None of the five defects overturns a conclusion; all five
would be caught by a referee. They remain in the corpus, annotated — because
the *distribution* of errors is more informative than clean numbers would be.
If you're building on agent-generated research, the lesson is concrete: **trust
the code, audit the prose.**

---

*Next: [Part 8 — Physics, Gods, and the Firewall Between Them](08-the-metaphysical-firewall.md):
the agent that proved a question unanswerable, formally, and found the same
firewall already built inside a 3,000-year-old tradition.*
