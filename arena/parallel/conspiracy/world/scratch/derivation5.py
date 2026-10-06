#!/usr/bin/env python3
"""
derivation5.py -- fifth pass, claim (a) Flat Earth and two flagged figures from pass 4.

Nothing here is fitted. Inputs are marked (V) = verified live in this session
against the named source, or (C) = standard constant.

Output: scratch/derivation5.out
"""
import math

AU   = 149597870.7      # (C) IAU astronomical unit, km
C    = 299792.458       # (C) speed of light, km/s
V_ORB = 29.78           # (C) Earth mean orbital speed, km/s
AS   = 206264.806       # arcsec per radian
PC   = 3.0857e13        # parsec, km
LY   = 9.4607e12        # light-year, km
MI   = 1.609344         # miles -> km
YEAR = 365.25 * 86400   # s

W = 78

def head(t):
    print("=" * W)
    print(t)
    print("=" * W)

# ----------------------------------------------------------------------
head("A. STELLAR PARALLAX AGAINST A NEARBY DOME (claim a, new decisive test)")

# (V) Wikipedia, "Proxima Centauri", body (Gaia Data Release 3, 2020):
#     "Based on a parallax of 768.0665 +/- 0.0499 mas ... Proxima Centauri is 4.2465 ly
#      (1.3020 pc) from the Sun."   The article's LEAD rounds this to "4.25 light-years
#      (1.3 parsecs)"; the body figures are the precise ones and are mutually consistent.
p_obs_mas = 768.0665
p_obs = p_obs_mas / 1000.0                  # arcsec
d_prox_pc = 1.3020
d_prox = d_prox_pc * PC
print("VERIFIED INPUTS (V)")
print("  parallax 768.0665 +/- 0.0499 mas  (Gaia DR3, 2020) = %.6f arcsec" % p_obs)
print("  distance 4.2465 ly = 1.3020 pc      d = %.4e km" % d_prox)
print("  cross-check 1/d[pc] = %.6f arcsec vs quoted %.6f -> %.3f%% (consistent)"
      % (1.0 / d_prox_pc, p_obs, 100 * ((1.0 / d_prox_pc) / p_obs - 1)))
print("  NOTE: this pass's first draft inverted the article's rounded LEAD (1.3 pc) to get")
print("        0.7692 arcsec and then built a 'the two expressions differ by 0.23%' note.")
print("        That 0.23% was an artefact of the rounding. The parallax is stated directly")
print("        in the body and is used below. 1 AU / 6371 km = 2.35e4.")
print()
print("  The flat-Earth model puts the stars on a nearby inner surface of a 'dome'.")
print("  Scanning every altitude quoted in that literature 1,000-10,000 miles:")
print()
print("  dome altitude      dome R (km)   predicted annual parallax (ALL stars)   excess over measured")
for mi in (1000, 3000, 5000, 7000, 10000):
    D = mi * MI
    pi = AU / D * AS                      # radians -> arcsec
    print("   %6d mi  %14.0f   %14.3e arcsec   %13.2e x" % (mi, D, pi, pi / p_obs))

d_need = AU / (p_obs / AS)                # km
print()
print("  Distance the dome would have to sit at to match the measured parallax:")
print("    d = AU/p = %.4e km = %.2f pc = %.2f ly" % (d_need, d_need / PC, d_need / LY))
print("    = %.3e x the 3,000-mile figure  (or %.3e x the 10,000-mile figure)"
      % (d_need / (3000 * MI), d_need / (10000 * MI)))
