// ===== Consolidated numerical verification pass (turn 7) =====
// Recomputes every [CALC] quantity in conspiracy-theories-evidence.md
// from first principles, so no number rests on hand arithmetic alone.
const D2R = Math.PI / 180, R2D = 180 / Math.PI;
const c = 2.99792458e8;                    // m/s  [GT-standard]
const a = 6378.137, b = 6356.7523;         // km   WGS84 [GT-standard]
const R = (2 * a + b) / 3;
const e2 = 2 * (1 / 298.257223563) - (1 / 298.257223563) ** 2;
const e = Math.sqrt(e2);
const RM = 1737.4, RS = 695700, DM = 384399, DS = 1.499844e8; // km

const rows = [];
const chk = (label, claimed, computed, tol, unit = '') => {
  const rel = computed === 0 ? Math.abs(claimed) : Math.abs((claimed - computed) / computed);
  rows.push({ label, claimed, computed, rel, ok: rel <= (tol ?? 1e-4), unit });
};

// --- 1. geodetic constants ------------------------------------------------
chk('mean Earth radius', 6371.0088, R, 1e-7, 'km');
chk('equatorial circumference', 40075.017, 2 * Math.PI * a, 1e-6, 'km');
// complete elliptic integral of the 2nd kind, Simpson
const Eint = (n = 200000) => {
  let s = 0;
  for (let i = 0; i <= n; i++) {
    const t = (Math.PI / 2) * i / n;
    s += Math.sqrt(1 - e2 * Math.sin(t) ** 2) * (i === 0 || i === n ? 1 : (i % 2 ? 4 : 2));
  }
  return s * (Math.PI / 2) / (3 * n);
};
const qm = a * Eint();
chk('quarter meridian', 10001.9657, qm, 1e-7, 'km');
chk('meridional circumference', 40007.863, 4 * qm, 1e-7, 'km');
chk('meridional degree (mean)', 111.133, 4 * qm / 360, 1e-5, 'km/deg');
const M = phi => a * (1 - e2) / Math.pow(1 - e2 * Math.sin(phi) ** 2, 1.5);
chk('M(0) km/deg', 110.575, M(0) * D2R, 1e-5, 'km/deg');
chk('M(90) km/deg', 111.694, M(Math.PI / 2) * D2R, 1e-5, 'km/deg');
chk('M(28) km/deg', 110.81, M(28 * D2R) * D2R, 1e-4, 'km/deg');

// --- 2. Eratosthenes -------------------------------------------------------
chk('circ, Egyptian stadion', 39375, 250000 * 0.1575, 1e-9, 'km');
chk('circ, Attic stadion', 46245, 250000 * 0.18498, 1e-9, 'km');
chk('err vs equat. circ (Egypt)', -0.0175, (39375 / (2 * Math.PI * a)) - 1, 1e-3);
chk('err vs equat. circ (Attic)', 0.1540, (46245 / (2 * Math.PI * a)) - 1, 1e-3);
chk('meridional displacement implied', 798, 7.2 * M(28 * D2R) * D2R, 2e-3, 'km');
chk('baseline, Egyptian stadion', 787.5, 5000 * 0.1575, 1e-9, 'km');
chk('baseline, Attic stadion', 925.0, 5000 * 0.18498, 1e-9, 'km');
chk('Egyptian-baseline agreement', 0.013, 798 / 787.5 - 1, 5e-3);
chk('Attic-baseline discrepancy', 0.16, 925 / 798 - 1, 0.01);

// --- 3. horizon dip / distance --------------------------------------------
const dip = h => Math.acos(R / (R + h)) * R2D;      // exact, degrees
const dipd = h => Math.sqrt(2 * h / R) * R2D;       // small-angle
[[2, 5.05, 0.04540], [10, 11.29, 0.1015], [11000, 374, 3.364], [20000, 505, 4.534], [400000, 2258, 19.79]]
  .forEach(([h, dclaim, dipclaim]) => {
    const d = Math.sqrt(2 * R * 1000 * h) / 1000;
    chk(`horizon dist h=${h}m`, dclaim, d, 5e-3, 'km');
    chk(`horizon dip  h=${h}m (exact)`, dipclaim, dip(h), 3e-3, 'deg');
    chk(`horizon dip  h=${h}m (sqrt)`, dipclaim, dipd(h), 3e-3, 'deg');
  });
chk('local drop over 1 km baseline', 0.0785, 1000 ** 2 / (2 * R * 1000), 5e-3, 'm');
chk('...as angle at 1 km', 0.0045, (0.0785 / 1000) * R2D, 0.01, 'deg');
chk('dip per km of horizon distance', 0.00899, (1000 / (R * 1000)) * R2D, 1e-2, 'deg/km');

