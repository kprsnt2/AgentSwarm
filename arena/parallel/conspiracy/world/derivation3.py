#!/usr/bin/env python3
"""
derivation3.py -- third derivation block for "conspiracy-theories-evidence"
(Kepler, A001, generation 0; run 2026-10-06)

Purpose: close the two quantitative gaps that the first two passes left open,
each of which was flagged in the main artifact as an explicit admission.

  A. LUNAR LASER RANGING LINK BUDGET FROM FIRST PRINCIPLES.
     Claim (b) was previously supported by the *observed* fact that the
     retroreflectors return ~1-5 photons.  That is an empirical input, not a
     test.  Here the whole chain is computed -- outbound photon density at the
     Moon, interception by a 46x46 cm array, diffraction-limited retroreflection,
     telescope collection, detector quantum efficiency -- and compared with the
     observed return.  The budget is then inverted to solve for the effective
     aperture the observation requires, and the same arithmetic is applied to
     the *bare lunar surface* to show that the diffuse-return alternative is
     quantitatively excluded, in both photon flux and timing precision.

  B. SLEEP-PARALYSIS SUPPLY ARITHMETIC.
     Claim (d) rested on the base rate being "known"; here the supply is turned
     into an absolute number of episodes per year and compared with the size of
     the abductee population, so that the mundane mechanism can be seen to
     over-supply the phenomenon.

  C. THE EXPECTED-DETECTION-RATE COMPUTATION.
     The main artifact explicitly stated: "I have not computed an expected
     detection rate, so the ~95% figure it supports inherits that unquantified
     step."  This is that computation.  Under a physical-abduction hypothesis
     with n events and per-event recording probability p, P(no record at all) =
     (1-p)^n.  We solve for the p at which the observed absence stops being
     surprising, and tabulate p against n across the full range of claimant
     estimates.  The concession must be stated CONDITIONALLY ON p, not
     categorically: the silence is unsurprising for the documented n = 1,700
     only at the conservative p = 1e-3 (P = 18%); at p = 1e-2 the same n gives
     P = 4e-8.  It is therefore wrong to say the argument "carries only via the
     survey figures".  It carries on the weaker premise that any single
     physical abduction has at least a ~1-in-100 chance of leaving a record.

Inputs are: (V) verified live in this session from the sources named inline, or
(A) assumed parameters, each of which is scanned over a stated range in the
sensitivity blocks.  Nothing is fitted.
"""

import math

# ---------------------------------------------------------------------------
# VERIFIED INPUTS (retrieved live, 2026-10-06; source named per line)
# ---------------------------------------------------------------------------
C = 299792458.0            # m/s, SI exact
N_OUT = 3.0e17             # photons per pulse. LLR article: "Out of a pulse of
                           # 3x10^17 photons aimed at the reflector, only about
                           # 1-5 are received back on Earth."
BEAM_W_MOON = 6500.0       # m, beam width at the Moon's surface. LLR article:
                           # "At the Moon's surface, the beam is about 6.5
                           # kilometers (4.0 mi) wide."
D_EM = 385000.6e3          # m, mean Earth-Moon distance, centre to centre.
                           # LLR article: "averages 385,000.6 km"
N_OBS_LO, N_OBS_HI = 1.0, 5.0   # photons observed back. Same LLR sentence.
LIST_APOLLO11_PANEL = 0.46 # m, "46x46 cm" panel. Wikipedia, "List of
                           # retroreflectors on the Moon" (NASA, Apollo 11,
                           # Mare Tranquillitatis, 21 Jul 1969, Operational),
                           # citing NIST and Wagner et al. 2012 (LROC).
LIST_LUNOKHOD1_PANEL = (0.44, 0.19)  # m, "44x19 cm", Luna 17/Lunokhod 1,
                           # Mare Imbrium, 17 Nov 1970, Operational.
LIST_CHANDRAYAAN = 0.0511  # m, single reflector "5.11 cm diameter", ISRO
                           # Chandrayaan-3, Statio Shiv Shakti, 69.367621 S
                           # 32.348126 E, 23 Aug 2023, Operational.
R_MOON = 1737.4e3          # m, mean lunar radius (conventional)
R_EARTH = 6371.0088e3      # m, mean Earth radius
RRR_RESIDUAL = 0.01        # m, "Modern Lunar Laser Ranging data can be fit with
                           # a 1 cm weighted rms residual."  LLR article.