print()
print("  ORDERS OF MAGNITUDE, stated from the table, not asserted:")
excesses = [(AU / (mi * MI) * AS) / p_obs for mi in (1000, 3000, 5000, 7000, 10000)]
print("    smallest excess (10,000 mi dome) = %.3e = 10^%.1f" % (min(excesses), math.log10(min(excesses))))
print("    largest  excess ( 1,000 mi dome) = %.3e = 10^%.1f" % (max(excesses), math.log10(max(excesses))))
print("    => the exclusion is ~9 to 10.4 orders of magnitude in angle (NOT 8-10).")
print()
print("  WHY THIS IS DECISIVE, AND WHAT IT DOES NOT DEPEND ON")
print("  * On a single dome every star sits at essentially ONE distance, so ALL of them")
print("    would show the SAME ~1e9-1e10 arcsec annual swing. Measured: 0.768 arcsec for")
print("    the nearest star, a few tenths of an arcsecond for its nearest companions, and")
print("    vastly below 0.01 arcsec for the overwhelming majority of catalogued stars.")
print("    EVERY real parallax is 6 to 10 orders of magnitude below the dome prediction.")
print("    (An earlier draft said '<0.01 arcsec for every other star in the sky', which is")
print("     false: Alpha Centauri ~0.75\", Barnard's Star ~0.55\", Sirius ~0.38\". Softened.)")
print("  * The exclusion is 9-10.4 orders of magnitude in angle (see the computed block")
print("    below): no choice of dome altitude fixes it; 1,000 mi and 10,000 mi both fail")
print("    by the same margin. That robustness is what distinguishes this test from the")
print("  * The only free parameter is the parallax BASELINE. Getting 0.768 arcsec instead")
print("    of ~1e10 arcsec is a direct geometric measurement that Earth moves 1 AU.")
print("    A stationary plane has baseline = 0, hence ZERO annual parallax for every star.")
print("    Measured parallax is therefore positive proof of orbital motion, not merely")
print("    a value inconsistent with the dome. Precisely: the CONVENTIONAL parallax uses")
print("    the 1-AU baseline (a = 1 AU, the parsec definition), while the two six-month-")
print("    apart viewpoints are separated by the orbit's DIAMETER, 2a = 2 AU. An earlier")
print("    draft wrote 'the Earth moves a distance 2a = 1 AU over six months', which is a")
print("    factor-of-2 error and contradicted this section's own a = 1 AU definition.")

# ----------------------------------------------------------------------
head("B. STELLAR ABERRATION -- an independent measurement of the same orbit")

# (V) Wikipedia, "Aberration (astronomy)": the apparent position of a star "varies
#     periodically over the course of a year as the Earth's velocity changes as it
#     revolves around the Sun, by a maximum angle of approximately 20 arcseconds".
v_computed = 2 * math.pi * AU / YEAR      # km/s
print("VERIFIED INPUTS (V): annual aberration maximum '~20 arcseconds', of order v/c,")
print("  caused by Earth's revolution about the Sun  [Wikipedia, 'Aberration (astronomy)']")
print()
for lbl, v in (("mean orbital speed (quoted)", V_ORB),
               ("2*pi*AU/yr (computed here)", v_computed)):
    kap = v / C * AS
    print("  %-30s v = %7.3f km/s -> kappa = v/c = %.4e rad = %6.3f arcsec"
          % (lbl, v, v / C, kap))
print()
print("  predicted %.2f arcsec vs observed '~20 arcseconds'  -> agreement to better" % (V_ORB / C * AS))
print("  than the 3% implied by that rounding; the classical constant is ~20.5 arcsec.")
print("  NOTE ON THE COMPARISON: the source states the observation in round numbers,")
print("  so this is a 'predicted 20.49 against an observation quoted as about 20'")
print("  agreement, not a 0.1% test. It is nevertheless a two-significant-figure")
print("  prediction of a quantity that a stationary Earth must predict to be EXACTLY zero.")
print()
print("  Aberration is INDEPENDENT of parallax and the two separate cleanly:")
print("    - aberration depends only on observer VELOCITY, not on the star's distance;")
print("    - parallax depends only on baseline and distance.")
print("  Aberration is in phase with the orbit (period 1 year, 90 deg out of phase with")
print("  parallax), so it cannot be an artefact of the same geometry. Either alone")
print("  refutes a stationary plane; together they measure the orbit two ways.")
print()
print("  Third, independent signature of the same velocity -- annual Doppler shift:")
dl = V_ORB / C * 500.0
print("    dlambda/lambda = v/c = %.4e -> +/- %.4f nm at 500 nm (= +/- %.2f angstrom)"
      % (V_ORB / C, dl, dl * 10))