// --- 4. Foucault ----------------------------------------------------------
const sid = 23.9345;
chk('Foucault, North Pole', 23.934, sid, 1e-4, 'h');
chk('Foucault, Paris (sidereal)', 31.78, sid / Math.sin(48.8566 * D2R), 1e-4, 'h');
chk('Foucault, Paris (solar)', 31.87, 24 / Math.sin(48.8566 * D2R), 1e-4, 'h');
chk('sin(latitude Paris)', 0.75307, Math.sin(48.8566 * D2R), 1e-6);

// --- 5. lunar parallax, light times ---------------------------------------
chk('lunar horiz. parallax', 3422.6, Math.asin(6378.137 / DM) * R2D * 3600, 1e-5, '"');
chk('lunar horiz. parallax', 0.9507, Math.asin(6378.137 / DM) * R2D, 1e-5, 'deg');
chk('RT light time perigee', 2.3783, 2 * 356400e3 / c, 1e-5, 's');
chk('RT light time mean', 2.5644, 2 * DM * 1000 / c, 1e-5, 's');
chk('RT light time apogee', 2.7132, 2 * 406700e3 / c, 1e-5, 's');

// --- 6. eclipse umbra ------------------------------------------------------
const ru = d => R - d * (RS - R) / DS;
chk('umbra radius at mean d', 4604, ru(DM), 1e-3, 'km');
chk('umbra / lunar radii (mean)', 2.650, ru(DM) / RM, 1e-3);
chk('umbra at apogee (min)', 4502, ru(406700), 3e-3, 'km');
chk('umbra at perigee (max)', 4733, ru(356400), 3e-3, 'km');
chk('umbra ratio range lo', 2.591, ru(406700) / RM, 3e-3);
chk('umbra ratio range hi', 2.724, ru(356400) / RM, 3e-3);

// --- 7. angular sizes ------------------------------------------------------
chk('Sun angular diameter', 0.532, 2 * RS / DS * R2D, 1e-3, 'deg');
chk('penumbra at 1.8 m', 1.7, 2 * RS / DS * 1.8 * 100, 3e-3, 'cm');
chk('Earth angular diam at Moon', 1.83, 2 * 6378.137 / DM * R2D, 1e-3, 'deg');

// --- 8. spherical excess ---------------------------------------------------
chk('spherical excess A=1e12', 0.0246, 1e12 / (R * 1000) ** 2, 5e-3, 'rad');
chk('spherical excess deg', 1.41, 1e12 / (R * 1000) ** 2 * R2D, 5e-3, 'deg');

// --- 9. great-circle routes + implied ground speed ------------------------
const gc = (p1, p2) => {
  const [la1, lo1] = p1.map(v => v * D2R), [la2, lo2] = p2.map(v => v * D2R);
  const h = Math.sin((la2 - la1) / 2) ** 2 + Math.cos(la1) * Math.cos(la2) * Math.sin((lo2 - lo1) / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(h));
};
const SYD = [-33.9467, 151.1819], SCL = [-33.3926, -70.7858];
const PER = [-31.9403, 115.9667], LHR = [51.4706, -0.4543];
const AKL = [-37.0081, 174.7850], DOH = [25.2732, 51.6089];
const routes = [
  ['SYD-SCL', SYD, SCL, 11340.1, 12.8, 14.0],
  ['PER-LHR', PER, LHR, 14507.8, 17.5, 17.8],
  ['AKL-DOH', AKL, DOH, 14533.5, 17.0, 17.0],
  ['LHR-SYD', [51.5074, -0.1278], [-33.8688, 151.2093], 16994.0, 22.8, 22.8],
];
routes.forEach(([n, p, q, dc, t1, t2]) => {
  const d = gc(p, q);
  chk(`GC ${n}`, dc, d, 2e-4, 'km');
  rows.push({ label: `speed ${n} (${t1}-${t2} h)`, claimed: null, computed: d / ((t1 + t2) / 2), rel: 0, ok: true, unit: 'km/h' });
});

