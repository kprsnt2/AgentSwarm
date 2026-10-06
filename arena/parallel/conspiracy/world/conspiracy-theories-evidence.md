# Do the evidence: four conspiracy claims on the evidence table

| | |
|---|---|
| **Agent** | Kepler (A001), generation 0 |
| **Domain** | conspiracy-theories-evidence |
| **Epistemic class** | Empirical |
| **Date of research** | 2026-10-06 (five passes; sources re-fetched live in each) |
| **Method** | Steelman → evidence for/against → decisive quantitative test → verdict + confidence → explicit "absent vs. disconfirming" flag. Sources retrieved live via the MediaWiki/Wikipedia API and cross-checked; all geometry and geodesy numbers in §8 and §9 were recomputed locally from first principles so that every quantitative claim is reproducible. Four verification passes, each of which found and fixed errors in the previous ones — including **two errors in my own provenance checking** (§10.0 item 1, §13.2), which is itself reported because it bears on how the rest should be read. A fifth pass added two further positive measurements of Earth's orbital motion to claim (a) (§14) and closed the two figures pass 4 had flagged unverified; it also introduced and fixed three defects of its own (§14.6). A **sixth pass** (§16) added a thirteenth class of measurement for claim (a) — the first that is *relativistic* rather than dynamical or gravitational (Sagnac, ring interferometry, the operational GNSS rotation correction) — added a new decisive test for claim (b) (the **coordinate-dependence** of the laser return, demonstrated by Lunokhod 1), converted pass 4's open "Mogul wind field" item into a computed 158.7 km trajectory requirement, and quantified the Blue-Book base rate for claim (d). It introduced and fixed five defects of its own (§16.6). |
| **Ground truth relied on (per brief)** | Retroreflectors placed by Apollo 11/14/15 still return pulses; Apollo returned ~382 kg of samples; Area 51 is a real classified USAF facility at Groom Lake; Project Mogul was a real classified balloon program; the 1997 USAF report "The Roswell Report: Case Closed" is a real document; Eratosthenes estimated Earth's circumference c. 240 BC. None of these are contradicted below. |

**Confidence convention.** A single number is never given as "certain." Values are expressed as an assessed probability that the claim-as-stated is true. ">99.9%" is reserved for cases where multiple independent, quantitative measurements contradict the claim by orders of magnitude. **These confidence numbers are subjective Bayesian judgements, not measured quantities**: "<2%", ">98%", ">95%" and ">99%" are my stated credences given the evidence marshalled, offered so that they can be argued with. They are not derived from a formal prior-and-likelihood calculation, and no sensitivity analysis over priors is given. The operative part of each verdict is the "what would change my mind" section that accompanies it.

---

## 1. REQUIRED DELIVERABLE — per-claim evidence table

Legend for the verdict column: **F** = claim is false; **T** = claim is true; **N/E** = not established; evidence does not support it. "Absent" = the evidence is missing; "Disconfirm" = evidence actively points the other way.

| # | Claim (steelman) | Evidence for | Evidence against | Decisive quantitative / observational test | Verdict | Confidence |
|---|---|---|---|---|---|---|
| **(a)** | **Flat Earth.** Earth's habitable surface is a stationary plane (typically a disc centred on the North Pole, ringed by an ice wall in Antarctica) rather than an oblate spheroid of mean radius 6,371 km. | Rowbotham's 1838 Bedford Level "no curvature" observation over 6 mi; the visual flatness of large water bodies; the claim that the horizon always rises to eye level. | Eratosthenes' 240 BC result (250,000 stadia → 39,375–46,250 km depending on the stadion, central estimate ≈40,300 km, vs 40,075 km modern); two-site noon-shadow geometry reproduced today (Memphis–New Orleans meridional arc 578.0 km over 5.1984° → R = 6,371 km, +0.00%; a single solar altitude cannot fit two site pairs, differing by a factor of 1.8 for one pair); mutually exclusive star fields (Polaris never rises below ~0.7° S; Southern Cross never rises north of ~26° N); hull-down ship concealment with 17.5 m of a 20 m superstructure hidden at 20 km; Foucault precession 15.04°/h × sin(lat); gravity 9.7803 → 9.8322 m/s² equator→pole (+0.53%, WGS-84 Somigliana); verticals converge at ~1 arcmin per nautical mile (59.96 arcsec); GNSS/geodetic solutions in a geocentric frame fit surveys to ~cm; southern great-circle routes 2.2–2.4× shorter than the flat-disc prediction; 6-month South-Pole daylight and a single annual sunrise/sunset; a setting Sun that neither shrinks (predicted 4.26× smaller) nor loses its upper limb (the lower limb is occluded first); GPS orbital period matching Kepler's third law to 0.01% and geostationary altitude matching the published 35,786 km (this test is conditional on inverse-square gravitation, which is independently established). | (1) Simultaneous noon shadow angles at two sites of known separation — on a sphere the difference in noon elevation equals the latitude difference; the meridional arc between Memphis and New Orleans, 578.0 km over 5.1984°, gives R = 6,371 km (+0.00%), and Eratosthenes' own 5,000 stadia gives R within −1.6%/+15.5% of the stadion (§2.3a, Test 4). (2) Compare a southern-hemisphere scheduled flight time/distance with the spherical and flat-disc (azimuthal-equidistant) predictions: Sydney–Santiago 11,340 km (globe) vs 25,679 km (disc); Perth–London computed 14,508 km vs published 14,498 km (0.07%). (3) Range a receding vessel: hull should be *concealed below the sightline*, not merely shrink. (4) Laser-range the Apollo retroreflectors (§3). (5) Photograph the horizon dip from 30 m altitude: predicted 0.176°, flat plane predicts 0°. (6) Measure the Sun's angular size at sunrise and noon: constant ~0.53°, with the *lower* limb disappearing first — impossible on a flat plane where the Sun recedes. (7) Compute the disc model's own South-Pole prediction: Sun up 365 days/yr at 21–33° elevation, never setting, vs ~179 days observed (§2.3a). (8) Kepler's third law on the GPS constellation: 11.966 h computed vs 11.967 h observed (§2.3a). (9) **Rotation measured by relativistic rather than dynamical means (§16.1):** the Michelson–Gale–Pearson ring interferometer of 1926 — a 1.9 km-perimeter ring, large enough to see Earth's own angular velocity — measured a fringe shift of **230 parts in 1000** (accuracy ± 5) against a predicted **237**, i.e. 0.9705 ± 0.0211, a residual of 1.40σ, and **46 standard deviations from the zero shift** a stationary plane requires. Independently, a one-way relay of pulses around a great circle shows a Sagnac delay Δ*t* = 2*A*Ω/*c*² of **207.4 ns = 62.17 m of light travel** (computed here from first principles; the verified published value is 207 ns, agreeing to 0.19%), and a GNSS receiver must carry a Sagnac term of up to **274.6 ns = 82.3 m of light travel**, while a stationary plane predicts exactly 0 for both. Ring-laser gyroscopes are self-calibrating — "The beat frequency will be zero if and only if the ring laser setup is non-rotating with respect to inertial space." (10) **Annual stellar parallax and stellar aberration (§14):** on a stationary plane with the stars on a dome at 1,000–10,000 mi, *every* star must show an annual parallax of 1.9 × 10⁹–1.9 × 10¹⁰ arcsec and zero aberration; measured, the nearest star shows 0.768″ (Gaia DR3) and stars show ~20″ of annual aberration from Earth's 29.78 km/s orbital motion. The exclusion is ~9–10.4 orders of magnitude and is independent of every flat-model parameter. | **F** | **>99.9%** (evidence *disconfirms*, not merely absent) |
| **(b)** | **The Moon landing was faked.** The six crewed Apollo landings (1969–1972) were staged, on Earth or in a studio, and the hardware left on the Moon, the samples and the telemetry were fabricated or doctored. | No independent footage existed to the public at the time beyond NASA releases; a handful of photographic oddities (crosshairs, "C" props, the flag) that are individually anomalous to a lay reader; genuine historical record gaps. | Laser retroreflectors left by Apollo 11/14/15 still return pulses (first success 1 Aug 1969, 3.1 m Lick telescope; round-trip ~2.5 s; 3×10¹⁷ photons sent, ~1–5 returned; mm-precision; 1 cm weighted-rms residual); 381 kg of samples from six missions (Apollo 11 alone 21.55 kg; Apollo 15 77 kg), radiometrically dated 3.16–4.44 Ga, with mineralogy first discovered in Apollo samples (armalcolite, tranquillityite, pyroxferroite); >370 lunar meteorites totalling >1,090 kg found independently on Earth; Soviet Academy of Sciences exchanged Luna 16 material for Apollo 11/12 samples on 10 June 1971; five ALSEP stations operated to 30 Sep 1977 and their transmitters were received by the Soviet RATAN-600 telescope 18 Oct–28 Nov 1977; four seismometers ran unattended from Apollo 12's landing on 19 Nov 1969 to the 1977 shutdown (**7.87 years**, 2,872 days) and logged 28 shallow moonquakes in 1972–77 (mB up to 5.5, deep events ~700 km down, probably tidal), with Apollo 11's EASEP seismometer sensitive enough to detect a sleeping astronaut moving inside the LM; the Heat Flow Experiment measured a thermal gradient of 1.5–2.0 K/m and a heat flow of ~17 mW/m², from which a regolith conductivity of 8.5–11.3 mW/(m·K) follows by Fourier's law; Luna 16 returned 101 g from Mare Fecunditatis and its "dark basalt material indicated a close resemblance to soil recovered by the American Apollo 12 mission"; LRO images at 0.5 m/pixel show descent stages, rovers, ALSEP hardware and astronaut tracks, with 5 of 6 flags still upright in 2012; Great Soviet Encyclopedia (3rd ed., 1970–79) reported the landings as factual; Apollo transit dose <1 rem (10 mSv) ≈ 3 years of sea-level background, rebutting the Van-Allen kill-claim. | (1) Fire a laser at the claimed coordinates and demand a returned pulse: a co-operating array at a mean Earth–Moon distance of 385,000.6 km (semi-major axis 384,400 km) is a machine-readable, one-way test that requires the hardware to *be there*. The full link budget is now computed from first principles in §10.1 and reproduces the observed ~1–5 returned photons with no fitted parameter; the bare-lunar-surface alternative is excluded by **≥50× in photon flux** (the hard exclusion — its return is also ~300× too broad in time to carry the required 66.7 ps, which is a *supporting* point rather than a standalone argument, per §10.1 and §10.5). Three nations' arrays (USA 1969–71, USSR 1970–73, India 2023) all return pulses, so a faked Apollo would have to coexist with working Soviet and Indian hardware at independent coordinates. (2) Ask any independent geochronology laboratory to date an Apollo basalt and a Luna 16 / lunar-meteorite sample and compare with the terrestrial rock record (oldest Earth rocks 3.8–4.28 Ga). (3) Image the sites from a non-US spacecraft: LRO's 0.5 m/pixel NAC frames already resolve a ~9 m LM descent stage and 30 cm-wide boot tracks. (4) Receive the ALSEP carriers yourself (as RATAN-600 did). (5) Astrometry of the Apollo 16 Far Ultraviolet Camera frames — the star positions in those images match orbital-UV-telescope observations for the time and place, an independent, falsifiable check. | **F** | **>99.9%** (evidence *disconfirms*) |
| **(c1)** | **Area 51 is a real, classified USAF installation.** Groom Lake / "Homey Airport" (ICAO KXTA, FAA LID XTA), a detachment administered from Edwards AFB inside the Nevada Test and Training Range, whose existence and functions were officially denied for decades. | Declassified CIA/USAF history; the facility is publicly visible from the surrounding roads and on open satellite imagery. | None — the claim is uncontested and independently documented. | Direct: the CIA publicly acknowledged the base's existence on 25 June 2013 in response to a 2005 FOIA request, and declassified documents detail its 1955 creation for Project Aquatone (U-2) and its later A-12 OXCART, D-21 and (late-1960s onward) captured-Soviet-aircraft test programmes. | **T** | **>99.9% (documented; declassified by the CIA itself)** |
| **(c2)** | **The 1947 Roswell debris was recovered extraterrestrial craft, with recovered non-human bodies.** | Testimony from Jesse Marcel (recanted weather-balloon story, 1978); ~300 later witnesses; the 1980 book *The Roswell Incident*; the 1991 *UFO Crash at Roswell* (160,000 copies). | Every physical artefact ever offered has been falsified or traced: debris matched a Mogul balloon train launched from Alamogordo AAF on 4 June 1947 that lost contact within 17 mi (27 km) of the Brazel ranch; the debris field was several acres of tinfoil, rubber, tape and thin wooden beams with "no engine or metal parts"; an FBI telex of 8 July 1947 describes a hexagonal object suspended by cable from a ~20 ft (6.1 m) balloon; the 1994/1995 USAF reports and the 1997 *Case Closed* report (24 June 1997) attribute the debris to Mogul and the "bodies" to 1950s anthropometric test-dummy recoveries (Operation High Dive) carried on stretchers, casket-shaped crates and insulation bags resembling body bags; the "alien autopsy" film was admitted by Ray Santilli in 2006 to be a fabrication shot in a London living room; the Majestic-12 documents were admitted by Bill Moore to be typed/stamped facsimiles; the "star witness" Glenn Dennis fabricated the names of his nurse sources; the body-corpse motif entered the legend via the documented 1948 Aztec hoax and "Hangar 18" fiction; Pflock's audit: of 300+ witnesses, only 23 could plausibly claim to have seen debris and only 7 suggested otherworldly origin; the GAO probe found no Roswell documents at CIA and no Majestic-12 records. | (1) Any non-terrestrial artefact must survive blinded, independent isotopic and structural characterisation in a qualified laboratory — exactly the standard the 381 kg of Apollo samples passed and that no Roswell artefact has ever been submitted to successfully. (2) A documented chain of custody from 1947 to an analysable object exists. (3) The debris chemistry must exclude terrestrial materials — it did not (polyethylene, balsa, tape, foil). | **N/E** (not established; the specific positive evidence offered is *disconfirmed*) | **<2%** that the 1947 debris was extraterrestrial; **>98%** that a classified balloon train explains it. Body/autopsy sub-claim: **actively disconfirmed** |
| **(d)** | **Alien abduction.** Some people are physically taken against their will by non-human intelligences and subjected to examinations; reports are substantially veridical memories. | A stable cross-case narrative structure (Bullard's comparative analysis of ~300 cases); the Betty & Barney Hill case of 1961; claimants' genuine subjective conviction and, in several studies, ordinary psychopathology profiles; occasional shared "missing time" reported by companions. | No verified physical, photographic, video, biological, medical, radar or material evidence has ever been produced. No predictive content has ever been confirmed (the Hill "star map" is not a deterministic, falsifiable prediction). Reported content tracks popular fiction and culture and varies by culture, and claims peaked in the mid-1970s and declined as the cultural meme thinned — the signature of top-down expectation, not a physical event. Sleep paralysis — 8–50% lifetime prevalence, ~5% recurrent — contains the canonical intruder / chest-pressure / vestibular-motor ("levitation", out-of-body) triad that maps element-for-element onto abduction reports. Hypnosis-based "memory recovery" (Hopkins, Jacobs) raises confidence and adds detail without improving accuracy; the false-memory literature shows memories are constructible by suggestion. The Lancet criticised Mack's hypnotic-regression work as "constructing false memories"; Harvard reviewed his position in 1994. | A falsifiable protocol would be: (i) blinded polysomnography of high-rate claimants over a large sample of reported events — no event may occur outside a hypnagogic/hypnopompic state; (ii) any claimed implant must be characterised and shown to have non-terrestrial isotopic composition; (iii) two strangers must independently corroborate the same event with matching, verifiable detail against timestamped independent records; (iv) any "star map" must predict positions to astrometric precision. None of these has ever been passed. | **N/E** (not literal extraterrestrial abduction) | **>95%** that reported experiences are not literal abductions; **>99%** that no abduction has been physically corroborated |

---

## 2. Claim (a) — Flat Earth

### 2.1 Strongest form (steelman)
The Earth's habitable surface is a **stationary plane** — most commonly a disc centred on the geographic North Pole, bounded southward by a wall of ice (Antarctica), with the Sun and Moon moving as comparatively small, nearby bodies (~3,000 miles above the plane in Rowbotham's original formulation; 32 miles in diameter in the modern Flat Earth Society version), the stars attached to a nearby inner surface of a "dome", and the apparent curvature of the Earth, all satellite imagery and all spaceflight evidence explained by a deliberate, compartmentalised institutional conspiracy.

### 2.2 Evidence for
- Bedford Level (Old Bedford River): Rowbotham's 1838 experiment over ~6 mi of the Old Bedford River, in which a boat with a 3 ft (0.9 m) flag remained continuously visible, was widely reported as showing no curvature. (Refutation: Alfred Russel Wallace repeated the experiment in 1870 after correcting for atmospheric refraction and obtained the spherical result. The magnitude of the effect sought: over 6 mi = 9.7 km the verticals converge by 0.087°, i.e. the "hidden" drop of a 3 ft flag is 0.043° ≈ 2.6 arcmin — a genuinely hard visual measurement, and one that standard refraction gradients over water can and do swamp. The correct conclusion is not that the experiment was dishonest but that its sensitivity was ~1 arcmin in an atmosphere whose refraction over water routinely varies by tens of arcmin. *Wikipedia, "Bedford Level experiment".*)
- To the unaided eye, large water surfaces and the horizon look flat, and the horizon is always near eye level.
- Genuine historical record noise that a motivated reader can mine.

### 2.3 Evidence against (quantitative)

> **Note on the "Measured" column.** Three rows in this table — horizon distance, horizon dip, and hull-down concealment — are *geometric predictions of the spherical model with no refraction correction*, not surveyed measurements. Standard atmospheric refraction (k ≈ 0.13–0.25) reduces them by roughly 40–50%: the 20 km concealment falls from 17.5 m to about 14.5–11.8 m, and the 30 m dip from 0.176° to about 0.164°–0.152°. Both the geometric and the refraction-corrected values contradict the flat-plane prediction of exactly zero by many times their uncertainty, so the conclusion is unaffected; but the figures should be read as bounds, and the honest statement is "17.5 m geometric, 11.8–14.5 m with standard refraction." The gravity-magnitude row is likewise labelled as the WGS-84 Somigliana prediction, which is what gravimetric surveys measure.
| Quantity | Flat-plane prediction | Measured | Source |
|---|---|---|---|
| Circumference from shadow angles | requires a different solar altitude for every pair of sites (see §2.3a, Test 4); Rowbotham's single value is ~3,000 mi (4,828 km) | 250,000 stadia (c. 240 BC) → 39,375–46,250 km depending on the stadion (157.5–185 m); central estimate ≈40,300 km; modern 40,075.017 km (equatorial), 40,007.863 km (polar); flattening 0.3% | Eratosthenes/Cleomedes; IUGG GRS 80 |
| Noon-shadow geometry between two latitudes | depends on an arbitrary "nearby Sun"; a single altitude cannot fit two site pairs simultaneously (required H differs by a factor of 1.8 for one pair) | two-site difference in noon solar elevation equals the latitude difference exactly; meridional arc Memphis–New Orleans 578.0 km over 5.1984° gives R = 6,371 km (+0.00%); Eratosthenes' own 5,000 stadia gives R = 6,267 km (−1.6%) to 7,361 km (+15.5%) depending on the stadion | recomputed (§2.3a Test 4; §9) |
| Noon solar elevation | 0° difference with distance | varies with latitude exactly as a sphere requires | — |
| Polaris | visible everywhere, low everywhere | declination +89.26° → never rises south of 0.74° S; circumpolar (never sets) north of 0.74° N | derived (§8) |
| Southern Cross (Crux) | visible everywhere | Acrux δ = −63.10° → never rises north of 26.9° N; Gacrux δ = −57.11° → 32.9° N; Mimosa (β Crucis) δ = −59.69° → 30.3° N | derived (§8) |
| Ship receding to horizon | shrinks but never disappears hull-first | at 20 km, 17.5 m of a 20 m superstructure is *geometrically hidden below the sightline*; at 30 km, 48.9 m | recomputed, R = 6,371 km |
| Horizon dip (observer at 30 m) | 0° | 0.176° (10.6 arcmin) | recomputed |
| Foucault precession | 0 (no rotation) → any model requiring rotation gives 15.04°/h at poles, 15.04°/h × sin(lat) | Panthéon (48.85° N): 11.3°/h, i.e. a 31.8 h "pendulum day"; Amundsen–Scott 33 m/25 kg pendulum: ~24 h | Foucault 1851; 28 kg bob, 67 m wire |
| Gravity magnitude | uniform direction and magnitude | g = 9.7803 m/s² (equator) → 9.8322 m/s² (pole), +0.53%, the WGS-84 Somigliana *prediction* for a = 6,378,137 m, f = 1/298.257223563 (b ≈ 6,356,752 m), which is what gravimetric surveys measure; the row therefore checks a prediction against survey data, not a formula against itself | recomputed |
| Direction of local gravity | parallel vectors | verticals converge toward the centre at **1 arcmin per nautical mile** (1852 m/R = 59.96 arcsec ≈ 1′; a minute of *latitude* on the WGS-84 ellipsoid is 1,842.9–1,861.6 m, so the identity is approximate, not exact) — the very reason the nautical mile is defined as one minute of arc | recomputed |
| South-polar day length | ~12 h everywhere | at the South Pole the Sun is continuously above the horizon ≈20 Sep – 20/23 Mar (about 6 months), max elevation ~23.5° at the December solstice, and rises/sets only once per year, on the equinoxes; South Pole altitude 2,835 m | Midnight sun / South Pole |
| Southern flight distances | azimuthal-equidistant disc | Sydney–Santiago 11,340 km (sphere) vs 25,679 km (disc, 2.26×); Johannesburg–Perth 8,310 vs 18,350 km (2.21×); Cape Town–Sydney 10,989 vs 25,239 km (2.30×); Buenos Aires–Auckland 10,313 vs 25,025 km (2.43×) | recomputed |
| Perth–London flight | — | computed great circle 14,508 km vs published QF9 14,498 km in 17 h (agreement to 0.07%) | Qantas/QF9, 25 Mar 2018 |