print("    observed to that precision in stellar spectra (standard astronomical practice).")

# ----------------------------------------------------------------------
head("B2. STELLAR ANGULAR SIZE AT DOME DISTANCE  (SUPPORTING point, not load-bearing)")

# (V) Wikipedia, "Betelgeuse": Michelson measured the angular diameter at 0.047 arcsecond
#     for a uniform disk ("limb darkening would increase the angular diameter by about
#     17%, hence 0.055 arcseconds"); infobox radius ~640 R_sun; dist 408 ly = 125 pc.
th = 0.047 / AS                             # radians, uniform disk
R_sun = 695700.0                            # km
print("VERIFIED INPUTS (V), Wikipedia, 'Betelgeuse':")
print("  angular diameter 0.047 arcsec (Michelson, uniform disk; 0.055 arcsec corrected")
print("    for limb darkening); radius ~640 R_sun; distance 125 pc (the article's body converts this to 410 ly)")
print()
print("  If that disc were at dome distance:")
for mi in (3000, 7000):
    D = mi * MI
    print("   at %5d mi: physical radius = %.2f m  (diameter %.2f m)"
          % (mi, th / 2 * D * 1000, th * D * 1000))
print()
print("  CROSS-CHECK that the two verified numbers are mutually consistent:")
for lbl, t_ in (("uniform disk 0.047\"", 0.047), ("limb-darkened 0.055\"", 0.055)):
    R_phys = 640 * R_sun
    d_impl = 2 * R_phys / (t_ / AS)         # km
    print("    implied distance from theta=%.3f\" and R=640 R_sun:  %.3e km = %.0f ly = %.0f pc"
          % (t_, d_impl, d_impl / LY, d_impl / PC))
print("    article's own distance: 408 ly = 125 pc  -> the 0.047\" uniform-disk value")
print("    reproduces it to %.1f%%. So the angular diameter and the radius are both real"
      % (100 * (2 * 640 * R_sun / (0.047 / AS)) / (408 * LY) - 100))
print("    measurements of a star hundreds of parsecs away, not a metre-scale lamp.")
print("  PROVENANCE FLAG: the article's own infobox carries parallax 5.95 mas (= 168 pc)")
print("    alongside dist 125 pc -- an internal inconsistency in the source: 168 pc vs")
print("    125 pc is 34.4% on the 125 pc base (the body also carries 410 ly for the 125 pc")
print("    track). It does not bear on this argument, since both values are hundreds of")
print("    parsecs, and 125 pc = %.2e km vs a 10,000-mile dome (1.61e4 km) is a factor of"
      % (125 * PC))
print("    %.1e -- i.e. 10^%.1f to 10^%.1f times further, NOT 10^13."
      % (125 * PC / (10000 * MI), math.log10(125 * PC / (10000 * MI)),
         math.log10(125 * PC / (1000 * MI))))
print("    An earlier draft wrote '~10^13 times further', which is high by ~1-2 orders.")
print("  LABEL: supporting. Assumes the interferometric angular diameters are real, which")
print("  a dome modeller can deny at some cost in other physics, so it is not the")
print("  load-bearing exclusion. Sections A and B carry that.")

# ----------------------------------------------------------------------
head("C. THE TWO FIGURES PASS 4 FLAGGED 'NOT VERIFIED IN THIS SESSION'")

# --- C1: intact-rock thermal conductivity -----------------------------
k_reg = 9.7 / 1000.0                        # W/(m.K): pass-4 DERIVED central value
print("C1. Intact-rock thermal conductivity, used only as a scale for derived regolith k.")
print("    Derived in pass 4: k_regolith = 8.5-11.3 mW/(m.K), central 9.7 mW/(m.K)")
print("    (V) Wikipedia, 'List of thermal conductivities', values read this session:")
rocks = [
    ("Stephens Basalt (NTS samples)", 1.36, 1.92),
    ("Barre Granite, dry, 50 bar", 2.1, 2.8),
    ("Barre Granite, all pressures to 5000 bar", 2.1, 4.5),
    ("Marble", 2.07, 2.94),
    ("pass-4 asserted 'intact igneous 2-4'", 2.0, 4.0),
]
print("    (Indiana Limestone was in the first draft at 0.62-1.33; the source table's")
print("     wikitext is ambiguous there and two different ranges sit in adjacent cells,")
print("     so the row is DROPPED rather than guessed at. It is sedimentary, a poor lunar")
print("     analogue anyway, and its removal does not change the igneous conclusion.)")
print("    %-42s %10s %12s" % ("rock", "W/(m.K)", "ratio vs regolith"))
for name, a, b in rocks:
    print("    %-42s %5.2f-%5.2f %6.0fx - %6.0fx" % (name, a, b, a / k_reg, b / k_reg))
