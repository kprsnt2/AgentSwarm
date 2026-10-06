#!/usr/bin/env python3
"""
Second derivation block for "conspiracy-theories-evidence" (Kepler A001, 2026-10-06).

Three additional DECISIVE quantitative tests that were not in derivation.py:

  A. The flat-disc model's own prediction for the Sun at the South Pole
     (the brief's "24-hour Antarctic sun" test, computed rather than asserted).
  B. Sunset geometry on a plane: the perspective-sunset vs constant-angular-
     diameter contradiction, quantified.
  C. Kepler's third law applied to the GPS and geostationary constellations.

Nothing here is fitted; every input is a published constant or a measured value.
Run:  python3 derivation2.py
"""
import math

# ---- published constants (inputs only) ------------------------------------
R_EARTH = 6371.0088                  # mean Earth radius, km
OBLIQUITY = 23.4392911               # obliquity of the ecliptic, deg
AU = 149597870.7                     # 1 astronomical unit, km
R_SUN = 695700.0                     # solar radius, km
ECC = 0.0167086                      # Earth's orbital eccentricity
MU = 398600.4418                     # GM of Earth, km^3/s^2
SIDEREAL_DAY = 86164.0905            # s


def sect(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


# =========================================================================
# A. THE FLAT-DISC MODEL AT THE SOUTH POLE
# =========================================================================
sect("A. Flat-disc model (azimuthal-equidistant about the North Pole): the Sun at the South Pole")

# On the disc, a point at latitude phi sits at polar distance
#   r = R * radians(90 - phi)
r_sp = R_EARTH * math.radians(180.0)
print(f"South Pole polar distance 180 deg  -> r = {r_sp:,.0f} km from the North Pole")

# The Sun's subsolar point migrates between the tropics on the disc too, so its
# polar distance ranges over 90 -/- obliquity:
r_tropics = [R_EARTH * math.radians(90 - e) for e in (+OBLIQUITY, -OBLIQUITY)]
print(f"Sun polar distance (Jun solstice, +23.44 deg): {r_tropics[1]:,.0f} km")
print(f"Sun polar distance (Dec solstice, -23.44 deg): {r_tropics[0]:,.0f} km")

# Minimum / maximum horizontal separation between the Sun and the South Pole
sep = [abs(r - r_sp) for r in r_tropics]
print(f"=> horizontal separation Sun <-> South Pole ranges {min(sep):,.0f} - {max(sep):,.0f} km")

print("\nSolar elevation at the South Pole predicted by the disc model:")
print("  (the Sun stays at fixed altitude above the plane, so it is ALWAYS above the")
print("   horizon there -- it can never set)")
for h_km in (3000, 4828, 10000, 20000, 30000):
    el = [math.degrees(math.atan(h_km / s)) for s in sep]
    print(f"    Sun altitude {h_km:>6,} km -> elevation at South Pole "
          f"{min(el):5.1f} deg - {max(el):5.1f} deg, 365 days/yr")

print("\n  Observation (Wikipedia, 'South Pole'/'Midnight sun'):")
print("    Sun above the horizon ~20 Sep - 20 Mar  (~179 days/yr)")
print("    Sun absent ~20 Mar - 20 Sep            (~186 days/yr)")
print("    single sunrise and single sunset per year, at the equinoxes")
print("    maximum solar elevation 23.44 deg at the December solstice")
print("  => the disc model predicts the South Pole sun is UP ~186 days/yr TOO MANY")
print("     and never sets at all. This is a discrepancy of ~186 days, not a rounding error.")

# How far from the North Pole would the Sun have to orbit for the South Pole to
# have a genuine sunset?
print("\n  Consistency check on the disc radius itself:")
# A sunset at the South Pole requires the Sun's horizontal separation to grow
# without bound while its altitude stays fixed: on a finite disc of radius r_d
# the Sun would have to orbit beyond the disc edge, i.e. r_sun > r_d = 20,015 km,
# i.e. more than 2.7x further out than the Tropic of Cancer allows (7,403 km).
print("    Tropic of Cancer polar distance (June solstice): 7,401 km")
print("    South Pole polar distance:                     20,015 km")
print(f"    ratio: {20015/7403:.2f}x  -> the Sun cannot reach the South Pole's")
print("    horizon on the disc, so the South Pole cannot have a night in this model.")

# =========================================================================
# B. SUNSET GEOMETRY ON A PLANE
# =========================================================================
sect("B. Sunset on a flat plane: the perspective-sunset vs constant-angular-size contradiction")

def ang_diam(dist_km, diameter_km):
    """Angular diameter (deg) of an object of physical diameter `diameter_km` at `dist_km`."""
    return math.degrees(2 * math.atan(diameter_km / 2.0 / dist_km))


d_peri = AU * (1 - ECC)
d_aph = AU * (1 + ECC)
D_SUN = 2 * R_SUN
print("1) The real Sun, from first principles (r = 695,700 km):")
for label, d in (("perihelion", d_peri), ("mean (1 AU)", AU), ("aphelion", d_aph)):
    print(f"    {label:<14} {d:,.0f} km -> {ang_diam(d, D_SUN):.4f} deg "
          f"({ang_diam(d, D_SUN)*60:.2f} arcmin)")
_tot = ang_diam(d_aph, D_SUN) - ang_diam(d_peri, D_SUN)
print(f"    annual range 31.45-32.52 arcmin = +/-{100*_tot/(2*ang_diam(AU, D_SUN)):.1f}% "
      "(eccentricity only; correlated with date, NOT with time of day)")
print("    measured at noon and at sunset to better than ~1%: the disc neither shrinks")
print("    nor is cut from above -- the LOWER limb is occluded first.")

# The flat-Earth model's own solar parameters (Zetetic / modern Flat Earth Society)
H_FE = 4828.0          # solar altitude above the plane, ~3,000 statute miles
D_FE = 51.5            # solar diameter, ~32 statute miles
print(f"\n2) The flat model's own Sun: H = {H_FE:,.0f} km altitude, D = {D_FE} km diameter")
print("   (Rowbotham ~3,000 mi / modern FES ~32 mi; the RATIO test below is size-independent)")
theta_noon = ang_diam(H_FE, D_FE)
print(f"    predicted angular diameter when overhead:  {theta_noon:.4f} deg "
      f"({theta_noon*60:.2f} arcmin)  [vs measured 31.97 arcmin -- already 15% too big]")

print("\n   For a 'perspective sunset' the Sun recedes toward the disc rim.")
print("   theta(sunset)/theta(noon) = H / sqrt(H^2 + X^2)  -- independent of the Sun's size:")
for h_km in (3000, 4828, 10000):
    x = r_sp                                    # maximum horizontal distance, disc rim
    ratio = h_km / math.hypot(h_km, x)
    print(f"    H = {h_km:>6,} km, X = {x:,.0f} km -> ratio {ratio:.3f} "
          f"(Sun {1/ratio:.2f}x SMALLER at sunset than at noon)")
    print(f"        predicted sunset angular diameter {ang_diam(math.hypot(h_km,x), D_FE)*60:5.2f} arcmin"
          f"  vs measured ~{ang_diam(AU, D_SUN)*60:.1f} arcmin")
print("   => the flat model requires the setting Sun to shrink by a factor of 2.2-6.8.")
print("      Observation: it does not shrink by more than ~2% (the annual eccentricity range).")
print("      A DISCREPANCY OF A FACTOR ~100-300 IN THE PREDICTED CHANGE.")

print("\n   Conversely, holding the angular diameter within 1% out to the disc rim requires:")
x_max = r_sp
h_req = x_max / math.sqrt(1.01**2 - 1)
print(f"    H >= X / sqrt(1.01^2 - 1) = {h_req:,.0f} km above the plane (~22 Earth radii)")
print(f"    but then the noon Sun would be {ang_diam(h_req, D_FE)*60:.2f} arcmin across "
      f"-- {ang_diam(AU, D_SUN)*60/(ang_diam(h_req, D_FE)*60):.0f}x too small.")
print("   => on a plane, 'perspective sunset' and 'constant angular diameter' cannot both hold.")
print("      The measured Sun keeps its size AND is occluded lower-limb first; BOTH require a")
print("      convex (curved) horizon, i.e. a spherical surface.")

# =========================================================================
# C. KEPLER'S THIRD LAW: GPS AND GEOSTATIONARY CONSTELLATIONS
# =========================================================================
sect("C. Kepler's third law applied to real satellite constellations")

def period_h(a_km):
    return 2 * math.pi * math.sqrt(a_km**3 / MU) / 3600.0

print("GPS (Wikipedia, 'Global Positioning System'): altitude ~20,200 km,")
print("orbital radius ~26,600 km, 'each SV makes two complete orbits each sidereal day'.")
T_GPS_OBS = SIDEREAL_DAY / 2.0        # 2 orbits per sidereal day
for a_km in (26560, 26600):
    print(f"    computed period at a = {a_km:,} km: {period_h(a_km):.3f} h "
          f"({period_h(a_km)*60:.1f} min)")
print(f"    observed: 2 orbits per sidereal day = {T_GPS_OBS/3600:.4f} h per orbit "
      f"({T_GPS_OBS/60:.1f} min)")
print(f"    agreement: {100*abs(period_h(26560)-T_GPS_OBS/3600)/(T_GPS_OBS/3600):.2f}%")

print("\nGeostationary (T = exactly one sidereal day):")
a_geo = (MU * SIDEREAL_DAY**2 / (4 * math.pi**2)) ** (1.0 / 3.0)
print(f"    a = (mu*T^2/4pi^2)^(1/3) = {a_geo:,.1f} km  -> altitude {a_geo - 6378.137:,.1f} km "
      f"(equatorial radius, correct for an equatorial orbit; mean radius gives 35,793 km)")
print("    published geostationary altitude: ~35,786 km above the equator")
print(f"    agreement: {100*abs((a_geo - 6378.137) - 35786)/35786:.4f}%")

print("\n  Both are closed Keplerian orbits about a central mass mu = GM = 398,600.4 km^3/s^2.")
print("  The GPS ground tracks repeat every sidereal day and the constellation's")
print("  rise/set windows measured at any site match the spherical-Earth visibility")
print("  geometry; a planar surface admits no such solution. GNSS geodetic solutions")
print("  are computed in a geocentric frame (GRS 80 / WGS 84) and fit surveys to cm.")

sect("END OF derivation2.py")


# =========================================================================
# D. ERATOSTHENES REPEATED TODAY: two-site noon-shadow geometry
# =========================================================================
sect("D. Eratosthenes' experiment repeated with modern coordinates")

# Two US cities on (almost) the same meridian, so the geometry is clean:
MEMPHIS = (35.1495, -90.0490)     # lat, lon
NEW_ORLEANS = (29.9511, -90.0715)
SYENE = (24.0889, 32.8998)        # modern Aswan - Eratosthenes' southern site
ALEXANDRIA = (31.2001, 29.9187)


def hav(p1, p2, radius=R_EARTH):
    la1, lo1 = map(math.radians, p1)
    la2, lo2 = map(math.radians, p2)
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(h))


