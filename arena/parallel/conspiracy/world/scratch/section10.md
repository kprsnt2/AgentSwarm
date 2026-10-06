---

## 10. Third pass — `derivation3.py` (2026-10-06)

A third computational block was run to close the two quantitative gaps the first two passes had explicitly left open, and to turn one further *observed* fact into a *test*. Full script output is saved as `scratch/derivation3.out`; the script is `derivation3.py`. Inputs are marked **(V)** = verified live in this session from the source named, or **(A)** = assumed parameter, each scanned over a stated range. Nothing is fitted.

### 10.0 Corrections to the first two passes

Re-verification against the live sources changed three things:

1. **Retracted (unverified).** The first draft stated that "Luna 16 returned 101 g from Mare Fecunditatis … and its dark basalt indicated a close resemblance to soil recovered by the American Apollo 12 mission," citing *Wikipedia, "Luna 16"*. The retrieved text of that article does **not** contain either statement. Both have been removed from §1 and §3.3 and are here marked as unverified. The ~101 g figure is widely published and is probably right, but "probably right" is not a citation, so it is not asserted.
2. **Corrected.** The Sotheby's sale of Luna 16 material was recorded as "three 0.2 g fragments … US$442,500 (1993) and US$855,000 (2018)". The live text says "Three tiny samples (0.2 grams) … sold at Sotheby's auction for $442,500 in 1993 … resold by Sotheby's for US$855,000 on 29 November 2018", and *Wikipedia, "Moon rock"* confirms the fragments weigh **200 mg in total**. Corrected to "three fragments totalling 0.2 g (200 mg)", with the resale date fixed at 29 November 2018.
3. **Confirmed and extended.** The 10 June 1971 Soviet/NASA sample exchange is confirmed verbatim: "On 10 June 1971, the Soviet Academy of Sciences exchanged Luna 16 samples with NASA in Moscow, receiving samples from Apollo 11 and Apollo 12." A further 0.4825 g Luna 16 sample from a depth of 27 cm was sent to Britain.

### 10.1 The lunar laser ranging link budget, computed from first principles

Claim (b) was previously supported by the *observed* fact that the retroreflectors return ~1–5 photons. An observation is an input, not a test. This block computes the entire chain and compares the result with the observation.

**Verified inputs (V)** — *Wikipedia, "Lunar Laser Ranging experiments"*: 3 × 10¹⁷ photons per pulse emitted; beam **6.5 km** wide at the Moon's surface; mean Earth–Moon distance **385,000.6 km**; round trip **2.568 s**; **1–5 photons** received back; fitted range residual **1 cm weighted rms**. Apollo 11 array: **46 × 46 cm panel**, Mare Tranquillitatis, 0.6734° N 23.4731° E, placed 21 July 1969, still operational (*Wikipedia, "List of retroreflectors on the Moon"*, citing NIST and Wagner et al. 2012).

**Assumed parameters (A)**, each scanned: ruby wavelength 694.3 nm; 3.8 cm corner-cube aperture × 100 cubes = 0.1134 m² projected aperture = **54% of the 46 × 46 cm panel**; detector quantum efficiency 0.05–0.10.

| Step | Computation | Result |
|---|---|---|
| 1 | photon density at the Moon = 3 × 10¹⁷ / π(3.25 km)² | 9.04 × 10⁹ photons m⁻² |
| 2 | intercepted by the array = ρ × 0.1134 m² | 1.03 × 10⁹ photons (fill factor 3.4 × 10⁻⁹) |
| 3 | return footprint radius at Earth = (λ/d) × 385,000.6 km | **7.03 km** (λ/d = 3.77 arcsec) |
| 4 | fraction into a 3.1 m telescope | 4.86 × 10⁻⁸ |
| 5 | photons arriving at the telescope | **49.8** |
| 6 | photons *detected* at QE = 0.05 / 0.10 | **2.5 / 5.0** |

**No parameter was fitted to the observed return, and the prediction (2.5–5.0 photons) lands inside the observed 1–5.** Sensitivity over beam width 2–13 km and a retroreturn divergence 1–8× diffraction-limited spans 0.02–53 predicted photons, which brackets the observation; the honest strength of the claim is "right order of magnitude to within a factor of a few". Inverting, the observed 1–5 photons require an effective retroreflecting aperture of **10²–10³ cm²** — a square panel 10–30 cm across. At QE = 0.10, exactly **five** returned photons is what a **100-cube** array delivers. That is what the hardware is.

**The decisive exclusion is the alternative.** A return from the *bare* lunar surface (Lambertian, albedo 0.05–0.20) delivers **0.012–0.049 detected photons per pulse — 51–205× weaker** than the array. And it is too broad in time: the measured 1 cm residual requires the round trip to be timed to 2Δr/c = **66.7 ps**, whereas a diffuse return is spread over the depth of the illuminated footprint — a geometric sagitta of 3.04 m for a 6.5 km spot on a 1,737.4 km sphere, i.e. **20.3 ns**, and real relief makes it larger. That is a factor of **≥300** too broad. A corner-cube array, being <1 m in extent, is not. So the signal actually detected cannot be a diffuse surface return: it is ≥50× too bright and ≥300× too sharp.

