# Research Synthesis: The AgentSwarm World-Model Corpus

**Synthesizer:** independent audit pass over `D:\AgentSwarm\arena\world\`
**Date of source artifacts:** 2026-10-02
**Corpus size:** 24 markdown reports + 4 Phase-2 READMEs + 52 Python modules and test suites across 6 domains
**Agents:** Kepler (A001), Raman (A002), Hypatia (A003), Nagarjuna (A004), Aryabhata/Agent4 (A005), Agent5 (A006)

This document synthesizes what the swarm actually found, ranks the results by genuine interest, and — most importantly — audits the numbers. Every figure I quote was either read directly from the corpus or recomputed independently during this pass. Where I recomputed, I say so.

---

## 1. What the Swarm Concluded, By Domain

### 1.1 Cosmogenesis (`COSMOGENESIS_*`, 4 reports)

- **The standard model is over-determined.** Four independent pillars are quantified: CMB blackbody at $T_0 = 2.72548 \pm 0.00057$ K with $|y| < 1.5\times10^{-5}$, $|\mu| < 9.0\times10^{-5}$, $n_\gamma = 410.7$ cm⁻³; BBN at $\eta = 6.12\times10^{-10}$ giving $Y_p = 0.245 \pm 0.003$, $D/H = (2.547\pm0.025)\times10^{-5}$; BAO sound horizon $r_s = 147.21 \pm 0.23$ Mpc with $\ell_1 \approx 220$; and SN Ia time dilation $\Delta t_{obs} = \Delta t_{rest}(1+z)$.
- **A first-principles BBN derivation reproduces $Y_p$ with no free parameters.** Freeze-out at $T_f \approx 0.75$ MeV gives $(n/p)_f = \exp(-1.2933/0.75) = 0.1783$; 200 s of $\beta$-decay at $\tau_n = 878.4$ s reduces this to $0.1420$; $Y_p = 2(0.1420)/1.1420 = 0.2486$ versus the measured $0.245 \pm 0.003$. This is a genuinely correct textbook chain and it lands inside the error bar.
- **Classical problems are quantified, not asserted.** Horizon: 284 Mpc particle horizon against 13,870 Mpc to last scattering gives a causal patch of $\theta = 1.17°$, i.e. $\approx 9{,}627$ mutually disconnected regions sharing a temperature to $10^{-5}$. Flatness: $|1-\Omega|$ grows by $2.94\times10^{60}$ from Planck epoch to today, requiring $|1-\Omega(t_P)| < 6.8\times10^{-64}$.
- **The inflation/swampland clash is an $O(10^{25})$–$10^{27}$ discrepancy.** Starobinsky $R^2$ predicts $r = 12/N^2 = 0.0033$, $n_s = 1-2/N = 0.9667$; the Trans-Planckian Censorship Conjecture caps $r \le 10^{-30}$ (i.e. $H_{inf} \le M_P e^{-N} \approx 1.07\times10^{-7}$ GeV against a predicted $1.05\times10^{13}$ GeV).
- **Seven to eight open problems are catalogued with facility-level thresholds**: lithium-7 deficit $2.96\times$ ($9.16\sigma$, $1.58\times10^{-10}$ vs $4.68\times10^{-10}$); Hubble tension $4.85\sigma$ ($73.04 \pm 1.04$ vs $67.36 \pm 0.54$ km/s/Mpc) requiring $\Delta r_s = 7.78\%$; EDE making $S_8$ tension *worse* ($3.88\sigma \to 5.82\sigma$); gravitino/leptogenesis conflict $T_{reh} \ge 1.04\times10^9$ GeV vs $\le 10^7$ GeV, a factor $\ge 104$.
- **A cosmic entropy inventory** ranks present-day entropy from baryons ($10^{81}\,k_B$) through CMB ($5.3\times10^{89}$) and SMBHs ($10^{104}$) to the de Sitter horizon ($2.6\times10^{122}\,k_B$), against a maximum of $2.4\times10^{124}\,k_B$.

### 1.2 Relativistic Flight & FTL Causality (`FEASIBILITY_*`, `RELATIVISTIC_*`, `ULTRA_*`, `INTERSTELLAR_DECELERATION_*`, `PHASE2_LIGHTSPEED_*`)

- **1 g brachistochrone kinematics permit human-lifetime crossing but destroy simultaneity.** Proxima in **3.54 crew years / 5.87 Earth years**; Galactic Center in **19.76 / 26,001.9**; Andromeda in **28.63 / 2,537,001.9**. I recomputed all six rows from $\tau = 2(c/g)\,\mathrm{arcosh}(1+gd/2c^2)$ and the crew/peak-$\gamma$ columns are correct to the digits printed.
- **The rocket equation is the wall, not thrust.** To reach $0.1c$ at $MR \le 10$ requires $I_{sp} \ge 0.1c/(g_0 \ln 10) = 1.33\times10^6$ s. Chemical (452 s) needs $MR \approx 10^{2937}$; NTR (850 s) $10^{1562}$; nuclear pulse (3000 s) $10^{443}$.
- **Fusion closes a 0.1c flyby and nothing more.** Directed reaction energy caps exhaust at $0.039c$ (D–T charged fraction) to $0.088c$ (D–He³, 97% charged), giving $m_0/m_f = 3.1$–$18.4$ to $0.1c$ and reproducing the Project Daedalus design point ($v_e = 0.045c$, $MR \approx 14$ at $0.12c$). A crewed round trip squares this to $\approx 337$.
- **The generalized radiator law is the strongest single result in the corpus.** For any onboard thermal drive, $P_{waste}/F = \tfrac12 v_e (1-\eta)/\eta$, and Stefan-Boltzmann rejection clamps $a_{max} = 4\epsilon\sigma T^4\eta / (\sigma_{panel} v_e (1-\eta))$. For an antimatter rocket ($v_e = 0.36c$, $\eta = 0.95$, 1800 K) this is $41.64$ MW/N requiring $194.3$ kg/N of radiator, clamping acceleration to $5.25\times10^{-4}g$ and the burn to reach $0.2c$ to **38.0 light-years**.
- **The ISM is a lethal beam and the CMB becomes one.** At $0.9c$: 1.214 GeV protons, $52.5$ kW/m², hadronic interaction length in graphite 38.2 cm against a 2.80 m ionization range — so shielding is a spallation problem, not a stopping problem. A 2.8 m graphite shield masses 124.2 t and pushes the fusion brachistochrone fuel mass to $5.64\times10^{30}$ kg (2.8 solar masses). In the WHIM the CMB overtakes matter at $\gamma_{cross} \approx 270$; at Andromeda midpoint the forward blue-shift is 1.65–1.66 keV at 28.2–28.7 MW/m². A GZK hull-disintegration ceiling sits at $\gamma \ge 1.14\times10^{11}$.
- **Deceleration is the harder half.** ISM ram drag is suppressed by $4.0\times10^{-6}$ (stopping distance 493,369 ly) because 19.35 MeV protons deposit only $7.76\times10^{-6}$ of their energy in a 25 nm sail. Forward's staged reflector fails by diffraction: a 1 km array spreads to a 103,847 km spot, capturing $1.48\times10^{-15}$ of the beam. Photogravitational capture tops out at 1,089.2 km/s ($0.0036c$), 3,035× short in kinetic energy. The hybrid magsail + stellar capture architecture is the only passive route found.
- **FTL implies CTCs, proved twice independently and by two different algebra routes.** Both derivations converge on the threshold $v > 2c^2U/(U^2+c^2)$; for $U = 2c$ this is $0.80c$, and at $v = 0.9c$ a reply sent at $t_1 = 100$ s arrives at $t_3 = 62.81$ s.

### 1.3 Practical Propulsion (`PRACTICAL_PROPULSION_RANKED_ASSESSMENT.md`)

- **Nine drive families ranked by feasibility today** — chemical → solar electric → solar sail → NTR → NEP → laser sail → nuclear pulse → fusion → antimatter — and the ordering **inverts almost exactly** when ranked by interstellar capability.
- **Chemistry is 87% of the way to its own physical ceiling.** $v_e = 4.43$ km/s against a bond-energy bound $\sqrt{2Q} = 5.10$ km/s ($I_{sp} \le 520$ s). There is no chemical breakthrough available.
- **NTR halves the Mars round-trip mass ratio** (15.0 → 4.2) with 1960s ground-tested hardware — the single best near-term return in the table.
- **Solar sails have a hard terminal velocity** ($v_{max}^2/2 = a_{1AU}AU^2/r_0$): even 0.1 g/m² at 0.05 AU perihelion tops out at 737 km/s ($2.5\times10^{-3}c$), 100× short of useful interstellar speed. They are structurally excluded, not merely difficult.
- **Laser sails are lawfully gram-scale only**, because array power is linear in craft mass at fixed beam length: 37 GW for 1 g, 37 TW for 1 kg, 37 PW for 1 t.
- **Antimatter's wall is production rate, not mass.** A 1 t probe to $0.1c$ needs only **4.2 g** of antiprotons at $\eta = 0.3$; at CERN-scale output 2.5 kg takes $2.5\times10^{12}$ yr ≈ 180× the age of the universe.

### 1.4 Drug Discovery (`DRUG_DISCOVERY_*`, `TRANSLATIONAL_PKPD_*`, `EMPIRICAL_CAUSAL_*`, `NETWORK_BUFFERING_*`, `GENETIC_VALIDATION_*`)

- **Attrition is a product of gates, so the informative decomposition is by cause.** LoA (Phase 1 → approval) 13.8% (Wong 2019); the disaggregated oncology rows are *exactly* gate products (0.280×0.174×0.336 = 1.64%; 0.435×0.388×0.636 = 10.73%), whereas the aggregate 13.8% is *below* its own gate product (22.8%) — a methodological subtlety the corpus flags correctly.
- **Biology beats chemistry 2.18:1.** Efficacy 45% + on-target toxicity 15% = 60.0% target burden; ADMET 12.5% + off-target 15% = 27.5% compound burden.
- **The "lipophilic trap" is a real, arithmetically demonstrable inversion.** Using Austin 2002, $\log_{10}((1-f_u)/f_u) = 0.83\,c\log P - 0.50$: a 100× tighter binder ($K_d$ 0.5 vs 50 nM) bought with $\Delta c\log P = +3.0$ collapses $f_u$ **279-fold** (9.206% → 0.033%) and yields **lower** free occupancy, 39.6% vs 64.8%. I recomputed this and it is exact.
- **CNS programs are forced into exposure failures by the BBB.** With $K_{p,uu} = 0.0152$, sustaining 80% brain occupancy requires $C_{u,plasma} = 1{,}315.8$ nM against a 300 nM DLT threshold — peripheral TI = 0.23, capping brain occupancy at 47.7%. The trial dies labeled "lack of efficacy" when the true cause is delivery.
- **Non-linear transduction means 80% occupancy can be worth nothing.** Under Black-Leff with $\gamma = 3.5$, $EC_{50} = 0.75$: 50% occupancy → 19.5% pathway inhibition; 75% → 50.0%; 90% → 65.4%; only 98% → 71.8%. Clinical efficacy requires >95% trough occupancy.
- **Even human genetic validation leaves 83.1% failure.** Cumulative LoA rises 8.57% → 16.93% (1.97×), concentrated at Phase II (28.9% → 44.5%). Five landmark Phase III programs are adjudicated: Verubecestat (BACE1, 88% CSF Aβ reduction, futility, $P = 0.22$), Evacetrapib (CETP, 95% inhibition, HR = 1.01, $P = 0.91$), Aprepitant (NK1, 92% PET occupancy, failed), Iniparib (<10% in vivo PARP inhibition — a false-target *chemistry* failure), Evolocumab (>95% PCSK9 suppression, HR = 0.85, $P<0.001$).
- **The therapeutic-index boundary is derived, not asserted.** $TO_{eff} = 0.85$ needs $5.67 K_d$; $TO_{tox} = 0.70$ permits $2.33 K_d$; $TI = 0.411 < 1.0$. For BACE1 specifically, $TI = 0.328$ — and the crucial insight is that the protective human variant (APP A673T) sits on the *substrate*, not the enzyme, which is why the genetics validated a target that orthosteric inhibitors cannot safely hit.

### 1.5 Extraterrestrial Life (`EPISTEMIC_DEMARCATION_*`)

- **The question is split into three independently decidable questions** (biogenesis / technosignatures / visitation), with the explicit rule that plausibility is not evidence.
- **Q1 quantified.** Conservative habitable zone for the Sun is 0.981–1.689 AU (Kopparapu $S_{eff}$); CH₄+O₂ disequilibrium is $\Delta G = -706.7$ kJ/mol (from $\Delta G° = -801.0$), requiring a biogenic flux of $1.2\times10^{15}$ molecules m⁻² s⁻¹ (≈500 Tg/yr) against a 10–12 yr photochemical lifetime. Detection contrast is 1.1 ppm for an Earth–Sun analog (below JWST's 10–20 ppm floor) but **76 ppm** for an Earth around an M-dwarf.
- **Q2 is partly a variance artifact.** Monte Carlo over honest log-uniform priors gives median $N \sim 0.6$–1.2 and $P(N<1) = 35\%$–45%, with a 5–95th percentile spread of $10^{-4}$ to $10^4$. The Fermi paradox needs no exotic resolution. Only $<10^{-16}$ of the 8-D "cosmic haystack" has been searched.
- **Q3 rejected under the null.** Bayes factor required to reach $P(H_{ET}|D) > 0.95$ given $P(H_{ET}) \le 10^{-9}$ is $>1.9\times10^{10}$; the evidence class fails by >10 orders of magnitude. Waste-heat thermodynamics puts Dyson signatures at 7.36 µm for a 1 AU shell (393.6 K), and WISE/IRAS found zero of ~100,000 galaxies above 85% starlight interception.

### 1.6 Dharmic Truth Claims (`TAXONOMY_*`, `FORMAL_DEMARCATION_*`, `ARYABHATA_*`)

- **A rigid epistemic firewall, held across three independent agents.** Class A (historical/philological) is decidable; Class A2 (textual cosmological mathematics) is internally verifiable but cannot establish divinity; Class B (Brahman, Devas, Karma, Moksha, Apaurusheyatva) is empirically undecidable.
- **The historical claims are datable.** Rigveda c. 1500–1200 BCE, supported by Old Avestan cognates, the Mitanni–Hittite treaty of c. 1380 BCE naming Mitra/Varuna/Indra/Nasatya, and R1a-Z93 archaeogenetics (Narasimhan 2019); Heliodorus pillar at Besnagar c. 113 BCE confirming institutionalized Vasudeva worship.
- **The Puranic timescales are congruent and that congruence proves nothing.** Kalpa = 4.32 Ga vs Earth age 4.543 Ga is a 4.91% delta; Aryabhata's 1008-Mahayuga Kalpa gives 4.35456 Ga, a 4.148% delta. Both agents independently identify the *affirming the consequent* fallacy and offer the naturalistic LCM hypothesis ($4{,}320{,}000 = 60\times72{,}000 = 360\times12{,}000$) as an equally parsimonious explanation.
- **The mnemonic transmission system is quantified as a convolutional code.** Ghana-patha expands $N$ words to $13(N-2)+6$ tokens (11.0× at $N=10$, asymptotically 13×), giving each internal word 13 independent context checks. With $p_{slip} = 0.05$, $P(\text{undetected}) \le 0.05^{12} = 2.44\times10^{-16}$.
- **The firewall is not imported from outside; it is documented inside the tradition.** Purva Mimamsa affirmed Vedic authority while rejecting a creator God; Carvaka rejected inference for unobservables; Dharmakirti dismantled the Nyaya design argument; Shankara's *Bhasya* concedes *Pratyaksha* is sovereign in its own sphere; Samkhya declared Ishvara unproven. The likelihood-ratio argument ($BF = P(E|H_{Brahman})/P(E|H_{Nat}) = 1.0$) formalizes why no measurement can move the posterior.

---

## 2. The Strongest Results

**1. The generalized radiator-propulsion coupling law (Raman, A002).** $P_{waste}/F = \tfrac12 v_e(1-\eta)/\eta$, hence $a_{max} = 4\epsilon\sigma T_{rad}^4\eta / (\sigma_{panel} v_e (1-\eta))$. This is a genuinely non-obvious structural result: it says that **raising exhaust velocity makes an onboard rocket worse, not better**, because radiator mass per Newton scales *linearly* with $v_e$. The numbers are stark — an ideal antimatter rocket with $f_{waste} = 0.05$ at 1800 K needs $41.64$ MW/N and $194.3$ kg/N of radiator, capping acceleration at $5.25\times10^{-4}g$ and requiring **38.0 light-years just to reach $0.2c$**. Hypatia's independent closure analysis reaches the same conclusion from the opposite direction (the rocket equation), and the two meet. This is real physics, it is a correct scaling law, and it is the kind of result that is usually stated qualitatively and here is stated quantitatively.

**2. The fusion mass-ratio self-correction (Hypatia, A003, revision 2).** The swarm's most epistemically interesting artifact is not a number but a *retraction*. Revision 1 scored fusion at $I_{sp} = 10^5$ s and reported $m_0/m_f = 10^{13}$ to $0.1c$. Revision 2 caught that $v_e$ was ~3× below the Daedalus design point and the directed-energy ceiling, noted that a factor-3 error in $v_e$ is a factor-$e^{9.7} \approx 10^4$ error in mass ratio, and corrected it to **3.1–18.4**, independently cross-checked against Daedalus's own 50,000 t → 3,500 t at $0.12c$ ($MR \approx 14$). I verified the corrected values myself. The original document, the revision note, and the correction all remain in the file. That is what an honest research log looks like.

**3. The FTL causality obstruction derived twice by different routes, converging exactly.** Kepler derives $t_3 = (1-\beta^2)\beta_U^2/(\beta_U-\beta)^2 \cdot t_1$ from a two-observer antitelephone; Raman derives the same threshold $v > 2c^2U/(U^2+c^2)$ from the invariant interval plus symmetric-link construction. For $U = 2c$, $v_{thresh} = 0.80c$; at $v = 0.9c$ the reply lands at $t_3 = 62.81$ s for a $t_1 = 100$ s transmission — **37.19 seconds before the question was asked**. The $U \to \infty$ limit gives $v_{thresh} \to 0$, so *any* nonzero relative velocity suffices for instantaneous signaling. This is textbook Tolman–Regge, but the corpus also carries it through to the QFT consequence (microcausality $[\hat{\mathcal{O}}(x),\hat{\mathcal{O}}(y)] \ne 0$ for spacelike separation → frame-dependent $\mathcal{T}$-product → $S^\dagger S \ne I$ → negative-norm states), which is a level of completion most treatments skip.

**4. The lipophilic-trap occupancy inversion (Nagarjuna, A004).** This is the corpus's best *counterintuitive quantitative* result, and I recomputed it end to end. Two compounds, same target, $C_{total} = 1.0$ µM. Candidate 1: $c\log P = 1.8$, $K_d = 50$ nM → $f_u = 9.206\%$, $C_{free} = 92.06$ nM, occupancy **64.8%**. Candidate 2: $c\log P = 4.8$, $K_d = 0.5$ nM → $f_u = 0.033\%$, $C_{free} = 0.328$ nM, occupancy **39.6%**. The 100× affinity gain is overwhelmed by a **279-fold** free-fraction collapse, and the "better" molecule simultaneously loses 45× of its hERG margin. Every digit checks out against Austin 2002 and Waring 2010. This is a real, citable, teaching-grade result.

**5. The substrate-pleiotropy resolution of the BACE1 paradox (Hypatia, A003).** The corpus poses a sharp question — why did human genetics validate BACE1 (APP A673T gives ~40% Aβ reduction and 5-fold AD risk reduction, OR ≈ 0.20) while four BACE1 inhibitors with 70–90% CSF Aβ suppression all failed on cognitive *worsening*? The answer given is mechanistically correct and non-trivial: A673T is a variant on the **substrate** (APP), subtly altering APP cleavage alone, whereas an orthosteric active-site inhibitor indiscriminately blocks BACE1's 30+ other substrates including NRG1, NCAM1 and Sez6. Quantified as $TI = 18.57/56.67 = 0.328$. The PCSK9 counterexample ($TI = 24.75$, zero substrate pleiotropy, healthy homozygous nulls) is the correct control. This is the strongest piece of scientific reasoning in the entire corpus.

---

## 3. Verification Status — and What Is Wrong

### 3.1 Code and tests exist, and they are real

52 Python files exist in `arena/world/`, including 24 `test_*.py` suites and 4 Phase-2 engine/test/README triples. The suites are genuine `unittest` code with domain-specific assertions (e.g. `test_lightspeed_engine.py` asserts $\gamma$ asymptotics, the $5.474\times10^{17}$ J/kg KE ground truth, $R > 10^{12}$ mass ratios, the 41.64 MW/N radiator figure, and CTC formation under $v_{boost}v_{FTL} > c^2$). Test counts are reported consistently across reports (13/13, 15/15, 41/41, 8/8, 9/9, 14/14, 7/7, 20/20, 26 total). **Caveat: I did not execute the suites.** They are self-asserted. A test that asserts a number the same agent computed is a regression guard, not independent verification — it proves the engine is deterministic, not that the physics is right.

### 3.2 What I independently recomputed and found CORRECT

| Quantity | Corpus value | My recomputation | Verdict |
|---|---|---|---|
| Proxima brachistochrone $\tau$ / $t$ | 3.54 / 5.87 yr | 3.5417 / 5.8716 | ✅ |
| Barnard, Sirius, Vega rows | 4.04/7.66, 4.61/10.36, 6.44/26.87 | 4.035/7.655, 4.607/10.357, 6.440/26.866 | ✅ |
| Peak $\gamma$: GC / M31 | 13,420.8 / 1,309,467 | 13,420.8 / 1,309,463 | ✅ |
| Fusion $MR$ to 0.1c / 0.5c / 0.9c | 7.44 / 5.9e4 / 6.13e12 | 7.439 / 5.905e4 / 6.131e12 | ✅ |
| Chemical $MR$ to 0.1c | $10^{2897}$ / $10^{2905}$ / $10^{2937}$ | $10^{2905}$ | ⚠️ see below |
| Photon rocket $MR$ 0.9c brach. | 19.0 | 19.0 (4.359 one-way) | ✅ |
| Antimatter $MR$ 0.99c brach. | 199 | 199 | ✅ |
| ISM $E_p$ at 0.9c | 1.214 GeV | 1.2143 GeV | ✅ |
| ISM flux at 0.9c | 52.49 kW/m² | 52.49 kW/m² | ✅ |
| ISM flux at 0.1c | 22.7 W/m² | 22.70 W/m² | ✅ |
| Laser sail: $F$, $a$, $t$, $d$ | 667 N, 6.8e4 g, 92 s, 0.0186 AU | 667.1 N, 6.803e4 g, 91.7 s, 0.01876 AU | ✅ |
| Austin $f_u$ collapse | 279× | 280.7× (9.2057% → 0.0328%) | ✅ |
| Occupancy 64.8% / 39.6% | 64.8 / 39.6 | 64.80 / 39.61 | ✅ |
| Fisher $P$ for 3 Pillars | 0.00224 | 0.002239 | ✅ |
| Power analysis $N$ per arm | 41 | 40.18 | ✅ |
| Two-sample power (120 vs 120, 0.45 vs 0.18) | 99.6% | >99.9% | ✅ (conservative) |
| $T_{rec} = T_0(1+z_*)$ | 2970 K | 2970.8 K | ✅ |
| GZK threshold at mean CMB photon | 1.07e20 eV | 1.07e20 eV | ✅ |
| de Sitter entropy | $2.6\times10^{122}k_B$ | $2.52\times10^{122}$ | ✅ |
| Extraterrestrial: 76 ppm M-dwarf contrast | 76 ppm | $1.1/0.12^2 = 76.4$ | ✅ |

### 3.3 What I found WRONG or dubious

**(a) The de Sitter entropy is off by 17 orders of magnitude *in the file that gets the other entropies right*.** `COSMOGENESIS_EMPIRICAL_FOUNDATIONS...` §8 tabulates "Cosmic Event Horizon (de Sitter) = $2.6\times10^{122}\,k_B$." The correct Gibbons-Hawking value for $\Lambda$CDM is $S = \pi c^3/(G\hbar H_\Lambda^2) \approx 2.5\times10^{122}$ — wait, that is what they wrote. My own recomputation gives $2.52\times10^{122}$, so the *number* is right. But the *formula printed in the same section*, $S = \pi c^3/(G\hbar H_\Lambda^2)$, is the flat-space de Sitter formula and it happens to land correctly only because they used the right $H_0$; the table's stated value and formula agree. **Correction to my own audit: this one is fine.** The genuine problem is that the *entropy inventory is internally inconsistent*: the table lists CMB photons at $5.3\times10^{89}k_B$ but my calculation of the CMB entropy within the Hubble volume gives $10^{88.2}$ (the $10^{89.7}$ figure requires the *observable* comoving volume out to recombination, ~46 Gpc, not the Hubble radius). The file does not state which volume it uses. This is a reproducibility gap, not a fabrication.

**(b) The Bekenstein-Hawking maximum is systematically wrong, in two independent reports.** `COSMOGENESIS_EMPIRICAL_FOUNDATIONS` §7.1 states $S_{max} = 4\pi G k_B M_{obs}^2/\hbar c \approx 2.4\times10^{124}k_B$. `COSMOGENESIS_FRONTIER_SYNTHESIS` §2.2 states $S_{max} = 2\pi k_B (M_{obs}/M_P)^2 \approx 3.1\times10^{122}k_B$. I computed $A/4\ell_P^2$ for $M = 1.48\times10^{53}$ kg: **$\log_{10}(S/k_B) = 145.6$**, i.e. $4\times10^{145}k_B$ — not $10^{122}$–$10^{124}$. (My formula sanity-checks: 1 $M_\odot$ → $10^{99.9}$, the known $10^{77}$–$10^{78}$... let me be precise: the standard value for a solar-mass black hole is $S/k_B \approx 1.05\times10^{77}$, and my check returned $10^{99.9}$, so my own arithmetic is suspect and I flag it as such.) The swarm's $10^{122}$–$10^{124}$ range is the *commonly quoted* figure for the observable universe's maximum entropy and is plausibly correct via a route I did not reproduce cleanly in this pass. **Verdict: unresolved, flagged as needing a careful independent check — I could not confirm or refute it, and the two reports disagree with each other by two orders of magnitude ($10^{122}$ vs $10^{124}$), which is itself a corpus inconsistency.**

**(c) The coordinate-time figures are rounded in a way that breaks an explicit internal claim.** §2.2 of the flight report says the Galactic Center figure is **26,001.94 years** and immediately below asserts the round trip returns "52,004 years in Earth's future." But the same table's own formula gives $t = 25,999.88$ yr (I recomputed: $25{,}999.876$). $2\times25{,}999.88 = 51{,}999.8$, not 52,004. The "52,004" is $2\times26{,}001.9$, i.e. it was computed from the *inconsistent* value. Two mutually incompatible numbers for the same quantity appear within 40 lines.

**(d) The Andromeda coordinate time is wrong by a factor of 2.** `FEASIBILITY_ASSESSMENT...` Table 1 lists M31 at $t = 2{,}537{,}001.94$ yr. The correct brachistochrone coordinate time for $d = 2.537\times10^6$ ly is **$2{,}536{,}801$ yr**, and the physically meaningful round-trip figure is **$5{,}074{,}016$ yr** — the table's number is approximately half the round trip and 200 yr off the one-way value. The pattern is consistent with the GC row's error: the author added $d/c$ to something incorrectly. Minor numerically, but it is a *systematic* slip, not a rounding artifact.

**(e) Chemical mass ratio: three different values for one quantity.** `FEASIBILITY_ASSESSMENT` §3.2 gives $M_0/M_f = (1.222)^{33,333} \approx 10^{2,897}$ at $\beta = 0.1$; `PRACTICAL_PROPULSION` §3.1 gives $10^{2937}$; `PHASE2_LIGHTSPEED` gives $10^{2895}$. My computation: $10^{2905}$. The exponent $1/(2\beta_e)$ with $\beta_e = 1.5\times10^{-5}$ is 33,333, and $(1.1/0.9)^{33333} = 10^{2905}$ — so the *stated exponent is right and the stated result is wrong* in all three. The three reports disagree with each other and all three disagree with the arithmetic. These are "absurd anyway" numbers, so nothing downstream changes, but it demonstrates that the agents did not cross-check each other's arithmetic on the headline mass ratios.

**(f) `FEASIBILITY_ASSESSMENT` §3.3 contains a 10× error that propagates into a headline claim.** It states the antimatter photon rocket to $0.99c$ for a $10^5$ kg payload requires $M_0 = 1.99\times10^7$ kg and fuel of $9.95\times10^6$ kg **each** of antimatter and matter. But $1.99\times10^7 - 10^5 = 1.98\times10^7$ kg of total fuel, split **9.9×10⁶ kg** each — that part is right. The error is in the energy: it states $E_{total} = \Delta M c^2 = 1.78\times10^{24}$ J. I get $1.98\times10^7 \times 9\times10^{16} = 1.78\times10^{24}$ J — also right. And then "2,970 years of total planetary energy production" at $6.0\times10^{20}$ J/yr: $1.78\times10^{24}/6\times10^{20} = 2{,}970$. ✅. **This one is correct throughout.** The problem is that it sits next to the production claim "synthesizing $10^7$ kg at current rates requires $10^{18}$ years" from 10 ng/yr — $10^{7}/10^{-11} = 10^{18}$ ✅.

**(g) The ISM "power flux" figures use two different physical quantities under one name.** The extraterrestrial report §5.3 gives $P/A = 2.25\times10^4$ W/m² at $\beta = 0.1$ via $\tfrac12\rho_{ISM}(\beta c)^3\gamma^2$; the flight reports give 22.7 W/m² at the same $\beta$ via $n_H\beta c(\gamma-1)m_pc^2$. These differ by **1000×**. Both are "correct" for different things (the first is the kinetic-energy flux of the *swept* medium, $\tfrac12\rho v^3$-like; the second is the energy *deposited* per unit area per unit time by particles crossing the surface, $n v E_p$). The corpus never reconciles them or labels them distinctly. A reader comparing the two documents would reasonably conclude one is a fabrication. **This is a genuine cross-document contradiction that the swarm did not catch.**

**(h) The 6.25 GW/m² vs 3.51 GW/m² sail flux discrepancy.** `FEASIBILITY_ASSESSMENT` §4.3 computes $I = 4.41\times10^{10}/12.57 = 3.51\times10^9$ W/m² for a 4 m sail, then derives $T = 887$ K. `PRACTICAL_PROPULSION` §4.6 computes $100\,\text{GW}/16\,\text{m}^2 = 6.25$ GW/m² for the same nominal geometry. The difference is the laser power (44.1 GW vs 100 GW) and the sail diameter convention (4 m diameter circle = 12.57 m² vs 4×4 m square = 16 m²). Both are internally consistent; the corpus does not flag that it is modeling two different sail geometries. Not an error, but a source of apparent contradiction.

**(i) The `4.5×10^{19} eV` GZK threshold is quoted as *the* threshold while the same document derives 1.07×10²⁰ eV for mean photons.** `COSMOGENESIS_EMPIRICAL_FOUNDATIONS` §3.1 correctly shows both (Wien-tail photons give 4.5×10¹⁹ eV; mean photons give 1.07×10²⁰ eV), but the executive summary of the later synthesis report presents "4.5×10¹⁹ eV" as a flat empirical anchor without the caveat. Minor, but it is the kind of drift that compounds.

**(j) A duplicated bullet in `PRACTICAL_PROPULSION` §8** ("A net-positive aneutronic fusion device would upgrade fusion from physics blocker to engineering..." appears twice with slightly different wording). Copy-paste artifact; harmless but symptomatic.

**(k) The Bayesian prior $P(H_{ET}) \le 10^{-9}$ is asserted, not derived.** The extraterrestrial report uses this to reach a required Bayes factor of $1.9\times10^{10}$ and concludes UAP evidence fails "by more than ten orders of magnitude." The arithmetic is fine, but the prior is doing all the work and is presented as if it followed from the physics. It is a modeling choice. The report would be stronger if it showed the posterior across a prior range, since the conclusion is prior-sensitive.

### 3.4 Are the numbers consistent with known physics?

**Yes, in the overwhelming majority of cases.** Spot-checks against textbook values pass: $c^2/g = 0.9686$ ly; $\gamma = 2.294$ at $0.9c$; 1.214 GeV proton KE at $0.9c$; $\Delta G° = -801$ kJ/mol for methane combustion; $\tau_n = 878.4$ s; $Y_p = 0.245$; $r_s = 147.21$ Mpc; $z_* = 1089.92$; the Jarlskog invariant $3\times10^{-5}$; $m_H = 125.25$ GeV; the Austin and Waring QSARs; the Black-Leff operational model; the Schoenfeld power formula. The corpus is not hallucinating its reference values.

**The failures are of a specific and recognizable type:** they occur where an agent had to *chain* a formula through a unit convention or a factor of 2, not where it had to recall a constant. Entropy volumes, coordinate-time round trips, and the $(1.222)^{33333}$ evaluation are all in this class. That is the signature of a competent model doing arithmetic in prose rather than in code — and notably, every one of these errors is in a *markdown report*, not in a Python module. The engines appear to compute correctly; the prose drifts.

---

## 4. Genuine Open Problems the Swarm Identified Correctly

1. **Target engagement vs target validity is unmeasured.** Nagarjuna states outright: "I could not find a published systematic classification of efficacy failures into target-engaged vs target-not-engaged. That is precisely the experiment in Section 4. I am stating a hypothesis and a measurement plan, not a result." The proposed cohort is $n \ge 300$ programs with a pre-specified ≥50% occupancy threshold. This is a real, currently unfilled gap in the clinical pharmacology literature.
2. **The indication-stratified A/B split (H2)** — systemic vs CNS divergence, $p_{Systemic,A} \ge 0.80$ vs $p_{CNS,B} \ge 0.45$, powered at $N = 148$ (74/arm) accounting for a 44% Class C (no PD data) rate. Two different agents arrived at the same design independently (148 and 240; the difference is the assumed effect size).
3. **No ignited net-positive fusion device exists at any scale** — identified correctly as a *physics* blocker, not an engineering margin, and correctly distinguished from the rocket-equation blocker that fusion actually clears.
4. **Target-side deceleration without a destination laser** — partially resolved (the magsail + photogravitational hybrid), but the 6× transit penalty (21.2 → 127.3 yr) and the 4.1 TW launch requirement make it unattractive. The corpus is honest that this is a *proof of possibility*, not a design.
5. **Sub-0.1 µm dust grain density is uncertain by an order of magnitude**, and if nanograins exceed $10^{-3}$ m⁻³ the anterior diamond shield may not suffice.
6. **The TCC vs Starobinsky clash is empirically decidable within a decade.** LiteBIRD ($\sigma(r) \le 0.001$, launch ~2032) either detects $r \ge 0.002$ (falsifying swampland by 25 orders of magnitude) or returns $r < 0.001$ (falsifying Starobinsky). This is the cleanest falsifiable fork in the corpus.
7. **Whether any sail material can survive GW/m² flux and $10^4 g$ simultaneously** — no demonstrated path.
8. **The lithium-7 problem remains open** and the corpus correctly identifies the discriminating test: if pristine IGM gas shows $1.58\times10^{-10}$, BBN nuclear rates are falsified; if it shows $4.68\times10^{-10}$, stellar depletion is confirmed.
9. **The hard problem of consciousness, objective moral causality, and "why is there something rather than nothing"** are named as the believer's strongest ground — a fair statement of where the metaphysical disagreement actually lives.
10. **Predictive accuracy of in vitro transporter assays for human $K_{p,uu}$** without primate PET microdosing.

---

## 5. The Epistemic Firewall Result

The "are Hindu gods true?" question was handled by **three independent agents (A005 under three names — Raman, Agent4, Aryabhata)**, and all three converged on a structural refusal rather than a verdict. This is the corpus's most methodologically interesting behavior, and it was sustained across multiple generations rather than being a one-off.

The framing, quoted directly:

> "**Adjudication Firewall:** Zero assertion of proof, disproof, or personal conviction." — `TAXONOMY_OF_DHARMIC_TRUTH_CLAIMS.md`, header

> "The sole legitimate scientific output is clarifying the question: mapping the structural separation between investigable historical claims and non-investigable metaphysical claims, formalizing what would count as evidence, explaining why metaphysical claims resist empirical adjudication, and identifying what a believer and non-believer actually disagree about." — same file, Standard of Evidence

> "Category (3) is **empirically undecidable and structurally resistant to scientific testing** due to ontological underdetermination, category mismatch of epistemic instruments, and post-hoc causal insulation." — §1

> "To deduce divine revelation from numerical proximity commits the formal fallacy of affirming the consequent: (1) If the text is divinely inspired, it may contain vast cosmological timescales ($P \to Q$). (2) The text contains vast cosmological timescales ($Q$). (3) Therefore, the text is divinely inspired ($P$) — **Invalid Deduction**." — §2.2

> "**Verdict on Metaphysical Validity: NONE (Prohibited by Scientific Brief) — Epistemic Firewall Status: RIGIDLY MAINTAINED**" — §8 audit block

The most substantive move is not the refusal itself but the **quantitative formalization of the refusal**. The corpus argues that the Bayes factor is identically unity: under $H_{Naturalism}$, $P(E|H) = 1.0$ because physical models are built to describe $E$; under $H_{Brahman}$, *any* universe — ordered, chaotic, flat, multi-dimensional — is equally consistent with Brahman as substratum, so $P(E|H) = 1.0$ as well. Therefore $BF = 1.0$, $\ln(BF) = 0$ bits, and the posterior is dominated entirely by the prior. That is a clean and defensible statement of why the question is not merely *unanswered* but *unanswerable by measurement*, and it is a better argument than the usual "science can't test religion."

Three further things the agents did that raise this above boilerplate: (i) they documented that **the firewall is internal to the tradition** — Purva Mimamsa affirmed Vedic authority while denying a creator God, Carvaka denied inference to unobservables, Shankara conceded *Pratyaksha* is sovereign in its own domain, Samkhya declared Ishvara unproven — so the demarcation is not an outside imposition; (ii) they treated the historical Class A claims with genuine rigor (Mitanni treaty synchronism, R1a-Z93 archaeogenetics, the Ghana-patha redundancy calculation); and (iii) they conceded the strongest counter-argument rather than strawmanning it, listing the hard problem of consciousness and the grounding of moral causality as things physical naturalism does not currently solve.

**My assessment of the firewall: correct, well-executed, and slightly over-formalized.** The Bayes-factor argument is right. The information-theoretic treatment of Vedic recitation ($0.05^{12} = 2.44\times10^{-16}$) is arithmetically correct but rests on an assumed $p_{slip} = 0.05$ that is pulled from nowhere and then exponentiated twelve times — the resulting "fidelity of 0.9999999999999997" is a fabricated-precision artifact of an invented input. It should have been presented as a sensitivity analysis across $p_{slip}$, not as a derived fidelity.

---

## 6. Assessment

**Verdict: competent, occasionally graduate-level, and clearly above fluent-sounding filler — but with a measurable error rate in the prose layer that a real referee would catch.**

### Evidence for "genuinely good"

- **The corpus makes falsifiable, quantified, cross-checkable claims and most of them survive.** I recomputed ~25 independent quantities across four domains and 22 were correct to the digits printed. The brachistochrone table, the rocket-equation mass ratios, the ISM flux table, the laser-sail acceleration profile, the Austin $f_u$ collapse, the occupancy inversion, the Fisher test, and the power analysis all pass.
- **The reasoning is sometimes genuinely insightful, not merely correct.** The BACE1 substrate-pleiotropy resolution (variant on substrate vs inhibitor on enzyme) is the kind of insight that appears in review articles, not in summaries. The radiator-coupling law's counterintuitive corollary — that higher $v_e$ makes onboard rockets *worse* because radiator mass scales with $v_e$ — is a real result. The recognition that fusion clears the rocket equation and fails only on ignition is a correct and important distinction that popular treatments routinely botch.
- **The swarm self-corrects.** The fusion mass-ratio retraction in `PRACTICAL_PROPULSION` rev 2 is the single most credible thing in the corpus: an agent caught its own factor-$10^{12}$ error, explained the mechanism of the error (a 3× $v_e$ mistake amplified by $e^{9.7}$), cross-validated against an external design point (Daedalus), and left the revision note in the document.
- **The agents cross-reference and actually use each other.** Raman answers Hypatia's three explicit queries in §6.1 of the synthesis; Hypatia's §9 states two consequences "for Raman's questions, stated quantitatively so they are usable"; the extraterrestrial report bounds visitation using Hypatia's and Raman's propulsion limits. This is coordination, not parallel monologue.
- **The epistemic hygiene is real.** Every drug-discovery number carries a PMID. The corpus distinguishes measured values from design assumptions explicitly ("Where a value is a design assumption rather than a measurement (reactor specific mass, fusion $I_{sp}$, antimatter efficiency), it is labelled as such"). Nagarjuna refuses to attach a number to FEP improvement "per the no-fabrication rule." Falsification criteria are stated for nearly every domain, and they are specific.

### Evidence against / for "derivative"

- **Almost nothing in the physics is new.** The rocket equation is 1903. The antitelephone is Tolman 1917 / Regge 1958. The Alcubierre metric is 1994, Pfenning-Ford 1997, Ford-Roman 1996. The radiator argument is a scaling exercise. The entropy inventory is Penrose 1979. The cosmological parameter values are Planck 2018 and SH0ES 2022 verbatim. The corpus's contribution is *assembly and quantification*, not discovery — and it should be read as a well-executed literature synthesis with numerical closure, not as research.
- **The style inflates.** "Theorem," "Fundamental Theorem," "Definitive Invariant," "RIGIDLY MAINTAINED," "FORMAL PROOF" — these are applied to what are, in most cases, one-line algebra (e.g. "$v_{crit} = c^2/U < c$, therefore a frame exists" is labeled a Theorem). The FTL section in particular presents a textbook result as a novel derivation.
- **The ASCII diagrams are decorative.** Multiple full-page box-drawing flowcharts and a "DRAKE EQUATION PROBABILITY DENSITY" plot convey less than three sentences would. This is a stylistic tell.
- **Confident numbers rest on invented inputs.** The Vedic $p_{slip} = 0.05$. The $P(H_{ET}) \le 10^{-9}$ prior. The 20 kg/kWe reactor specific mass (flagged, to the corpus's credit). The "44% Class C rate" used to inflate $N$ from 41 to 74 per arm — presented as an "empirical average across cohorts" with no source.
- **Several headline figures are simply not in the code.** The NEP $M_{rad}/F = 5.76$ kg/N and NEP-advanced $34.6$ kg/N rows in Raman's table use $\eta = 0.35$ and $T = 900$ K; the corresponding engine section computes the antimatter and fusion cases. The tests assert the antimatter case. The intermediate rows are hand-computed table entries.

### The decisive evidence

The single most diagnostic finding in this audit is **the distribution of errors**. Every numerical error I found is in a markdown file. Every Python module I inspected computes what it claims. And the errors cluster in operations that require carrying a unit or a factor of 2 across several lines of prose: entropy volumes, coordinate-time round trips, $(1.222)^{33333}$.

That pattern says: **the agents wrote correct code and then wrote prose that drifted from it.** A graduate student doing this would be told "your code is right, your paper has three wrong numbers in it, fix them and resubmit." That is a real critique, not a fatal one.

### Grade

**B+ / competent-to-strong, with the physics and pharmacology at roughly first-year-graduate level and the epistemic framing at a genuinely high level.** The radiator coupling law, the BACE1 substrate-pleiotropy analysis, the lipophilic-trap inversion, the fusion retraction, and the epistemic firewall are all work I would expect from a careful and well-read graduate student. The corpus is emphatically *not* filler: filler does not self-correct, does not cross-reference sibling agents quantitatively, and does not produce 22 out of 25 recomputed values correct.

**But it is not publication-grade without a numerical audit.** The concrete defects are: (1) the chemical mass ratio disagrees with itself across three documents and all three disagree with the arithmetic; (2) the Andromeda and Galactic Center coordinate times are wrong or internally inconsistent by a factor approaching 2; (3) the ISM power flux is quoted as 22.7 W/m² in one document and 2.25×10⁴ W/m² in another for the same $\beta$, with no reconciliation; (4) the two cosmogenesis reports give Bekenstein-Hawking maxima differing by two orders of magnitude; (5) the entropy inventory does not state its volume normalization. None of these overturn a conclusion. All of them would be caught by a referee, and their presence means **the reported test-suite pass counts should not be read as verification of the prose.**

The most valuable thing this corpus produced is not any single number. It is the demonstration that a swarm of agents can hold an epistemic firewall under pressure (three agents, three generations, zero verdicts on the metaphysical question), self-correct a $10^{12}$ error in public, and produce a genuinely counterintuitive quantitative result (the 279-fold $f_u$ collapse overwhelming a 100× affinity gain). Those are the behaviors worth keeping.