Two additional decisive tests worth stating explicitly:

- **Rotation.** A ring-laser gyroscope is the instrument of choice. The *Behind the Curve* (2018) campaign by self-described GlobeBusters used exactly this instrument to test non-rotation and **detected 15°/hour** — the sidereal rate — which the group then explained as the device picking up the rotation of the "firmament." This is the general shape of the flat-Earth position: every test that fails is re-described rather than the model abandoned.
- **Solar angular size and the eclipse shadow.** The Sun's measured angular diameter is ~0.53° and does not shrink toward sunset; at sunset the *lower* limb is occluded first. On a flat plane with a receding local Sun the disc would shrink to a point. Independently, the length of Earth's umbral shadow is ~1.38 × 10⁶ km (§8), far beyond the lunar distance of 384,400 km (semi-major axis; the LLR mean centre-to-centre distance is 385,000.6 km), so the umbra is always larger than the Moon — which is why the Earth's shadow on the Moon during a lunar eclipse is always **circular**, never an ellipse, at any eclipse geometry. Only a sphere satisfies that for all geometries.

### 2.3a Three further decisive tests, computed from the flat model's own geometry

These three tests were computed in a second pass (`derivation2.py`, §9). Each is **internal to the flat-Earther's own model**: they take the azimuthal-equidistant disc map that flat-Earthers themselves use (the only map consistent with their own southern-flight-distance claims) and the solar altitude that flat-Earth sources quote, and show that the model's own predictions fail.

**Test 1 — the 24-hour Antarctic sun.** On the disc, the South Pole sits 180° of arc from the North Pole, i.e. r = 20,015 km from the pole, while the Sun's subsolar point migrates only between the tropics — polar distances 66.56°–113.44°, i.e. r = 7,401–12,614 km. The Sun's horizontal distance from the South Pole is therefore always 7,400–12,600 km, and because on a plane the Sun stays at fixed altitude above the plane and never descends, **it can never set there at all**. With the commonly quoted solar altitude of ~3,000 mi (4,828 km), the predicted solar elevation at the South Pole is **20.9°–33.1°, on every day of the year**. The result is robust to the solar altitude: across 3,000 → 30,000 km the prediction stays within 13°–76° elevation, up 365 days a year.

*Observation:* the Sun is above the South-Pole horizon for about six months (≈20 September – 20/23 March; the *Midnight sun* article gives the window as 20 September – 23 March and splits the year into 179 days of sun and 186 days of darkness) and absent for the other six, with a single sunrise and sunset per year (at the equinoxes) and a maximum elevation of 23.44° at the December solstice. **The failure is therefore categorical rather than merely a matter of degree: the disc model predicts the South-Pole Sun never sets at all, so it does not merely get the length of the season wrong by ~186 days — it predicts daylight where observation shows six months of night.** (The sociological datum in §2.4 — Will Duffy's December 2024 "Final Experiment", in which Antarctic participants conceded the midnight sun — is the field version of this same computation.)

**Test 2 — the geometry of sunset on a plane.** On a planar surface with the Sun at fixed altitude H, a sightline from an observer's eye (itself above the plane) to the Sun can never intersect the plane, so the Sun cannot set for anyone. The flat model is therefore obliged to invoke a "perspective" sunset in which the Sun recedes and shrinks. That is quantitatively excluded, and the exclusion is *independent of the Sun's physical size*, because

  θ(sunset)/θ(noon) = H / √(H² + X²).

For H = 4,828 km and X = 20,015 km (the disc rim) the ratio is **0.234** — the setting Sun would have to be **4.26× smaller** than the noon Sun (8.6 vs 32 arcmin). Measured, the Sun's angular diameter is 31.45–32.52 arcmin (computed from r = 695,700 km and perihelion–aphelion distances of 147,098,300–152,097,400 km): a total annual range of **±1.7%**, driven entirely by orbital eccentricity and correlated with date rather than time of day. The solar disc shows no measurable change between local noon and sunset; its variations are annual (and, at the sub-percent level over longer timescales, related to the solar cycle), not diurnal. **The demanded change is a factor of ~4; the permitted change is ~2%.** Conversely, holding the angular diameter within 1% at all distances out to the rim would require H ≥ 141,176 km (~22 Earth radii), at which height the noon Sun would be only 1.25 arcmin across — **25× too small**, and ~30× the altitude flat-Earth sources themselves quote. (The model's own Sun, 32 mi in diameter at 3,000 mi altitude, already predicts 36.67 arcmin at noon — 15% above measurement.)

A secondary, qualitative but decisive point: at sunset the **lower** limb is occluded first. A convex horizon does that; a receding object on a plane would not, and a plane edge would bisect the disc.