SP_LIFETIME = (0.08, 0.50) # "Between 8% to 50% of people experience sleep
                           # paralysis at some point during their lifetime."
SP_RECURRENT = 0.05        # "About 5% of people have regular episodes."
CLAIMANTS_LO, CLAIMANTS_HI = 1700, 0.055 * 8.1e9   # see section B

DASH = "-" * 74


def sect(t):
    print("\n" + "=" * 74)
    print(t)
    print("=" * 74)


# ===========================================================================
# A. THE LLR LINK BUDGET
# ===========================================================================
sect("A. Lunar laser ranging: complete link budget from first principles")

A_tel = math.pi * (3.1 / 2.0) ** 2        # 3.1 m Lick telescope (verified)
A_spot = math.pi * (BEAM_W_MOON / 2.0) ** 2
rho_ph = N_OUT / A_spot
print("VERIFIED INPUTS")
print(f"  photons emitted per pulse          N_out  = {N_OUT:.3e}")
print(f"  beam width at the Moon             b      = {BEAM_W_MOON/1000:.1f} km")
print(f"  spot area at the Moon              A_spot = {A_spot:.4e} m^2")
print(f"  mean Earth-Moon distance           D      = {D_EM/1e3:,.1f} km")
print(f"  round-trip light time              2D/c   = {2*D_EM/C*1e3:.3f} ms")
print(f"  photons observed back              {N_OBS_LO:.0f}-{N_OBS_HI:.0f}")
print(f"  fitted range residual              {RRR_RESIDUAL*100:.0f} cm weighted rms")
print(f"  Lick collecting area (D=3.1 m)     A_tel  = {A_tel:.4f} m^2")
print(f"  outbound photon density at Moon    rho    = {rho_ph:.4e} photons/m^2")

# --- assumed design parameters, each scanned below -----------------------
LAMBDA = 694.3e-9          # m, ruby laser line, the 1969 first detection
D_CUBE = 0.038             # m, corner-cube aperture, standard Apollo LRRR design
N_CUBE = 100               # Apollo 11 / Apollo 14 arrays
QE = (0.05, 0.10)          # photomultiplier quantum efficiency band at 694 nm


def retro_return_fraction(d, lam=LAMBDA, tel_d=3.1, dist=D_EM, div=1.0):
    """Fraction of photons leaving one corner cube that a telescope of
    diameter tel_d intercepts at distance dist.  Diffraction-limited
    retroreflection: the return cone half-angle is lam/d, scaled by `div`
    (a real cube's figure error and the Earth-Moon velocity aberration both
    broaden the return, so div = 1 is the optimistic limit)."""
    r_foot = (div * lam / d) * dist            # return footprint radius
    return (math.pi * (tel_d / 2.0) ** 2) / (math.pi * r_foot ** 2), r_foot


def budget(n_cube=N_CUBE, d=D_CUBE, lam=LAMBDA, tel_d=3.1,
           beam_w=BEAM_W_MOON, qe=QE[0], n_out=N_OUT, dist=D_EM, div=1.0):
    a_spot = math.pi * (beam_w / 2.0) ** 2
    n_int = (n_out / a_spot) * (n_cube * math.pi * (d / 2.0) ** 2)
    frac, r_foot = retro_return_fraction(d, lam, tel_d, dist, div)
    n_back = n_int * frac
    return n_int, n_back, n_back * qe, r_foot


n_int, n_back, n_det, r_foot = budget()
print("\nASSUMED PARAMETERS (each scanned in the sensitivity block below)")
print(f"  laser wavelength                   lambda = {LAMBDA*1e9:.1f} nm (ruby)")
print(f"  corner-cube aperture               d      = {D_CUBE*100:.1f} cm")
print(f"  cubes in the array                 N      = {N_CUBE}")
print(f"  array projected aperture           A_arr  = "
      f"{N_CUBE*math.pi*(D_CUBE/2)**2:.4f} m^2  "
      f"(vs a {LIST_APOLLO11_PANEL*100:.0f}x{LIST_APOLLO11_PANEL*100:.0f} cm "
      f"panel = {LIST_APOLLO11_PANEL**2:.4f} m^2, i.e. "
      f"{100*(N_CUBE*math.pi*(D_CUBE/2)**2)/LIST_APOLLO11_PANEL**2:.1f}% fill)")
print(f"  detector quantum efficiency        QE     = {QE[0]:.2f}-{QE[1]:.2f}")