print()
print("    FINDING: pass 4's '2-4 W/(m.K), ~300x less conductive' is FAIR inside that")
print("    band (206-412x) and the band is defensible for granite, but basalt - the")
print("    closest lunar analogue - measures 1.36-1.92, so the honest range across all")
print("    listed igneous/sedimentary rock is roughly 140x-460x less conductive.")
print("    Restated: 2-3 ORDERS OF MAGNITUDE, not 'about 300x'. Conclusion unchanged;")
print("    the '~300x' figure is now a range and the mechanism caveat from pass 4 stands.")

# --- C2: Earth vs Moon specific heat output ---------------------------
print()
print("C2. Earth's specific heat output, used in pass 4 only as a scale check.")
print("    (V) Wikipedia, 'Earth's internal heat budget': 'estimated at 47 +/- 2 terawatts';")
print("        'Estimates ... span a range of 43 to 49 terawatts'.")
qE, qE_lo, qE_hi = 47e12, 43e12, 49e12
mE, mM = 5.9722e24, 7.346e22
A_E = 4 * math.pi * (6371.0088e3) ** 2
print("    Earth total 47 +/- 2 TW  ->  range %d-%d TW" % (43, 49))
print("    Earth mean flux = 47e12 / %.4e m2 = %.1f mW/m2" % (A_E, qE / A_E * 1000))
print("      (article states 'an average heat flux of 91.6 mW/m2' -> matches)")
print("    Earth specific output = %.3e W/kg   (range %.2e - %.2e)"
      % (qE / mE, qE_lo / mE, qE_hi / mE))
qM = 6.4e11
print("    Moon total 6.4e11 W  (pass-4 DERIVED: 17 mW/m2 over 4piR^2 = 3.79e13 m2)")
print("    Moon specific output = %.3e W/kg" % (qM / mM))
print("      pass 4 wrote '8.8e-12' -> %s; and Earth '~8e-12' -> %s (now 7.9e-12)"
      % ("correct" if abs(qM / mM - 8.8e-12) < 0.2e-12 else "REVIEW",
         "correct" if abs(qE / mE - 8e-12) < 0.2e-12 else "REVIEW"))
print("    Earth/Moon ratio = %.2f -> same order of magnitude. Scale check only."
      % ((qE / mE) / (qM / mM)))
print("    FINDING: pass 4's Earth figure is confirmed (7.9e-12 W/kg, and 47 +/- 2 TW is")
print("    the right central value with a stated +/- 2 TW that pass 4 omitted). The Moon")
print("    figure is confirmed. Non-load-bearing, as pass 4 said.")

# ----------------------------------------------------------------------
head("D. CROSS-CHECK: do A and B disturb the earlier passes?")
print("  A and B are new tests for claim (a) only. They add a positive measurement of")
print("  Earth's orbital motion (parallax 0.77 arcsec, aberration ~20 arcsec) to a claim")
print("  section that previously refuted the flat plane only by *inconsistency*")
print("  (star fields, shadows, flights, pendulums). That matters: 'stationary plane' is")
print("  now excluded by a direct geometric measurement, not just by arithmetic")
print("  contradiction. Verdict for (a) is unchanged; the evidence class is stronger.")
print()
print("  One thing this pass does NOT do: it does not touch claims (b), (c) or (d),")
print("  whose arithmetic was already computed and audited in passes 3 and 4.")
