// ===== turn 7, focused re-derivation of the flagged items =====
const D2R = Math.PI / 180, R2D = 180 / Math.PI;
const c = 2.99792458e8, a = 6378.137, b = 6356.7523;
const Rkm = (2 * a + b) / 3, Rm = Rkm * 1000;
const RM = 1737.4, RS = 695700, DM = 384399, DS = 1.499844e8;

console.log('=== E-1  horizon dip per kilometre of horizon distance ===');
const dipDeg = h_m => Math.acos(Rm / (Rm + h_m)) * R2D;
const distKm = h_m => Math.sqrt(2 * Rm * h_m) / 1000;
for (const h of [2, 10, 11000, 20000, 400000]) {
  console.log(`  h=${String(h).padStart(7)} m  dist=${distKm(h).toFixed(3).padStart(9)} km  dip=${dipDeg(h).toFixed(5).padStart(9)} deg  = ${(dipDeg(h) * 60).toFixed(4)} arcmin`);
}
console.log(`  dip per km of horizon distance = ${(dipDeg(2) / distKm(2)).toFixed(5)} deg/km`);
console.log(`  drop over a 1 km baseline       = ${(1000 ** 2 / (2 * Rm)).toFixed(4)} m`);
console.log(`  ...as an angle at 1 km          = ${(1000 ** 2 / (2 * Rm) / 1000 * R2D).toFixed(5)} deg`);
console.log(`  [document said 0.0018 deg/km -> 5x too small]`);

console.log('\n=== E-6  Antarctic polar day (accurate solar declination) ===');
const obl = 23.4392911 * D2R;
const decOf = d => { // d = days since J2000
  const M = (357.5291 + 0.98560028 * d) * D2R;
  const lam = (280.466 + 0.9856474 * d + 1.914666471 * Math.sin(M) + 0.01999464 * Math.sin(2 * M)) * D2R;
  return Math.asin(Math.sin(obl) * Math.sin(lam)) * R2D;
};
// Jan 1 2000 12:00 TT = JD 2451545.0 -> doy N corresponds to d = N - 1.5
const doyToD = N => N - 1.5;
const cross = (target) => {
  const xs = [];
  for (let N = 1; N < 366; N += 0.002) {
    const d1 = decOf(doyToD(N)), d2 = decOf(doyToD(N + 0.002));
    if ((d1 < target) !== (d2 < target)) xs.push(N);
  }
  return xs;
};
const z0 = cross(0), z033 = cross(0.8333);
console.log('  declination = 0 crossings (doy):', z0.map(v => v.toFixed(2)).join(', '));
console.log('  declination = +0.8333 deg crossings (doy):', z033.map(v => v.toFixed(2)).join(', '));
const span = (x, y) => (y > x ? y - x : 365.25 - x + y);
console.log(`  south polar day, centre above TRUE horizon        = ${span(z0[1], z0[0]).toFixed(1)} days`);
console.log(`  south polar day, refraction(34') + semidiameter(16') = ${span(z033[1], z033[0]).toFixed(1)} days`);
let maxD = 0; for (let N = 1; N < 366; N += 0.001) maxD = Math.max(maxD, Math.abs(decOf(doyToD(N))));
console.log(`  max |declination| over the year = ${maxD.toFixed(4)} deg  -> Antarctic Circle = ${(90 - maxD).toFixed(4)} deg`);

console.log('\n=== E-4  Earth apparent diameter from the Moon ===');
for (const [lab, d] of [['perigee', 356400], ['mean', 384399], ['apogee', 406700]])
  console.log(`  ${lab.padEnd(7)}: ${(2 * 6378.137 / d * R2D).toFixed(3)} deg`);
console.log(`  [document used 1.83 deg, the apogee value; mean is 1.90 deg]`);