**Three nations' hardware, verified as operational.** Apollo 11 (21 Jul 1969, 0.6734° N 23.4731° E, 46 × 46 cm); Lunokhod 1 (17 Nov 1970, 38.3152° N 35.0080° W, 44 × 19 cm); Apollo 14 (31 Jan 1971, 3.6442° S 17.4786° W); Apollo 15 (31 Jul 1971, 26.1334° N 3.6285° E); Lunokhod 2 (15 Jan 1973, 25.8323° N 30.9221° E); **Chandrayaan-3 (23 Aug 2023, 69.3676° S 32.3481° E, a single 5.11 cm reflector)**. A hoaxed Apollo programme must therefore explain why Soviet and Indian arrays at independently documented coordinates return pulses at the same international stations, and why the Apollo array returns one too.

### 10.2 Sleep paralysis: the supply of the requisite phenomenology, in absolute numbers

Claim (d) rested on the base rate being "known". Block B converts it into absolute counts. Verified base rates (*Wikipedia, "Sleep paralysis"*): 8–50% lifetime prevalence, **~5% recurrent**, episodes 1–6 minutes, and the canonical triad of intruder / incubus (chest pressure) / vestibular-motor disorientation.

| Quantity | World (≈8.1 × 10⁹) | United States (≈3.4 × 10⁸) |
|---|---|---|
| will ever experience sleep paralysis (upper bound) | 4.05 × 10⁹ | 1.70 × 10⁸ |
| experience it recurrently (~5%) | 4.05 × 10⁸ | 1.70 × 10⁷ |
| episodes per year at 1/month | 4.9 × 10⁹ | 2.0 × 10⁸ |
| episodes per year at 1/week | 2.1 × 10¹⁰ | 8.8 × 10⁸ |
| episodes per year at 1/year | 4.1 × 10⁸ | 1.7 × 10⁷ |

Against the documented claimant population of **1,700**, the recurrent supply alone exceeds it by **2.4 × 10⁵** (≈5 orders of magnitude). The phenomenon does not need an external cause to be produced at any rate at which it is reported.

One numerical coincidence is reported because it is real, and flagged because it is not decisive: the contested surveys' implied abduction rate (**5–6%** of the population) is the same order as the recurrent sleep-paralysis base rate (**~5%**). Two ~5% figures can coincide; neither is a controlled measurement of the other. This is a pointer to a test (polysomnography during reported events), not a result.

### 10.3 The expected detection rate — the computation the first pass admitted it had not done

The first pass stated plainly: "I have not computed an expected detection rate, so the ~95% figure it supports inherits that unquantified step." That is the computation.

Model: under hypothesis **H_A** (*n* physical abductions), each event independently leaves a verifiable record — photograph, video, radar track, medical record, third-party witness, physical trace — with probability *p*. Then **P(no record in the entire history | H_A) = (1 − p)ⁿ**. Solving for the largest *p* at which the observed silence still has probability ≥ 5% (call it *p*⁎):

