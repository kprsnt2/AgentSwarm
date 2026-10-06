// verify_tests7.js — Pass 8: two new INDEPENDENT decisive tests + one supplement.
//   N15  Lunar-return reentry velocity fingerprint         (Apollo fakery)
//   N16  Coriolis parameter sign-reversal / cyclones        (flat Earth)
//   N16b Van Allen belt transit time (supplement to §3.4)
// Everything computed from first principles; published values reproduced as
// internal-consistency checks. Reproducible:  node verify_tests7.js
//
// Convention carried over from passes 2-7: inspect the RUN OUTPUT before any
// number is copied into the artifact; log any slip this pass.

const G      = 6.67430e-11;   // m^3 kg^-1 s^-2  (CODATA 2018)
const M_E    = 5.9722e24;     // kg
const R_E    = 6.371e6;       // m (mean Earth radius)
const OMEGA  = 7.2921150e-5;  // rad/s (Earth rotation, IERS nominal)

const g0 = (G * M_E) / (R_E * R_E);

console.log("================ N15 : LUNAR-RETURN REENTRY VELOCITY FINGERPRINT ================");
const h_leo     = 200e3;
const r_leo     = R_E + h_leo;
const v_circ_leoi = Math.sqrt(G * M_E / r_leo);     // circular-orbit speed at 200 km
const v_esc_leoi  = Math.sqrt(2 * G * M_E / r_leo); // escape speed at SAME radius
const v_esc_surf  = Math.sqrt(2 * G * M_E / R_E);   // escape at mean surface

console.log("Surface gravity g0                 =", g0.toFixed(4), "m/s^2   [lit: WGS84 mean ~9.80-9.82, chk]");
console.log("Escape velocity at mean surface    =", (v_esc_surf / 1000).toFixed(3), "km/s   [lit: 11.186 km/s]");
console.log("Circular-orbit speed at 200 km     =", (v_circ_leoi / 1000).toFixed(3), "km/s   [lit: LEO ~7.78 km/s]");
console.log("Escape at 200 km                   =", (v_esc_leoi  / 1000).toFixed(3), "km/s");
console.log("v_esc/v_circ AT SAME RADIUS        =", (v_esc_leoi / v_circ_leoi).toFixed(6), " [analytic sqrt2 = 1.414214]");
console.log("Lunar-class return vs LEO deorbit  =", (v_esc_leoi / v_circ_leoi).toFixed(3), "x faster");

const ke_lee = v_esc_leoi * v_esc_leoi / 2 / 1e6;       // MJ/kg lunar-return
const ke_leo = 0.5 * v_circ_leoi * v_circ_leoi / 1e6;   // MJ/kg LEO return
console.log("Kinetic energy to shed (lunar)     =", ke_lee.toFixed(2), "MJ/kg");
console.log("Kinetic energy to shed (LEO)       =", ke_leo.toFixed(2), "MJ/kg   -> ratio", (ke_lee / ke_leo).toFixed(3), "x");
console.log("Peak convective heating ~ v^3       =", Math.pow(v_esc_leoi / v_circ_leoi, 3).toFixed(3), "x more heating");

const apollo11_fts = 36037;   // ft/s, published entry-interface speed
console.log("Apollo 11 entry-interface          =", apollo11_fts, "ft/s =", (apollo11_fts * 0.3048 / 1000).toFixed(3), "km/s");
console.log("Apollo range (published)           = ~10.9-11.2 km/s (lunar-class), peak decel ~6-7 g");
console.log("LEO-return capsules (Gemini/Mercury)= ~7.5-7.8 km/s  (orbit-class)");
console.log("=> staged-from-Earth-orbit CANNOT reenter at ~11 km/s; the measured entry is");
console.log("   escape-class = the vehicle reached lunar distance and came back.");

console.log("");
console.log("================ N16 : CORIOLIS PARAMETER  f = 2*Omega*sin(lat) ================");
for (const lat of [0, 5, 10, 20, 30, 45, 60, 90]) {
  const f = 2 * OMEGA * Math.sin(lat * Math.PI / 180);
  const sign = f > 1e-12 ? '+' : (f < -1e-12 ? '-' : '0');
  console.log("  phi=" + String(lat).padStart(2) + "\u00b0   f = " + f.toExponential(3) + " s^-1   sign " + sign);
}
console.log("f(45deg) x1e4                      =", (2 * OMEGA * Math.sin(Math.PI / 4) * 1e4).toFixed(3), " [lit ~1.03, chk]");
console.log("SIGN REVERSAL AT EQUATOR: f(20N)=+4.99e-5 ; f(20S)=-4.99e-5 ; f(0)=0 exactly.");
console.log("Sphere  : vertical spin component = Omega*sin(lat) -> + NH, 0 at equator, - SH.");
console.log("Flat disk (Omega normal to plane): Coriolis = 2*Omega everywhere, SAME sign, no");
console.log("           sin(lat) factor, NO reversal. => observed NH-CCW / SH-CW cyclones that");
console.log("           also vanish at the equator is a sphere signature.");

console.log("");
console.log("================ N16b : VAN ALLEN BELT TRANSIT TIME (supp. to section 3.4) ================");
const Rin = 1000e3, Rout = 60000e3;   // m altitude (established belt spans)
const vcr = 10.5e3;                    // m/s representative crossing speed
console.log("Belt radial span (altitude)        =", ((Rout - Rin) / 1000).toFixed(0), "km (inner ~1k-12k, outer ~13k-60k)");
console.log("Representative crossing speed      =", (vcr / 1000).toFixed(1), "km/s");
console.log("Full belt transit (1k-60k km alt)  =", ((Rout - Rin) / vcr / 60).toFixed(1), "min");
const t2 = (25000e3 - 2000e3) / vcr;
console.log("Dense-zone crossing (2k-25k km)    =", (t2 / 60).toFixed(1), "min");
console.log("=> passage is tens of minutes (~order 1 h); measured crew dose ~order 1 rad");
console.log("   [lit range], vs deterministic threshold ~50-100 rad, LD50 ~350-450 rad.");