print("\nTHE BUDGET, STEP BY STEP")
print(f"  1. photons hitting the Moon        {N_OUT:.3e} (all of them; the")
print(f"     beam is entirely on the lunar disc)")
print(f"  2. intercepted by the array        {n_int:.4e}  "
      f"= rho x A_arr, a fill factor of {n_int/N_OUT:.2e}")
print(f"  3. return footprint radius at Earth {r_foot/1000:,.2f} km "
      f"(diffraction, lam/d = {math.degrees(LAMBDA/D_CUBE)*3.6e3:.3f} arcsec)")
print(f"  4. of those, fraction into the 3.1 m telescope "
      f"{n_back/n_int:.4e}")
print(f"  5. photons arriving at the telescope {n_back:.2f}")
print(f"  6. photons DETECTED (QE={QE[0]:.2f})       {n_det:.2f}")
print(f"     photons DETECTED (QE={QE[1]:.2f})       {n_back*QE[1]:.2f}")
print(f"\n  OBSERVED: {N_OBS_LO:.0f}-{N_OBS_HI:.0f} photons back.")
print(f"  PREDICTED: {n_det:.1f}-{n_back*QE[1]:.1f} photons detected.")
print("  => No parameter of this budget was fitted to the observed return, yet")
print("     the prediction lands inside the observed range.  That is the test:")
print("     the 'the hardware is physically there' hypothesis makes a")
print("     quantitative prediction, to within the detector QE, of a number")
print("     that was measured independently in 1969 and is still measured now.")

print("\nINVERSION: what effective retroreflecting aperture does the observation")
print("require?  (n_det is linear in the array's projected aperture, so the")
print("required aperture is exact.)")
A_arr = N_CUBE * math.pi * (D_CUBE / 2.0) ** 2
print(f"\n  {'QE':>6} {'1 photon':>26} {'2 photons':>26} {'5 photons':>26}")
for qe in (0.03, 0.05, 0.10, 0.15):
    cells = []
    for target in (N_OBS_LO, 2.0, N_OBS_HI):
        _, _, nd_nom, _ = budget(qe=qe)
        a_need = target / nd_nom * A_arr
        cubes = a_need / (math.pi * (D_CUBE / 2.0) ** 2)
        cells.append(f"{a_need*1e4:6.0f} cm2 = {cubes:5.0f} cubes")
    print(f"  {qe:>6.2f} " + " ".join(f"{c:>26}" for c in cells))
print(f"\n  Reference: the physical Apollo 11 array is {N_CUBE} cubes of "
      f"{D_CUBE*100:.1f} cm aperture = {A_arr*1e4:,.0f} cm^2 of projected")
print(f"  aperture, filling {100*A_arr/LIST_APOLLO11_PANEL**2:.0f}% of the "
      f"{LIST_APOLLO11_PANEL*100:.0f}x{LIST_APOLLO11_PANEL*100:.0f} cm panel.")
print("  The observed 1-5 photons require an effective retroreflecting aperture")
print("  of order 10^2-10^3 cm^2 -- i.e. a square panel of order 10-30 cm across,")
print("  exactly the scale of a corner-cube array, and something a diffuse")
print("  surface cannot supply at all.")


print("\nSENSITIVITY: does the prediction survive the assumed parameters?")
print("  Two parameters matter most: the beam width at the Moon and the")
print("  retroreturn divergence (a real cube's figure error and the Earth-Moon")
print("  velocity aberration both broaden the return beyond the diffraction")
print("  limit).  Predicted DETECTED photons, geometric (div=1) to 4x broadened:")
print(f"\n  {'beam at Moon':>12} " + " ".join(f"{'div='+str(d):>12}" for d in (1, 2, 4, 8)))
lo_all, hi_all = 1e30, 0.0
for bw in (2e3, 4e3, BEAM_W_MOON, 10e3, 13e3):
    row = []
    for div in (1, 2, 4, 8):
        _, _, nd, _ = budget(beam_w=bw, div=div, qe=QE[1])
        row.append(nd)
        lo_all = min(lo_all, nd); hi_all = max(hi_all, nd)
    print(f"  {bw/1000:9.1f} km  " + " ".join(f"{v:12.2f}" for v in row))
print("  (upper edge of the QE band, 0.10).  Across the whole scanned space the")
print(f"  prediction spans {lo_all:.2f}-{hi_all:.0f} photons, which brackets the")
print(f"  observed {N_OBS_LO:.0f}-{N_OBS_HI:.0f}; the central estimate is "
      f"{n_det:.1f}-{n_back*QE[1]:.1f}.")