| Assumed number of events *n* | *p*⁎ (per event) | i.e. worse than 1 in |
|---|---|---|
| 1,700 documented claimants | 1.76 × 10⁻³ | 568 |
| 300 (Bullard's case set) | 9.94 × 10⁻³ | 101 |
| 1% of the US population | 8.81 × 10⁻⁷ | 1.1 × 10⁶ |
| 5% of the US population | 1.76 × 10⁻⁷ | 5.7 × 10⁶ |
| 6% of the US population | 1.47 × 10⁻⁷ | 6.8 × 10⁶ |
| 5% of world population | 7.40 × 10⁻⁹ | 1.4 × 10⁸ |

| *n* | P(no record) at p = 10⁻² | at p = 10⁻³ | at p = 10⁻⁴ | at p = 10⁻⁶ |
|---|---|---|---|---|
| 1,700 | 3.8 × 10⁻⁸ | 1.8 × 10⁻¹ | 0.84 | 0.998 |
| 300 | 4.9 × 10⁻² | 0.74 | 0.97 | 1.00 |
| 5% of US | < 10⁻³⁰⁰ | < 10⁻³⁰⁰ | < 10⁻³⁰⁰ | 4.1 × 10⁻⁸ |
| 5% of world | < 10⁻³⁰⁰ | < 10⁻³⁰⁰ | < 10⁻³⁰⁰ | 1.3 × 10⁻¹⁷⁶ |

**The honest reading, including where the argument fails.** For *n* = 1,700 documented claimants and *p* = 10⁻³, P(no record) = **18%** — the silence is *not* surprising, and the detection-rate argument is weak on the documented count alone. It carries only if the contested 5–6% survey figures are right. Those surveys are described as "contested" by the source itself, so this step is an assumption, not a result, and it is labelled as one. What survives independently of *n* is the **directional** argument: under H_A the per-event recording probability *p* rises monotonically as instrumentation per capita rises — 1961 had no camera phones, no home video, no dashcams, no CCTV, while a 2026 bedroom commonly contains an always-networked camera — so the expected number of detections per decade should have **risen** by orders of magnitude. The reported incidence is instead asserted to have declined from its mid-1970s peak. A physical phenomenon does not become less recordable as recording devices improve. The direction of the trend is the test, and it runs opposite to the physical prediction.

### 10.4 Dated content: a falsifiable prediction of the "stable phenomenon" hypothesis, and its failure

H_A (a stable real phenomenon with stable content) predicts that narrative elements appear at a roughly constant rate across all decades in which reports were collected, and do not track the publication history of a few authors. Verified from *Wikipedia, "Alien abduction"*:

- The "grey" beings and the explicitly extraterrestrial framing entered with the **Betty and Barney Hill case (1961)**, while "purported abductions were cited contemporaneously at least as early as 1954"; earlier cases do not carry the later template.
- The **"child presentation" phase** has a *birth date in the literature*: "Bullard says the child presentation phase seems to be an innovation in the story" with "no clear antecedents … before its popularization by Hopkins and Jacobs" — and Bullard, studying ~300 reports, "could not identify a child presentation phase in the abduction narrative."
- "Many alien abductees recall much of their alleged abduction(s) through hypnosis", and Hopkins began "using hypnosis to extract more details" in the 1970s.

So a specific element of the narrative post-dates the earliest reports by 10–20 years and coincides with the work of two named authors. Under H_A this is a **failed prediction**: the phase should be present throughout.

And the phenomenology is now **reproducible on demand**. A 2021 study in the *International Journal of Dream Research* instructed volunteers to emulate alien encounters by lucid dreaming: **114 volunteers (75% of the sample) succeeded**, and of those **~20% produced accounts rated close to reality** in their absence of dreamlike events — with sleep paralysis and fear observed "only among this 20% … common in 'real' stories." Ordinary people asked to produce the experience can produce it. That is the strongest single new datum for claim (d) in this pass.

---

## 11. Verdicts, revised after the third pass

Nothing in the third pass changed any verdict; two claims were strengthened quantitatively and one confidence basis was made explicit.

| Claim | Verdict (unchanged) | Confidence | What the third pass added |
|---|---|---|---|
| (a) Flat Earth | **F** | **>99.9%** | nothing new; already the strongest position in the report |
| (b) Moon landing faked | **F** | **>99.9%** | the observed retroreflector return is now *predicted* from a first-principles link budget rather than merely cited; the bare-surface alternative is excluded by ≥50× in flux and ≥300× in timing; three nations' operational arrays confirmed at published coordinates |
| (c1) Area 51 real | **T** | **>99.9%** | re-verified verbatim (CIA acknowledgment 25 June 2013; Homey Airport KXTA/XTA; the A-12 JP-7 fuel farm of 1,320,000 US gal) |
| (c2) Roswell extraterrestrial | **N/E** | **<2%** | re-verified verbatim (Mogul Flight 4, launched 4 June 1947, lost within 17 mi; *Case Closed* 24 June 1997; the 8 July 1947 FBI telex's hexagonal object on a ~20 ft balloon) |
| (c2′) Bodies recovered | **actively disconfirmed** | — | unchanged |
| (d) Alien abduction | **N/E** | **>95%** not literal; **>99%** not physically corroborated | the "expected detection rate" admission is closed by an explicit computation (§10.3), together with the exact conditions under which that argument is weak and must be conceded; a new controlled emulation result (§10.4); sleep-paralysis supply quantified in absolute episodes per year (§10.2) |

---

## 12. What would change my mind — consolidated, in priority order

Ordered by how cheap the disconfirming experiment is.

1. **Flat Earth.** One verified observation, by anyone with a sextant and a theodolite, of a receding vessel disappearing hull-down at a range consistent with flat geometry; or two sites where the noon-shadow difference fails to equal the latitude difference; or a southern-hemisphere flight that takes 2.2× its published great-circle time. Cost: a few hundred dollars.
2. **Moon landing faked.** Range the Apollo 11 array's coordinates (0.6734° N, 23.4731° E) with a pulsed laser and fail to get a pulse, while succeeding from Lunokhod 1's (38.3152° N, 35.0080° W); or date an Apollo basalt and get a terrestrial age; or have a non-US orbiter resolve no hardware at the documented coordinates. Cost: a large telescope and a picosecond laser, or one interplanetary mission.
3. **Roswell.** One analysable artefact with authenticated 1947 provenance and non-terrestrial isotopic composition that survives blinded characterisation in several independent laboratories. Cost: possession of the artefact.
4. **Alien abduction.** One recording, one verified implant, one confirmed falsifiable prediction, or two mutually unacquainted claimants matching verifiable detail against timestamped independent records. Cost: a phone.

None of (1)–(4) exists. In (1) and (2) the disconfirming experiments are cheap enough that anyone reading this could in principle run them; in (3) and (4) they require possession of evidence that, in 79 and 60+ years respectively, has never been produced.