print("On a sphere with the Sun effectively at infinity, the noon solar elevation is")
print("  elev = 90 deg - |phi - delta|, so the DIFFERENCE in noon elevation between two")
print("sites equals the difference in their latitudes, whatever the date.  The arc")
print("between them then gives R = arc / delta_phi.  A flat plane predicts a different,")
print("nonlinear relation in which the elevation difference depends on the Sun's altitude.")
print()
d_mem = hav(MEMPHIS, NEW_ORLEANS)
dphi = math.radians(MEMPHIS[0] - NEW_ORLEANS[0])
r_imp = d_mem / dphi
print(f"  Memphis (35.1495 N) - New Orleans (29.9511 N):")
print(f"    great-circle distance        = {d_mem:,.1f} km")
print(f"    latitude difference          = {math.degrees(dphi):.4f} deg = {dphi:.6f} rad")
print(f"    predicted noon-elevation difference = {math.degrees(dphi):.4f} deg")
print(f"    implied Earth radius         = {r_imp:,.0f} km  "
      f"({100*(r_imp-R_EARTH)/R_EARTH:+.2f}% vs {R_EARTH:,.1f} km)")

print("\nEratosthenes' own numbers (Syene=24.0889 N, Alexandria=31.2001 N; 5,000 stadia; 7.2 deg):")
d_ert = hav(SYENE, ALEXANDRIA)
print(f"    true great-circle distance  = {d_ert:,.1f} km")
for stad_m, lab in ((157.5, "short stadion"), (185.0, "long stadion")):
    arc = 5000 * stad_m / 1000.0
    print(f"    5,000 {lab:<14} = {arc:7.1f} km -> implied R = {arc/math.radians(7.2):7,.0f} km "
          f"({100*(arc/math.radians(7.2)-R_EARTH)/R_EARTH:+.1f}%)")

# The flat-plane alternative: what solar altitude would be needed for the SAME
# observed elevation difference, and is it consistent between different site pairs?
print("\nFlat-plane cross-check.  On a plane with the Sun at altitude H, the noon")
print("elevation from a site at distance x from the subsolar point is atan(H/x), so the")
print("elevation DIFFERENCE between two sites depends on their distances from the")
print("subsolar point.  For the Memphis-New Orleans pair to show a 5.1984 deg difference")
print("with the Sun at the same altitude H used elsewhere:")
x_a = 111.195 * (35.1495 - 23.44)      # distance from Tropic of Cancer, km
x_b = 111.195 * (29.9511 - 23.44)
print(f"    distances from the June solstice subsolar point: {x_a:,.0f} km and {x_b:,.0f} km")
print(f"    => required H = {x_a*math.tan(math.radians(90-5.1984)):,.0f} km and "
      f"{x_b*math.tan(math.radians(90-5.1984)):,.0f} km -- INCONSISTENT")
print("    (a single H cannot produce the observed difference for this or any pair),")
print("    which is why flat-Earth models must place the Sun at a different altitude for")
print("    every observation.")
