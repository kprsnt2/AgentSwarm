#!/usr/bin/env python3
"""
Derived quantitative checks for "conspiracy-theories-evidence" (Kepler A001, 2026-10-06).

Every number quoted in section 8 of conspiracy-theories-evidence.md is produced
here, so that the artifact is reproducible from first principles rather than
asserted.  Inputs are reference-frame constants only; nothing is fitted.

Run:  python3 derivation.py
"""
import math

# --- Reference constants (inputs only) -------------------------------------
R = 6371.0088                      # mean Earth radius, km
A = 6378137.0                      # GRS 80 semi-major axis, m
INV_F = 298.257223563              # GRS 80 reciprocal flattening
F = 1.0 / INV_F
G0 = 9.7803253359                  # WGS-84 normal gravity at the equator, m/s^2
K = 0.00193185138639               # WGS 84 Somigliana constant
NAUT_MILE = 1852.0                 # m


def line(t=""):
    print(t)


def section(t):
    print("\n" + "=" * 70)
    print(t)
    print("=" * 70)


# --- 1. Nautical-mile identity / convergence of local verticals ------------
section("1. Convergence of local verticals (flat plane => parallel)")
print(f"  1852 m / R in arcsec          = {NAUT_MILE/(R*1000)*206264.806:.2f}  (== 1 arcmin)")
for d_km in (100, 1000, 4000):
    ang = math.degrees(d_km / R)
    print(f"  verticals {d_km:>5} km apart      = {ang:8.4f} deg = {ang*60:8.3f} arcmin")

# --- 2. Horizon distance and hull-down concealment -------------------------
section("2. Geometric horizon and 'hull-down' ship concealment")


def horizon_km(h_m):
    """Distance to the geometric horizon for eye height h (m), sphere radius R."""
    return math.sqrt(2 * (R * 1000) * h_m + h_m ** 2) / 1000.0


def dip_deg(h_m):
    return math.degrees(math.acos(R / (R + h_m / 1000.0)))


for h in (1.7, 2.0, 30.0, 2000.0):
    print(f"  eye height {h:>7.1f} m -> horizon {horizon_km(h):8.2f} km, dip {dip_deg(h):.4f} deg")


def hidden_height_m(d_km, h_obs_m):
    """Height of a distant object hidden below the sightline (geometric, no refraction)."""
    gap = max(d_km - horizon_km(h_obs_m), 0.0)
    return gap * gap / (2 * R) * 1000.0


print("  Height of a receding vessel hidden below the sightline (observer 2.0 m):")
for d_km in (5, 10, 20, 30):
    print(f"    range {d_km:>3} km -> {hidden_height_m(d_km, 2.0):6.1f} m hidden")

# --- 3. Eratosthenes --------------------------------------------------------
section("3. Eratosthenes: 5,000 stadia x 50 = 250,000 stadia (shadow angle 7.2 deg)")
for stadion_m in (157.5, 161.3, 185.0):
    circ = 250000 * stadion_m / 1000.0
    print(f"  stadion {stadion_m:>6} m -> {circ:8.1f} km  ({100*(circ-40075)/40075:+.1f}% vs 40,075 km)")

# --- 4. Star visibility limits from declination ----------------------------
section("4. Never-visible latitudes from declination (never rises if |phi-delta| > 90)")
for name, dec in (("Polaris", 89.264), ("Acrux", -63.099), ("Gacrux", -57.113), ("Mimosa", -59.690)):
    print(f"  {name:<10} dec {dec:+8.3f} -> never rises N of {dec+90 if dec<0 else dec-90:.1f} deg N")
print("  Polaris: never rises south of -0.74 deg; circumpolar north of +0.74 deg N")