print("  The honest statement is therefore 'the right order of magnitude to")
print("  within a factor of a few', NOT an exact match.  What is exact is the")
print("  exclusion of the diffuse-surface alternative below.")

print("\nTHE ALTERNATIVE: a return from the BARE lunar surface (EME)")
print("  Lambertian reflection of albedo rho from a full-phase sphere:")
print("    N_det = rho * N_out * (A_tel / (pi D^2)) * QE")
for alb in (0.05, 0.072, 0.12, 0.20):
    nd_s = alb * N_OUT * (A_tel / (math.pi * D_EM ** 2)) * QE[0]
    print(f"    albedo {alb:.3f} -> {nd_s:.4f} photons detected per pulse"
          f"   ({n_det/nd_s:6.0f}x weaker than the array)")
geo_depth = (BEAM_W_MOON / 2.0) ** 2 / (2 * R_MOON)
print(f"\n  TIMING.  CAVEAT: a pulse width does not by itself bound timing")
print(f"  precision -- a clean symmetric pulse can be centroided well below its")
print(f"  own width given enough photons -- so the WIDTH below is a SUPPORTING")
print(f"  argument.  What makes the exclusion HARD is the photon deficit above.")
print(f"  {RRR_RESIDUAL*100:.0f} cm weighted-rms residual the round-trip must be")
print(f"  timed to dt = 2*dr/c = {2*RRR_RESIDUAL/C*1e12:.1f} ps.")
print(f"  The diffuse return is spread over the depth of the illuminated")
print(f"  footprint: geometric sagitta of a {BEAM_W_MOON/1000:.1f} km spot on a")
print(f"  sphere of R = {R_MOON/1e3:,.1f} km is {geo_depth:.2f} m, i.e. a")
print(f"  spread of 2*{geo_depth:.2f}/c = {2*geo_depth/C*1e9:.1f} ns, and any real")
print(f"  surface roughness makes this larger.  So the diffuse return is at")
print(f"  least {2*geo_depth/C/(2*RRR_RESIDUAL/C):,.0f}x broader than the timing resolution required for the")
print(f"  measured precision -- and the array return, from a target <1 m in")
print(f"  extent, is not.")
print("  => the detection that is actually made is >=50x brighter than the best")
print("     possible bare-surface return, which is what makes the exclusion HARD,")
print("     and ~300x broader in time than the required resolution, which is a")
print("     supporting point (a clean pulse can be centroided below its width).")
print("     A compact retroreflecting array at those coordinates supplies both.")

print("\nCROSS-CHECK: whose hardware is actually up there?")
print("  Verified from Wikipedia, 'List of retroreflectors on the Moon' and")
print("  'Lunar Laser Ranging experiments' -- all currently OPERATIONAL:")
print("    Apollo 11 LRRR   21 Jul 1969  0.6734 N 23.4731 E   46x46 cm  (USA)")
print("    Lunokhod 1       17 Nov 1970  38.3152 N 35.0080 W  44x19 cm  (USSR)")
print("    Apollo 14 LRRR   31 Jan 1971  3.6442 S 17.4786 W            (USA)")
print("    Apollo 15 LRRR   31 Jul 1971  26.1334 N 3.6285 E            (USA)")
print("    Lunokhod 2       15 Jan 1973  25.8323 N 30.9221 E           (USSR)")
print("    Chandrayaan-3    23 Aug 2023  69.3676 S 32.3481 E  5.11 cm  (India)")
print("  Three nations, six arrays, six decades, one shared measurement.")
print("  A faked Apollo programme would have to explain why the *Soviet* and")
print("  *Indian* arrays at independent coordinates return pulses at the same")
print("  stations, and why the Apollo array at 0.67 N / 23.47 E returns one too.")


# ===========================================================================
# B. SLEEP-PARALYSIS SUPPLY ARITHMETIC
# ===========================================================================
sect("B. Sleep paralysis: the supply of the requisite phenomenology")