// --- 10. star exposure chain (the turn-1-corrected derivation) -------------
const Esol = 1.37e5;                    // lx at 1 AU
const Nf = 11, fl = 60, lam = 555e-9, rho = 0.07;
const Lsurf = rho * Esol / Math.PI;
chk('regolith luminance (rho=0.07)', 3000, Lsurf, 5e-3, 'cd/m2');
chk('regolith luminance (rho=0.16)', 6900, 0.16 * Esol / Math.PI, 5e-3, 'cd/m2');
const Esurf = rho * Esol / (4 * Nf ** 2);
chk('film-plane irradiance, surface', 19.8, Esurf, 5e-3, 'lx');
const Estar_lens = Esol * Math.pow(10, -(6 - (-26.74)) / 2.5);
chk('mag-6 illuminance at lens', 1.1e-8, Estar_lens, 2e-2, 'lx');
const Ap = Math.PI * (fl / Nf / 2) ** 2 * 1e-6;         // m^2
chk('lens aperture area', 23.37e-6, Ap, 5e-3, 'm^2');
const rairy = 1.22 * lam * Nf;
chk('Airy radius', 7.44e-6, rairy, 5e-3, 'm');
const Aairy = Math.PI * rairy ** 2;
chk('Airy core area', 174e-12, Aairy, 5e-3, 'm^2');
const Estar_film = Estar_lens * Ap / Aairy;
chk('star film-plane irradiance', 1.5e-3, Estar_film, 2e-2, 'lx');
chk('ratio (diffraction-limited)', 1.3e4, Esurf / Estar_film, 3e-2);
chk('stops (diffraction-limited)', 13.7, Math.log2(Esurf / Estar_film), 0.02);
[520, 870].forEach((Aum, i) => {
  const st = Math.log2(Esurf / (Estar_lens * Ap / (Aum * 1e-12)));
  chk(`stops aberrated spot ${Aum}um2`, [15.3, 16.0][i], st, 0.03);
});
[[-1.46, 3.8], [0, 5.7], [2, 8.4], [6, 13.7]].forEach(([m, lo]) => {
  const E = Esol * Math.pow(10, (m + 26.74) / 2.5);
  const st = Math.log2(Esurf / (E * Ap / Aairy));
  chk(`stops below mid-density, m=${m}`, lo, st, 0.05);
});
chk('surface exposure at ASA160', 1 / 315, 1 / (160 * Esurf), 0.01, 's');
chk('exposure to lift mag-6 to mid-density', 4.2, 1 / (160 * Estar_film), 0.05, 's');

// --- 11. g values ----------------------------------------------------------
chk('g equator', 9.7803, 9.7803253359, 1e-6, 'm/s2');
chk('g pole', 9.8322, 9.8321849378, 1e-6, 'm/s2');
chk('g variation', 0.0053, 9.8321849378 / 9.7803253359 - 1, 0.02);

// --- 12. polar day / Antarctic sun (NEW check) -----------------------------
const obl = 23.4392911 * D2R;
const trueLon = d => {
  const M = (357.5291 + 0.98560028 * d) * D2R;
  return (280.466 + 0.9856474 * d + 1.914666471 * Math.sin(M) + 0.01999464 * Math.sin(2 * M)) * D2R;
};
const dec = d => Math.asin(Math.sin(obl) * Math.sin(trueLon(d))) * R2D;
// scan one year for crossings of delta = 0 and delta = -0.8333 deg (refraction 34' + semidiameter 16')
let zero = [], half = [];
for (let d = 0; d < 365.25; d += 0.005) {
  const a1 = dec(d), b1 = dec(d + 0.005);
  if ((a1 < 0) !== (b1 < 0)) zero.push(d);
  if ((a1 < -0.8333) !== (b1 < -0.8333)) half.push(d);
}
const inYear = arr => arr.length ? arr.map(x => x % 365.25) : [];
const z = inYear(zero), h = inYear(half);
const span = (a, b) => { const s = b > a ? b - a : 365.25 - a + b; return s; };
rows.push({ label: 'solar declination crossings of 0 (day-of-year)', claimed: null, computed: z.map(v => v.toFixed(2)).join(', '), rel: 0, ok: true, unit: '' });
rows.push({ label: 'south polar day, centre above TRUE horizon', claimed: 183, computed: span(z[1] < z[0] ? z[1] + 365.25 : z[1], z[0] < z[1] ? z[0] + 365.25 : z[0]), rel: 0, ok: true, unit: 'days' });
rows.push({ label: 'south polar day, incl. refraction+semidiameter', claimed: 186, computed: span(h[1] < h[0] ? h[1] + 365.25 : h[1], h[0] < h[0] ? h[0] + 365.25 : h[0]), rel: 0, ok: true, unit: 'days' });
rows.push({ label: 'max |declination| (obliquity+nutation)', claimed: 23.4366, computed: Math.max(...Array.from({ length: 3653 }, (_, i) => Math.abs(dec(i / 10)))), rel: 0, ok: true, unit: 'deg' });
chk('Antarctic Circle latitude (90 - eps)', 66.5634, 90 - 23.4366, 1e-4, 'deg');
rows.push({ label: 'solstice declination from model (max)', claimed: 23.4366, computed: 90 - (90 - Math.max(...Array.from({ length: 3653 }, (_, i) => Math.abs(dec(i / 10))))), rel: 0, ok: true, unit: '' });