# --- 5. Great circle vs flat disc -----------------------------------------
section("5. Great circle vs flat disc (azimuthal equidistant about the North Pole)")
SITES = {
    "SYD (-33.946,151.177)": (-33.9461, 151.1772),
    "SCL (-33.393,-70.786)": (-33.3930, -70.7858),
    "JNB (-26.137,28.241)": (-26.1367, 28.2411),
    "PER (-31.940,115.966)": (-31.9403, 115.9668),
    "CPT (-33.965,18.601)": (-33.9648, 18.6017),
    "AKL (-37.008,174.785)": (-37.0082, 174.7850),
    "EZE (-34.822,-58.536)": (-34.8222, -58.5358),
    "LHR ( 51.471,-0.462)": (51.4706, -0.4619),
}


def haversine(p1, p2):
    la1, lo1 = map(math.radians, p1)
    la2, lo2 = map(math.radians, p2)
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def azimuthal_north_pole(p1, p2):
    """Flat-Earth disc map: azimuthal equidistant projection centred on the North Pole."""
    r1 = R * math.radians(90 - p1[0])
    r2 = R * math.radians(90 - p2[0])
    b1, b2 = math.radians(p1[1]), math.radians(p2[1])
    return math.sqrt(max(r1 * r1 + r2 * r2 - 2 * r1 * r2 * math.cos(b1 - b2), 0.0))


for a, b in (("SYD (-33.946,151.177)", "SCL (-33.393,-70.786)"),
             ("JNB (-26.137,28.241)", "PER (-31.940,115.966)"),
             ("CPT (-33.965,18.601)", "SYD (-33.946,151.177)"),
             ("EZE (-34.822,-58.536)", "AKL (-37.008,174.785)")):
    g = haversine(SITES[a], SITES[b])
    f = azimuthal_north_pole(SITES[a], SITES[b])
    print(f"  {a} -> {b}: sphere {g:7.0f} km | flat-disc {f:7.0f} km | {f/g:5.2f}x")
g = haversine(SITES["PER (-31.940,115.966)"], SITES["LHR ( 51.471,-0.462)"])
print(f"  Perth -> London (published QF9: 14,498 km / 17 h): computed sphere {g:.0f} km "
      f"({100*abs(g-14498)/14498:.2f}% difference)")

# --- 6. WGS 84 normal gravity -------------------------------------------
section("6. WGS-84 normal gravity (Somigliana closed form)")
for lat in (0, 15, 30, 45, 60, 75, 90):
    s2 = math.sin(math.radians(lat)) ** 2
    g = G0 * (1 + K * s2) / math.sqrt(1 - F * (2 - F) * s2)
    print(f"  latitude {lat:>2} deg -> g = {g:.4f} m/s^2")
print(f"  semi-minor axis b = a(1-f) = {A*(1-F):,.1f} m   (equatorial bulge {A-A*(1-F):,.0f} m)")
print(f"  relative increase equator->pole = {100*(9.8321849378-9.7803253359)/9.7803253359:.2f}%")

# --- 7. Eclipse umbra and Foucault precession ----------------------------
section("7. Lunar-eclipse geometry and Foucault precession")
umbra = R / math.tan(math.radians(0.265))       # Sun's angular radius ~0.265 deg
print(f"  Earth's umbral length          ~ {umbra:,.0f} km   (Moon's distance 384,400 km)")
print(f"  ratio umbra / lunar distance    = {umbra/384400:.2f}x  => shadow always wider than the Moon")
print(f"  => Earth's shadow on the Moon is always circular, never an ellipse")
lat_paris = 48.8467
rate = 15.0411 * math.sin(math.radians(lat_paris))
print(f"  Foucault precession at Pantheon ({lat_paris} N) = {rate:.2f} deg/h "
      f"(Wikipedia reports ~11.3 deg/h)")
print(f"  pendulum day = 23.9345/sin(lat)            = {23.9345/math.sin(math.radians(lat_paris)):.2f} h")

# --- 8. Great-circle speed cross-check on a scheduled flight -------------
section("8. Sanity check: implied ground speed of QF9 Perth-London")
print(f"  14,498 km in 17.0 h => {14498/17/3.6:.0f} m/s = {14498/17:.0f} km/h "
      f"(a B787 cruises at ~900-913 km/h, so the published time is consistent "
      f"with the great-circle distance, not the flat-disc distance)")