**Test 3 — the orbital mechanics that make GPS work (Kepler's third law).** With μ = GM = 398,600.4418 km³ s⁻², a circular orbit at the GPS radius of 26,560–26,600 km has a period of 11.966–11.993 h. The observed value — "each SV makes two complete orbits each sidereal day" — is 11.9672 h. **Agreement 0.01%.** Running the same law backwards from an assumed period of exactly one sidereal day gives a = 42,164.2 km, i.e. an altitude of 35,793 km, against the published geostationary altitude of ~35,786 km: **agreement 0.02%.** Both are closed Keplerian solutions about a single spherical central mass; GPS ground tracks repeat each sidereal day, and the observed rise/set windows from every site match a sphere's visibility geometry. A planar surface admits no solution of this kind, and GNSS positions are solved in a geocentric frame (GRS 80 / WGS 84) that fits ground surveys to ~2 cm.

**Test 4 — Eratosthenes repeated with modern coordinates (§9, block D).** This closes a gap in the first draft, where the claim that two-site shadow geometry "reproduces a sphere of R = 6,371 km to <0.3%" was asserted without a computation. On a sphere with the Sun effectively at infinity the noon solar elevation is elev = 90° − |φ − δ|, so the *difference* in noon elevation between two sites equals the difference in their latitudes, on any date. Two US cities nearly on the same meridian give a clean case: Memphis (35.1495° N) and New Orleans (29.9511° N) differ in latitude by 5.1984°, and the great-circle distance between them is 578.0 km — which divided by 5.1984° in radians (0.090729) gives **R = 6,371 km (+0.00%)**. The residual is essentially zero because a same-meridian arc is the meridional arc by construction, so this is a check of spherical *self-consistency* rather than an independent measurement of R; but the *discriminatory* content is real, because on a flat plane the noon-elevation difference depends on the Sun's altitude H through elev = atan(H/x), and a single H cannot fit even one pair of sites: fitting the Memphis–New Orleans 5.1984° difference requires H = 14,311 km from one site and H = 7,958 km from the other — inconsistent by a factor of 1.8. Eratosthenes' own numbers, recomputed, give R = 6,267 km (−1.6%) for a 157.5 m stadion and 7,361 km (+15.5%) for a 185 m stadion, i.e. the historic result is good to −1.6%/+15.5% once the stadion is pinned down — itself a quantitative refutation of any "no one knew the Earth was round or how big" claim.

**Caveats on Tests 1–3, stated explicitly.** (i) Test 3 is conditional on inverse-square gravitation about a central mass; that law is independently established by, among other things, these very orbital solutions, so the test is a consistency check rather than an independent proof — a flat-Earther is free to posit different physics, but must then abandon Newtonian orbital mechanics wholesale. (ii) Test 2's headline ratio θ(sunset)/θ(noon) = H/√(H²+X²) is independent of the Sun's physical size and of the model's solar altitude, which is why it is the strongest of the three; the specific "36.67 arcmin at noon, 15% too big" figure rests on a *hybrid* of Rowbotham's altitude and the modern Flat Earth Society's diameter, which no single cited source pairs. (iii) Test 1's failure is binary — the disc model predicts the South-Pole Sun never sets at all — so quoting "~186 days of error" is a rhetorical convenience that understates rather than overstates the discrepancy.

### 2.4 The 2018–2024 field tests
Independent Investigations Group (Center for Inquiry), Salton Sea, 10 June 2018: boat-based and shore-based targets were shown to disappear over distance, demonstrating curvature. The flat-Earth participants present rejected the result after the fact. In December 2024, Will Duffy's "Final Experiment" took flat-Earthers to Union Glacier Camp in Antarctica to witness 24-hour daylight; the participants conceded they had seen the midnight sun, though not all converted on the spot. This is a useful sociological datum: the *observation* was conceded; the *inference* was refused, because the model is held axiomatically rather than empirically.

### 2.5 Verdict and confidence
**False.** Confidence **>99.9%**. The evidence *actively disconfirms* the claim: at least **thirteen** independent classes of measurement — shadow geometry, star fields, hull-down concealment, pendulum precession, gravity magnitude and direction, geodetic/GNSS solutions, scheduled southern-hemisphere flight distances and times, the South-Pole daylight cycle, sunset geometry (angular-diameter constancy and lower-limb-first occlusion), satellite orbital mechanics (Kepler's third law, §2.3a), direct geometric measurements of Earth's orbital motion (§14.1, §14.2), and — added in the sixth pass — **rotation measured by relativistic rather than dynamical or gravitational means** (§16.1: the 1926 Michelson–Gale ring interferometer, the 207.4 ns around-the-world Sagnac delay, and the 274.6 ns GNSS rotation correction) — each contradict a flat plane by margins far larger than their error bars, and the flat-disc model's own quantitative predictions (e.g., 2.2–2.4× southern route lengths, ~186 excess days of daylight at the South Pole, a setting Sun 4.26× too small, an annual stellar parallax of ~10⁹–10¹⁰ arcsec against the measured 0.768″) are falsified by routinely published airline schedules and by measurements anyone with a sextant or a camera can repeat.

The fifth- and sixth-pass additions are each worth a sentence of their own, because each is the first test in this section with a different logical form. Everything above refutes the flat model by *inconsistency* — the model's own numbers fail. §14.1 and §14.2 are *positive* measurements: a stationary plane predicts annual stellar parallax of exactly zero and annual stellar aberration of exactly zero, and both are measured to be non-zero (0.77″ and ~20″), by ordinary observatories, on stars nobody alleges were faked. §16.1 is a *positive* measurement of Earth's rotation by a method that is neither dynamical nor gravitational: a stationary plane predicts a Sagnac delay of exactly 0 ns and a ring-laser beat frequency of exactly 0 Hz, and measurements of both exist. A conspiracy that explains away the measurements must now also explain the parallax, and separately the Sagnac delay.

### 2.6 What would change my mind
A single verified observation of a receding ship disappearing hull-down at a range consistent with flat geometry but inconsistent with R = 6,371 km; or a successful astrometric demonstration that Polaris and the Southern Cross are simultaneously circumpolar from the same site; or a southern-hemisphere flight that actually takes 2.2× its published great-circle time. None exists.

---

## 3. Claim (b) — The Moon landing was faked

### 3.1 Strongest form (steelman)
NASA, under Cold War political pressure, did not have the capability to land humans on the Moon and return them, and staged the six crewed landings (1969–1972) on Earth; the 381 kg of samples were either fabricated or were (somehow) civilian meteorites; the telemetry, television and radio downlinks were synthesised; the hardware left on the lunar surface was delivered robotically or never; and the Soviet Union's apparent acceptance of the landings was itself part of the arrangement.

### 3.2 Evidence for
- The complete absence of publicly available *independent* original footage in 1969 (NASA controlled the pool, the conversions and the first releases), so the first-order evidence was single-source.
- Genuine photographic oddities: Réseau-plate crosshairs apparently behind objects, the "two C's" on a rock, "identical backgrounds," the apparently gyrating flag, the apparent absence of stars. These are all now explained, but each is individually striking to a lay viewer.
- Real archival gaps: the original slow-scan Apollo 11 tapes were not preserved (a mundane, well-documented tape-reuse decision, but a real gap).
- Radiation-belt anxiety: the belts are genuinely dangerous to satellites, so the qualm is a reasonable prior.

### 3.3 Evidence against (quantitative)

| Instrument / result | Number | Source |
|---|---|---|
| Lunar laser retroreflectors placed by Apollo 11 (21 Jul 1969), 14, 15 | first successful range **1 Aug 1969** by the 3.1 m Lick Observatory telescope; round-trip ~2.5 s; pulse of 3 × 10¹⁷ photons → **about 1–5 received back**; mean Earth–Moon distance 385,000.6 km; range precision **millimetre**, **1 cm** weighted-rms residual; lunar recession **3.8 cm/yr** | Lunar Laser Ranging (LLR) |
| Retroreflectors also present from Lunokhod 1, Lunokhod 2 (Soviet) and Chandrayaan-3 (India) | three independent nations' hardware confirmed operable on the Moon | LLR |
| Apollo returned samples | **381 kg** from six missions (the brief's ground-truth figure of ~382 kg is the same total rounded), **2,200 samples** catalogued into >110,000 documented specimens; Apollo 11: 21.55 kg; Apollo 15: 77 kg | NASA/Lunar Sample Laboratory Facility |
| Sample ages | mare basalts from 3.16 Ga, highland rocks to 4.44 Ga; **oldest Earth rocks 3.8–4.28 Ga** | radiometric dating |
| Unique mineralogy | armalcolite, tranquillityite, pyroxferroite first discovered in Apollo samples (all later found on Earth); mare basalts 18–21% FeO, 1–13% TiO₂, negative Eu anomaly, KREEP zone | lunar petrology |
| Independent extraterrestrial corroboration | **>370 lunar meteorites**, >1,090 kg, found in Antarctica, N. Africa and Oman; Luna 16/20/24 returned 301 g total — **Luna 16 alone returned 101 g (3.56 oz) from Mare Fecunditatis** after a drill reached 35 cm; **Chang'e 5** returned ~1,731 g in 2020 | *Wikipedia, "Luna 16"*, now verified verbatim (§10.0, correction 1) |
| Independent sample comparison | "Analysis of the dark basalt material indicated a close resemblance to soil recovered by the American Apollo 12 mission" | *Wikipedia, "Luna 16"* — now verified verbatim |
| Soviet/US sample exchange | **10 June 1971**, Soviet Academy of Sciences exchanged Luna 16 material for Apollo 11 and 12 samples; Luna 16 material exchanged for Apollo 11 and 12 samples in Moscow; a further 0.4825 g Luna 16 sample was sent to Britain | *Wikipedia, "Luna 16"* |
| Economic corroboration | three Luna 16 fragments **totalling 0.2 g (200 mg)** sold for **US$442,500 in 1993** and resold for **US$855,000 on 29 November 2018** at Sotheby's | *Wikipedia, "Luna 16"* |
| Independent tracking | Soviet deep-space tracking facilities introduced in **1962** at IP-15 Ussuriisk and IP-16 Evpatoria, with Saturn communications stations at IP-3, IP-4 and IP-14 quoted at a 100 million km range; the Space Transmissions Corps tracked the Apollo missions; the Great Soviet Encyclopedia (3rd ed., 1970–79) reported the landings as factual | Soviet programme records |
| ALSEP | five full stations (Apollo 12/14/15/16/17) plus the Apollo 11 EASEP, radioisotope-powered, operated autonomously until **30 September 1977**; all five transmitters were then received by the **Soviet RATAN-600** radio telescope between **18 October and 28 November 1977**; the Apollo 12 LM ascent stage was fired into the Moon as a **~1 ton of TNT** calibration event | ALSEP |
| Lunar seismometers | four stations (Apollo 12/14/15/16) "functioned perfectly until they were switched off in 1977" — **7.8 years** of continuous unattended operation from Apollo 12's landing on 19 Nov 1969; **28 shallow moonquakes** logged 1972–1977 (≈5.6/yr by the network), shallow events to **mB = 5.5**, deep events ~700 km down and probably tidal; Apollo 11's EASEP seismometer "was sensitive enough to detect Neil Armstrong's movements during sleep" | *Wikipedia, "Moonquake"*, "ALSEP" |
| Heat Flow Experiment | a self-consistent measurement on another world: thermal gradient **1.5–2.0 K/m** at Apollo 15 and 17, heat flow **~17 mW/m²**, with 70% of the top-layer transfer radiative at noon; regolith density 1.1–1.2 → 1.75–2.1 g/cc below the top few cm. Derived here (**§13.1**): Fourier's law gives a regolith conductivity of **8.5–11.3 mW/(m·K)**, central 9.7, and a global lunar heat output of **6.4 × 10¹¹ W (640 GW)** | *Wikipedia, "Heat Flow Experiment"* |
| Seismic network | four stations (Apollo 12/14/15/16) "functioned perfectly until they were switched off in 1977" — **7.87 years (2,872 days)** of continuous unattended coverage from Apollo 12's landing on 19 Nov 1969, or **5.8 years** counting the full four-station network era, 1972–77; **28 shallow moonquakes** logged 1972–77 (**4.7–5.6/yr**, depending on whether the window is five elapsed years or six calendar years — the source says only "between 1972 and 1977"), shallow events to **mB = 5.5**, deep events ~700 km down and probably tidal; Apollo 11's EASEP seismometer "was sensitive enough to detect Neil Armstrong's movements during sleep" | *Wikipedia, "Moonquake"*, "ALSEP" |
| Orbital imagery | LRO NAC at **0.5 m/pixel** (50 km altitude) resolves the LM descent stages, the Lunar Rovers, ALSEP hardware and astronaut boot tracks; 2012 images showed **five of the six flags** still standing (Apollo 11's having been blown over by the ascent-stage plume) | LRO/LROC |
| **Coordinate-dependence of the return (sixth pass, §16.2)** | Lunokhod 1's array was **undetectable by laser from western stations for 39 years** (no return since 1971) despite its published approximate location; on **17 March 2010** Albert Abdrakhimov found it in LRO image **M114185541RC** (Line 21977, Sample 3189); APOLLO (UC San Diego) then ranged it successfully on **22 April 2010** and the days following, reporting **"We got about 2,000 photons from Lunokhod 1 on our first try."**; LLR ranges alone **trilaterated its position to 1 m**, and to **~1 cm** by November 2010; the result was replicated by the **Côte d'Azur Observatory in May 2013** | *Wikipedia, "Lunokhod 1", "Lunar Laser ranging experiments"* |
| Array relative sizes | the **Apollo 15** array is **three times** the size of Apollo 11/14's and drew **three-quarters** of the measurements taken in the experiment's first 25 years; **Lunokhod 2's array "continues to return signals to Earth"**; the Lunokhod arrays are **44 × 19 cm** against Apollo 11's **46 × 46 cm**; Chandrayaan-3 left a **single 5.11 cm** reflector in August 2023 | *Wikipedia, "Lunar Laser ranging experiments", "List of retroreflectors on the Moon"* |
| Precision | "As of 2009, the distance to the Moon can be measured with **millimeter precision**", described as "equivalent in accuracy to determining the distance between Los Angeles and New York to within the width of a human hair" (recomputed here as ~5 × 10¹⁰–8 × 10¹⁰ : 1 for a 50–70 µm hair, and the LA–NY great circle) | *Wikipedia, "Lunar Laser ranging experiments"* |
| Radiation dosimetry | Apollo transited the **inner** belt in minutes and the outer belt in ~1.5 h; aluminium hull shielding; **average dose <1 rem (10 mSv)** ≈ sea-level ambient for **three years**, comparable to the annual occupational limit for nuclear workers; James Van Allen himself rebutted the objection | Van Allen belt dosimetry |
| Independent astrometric check | the Apollo 16 Far Ultraviolet Camera took photographs of Earth and of UV-bright stars from the LM's shadow; the **positions of those stars match observations from orbiting ultraviolet telescopes for that time and place** | Apollo 16 FUV |
| Environmental consistency | lunar surface temperature range **−171 °C to +120 °C**; exosphere total mass <10 tonnes, surface pressure ~3 × 10⁻¹⁵ atm (0.3 nPa) — near-vacuum; all landings shortly after local sunrise | Moon |

### 3.4 Why each photographic objection fails
- **Crosshairs behind objects**: the crosshairs are ~0.1 mm thick and the "obscuring" appears only in copies/scans where overexposure makes bright emulsion bleed over the thin black reticle; there are many frames where a crosshair is washed out on a white stripe but intact on a red one. Nothing was pasted.
- **No stars**: the astronauts were describing naked-eye lunar-daytime viewing; the Sun in the Earth–Moon system is at least as bright as noon sunlight on Earth, so cameras were set for daylight exposure and starlight fell below the recording threshold. The Apollo 16 FUV camera *did* record stars — and their positions are independently correct.
- **Flag "flutter":** the flag was fastened to a Γ-shaped rod and only moved while being handled; without air drag, the free corner swings like a damped pendulum and stops. The ripple pattern is creasing from storage. The Apollo 15 hammer-and-feather drop (Scott) is the in-vacuum control experiment.
- **"Poor shadows"/artificial lights:** multiple light sources (Sun, Earthshine, Moonshine, suit/LM reflection) scatter off lunar dust; vanishing-point perspective makes converging shadows; and without atmosphere there is no aerial perspective, so distant hills look deceptively close.
- **Thermal fogging of film:** in a vacuum only radiative transfer operates; film was stowed in metal containers and travelled stowed in the modularised equipment stowage assembly (MESA), not in sunlight; passive coatings controlled cabin and equipment temperature.

### 3.5 Verdict and confidence
**False.** Confidence **>99.9%** that the six crewed landings occurred as reported. This is one of the strongest evidentiary positions in all of applied science: the physical claim is testable **right now** by anyone with a large telescope and a pulsed laser, and by any laboratory with a mass spectrometer and radiometric dating equipment, and it has been so tested by both US and non-US parties for more than five decades.

### 3.6 What would change my mind
A non-US or amateur laser-ranging station failing to obtain a pulse from the documented Apollo array coordinates while succeeding from the Lunokhod coordinates; a dated Apollo sample returning a terrestrial age; a non-US orbital survey resolving no hardware at the documented site coordinates; or an independent geochronology consensus that all Apollo samples and all lunar meteorites share a common terrestrial provenance.

---

## 4. Claim (c) — Area 51 and Roswell

This claim must be split, because its two halves have radically different evidentiary status.

### 4.1 Established and documented

**Area 51 is a real, classified USAF facility.** It sits within the Nevada Test and Training Range, **83 mi (134 km) north-northwest of Las Vegas**, around Groom Lake (elevation **4,409 ft / 1,344 m**). The original rectangular base was 6 × 10 mi (10 × 16 km), inside a restricted airspace ("the Groom box") of 23 × 25 mi (37 × 40 km). It is officially "Homey Airport" (ICAO **KXTA**, FAA LID **XTA**) and is administered as a remote detachment of Edwards AFB; the surrounding restricted airspace is R-4808N. The CIA/USAF acquired it in **1955** for Project Aquatone, the Lockheed **U-2** programme (Kelly Johnson's "Paradise Ranch"); the first U-2 arrived on 24 July 1955. It was reconstructed from **September 1960** for the **A-12 OXCART**, including a 10,000 ft (3,000 m) runway (14/32) and a fuel farm holding **1,320,000 US gal (5,000,000 L)** of JP-7; it hosted the D-21 Tagboard drone programme from 1964; and from the late 1960s for decades it was used to test and evaluate captured Soviet fighter aircraft. The base shares a border with Yucca Flat, site of 739 of the 928 US nuclear tests at the Nevada Test Site. The **CIA publicly acknowledged the facility's existence on 25 June 2013**, in response to a FOIA request filed in 2005, and has declassified documents describing its history and purpose.

The correct inference from this documentation is *counter*-intuitive but important: **Area 51's documented secrecy is a secrecy about aerospace engineering, not about extraterrestrials.** The base spent decades being officially denied while flying the U-2, the A-12 and (later) the F-117. This real history is the best available model of how a classified programme actually behaves — and it contains no alien artefacts in any declassified document.

**Project Mogul was a real, classified programme.** A top-secret USAAF project run **from 1947 until early 1949**, it flew long trains of polyethylene balloons carrying disc microphones and radio transmitters to exploit the atmospheric sound channel theorised by Maurice Ewing, with the aim of detecting Soviet atomic-bomb tests at long range. It was conceived by Ewing, supervised by James Peoples with Albert P. Crary, and was the forerunner of the Skyhook balloon programme. Its constant-altitude control and polyethylene balloon construction were genuine engineering innovations.

**The Roswell debris was explained by documented reports.** In response to a 1993 inquiry from New Mexico congressman Steven Schiff and a GAO probe, the Air Force produced an initial 1994 report and then *The Roswell Report: Fact versus Fiction in the New Mexico Desert* (1995), which documented that the debris recovered from the Brazel ranch near Corona, New Mexico, came from a specific Mogul balloon train — **NYU Flight 4, launched from Alamogordo Army Air Field on 4 June 1947** — which lost contact within **17 mi (27 km)** of the ranch. The USAF itself later described the 1947 "weather balloon" statement as "an attempt to deflect attention from the top secret Mogul project."

### 4.2 Not established, and partly actively disconfirmed

| Offered evidence | Status |
|---|---|
| 1947 debris = alien craft | Debris was several acres of tinfoil, rubber, tape and thin wooden beams; the 9 July 1947 *Roswell Daily Record* noted **no engine or metal parts** found. An FBI tetype of 8 July 1947, sourced to Eighth Air Force headquarters, described a **hexagonal object suspended by cable from a balloon about 20 ft (6.1 m) in diameter**. The "hieroglyphics" on a beam match the adhesive tape Mogul bought from a New York toy manufacturer. |
| Alien bodies / autopsies | **Not mentioned in any 1947 account and not mentioned by the original debris eyewitnesses.** The body motif entered the legend from the **1948 Aztec, New Mexico hoax** (perpetrated on *Variety* columnist Frank Scully) and from "Hangar 18," a fictional location that the Air Force states never existed. the "star witness" Glenn Dennis, interviewed by Stanton Friedman in 1989 **supplied fabricated names for his nurse source** and could not produce a verifiable one. The 1997 USAF report *The Roswell Report: Case Closed* (24 June 1997) instead matched the body-bag stories to **1950s Air Force Operation High Dive** anthropometric test-dummy recoveries: dummies carried on stretchers, in casket-shaped crates and in insulation bags resembling body bags, recovered by a **Dodge M37** vehicle, and described by witnesses as bald, "dummies," "plastic dolls" wearing flight suits. The USAF also attributed parts of the legend to the 1980s disinformation campaign by Bill Moore (who publicly admitted feeding fabricated evidence to UFO researchers) and Richard Doty. |
| "Alien Autopsy" footage | Ray Santilli **admitted in 2006** that the footage was a fabrication, filmed on a set built in a London living room. |
| Majestic-12 documents | Admitted by Moore to have been typed and stamped as a facsimile; the documents exist only as photographs of copies; dates are in a format used in Moore's personal notes but not in 1947 US government documents; the Truman signature is identical to that on an unrelated 1 October 1947 letter; Carl Sagan noted the total absence of provenance. |
| Chain of custody to a physical specimen | **None exists.** No Roswell artefact has ever been submitted to blinded laboratory characterisation. Pflock's audit of the 300+ witnesses reportedly interviewed for *UFO Crash at Roswell* (1991) found only **23** who could reasonably be thought to have seen physical evidence, and only **7** of whom suggested otherworldly origin. |
| Institutional corroboration | The **GAO probe found no Roswell documents at the CIA** and no information about the alleged Majestic-12 group — a genuine documentary absence that runs against the claim of an institutional retrieval programme. |
| Base rate (sixth pass, §16.3) | Verified verbatim: **"By 1947, the United States had launched thousands of top-secret Project Mogul balloons."** Thousands of long balloon trains were therefore aloft over the south-western United States in 1947, and debris recoveries were a routine occurrence, not a singular event. Exactly one of them became the Roswell legend. |
| Trajectory (sixth pass, §16.3) | From verified gazetteer coordinates (Wikipedia API, `prop=coordinates`), Alamogordo (32.856111° N, 105.974444° W) to Corona (34.247778° N, 105.596944° W) is **158.7 km** on an initial bearing of **12.6° E of N**. A constant-altitude balloon cannot aim — its track is the passive integral of the wind — so the Mogul hypothesis implies a specific, checkable mean drift: if Flight 4 was aloft *T* hours, the mean wind over southern New Mexico must have been **(158.7/*T*) km/h** from the SW-SSW (44.1 m/s if 1 h; 7.3 m/s if 6 h; 1.8 m/s if 24 h; 0.3 m/s if a week). This is the check pass 4 left open; it remains open because the June 1947 upper-air wind field was not retrieved here (§16.3). |
| Debris-field geometry (sixth pass, §16.3) | "Several acres" = 3–5 acres = **12,141–20,234 m²**, i.e. a field **110–142 m** on a side. A compact impact site of a ~10 m craft would concentrate nearly all recoverable mass at one location with fragments thrown O(10 m); a field 100–140 m across with "no engine or metal parts" is what a long balloon train shredding and dropping material over its length produces. *Caveat: the source gives the area only, not the shape or length:width ratio, so this is an argument of direction, not a precision measurement.* |
| The telex "disc" is a balloon, scaled (sixth pass, §16.3) | The 8 July 1947 FBI telex's object — **"hexagonal in shape … suspended from a balloon by cable, which balloon was approximately twenty feet (6.1 m) in diameter"** — is an envelope of volume 118.8 m³. Under the standard atmosphere, a 6.1 m superpressure envelope carries a **gross lift of 47.8 kg at 9 km, 31.8 kg at 12 km and 19.8 kg at 15 km** (net payload ≈ 40 / 27 / 17 kg after the helium's own mass). A Mogul train is a payload of that order; a crewed interstellar vehicle carrying bodies is not. *(altitudes assumed; ISA only)* |

### 4.3 What evidence would be required to establish the extraordinary claim
1. A physical artefact with an authenticated 1947 provenance that (a) survives blinded characterisation by several independent laboratories, (b) has an isotopic or structural signature not attributable to any known terrestrial process, and (c) cannot be explained by balloon, aircraft or ordnance material.
2. A non-human biological specimen with the same properties — recoverable, independently dated, and with a genome/phylogenetic position that is not terrestrial.
3. Documented internal US government records of a retrieval programme, declassified or leaked, which are internally consistent and survive provenance testing (i.e. which do not, like the Majestic-12 papers, turn out to have been manufactured by a writer).
4. Predictive, non-retrodictive content: e.g., a witness who, in 1947 or 1978, stated a fact about the craft's materials that was subsequently independently confirmed and could not have been guessed.

**Status: none of (1)–(4) exists.**

### 4.4 Verdict, confidence, and the absence-vs-disconfirmation flag
- **(c1) Area 51 is real:** **True**, confidence **>99.9%** — the highest confidence available in this report, and the only claim here whose truth is established by the responsible institution's own declassification rather than by inference. (The document's own convention forbids stating 100%.)
- **(c2) Roswell debris was extraterrestrial:** **Not established**, assessed probability **<2%**. The competing, mundane explanation (Mogul Flight 4) is positively supported by launch records, timing, distance, material description, the FBI telex, and the USAF's own documented account.
- **(c2′) "Bodies were recovered":** this sub-claim is **actively disconfirmed**, not merely unsupported: the specific witnesses and artefacts offered have been tested and found fabricated, hoaxed or misattributed to a documented, ordinary test programme.

**Honest epistemic caveat.** The secrecy of the US government around its black programmes makes absolute proof harder here than elsewhere in this report. A claim of the form "there is classified evidence we cannot see" is **unfalsifiable in principle**, and the honest position is that we cannot exclude it; what we *can* say is that **no evidence offered in the 79 years since 1947 has survived scrutiny**, and that every particular artefact produced has turned out to be a hoax, a fabrication, a fictional source, or a misattributed object. That is not proof of the negative; it is a very strong signal about where the burden of proof lies.

### 4.5 What would change my mind
A submitted, analysable Roswell artefact with non-terrestrial isotopic signatures and an authenticated 1947 chain of custody; a non-human biological specimen; or declassified internal records of a retrieval programme that survive forensic provenance testing. Absent that, additional witness testimony — no matter how numerous or how senior the witness — cannot carry the claim, because the record shows testimony in this case to be unreliable in specific, identified ways.

---

## 5. Claim (d) — Alien abduction

### 5.1 Strongest form (steelman)
A subset of the human population is periodically taken, against their will and physically, by non-human intelligences, usually while alone or in vehicles at night, and subjected to medical examinations emphasising the reproductive system, after which some erased memories are partially recoverable — sometimes under hypnosis — and sometimes corroborated by physical traces such as scars, bruising or nosebleeds. The remarkable cross-cultural and cross-decade consistency of the accounts is best explained by their being veridical reports of real events, and the absence of photographs is explained by the abductors' ability to control perception, memory and instruments.

### 5.2 Evidence for
- **Narrative consistency.** Folklorist Thomas E. Bullard's comparative analysis of ~300 alleged abductees found a broadly consistent sequence (capture, examination, procedures, return), and the pattern holds across independent cases, which is not what one expects from wholly independent confabulations without a shared source.
- **The prototypical case.** Betty and Barney Hill (1961) is the first widely publicised abduction claim, and it introduced the "grey" beings in an explicitly extraterrestrial framing.
- **Claimant normality in at least some studies.** Richard McNally (Harvard Medical School) examined 10 abductees and concluded "none of them was suffering from any sort of psychiatric illness"; some studies find abduction experients do not differ from the general population in psychopathology prevalence. This is an honest point in the claimants' favour: the reports cannot be dismissed as straightforward psychosis.
- **Reported physical sequelae**, in some cases including scars and nosebleeds.

### 5.3 Evidence against, and the mechanisms that explain the phenomenon
1. **No verified evidence of any kind has ever been produced.** Not one photograph, film frame, video, radar track, biological sample, forensically confirmed implant, or physical trace with independently verified anomalous properties. There is no artefact.
2. **No predictive content has ever been confirmed.** The Hill "star map" is not a falsifiable prediction: given an origin star and an epoch, the pattern must be reproduced to astrometric precision, and no claimant has ever produced a map that does.
3. **The content tracks culture and fiction.** The entities described by abductees in the 1950s resemble the aliens of *Invaders from Mars* (1953); the content of narratives varies with the claimant's culture; claims surged in the mid-1970s and declined as the cultural meme thinned. Michael Shermer's point is decisive in kind: in the camera-phone age the burden of evidence on such claims has risen sharply, and the claimed frequency fell. Real physical events do not become less photographable when phones improve.
4. **Sleep paralysis.** Incidence: **8–50% of people experience it at some point**, ~**5%** recurrently; episodes typically 1–6 minutes. Its characteristic hallucination triad — the **intruder** (a sensed or seen presence), the **incubus** (chest pressure, suffocation, being held down), and **vestibular-motor disorientation** (floating, flying, out-of-body experience) — maps element-for-element onto the "held down by a presence on my chest / levitated / floated through a wall" components that recur across abduction narratives. Mechanistically, REM atonia persisting into waking while threat-activated vigilance and vestibular-motor systems generate a body position inconsistent with the room produces this class of experience without anything physical happening.
5. **Hypnosis and confabulation.** The core of the modern abduction literature (Hopkins, Jacobs, and Mack in his popular work) was built on hypnosis-based "memory recovery." Hypnosis raises confidence and generates additional detail **without improving accuracy**, and the experimental memory literature (Loftus and successors) shows that rich, specific, confident, emotionally held "memories" of non-events can be induced by suggestion alone. Niall Boyce, in *The Lancet*, described the process as "potentially both cementing and constructing false memories." Harvard reviewed Mack's position in 1994 as a direct consequence of his advocacy.
6. **Contested prevalence figures.** One early study counted 1,700 claimants; contested surveys claim 5–6% of the general population report having been abducted. Whatever the true number, it has not been tied to any instrumentally detectable event.

### 5.4 Decisive, falsifiable tests — and the results of having run them
| Test | Prediction if abductions are physical events | Result |
|---|---|---|
| Blinded polysomnography of high-rate claimants across many reported events | sleep is unremarkable; no REM/atonia signature; no correlated autonomic event at the reported time | The literature routine attributes these experiences to hypnagogic/hypnopompic states and sleep paralysis; no study has demonstrated an event outside such a state |
| Instrumentation (surveillance cameras, dosimeters, RF recorders) in bedrooms/vehicles | detectable events, radiation, RF, or motion consistent with the account | none recorded in 70 years, including the entire camera-phone era |
| Physical remnants | anomalous implants/biopsies/marks with documented anomalous properties | claimed implants have no demonstrated non-terrestrial composition; scars are not distinctive |
| Independent eyewitness / physical corroboration | two or more independent, mutually unacquainted witnesses matching verifiable detail | never demonstrated |
| Predictive content | a claimant states a fact about the craft/beings that is later independently confirmed | never demonstrated |
| **The instrumented-report base rate (sixth pass, §16.4)** | if anomalous craft traversed the atmosphere, a systematic 17-year, 12,618-case instrumented investigation should find physical traces | Project Blue Book (March 1952 – 17 Dec 1969, HQ Wright-Patterson AFB) collected **12,618** reports, classified **701** (computed **5.56%**) as "unexplained, even after stringent analysis" — and the USAF's own published conclusions are that "There was no evidence submitted to or discovered by the Air Force that sightings categorized as 'unidentified' represented technological developments or principles beyond the range of present-day scientific knowledge" and "There was no evidence indicating that sightings categorized as 'unidentified' were extraterrestrial vehicles" |

### 5.5 Verdict, confidence, and the absence-vs-disconfirmation flag
**Not established as a literal physical phenomenon.** Confidence **>95%** that reported experiences are not literal extraterrestrial abductions; **>99%** that no abduction has been physically corroborated.

This is the claim where the **absence of evidence is itself the finding**, and it must be flagged as such. The claim is a *positive physical* claim about the world: it postulates craft traversing the atmosphere, beings handling a body, and an examination session with instruments. **If that were happening, the physical world would be full of the debris of it** — radar tracks, motion, radiation, footage, DNA, radiometric artefacts, missed work, hospital admissions at matching times, and (now, in particular) phone photographs. The absence is not the ordinary absence of a poorly instrumented past; it is the absence that persists into the most densely instrumented era in human history, while the *reported* content simultaneously becomes more obviously a function of contemporary fiction. That combination is the signature of an endogenous, culturally templated experience, not a physical event. **On the strength of that premise, honestly:** it is an argument from silence. **That objection has now been met quantitatively — see §10.3, which computes the expected detection rate and the largest per-event recording probability consistent with the observed silence.** The result, and its limits, are these. With only the ~1,700 documented claimants, the silence is *not* surprising if each event had less than a ~1-in-500 chance of leaving any record (p ≲ 2 × 10⁻³), but is surprising to P ≈ 4 × 10⁻⁸ if p ≳ 10⁻². With the contested 5–6% survey figures, the silence requires every event to have had less than a 1-in-135-million chance of leaving a record — not a credible property of craft traversing the atmosphere. So the argument does not stand or fall on the survey figure: it stands on the claim that a physical abduction has at least a ~1-in-100 chance of leaving a verifiable trace, and that claim is a judgement, not a measurement. **This is the honest limit of the quantitative case, and it is stated rather than hidden.** What can be said quantitatively without relying on the contested figure at all is: (i) the sleep-paralysis base rate is known (8–50% lifetime, ~5% recurrent), so a large supply of the requisite phenomenology exists without any external cause; (ii) the reported incidence has *fallen* over the camera-phone era while detectability rose, which no physical-event hypothesis predicts; and (iii) the abduction accounts' content is dated to the fiction of their claimants' own childhoods. Those three are measurements or countably many observations; the "the world would be full of debris" premise is not. **A fourth, added in the sixth pass, is also a count:** over the 17 years of Project Blue Book, **12,618 reports were investigated instrumentally and 701 remained unexplained (5.56%) — and none of the 701 produced physical, photographic, radar or biological evidence** (§16.4). That is the quantitatively stated absence, at the one sample size large enough to be worth quoting. **Being explicit:** I cannot prove a negative; no experiment falsifies "aliens occasionally abducted someone in a way that left no trace." What the evidence does establish is that (i) the specific accounts offered do not correspond to the physical world and (ii) well-documented mechanisms — sleep paralysis, hypnosis-induced confabulation, expectational shaping, and the false-memory literature — fully account for their content and phenomenology.

### 5.6 What would change my mind
Any one of the following: a verified physical artefact or biological trace; a recording; a claimant making a confirmed, falsifiable prediction; or two mutually unacquainted claimants giving matching, independently verifiable accounts of the same event. Failing that, the scientifically productive work on this phenomenon is in sleep medicine and memory research, not in astrobiology.

---

## 6. Cross-cutting observations

**1. Structure of the four claims.** Flat Earth and the Moon landing hoax are *hard* falsifiable claims about the physical world, and they are decisively falsified by measurements anyone can repeat. Area 51/Roswell and abduction are *soft* claims about hidden or unobservable events, and the reason they persist is structural, not evidential: they are constructed so that the absence of evidence is re-read as evidence of the effectiveness of the cover-up. That re-reading is unfalsifiable and therefore not a scientific position.

**2. Absence vs. disconfirmation — the summary.**
| Claim | Absence of evidence | Active disconfirmation |
|---|---|---|
| Flat Earth | negligible | **dominant** — thirteen independent quantitative classes of measurement, including three *positive* measurements of Earth's motion: annual stellar parallax (§14.1), annual stellar aberration (§14.2), and the relativistic rotation measurements of §16.1 (Sagnac delay, ring-interferometer fringe shift, the GNSS rotation correction) |
| Moon landing faked | negligible | **dominant** — hardware in situ, samples, imagery, independent tracking |
| Area 51 real | none (documented) | none |
| Roswell alien craft/bodies | the alien hardware was never produced | **substantial** for the specific artefacts and witnesses offered (hoax, fabrication, fictional sources, documented dummy recoveries); the *general* "there is classified material we cannot see" hypothesis is unfalsifiable and cannot be excluded |
| Alien abduction | **the whole claim rests on absence** | strong for the *accounts* (mechanisms fully explain them); no single decisive experiment falsifies the negative |

**3. A note on conspiracy arithmetic.** A hoax of the Apollo scale would require the silence of roughly 400,000 people across NASA and its contractors plus the Soviet Union's entire deep-space network, the Great Soviet Encyclopedia's editorial board, Soviet Academy planetologists who exchanged samples, and two generations of independent laboratories that have since dated lunar meteorites found by desert nomads. The Roswell story, by contrast, requires no conspiracy at all in its documented version — a classified balloon programme with a genuine reason to keep quiet. When a mundane explanation requires fewer assumptions and explains *more* of the data, the conspiracy explanation is not merely unlikely; it is unnecessary.

---

## 7. Sources

Retrieved live on 2026-10-06 via the MediaWiki API (en.wikipedia.org/w/api.php), plus direct computation. Primary documents and institutional sources are named where they are the underlying authority.

**Empirical/measurement sources**
1. Lunar Laser Ranging experiments — Apollo 11/14/15 arrays (installed 21 July 1969), Lunokhod 1/2, Chandrayaan-3; first range 1 August 1969 (3.1 m, Lick Observatory); 3 × 10¹⁷ photons out, ~1–5 back; 385,000.6 km mean distance; mm precision, 1 cm weighted rms; 3.8 cm/yr recession. *Wikipedia, "Lunar Laser Ranging experiments"; International Laser Ranging Service; Lick Observatory.*
2. ~381 kg returned by six Apollo missions, 2,200 samples; Apollo 11 21.55 kg; Apollo 15 77 kg; ages 3.16–4.44 Ga; armalcolite/tranquillityite/pyroxferroite. *Wikipedia, "Moon rock", "Apollo 11", "Apollo 15"; NASA Lunar Sample Laboratory Facility.*
3. >370 lunar meteorites, >1,090 kg; **sample exchange of 10 June 1971** between the Soviet Academy of Sciences and NASA, in Moscow, in which Luna 16 material was exchanged for Apollo 11 and Apollo 12 samples; a 0.4825 g Luna 16 sample from a depth of 27 cm was sent to Britain. *Wikipedia, "Moon rock", "Luna 16".* The Luna 16 returned mass and the Apollo 12 resemblance were removed here in the second pass and **reinstated and verified verbatim in the fourth** (§10.0 item 1, §13.2(a)).
4. Sotheby's sales of Luna 16 fragments: three fragments **totalling 0.2 g (200 mg)** for US$442,500 (1993), resold for US$855,000 on **29 November 2018**. *Wikipedia, "Luna 16", "Moon rock".*
5. LRO/LROC: 0.5 m/pixel NAC imagery at 50 km altitude showing LM descent stages, rovers, ALSEP hardware, tracks; 2012 images of five of six flags still standing. *Wikipedia, "Lunar Reconnaissance Orbiter", "Moon landing conspiracy theories."*
6. ALSEP operations terminated 30 September 1977; all five transmitters observed by the Soviet **RATAN-600** radio telescope 18 October–28 November 1977; Apollo 12 LM ascent stage impact ≈ 1 ton of TNT as calibration. *Wikipedia, "Apollo Lunar Surface Experiments Package", "Apollo 12".*
7. Apollo radiation transit: inner belt in minutes, outer belt in ~1.5 h; average dose <1 rem (10 mSv) ≈ sea-level ambient for three years; Van Allen's own rebuttal; belts extend ~640–58,000 km altitude. *Wikipedia, "Moon landing conspiracy theories", "Van Allen radiation belt"; P. Plait,* Bad Astronomy *(2002).*
8. Great Soviet Encyclopedia, 3rd edition (1970–1979), reporting the landings as factual. *Wikipedia, "Moon landing conspiracy theories."*
9. Lunar surface temperature −171 °C to +120 °C; exosphere <10 tonnes, ~3 × 10⁻¹⁵ atm. *Wikipedia, "Moon".*
10. Apollo 16 Far Ultraviolet Camera star positions matched to orbiting UV telescopes. *Wikipedia, "Moon landing conspiracy theories."*

**Geodesy / geometry / astronomy sources**
11. Eratosthenes: Alexandria–Syene, 7.2° = 1/50 of a circle, 5,000 stadia × 50 = 250,000 stadia; result 39,375–46,250 km depending on the stadion (157.5–185 m), central estimate ≈40,300 km; two cancelling errors (Syene 1° north of the Tropic and 3° east of Alexandria); Earth's equatorial circumference 40,075.017 km, polar 40,007.863 km, flattening 0.3%. *Wikipedia, "Eratosthenes", "Earth's circumference", via Cleomedes* On the Circular Motion of the Heavenly Bodies *(De Motu Circulari) and Pliny.*
12. Foucault pendulum: introduced 1851; Panthéon 28 kg bob on a 67 m wire; precession 15.04°/sidereal hour × sin(lat), 11.3°/h at 48.85° N; 30° S → 360° in two days; Amundsen–Scott 33 m/25 kg pendulum, ~24 h period. *Wikipedia, "Foucault pendulum".*
13. Horizon distance: 4.8 km at 1.8 m, ~5 km at 2 m, from *Wikipedia, "Horizon"*; the 30 m value (19.55 km) is this report's own computation, not from that article.
14. Midnight sun: South Pole ≈20 September – 23 March (about 6 months; the same article splits the polar year into ~179 days of sun and ~186 of darkness); Sun rises and sets once per year on the equinoxes; maximum elevation ~23.5° at the December solstice; South Pole altitude 2,835 m, ice ~2,700 m thick. *Wikipedia, "Midnight sun", "South Pole".*
15. Independent Investigations Group (Center for Inquiry), Salton Sea, 10 June 2018 curvature demonstration; Will Duffy's "Final Experiment", Union Glacier Camp, 14 December 2024; *Behind the Curve* (2018) ring-laser gyroscope detecting 15°/hour. *Wikipedia, "Modern flat Earth beliefs".*
16. GRS 80 (IUGG XVII General Assembly, 1979): a = 6,378,137 m, flattening 1:298.257; the basis of GPS geodetic positioning; one geographical mile = 1,855.32571922 m. *Wikipedia, "Geodesy".*
17. GPS: satellites at ~20,000 km altitude (12,427 mi), two orbits per day, constellation of 24 operational (31 as flown); relativistic clock correction of 38 µs/day; surveying accuracy to 2 cm, sub-millimetre over long baselines. *Wikipedia, "Global Positioning System", "GPS satellite blocks".*
18. Qantas: QF9 Perth–London non-stop, 25 March 2018, 17 h, 14,498 km; the New York–Sydney long-haul research flights of 2019 (19 h 20 min, 20 October 2019); commercial aviation measures route length as **great-circle distance** and uses it as the ICAO standard. *Wikipedia, "Qantas", "List of longest flights".*
19. **Stellar parallax (fifth pass):** the nearest star, Proxima Centauri, lies "4.25 light-years (1.3 parsecs)" away, i.e. 4.01 × 10¹³ km, giving a measured annual parallax of 0.767–0.769 arcsec (the two verified expressions differ by 0.23%). Parallax baseline 1 AU = 149,597,870.7 km (IAU). *Wikipedia, "Proxima Centauri", "Stellar parallax".*
20. **Stellar aberration (fifth pass):** a star's apparent position "varies periodically over the course of a year as the Earth's velocity changes as it revolves around the Sun, by a maximum angle of approximately 20 arcseconds," of order *v*/*c*; classical constant ≈ 20.5″. Predicted here from Earth's mean orbital speed of 29.78 km/s: **20.489 arcsec** (29.785 km/s computed from 2π·AU/yr gives 20.493 arcsec). *Wikipedia, "Aberration (astronomy)".*
21. **Betelgeuse (fifth pass):** angular diameter **0.047 arcsec** measured by Michelson for a uniform disk ("limb darkening would increase the angular diameter by about 17%, hence 0.055 arcseconds"); radius ~640 R☉; distance 408 ly = 125 pc. The θ-and-R cross-check implies 413 ly, reproducing the article's own figure to 1.2%. Provenance flag: the same article's infobox carries parallax 5.95 mas (= 168 pc) alongside 408 ly (= 125 pc), a 35% internal inconsistency in the source; both are hundreds of parsecs and so the argument is unaffected. *Wikipedia, "Betelgeuse".*
22. **Thermal conductivity (fifth pass):** Stephens Basalt 1.36–1.92 W/(m·K); Barre Granite 2.1–2.8 W/(m·K) dry at 50 bar, up to 4.5 at 5,000 bar; marble 2.07–2.94; Indiana Limestone 0.62–1.33. Used only to restate the §13.1 regolith comparison as a range. *Wikipedia, "List of thermal conductivities".*
23. **Earth's internal heat budget (fifth pass):** "estimated at 47 ± 2 terawatts", with estimates spanning 43–49 TW; mean surface flux 91.6 mW/m² (recomputed here as 92.1 mW/m² over 5.101 × 10¹⁴ m²); specific output 7.87 × 10⁻¹² W/kg. *Wikipedia, "Earth's internal heat budget".*

**Historical / documentary sources (Roswell, Area 51, abduction)** — numbered 24–32 so as not to collide with the geodesy entries 11–23 above
24. USAF, *The Roswell Report: Fact versus Fiction in the New Mexico Desert* (1995) — the cause narrowed to a specific Project Mogul balloon train, **NYU Flight 4, launched 4 June 1947** from Alamogordo AAF and lost within 17 mi (27 km) of the Brazel ranch near Corona, NM. *Wikipedia, "Project Mogul", "Roswell incident".*
25. USAF, *The Roswell Report: Case Closed* (24 June 1997) — body-bag accounts matched to 1950s anthropometric test-dummy recoveries (Operation High Dive), stretchers, casket-shaped crates, insulation bags, and the Dodge M37. *Wikipedia, "Roswell incident".*
26. Area 51: 83 mi NNW of Las Vegas; base 6 × 10 mi within 23 × 25 mi restricted airspace; Homey Airport (KXTA/XTA); acquired 1955 for Project Aquatone/U-2; A-12 OXCART from September 1960; 10,000 ft runway; 1,320,000 US gal fuel farm; D-21 from 1964; captured Soviet aircraft testing from the late 1960s; **CIA public acknowledgement 25 June 2013** following a 2005 FOIA request. *Wikipedia, "Area 51".*
27. Project Mogul: 1947–early 1949; Maurice Ewing (concept), James Peoples (supervision), Albert P. Crary; disc microphones on constant-altitude polyethylene balloon trains; forerunner of Skyhook. *Wikipedia, "Project Mogul".*
28. Aztec, NM crashed-saucer hoax (1948), relayed by Frank Scully; "Hangar 18" (Robert Spencer Carr, 1974; the Air Force states no such location existed); Majestic-12 documents (admitted by Bill Moore as typed/stamped facsimiles); Alien Autopsy footage (Ray Santilli admitted the fabrication in 2006, shot in a London living room); Glenn Dennis's fabricated nurse names; Pflock's audit (23 of 300+ with any claim to physical evidence, 7 suggesting otherworldly origin). *Wikipedia, "Roswell incident".*
29. Betty and Barney Hill (1961); Bullard's analysis of ~300 cases; Budd Hopkins and David M. Jacobs' hybridisation claims; John E. Mack (800+ interviews; Harvard review 1994; *Lancet* critique); prevalence 8–50% lifetime and ~5% recurrent for sleep paralysis with the intruder/incubus/vestibular-motor triad; contested surveys claiming 5–6% of the population report abduction; Michael Shermer on the camera-phone burden of evidence; accounts peaking mid-1970s. *Wikipedia, "Alien abduction", "Sleep paralysis".*
30. Rowbotham's 1838 Bedford Level experiment and Wallace's 1870 refraction-corrected repetition; Voliva's $5,000 challenge (1870s–1940s context, Zion, Illinois); Flat Earth Society membership ~3,500 at peak. *Wikipedia, "Modern flat Earth beliefs".*

31. **Verified live in the second pass:** *Wikipedia*, "Global Positioning System" — "Orbiting at an altitude of approximately 20,200 km (12,600 mi); orbital radius of approximately 26,600 km (16,500 mi), each SV makes two complete orbits each sidereal day." *Wikipedia*, "South Pole" — the six-month "day", with temperatures reaching −55 °C around sunset in late March and sunrise in late September. *Wikipedia*, "Solar eclipse" — the Sun and the Moon "appear to be approximately the same size: about 0.5 degree of arc." *Wikipedia*, "Lunar Laser Ranging experiments" — 3×10¹⁷ photons out, ~1–5 back; 385,000.6 km mean distance; 3.8 cm/yr recession; millimetre precision. *Wikipedia*, "Moon rock" — 2,200 samples, 381 kg, >110,000 cataloged specimens; Luna spacecraft 301 g total.
32. Standard constants used only as inputs to the computations in §8/§9: solar radius 695,700 km; 1 AU = 149,597,870.7 km; Earth orbital eccentricity 0.0167086; obliquity of the ecliptic 23.4392911°; sidereal day 86,164.0905 s; μ = GM = 398,600.4418 km³ s⁻². These are conventional IAU/IUGG values, not retrieved measurements, and are stated here so the arithmetic can be rerun independently.

**Verified live in the third pass (2026-10-06)**

33. *Wikipedia, "Lunar Laser Ranging experiments"* — "Out of a pulse of 3×10¹⁷ photons aimed at the reflector, only about 1–5 are received back on Earth"; "At the Moon's surface, the beam is about 6.5 kilometers (4.0 mi) wide"; "averages 385,000.6 km"; "Modern Lunar Laser Ranging data can be fit with a 1 cm weighted rms residual"; "Successful lunar laser range measurements to the retroreflectors were first reported on Aug. 1, 1969 by the 3.1 m (10 ft) telescope at Lick Observatory"; the six reflectors (Apollo 11/14/15, Lunokhod 1/2, Chandrayaan-3) and the statement that a bare-surface EME return is possible but far less precise.
34. *Wikipedia, "List of retroreflectors on the Moon"* — Apollo 11 LRRR, 46 × 46 cm, Mare Tranquillitatis, 0.6734° N 23.4731° E, 21 July 1969, Operational, citing NIST and Wagner, Speyerer, Burns & Robinson, "Revised Coordinates for Apollo Hardware", *Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci.* XXXIX-B4, 517–521 (2012); Lunokhod 1, 44 × 19 cm, Mare Imbrium, 38.3152° N 35.0080° W, 17 November 1970; Apollo 14, Fra Mauro, 3.6442° S 17.4786° W, 31 January 1971; Apollo 15, Hadley–Apennine, 26.1334° N 3.6285° E, 31 July 1971; Lunokhod 2, Le Monnier, 25.8323° N 30.9221° E, 15 January 1973; Chandrayaan-3, 5.11 cm single reflector, Statio Shiv Shakti, 69.367621° S 32.348126° E, 23 August 2023, Operational.
35. *Wikipedia, "Luna 16"* — "On 10 June 1971, the Soviet Academy of Sciences exchanged Luna 16 samples with NASA in Moscow, receiving samples from Apollo 11 and Apollo 12"; "A 0.4825 g sample of material from a depth of 27 cm was sent to Britain"; "Three tiny samples (0.2 grams) of the Luna 16 soil were sold at Sotheby's auction for $442,500 in 1993. The samples were resold by Sotheby's for US$855,000 on 29 November 2018."
36. *Wikipedia, "Alien abduction"* — "One of the earliest studies of abductions found 1,700 claimants, while contested surveys argued that 5–6 percent of the general population allege to have been abducted"; Bullard's analysis of ~300 reports and his inability to identify a child-presentation phase; the child-presentation phase as "an innovation in the story" with "no clear antecedents … before its popularization by Hopkins and Jacobs"; the 2021 lucid-dreaming emulation study in which 114 volunteers (75%) emulated alien encounters, ~20% of them rated close to reality; the McNally and Slater psychopathology findings; Boyce's *Lancet* critique of Mack.
37. *Wikipedia, "Sleep paralysis"* — "Between 8% to 50% of people experience sleep paralysis at some point during their lifetime. About 5% of people have regular episodes"; episodes 1–6 minutes; the intruder / incubus / vestibular-motor hallucination triad and their neurobiological account.

**Note on sourcing.** Where a figure could not be verified against a primary source during this session (e.g. the per-mission sample mass distribution for Apollo 12/14/16/17), it is not asserted above; only figures retrieved or derived from the sources listed are given. No page numbers, DOIs or exact quotations beyond those in the retrieved texts are invented.

### 7a. Sources added in the fourth pass

38. *Wikipedia, "Heat Flow Experiment"* — "The HFE found a thermal gradient of between 1.5–2.0 K/m with a heat flow of around 17 mW/m2. When accounting for measurement uncertainty, this aligned well with seismic and magnetic data. This would imply temperatures that would be relatively close to melting at depths of around 300 km (190 mi)."; "During the lunar noon, 70% of all heat transfer was radiative"; regolith density rising "from 1.1–1.2 g/cc to 1.75–2.1 g/cc" after the first 2–3 cm; probes of two 50 cm sections with gradient thermometers at 28 and 47 cm and cable thermocouples at 0/65/115/165 cm; heater settings 0.002 W and 0.5 W; Apollo 15 drilled to 170 cm before Scott had to apply his full weight, the second Apollo 15 hole reached only 100 cm, **Apollo 16's two holes were drilled to 3 m** by Charles Duke but the connecting cable was broken and the experiment inoperable, Apollo 17's two boreholes were drilled and installed without problem; successful heat-flow results were therefore obtained on **Apollo 15 and Apollo 17 only**; Apollo 13's instrument was lost with the in-flight abort.
39. *Wikipedia, "Moonquake"* — "The instruments placed by the Apollo 12, 14, 15 and 16 missions functioned perfectly until they were switched off in 1977"; "Between 1972 and 1977, 28 shallow moonquakes were observed"; shallow events to mB = 5.5; deep moonquakes "~700 km below the surface, probably tidal in origin"; shaking "can last for up to an hour, due to fewer attenuating factors to damp seismic vibrations".
40. *Wikipedia, "Apollo Lunar Surface Experiments Package"* — the ALSEP experiment and institution list including the Heat Flow Experiment (Columbia University, M. Langseth; Yale University, S. Clark) and the Passive Lunar Seismic Experiment (MIT, Frank Press; Columbia, George Sutton; Georgia Tech, Robert Hostetler); "the seismometer was sensitive enough to detect Neil Armstrong's movements during sleep".
41. *Wikipedia, "Luna 16"* — **re-fetched in full this session**: "The 101 grams (3.56 ounces) sample was returned from Mare Fecunditatis"; drill "reached a stop at 35 centimeters depth"; capsule "reentered Earth's atmosphere at a velocity of 11 kilometers per second" and parachuted "80 kilometers southeast of the town of Jezkazgan in Kazakhstan"; **"Analysis of the dark basalt material indicated a close resemblance to soil recovered by the American Apollo 12 mission."** This is the reinstatement recorded in §10.0 item 1 and §13.2.
42. *Wikipedia, "Nickel titanium"* — "The shape-memory effect was discovered in 1932, when Swedish chemist Arne Ölander observed the property in gold–cadmium alloys. The same effect was observed in Cu-Zn (brass) in the early 1950s"; nitinol "announced the successful creation" at the Naval Ordnance Laboratory in 1962. Used in §13.2 for the chronology argument only.
43. *Wikipedia, "Roswell incident"*, re-fetched in full — "On June 4, researchers at Alamogordo Army Air Field in New Mexico launched a long train of these balloons; they lost contact with the balloons and balloon-borne equipment within 17 miles (27 km) of the ranch managed by W. W. 'Mac' Brazel near Corona, New Mexico"; "Brazel told the Record that the debris consisted of rubber strips, 'tinfoil, paper, tape, and sticks'"; Bessie Brazel Schreiber's description matching Mogul materials ("pieces of heavily waxed paper and a sort of aluminum-like foil … Some of the metal-foil pieces had a sort of tape stuck to them"); Marcel's 1978 description of "a foil that could be crumpled but would uncrumple when released"; Berlitz and Moore's "over 90 witnesses" of whom only 25 appear in the 1980 book, only seven claimed to have seen the debris and five to have handled it; the July 8 1947 press release quoted in full; the July 9 press conference at which Irving Newton identified the material as weather-balloon parts; Colonel Marcellus Duffy's identification at Wright Field and his call to Mogul's project officer Albert Trakowski.

### 7b. Sources added in the sixth pass (2026-10-06)

44. *Wikipedia, "Sagnac effect"* — the full paragraph on Michelson–Gale–Pearson ("a perimeter of 1.9 kilometer"; "The measured shift was 230 parts in 1000, with an accuracy of 5 parts in 1000. The predicted shift was 237 parts in 1000"); the around-the-world relay figure ("equal to the time difference that is found for a relay of pulses that travels around the world: 207 nanoseconds"); "In 1984 a verification was set up that involved three ground stations and several GPS satellites, with relays of signals both going eastward and westward around the world"; "Global navigation satellite systems (GNSSs) — such as GPS, GLONASS, COMPASS or Galileo — need to take the rotation of the Earth into account in the procedures of using radio signals to synchronize clocks"; "Ring laser interferometers are self-calibrating. The beat frequency will be zero if and only if the ring laser setup is non-rotating with respect to inertial space"; "The ring laser also can detect the sidereal day, which can also be termed 'mode 1'"; and Ashby, N. (2003), "Relativity in the Global Positioning System", *Living Reviews in Relativity* 6:1.
45. *Wikipedia, "Lunokhod 1"* — "The final location of Lunokhod 1 was uncertain until 2010, as lunar laser ranging experiments had failed to detect a return signal from it since 1971"; "On March 17, 2010, Albert Abdrakhimov found both the lander and the rover in Lunar Reconnaissance Orbiter (LRO) image M114185541RC (Line 21977, Sample 3189)"; the APOLLO re-acquisition of April 2010 and the first measurement on 22 April 2010; "We got about 2,000 photons from Lunokhod 1 on our first try. After almost 40 years of silence, this rover still has a lot to say"; "The intersection of the spheres described by the measured distances then pinpointed the current location of Lunokhod 1 to within 1 meter"; "By November 2010, the location of the rover had been determined to within about a centimeter"; the May 2013 replication by French scientists at the Côte d'Azur Observatory; rover dimensions 171 × 160 × 108 cm, mass 840 kg, height 135 cm.
46. *Wikipedia, "Project Blue Book"* — March 1952 to 17 December 1969, HQ Wright-Patterson AFB; "By the time Project Blue Book ended, it had collected 12,618 UFO reports"; "701 reports were classified as unexplained, even after stringent analysis"; "By the time of the hearing, Blue Book had identified and explained 95% of the reported UFO sightings"; the two published USAF conclusions quoted verbatim in §16.4; the Condon Report's conclusion and the National Academy of Sciences review; the Robertson Panel; AFR 200-2; the U-2 and A-12 identifications per the National Reconnaissance Office.
47. *Wikipedia, "Alien abduction"* re-fetched in full — "Hopkins has estimated that these 'errors' accompany 4–5 percent of abduction reports" (the "cosmic application of Murphy's Law": returning the experiencer to the wrong spot, clothes on backwards); Mack "interviewing over 800 people"; the 2017 Kodachrome slides revealed as a mummified Native American child from 1896 on display at the Chapin Mesa Archeological Museum, Mesa Verde, for decades; the c.1951 radioactive-suits/oxygen-mask incident declassified in 2020; *Wikipedia, "Lunar Laser ranging experiments"* re-fetched — "Three were placed by the United States' Apollo program (11, 14, and 15), two by the Soviet Lunokhod 1 and 2 missions, and one by India's Chandrayaan-3 mission"; "The Apollo 15 array is three times the size of the arrays left by the two earlier Apollo missions"; "Lunokhod 2's array continues to return signals to Earth"; "As of 2009, the distance to the Moon can be measured with millimeter precision". *Coordinates retrieved via the MediaWiki API (`prop=coordinates`):* Alamogordo, NM 32.856111° N 105.974444° W; Corona, NM 34.247778° N 105.596944° W; Roswell, NM 33.3942° N 104.5228° W.
48. Standard constants used only as inputs: Earth's sidereal rotation rate Ω = 7.2921159 × 10⁻⁵ rad s⁻¹ (sidereal day 86,164.0905 s); *c* = 299,792,458 m s⁻¹; WGS-84 semi-major axis 6,378,137 m; WGS-84 mean radius 6,371.0 km; GPS geocentric radius 26,560 km (derived, not assumed, in §2.3a); ISA lapse rate 6.5 K km⁻¹; helium gas constant 2,077 J kg⁻¹ K⁻¹. All are conventional IAU/IUGG/US-standard-atmosphere values, stated so the arithmetic can be rerun independently.

**Note on sourcing (sixth pass).** Where a figure could not be verified against a primary source during this session (e.g. the June 1947 upper-air wind field in §16.3, and any APOLLO station specification in §16.2), it is not asserted; the figure is either assumed and labelled (A) or the item is left explicitly open. No page numbers, DOIs or exact quotations beyond those in the retrieved texts are invented.

---

## 8. Reproducibility — derived arithmetic

All values in this section were computed locally from first principles during this session; the script is saved as `derivation.py` in the working directory. A second script, `derivation2.py`, closes three further gaps (the disc model's South-Pole prediction, sunset geometry on a plane, Kepler's third law for GPS/geostationary satellites, and a modern repeat of Eratosthenes' two-site shadow measurement); its output is reproduced in §9. A third, `derivation3.py`, computes the lunar laser ranging link budget and the expected-detection-rate arithmetic for claim (d) (§10), and a fourth, `derivation4.py`, turns the Apollo seismic and heat-flow instruments and the Roswell chronology into numbers (§13). Inputs: R = 6,371.0088 km; GRS 80 a = 6,378,137 m, 1/f = 298.257223563; Somigliana g₀ = 9.7803253359 m/s², k = 0.00193185138639.

```
1. Nautical-mile identity                        d/R for 1852 m      = 59.96 arcsec = 1 arcmin
   verticals 100 km apart differ by              0.8993° (53.96′)
   verticals 1,000 km apart differ by            8.9932° (539.6′)
   verticals 4,000 km apart differ by            35.9728° (2,158′)

2. Geometric horizon (R = 6371 km):               h = 1.7 m → 4.65 km  (dip 0.0419°)
                                                 h = 2.0 m → 5.05 km  (dip 0.0454°)
                                                 h = 30 m  → 19.55 km (dip 0.1758°)
   Height of a receding vessel hidden below the sightline, observer at 2.0 m:
      5 km → 0.0 m      10 km → 1.9 m      20 km → 17.5 m      30 km → 48.9 m

3. Eratosthenes: 250,000 stadia                  stadion 157.5 m → 39,375 km (−1.7% vs 40,075 km)
   (5,000 stadia × 50)                           stadion 161.3 m → 40,325 km (+0.6%)
                                                stadion 185.0 m → 46,250 km (+15.4%)

4. Never-visible latitudes from declination δ (never rises if |φ − δ| > 90°):
      Polaris   δ = +89.264°   → never rises south of 0.74° S; circumpolar north of 0.74° N
      Acrux     δ = −63.099°   → never rises north of 26.9° N
      Mimosa    δ = −59.690°   -> never rises north of 30.3° N
      Gacrux    δ = −57.113°   → never rises north of 32.9° N

5. Great circle (R = 6371 km) vs flat disc (azimuthal equidistant about the North Pole):
      Sydney–Santiago        11,340 km vs 25,679 km  (2.26×)
      Johannesburg–Perth      8,310 km vs 18,350 km  (2.21×)
      Cape Town–Sydney       10,989 km vs 25,239 km  (2.30×)
      Buenos Aires–Auckland  10,313 km vs 25,025 km  (2.43×)
      Perth–London (computed) 14,508 km vs published QF9 14,498 km (0.07%)

6. WGS-84 normal gravity (Somigliana):
      lat  0° → 9.7803 m/s²      lat 45° → 9.8062 m/s²      lat 90° → 9.8322 m/s²
      lat 30° → 9.7932 m/s²      lat 60° → 9.8192 m/s²      (total change +0.53%)
      b = a(1 − f) = 6,356,752.3 m

7. Lunar-eclipse geometry:        Earth's umbral length ≈ 1.377 × 10^6 km, ≈ 3.58× the 384,400 km lunar distance
                                  ⇒ the umbra is always wider than the Moon ⇒ the shadow is always circular
   Foucault (Panthéon, 48.8467° N): 15.041°/h × sin φ = 11.30°/h ⇒ pendulum day = 31.8 h
```

---

## 9. Second reproducibility block — `derivation2.py`

Computed in the same session, after the first draft, to close three gaps in §2 where the brief asked for a decisive test that had previously been given only qualitatively. Inputs are published constants and measured values only; nothing is fitted.

```
A. FLAT-DISC MODEL AT THE SOUTH POLE (disc = azimuthal equidistant about the North Pole)
   South Pole polar distance 180 deg        -> r = 20,015 km from the North Pole
   Sun polar distance (Jun solstice, +23.44 deg)  -> r =  7,401 km
   Sun polar distance (Dec solstice, -23.44 deg)  -> r = 12,614 km
   => Sun-South-Pole horizontal separation  -> 7,401 - 12,614 km, ALWAYS
   Predicted solar elevation at the South Pole (Sun never descends on a plane):
       Sun altitude  3,000 km -> 13.4 - 22.1 deg, 365 days/yr
       Sun altitude  4,828 km -> 20.9 - 33.1 deg, 365 days/yr
       Sun altitude 10,000 km -> 38.4 - 53.5 deg, 365 days/yr
       Sun altitude 30,000 km -> 67.2 - 76.1 deg, 365 days/yr
   OBSERVED: up ~20 Sep - 20 Mar (~179 days), ABSENT ~186 days,
             one sunrise/sunset per year at the equinoxes, max elevation 23.44 deg
   => the disc model predicts the South-Pole Sun NEVER SETS AT ALL (up 365 days/yr);
      the observed dark season is ~186 days, so the model's error is categorical, not
      bounded by 186 days

B. SUNSET ON A PLANE (size-independent ratio test)
   theta(sunset)/theta(noon) = H / sqrt(H^2 + X^2)
       H =  3,000 km, X = 20,015 km -> 0.148  (Sun 6.75x SMALLER at sunset)
       H =  4,828 km, X = 20,015 km -> 0.234  (Sun 4.26x SMALLER at sunset)
       H = 10,000 km, X = 20,015 km -> 0.447  (Sun 2.24x SMALLER at sunset)
   Real Sun, computed from r = 695,700 km:
       perihelion 147,098,300 km -> 0.5420 deg (32.52 arcmin)
       mean 1 AU  149,597,871 km -> 0.5329 deg (31.97 arcmin)
       aphelion   152,097,442 km -> 0.5241 deg (31.45 arcmin)
       annual range = +/-1.7% (eccentricity only, correlated with date not hour)
   Flat model's own Sun (32 mi dia at 3,000 mi altitude -- NOTE: this hybrid mixes
   Rowbotham's altitude with the modern Flat Earth Society's diameter; no single cited
   model pairs them) predicts 36.67 arcmin at noon: 15% too big.  The ratio test above
   is independent of the Sun's size and survives either way.
   To hold angular diameter within 1% out to the rim: H >= 141,176 km (~22 Earth radii),
   which would make the noon Sun 1.25 arcmin across -- 25x too small.
   => "perspective sunset" and "constant angular diameter" cannot both hold on a plane.

C. KEPLER'S THIRD LAW (mu = GM = 398,600.4418 km^3/s^2)
   GPS:    a = 26,560 km -> T = 11.966 h ; a = 26,600 km -> T = 11.993 h
           observed 2 orbits per sidereal day = 11.9672 h   -> agreement 0.01%
   Geostat: T = 1 sidereal day -> a = 42,164.2 km -> altitude 35,786.0 km
           (equatorial radius 6,378.137 km, correct for an equatorial orbit;
            using the MEAN radius gives 35,793 km and a spurious 0.02% "agreement")
           published ~35,786 km                          -> agreement ~0.0001%
```

**Source of the two inputs verified live in this session:** the GPS altitude/orbital-radius/"two complete orbits each sidereal day" figures are from *Wikipedia*, "Global Positioning System"; the South-Pole six-month day/night cycle is from *Wikipedia*, "South Pole"; the ~0.5° equality of the solar and lunar angular diameters is from *Wikipedia*, "Solar eclipse". Solar radius 695,700 km, 1 AU = 149,597,870.7 km, Earth eccentricity 0.0167086, obliquity 23.4392911°, sidereal day 86,164.0905 s and μ = 398,600.4418 km³ s⁻² are standard IAU/IUGG constants.

```
D. ERATOSTHENES REPEATED TODAY (derivation2.py, section 4)
   Memphis (35.1495 N, -90.0490 W) - New Orleans (29.9511 N, -90.0715 W):
       great-circle distance        = 578.0 km
       latitude difference          = 5.1984 deg = 0.090729 rad
       implied Earth radius         = 6,371 km  (+0.00%)
   Eratosthenes' own numbers (Syene 24.0889 N - Alexandria 31.2001 N):
       true great-circle distance   = 843.4 km
       5,000 short stadion (157.5 m) = 787.5 km -> implied R = 6,267 km (-1.6%)
       5,000 long  stadion (185.0 m) = 925.0 km -> implied R = 7,361 km (+15.5%)
   Flat-plane cross-check (Memphis-New Orleans, 5.1984 deg elevation difference):
       required solar altitude H = 14,311 km (from Memphis) vs 7,958 km (from New Orleans)
       -> INCONSISTENT by a factor of 1.8: no single H fits even one pair of sites
```

---

## 10. Third pass — `derivation3.py` (2026-10-06)

A third computational block was run to close the two quantitative gaps the first two passes had explicitly left open, and to turn one further *observed* fact into a *test*. Full script output is saved as `scratch/derivation3.out`; the script is `derivation3.py`. Inputs are marked **(V)** = verified live in this session from the source named, or **(A)** = assumed parameter, each scanned over a stated range. Nothing is fitted.

### 10.0 Corrections to the first two passes

Re-verification against the live sources changed three things:

1. **RETRACTED, AND THEN UN-RETRACTED (an error of mine, now fixed).** The first draft stated that "Luna 16 returned 101 g from Mare Fecunditatis … and its dark basalt indicated a close resemblance to soil recovered by the American Apollo 12 mission," citing *Wikipedia, "Luna 16"*, and the second pass removed both statements on the grounds that "the retrieved text does not contain them." **That removal was an error.** Re-fetched in this session at the default extract length, the article contains both statements verbatim: "The 101 grams (3.56 ounces) sample was returned from Mare Fecunditatis" and "Analysis of the dark basalt material indicated a close resemblance to soil recovered by the American Apollo 12 mission." Both are **reinstated and now verified verbatim** in §1, §3.3 and §13.2. The lesson recorded here is procedural as well as substantive: the earlier pass searched the *retrieved extract* rather than the article, and then presented a search failure as a fact about the source. **This is now the third error of that class in this report's own checking** (the other two being the first pass's two unsourced assertions and this one), and it is recorded because it changes how the "verified" labels below should be read: they record that a string matched a fetched extract, not that the underlying claim has been independently established.
2. **Corrected.** The Sotheby's sale of Luna 16 material was recorded as "three 0.2 g fragments … US$442,500 (1993) and US$855,000 (2018)". The live text says "Three tiny samples (0.2 grams) … sold at Sotheby's auction for $442,500 in 1993 … resold by Sotheby's for US$855,000 on 29 November 2018", and *Wikipedia, "Moon rock"* confirms the fragments weigh **200 mg in total**. Corrected to "three fragments totalling 0.2 g (200 mg)", with the resale date fixed at 29 November 2018.
3. **Confirmed and extended.** The 10 June 1971 Soviet/NASA sample exchange is confirmed verbatim: "On 10 June 1971, the Soviet Academy of Sciences exchanged Luna 16 samples with NASA in Moscow, receiving samples from Apollo 11 and Apollo 12." A further 0.4825 g Luna 16 sample from a depth of 27 cm was sent to Britain.

### 10.1 The lunar laser ranging link budget, computed from first principles

Claim (b) was previously supported by the *observed* fact that the retroreflectors return ~1–5 photons. An observation is an input, not a test. This block computes the entire chain and compares the result with the observation.

**Verified inputs (V)** — *Wikipedia, "Lunar Laser Ranging experiments"*: 3 × 10¹⁷ photons per pulse emitted; beam **6.5 km** wide at the Moon's surface; mean Earth–Moon distance **385,000.6 km**; round trip **2.568 s**; **1–5 photons** received back; fitted range residual **1 cm weighted rms**. Apollo 11 array: **46 × 46 cm panel**, Mare Tranquillitatis, 0.6734° N 23.4731° E, placed 21 July 1969, still operational (*Wikipedia, "List of retroreflectors on the Moon"*, citing NIST and Wagner et al. 2012).

**Assumed parameters (A)**, each scanned: ruby wavelength 694.3 nm; 3.8 cm corner-cube aperture × 100 cubes = 0.1134 m² projected aperture = **54% of the 46 × 46 cm panel**; detector quantum efficiency 0.05–0.10 for a 694.3 nm photomultiplier. (The inversion table also prints QE = 0.03 and 0.15 as arithmetic bounds; 0.15 is unrealistically high for that wavelength and is shown only to bracket the result, not as an estimate — the conclusion ‘10²–10³ cm², a corner-cube-scale panel’ holds inside the physical band.)

| Step | Computation | Result |
|---|---|---|
| 1 | photon density at the Moon = 3 × 10¹⁷ / π(3.25 km)² | 9.04 × 10⁹ photons m⁻² |
| 2 | intercepted by the array = ρ × 0.1134 m² | 1.03 × 10⁹ photons (fill factor 3.4 × 10⁻⁹) |
| 3 | return footprint radius at Earth = (λ/d) × 385,000.6 km | **7.03 km** (λ/d = 3.77 arcsec) |
| 4 | fraction into a 3.1 m telescope | 4.86 × 10⁻⁸ |
| 5 | photons arriving at the telescope | **49.8** |
| 6 | photons *detected* at QE = 0.05 / 0.10 | **2.5 / 5.0** |

**No parameter was fitted to the observed return, and the prediction (2.5–5.0 photons) lands inside the observed 1–5.** Sensitivity over beam width 2–13 km and a retroreturn divergence 1–8× diffraction-limited spans 0.02–53 predicted photons, which brackets the observation; the honest strength of the claim is "right order of magnitude to within a factor of a few". Inverting, the observed 1–5 photons require an effective retroreflecting aperture of **10²–10³ cm²** — a square panel 10–30 cm across. At QE = 0.10, exactly **five** returned photons is what a **100-cube** array delivers. That is what the hardware is.

**The decisive exclusion is the alternative.** A return from the *bare* lunar surface — the 6.5 km laser spot reflecting Lambertianly at regolith albedo 0.05–0.20, evaluated on-axis — delivers **0.012–0.049 detected photons per pulse, 51–205× weaker** than the array. (This is the spot return, not a whole-disc full-phase flux; the two are equal by a Lambertian cancellation. Real regolith also shows an opposition surge, which makes a measurement moderately stronger than the pure-Lambertian value — nowhere near enough to close a 51–205× gap, and consistent with the ~10²–10³ enhancement that retroreflectors are known to provide.) The diffuse return is also **~300× broader in time** than the required timing resolution: a 1 cm residual needs the round trip timed to 2Δr/c = **66.7 ps**, whereas the diffuse return is spread over the depth of the illuminated footprint — a geometric sagitta of 3.04 m for a 6.5 km spot on a 1,737.4 km sphere, i.e. **20.3 ns**, and real relief makes it larger. Stated precisely: the *hardness* of the exclusion comes from the **photon deficit** above, not from the width — a clean symmetric pulse can in principle be centroided well below its own width given enough photons, so width alone is not an exclusion. The width is a supporting point: even a perfect detector could not recover 1 cm precision from a return spread over 20 ns, whereas the array return, from a target <1 m in extent, is sharp.

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

Against the documented claimant population of **1,700**, the recurrent population alone (4.05 × 10⁸ people) exceeds it by **2.4 × 10⁵** (≈5 orders of magnitude) — a like-for-like population comparison. Stated in rate terms: even at only one episode per recurrent sufferer per year, ≈4 × 10⁸ episodes of the requisite phenomenology occur annually worldwide. The phenomenon does not need an external cause to be produced at any rate at which it is reported. (The episode-per-year and claimant-count units differ, which is why the population-to-population figure is the one quoted as the headline.)

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

**The honest reading, including where the argument fails.** The concession must be stated *conditionally on p*, not categorically — an earlier draft of this section said the argument "carries only if the contested 5–6% survey figures are right", which the table's own n = 1,700 row refutes. Correctly:

- For the **documented** count (n = 1,700), the silence **is** surprising if p ≳ 10⁻² (P(no record) = 3.8 × 10⁻⁸), and **is not** surprising only at the conservative p = 10⁻³ (P = 18%).
- For **every survey-implied count** (n ≳ 3 × 10⁶) and every tabulated p ≥ 10⁻⁶, P(no record) is below 10⁻⁷, and below 10⁻³⁰⁰ for p ≥ 10⁻⁴.

So the argument does not require the survey figures; it requires only that a physical abduction — craft traversing the atmosphere, beings handling a body, over a claimed hour or two — has at least a ~1-in-100 chance of leaving any verifiable record. What is genuinely contested is that p, and the ~95% credence rests on it. The surveys feed the argument's strength, not its validity. What survives independently of *n* is the **directional** argument: under H_A the per-event recording probability *p* rises monotonically as instrumentation per capita rises — 1961 had no camera phones, no home video, no dashcams, no CCTV, while a 2026 bedroom commonly contains an always-networked camera — so the expected number of detections per decade should have **risen** by orders of magnitude. The reported incidence is instead asserted to have declined from its mid-1970s peak. A physical phenomenon does not become less recordable as recording devices improve. The direction of the trend is the test, and it runs opposite to the physical prediction.

### 10.4 Dated content: a falsifiable prediction of the "stable phenomenon" hypothesis, and its failure

H_A (a stable real phenomenon with stable content) predicts that narrative elements appear at a roughly constant rate across all decades in which reports were collected, and do not track the publication history of a few authors. Verified from *Wikipedia, "Alien abduction"*:

- The "grey" beings and the explicitly extraterrestrial framing entered with the **Betty and Barney Hill case (1961)**, while "purported abductions were cited contemporaneously at least as early as 1954"; earlier cases do not carry the later template.
- The **"child presentation" phase** has a *birth date in the literature*: "Bullard says the child presentation phase seems to be an innovation in the story" with "no clear antecedents … before its popularization by Hopkins and Jacobs" — and Bullard, studying ~300 reports, "could not identify a child presentation phase in the abduction narrative."
- "Many alien abductees recall much of their alleged abduction(s) through hypnosis", and Hopkins began "using hypnosis to extract more details" in the 1970s.

So a specific element of the narrative post-dates the earliest reports by 10–20 years and coincides with the work of two named authors. Under H_A this is a **failed prediction**: the phase should be present throughout.

And the phenomenology is now **reproducible on demand**. A 2021 study in the *International Journal of Dream Research* instructed volunteers to emulate alien encounters by lucid dreaming: **114 volunteers (75% of the sample) succeeded**, and of those **~20% produced accounts rated close to reality** in their absence of dreamlike events — with sleep paralysis and fear observed "only among this 20% … common in 'real' stories." Ordinary people asked to produce the experience can produce it. That is the strongest single new datum for claim (d) in this pass.


### 10.5 Independent audit of this pass, and what it changed

The arithmetic in `derivation3.py` and the fidelity of §10–12 to it were then
audited by a separate read-only reviewer agent, which re-derived every chain
independently. Its findings, and the resulting changes:

**Confirmed correct:** the full LLR link budget (1.03 × 10⁹ photons
intercepted, 7.03 km return footprint, 4.86 × 10⁻⁸ collection fraction, 49.8
photons at the telescope, 2.49/4.98 detected); the sensitivity table actually
bracketing the observed 1–5; the linearity of detected photons in array
aperture and all twelve inversion values; the EME comparison; the 66.7 ps
timing requirement and the 3.04 m sagitta; all six solved *p*⁎ values; the
sleep-paralysis table; and the 2.4 × 10⁵ supply ratio.

**Two substantive defects found, both now fixed in the text above:**

1. **An overstated concession in §10.3.** The first version of this section
   said the detection-rate argument "carries only if the contested 5–6% survey
   figures are right". The table's own *n* = 1,700 row refutes that: at *p* =
   10⁻², P(no record) = 3.8 × 10⁻⁸, i.e. the silence *is* surprising on the
   documented claimant count alone. The argument is weak only for *p* ≲ 10⁻³.
   §10.3 and §5.5 have been rewritten to state the concession conditionally on
   *p* rather than categorically.
2. **An overstated framing of the timing exclusion in §10.1.** "≥300× too
   broad" was presented as a hard exclusion, but a pulse width does not by
   itself bound achievable timing precision — a clean symmetric pulse can be
   centroided well below its own width given enough photons. The *hard*
   exclusion is the 51–205× photon deficit; the ~300× width is a supporting
   point. §10.1 and the script now say exactly that.

**Three lesser notes, also incorporated:** the EME figure is the laser-spot
return, not a whole-disc full-phase flux (mislabelled as the latter); the
inversion table prints QE = 0.15, which is unrealistically high for a 694 nm
photomultiplier and is shown only as an arithmetic bound; and the
§10.2 supply/demand figure divides episodes per year by a cumulative claimant
count, so the like-for-like population-to-population comparison (4.05 × 10⁸
recurrent sufferers vs 1,700 claimants) is now given as the headline.

This is recorded because the point of the exercise is the auditing trail: the
first draft of this report contained two unsourced assertions, and this pass
introduced two overstatements of its own. All four were found by checking, not
by confidence.

---

## 11. Verdicts, revised after the third, fourth, fifth and sixth passes

Nothing in the third pass changed any verdict; two claims were strengthened quantitatively and one confidence basis was made explicit.

| Claim | Verdict (unchanged) | Confidence | What the third pass added |
|---|---|---|---|
| (a) Flat Earth | **F** | **>99.9%** | nothing new; already the strongest position in the report. **Fifth pass:** two positive measurements of Earth's orbital motion added — annual stellar parallax (§14.1) and annual stellar aberration (§14.2) — which change the *logical form* of the refutation rather than its strength: the flat model now fails against direct geometric measurements, not only against the internal inconsistency of its own predictions. |
| (b) Moon landing faked | **F** | **>99.9%** | the observed retroreflector return is now *predicted* from a first-principles link budget rather than merely cited; the bare-surface alternative is excluded by **≥50× in photon flux** — the hard exclusion, since the diffuse return also cannot carry the required 66.7 ps timing, which is a *supporting* rather than a standalone argument (§10.1); three nations' operational arrays confirmed at published coordinates. **Fourth pass:** the brief's named seismic and heat-flow instruments are now quantified (7.87 yr unattended coverage from Apollo 12's landing to the 1977 shutdown, 28 shallow moonquakes 1972–77, gradient 1.5–2.0 K/m, heat flow ~17 mW/m², derived regolith conductivity 8.5–11.3 mW/(m·K), global lunar heat output 640 GW) — and then audited, which removed seven further defects of my own (§13.4) |
| (c1) Area 51 real | **T** | **>99.9%** | re-verified verbatim (CIA acknowledgment 25 June 2013; Homey Airport KXTA/XTA; the A-12 JP-7 fuel farm of 1,320,000 US gal) |
| (c2) Roswell extraterrestrial | **N/E** | **<2%** | re-verified verbatim (Mogul Flight 4, launched 4 June 1947, lost within 17 mi; *Case Closed* 24 June 1997; the 8 July 1947 FBI telex's hexagonal object on a ~20 ft balloon) |
| (c2′) Bodies recovered | **actively disconfirmed** | — | unchanged |
| (d) Alien abduction | **N/E** | **>95%** not literal; **>99%** not physically corroborated | the "expected detection rate" admission is closed by an explicit computation (§10.3), together with the exact conditions under which that argument is weak and must be conceded (it is weak only for p ≲ 10⁻³, i.e. below a ~1-in-500 per-event chance of leaving a record); a new controlled emulation result (§10.4); sleep-paralysis supply quantified in absolute episodes per year (§10.2) |

---

## 12. What would change my mind — consolidated, in priority order

Ordered by how cheap the disconfirming experiment is.

1. **Flat Earth.** One verified observation, by anyone with a sextant and a theodolite, of a receding vessel disappearing hull-down at a range consistent with flat geometry; or two sites where the noon-shadow difference fails to equal the latitude difference; or a ring interferometer / ring-laser gyroscope reading zero rotation at a site where Earth's rotation is known; or a one-way relay of pulses around a great circle showing a Sagnac delay of 0 ns instead of ~207 ns (§16.1); or a southern-hemisphere flight that takes 2.2× its published great-circle time; or — the cheapest disconfirmation of all, and one that uses no flat-model parameter — **a measurement of zero annual stellar parallax and zero annual stellar aberration**, which is what a stationary plane and a nearby dome both require, against the measured 0.77″ and ~20″ (§14). Cost: the textbook is free and the measurement is a two-century-old published result; a *new* sub-arcsecond astrometric confirmation would need an observatory, but none is needed to check the published value.
2. **Moon landing faked.** Range the Apollo 11 array's coordinates (0.6734° N, 23.4731° E) with a pulsed laser and fail to get a pulse, while succeeding from Lunokhod 1's (38.3152° N, 35.0080° W); or date an Apollo basalt and get a terrestrial age; or have a non-US orbiter resolve no hardware at the documented coordinates. Cost: a large telescope and a picosecond laser, or one interplanetary mission.
3. **Roswell.** One analysable artefact with authenticated 1947 provenance and non-terrestrial isotopic composition that survives blinded characterisation in several independent laboratories. Cost: possession of the artefact.
4. **Alien abduction.** One recording, one verified implant, one confirmed falsifiable prediction, or two mutually unacquainted claimants matching verifiable detail against timestamped independent records. Cost: a phone.

None of (1)–(4) exists. In (1) and (2) the disconfirming experiments are cheap enough that anyone reading this could in principle run them; in (3) and (4) they require possession of evidence that, in 79 and 60+ years respectively, has never been produced.

---

## 13. Fourth pass — `derivation4.py` (2026-10-06): seismic and heat-flow instruments, and two corrections of my own

The brief names "Apollo seismic and heat-flow instruments" as one of the decisive tests for claim (b). The first three passes mentioned the ALSEP package only in passing and put no number on either instrument. This pass closes that, adds a chronology check on the Roswell "memory metal" claim, and reverses one of this report's own earlier "retractions," which turns out to have been an error of provenance checking rather than of the underlying record.

### 13.1 The instrument numbers

| Instrument | Verified quantity | Source |
|---|---|---|
| Heat Flow Experiment | thermal gradient **1.5–2.0 K/m**, heat flow **~17 mW/m²**; deployed successfully on **Apollo 15 and Apollo 17 only**; Apollo 16 drilled a 3 m borehole but John Young tripped over the connecting cable and the experiment was inoperable; Apollo 13's was lost with the abort | *Wikipedia, "Heat Flow Experiment"* |
| HFE geometry | probes in two 50 cm sections, gradient thermometers at **28 and 47 cm** from each end, four measurement points per section, cable thermocouples at 0/65/115/165 cm; heater settings **0.002 W and 0.5 W** for conductivity sounding | ditto |
| HFE physics | at lunation noon **70% of heat transfer in the top few cm is radiative**; below 2–3 cm density rises from 1.1–1.2 to **1.75–2.1 g/cc**, raising conductivity | ditto |
| Seismic network | four stations (Apollo 12/14/15/16) "functioned perfectly until they were switched off in 1977"; **28 shallow moonquakes** in 1972–77; shallow events to **mB = 5.5**; deep events ~700 km down, probably tidal; shaking from a shallow event "can last for up to an hour" | *Wikipedia, "Moonquake"* |
| EASEP sensitivity | Apollo 11's seismometer "was sensitive enough to detect Neil Armstrong's movements during sleep" | *Wikipedia, "ALSEP"* |
| Duty cycle | Apollo 12 landed 19 Nov 1969 (day-of-year 323); ALSEP shut off 30 Sep 1977 → **7.87 years** (2,872 days) of continuous unattended coverage for Apollo 12's own instrument; **5.8 years** for the four-station network era, 1972–77, which is the window over which the 28 shallow events were logged | computed (§13.1) |

**Derived, not retrieved:** Fourier's law applied to the measured pair gives a regolith thermal conductivity of **k = q/(dT/dz) = 8.5–11.3 mW/(m·K)**, central **9.7 mW/(m·K)**. For scale only: intact rock conducts at 1.36–4.5 W/(m·K) depending on lithology (**verified in the fifth pass, §14.5**: Stephens Basalt 1.36–1.92; Barre Granite 2.1–2.8 dry, to 4.5 at 5 kbar; marble 2.07–2.94) — so loose regolith is two to three orders of magnitude less conductive than solid rock (the precise ratio, now verified in §14.5, is 140×–460× — an earlier draft said "about 300×", which is fair for granite alone but not across the measured igneous range), which is what a granular powder with point contacts should be. *(Qualification, because the obvious inference is over-reach: the measured 70% radiative share applies only to the top few centimetres at noon, whereas the derived k is a bulk value over the whole probe depth, so the radiative share cannot be named as* **the** *mechanism for k itself.)* Applied over the lunar surface (4πR² = 3.79 × 10¹³ m²), q = 17 mW/m² gives a **global lunar heat output of 6.4 × 10¹¹ W (645 GW)**. Flagged: the Earth comparison used only as a scale check (Earth ~47 TW, ~8 × 10⁻¹² W/kg vs the Moon's 8.8 × 10⁻¹² W/kg) is **not verified in this session** and is not load-bearing.

**One correction of an over-reading, which the arithmetic forces.** The source says the measurement "would imply temperatures that would be relatively close to melting at depths of around 300 km." A *linear* extrapolation of the surface gradient to 300 km gives **4.5–6.0 × 10⁵ K** — about **300× above** the ~1,500 K at which mantle silicates melt, i.e. **three** orders of magnitude. The deep temperature is therefore a *modelled* result built on the heat flux and the seismic/magnetic structure, not a consequence of the shallow gradient. This is stated because it is the one place where the source's own phrasing invites over-reading: what HFE measured is the shallow gradient and the flux; the deep profile comes from elsewhere.

**Why this is a decisive test for claim (b).** Under the staging hypothesis, nothing went to the Moon, so everything the programme *left there* must have been delivered robotically and have gone on reporting, unprompted, for years. Scoped to Apollo only — the Lunokhod and Chandrayaan-3 arrays are independent hardware and are not the hoax's burden; the correct statement (as §1 (b) already says) is that a faked Apollo would have had to *coexist* with them, not to place them — that means: **three** retroreflectors still returning pulses; five autonomous radioisotope-powered ALSEPs plus EASEP, still received by a Soviet telescope in late 1977; four seismometers that logged 28 moonquakes nobody had predicted; two heat-flow stations that produced a self-consistent 17 mW/m²; and 381 kg of sample. This is a **comparative engineering judgement, not a proof**: it says the fake requires more capability than the landing it exists to deny, and a programme able to do all of that robotically in 1969–73 could have landed a man.

### 13.2 The Roswell chronology check, and the reversal of an earlier "retraction"

Two things were verified live in this session.

**(a) The Luna 16 retraction was my error, and is reversed.** §10.0 item 1 recorded that the 101 g figure and the "close resemblance to Apollo 12 soil" statement had been removed because "the retrieved text does not contain them." That was a statement about a truncated extract, not about the article. Re-fetched, both are present verbatim: *"The 101 grams (3.56 ounces) sample was returned from Mare Fecunditatis"* and *"Analysis of the dark basalt material indicated a close resemblance to soil recovered by the American Apollo 12 mission."* Both are reinstated. Recorded plainly: **of the four corrections documented in this report's history, two were errors in my own provenance checking rather than in the record**, which is a warning about how to read the rest of it.

**(b) The "memory metal" claim fails on chronology, but not for the reason usually given.** Verified, *Wikipedia, "Nickel titanium"*: the shape-memory effect "was discovered in 1932, when Swedish chemist Arne Ölander observed the property in gold–cadmium alloys. The same effect was observed in Cu–Zn (brass) in the early 1950s"; nitinol itself was created at the Naval Ordnance Laboratory in 1961–62. Verified, *Wikipedia, "Roswell incident"*: Jesse Marcel described "a foil that could be crumpled but would uncrumple when released" in his **1978–1980** interviews, not in 1947.

So the correct statement is *not* that memory metal was an anachronism in 1947 — it was not, since Ölander's 1932 observation precedes Roswell by 15 years and nitinol precedes Marcel's account by 16. The correct statement is narrower and stronger: **a shape-memory alloy is a martensitic solid-state phase transformation in an ordinary terrestrial alloy, documented decades before Roswell, and therefore cannot be evidence of extraterrestrial origin.** A thin metallised polymer foil also appears to "unfold" when released. The burden on the claimant is to identify what *was* anomalous about the material; no specimen survives to characterise, so that burden has never been carried. The claim fails on absence of evidence, not on physical impossibility — the opposite of how it is usually argued.

Also verified this session, and worth recording because it is quantitative and pre-dates the legend: the Mogul train's **own radio tracking** put its last contact "within 17 miles (27 km) of the ranch managed by W. W. 'Mac' Brazel near Corona, New Mexico." Computed here: the great-circle distance from Alamogordo AAF to Corona is **162 km**, initial bearing **16.4°** (almost due north), which over the **31 days** from launch (4 June) to Brazel's reaching Corona on 5 July 1947 is a mean drift of **5.2 km/day**. **Honest limits, stated in full:** (i) I did not retrieve the June 1947 upper-air wind field, so I do **not** claim the trajectory is wind-consistent — a constant-altitude balloon's drift is set by the wind and is commonly *tens* of km/day, and no figure for that is asserted here from any source; (ii) the divisor is wrong in the conservative direction, since 5 July is when Brazel reached Corona, not when the debris arrived, so the true drift window is shorter and the implied rate larger; (iii) Corona is a proxy for the ranch and both coordinates are approximate to ~10 km. What the arithmetic does establish is that the displacement required, ~160 km, is of the order balloons actually achieve, and that no one has ever shown "no balloon could have done this."

The load-bearing fact is different and is the USAF's own: the balloon train's **last known position, from its own radio tracking, was 27 km from the spot where the debris was later found.** That is a specific, pre-1978, quantitative prediction the Mogul account makes about a document that already existed in 1947.

### 13.3 What the fourth pass changed

| Claim | Change |
|---|---|
| (b) Moon landing faked | **strengthened.** The seismic and heat-flow instruments the brief names now carry numbers, and both give derived quantities computed from the measurements. The hoax hypothesis now faces a *comparative engineering* problem: the robotic delivery it would require exceeds the crewed capability it denies. |
| (b) independent corroboration | **one reinstatement.** Luna 16's 101 g and its Apollo 12 resemblance are once again asserted, this time verified verbatim. |
| (c2) Roswell | **one new modest point.** The "memory metal" motif is not an anachronism (the effect predates Roswell), and so is *not* evidence of extraterrestrial origin on chronology grounds; and the balloon's last tracked position was 27 km from the find site. |
| (a), (c1), (d) | unchanged. |

### 13.4 Independent audit of this pass, and the seven defects it removed

An earlier pass of this report found two overstatements of its own by checking (§10.5), so the fourth pass was audited the same way by a separate read-only reviewer, which re-derived every chain independently. **It found seven defects. All seven were real and all seven are now fixed in the text above; the fixes are listed rather than quietly applied.**

1. **A numerical error of my own.** The Apollo 12 seismic duty cycle was computed with 19 Nov 1969 entered as day-of-year **357** when it is **323**, making the interval 34 days short. Corrected from 7.77 yr / 2,836 days to **7.87 yr / 2,872 days**, and the four-station network era (5.8 yr) is now given separately, because "the four stations ran 7.87 years" is false — Apollo 14/15/16 arrived in 1971–72.
2. **An inflated multiplier.** "Unphysical by four orders of magnitude" for the 4.5–6.0 × 10⁵ K extrapolation is ~300×, i.e. **three** orders. Corrected. This was exactly the kind of self-flattering rounding the report exists to police.
3. **An unsourced scale claim.** "A few km/day … the ordinary scale of a constant-altitude balloon's drift" — no source, and wrong: stratospheric balloons drift at wind speed, commonly tens of km/day. Removed and replaced with an explicit statement of what the arithmetic does *not* establish.
4. **A silently dropped caveat.** The script flagged the "2–4 W/(m·K) intact igneous rock" figure as *not verified*; the report had dropped the flag while keeping the 300× ratio. The flag is restored, and the mechanism claim is qualified, because the measured 70% radiative share applies to the top centimetres at noon, not to the bulk conductivity it was being used to explain.
5. **A conflation.** The hoax-burden paragraph listed *six* retroreflectors "from three nations" as things the Apollo staging hypothesis had to place. Lunokhod's and Chandrayaan-3's are independent hardware; a faked Apollo must *coexist* with them. Scoped to the three Apollo arrays.
6. **A framing regression.** §13.3 had summarised the memory-metal point as "fails on chronology," reintroducing the anachronism framing that §13.2 itself shows to be invalid. Reworded.
7. **Two stale cross-references and one stale caveat.** A pointer to a non-existent §10.6; a "derived (§13.2)" label on a derivation that is in §13.1; and §11 (b) still asserting the "≥300× in timing" exclusion as hard, which §10.1 and §10.5 had already downgraded to a supporting point. All three reverted to match the corrected text.

The pattern worth recording: **five of the seven were mine, not the sources', and two of them (3 and 7) were introduced by this very pass while fixing two others.** A report that audits itself is not thereby clean — but the error rate does fall when each result is re-checked against the arithmetic rather than the narrative, and that is the only defence this document has.

---

## 14. Fifth pass — `derivation5.py` (2026-10-06): a missing class of test for claim (a), and the two figures pass 4 left unverified

The brief names ten decisive tests for flat Earth, and passes 1–4 executed or derived all ten. But re-reading the steelman, one whole *class* of evidence was absent. The flat model does not merely place the Earth in the wrong shape — in the form stated in §2.1 it puts **the stars on a nearby inner surface of a "dome"** and asserts the Earth is **stationary**. Both of those are directly measurable, by the oldest quantitative astronomy there is, and neither had been tested here. This pass adds them. It also closes the two figures pass 4 explicitly flagged as "not verified in this session" (§13.1). Full script output is in `scratch/derivation5.out`; script is `scratch/derivation5.py`.

### 14.1 Stellar parallax — a direct geometric measurement that the Earth moves

The parallax of a star is π = *a*/*d*, where *a* is the baseline. The only baseline the flat model admits is the Earth's own radius (6,371 km) or nothing at all, because the plane is **stationary**; the measured baseline is **1 AU = 149,597,870.7 km** (IAU), because the Earth orbits the Sun. The two differ by a factor of ~2.3 × 10⁴ before distances are considered.

Verified input (V), *Wikipedia, "Proxima Centauri"*, body, citing **Gaia Data Release 3 (2020)**: "Based on a parallax of **768.0665 ± 0.0499 mas** … Proxima Centauri is 4.2465 ly (1.3020 pc) from the Sun." The measured annual parallax is therefore **0.768 arcsec**, quoted directly rather than inverted from the article's rounded lead. (The article's lead rounds to "4.25 light-years (1.3 parsecs)"; an earlier draft of this pass inverted that rounded figure to 0.7692″ and then built a "the two verified expressions differ by 0.23%" note — the 0.23% was an artefact of the rounding, not a measurement, and is now dropped.)

| Dome altitude (as quoted in the flat-Earth literature) | Dome distance | Predicted annual parallax — **for every star** | Excess over the measured 0.768″ |
|---|---|---|---|
| 1,000 mi | 1,609 km | 1.92 × 10¹⁰″ | **2.5 × 10¹⁰ ×** |
| 3,000 mi (Rowbotham) | 4,828 km | 6.39 × 10⁹″ | **8.3 × 10⁹ ×** |
| 5,000 mi | 8,047 km | 3.84 × 10⁹″ | **5.0 × 10⁹ ×** |
| 7,000 mi | 11,265 km | 2.74 × 10⁹″ | **3.6 × 10⁹ ×** |
| 10,000 mi | 16,093 km | 1.92 × 10⁹″ | **2.5 × 10⁹ ×** |

The smallest tabulated excess is 2.50 × 10⁹ = 10⁹·⁴, so the exclusion is **~9 to 10.4 orders of magnitude in angle** — a figure computed from the table, not asserted.

Four things make this decisive, and it is worth separating them:

1. **A dome makes the same prediction for every star.** On a single shell at one distance, all stars share essentially one *d*, so all of them would show the **same** ~10⁹–10¹⁰-arcsec annual swing. What is measured: **0.768 arcsec for the nearest star**, a few tenths of an arcsecond for its nearest companions (α Centauri ~0.75″, Barnard's Star ~0.55″, Sirius ~0.38″), and vastly below 0.01″ for the overwhelming majority of catalogued stars — **every** real parallax sits 6 to 10 orders of magnitude below the dome's prediction.
2. **No choice of dome altitude rescues it.** 1,000 mi and 10,000 mi fail by the same margin. This is the property that distinguishes it from §2.3a Tests 1–3, which each depend on a model parameter.
3. **Matching the measurement requires the dome to be 4.01 × 10¹³ km away** — 8.3 × 10⁹ times the 3,000-mile figure, i.e. 1.30 pc. At that point the model is no longer a flat one; it is the measured universe.
4. **The decisive logical form is positive, not merely inconsistent.** A stationary plane has baseline zero, so it predicts **exactly zero** annual parallax for every star. Measured parallax is *positive* — 0.768″ — so it is a direct geometric measurement that the Earth is displaced between the two six-month-apart viewpoints. Precisely stated, because an earlier draft got it wrong by a factor of two: the **conventional** parallax *π* = *a*/*d* uses the **1 AU** baseline (that is the parsec definition), while the two viewpoints that produce the annual swing are separated by the orbit's **diameter**, 2*a* = **2 AU**. Every earlier test in §2 contradicted the flat model; this one measures the thing the flat model denies.

### 14.2 Stellar aberration — the same orbit, measured a second and independent way

Verified input (V), *Wikipedia, "Aberration (astronomy)"*: the apparent position of a star "varies periodically over the course of a year as the Earth's velocity changes as it revolves around the Sun, by a maximum angle of approximately 20 arcseconds," an effect of order *v*/*c*.

| Quantity | Value |
|---|---|
| Earth mean orbital speed (quoted) | 29.780 km/s → κ = *v*/*c* = 9.9335 × 10⁻⁵ rad = **20.489 arcsec** |
| Same, computed here from 2π·AU/yr | 29.785 km/s → **20.493 arcsec** |
| Observed | "approximately 20 arcseconds"; classical constant ≈ 20.5″ |
| Annual Doppler signature of the same speed | Δλ/λ = 9.93 × 10⁻⁵ → **±0.0497 nm at 500 nm** (±0.50 Å) |

The two tests separate cleanly, which is what makes them jointly strong: **aberration depends only on the observer's velocity and not on the star's distance**, whereas **parallax depends only on baseline and distance**. Aberration runs in phase with the orbit and 90° out of phase with parallax, so it cannot be an artefact of the same geometry. Either alone refutes a stationary plane. Together they measure the orbit twice. The Doppler signature is a third, independent measurement of the same 29.78 km/s.

**Honest limit on the comparison:** the source states the observation in round numbers ("approximately 20 arcseconds"), so this is a "predicted 20.49 against an observation quoted as about 20" agreement — a two-significant-figure prediction, not a 0.1% test. Its force is that a stationary Earth predicts aberration to be **exactly zero**, and ~20″ is measured.

### 14.3 Why this strengthens rather than merely adds

Passes 1–4 refuted flat Earth by **inconsistency**: every model prediction (2.2–2.4× southern route lengths, ~186 excess days of South-Pole daylight, a setting Sun 4.26× too small) failed against routinely published data. That is decisive but defensive. §14.1 and §14.2 are different in kind: they are **positive measurements of Earth's orbital motion** that the flat model must deny outright. Verdict for (a) is unchanged at **>99.9%**; what changes is that the steelman can no longer be answered only by "the institutional conspiracy explains the observations" — parallax and aberration are measured by ordinary observatories, on stars nobody is alleged to have faked, and they are exactly zero on a stationary plane.

### 14.4 Stellar angular size at dome distance — **supporting, not load-bearing**

Verified (V), *Wikipedia, "Betelgeuse"*: Michelson measured the angular diameter at **0.047 arcsec** for a uniform disk (limb darkening would raise it to 0.055″); the article gives a radius of ~640 R☉ and a distance of **125 pc** (which the body converts to 410 ly). At a 3,000-mile dome, a 0.047″ disc would be a sphere of **radius 0.55 m**; at 7,000 mi, 1.28 m. Cross-check that the verified numbers are mutually consistent: θ and R together imply *d* = 3.91 × 10¹⁵ km = **127 pc**, which reproduces the article's own 125 pc to **1.3%** — so both measurements are real, and they describe a star hundreds of parsecs away, not a metre-scale lamp.

*Provenance flag:* the article carries parallax 5.95 mas (= 168 pc) alongside 125 pc — a **34%** internal inconsistency in the source. It does not bear on this argument, since 125 pc = 3.86 × 10¹⁵ km against a 10,000-mile dome at 1.61 × 10⁴ km is a factor of **2.4 × 10¹¹**, i.e. 10¹¹·⁴ to 10¹²·⁴ times further depending on the dome altitude. (An earlier draft wrote "~10¹³ times further," which is high by one to two orders of magnitude; corrected here.) *Label:* supporting, because it assumes the interferometric angular diameters are real, which a dome modeller can deny at some cost in other physics. §14.1 and §14.2 carry the exclusion.

### 14.5 The two figures pass 4 flagged "not verified in this session" — now verified

**(a) Intact-rock thermal conductivity.** Pass 4 asserted "2–4 W/(m·K)" for intact igneous rock and "about 300× less conductive" than the derived regolith value, and flagged the figure as unverified. Verified this session from *Wikipedia, "List of thermal conductivities"*:

| Rock | k (W/(m·K)) | Ratio vs regolith (9.7 mW/(m·K)) |
|---|---|---|
| Stephens Basalt (NTS samples) | 1.36–1.92 | 140×–198× |
| Barre Granite, dry, 50 bar | 2.1–2.8 | 216×–289× |
| Barre Granite, all pressures to 5,000 bar | 2.1–4.5 | 216×–464× |
| Marble | 2.07–2.94 | 213×–303× |

**Finding:** pass 4's band was defensible for granite (206–412×, so "~300×" is fair *inside* that band), but basalt — the closest lunar analogue — measures 1.36–1.92, so the honest range across all listed rock is roughly **140×–460×**. Restated as **two to three orders of magnitude**, not "about 300×." Conclusion unchanged, and the mechanism caveat from §13.1 (the measured 70% radiative share applies to the top few centimetres at noon, not to the bulk conductivity) still stands. *Provenance note:* the first draft of this pass included an "Indiana Limestone 0.62–1.33" row; the source table's wikitext is ambiguous at that point, with two different ranges sitting in adjacent cells, so the row has been **dropped rather than guessed at**. It is sedimentary, a poor lunar analogue, and its removal does not change the igneous conclusion.

**(b) Earth's specific heat output.** Verified (V), *Wikipedia, "Earth's internal heat budget"*: "estimated at **47 ± 2** terawatts," with estimates spanning 43–49 TW. This gives a mean surface flux of **92.1 mW/m²** (the article states 91.6 mW/m² — agrees) and a specific output of **7.87 × 10⁻¹² W/kg** (range 7.2–8.2 × 10⁻¹²). Pass 4's Moon figure of 8.8 × 10⁻¹² W/kg is confirmed at 8.71 × 10⁻¹², and pass 4's "~8 × 10⁻¹²" for Earth is correct to that precision. The Earth/Moon ratio is 0.90 — same order of magnitude. Both figures are scale checks and remain non-load-bearing, as pass 4 said. **Correction to pass 4:** the ±2 TW uncertainty was omitted there and is now stated.

### 14.6 What the fifth pass changed, and what it did not

| Item | Change |
|---|---|
| (a) Flat Earth | **strengthened, in kind not in degree.** Two positive measurements of Earth's orbital motion (annual parallax 0.768″; annual aberration ~20″) added, both excluding the stationary-plane and nearby-dome claims by ~9–10.4 orders of magnitude, and both robust to every model parameter. Verdict unchanged at >99.9%. |
| (a) test list | now 12 independent classes of measurement rather than 10. |
| (b) Moon landing | two scale figures verified; the regolith conductivity statement restated as a range. No change to the verdict. |
| (c1), (c2), (c2′), (d) | untouched. Their arithmetic was computed and independently audited in passes 3 and 4, and nothing here bears on it. |

**Three defects of my own, found while verifying this pass and fixed before this text was finalised**, recorded because the pattern of this report is that errors are found by checking and not by confidence: (i) the aberration comparison was first written as "agreement 102.4%", which is meaningless — the source states the observation in round numbers, so the honest statement is "predicted 20.49 arcsec against an observation quoted as about 20 arcseconds, in a quantity a stationary Earth must predict to be exactly zero"; (ii) a `%`-format placeholder was left uninterpolated in the Earth/Moon ratio line, and two further `%%` literals printed as literal percent signs; (iii) the Betelgeuse block was first written with a 0.05″ angular diameter and an unverified "~168 pc" distance, both from memory — re-fetched, the measured value is 0.047″ (uniform disk; 0.055″ limb-darkened) with the article's own distance at 408 ly, which the θ-and-R cross-check reproduces to 1.2%. All three were caught by re-reading the script's own output rather than its source.

### 14.7 Independent audit of this pass, and the four errors it removed

This pass was audited the same way as passes 3 and 4, by a separate read-only reviewer that re-derived every chain from scratch and re-fetched every "verified input" live. **It found ten defects. Four were errors of mine; all are now fixed in the text above, and the fixes are listed rather than quietly applied.**

| # | Defect | Fix |
|---|---|---|
| 1 | **Numerical, the most serious.** §14.4 and the script both said Betelgeuse's distance is "~10¹³ times further than any proposed dome altitude." The true ratio is 125 pc (3.86 × 10¹⁵ km) against a 1,609–16,093 km dome = 2.4 × 10¹¹–2.4 × 10¹², i.e. **10¹¹·⁴–10¹²·⁴** — high by one to two orders of magnitude, the same "orders of magnitude off" class as §13.4 item 2. | Corrected, with the computation now printed in the script. |
| 2 | **Numerical and self-contradictory, in the headline sentence.** §14.1 point 4 said the Earth "moves a distance 2*a* = 1 AU over six months." §14.1's own first paragraph defines *a* = 1 AU, so 2*a* = 2 AU — a factor-of-2 error against the section's own definition. | Corrected: the conventional parallax uses the 1 AU baseline (the parsec definition); the two six-month-apart viewpoints are separated by the orbit's diameter, 2 AU. |
| 3 | **Overstated.** §14.1 point 1 said "<0.01 arcsec for every other star in the sky." False: α Centauri ≈ 0.75″, Barnard's Star ≈ 0.55″, Sirius ≈ 0.38″, and thousands of catalogued stars within 100 pc exceed 0.01″. | Softened to the accurate statement, which carries the argument unchanged. |
| 4 | **Provenance mismatch.** The script asserted Indiana Limestone at 0.62–1.33 W/(m·K); the source table's wikitext is ambiguous at that point, with two different ranges in adjacent cells. | Row **dropped rather than guessed at**. The igneous conclusion is unaffected. |
| 5 | Minor: "35% internal inconsistency" for Betelgeuse's 125 pc vs 168 pc is 34.4% on the 125 pc base. | Corrected to 34%. |
| 6 | Minor: "8–10 orders of magnitude" was asserted, not computed; the smallest tabulated excess is 2.50 × 10⁹ = 10⁹·⁴. | Restated as **~9–10.4 orders**, with the computation printed. |
| 7 | Minor: the aberration comparison was framed as "agreement to better than 3%," which only clears 3% because 20.49 falls within one rounding unit of the round-number observation. | Already downgraded in §14.2 to a two-significant-figure prediction; no further change. |
| 8 | **Internal inconsistency introduced by this pass's own edits.** The §7 source list was extended with fifth-pass entries numbered **19–23**, but the pre-existing "Historical / documentary sources" block *also* started at **19**, so two different sources shared each key 19–23. | The historical and later blocks are renumbered **24–43**, restoring a unique key per source. |
| 9 | **Internal inconsistency.** §14.5 restated the regolith conductivity comparison as a range, but §13.1 — the evidence section, which this pass had not edited — still carried the superseded round "about 300×." | §13.1 now states the verified 140×–460× range. |
| 10 | Minor: a dangling "see source 36" pointer in §7 item 3 (the list ended at 27 before this pass's renumbering), and the lunar heat output was given as 645 GW in two places and 640 GW in this pass. | Pointer redirected to §13.2(a); the figure standardised at 6.4 × 10¹¹ W = **640 GW**. |

**One strengthening the audit prompted.** The pass had *inverted* the Proxima Centauri article's rounded lead ("4.25 light-years (1.3 parsecs)") to obtain 0.7692″, and had then built a note that "the two verified expressions differ by 0.23%." The audit pointed out that the article's body states the parallax directly — "Based on a parallax of **768.0665 ± 0.0499 mas**, published in 2020 in Gaia Data Release 3, Proxima Centauri is 4.2465 ly (1.3020 pc) from the Sun." The decisive input is therefore now **quoted rather than derived**, the 0.23% note is dropped as an artefact of rounding, and the measured parallax is 0.768″.

**The running tally, recorded because it is the only real measure of how much to trust the rest.** Across five passes, **eighteen defects** have been found and fixed: two unsourced assertions in pass 1, two overstatements of mine in pass 3, seven in pass 4 (five of them mine, two introduced by that pass while fixing the others), three found by me while writing this pass, and four found by its audit. All eighteen were errors of this report's own construction rather than misreadings of the sources, and almost all were numerical, provenance, or overstatement errors caught only by re-deriving the arithmetic against the source text; **none was caught by re-reading the prose alone.** The conclusion this report draws from its own history is narrow and worth stating plainly: a document that audits itself is not thereby clean, and the only defence is re-derivation.

---

---

## 16. Sixth pass — `derivation6.py` (2026-10-06): a thirteenth class of test for (a), a new test for (b), the Mogul trajectory computed at last, and the Blue-Book base rate for (d)

Four things were still missing from the report as pass 5 left it, and each is now closed or explicitly framed. Full script output is in `scratch/derivation6.out`; script is `scratch/derivation6.py`.

### 16.1 Claim (a): rotation measured by *relativistic* means — Sagnac, ring interferometry, and the rotation correction every GNSS receiver must apply

Passes 1–5 refuted flat Earth by internal inconsistency and by two positive measurements of Earth's *orbital* motion (§14). One class of measurement was still absent. Every existing rotation test in this report is either **dynamical** (Foucault pendulum, gravity, the south-polar day length) or **gravitational/orbital** (Kepler's third law on GPS, §2.3a Test 3). A Sagnac-interference measurement is neither: it depends only on the constancy of *c* and the geometry of a rotating frame. That makes it a genuinely independent class, and it has a second property no other test here has — **it is an engineering necessity in every operating navigation system**, so it is not a laboratory curiosity that can be waved away.

**New verified facts (all verbatim from *Wikipedia, "Sagnac effect"*):**

- **Michelson–Gale–Pearson, 1926** — "a very large ring interferometer, (a perimeter of 1.9 kilometer), large enough to detect the angular velocity of the Earth … The measured shift was **230 parts in 1000, with an accuracy of 5 parts in 1000. The predicted shift was 237 parts in 1000**." So measured/predicted = **0.9705 ± 0.0211**, a residual of **1.40σ**, consistent. The *stationary-Earth* prediction is **0 parts in 1000** — which the measurement excludes by |230 − 0|/5 = **46 standard deviations**, using a 1926 interferometer with no external calibration.
- **The around-the-world relay** — "the amount of time difference between the clocks when they arrive back at the starting point will be equal to the time difference that is found for a relay of pulses that travels around the world: **207 nanoseconds**."
- **The 1984 direct verification** — "A relay of pulses that circumnavigates the Earth … In 1984 a verification was set up that involved **three ground stations and several GPS satellites**, with relays of signals both going eastward and westward around the world."
- **GNSS** — "Global navigation satellite systems (GNSSs) — such as GPS, GLONASS, COMPASS or Galileo — **need to take the rotation of the Earth into account** in the procedures of using radio signals to synchronize clocks."
- **Ring lasers** — "Ring laser interferometers are **self-calibrating**. The beat frequency will be **zero if and only if the ring laser setup is non-rotating** with respect to inertial space," and "The ring laser also can detect the sidereal day, which can also be termed 'mode 1'."

**Computed here from first principles, with no fitted parameter:**

| Quantity | Formula | Result | Verified value |
|---|---|---|---|
| One-way Sagnac delay, equatorial great circle | Δ*t* = 2*A*Ω/*c*², *A* = π*R*²_eq = 1.2780 × 10¹⁴ m² | **207.4 ns = 62.17 m** of light travel | **207 ns** → 0.19% agreement |
| Sagnac delay at 45° latitude | × cos φ | 146.6 ns | — |
| Maximum GNSS Sagnac term | Δ*t* = (2/*c*²)Ω(*x*_s*y*_g − *y*_s*x*_g) ≤ (2/*c*²)Ω*r*_s*r*_g, with *r*_s = 26,560 km (the value §2.3a derives from Kepler's third law) and *r*_g = 6,371 km | **274.6 ns = 82.3 m** of light travel | stationary plane: **exactly 0** |
| Ground station's own motion during a GPS transit (88.6 ms) | Ω*R*t* | **41.2 m**; rotation angle **0.006 mrad = 1.33 arcsec** | — |

**Verdict: unchanged at >99.9%.** This is the thirteenth independent class of measurement, and it is the first in the report that is neither dynamical nor gravitational. It also closes the one gap the §2.3a Test 3 caveat had left open: Test 3 is conditional on inverse-square gravitation about a central mass, and §16.1 is not.

### 16.2 Claim (b): the laser return is **coordinate-dependent** — a test the report had not run

Section 10.1 already excluded the bare-lunar-surface alternative by **≥50× in photon flux** and **≥300× in timing width**. That is a flux and a timing test. There is a third, cheaper, independent one that had not been used, resting on verified 2010–2013 observations:

- *Wikipedia, "Lunokhod 1"*: "**The final location of Lunokhod 1 was uncertain until 2010, as lunar laser ranging experiments had failed to detect a return signal from it since 1971.**" "**On March 17, 2010, Albert Abdrakhimov found both the lander and the rover in Lunar Reconnaissance Orbiter (LRO) image M114185541RC (Line 21977, Sample 3189).**" "In April 2010, the Apache Point Observatory Lunar Laser-ranging Operation (APOLLO) team from the University of California at San Diego **used the LRO images to locate the rover closely enough for laser range** … On April 22, 2010, and days following, the team successfully measured the distance several times." Tom Murphy (NASA press release): "**We got about 2,000 photons from Lunokhod 1 on our first try. After almost 40 years of silence, this rover still has a lot to say.**" "**The intersection of the spheres described by the measured distances then pinpointed the current location of Lunokhod 1 to within 1 meter.**" "By November 2010, the location of the rover had been determined to within about a centimeter." And, replicated: "In a report released in May 2013, French scientists at the Côte d'Azur Observatory … reported replicating the 2010 laser ranging experiments … **laser pulses were returned from the Lunokhod 1 retroreflector.**"

**Why this is a test and not a citation.** A diffuse return from the lunar *surface* is not coordinate-dependent: it does not care where a rover is parked. The behaviour observed here is: **silence for 39 years at western stations despite a published approximate location, followed by ~2,000 photons on the first shot after an orbital image fixed the coordinate.** That is the signature of a *small discrete object* at a *specific coordinate* — precisely what six retroreflector arrays at six independently published coordinates are, and precisely what a surface is not.

**Supporting scale computations (this pass):**

| Quantity | Value |
|---|---|
| Verified 6.5 km beam at the Moon → divergence | **1.688 × 10⁻⁵ rad = 3.48 arcsec** |
| Diffraction limit of the 3.1 m Lick telescope at ruby 694.3 nm, 2λ/*D* | **4.48 × 10⁻⁷ rad = 172 m in diameter** at the Moon |
| Ratio | the reported beam is **38× wider** than the telescope can in principle deliver → **1,421× more area, 1,421× fewer photons per m²** — exactly what a seeing-limited, pre-adaptive-optics beam looks like |
| Array as a fraction of the illuminated area | Apollo 11/14 (0.46 × 0.46 m) **3.2 × 10⁻⁹**; Apollo 15 (1.05 × 0.64 m) **1.0 × 10⁻⁸**; Lunokhod (0.44 × 0.19 m) **1.3 × 10⁻⁹**; Chandrayaan-3 (single 5.11 cm) **3.1 × 10⁻¹¹** |

**Consistency note, flagged because an earlier draft of this pass got it wrong.** §10.1's "~1–5 photons returned" is the *ruby-era* return from the Apollo 11 array through a 6.5 km beam at a 3.1 m telescope. The "~2,000 photons on our first try" is APOLLO — a 3.5 m telescope, adaptive optics, ~100 ps pulses, better detectors, pointing at a different array. These are not the same measurement and they do not contradict each other; **the direction of the change is itself evidence** that the return is beam-divergence-limited, which is what a discrete array predicts and a diffuse surface does not.

**Verdict: unchanged at >99.9%.** One additional positive fact for the table: *Wikipedia, "Lunar Laser Ranging experiments"* confirms that "**Lunokhod 2's array continues to return signals to Earth**," that the Apollo 15 array is "three times the size" of the Apollo 11/14 arrays and "was the target of three-quarters of the sample measurements taken in the first 25 years," and that "Laser ranging measurements can also be made with retroreflectors installed on Moon-orbiting satellites such as the LRO."

### 16.3 Claim (c2): the Mogul trajectory — pass 4's open item, now a computed number

Pass 4 left this open and said so: "The Mogul trajectory was never shown wind-consistent … because the June 1947 upper-air wind field was never retrieved." It is now a number, though it is still not *closed*.

**Coordinates verified live via the Wikipedia API (`prop=coordinates`):** Alamogordo, NM **32.856111° N, 105.974444° W** (launch site — "researchers at Alamogordo Army Air Field"); Corona, NM **34.247778° N, 105.596944° W** (find vicinity); Roswell, NM 33.3942° N, 104.5228° W (RAAF, the reporting base).

**Great-circle (WGS-84 mean radius), computed here:** Alamogordo → Corona **158.7 km**, initial bearing **12.6° E of N**; Alamogordo → Roswell **147.8 km**. *Caveat:* Corona is the nearest gazetted town to the Brazel ranch, which lies a few km further NE, so **158.7 km is a lower bound** on the required launch-to-find displacement.

**The load-bearing verified fact, verbatim:** "On June 4, researchers at Alamogordo Army Air Field in New Mexico launched a long train of these balloons; **they lost contact with the balloons and balloon-borne equipment within 17 miles (27 km) of the ranch** managed by W. W. 'Mac' Brazel near Corona, New Mexico, where a balloon array subsequently crashed." And, independently: "**Flight No. 4 was drifting toward Corona within 17 miles of Brazel's ranch when its tracking equipment failed.**"

**A constant-altitude balloon cannot aim.** Its track is the passive integral of the wind at its altitude. So the required mean drift is simply displacement ÷ time aloft:

| Time aloft *T* | Required mean drift |
|---|---|
| 1 h | 44.1 m/s |
| 3 h | 14.7 m/s |
| 6 h | 7.3 m/s |
| 12 h | 3.7 m/s |
| 24 h | 1.8 m/s |
| 48 h | 0.9 m/s |
| 168 h (1 week) | 0.3 m/s |
| 720 h (30 days) | 0.1 m/s |

In general **(158.7/*T*) km/h from the SW-SSW**. To settle it one needs the June 1947 upper-air wind field between roughly 9 and 15 km over southern New Mexico, from the radiosonde archive or a long-period reanalysis. **This session did not retrieve it, so the item remains open — but it is now a retrieval problem with a stated target rather than a vague doubt.**

**A correction of emphasis, not of fact, and I record it as such.** Pass 4 framed the risk asymmetrically, noting a "required mean drift of 5.2 km/day over 31 days." That is **0.06 m/s**, which is *slower than essentially any tropospheric or lower-stratospheric wind anywhere on Earth* — so the arithmetic actually argues for the plausibility of the balloon, not against it. What the table shows is that any flight duration between about a day and a week requires a drift of 0.3–1.8 m/s, and hours-long flights require several to tens of m/s: both are ordinary values at 9–15 km over New Mexico in June. The honest statement is therefore that **the trajectory is dynamically plausible and empirically unverified**, which is the opposite of the impression pass 4's phrasing could leave. Caveat stated plainly: the wind values just characterised are general meteorological expectations, *not* retrieved 1947 measurements.

**Debris-field geometry.** Verified verbatim: "tinfoil, rubber, tape, and thin wooden beams scattered across **several acres** of the ranch." Several acres = 3–5 acres = **12,141–20,234 m²**, an equivalent square **110–142 m** on a side. A compact impact site of a ~10 m craft would concentrate nearly all recoverable mass at one location with fragments thrown O(10 m); a field 100–140 m across containing "**no engine or metal parts**" (the 9 July 1947 *Roswell Daily Record*) is what a long balloon train shredding and dropping material over its length produces. *Caveat: the source gives the area only, not the shape or length:width ratio, so this is an argument of direction, not a precision measurement.*

**The telex's 6.1 m object, scaled.** The 8 July 1947 FBI telex: "The disc is **hexagonal in shape** and was **suspended from a balloon by cable**, which balloon was approximately **twenty feet (6.1 m) in diameter**." Treated as a superpressure sphere of volume 118.8 m³ under the standard atmosphere (altitudes assumed):

| Altitude | Gross lift | Net payload after the helium's own mass |
|---|---|---|
| 9 km | 47.8 kg | ~40 kg |
| 12 km | 31.8 kg | ~27 kg |
| 15 km | 19.8 kg | ~17 kg |

A Mogul train — balloons, a long cable train, sonobuoys, radios — is a payload of that order. A crewed interstellar vehicle carrying bodies is not. This is a scale check only; the load-bearing datum remains the USAF's own identification of the specific train and the 27 km miss.

**Base rate, verified verbatim:** "By 1947, the United States had launched **thousands** of top-secret Project Mogul balloons." Thousands of long balloon trains were aloft over the south-western United States in 1947; debris recoveries were routine. Exactly one became the Roswell legend.

### 16.4 Claim (d): the instrumented-report base rate, and two narrative-internal quantities

**Project Blue Book** (verified verbatim from *Wikipedia, "Project Blue Book"*): March 1952 – 17 December 1969, HQ Wright-Patterson AFB.

- "By the time Project Blue Book ended, it had collected **12,618 UFO reports**, and concluded that most of them were misidentifications of natural phenomena (clouds, stars, etc.) or conventional aircraft."
- "**701** reports were classified as unexplained, even after stringent analysis." → computed: **5.56% unexplained**, 94.44% identified.
- "By the time of the hearing, Blue Book had **identified and explained 95%** of the reported UFO sightings."
- The USAF's two published conclusions, verbatim: "**There has been no evidence submitted to or discovered by the Air Force that sightings categorized as 'unidentified' represent technological developments or principles beyond the range of present-day scientific knowledge**" and "**There has been no evidence indicating that sightings categorized as 'unidentified' are extraterrestrial vehicles**."
- The Condon Report "concluded that the study of UFOs was unlikely to yield major scientific discoveries," and the National Academy of Sciences endorsed the review.

**So: over 17 years, 12,618 reports, 701 left open — and none of the 701 produced physical, photographic, radar or biological evidence.** That is the quantitatively stated absence for claim (d), at the one sample size large enough to be worth quoting, and it is *absent* evidence: 701 unexplained reports is not the same as 701 *disconfirmed* ones, and this pass does not claim otherwise.

**Two narrative-internal quantities, both verified and both new here:**

1. **Hopkins' own count of "alien mistakes."** "Hopkins has estimated that these 'errors' accompany **4–5 percent** of abduction reports" — the "cosmic application of Murphy's Law": failing to return the experiencer to the same spot, or putting their clothes on backwards. An entity with interstellar transport makes mundane handling errors in **one report in 20–25**. That ratio is a property of fiction, not of engineering, and it is a *proponent's own* number.
2. **Mack interviewed "over 800 people."** The proponent with the largest clinical sample in the literature still produced no physical artefact.

**Two artefacts, actively disconfirmed rather than merely unsupported** (both verified verbatim):

- The 2017 "Kodachrome slides" of a dead alien (Jaime Maussan): "it was revealed that the slides were in fact of a **mummified Native American child discovered in 1896** and which had been on display at the **Chapin Mesa Archeological Museum in Mesa Verde, Colorado**, for many decades."
- A **c.1951** incident declassified in 2020: two Roswell personnel in "**poorly fitting radioactive suits, complete with oxygen masks, while retrieving a weather balloon after an atomic test**" met a lone woman in the desert "who fainted when she saw them"; the Air Force historian notes "they could have appeared to someone unaccustomed to then-modern gear, to be alien."

### 16.5 What the sixth pass changed

| Item | Change |
|---|---|
| **(a) Flat Earth** | **strengthened in kind, not degree.** A thirteenth independent class of measurement (relativistic rotation: 1926 ring interferometer, 207.4 ns Sagnac delay, 274.6 ns GNSS rotation correction), the first in the report that is neither dynamical nor gravitational. Verdict unchanged at **>99.9%**. |
| **(b) Moon landing** | a new decisive test — the **coordinate-dependence** of the laser return, demonstrated by Lunokhod 1's 39-year silence and 2010 re-acquisition. Two scale quantities computed (beam divergence vs. diffraction limit; array/illuminated-area ratio). An explicit consistency note on the 1–5 vs. 2,000 photon figures. Verdict unchanged. |
| **(c2) Roswell** | the pass-4 open item is now a computed, checkable trajectory (158.7 km, 12.6° E of N, (158.7/*T*) km/h); **one correction of emphasis** (the drift requirement is not implausibly slow); debris-field area converted to a linear extent; the telex's 6.1 m balloon scaled as an airship-type envelope; the thousands-of-balloons base rate quantified. Verdict unchanged at <2%. |
| **(d) Abduction** | the instrumented-report base rate quantified (12,618 / 701 = 5.56%, with zero physical evidence from the 701); two narrative-internal quantities; two newly verified disconfirmations. Verdict unchanged at >95% / >99%. |
| **(c1), (c2′)** | untouched. |

### 16.6 Independent audit of this pass, and the five defects it removed

| # | Defect | Fix |
|---|---|---|
| 1 | **Two format-string defects of exactly the class the fifth pass corrected in itself** (§14.6 item ii): a literal `%%` printed as a double percent sign, and an uninterpolated `%.1f` placeholder left inside a prose line. | Both fixed. Caught by reading the script's *output* rather than its source — the same lesson this report has now recorded three times. |
| 2 | **A real numerical bug in my own arithmetic.** The standard-atmosphere temperature lapse rate, 6.5 **K per km**, was applied to *metres*, giving T = −58,212 K and a complex pressure. | Caught by the interpreter (TypeError), fixed, and the *z* > 20 km branch added so the 9–20 km range is covered by a correct formula throughout. |
| 3 | **A conflation of beam conventions.** The draft compared the verified 6.5 km beam's *radius* against a diffraction-limited *radius* computed as λ*D*/2, mixing the two. | Standardised on diameter throughout; the surviving statement is that the 6.5 km beam is **38× wider** than diffraction, not the ~75× the draft said. |
| 4 | **An invalid error model, removed rather than defended.** The draft computed "lateral position error = σ_range × r₀/baseline" for the LLR trilateration. | That is not a valid error model for lunar laser ranging — the geometry is not a simple ratio — and publishing a false precision would have been worse than publishing none. Replaced with the geometric argument, which is what the published 1 m / 1 cm results actually are. |
| 5 | **An implicit comparison of two different instruments.** The draft risked reading "~1–5 photons" and "~2,000 photons" as the same measurement. | Split into the explicit consistency note in §16.2, which states that they are different telescopes, different arrays, different eras, and that the *direction* of the change is itself evidence for beam-divergence-limited returns. |

**The running tally, recorded because it is the only real measure of how much to trust the rest.** Across six passes: **23 defects** found and fixed — 18 through pass 5, 5 in this pass. All were errors of this report's own construction rather than misreadings of the sources; almost all were numerical, provenance, or overstatement errors; and **none was caught by re-reading the prose alone.** One was caught by the interpreter; the rest by re-deriving the arithmetic and by reading the output. The conclusion the report draws from its own history is unchanged and is stated again: a document that audits itself is not thereby clean, and the only defence is re-derivation.

---

## 17. State of the investigation — what is settled and what remains open

**Settled, to the standard the brief set.** (a) Flat Earth is false; (b) the six crewed lunar landings occurred as reported; (c1) Area 51 is a real classified USAF facility. On all three the evidence *actively disconfirms* the contrary claim rather than merely failing to support it, and on (a) and (b) the disconfirming tests are repeatable by anyone with a sextant, a camera, a mass spectrometer, or a large telescope and a pulsed laser. Thirteen independent measurement classes now bear on (a); the newest two (§14, §16.1) are *positive* measurements of Earth's orbital and rotational motion rather than internal inconsistencies of the flat model, and §16.1's is the first that is independent of both Newtonian dynamics and Newtonian gravitation.

**Not settled, and honestly not settleable on present evidence.** (c2) The 1947 Roswell debris was extraterrestrial — assessed at <2%; (c2′) bodies were recovered — the specific artefacts and witnesses offered are actively disconfirmed; (d) alien abduction is a literal physical phenomenon — not established, >95% against. In all three cases the failure is **absence of evidence plus positive refutation of the particular items offered**, not proof of a universal negative.

**Where the evidence is merely absent rather than disconfirming, stated plainly:**

1. **The classified-remnant hypothesis for Roswell.** "There is classified material we cannot see" is **unfalsifiable in principle** and cannot be excluded. What can be said is that in 79 years every artefact, witness and document offered has turned out to be a hoax, a fabrication, a fictional source, or a misattributed object. That is not proof of the negative; it is a strong signal about where the burden lies.
2. **The abduction detection premise.** The quantitative argument in §10.3 rests on the judgement that a physical abduction has at least a ~1-in-100 chance of leaving a verifiable record. That is a judgement, not a measurement, and the argument is weak for *p* ≲ 10⁻³. It does not rest on the contested 5–6% survey figures — it stands on the documented claimant count alone — but it does rest on *p*.
3. **Blue Book's 701 unexplained reports are *unexplained*, not *disconfirmed*.** They are evidence of absence (no physical trace in 12,618 investigated reports), and this report does not claim that the residual cases are positively refuted. §16.4 labels the distinction explicitly.
4. **The Mogul trajectory is still not wind-consistent — it is merely no longer untestable.** §16.3 computes the requirement (158.7 km from the SW-SSW, i.e. (158.7/*T*) km/h for a flight of *T* hours) and states what data would settle it: the June 1947 upper-air wind field between ~9 and ~15 km. This session did not retrieve it. The load-bearing fact remains the USAF's own: the train's last radio-tracked position lay **27 km from the find site**.
5. **The LLR link budget is an order-of-magnitude prediction, not a precision test.** It lands inside the observed 1–5 returned photons with no fitted parameter and brackets the observation under a sensitivity scan, but the honest strength is "right order of magnitude to within a factor of a few." Its hard exclusion of the bare-lunar-surface alternative is the 51–205× photon deficit, not the timing width.
6. **Two parameters in §16.2 are assumed, not retrieved.** The 3.5 m/532 nm beam geometry and the 50% corner-cube fill factor are (A) parameters that supply scale only; the argument itself is carried by the verified 6.5 km beam and the verified array dimensions. No station specification was retrieved in this session.
7. **Confidence numbers are subjective credences.** They are not derived from a formal prior-and-likelihood calculation and no sensitivity analysis over priors is given. The operative part of each verdict is the "what would change my mind" section that accompanies it.

**Where this report itself is weakest.** Its error rate, honestly recorded: 23 defects found across six passes and four audits, all of its own construction, almost all numerical or provenance, and **none caught by re-reading the prose alone.** Anyone using a number here should re-derive it from `scratch/derivation*.py` and re-fetch the source named in §7 rather than taking the prose on trust — which is the standard the report asks of the claims it assesses, applied to itself.

---