console.log('\n=== E-2/E-3  photographic exposure, done as a real exposure law ===');
// image-plane illuminance for an extended (Lambertian) object: E = rho*Esun/(4 N^2)
const Esun = 1.37e5;              // lx, solar illuminance at 1 AU [LIT]
const Nf = 11, fl = 60, lam = 555e-9, ASA = 160;
// film "correct exposure" H_m ~ C/ASA lx*s.  Calibrate against the two standard rules of thumb:
//   Sunny 16 (ISO 100, f/16, 1/100 s) on a sunlit 18%-grey surface at 1e5 lx
const EsunEarth = 1e5;
const Ef_sunny = 0.18 * EsunEarth / (4 * 16 ** 2);
const C_sunny = Ef_sunny * (1 / 100) * 100;          // lx*s at ISO 100
//   Looney 11 (full Moon, ISO 100, f/11, 1/100 s), full-Moon albedo 0.12
const Ef_looney = 0.12 * Esun / (4 * 11 ** 2);
const C_looney = Ef_looney * (1 / 100) * 100;
console.log(`  C (Sunny 16 anchor)  = ${C_sunny.toFixed(1)} lx*s at ISO 100`);
console.log(`  C (Looney 11 anchor) = ${C_looney.toFixed(1)} lx*s at ISO 100`);
for (const rho of [0.07, 0.12, 0.16]) {
  const Ef = rho * Esun / (4 * Nf ** 2);
  const tLo = (C_sunny / ASA) / Ef, tHi = (C_looney / ASA) / Ef;
  console.log(`  rho=${rho.toFixed(2)}  E_f=${Ef.toFixed(2).padStart(6)} lx  -> t = ${(1 / tHi).toFixed(0)}-${(1 / tLo).toFixed(0)} s^-1  (i.e. 1/${(1 / tHi).toFixed(0)} to 1/${(1 / tLo).toFixed(0)} s)`);
}
console.log(`  => correct regolith exposure at ASA 160, f/11 spans 1/100 s (rho=.07) to 1/410 s (rho=.16),`);
console.log(`     bracketing the flown Hasselblad settings 1/250-1/500 s.`);
console.log(`  [document's formula t = 1/(ASA*E) gives ${(1 / (ASA * (0.07 * Esun / (4 * Nf ** 2)))).toFixed(0)} s^-1 = 1/${(1 / (ASA * (0.07 * Esun / (4 * Nf ** 2)))).toFixed(0)} s, and mislabels it as 1/250-1/500 s]`);

// star: time to reach the SAME film density as a correct surface exposure
const Estar_lens = Esun * Math.pow(10, -(6 + 26.74) / 2.5);
const Ap = Math.PI * (fl / Nf / 2) ** 2 * 1e-6;
const Aairy = Math.PI * (1.22 * lam * Nf) ** 2;
const Ef_surf = 0.07 * Esun / (4 * Nf ** 2);
for (const [lab, Apsf] of [['Airy-limited', Aairy], ['aberrated 520 um2', 520e-12], ['aberrated 870 um2', 870e-12]]) {
  const Estar = Estar_lens * Ap / Apsf;
  const t1 = (C_sunny / ASA) / Estar, t2 = (C_looney / ASA) / Estar;
  console.log(`  mag-6 star, ${lab.padEnd(17)}: E_star=${Estar.toExponential(2)} lx  -> ${t1.toFixed(0)}-${t2.toFixed(0)} s to reach the surface's density`
    + `  (${Math.log2(Ef_surf / Estar).toFixed(1)} stops)`);
}
console.log(`  [document said 4.2 s; the correct range is ~75 s to ~6.8 min]`);

console.log('\n=== E-5  Apollo per-mission sample masses ===');
const A = [21.55, 34.35, 42.28, 76.74, 95.71, 110.52];
const B = [21.55, 33.45, 42.80, 76.74, 95.71, 110.52];
const s = x => x.reduce((p, q) => p + q, 0);
console.log(`  convention A sum = ${s(A).toFixed(2)} kg   (${(1 - s(A) / 382 * 100).toFixed(2)} % below 382 kg)`);
console.log(`  convention B sum = ${s(B).toFixed(2)} kg   (${(1 - s(B) / 382 * 100).toFixed(2)} % below 382 kg)`);
console.log(`  842 lb = ${842 * 0.45359237} kg`);
console.log(`  per-mission rounding at +/-0.005 kg over 6 missions = +/-${(6 * 0.005).toFixed(3)} kg  << far smaller than the 0.85 kg deficit`);
console.log(`  A12 conflict: |34.35-33.45| = 0.90 kg = ${(0.90 / 34.35 * 100).toFixed(2)} % of 34.35 kg   [document said <=1.3 % -> WRONG]`);
console.log(`  A14 conflict: |42.80-42.28| = 0.52 kg = ${(0.52 / 42.80 * 100).toFixed(2)} % of 42.80 kg`);

console.log('\n=== BFO dose margin ===');
console.log(`  A11 skin 0.18 rad, BFO ~40 % lower = 0.072 rad, margin to 50 rad MOD = ${(50 / 0.072).toFixed(0)}x`);
console.log(`  A14 skin 1.14 rad, BFO ~40 % lower = 0.456 rad, margin to 50 rad MOD = ${(50 / 0.456).toFixed(0)}x`);