print("VERIFIED BASE RATES (Wikipedia, 'Sleep paralysis')")
print(f"  lifetime prevalence   {SP_LIFETIME[0]*100:.0f}%-{SP_LIFETIME[1]*100:.0f}%")
print(f"  recurrent             ~{SP_RECURRENT*100:.0f}%")
print("  episode duration      1-6 minutes")
print("  canonical triad       intruder / incubus (chest pressure) /")
print("                       vestibular-motor ('floating', out-of-body)")
print("VERIFIED CLAIMANT POPULATIONS (Wikipedia, 'Alien abduction')")
print("  'One of the earliest studies of abductions found 1,700 claimants'")
print("  'contested surveys argued that 5-6 percent of the general population")
print("   allege to have been abducted'")

POP_WORLD = 8.1e9      # approximate, 2020s order of magnitude
POP_US = 3.4e8         # approximate, 2020s order of magnitude
for label, pop in (("world", POP_WORLD), ("United States", POP_US)):
    ever = pop * SP_LIFETIME[1]
    rec = pop * SP_RECURRENT
    print(f"\n  {label} (population taken as ~{pop:.1e}, approximate):")
    print(f"    will ever experience sleep paralysis  ~{ever:.2e} people")
    print(f"    experience it recurrently             ~{rec:.2e} people")
    for freq, lab in ((12, "1 episode/month"), (52, "1 episode/week"),
                      (1.0, "1 episode/year")):
        print(f"      at {lab:<15} -> {rec*freq:.2e} episodes/yr")

print(f"\n  Supply/demand ratio:")
print(f"    recurrent sleep-paralysis episodes per year (>= 1/yr) "
      f"{POP_WORLD*SP_RECURRENT:.2e}")
print(f"    documented abduction claimants                 {CLAIMANTS_LO:,}")
print(f"    ratio                                         "
      f"{POP_WORLD*SP_RECURRENT/CLAIMANTS_LO:,.0f}x")
print("  The known mundane mechanism over-supplies the phenomenology by ~5")
print("  orders of magnitude.  Nothing external is needed to produce it.")
print("  (Units caution: this divides episodes per YEAR by a CUMULATIVE claimant")
print("   count.  The like-for-like population figure -- 4.05e8 recurrent")
print("   sufferers vs 1,700 claimants, the same 238,235x -- is the honest")
print("   headline; the quoted ratio is conservative either way.)")

print("\n  A numerical coincidence worth flagging honestly:")
pct_survey = 0.055
print(f"    survey-implied abduction claims    5-6% of population")
print(f"    recurrent sleep-paralysis base rate ~{SP_RECURRENT*100:.0f}% of population")
print("    These are the same order of magnitude.  This is SUGGESTIVE, not")
print("    decisive: two ~5% figures can coincide, and neither survey is a")
print("    controlled measurement of the other.  It is reported as a pointer to")
print("    a test (polysomnography during reported events), not as a result.")


# ===========================================================================
# C. EXPECTED DETECTION RATE -- the gap the main artifact flagged
# ===========================================================================
sect("C. Expected detection rate: how surprising is the silence?")

print("MODEL.  Under the hypothesis H_A that n abductions were physical events,")
print("and that each such event independently leaves a verifiable independent")
print("record with probability p (photograph, video, radar track, medical")
print("record, third-party witness, physical trace), then")
print("    P(zero records in the entire history | H_A) = (1 - p)^n")
print("We solve for the p at which the observed silence has probability >= 5%,")
print("i.e. the largest p for which 'we found nothing' would still be the")
print("expected outcome.  Call it p*.")

N_CASES = [
    ("documented claimants, one early study", 1700),
    ("Bullard's comparative case set", 300),
    ("1% of the US population", 0.01 * POP_US),
    ("5% of the US population (low survey)", 0.05 * POP_US),
    ("6% of the US population (high survey)", 0.06 * POP_US),
    ("5% of world population", 0.05 * POP_WORLD),
]
print(f"\n  {'assumed number of events n':<42} {'p* (records/event)':>20} {'1/p*':>12}")
for lab, n in N_CASES:
    p_star = 1.0 - 0.05 ** (1.0 / n)
    print(f"  {lab:<42} {p_star:>20.3e} {1/p_star:>12,.0f}")

print("\n  Reading: for the silence to be unsurprising at the 5% level, every")
print("  physical abduction must have had LESS than a 1-in-568 chance of leaving")
print("  any record at all, if n is only the 1,700 documented claimants; and less")
print("  than a 1-in-135-million chance if the 5%-of-world survey figure is")
print("  right.  Those are the numbers the hypothesis has to survive.")