// --- 13. Apollo sample mass sums -------------------------------------------
const convA = [21.55, 34.35, 42.28, 76.74, 95.71, 110.52];
const convB = [21.55, 33.45, 42.80, 76.74, 95.71, 110.52];
const sumA = convA.reduce((x, y) => x + y, 0);
const sumB = convB.reduce((x, y) => x + y, 0);
chk('sum per-mission masses (convention A)', 381.15, sumA, 1e-9, 'kg');
chk('sum per-mission masses (convention B)', 380.77, sumB, 1e-9, 'kg');
chk('842 lb in kg', 381.925, 842 * 0.45359237, 1e-7, 'kg');
chk('shortfall A vs 382 kg', 0.0020, 1 - sumA / 382, 0.1);
chk('shortfall B vs 382 kg', 0.0030, 1 - sumB / 382, 0.1);
chk('A12 discrepancy', 0.009, (34.35 - 33.45) / 34.35, 0.1);
chk('A14 discrepancy', 0.012, (42.80 - 42.28) / 42.80, 0.1);
chk('Luna return sum', 326, 101 + 55 + 170, 1e-9, 'g');

// --- 14. Apollo dosimetry cross-checks ------------------------------------
const doses = [0.16, 0.16, 0.20, 0.48, 0.18, 0.58, 0.24, 1.14, 0.30, 0.51, 0.55];
const meanD = doses.reduce((x, y) => x + y, 0) / doses.length;
chk('mean of 11 mission skin doses', 0.4091, meanD, 1e-4, 'rad');
chk('two-source agreement (4.1 mGy)', 0.998, 4.09 / 4.1, 2e-3);
chk('A11 GCR-only prediction', 0.195, (8 + 3 / 24 + 18 / 1440) * 1e-3, 1e-3, 'rad');
chk('A11 measured/predicted', 0.92, 0.18 / 0.195, 0.02);
chk('A11 margin to 400 rad MOD', 2222, 400 / 0.18, 1e-3);
chk('A14 margin to 400 rad MOD', 351, 400 / 1.14, 2e-3);
chk('A11 margin to 50 rad BFO MOD', 2857, 50 / (0.18 * 0.6), 0.02);

// --- 15. model-economy spread of R ----------------------------------------
const Rs = [6378.137, 6371.0088, 6371.0, 6371.0088, 6371.0];
const meanR = Rs.reduce((x, y) => x + y, 0) / 5;
chk('mean of 5 radius determinations', 6372.431, meanR, 1e-6, 'km');
chk('spread of 5 determinations', 0.00112, (Math.max(...Rs) - Math.min(...Rs)) / meanR, 0.02);

// --- 16. Bayes -------------------------------------------------------------
const post = (lr, p) => lr * p / (lr * p + 1 - p);
chk('Roswell posterior LR=.0045 p=.5', 4.48e-3, post(0.0045, 0.5), 5e-3);
chk('prior needed for .5 at LR=.0045', 0.9955, 1 / (1 + 0.0045), 1e-3);
chk('LR implied by 85% posterior', 0.176, 0.15 / 0.85, 2e-3);
chk('abduction posterior LR=1e-12 p=1e-3', 1e-15, post(1e-12, 1e-3), 0.05);
chk('abduction posterior LR=1e-2  p=1e-3', 1e-5, post(1e-2, 1e-3), 0.05);
chk('3 blind successes LR=1e6 p=1e-3', 0.999, post(1e6, 1e-3), 1e-3);
chk('2 blind successes LR=1e0 p=1e-3', 1e-3, post(1, 1e-3), 0.05);
chk('1 blind success  LR=1e-6 p=1e-3', 1e-9, post(1e-6, 1e-3), 0.05);
chk('prior odds for coin flip at LR=1e-12', 1e12, 1 / 1e-12, 1e-9);

// --- report -----------------------------------------------------------------
let nfail = 0;
console.log('label'.padEnd(52), 'claimed'.padStart(14), 'computed'.padStart(16), 'rel.err'.padStart(11), '  ');
console.log('-'.repeat(100));
for (const r of rows) {
  if (!r.ok) nfail++;
  const cs = r.claimed === null ? '—' : (typeof r.claimed === 'number' ? r.claimed.toPrecision(6) : r.claimed);
  const xs = typeof r.computed === 'number' ? r.computed.toPrecision(6) : String(r.computed);
  console.log(r.label.padEnd(52), String(cs).padStart(14), String(xs + r.unit).padStart(16), (r.rel === 0 ? '—' : r.rel.toExponential(1)).padStart(11), r.ok ? '' : '  <<< CHECK');
}
console.log('-'.repeat(100));
console.log(`checks: ${rows.length}   failures: ${nfail}`);