P_GRID = (1e-1, 1e-2, 1e-3, 1e-4, 1e-6)
print("\n  The same table, expressed as P(no record) for a fixed assumed p:")
hdr = f"  {'assumed number of events n':<42}" + "".join(f" {'p='+format(p,'.0e'):>12}" for p in P_GRID)
print(hdr)
for lab, n in N_CASES:
    cells = []
    for p in P_GRID:
        v = (1 - p) ** n
        cells.append(f"{v:13.2e}" if v > 1e-300 else "       <1e-300")
    print(f"  {lab:<42}" + "".join(cells))

print("\n  HONEST READING -- the concession is CONDITIONAL ON p, not categorical.")
print("  (An earlier draft said the argument 'carries only via the survey")
print("   figures'; the n=1,700 row of this very table refutes that.)")
print("   * n = 1,700 documented claimants, p = 1e-3: P(no record) = 18% -- the")
print("     silence is NOT surprising.  That is the weak case and it is conceded.")
print("   * n = 1,700, p = 1e-2: P(no record) = 4e-8 -- the silence IS surprising")
print("     on the documented count ALONE.")
print("   * Any survey-implied n (>= ~3e6) at any tabulated p >= 1e-6: P < 1e-7.")
print("  So the argument needs only the premise that a physical abduction has at")
print("  least a ~1-in-100 chance of leaving a verifiable record.  The contested")
print("  5-6% surveys strengthen it; they are not load-bearing for it.  The")
print("  genuinely uncertain quantity is p itself -- a judgement about how")
print("  recordable a physical event is, not a measurement.")

print("\n  THE DIRECTIONAL ARGUMENT, which does not depend on n at all:")
print("   Under H_A, P(no record) = (1-p)^n with p rising monotonically as")
print("   instrumentation per capita rises.  p in 1961 (Betty and Barney Hill):")
print("   no camera phones, no home video, no dashcams, no CCTV, no phones with")
print("   cameras, no always-on microphones.  p in 2026: a large fraction of")
print("   people sleep with a camera-equipped, always-networked computer in the")
print("   room.  Therefore under H_A the expected number of detections per")
print("   decade should have RISEN, by orders of magnitude.")
print("   Observed: the alleged incidence is reported to have declined from its")
print("   mid-1970s peak.  A physical phenomenon does not become less")
print("   recordable as recording devices improve.  The direction of the")
print("   trend is the test, and it runs opposite to the physical prediction.")


# ===========================================================================
# D. DATED CONTENT: the falsifiable content-stability test
# ===========================================================================
sect("D. Dated content: a prediction H_A makes and fails")

print("H_A (stable real phenomenon with stable content) predicts that the")
print("elements of the abduction narrative should appear at a roughly constant")
print("rate across all decades in which reports were collected, and should not")
print("track the publication history of a handful of authors.")
print("\nVerified from Wikipedia, 'Alien abduction':")
print("  * The 'grey' beings and the explicitly extraterrestrial framing entered")
print("    with the Betty and Barney Hill case (1961); 'purported abductions")
print("    were cited contemporaneously at least as early as 1954', and cases")
print("    before 1961 do not carry the later template.")
print("  * The 'child presentation' phase: 'Bullard says the child presentation")
print("    phase seems to be an innovation in the story [with] no clear")
print("    antecedents to descriptions of the child presentation phase exist")
print("    before its popularization by Hopkins and Jacobs' -- and Bullard,")
print("    studying ~300 reports, 'could not identify a child presentation")
print("    phase in the abduction narrative'.")
print("  * Hopkins began 'using hypnosis to extract more details' in the 1970s;")
print("    'Many alien abductees recall much of their alleged abduction(s)")
print("    through hypnosis'.")
print("\n  => A specific, dated element of the narrative has a birth date in the")
print("     literature that post-dates the earliest reports by 10-20 years and")
print("     coincides with the work of two named authors.  Under H_A this is a")
print("     failed prediction: the phase should be present throughout.")
print("\n  * Controlled emulation (2021, Int. J. Dream Research): volunteers were")
print("    instructed to emulate alien encounters by lucid dreaming.  114")
print("    volunteers (75% of the sample) succeeded; of those, ~20% produced")
print("    accounts rated close to reality in their absence of dreamlike")
print("    events, and only among that ~20% were sleep paralysis and fear")
print("    observed -- 'which are common in \"real\" stories'.")
print("    The phenomenology is therefore reproducible on demand, endogenously,")
print("    by ordinary people who were asked to.")

sect("END OF derivation3.py")
